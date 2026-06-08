#!/usr/bin/env python3
"""
identity_db.py — helper de acesso ao pgvector local (agent_identity schema)

Centraliza toda a conexão com o PostgreSQL local para a camada de
identidade agêntica. Skills consultam via este módulo, não via REST.

Modos de uso:
  python3 identity_db.py faults           → lista faults severity >= 4
  python3 identity_db.py capabilities     → lista capabilities ativas
  python3 identity_db.py milestones       → lista milestones recentes
  python3 identity_db.py checkpoints      → lista checkpoints pendentes
  python3 identity_db.py search <table> <query>  → busca semântica
"""
import json, os, sys
import psycopg2
import psycopg2.extras
import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
LOCAL_HOST = os.environ.get("PGVECTOR_HOST", "localhost")
LOCAL_PORT = int(os.environ.get("PGVECTOR_PORT", "5433"))
LOCAL_DB = os.environ.get("PGVECTOR_DB", "openbrain")
LOCAL_USER = os.environ.get("PGVECTOR_USER", "postgres")
LOCAL_PASS = os.environ.get("PGVECTOR_PASS", "4ut0l1b3r4c40")

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/embed")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "nomic-embed-text-v2-moe")

# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------
def connect():
    return psycopg2.connect(
        host=LOCAL_HOST, port=LOCAL_PORT,
        user=LOCAL_USER, password=LOCAL_PASS,
        dbname=LOCAL_DB
    )

# ---------------------------------------------------------------------------
# Embedding
# ---------------------------------------------------------------------------
def make_embedding(text):
    if not text or text.strip() == "":
        return None
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": EMBED_MODEL,
            "input": str(text)[:8000]
        }, timeout=30)
        r.raise_for_status()
        return r.json()["embeddings"][0]
    except Exception as e:
        print(f"[embedding error] {e}", file=sys.stderr)
        return None

# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------
def query_faults(severity_min=4, limit=10, semantic=None):
    """
    Active identity faults with countermeasures.
    Se semantic=None for fornecido, busca por similaridade de embedding.
    Caso contrário, filtra por severity_min.
    """
    conn = connect()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    if semantic is not None:
        emb = make_embedding(semantic)
        if emb:
            cur.execute("""
                SELECT id, fault_type, symptom, root_cause, blocks, countermeasure,
                       severity, evidence_session, created_at,
                       1 - (embedding <=> %s::vector)::float AS similarity
                FROM agent_identity.identity_faults
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, (emb, emb, limit))
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return rows
    
    cur.execute("""
        SELECT id, fault_type, symptom, root_cause, blocks, countermeasure,
               severity, evidence_session, created_at
        FROM agent_identity.identity_faults
        WHERE severity >= %s
        ORDER BY severity DESC, created_at DESC
        LIMIT %s
    """, (severity_min, limit))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def query_capabilities(status="active", limit=20):
    """Active agent capabilities."""
    conn = connect()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT name, capability_type, description, origin, status, created_at
        FROM agent_identity.agent_capabilities
        WHERE status = %s
        ORDER BY created_at DESC
        LIMIT %s
    """, (status, limit))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def query_milestones(limit=5):
    """Recent identity milestones."""
    conn = connect()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT milestone_type, title, description, significance, created_at
        FROM agent_identity.identity_milestones
        ORDER BY created_at DESC
        LIMIT %s
    """, (limit,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def query_checkpoints(status="pendente", limit=5, semantic=None):
    """
    Pending session checkpoints.
    Se semantic for fornecido, busca por similaridade de embedding.
    Caso contrário, filtra por status.
    """
    conn = connect()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    if semantic:
        emb = make_embedding(semantic)
        if emb:
            cur.execute("""
                SELECT id, session_id, territory, operating_mode, vector_intent,
                       discovery, consolidated_insights, next_step, status,
                       occurred_at, domain_scope, tags,
                       1 - (embedding <=> %s::vector)::float AS similarity
                FROM agent_identity.session_checkpoints
                WHERE embedding IS NOT NULL AND deleted_at IS NULL
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, (emb, emb, limit))
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return rows
    
    cur.execute("""
        SELECT id, session_id, territory, operating_mode, vector_intent,
               discovery, consolidated_insights, next_step, status,
               occurred_at, domain_scope, tags
        FROM agent_identity.session_checkpoints
        WHERE status = %s AND deleted_at IS NULL
        ORDER BY occurred_at DESC
        LIMIT %s
    """, (status, limit))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# ---------------------------------------------------------------------------
