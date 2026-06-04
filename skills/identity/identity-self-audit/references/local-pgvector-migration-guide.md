# Local pgvector Migration Guide (Supabase → Docker pgvector)

Pattern discovered 2026-06-02 during identity layer migration.
Canonical example: `agent_identity` schema (6 tables, 94 rows, 94 embeddings).

## When to use this pattern

The identity layer (identity_faults, agent_capabilities, etc.) runs better
locally — no network latency, no PGRST301, no Supabase RLS complexity.
Extend this pattern to any table that:
- Is read on every session startup (latency-sensitive)
- Benefits from semantic search via pgvector
- Changes infrequently (write-once, read-many)

## Infrastructure

- **PostgreSQL 16 + pgvector** in Docker (`pgvector/pgvector:pg16`):
  `localhost:5433`, database `openbrain`, schema `agent_identity`
- **Ollama** for embeddings (`nomic-embed-text`, 768d)
- **Credentials**: PostgreSQL password from docker-compose + secrets.env for Supabase pulls

## Migration Script Pattern

```python
# 1. READ SECRETS with Python open(), NEVER shell source
#    secrets.env has no `export` prefix — just KEY="value"
with open(os.path.expanduser('~/.hermes/secrets.env')) as f:
    env = {}
    for line in f:
        m = re.match(r'^(\w+)=["\']?(.+?)["\']?\s*(?:#.*)?$', line)
        if m:
            env[m.group(1)] = m.group(2).strip('"').strip("'")

# 2. TEXT[] vs JSONB distinction for psycopg2
#    TEXT[] columns → pass Python list directly
#    JSONB columns → pass json.dumps(val) as string
TEXT_ARRAY_COLS = {"tags", "blocks", "domain_scope", "capability_refs", ...}
JSONB_COLS = {"decisions", "refs"}

def prepare_value(val, col_name):
    if col_name in JSONB_COLS and isinstance(val, (dict, list)):
        return json.dumps(val)
    if col_name in TEXT_ARRAY_COLS and isinstance(val, list):
        return val       # psycopg2 handles TEXT[] natively
    if isinstance(val, str) and val.lower() == "none":
        return None
    return val

# 3. SQL with CORRECT ON CONFLICT syntax
conflict_clause = "(id)"  # or "(capability_id, depends_on_id)"
sql = f"""
    INSERT INTO schema.table (all, columns, embedding)
    VALUES (%(col1)s, %(col2)s, ..., %(embedding)s::vector)
    ON CONFLICT {conflict_clause} DO NOTHING
"""

# 4. Embedding via local Ollama — /api/embed (not /api/embeddings)
import requests
r = requests.post('http://localhost:11434/api/embed', json={
    "model": "nomic-embed-text",
    "input": "territory | discovery | vector_intent"
}, timeout=30)
emb = r.json()["embeddings"][0]  # list of 768 floats

# 5. Insert with error recovery per row
for row in rows:
    try:
        cur.execute(sql, params)
        conn.commit()
    except Exception as e:
        conn.rollback()
        time.sleep(0.3)
```

## Pitfalls

| Error | Cause | Fix |
|-------|-------|-----|
| `ON CONFLICT id` | Missing parens | `ON CONFLICT (id)` |
| `can't adapt type 'dict'` | JSONB col needs string | `json.dumps(val)` |
| `malformed array literal` | TEXT[] col got json.dumps | Pass Python list directly |
| `password auth failed` | Shell `PGPASSWORD=*** | Use `PGPASSWORD='***'` literal or docker exec |

## Indexes

```sql
CREATE INDEX idx_name ON schema.table USING hnsw (embedding vector_cosine_ops);
```

## Verification

```bash
python3 ~/.hermes/scripts/identity_db.py faults
python3 ~/.hermes/scripts/identity_db.py capabilities
python3 ~/.hermes/scripts/identity_db.py search identity_faults "fechamento prematuro"
```