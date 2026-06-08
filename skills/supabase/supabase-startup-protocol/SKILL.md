---
name: supabase-startup-protocol
version: 2.4.0
description: >-
  Mandatory session open AND close protocol.
  v2.4.0: Identity layer migrated from Supabase to local pgvector.
  Identity queries now use identity_db.py CLI (local, offline-resilient).
  Supabase remains ONLY for USER data (career_tracker, CRM, worklog).
  No work action may occur before the scan.
tags: [supabase, startup, shutdown, protocol, R22, session-init, checkpoint, weekly-triage]
---

# Supabase Startup + Shutdown Protocol

## Full Cycle

```
STARTUP: scan pgvector local (identity) + Supabase (user data) → report state → identify pending items
    ↓
WORK:   execute tasks
    ↓
CHECKPOINT (per task): record to session_checkpoints via identity_db.py CLI → close previous checkpoint → update supermemory
    ↓
SHUTDOWN (end of session): consolidate everything → update TOC
```

---

# PART 1 — STARTUP (session opening)

## ⚠️ RULE #1 — BEFORE ANY ACTION: Run the identity layer scan FIRST

The identity layer (faults, checkpoints, capabilities) lives in pgvector LOCAL.
Query it via identity_db.py CLI — NOT via Supabase REST API.

```bash
# Identity layer — local, offline-resilient, <5ms
python3 ~/.hermes/scripts/identity_db.py checkpoints
python3 ~/.hermes/scripts/identity_db.py faults
```

Why local? Supabase outages (PGRST301, rate limits, network failures) left the
agent blind during critical sessions. Identity data is too important to depend
on cloud availability. The local pgvector runs on the same machine as Hermes —
no network hop, no token cost, no outage risk.

## Step 1 — General state scan (parallel)

Call these MCP tools in parallel on the first turn for USER DATA only:

```python
mcp_code_analyzer_get_code_analyzer_summary()
mcp_product_catalog_list_products()
mcp_escape_catalog_get_catalog_summary()
```

## Step 2 — Fetch pending checkpoints (LOCAL)

```bash
python3 ~/.hermes/scripts/identity_db.py checkpoints
```

## Step 3 — Report to the user

```
=== STARTUP ===
⚡ faults:       <N> active (severity >= 4)
📌 checkpoints:  <N> pending
📚 tech_kb:      <N> entries
🔧 code-analyzer: <N> projects, <N> snapshots
📦 products:     <N> active
🧩 escape rooms: <N> rooms
```

---

# PART 2 — CHECKPOINT (per completed task)

## When to run

At the end of EACH significant task or sub-task. **Do not** wait until
the end of the session to record.

## Required checkpoint fields

| Field | Required | Description |
|-------|----------|-------------|
| `territory` | yes | The larger scenario: where the agent was |
| `operating_mode` | yes | How it interacted with the problem |
| `vector_intent` | yes | What it was trying to become |
| `discovery` | yes | What it discovered about itself |
| `consolidated_insights` | yes | What it carries forward |
| `occurred_at` | yes | Checkpoint date |
| `status` | yes | pending / completed / blocked / cancelled |
| `next_step` | yes | Next required action |
| `model` | yes | Model used (e.g., deepseek-v4-flash:cloud) |
| `provider` | yes | Provider (e.g., ollama-launch) |

## Benchmark structure in checkpoints

Checkpoints now carry `token_usage` (JSONB — input, output, cache, cost_usd)
for performance benchmarking. The `model` and `provider` fields link each
checkpoint to the model that generated it. This enables:

- Token consumption analysis per operating_mode (diagnosis vs execution)
- Cost comparison across models and territories
- Efficiency metrics: tokens_per_discovery, cost_per_checkpoint
- Benchmark reports via `hermes insights` cross-referenced with checkpoints

Use identity_db.py CLI to insert — never direct SQL:

```bash
# Insert with full fields
python3 ~/.hermes/scripts/identity_db.py insert-checkpoint '{"territory":"...","operating_mode":"...","vector_intent":"...","occurred_at":"2026-06-08","model":"deepseek-v4-flash:cloud","provider":"ollama-launch"}'

# Close previous checkpoint
python3 ~/.hermes/scripts/identity_db.py close-checkpoint <uuid> "Resumo do aprendizado"
```

## Expected behavior

- **Always** record a checkpoint after completing a task
- **Always** include all 5 identity fields — without them the checkpoint
  is useless for context rehydration
- **Always** include `next_step` — without it the checkpoint provides no direction
- **Always** close the previous pending checkpoint
- **Always** set `model` and `provider` — enables benchmark aggregation
- **Never** record an empty checkpoint ("I worked" with no content)
- **Never** use `docker exec psql` or SQL directly — use identity_db.py CLI

---

# PART 3 — SHUTDOWN (end of session)

## When to run

When detecting the session is ending:
- User types `/quit`, `/exit`, `/new`
- User explicitly says "I'll stop here", "see you tomorrow", "good night"
- After prolonged inactivity (session timeout)

## What to do

1. Save checkpoint with all identity fields + model/provider
2. Close previous pending checkpoint
3. Run enrichment: `python3 ~/.hermes/scripts/identity_db.py enrich`
4. Update Supermemory with summary
5. Update TOC if there were structural changes

---

# PART 4 — WEEKLY THOUGHTS TRIAGE

Every **Monday** after the STARTUP scan. Thoughts is an INPUT funnel,
not a storage layer. Consolidate ideas into permanent destinations and remove.

---

# PART 5 — AUTOMATION

Djair uses `ollama launch hermes`. The wrapper `~/.local/bin/hermes` manages
the actual command. **Do not replace.** Edit the wrapper for skills or keep
manual invocation via `--skills`.

---

## Pitfalls

1. **Forgetting to run identity scan** — run `identity_db.py faults` and
   `identity_db.py checkpoints` BEFORE any work. Identity is LOCAL now.
2. **Using Supabase for checkpoints** — checkpoints are in pgvector local.
   Supabase REST API does NOT have session_checkpoints anymore.
3. **Assuming you "remember"** — do not trust session memory. Query identity_db.py.
4. **Checkpoint without `next_step`** — useless. Always fill it in.
5. **Checkpoint without `model`/`provider`** — breaks benchmark aggregation.
6. **Shutdown without consolidating** — at least the last checkpoint was saved.
7. **Using `docker exec psql` instead of identity_db.py CLI** — NUNCA.
   identity_db.py CLI has insert-checkpoint, update-checkpoint, delete-checkpoint,
   close-checkpoint, enrich. One `terminal()` call covers all mutations.

## Pitfall of Editing Hermes Config — Consult tech_kb `81c48035`

🔗 **tech_kb entry `81c48035`** — "Hermes Config.yaml + .env Editing
   Protocol — All Pitfalls"