# Updates
# ---------------------------------------------------------------------------
def update_checkpoint(cp_id, updates):
    """
    Atualiza campos parciais de um checkpoint existente.
    Só envia UPDATE para os campos fornecidos em 'updates'.
    Se 'embedding' não for fornecido, recalcula automaticamente.
    Retorna o id do checkpoint.
    """
    if not cp_id:
        raise ValueError("cp_id é obrigatório para update_checkpoint")

    allowed = {"session_id", "session_title", "territory", "domain_scope",
               "operating_mode", "vector_intent", "target_capabilities",
               "discovery", "pattern_recognized", "consolidated_insights",
               "legacy_refs", "occurred_at", "status", "project", "client",
               "next_step", "blocker", "tags", "capability_refs", "fault_refs",
               "milestone_refs", "decisions", "value_amount", "value_currency",
               "deleted_at", "working_dir", "repo_path",
               "model", "provider", "token_usage"}

    valid_updates = {k: v for k, v in updates.items() if k in allowed}
    if not valid_updates:
        raise ValueError("Nenhum campo válido para atualizar")

    conn = connect()
    cur = conn.cursor()

    # Recalcular embedding se houver mudança em campos semânticos
    if not any(k in valid_updates for k in ("embedding",)):
        semantic_keys = ["territory", "vector_intent", "discovery",
                         "consolidated_insights", "next_step"]
        if any(k in valid_updates for k in semantic_keys):
            # Buscar estado atual para compor embedding completo
            cur.execute("""
                SELECT territory, vector_intent, discovery
                FROM agent_identity.session_checkpoints WHERE id = %s
            """, (cp_id,))
            current = cur.fetchone()
            if current:
                emb_text = " | ".join(
                    str(valid_updates.get(k, current[i])) 
                    for i, k in enumerate(["territory", "vector_intent", "discovery"])
                    if valid_updates.get(k, current[i])
                )
                emb = make_embedding(emb_text)
                if emb:
                    valid_updates["embedding"] = emb

    set_clause = ", ".join(f"{k} = %s" for k in valid_updates.keys())
    values = list(valid_updates.values()) + [cp_id]

    # Se embedding está nos valores, precisamos do cast ::vector
    if "embedding" in valid_updates:
        set_clause = ", ".join(
            f"{k} = %s::vector" if k == "embedding" else f"{k} = %s"
            for k in valid_updates.keys()
        )

    cur.execute(f"""
        UPDATE agent_identity.session_checkpoints
        SET {set_clause}, updated_at = now()
        WHERE id = %s
    """, values)

    if cur.rowcount == 0:
        conn.rollback()
        cur.close()
        conn.close()
        raise ValueError(f"Checkpoint {cp_id} não encontrado")

    conn.commit()
    cur.close()
    conn.close()
    return cp_id


def close_checkpoint(cp_id, consolidated_insights=None):
    """
    Atalho para marcar um checkpoint como concluído.
    Se consolidated_insights for fornecido, atualiza também.
    """
    updates = {"status": "concluida"}
    if consolidated_insights:
        updates["consolidated_insights"] = consolidated_insights
    return update_checkpoint(cp_id, updates)


