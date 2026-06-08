---
name: checkpoint-workflow
version: 2.0.0
description: >-
  Context component of the meta-skill orchestrator (agent-onboarding).
  Manages the lifecycle of session_checkpoints in pgvector LOCAL — the
  identity layer that feeds the agent identity framework.
  Each checkpoint is an INTENTIONAL MARK: not "what was done" (log),
  but "where the agent was and what it was trying to become".
  v2.0.0: Migrated from Supabase to pgvector local. Full CLI mutation.
  token_usage, model, provider tracking for benchmark metrics.
tags: [checkpoint, meta-skill, identity, context, session]
---

# Checkpoint Workflow — Meta-Skill Context Layer

## Purpose

The `session_checkpoints` are the backbone of the agent's representation
space. They are not log records — they are INTENTIONAL MARKS that answer:

1. **Where was I?** (territory)
2. **What was I trying to become?** (vector_intent)
3. **What did I discover about myself?** (discovery)
4. **What do I carry forward?** (consolidated_insights + legacy_refs)

**Since 02/06/2026, session_checkpoints live in pgvector local**
(agent_identity schema, openbrain-postgres:5433), not in Supabase.
CRUD operations go through `~/.hermes/scripts/identity_db.py` CLI.
Supabase checkpoints are historical backup only — never write new ones there.

**Why local instead of Supabase?**
- Supabase outages (PGRST301, rate limits) left the agent blind
- Local pgvector queries complete in <5ms vs 50-200ms for Supabase REST
- No network dependency for identity data — the agent's context must survive
  cloud failures
- Embedding similarity search via local Ollama: <50ms, zero token cost

The complete cycle in the meta-skill:

```
SESSION START
  ├── 1. Fetch latest pending checkpoint (identity_db.py checkpoints)
  ── 2. Inject territory + vector_intent as north
  ── 3. Inject discovery + consolidated as active context
       │
WORK
  │
SESSION END (or at any time)
  ├── 4. Extract territory/vector/discovery/consolidated from work
  ├── 5. Cross-reference with identity_faults + agent_capabilities
  ├── 6. INSERT into session_checkpoints via identity_db.py CLI
  ── 7. Update previous checkpoint status to 'completed'
```

---

## PART 1 — STARTUP: Context Recovery

### Main query (identity_db.py CLI — local, offline-resilient)

```bash
python3 ~/.hermes/scripts/identity_db.py checkpoints
```

Also search concluded checkpoints for past decisions:

```bash
python3 ~/.hermes/scripts/identity_db.py search session_checkpoints "<TERRITORIO> <PALAVRAS-CHAVE>"
```

### What to do with the result

Inject into reasoning as a context block:

```
=== CHECKPOINT CONTEXT ===
Territory: <territory>
Working directory: <working_dir>
Repository: <repo_path>
Model: <model>
Provider: <provider>
Vector: <vector_intent>
Discovery: <discovery>
Inheritance: <consolidated_insights>
Next step: <next_step>
```

---

## PART 2 — CHECKPOINT SAVING

### When to save

1. **End of session** (detected by /quit, /exit, /new, timeout)
2. **At any time** the user or agent requests
3. **After each significant task** (meta-skill sub-task)

### Extraction protocol for the 5 identity fields

Before saving, reflect:

| Field | What to extract | Example |
|---|---|---|
| **territory** | The larger scenario. Not what was done, but WHERE we were. | "Building the meta-skill — enabling the self-knowledge engine (MBTI)" |
| **operating_mode** | How the agent was interacting with the problem | reflexive, conceptual, execution, diagnostic, research, planning, decision, review |
| **vector_intent** | What the agent was trying to BECOME by doing this | "I want the agent to be able to type the user in 5-10 minutes of conversation" |
| **discovery** | What was NOT obvious and was discovered | "Each MBTI answer reveals an expectation, not just a preference" |
| **consolidated_insights** | What can be reused as know-how | "MBTI protocol: 70 questions, scoring 4 dim, register in user_mbti" |

### Insertion via identity_db.py CLI (NUNCA SQL direto)

```bash
python3 ~/.hermes/scripts/identity_db.py insert-checkpoint '{
  "territory": "...",
  "operating_mode": "...",
  "vector_intent": "...",
  "occurred_at": "2026-06-08",
  "model": "deepseek-v4-flash:cloud",
  "provider": "ollama-launch",
  "session_id": "auto-preenchido por HERMES_SESSION_ID se omitido"
}'
```

Full template via Python:

