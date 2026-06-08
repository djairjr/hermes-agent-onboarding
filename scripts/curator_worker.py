#!/usr/bin/env python3
"""
curator_worker.py — Async consolidation worker for the agent identity curator.

Runs as a cron job via `hermes cron create --schedule "every 5m" --script curator_worker.py --no-agent`.
Pure Python, no LLM — zero token cost.

Operations (run on each tick):
  1. PATTERN CONSOLIDATION — group similar tool calls, create/update tech_kb entries
  2. CHECKPOINT UPDATE — auto-create checkpoints for active sessions with discoveries
  3. EMBEDDING REFINEMENT — detect near-duplicate faults and tech_kb entries
  4. AGENT REPRESENTATION — regenerate static cache hourly
  5. DEPRECATED ENTRY DETECTION — find stale, deprecated, low-signal entries

Output: summarized as stdout. Empty stdout = silent (nothing to report).
"""

import json
import logging
import os
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
import psycopg2.extras
import requests

# ---------------------------------------------------------------------------
# Config (matches curator plugin config)
# ---------------------------------------------------------------------------
PG_HOST = os.environ.get("PGVECTOR_HOST", "localhost")
PG_PORT = int(os.environ.get("PGVECTOR_PORT", "5433"))
PG_DB = os.environ.get("PGVECTOR_DB", "openbrain")
PG_USER = os.environ.get("PGVECTOR_USER", "postgres")
PG_PASS = os.environ.get("PGVECTOR_PASS", "4ut0l1b3r4c40")

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/embed")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "nomic-embed-text-v2-moe")

# Thresholds
PATTERN_SIMILARITY = 0.85       # cluster tool calls this similar into a pattern
DEDUP_FAULT_SIMILARITY = 0.95   # faults this similar -> suggest merge
PATTERN_MIN_COUNT = 3            # minimum tool calls to form a pattern
TECHKB_MATCH_THRESHOLD = 0.85   # pattern already exists in tech_kb? skip

# Agent representation
REPRESENTATION_REGEN_INTERVAL = 3600  # seconds (1 hour)

# ---------------------------------------------------------------------------
# JSON encoder that handles Decimal and datetime
# ---------------------------------------------------------------------------
class _JSONEncoder(json.JSONEncoder):
    """Custom encoder that handles types from pgvector RealDictCursor."""
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


def _safe_json(obj):
    """Serialize to JSON, safely handling Decimal/datetime types."""
    return json.dumps(obj, cls=_JSONEncoder)


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("curator_worker")


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------
def get_conn():
    return psycopg2.connect(host=PG_HOST, port=PG_PORT,
                            user=PG_USER, password=PG_PASS, dbname=PG_DB)


def make_embedding(text: str) -> Optional[List[float]]:
    if not text or not text.strip():
        return None
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": EMBED_MODEL, "input": str(text)[:8000],
        }, timeout=30)
        r.raise_for_status()
        return r.json()["embeddings"][0]
    except Exception as e:
        logger.warning("embedding error: %s", e)
        return None