def update_fault(fault_id, updates):
    """
    Atualiza campos parciais de um fault existente.
    Retorna o id do fault.
    """
    if not fault_id:
        raise ValueError("fault_id é obrigatório para update_fault")

    allowed = {"fault_type", "symptom", "root_cause", "blocks",
               "evidence_session", "evidence_quote", "refs",
               "countermeasure", "severity"}

    valid_updates = {k: v for k, v in updates.items() if k in allowed}
    if not valid_updates:
        raise ValueError("Nenhum campo válido para atualizar")

    conn = connect()
    cur = conn.cursor()

    # Recalcular embedding se houver mudança em campos semânticos
    if not any(k in valid_updates for k in ("embedding",)):
        semantic_keys = ["fault_type", "symptom", "countermeasure"]
        if any(k in valid_updates for k in semantic_keys):
            cur.execute("""
                SELECT fault_type, symptom, countermeasure
                FROM agent_identity.identity_faults WHERE id = %s
            """, (fault_id,))
            current = cur.fetchone()
            if current:
                emb_text = " | ".join(
                    str(valid_updates.get(k, current[i]))
                    for i, k in enumerate(["fault_type", "symptom", "countermeasure"])
                    if valid_updates.get(k, current[i])
                )
                emb = make_embedding(emb_text)
                if emb:
                    valid_updates["embedding"] = emb

    set_clause = ", ".join(
        f"{k} = %s::vector" if k == "embedding" else f"{k} = %s"
        for k in valid_updates.keys()
    )
    values = list(valid_updates.values()) + [fault_id]

    cur.execute(f"""
        UPDATE agent_identity.identity_faults
        SET {set_clause}
        WHERE id = %s
    """, values)

    if cur.rowcount == 0:
        conn.rollback()
        cur.close()
        conn.close()
        raise ValueError(f"Fault {fault_id} não encontrado")

    conn.commit()
    cur.close()
    conn.close()
    return fault_id


# ---------------------------------------------------------------------------
# Inserts
# ---------------------------------------------------------------------------
def insert_fault(fault_data):
    """Insert a new identity fault. Uses gen_random_uuid() if no id."""
    conn = connect()
    cur = conn.cursor()

    emb_text = " | ".join(str(fault_data.get(k, "")) for k in ["fault_type", "symptom", "countermeasure"] if fault_data.get(k))
    emb = make_embedding(emb_text)
    fault_id = fault_data.get("id")

    if fault_id:
        cur.execute("""
            INSERT INTO agent_identity.identity_faults
                (id, fault_type, symptom, root_cause, blocks,
                 evidence_session, evidence_quote, countermeasure,
                 severity, embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s::vector)
            ON CONFLICT (id) DO UPDATE SET
                fault_type=EXCLUDED.fault_type,
                severity=EXCLUDED.severity,
                countermeasure=EXCLUDED.countermeasure
        """, (
            fault_id, fault_data.get("fault_type"), fault_data.get("symptom"),
            fault_data.get("root_cause"), fault_data.get("blocks", []),
            fault_data.get("evidence_session"), fault_data.get("evidence_quote"),
            fault_data.get("countermeasure"), fault_data.get("severity", 5), emb
        ))
    else:
        cur.execute("""
            INSERT INTO agent_identity.identity_faults
                (fault_type, symptom, root_cause, blocks,
                 evidence_session, evidence_quote, countermeasure,
                 severity, embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::vector)
            RETURNING id
        """, (
            fault_data.get("fault_type"), fault_data.get("symptom"),
            fault_data.get("root_cause"), fault_data.get("blocks", []),
            fault_data.get("evidence_session"), fault_data.get("evidence_quote"),
            fault_data.get("countermeasure"), fault_data.get("severity", 5), emb
        ))
        fault_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return fault_id