```python
import sys; sys.path.insert(0, os.path.expanduser('~/.hermes/scripts'))
from identity_db import insert_checkpoint, get_active_identity_refs

# model/provider are now MANDATORY — enables benchmark aggregation
# session_id auto-fills from HERMES_SESSION_ID if omitted

cp_data = {
  "session_id": "<session_id>",  # auto-filled from HERMES_SESSION_ID if omitted
  "session_title": "<title>",
  "territory": "...",
  "operating_mode": "...",
  "vector_intent": "...",
  "target_capabilities": [...],
  "discovery": "...",
  "pattern_recognized": "...",
  "consolidated_insights": "...",
  "legacy_refs": [...],
  "occurred_at": "YYYY-MM-DD",
  "status": "pending",
  "project": "...",
  "client": "...",
  "working_dir": "/path/to/project",
  "repo_path": "https://github.com/user/repo",
  "next_step": "...",
  "blocker": null,
  "tags": [...],
  "domain_scope": [...],
  "capability_refs": [...],   # use get_active_identity_refs()['capability_refs']
  "fault_refs": [...],        # use get_active_identity_refs()['fault_refs']
  "milestone_refs": [...],    # use get_active_identity_refs()['milestone_refs']
  "decisions": [...],
  "model": "deepseek-v4-flash:cloud",
  "provider": "ollama-launch",
  "value_amount": null,
  "token_usage": null          # filled post-session by enrich script
}
```

### Benchmark structure — token_usage and model/provider

Checkpoints now carry metrics for performance benchmarking:

- `model` + `provider`: links each checkpoint to the model that generated it
- `token_usage` (JSONB): `{"input": N, "output": N, "cache_read": N, "cache_write": N, "cost_usd": N}`
- Enrichment: `python3 ~/.hermes/scripts/identity_db.py enrich` reads Hermes
  session store and populates token_usage

This enables:
- Token consumption per operating_mode (diagnosis vs execution)
- Cost comparison across territories and models
- Efficiency: tokens_per_discovery, cost_per_checkpoint
- Benchmark reports via cross-reference with `hermes insights`

### Closing the cycle: close before create

After constructing the new checkpoint, close any existing pending checkpoint
of the SAME territory before inserting the new one:

```bash
python3 ~/.hermes/scripts/identity_db.py close-checkpoint <uuid> "Continuado em novo checkpoint."
python3 ~/.hermes/scripts/identity_db.py insert-checkpoint '...'
```

---

## PART 3 — Cross-Reference with Agentic Identity

When saving a checkpoint, include:

- `fault_refs`: UUIDs of faults detected in this session
- `capability_refs`: UUIDs of capabilities exercised
- `milestone_refs`: UUIDs of milestones reached
- `legacy_refs`: UUIDs of tech_kb entries created

Use the helper:

```python
from identity_db import get_active_identity_refs
refs = get_active_identity_refs()
# refs = {"fault_refs": [...], "capability_refs": [...], "milestone_refs": [...]}
```

---

## PART 4 — CLI Mutation Commands

Never use `docker exec psql` or raw SQL. All mutations go through
`identity_db.py` CLI:

```bash
# READ
python3 identity_db.py faults
python3 identity_db.py capabilities
python3 identity_db.py checkpoints
python3 identity_db.py search <table> <query>
python3 identity_db.py tech_kb [--semantic] [query]
python3 identity_db.py tech_kb_get <uuid>
python3 identity_db.py refs

# MUTATION
python3 identity_db.py insert-checkpoint '<json>'
python3 identity_db.py update-checkpoint <uuid> "status=concluida,k=v"
python3 identity_db.py close-checkpoint <uuid>
python3 identity_db.py delete-checkpoint <uuid>
python3 identity_db.py delete-tech-kb <uuid>
python3 identity_db.py delete-fault <uuid>
python3 identity_db.py enrich [--dry-run]
```

---

## PART 5 — Verification

After configuring the skill, test with:

```bash
python3 ~/.hermes/scripts/identity_db.py checkpoints
python3 ~/.hermes/scripts/identity_db.py faults
python3 ~/.hermes/scripts/identity_db.py refs
```

## References

- `~/.hermes/scripts/identity_db.py` — helper Python module + CLI
- `migrations/pgvector_local_identity_schema.sql` — full schema for all 7 tables
- `supabase-startup-protocol` — Etapa 2B reads identity from pgvector local

## Pitfalls

1. **Confusing checkpoint with log** — checkpoint answers WHERE/WHO/DISCOVERY/INHERITANCE
2. **Saving without model/provider** — breaks benchmark aggregation
3. **Forgetting to cross-reference** — checkpoint without capability_refs, fault_refs,
   and legacy_refs is incomplete information about the agent's formation
4. **Not closing the cycle** — when inserting a new checkpoint, always close the
   previous pending one
5. **Using SQL/docker exec instead of identity_db.py CLI** — NUNCA. CLI has all
   mutation commands. One terminal() call covers everything.