# ---------------------------------------------------------------------------
# Operation 1: Pattern Consolidation
# ---------------------------------------------------------------------------
def consolidate_patterns(conn) -> List[str]:
    """Group unprocessed tool call logs by similarity and create/update tech_kb entries."""
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Fetch unprocessed tool calls
    cur.execute("""
        SELECT id, tool_name, tool_args, result_summary, success, duration_ms, session_id
        FROM agent_identity.tool_call_log
        WHERE processed = false
        ORDER BY occurred_at ASC
        LIMIT 500
    """)
    rows = cur.fetchall()

    if not rows:
        cur.close()
        return []

    # Generate or fetch embeddings
    tool_texts = {}
    for r in rows:
        key = str(r["id"])
        text = f"{r['tool_name']} | {json.dumps(r['tool_args'], sort_keys=True, default=str)}"
        emb = make_embedding(text)
        if emb:
            tool_texts[key] = emb

    if not tool_texts:
        # Mark as processed anyway so we don't retry endlessly
        cur.execute("""
            UPDATE agent_identity.tool_call_log SET processed = true
            WHERE processed = false
        """)
        conn.commit()
        cur.close()
        return []

    # Group by similarity via pgvector
    groups = []
    assigned = set()

    for r in rows:
        rid = str(r["id"])
        if rid in assigned:
            continue

        emb = tool_texts.get(rid)
        if not emb:
            continue

        cur2 = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur2.execute("""
            SELECT id, tool_name, session_id
            FROM agent_identity.tool_call_log
            WHERE id != %s::uuid
              AND embedding IS NOT NULL
              AND 1 - (embedding <=> %s::vector) >= %s
            ORDER BY embedding <=> %s::vector
            LIMIT 20
        """, (rid, emb, PATTERN_SIMILARITY, emb))
        similar = cur2.fetchall()
        cur2.close()

        group_ids = [rid] + [str(s["id"]) for s in similar]
        assigned.update(group_ids)
        groups.append({
            "ids": group_ids,
            "tool_names": set([r["tool_name"]] + [s["tool_name"] for s in similar]),
            "sessions": set([r["session_id"]] + [s["session_id"] for s in similar]),
        })

    # Mark all processed
    cur.execute("""
        UPDATE agent_identity.tool_call_log SET processed = true
        WHERE id = ANY(%s)
    """, (list(assigned),))

    # Create tech_kb entries for groups >= PATTERN_MIN_COUNT
    reports = []
    for g in groups:
        if len(g["ids"]) < PATTERN_MIN_COUNT:
            continue

        tool_names = ", ".join(sorted(g["tool_names"]))

        pattern_text = f"tool pattern: {tool_names}"
        pattern_emb = make_embedding(pattern_text)
        if not pattern_emb:
            continue

        cur.execute("""
            SELECT id, name
            FROM agent_identity.tech_knowledge_base
            WHERE tags::jsonb ? 'tool-pattern'
              AND embedding IS NOT NULL
              AND 1 - (embedding <=> %s::vector) >= %s
            ORDER BY embedding <=> %s::vector
            LIMIT 1
        """, (pattern_emb, TECHKB_MATCH_THRESHOLD))
        existing = cur.fetchone()

        if existing:
            logger.info("pattern already exists: %s (%s)", existing["name"], existing["id"])
            continue

        synthesis = (
            f"Pattern detected: {len(g['ids'])} similar tool calls "
            f"across {len(g['sessions'])} sessions. "
            f"Tools: {tool_names}."
        )

        cur.execute("""
            INSERT INTO agent_identity.tech_knowledge_base
                (name, category, content, tags, status, embedding)
            VALUES (%s, %s, %s, %s, %s, %s::vector)
            RETURNING id
        """, (
            f"Pattern: {tool_names[:80]}",
            "pattern",
            _safe_json({"synthesis": synthesis, "tool_count": len(g["ids"]), "session_count": len(g["sessions"])}),
            json.dumps(["tool-pattern", "consolidated"]),
            "active",
            pattern_emb,
        ))
        new_id = cur.fetchone()[0]
        reports.append(f"pattern created: {new_id} -- {tool_names[:60]}")

    conn.commit()
    cur.close()
    return reports