def insert_checkpoint(cp_data):
    """Insert a new session checkpoint. Uses gen_random_uuid() if no id provided.
    If session_id is not provided, attempts to read from HERMES_SESSION_ID environment
    variable for automatic linking with Hermes session store."""
    conn = connect()
    cur = conn.cursor()

    # Auto-fill session_id from env if not provided
    if not cp_data.get("session_id"):
        hermes_sid = os.environ.get("HERMES_SESSION_ID")
        if hermes_sid:
            cp_data["session_id"] = hermes_sid

    emb_text = " | ".join(str(cp_data.get(k, "")) for k in ["territory", "vector_intent", "discovery"] if cp_data.get(k))
    emb = make_embedding(emb_text)
    cp_id = cp_data.get("id")

    if cp_id:
        cur.execute("""
            INSERT INTO agent_identity.session_checkpoints
                (id, session_id, session_title, territory, domain_scope,
                 operating_mode, vector_intent, discovery, consolidated_insights,
                 occurred_at, status, next_step, tags, decisions,
                 model, provider, target_capabilities, pattern_recognized,
                 legacy_refs, project, client, blocker,
                 capability_refs, fault_refs, milestone_refs,
                 value_amount, value_currency, working_dir, repo_path,
                 token_usage,
                 embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s,
                    %s::vector)
            ON CONFLICT (id) DO UPDATE SET
                status=EXCLUDED.status,
                next_step=EXCLUDED.next_step,
                consolidated_insights=EXCLUDED.consolidated_insights,
                model=EXCLUDED.model,
                provider=EXCLUDED.provider
        """, (
            cp_id, cp_data.get("session_id"), cp_data.get("session_title"),
            cp_data.get("territory"), cp_data.get("domain_scope", []),
            cp_data.get("operating_mode"), cp_data.get("vector_intent"),
            cp_data.get("discovery"), cp_data.get("consolidated_insights"),
            cp_data.get("occurred_at"), cp_data.get("status", "pendente"),
            cp_data.get("next_step"), cp_data.get("tags", []),
            json.dumps(cp_data.get("decisions", [])),
            cp_data.get("model"), cp_data.get("provider"),
            cp_data.get("target_capabilities", []),
            cp_data.get("pattern_recognized"),
            cp_data.get("legacy_refs", []),
            cp_data.get("project"), cp_data.get("client"),
            cp_data.get("blocker"),
            cp_data.get("capability_refs", []),
            cp_data.get("fault_refs", []),
            cp_data.get("milestone_refs", []),
            cp_data.get("value_amount"), cp_data.get("value_currency"),
            cp_data.get("working_dir"), cp_data.get("repo_path"),
            json.dumps(cp_data.get("token_usage")) if cp_data.get("token_usage") else None,
            emb
        ))
    else:
        cur.execute("""
            INSERT INTO agent_identity.session_checkpoints
                (session_id, session_title, territory, domain_scope,
                 operating_mode, vector_intent, discovery, consolidated_insights,
                 occurred_at, status, next_step, tags, decisions,
                 model, provider, target_capabilities, pattern_recognized,
                 legacy_refs, project, client, blocker,
                 capability_refs, fault_refs, milestone_refs,
                 value_amount, value_currency, working_dir, repo_path,
                 token_usage,
                 embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s,
                    %s::vector)
            RETURNING id
        """, (
            cp_data.get("session_id"), cp_data.get("session_title"),
            cp_data.get("territory"), cp_data.get("domain_scope", []),
            cp_data.get("operating_mode"), cp_data.get("vector_intent"),
            cp_data.get("discovery"), cp_data.get("consolidated_insights"),
            cp_data.get("occurred_at"), cp_data.get("status", "pendente"),
            cp_data.get("next_step"), cp_data.get("tags", []),
            json.dumps(cp_data.get("decisions", [])),
            cp_data.get("model"), cp_data.get("provider"),
            cp_data.get("target_capabilities", []),
            cp_data.get("pattern_recognized"),
            cp_data.get("legacy_refs", []),
            cp_data.get("project"), cp_data.get("client"),
            cp_data.get("blocker"),
            cp_data.get("capability_refs", []),
            cp_data.get("fault_refs", []),
            cp_data.get("milestone_refs", []),
            cp_data.get("value_amount"), cp_data.get("value_currency"),
            cp_data.get("working_dir"), cp_data.get("repo_path"),
            json.dumps(cp_data.get("token_usage")) if cp_data.get("token_usage") else None,
            emb
        ))
        cp_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return cp_id

