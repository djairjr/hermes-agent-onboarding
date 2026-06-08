"""pgvector queries for the curator plugin."""

import json
import logging
from typing import Any, Dict, List, Optional

import psycopg2
import psycopg2.extras
import requests

from . import config

logger = logging.getLogger(__name__)


def get_connection():
    """Return a connection to the local pgvector instance."""
    return psycopg2.connect(
        host=config.PG_HOST,
        port=config.PG_PORT,
        user=config.PG_USER,
        password=config.PG_PASS,
        dbname=config.PG_DB,
    )


def make_embedding(text: str) -> Optional[List[float]]:
    """Generate embedding via local Ollama."""
    if not text or not text.strip():
        return None
    try:
        r = requests.post(
            config.OLLAMA_URL,
            json={"model": config.EMBED_MODEL, "input": str(text)[:8000]},
            timeout=5,
        )
        r.raise_for_status()
        return r.json()["embeddings"][0]
    except Exception as e:
        logger.debug("embedding error: %s", e)
        return None


def search_faults(embedding: List[float], threshold: Optional[float] = None, limit: int = 3) -> List[Dict]:
    """Search identity_faults for similar entries. First match is the best."""
    if threshold is None:
        threshold = config.FAULT_THRESHOLD
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT id, fault_type, symptom, countermeasure, severity,
                   1 - (embedding <=> %s::vector) AS similarity
            FROM agent_identity.identity_faults
            WHERE embedding IS NOT NULL
              AND 1 - (embedding <=> %s::vector) >= %s
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (embedding, embedding, threshold, embedding, limit))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        logger.warning("fault search failed: %s", e)
        return []


def search_checkpoints(embedding: List[float], threshold: Optional[float] = None, limit: int = 3) -> List[Dict]:
    """Search concluded session_checkpoints for similar context."""
    if threshold is None:
        threshold = config.CP_THRESHOLD
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT id, territory, discovery, consolidated_insights, next_step,
                   1 - (embedding <=> %s::vector) AS similarity
            FROM agent_identity.session_checkpoints
            WHERE embedding IS NOT NULL
              AND status = 'concluida'
              AND deleted_at IS NULL
              AND 1 - (embedding <=> %s::vector) >= %s
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (embedding, embedding, threshold, embedding, limit))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        logger.warning("checkpoint search failed: %s", e)
        return []


def search_tech_kb(embedding: List[float], threshold: Optional[float] = None, limit: int = 3) -> List[Dict]:
    """Search tech_knowledge_base for similar entries."""
    if threshold is None:
        threshold = config.TECHKB_THRESHOLD
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT id, name, category, content,
                   1 - (embedding <=> %s::vector) AS similarity
            FROM agent_identity.tech_knowledge_base
            WHERE embedding IS NOT NULL
              AND 1 - (embedding <=> %s::vector) >= %s
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (embedding, embedding, threshold, embedding, limit))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        logger.warning("tech_kb search failed: %s", e)
        return []


def log_tool_call(occurred_at, session_id, tool_name, tool_args, result_summary,
                   success, duration_ms, fault_ref=None, checkpoint_ref=None):
    """Insert a tool call record into tool_call_log."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"""
            INSERT INTO {config.TOOL_CALL_LOG_TABLE}
                (occurred_at, session_id, tool_name, tool_args, result_summary,
                 success, duration_ms, fault_ref, checkpoint_ref, embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s::vector)
        """, (
            occurred_at, session_id, tool_name,
            json.dumps(tool_args) if isinstance(tool_args, dict) else tool_args,
            str(result_summary)[:500] if result_summary else None,
            success, duration_ms,
            fault_ref, checkpoint_ref,
            None,  # embedding computed async by worker
        ))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logger.warning("tool call log failed: %s", e)