# ---------------------------------------------------------------------------
# Operation 2: Checkpoint Update
# ---------------------------------------------------------------------------
def update_checkpoints(conn) -> List[str]:
    """Create auto-checkpoints for sessions with recent discoveries."""
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT session_id, tool_name, count(*) as call_count
        FROM agent_identity.tool_call_log
        WHERE occurred_at > NOW() - INTERVAL '30 minutes'
        GROUP BY session_id, tool_name
        ORDER BY session_id, call_count DESC
    """)
    session_tools = cur.fetchall()

    if not session_tools:
        cur.close()
        return []

    sessions = defaultdict(list)
    for r in session_tools:
        sessions[r["session_id"]].append(r)

    reports = []
    for session_id, tools in sessions.items():
        if not tools:
            continue

        cur.execute("""
            SELECT id FROM agent_identity.session_checkpoints
            WHERE session_id = %s AND status = 'pendente' AND deleted_at IS NULL
        """, (session_id,))
        existing = cur.fetchone()
        if existing:
            continue

        cur.execute("""
            SELECT count(*) FROM agent_identity.tech_knowledge_base
            WHERE created_at > NOW() - INTERVAL '30 minutes'
        """)
        new_kb = cur.fetchone()[0]

        cur.execute("""
            SELECT count(*) FROM agent_identity.identity_faults
            WHERE created_at > NOW() - INTERVAL '30 minutes'
        """)
        new_faults = cur.fetchone()[0]

        if new_kb == 0 and new_faults == 0:
            continue

        top_tool = tools[0]["tool_name"]
        territory = f"Auto-checkpoint: {top_tool} session"
        discovery_text = f"{new_kb} tech_kb entries, {new_faults} faults registered"
        emb = make_embedding(f"{territory} | {discovery_text}")
        if not emb:
            cur.close()
            continue

        cur.execute("""
            INSERT INTO agent_identity.session_checkpoints
                (session_id, territory, operating_mode, vector_intent,
                 discovery, consolidated_insights, occurred_at, status, next_step,
                 embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s::vector)
            RETURNING id
        """, (
            session_id,
            territory,
            "diagnostico",
            f"Auto-consolidate session {session_id}",
            discovery_text,
            f"Worker detected {new_kb} new tech_kb entries and {new_faults} new faults in session.",
            datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "pendente",
            "Review consolidated patterns via curator_worker.",
            emb,
        ))
        new_cp = cur.fetchone()[0]
        reports.append(f"auto-checkpoint: {new_cp} -- {territory}")

    conn.commit()
    cur.close()
    return reports


# ---------------------------------------------------------------------------
# Operation 3: Embedding Refinement (Dedup)
# ---------------------------------------------------------------------------
def refine_embeddings(conn) -> List[str]:
    """Detect near-duplicate faults and tech_kb entries, flag for review."""
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    reports = []

    cur.execute("""
        SELECT id, fault_type, symptom
        FROM agent_identity.identity_faults
        WHERE embedding IS NOT NULL
        ORDER BY created_at DESC
        LIMIT 100
    """)
    faults = cur.fetchall()

    for i, f1 in enumerate(faults):
        for f2 in faults[i + 1:]:
            cur2 = conn.cursor()
            cur2.execute("""
                SELECT 1 - (a.embedding <=> b.embedding)::float AS sim
                FROM agent_identity.identity_faults a, agent_identity.identity_faults b
                WHERE a.id = %s AND b.id = %s
            """, (f1["id"], f2["id"]))
            row = cur2.fetchone()
            cur2.close()
            if row and row[0] >= DEDUP_FAULT_SIMILARITY:
                reports.append(
                    f"near-duplicate faults: {str(f1['id'])[:8]} ({f1['fault_type'][:30]}) "
                    f"<-> {str(f2['id'])[:8]} ({f2['fault_type'][:30]}) sim={row[0]:.2f}"
                )

    cur.execute("""
        SELECT id, name
        FROM agent_identity.tech_knowledge_base
        WHERE tags::jsonb ? 'tool-pattern'
          AND embedding IS NOT NULL
        ORDER BY created_at DESC
        LIMIT 100
    """)
    patterns = cur.fetchall()

    for i, p1 in enumerate(patterns):
        for p2 in patterns[i + 1:]:
            cur2 = conn.cursor()
            cur2.execute("""
                SELECT 1 - (a.embedding <=> b.embedding)::float AS sim
                FROM agent_identity.tech_knowledge_base a, agent_identity.tech_knowledge_base b
                WHERE a.id = %s AND b.id = %s
            """, (p1["id"], p2["id"]))
            row = cur2.fetchone()
            cur2.close()
            if row and row[0] >= DEDUP_FAULT_SIMILARITY:
                reports.append(
                    f"near-duplicate patterns: {str(p1['id'])[:8]} ({p1['name'][:30]}) "
                    f"<-> {str(p2['id'])[:8]} ({p2['name'][:30]}) sim={row[0]:.2f}"
                )

    cur.close()
    return reports


# ---------------------------------------------------------------------------
# Operation 4: Agent Representation (cache, regenerated hourly)
# ---------------------------------------------------------------------------
def regenerate_representation(conn) -> Optional[str]:
    """Regenerate the agent_representation cache table."""
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT version, generated_at FROM agent_identity.agent_representation
        ORDER BY version DESC LIMIT 1
    """)
    latest = cur.fetchone()
    if latest:
        elapsed = (datetime.now(timezone.utc) - latest["generated_at"]).total_seconds()
        if elapsed < REPRESENTATION_REGEN_INTERVAL:
            cur.close()
            return None

    cur.execute("""
        SELECT milestone_type, title, created_at
        FROM agent_identity.identity_milestones
        ORDER BY created_at DESC LIMIT 10
    """)
    milestones = [dict(r) for r in cur.fetchall()]

    cur.execute("""
        SELECT name, capability_type, description
        FROM agent_identity.agent_capabilities
        WHERE status = 'active'
        ORDER BY created_at DESC
    """)
    capabilities = [dict(r) for r in cur.fetchall()]

    cur.execute("""
        SELECT fault_type, severity, countermeasure
        FROM agent_identity.identity_faults
        WHERE severity >= 4
        ORDER BY severity DESC
        LIMIT 15
    """)
    common_faults = [dict(r) for r in cur.fetchall()]

    cur.execute("""
        SELECT operating_mode,
               count(*) AS checkpoints,
               sum((token_usage->>'input')::bigint) FILTER (WHERE token_usage IS NOT NULL) AS total_input,
               sum((token_usage->>'output')::bigint) FILTER (WHERE token_usage IS NOT NULL) AS total_output
        FROM agent_identity.session_checkpoints
        WHERE token_usage IS NOT NULL
        GROUP BY operating_mode
        ORDER BY total_input DESC NULLS LAST
    """)
    token_summary = [dict(r) for r in cur.fetchall()]

    payload = {
        "milestones": milestones,
        "capabilities": capabilities,
        "common_faults": common_faults,
        "token_summary": token_summary,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    text_for_embed = (
        f"Agent with {len(capabilities)} capabilities, "
        f"{len(common_faults)} active faults, "
        f"{len(milestones)} milestones. "
        f"Operating modes: {', '.join(t['operating_mode'] for t in token_summary)}"
    )
    emb = make_embedding(text_for_embed)

    next_version = (latest["version"] + 1) if latest else 1
    payload_json = _safe_json(payload)

    if latest:
        cur.execute("""
            INSERT INTO agent_identity.agent_representation
                (version, generated_at, payload, model_used, embedding)
            VALUES (%s, now(), %s, %s, %s::vector)
        """, (next_version, payload_json, 'nomic-embed-text-v2-moe', emb))
    else:
        cur.execute("""
            INSERT INTO agent_identity.agent_representation
                (version, generated_at, payload, model_used, embedding)
            VALUES (%s, now(), %s, %s, %s::vector)
        """, (next_version, payload_json, 'nomic-embed-text-v2-moe', emb))

    conn.commit()
    cur.close()
    return (f"representation regenerated: version {next_version}, "
            f"{len(capabilities)} caps, {len(common_faults)} faults, {len(milestones)} milestones")


# ---------------------------------------------------------------------------
# Operation 5: Deprecated Entry Detection
# ---------------------------------------------------------------------------
def detect_deprecated(conn) -> List[str]:
    """Find deprecated, stale, or near-duplicate entries across all identity tables."""
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    reports = []

    # 5a. tech_kb entries with 'deprecated' tag or stale
    cur.execute("""
        SELECT id, name, category, created_at, updated_at
        FROM agent_identity.tech_knowledge_base
        WHERE tags::jsonb ? 'deprecated'
           OR name ILIKE '%deprecated%'
           OR (status = 'active' AND updated_at IS NOT NULL AND updated_at < NOW() - INTERVAL '60 days')
    """)
    for r in cur.fetchall():
        reports.append(
            f"deprecated tech_kb: {str(r['id'])[:8]} ({r['name'][:50]}) "
            f"cat={r['category']} last_update={r.get('updated_at','?')}"
        )

    # 5b. Stale pending checkpoints (older than 7 days, no recent activity)
    # Exclude deliberate long-term tests (stress-test, ongoing, periodic tags)
    cur.execute("""
        SELECT cp.id, cp.territory, cp.occurred_at, cp.session_id
        FROM agent_identity.session_checkpoints cp
        LEFT JOIN agent_identity.tool_call_log tcl ON tcl.session_id = cp.session_id
            AND tcl.occurred_at > NOW() - INTERVAL '2 days'
        WHERE cp.status = 'pendente'
          AND cp.deleted_at IS NULL
          AND cp.occurred_at < NOW() - INTERVAL '7 days'
          AND NOT (cp.tags @> ARRAY['stress-test'])
          AND NOT (cp.tags @> ARRAY['ongoing'])
          AND NOT (cp.tags @> ARRAY['periodic'])
          AND tcl.id IS NULL
        ORDER BY cp.occurred_at ASC
    """)
    for r in cur.fetchall():
        reports.append(
            f"stale checkpoint: {str(r['id'])[:8]} ({r['territory'][:50]}) "
            f"since {r['occurred_at']}"
        )

    # 5c. Old completed checkpoints (30+ days) — validate value before archiving
    # Soft-delete only if they generated milestones, capabilities, or tech_kb entries.
    # Queue wasted checkpoints (no value generated) for user review.
    cur.execute("""
        SELECT cp.id, cp.territory, cp.occurred_at, cp.session_id,
               EXISTS (SELECT 1 FROM agent_identity.identity_milestones WHERE session_id = cp.session_id) AS has_milestones,
               EXISTS (SELECT 1 FROM agent_identity.tech_knowledge_base WHERE created_at::date = cp.occurred_at) AS has_tech_kb
        FROM agent_identity.session_checkpoints cp
        WHERE cp.status = 'concluida'
          AND cp.deleted_at IS NULL
          AND cp.occurred_at < NOW() - INTERVAL '30 days'
        ORDER BY cp.occurred_at ASC
    """)
    old = cur.fetchall()
    for r in old:
        if r['has_milestones'] or r['has_tech_kb']:
            # Generated value — safe to soft-delete
            cur.execute("""
                UPDATE agent_identity.session_checkpoints
                SET deleted_at = now()
                WHERE id = %s
            """, (r['id'],))
            reports.append(
                f"archived checkpoint (value extracted): {str(r['id'])[:8]} ({r['territory'][:40]}) {r['occurred_at']}"
            )
        else:
            # No value generated — queue for user review
            cur.execute("""
                INSERT INTO agent_identity.curator_review_queue
                    (entry_type, entry_id, description)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                'wasted_checkpoint',
                r['id'],
                f"Checkpoint '{r['territory'][:80]}' ({r['occurred_at']}) concluded with no milestones or tech_kb entries. Potential waste pattern."
            ))
            reports.append(
                f"wasted checkpoint (no value): {str(r['id'])[:8]} ({r['territory'][:40]}) {r['occurred_at']}"
            )

    # 5d. Potentially stale capabilities (90+ days without update)
    cur.execute("""
        SELECT id, name, created_at
        FROM agent_identity.agent_capabilities
        WHERE status = 'active'
          AND created_at < NOW() - INTERVAL '90 days'
        ORDER BY created_at ASC
        LIMIT 20
    """)
    for r in cur.fetchall():
        reports.append(
            f"potentially stale capability: {str(r['id'])[:8]} {r['name'][:40]} since {r['created_at']}"
        )

    # 5e. Low-signal faults (severity < 4, older than 30 days)
    cur.execute("""
        SELECT id, fault_type, severity, created_at
        FROM agent_identity.identity_faults
        WHERE severity < 4
          AND created_at < NOW() - INTERVAL '30 days'
        ORDER BY created_at ASC
        LIMIT 10
    """)
    low = cur.fetchall()
    for r in low:
        reports.append(
            f"low-signal fault (sev={r['severity']}): {str(r['id'])[:8]} {r['fault_type'][:40]} from {r['created_at']}"
        )
    if len(low) > 10:
        reports.append(f"... and {len(low)-10} more low-signal faults")

    cur.close()
    return reports


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    reports = []
    start = time.time()

    try:
        conn = get_conn()

        pattern_reports = consolidate_patterns(conn)
        reports.extend(pattern_reports)

        cp_reports = update_checkpoints(conn)
        reports.extend(cp_reports)

        dedup_reports = refine_embeddings(conn)
        reports.extend(dedup_reports)

        rep_report = regenerate_representation(conn)
        if rep_report:
            reports.append(rep_report)

        dep_reports = detect_deprecated(conn)
        reports.extend(dep_reports)

        conn.close()

    except Exception as e:
        logger.error("worker failed: %s", e)
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    elapsed = time.time() - start

    if reports:
        print(f"curator_worker tick ({elapsed:.1f}s):")
        for r in reports:
            print(f"  * {r}")
    # else: silent


if __name__ == "__main__":
    main()