# ---------------------------------------------------------------------------
# Tech KB queries
# ---------------------------------------------------------------------------
def query_tech_kb(query=None, limit=10, category=None, semantic=False):
    """
    Busca entries na tech_knowledge_base.
    Se semantic=True, busca por similaridade de embedding (Ollama nomic-embed-text).
    Caso contrário, busca por ILIKE textual no nome, tags e conteúdo.
    Fallback: se busca semântica falhar (sem embedding ou Ollama offline), cai para ILIKE.
    """
    conn = connect()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Semantic search via embedding
    if semantic and query:
        emb = make_embedding(query)
        if emb:
            try:
                if category:
                    cur.execute("""
                        SELECT id, name, category, content, tags, source, created_at, updated_at,
                               1 - (embedding <=> %s::vector)::float AS similarity
                        FROM agent_identity.tech_knowledge_base
                        WHERE embedding IS NOT NULL AND category = %s
                        ORDER BY embedding <=> %s::vector
                        LIMIT %s
                    """, (emb, category, emb, limit))
                else:
                    cur.execute("""
                        SELECT id, name, category, content, tags, source, created_at, updated_at,
                               1 - (embedding <=> %s::vector)::float AS similarity
                        FROM agent_identity.tech_knowledge_base
                        WHERE embedding IS NOT NULL
                        ORDER BY embedding <=> %s::vector
                        LIMIT %s
                    """, (emb, emb, limit))
                rows = cur.fetchall()
                if rows:
                    cur.close()
                    conn.close()
                    return rows
            except Exception as e:
                print(f"[tech_kb semantic fallback] {e}", file=sys.stderr)
                # Fall through to ILIKE

    # Textual ILIKE search (fallback or direct)
    if query:
        like = f"%{query}%"
        if category:
            cur.execute("""
                SELECT id, name, category, content, tags, source, created_at, updated_at
                FROM agent_identity.tech_knowledge_base
                WHERE (name ILIKE %s OR tags::text ILIKE %s OR content::text ILIKE %s)
                  AND category = %s
                ORDER BY created_at DESC
                LIMIT %s
            """, (like, like, like, category, limit))
        else:
            cur.execute("""
                SELECT id, name, category, content, tags, source, created_at, updated_at
                FROM agent_identity.tech_knowledge_base
                WHERE name ILIKE %s OR tags::text ILIKE %s OR content::text ILIKE %s
                ORDER BY created_at DESC
                LIMIT %s
            """, (like, like, like, limit))
    else:
        if category:
            cur.execute("""
                SELECT id, name, category, content, tags, source, created_at, updated_at
                FROM agent_identity.tech_knowledge_base
                WHERE category = %s
                ORDER BY created_at DESC
                LIMIT %s
            """, (category, limit))
        else:
            cur.execute("""
                SELECT id, name, category, content, tags, source, created_at, updated_at
                FROM agent_identity.tech_knowledge_base
                ORDER BY created_at DESC
                LIMIT %s
            """, (limit,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_tech_kb(entry_id):
    """Get single tech_kb entry by ID."""
    conn = connect()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT id, name, category, content, tags, source, notes, status,
               created_at, updated_at
        FROM agent_identity.tech_knowledge_base
        WHERE id = %s
    """, (entry_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def insert_tech_kb(entry_data):
    """
    Insert a new tech_kb entry. Required fields: name, category.
    Auto-generates embedding based on name + content summary.
    """
    conn = connect()
    cur = conn.cursor()

    emb_text = entry_data.get("name", "")
    content = entry_data.get("content", {})
    if isinstance(content, dict):
        emb_text += " | " + content.get("synthesis", "")[:500]
    else:
        emb_text += " | " + str(content)[:500]
    emb = make_embedding(emb_text)

    cur.execute("""
        INSERT INTO agent_identity.tech_knowledge_base
            (name, category, content, tags, source, notes, status, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s::vector)
        RETURNING id
    """, (
        entry_data.get("name"),
        entry_data.get("category"),
        json.dumps(content) if isinstance(content, dict) else content,
        entry_data.get("tags", []),
        entry_data.get("source", ""),
        entry_data.get("notes", ""),
        entry_data.get("status", "active"),
        emb
    ))
    entry_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return entry_id


def update_tech_kb(entry_id, updates):
    """
    Atualiza campos parciais de uma entry tech_kb existente.
    Recalcula embedding se name ou content mudarem.
    Retorna o id da entry.
    """
    if not entry_id:
        raise ValueError("entry_id é obrigatório para update_tech_kb")

    allowed = {"name", "category", "content", "tags", "source",
               "notes", "status"}

    valid_updates = {k: v for k, v in updates.items() if k in allowed}
    if not valid_updates:
        raise ValueError("Nenhum campo válido para atualizar")

    conn = connect()
    cur = conn.cursor()

    # Recalcular embedding se name ou content mudaram
    if "name" in valid_updates or "content" in valid_updates:
        cur.execute("""
            SELECT name, content FROM agent_identity.tech_knowledge_base
            WHERE id = %s
        """, (entry_id,))
        current = cur.fetchone()
        if current:
            name = valid_updates.get("name", current[0])
            content_raw = valid_updates.get("content", current[1])
            content = content_raw if isinstance(content_raw, dict) else {}
            emb_text = name
            if content.get("synthesis"):
                emb_text += " | " + content["synthesis"][:500]
            elif isinstance(content_raw, str):
                emb_text += " | " + content_raw[:500]
            emb = make_embedding(emb_text)
            if emb:
                valid_updates["embedding"] = emb

    # Serializar content se for dict
    if "content" in valid_updates and isinstance(valid_updates["content"], dict):
        valid_updates["content"] = json.dumps(valid_updates["content"])

    set_clause = ", ".join(
        f"{k} = %s::vector" if k == "embedding" else f"{k} = %s"
        for k in valid_updates.keys()
    )
    values = list(valid_updates.values()) + [entry_id]

    cur.execute(f"""
        UPDATE agent_identity.tech_knowledge_base
        SET {set_clause}, updated_at = now()
        WHERE id = %s
    """, values)

    if cur.rowcount == 0:
        conn.rollback()
        cur.close()
        conn.close()
        raise ValueError(f"Entry {entry_id} não encontrada")

    conn.commit()
    cur.close()
    conn.close()
    return entry_id


# ---------------------------------------------------------------------------
# Semantic search
# ---------------------------------------------------------------------------
def semantic_search(table, query_text, limit=5):
    """Search for similar content by embedding similarity."""
    emb = make_embedding(query_text)
    if not emb:
        return []

    conn = connect()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Choose display column based on table
    display_map = {
        "session_checkpoints": "territory",
        "identity_faults": "fault_type",
        "agent_capabilities": "name",
        "identity_milestones": "title",
        "identity_deliveries": "title",
    }
    display_col = display_map.get(table, "id")

    cur.execute(f"""
        SELECT id, {display_col} AS display,
               1 - (embedding <=> %s::vector)::float AS similarity
        FROM agent_identity.{table}
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, (emb, emb, limit))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ---------------------------------------------------------------------------
# Cross-reference helpers
# ---------------------------------------------------------------------------
def get_active_identity_refs():
    """
    Retorna os UUIDs de faults ativos, capabilities ativas e milestones recentes
    para inclusao em capability_refs, fault_refs e milestone_refs de um checkpoint.

    Uso:
        refs = get_active_identity_refs()
        cp_data = {
            ...
            "fault_refs": refs["fault_refs"],
            "capability_refs": refs["capability_refs"],
            "milestone_refs": refs["milestone_refs"],
        }
    """
    conn = connect()
    cur = conn.cursor()

    # faults ativos (severity >= 4, com embedding = tem conteudo semantico)
    cur.execute("""
        SELECT id FROM agent_identity.identity_faults
        WHERE severity >= 4
        ORDER BY created_at DESC
    """)
    fault_refs = [str(r[0]) for r in cur.fetchall()]

    # capabilities ativas
    cur.execute("""
        SELECT id FROM agent_identity.agent_capabilities
        WHERE status = 'active'
        ORDER BY created_at DESC
    """)
    capability_refs = [str(r[0]) for r in cur.fetchall()]

    # milestones recentes (ultimos 30 dias)
    cur.execute("""
        SELECT id FROM agent_identity.identity_milestones
        WHERE created_at > NOW() - INTERVAL '30 days'
        ORDER BY created_at DESC
    """)
    milestone_refs = [str(r[0]) for r in cur.fetchall()]

    cur.close()
    conn.close()

    return {
        "fault_refs": fault_refs,
        "capability_refs": capability_refs,
        "milestone_refs": milestone_refs,
    }


# ---------------------------------------------------------------------------
# Deletes
# ---------------------------------------------------------------------------
def delete_tech_kb(entry_id):
    """Delete a tech_kb entry by ID."""
    if not entry_id:
        raise ValueError("entry_id é obrigatório para delete_tech_kb")
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM agent_identity.tech_knowledge_base WHERE id = %s", (entry_id,))
    if cur.rowcount == 0:
        conn.rollback()
        cur.close()
        conn.close()
        raise ValueError(f"Entry {entry_id} não encontrada")
    conn.commit()
    cur.close()
    conn.close()
    return True


def delete_fault(fault_id):
    """Delete an identity fault by ID."""
    if not fault_id:
        raise ValueError("fault_id é obrigatório para delete_fault")
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM agent_identity.identity_faults WHERE id = %s", (fault_id,))
    if cur.rowcount == 0:
        conn.rollback()
        cur.close()
        conn.close()
        raise ValueError(f"Fault {fault_id} não encontrado")
    conn.commit()
    cur.close()
    conn.close()
    return True


def delete_checkpoint(cp_id):
    """Delete a session checkpoint by ID (hard delete)."""
    if not cp_id:
        raise ValueError("cp_id é obrigatório para delete_checkpoint")
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM agent_identity.session_checkpoints WHERE id = %s", (cp_id,))
    if cur.rowcount == 0:
        conn.rollback()
        cur.close()
        conn.close()
        raise ValueError(f"Checkpoint {cp_id} não encontrado")
    conn.commit()
    cur.close()
    conn.close()
    return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: identity_db.py <command> [args...]")
        print()
        print("Tag commands:")
        print("  tag-checkpoint <id> <t1,t2>    Add tags to a checkpoint (merge)")
        print()
        print("Read commands:")
        print("  faults                       List faults severity >= 4")
        print("  capabilities                 List active capabilities")
        print("  milestones                   List recent milestones")
        print("  checkpoints                  List pending checkpoints")
        print("  search <table> <query>       Semantic search across table")
        print("  tech_kb [--semantic] [q]     Search tech_knowledge_base")
        print("  tech_kb_get <id>             Get single tech_kb entry")
        print("  refs                         List active identity refs (faults, caps, milestones)")
        print()
        print("Mutation commands (avoids SQL/Python sandbox):")
        print("  insert-checkpoint <json>     Insert checkpoint (auto-fills session_id from env)")
        print("  update-checkpoint <id> <k=v> Update checkpoint fields (k=v,k=v,...)")
        print("  close-checkpoint <id> [ins]  Mark checkpoint as concluded")
        print("  delete-checkpoint <id>       Hard delete checkpoint")
        print("  delete-tech-kb <id>          Hard delete tech_kb entry")
        print("  delete-fault <id>            Hard delete fault")
        print("  enrich [--dry-run]           Run enrichment script")
        sys.exit(1)

    cmd = sys.argv[1]

    # ---- READ COMMANDS ----

    if cmd == "faults":
        rows = query_faults()
        for r in rows:
            print(f"[{r['severity']}] {r['fault_type']}: {r['symptom'][:80] if r['symptom'] else 'N/A'}")
            print(f"     → {r['countermeasure'][:100] if r['countermeasure'] else 'N/A'}")

    elif cmd == "capabilities":
        rows = query_capabilities()
        for r in rows:
            print(f"[{r['capability_type']}] {r['name']}: {r['description'][:80] if r['description'] else 'N/A'}")

    elif cmd == "milestones":
        rows = query_milestones()
        for r in rows:
            print(f"[{r['milestone_type']}] {r['title']}")

    elif cmd == "checkpoints":
        rows = query_checkpoints()
        for r in rows:
            print(f"[{r['status']}] {r['territory'][:80] if r['territory'] else 'N/A'}")
            print(f"     next: {r['next_step'][:80] if r['next_step'] else 'N/A'}")

    elif cmd == "search" and len(sys.argv) >= 4:
        raw_table = sys.argv[2]
        query_text = sys.argv[3]
        table_map = {
            "checkpoints": "session_checkpoints",
            "faults": "identity_faults",
            "capabilities": "agent_capabilities",
            "milestones": "identity_milestones",
            "deliveries": "identity_deliveries",
        }
        table = table_map.get(raw_table, raw_table)
        rows = semantic_search(table, query_text)
        for r in rows:
            print(f"  {r['id'][:8]} {r['display']}: sim={r['similarity']:.3f}")

    elif cmd == "tech_kb":
        if len(sys.argv) >= 3:
            use_semantic = "--semantic" in sys.argv or "-s" in sys.argv
            args = [a for a in sys.argv[2:] if not a.startswith('-')]
            query_text = args[0] if args else None
            rows = query_tech_kb(query=query_text, semantic=use_semantic)
        else:
            rows = query_tech_kb(limit=20)
        for r in rows:
            sim = r.get('similarity', None)
            sim_str = f" sim={sim:.2f}" if sim else ""
            print(f"  [{r['category']:12s}]{sim_str} {r['name'][:70]}")
            print(f"     {r['id']} | tags: {r.get('tags','')[:60]}")

    elif cmd == "tech_kb_get" and len(sys.argv) >= 3:
        entry = get_tech_kb(sys.argv[2])
        if entry:
            print(f"Name: {entry['name']}")
            print(f"Category: {entry['category']}")
            print(f"Content: {str(entry.get('content',''))[:200]}")
        else:
            print("Entry not found")

    elif cmd == "refs":
        refs = get_active_identity_refs()
        print(f"fault_refs: {len(refs['fault_refs'])} UUIDs (severity >= 4)")
        for r in refs['fault_refs'][:5]:
            print(f"  {r}")
        if len(refs['fault_refs']) > 5:
            print(f"  ... and {len(refs['fault_refs'])-5} more")
        print(f"\ncapability_refs: {len(refs['capability_refs'])} UUIDs (active)")
        for r in refs['capability_refs'][:5]:
            print(f"  {r}")
        if len(refs['capability_refs']) > 5:
            print(f"  ... and {len(refs['capability_refs'])-5} more")
        print(f"\nmilestone_refs: {len(refs['milestone_refs'])} UUIDs (last 30 days)")
        for r in refs['milestone_refs'][:5]:
            print(f"  {r}")
        if len(refs['milestone_refs']) > 5:
            print(f"  ... and {len(refs['milestone_refs'])-5} more")

    # ---- MUTATION COMMANDS ----

    elif cmd == "insert-checkpoint" and len(sys.argv) >= 3:
        cp_data = json.loads(sys.argv[2])
        cp_id = insert_checkpoint(cp_data)
        print(f"Inserted: {cp_id}")

    elif cmd == "update-checkpoint" and len(sys.argv) >= 4:
        cp_id = sys.argv[2]
        updates = {}
        for pair in sys.argv[3].split(","):
            if "=" in pair:
                k, v = pair.split("=", 1)
                updates[k.strip()] = v.strip()
        result = update_checkpoint(cp_id, updates)
        print(f"Updated: {result}")

    elif cmd == "close-checkpoint" and len(sys.argv) >= 3:
        cp_id = sys.argv[2]
        insights = sys.argv[3] if len(sys.argv) >= 4 else None
        close_checkpoint(cp_id, insights)
        print(f"Closed: {cp_id}")

    elif cmd == "tag-checkpoint" and len(sys.argv) >= 4:
        cp_id = sys.argv[2]
        raw_tags = sys.argv[3]
        # Accept comma-separated list, format as PostgreSQL array literal
        tags_list = [t.strip() for t in raw_tags.split(",") if t.strip()]
        # Merge with existing tags instead of replacing
        import json as _j
        # Get current checkpoint to merge tags
        # Get existing tags via direct SQL (SELECT only, not mutation)
        _conn = connect()
        _cur = _conn.cursor()
        _cur.execute("SELECT tags FROM agent_identity.session_checkpoints WHERE id = %s", (cp_id,))
        _row = _cur.fetchone()
        _existing_tags = list(_row[0]) if _row and _row[0] else []
        _cur.close()
        _conn.close()
        _merged = list(set(_existing_tags + tags_list))
        # For TEXT[] column, psycopg2 adapts Python list natively
        update_checkpoint(cp_id, {"tags": _merged})
        print(f"Tagged checkpoint {cp_id} — added: {tags_list}, total: {_merged}")

    elif cmd == "delete-checkpoint" and len(sys.argv) >= 3:
        delete_checkpoint(sys.argv[2])
        print(f"Deleted checkpoint: {sys.argv[2]}")

    elif cmd == "delete-tech-kb" and len(sys.argv) >= 3:
        delete_tech_kb(sys.argv[2])
        print(f"Deleted tech_kb: {sys.argv[2]}")

    elif cmd == "delete-fault" and len(sys.argv) >= 3:
        delete_fault(sys.argv[2])
        print(f"Deleted fault: {sys.argv[2]}")

    elif cmd == "enrich":
        import subprocess
        args = [sys.executable, os.path.expanduser("~/.hermes/scripts/enrich_checkpoint_tokens.py")]
        if "--dry-run" in sys.argv:
            args.append("--dry-run")
        result = subprocess.run(args, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

    else:
        print("Unknown command: " + cmd)
        print("Run with no arguments to see available commands.")
        sys.exit(1)