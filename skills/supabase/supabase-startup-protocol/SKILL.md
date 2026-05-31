---
name: supabase-startup-protocol
version: 2.3.0
description: >
  Mandatory session open AND close protocol. Scan Supabase on startup,
  checkpoint to Supabase after each task, and consolidate at session end.
  No work action may occur before the scan.
  v2.3.0: PGRST301 pitfall permanently resolved — explicit instructions
  for using service_role_key with redact_secrets enabled.
tags: [supabase, startup, shutdown, protocol, R22, session-init, checkpoint, weekly-triage]
---

# Supabase Startup + Shutdown Protocol

## Full Cycle

```
STARTUP: scan Supabase → report state → identify pending items
    ↓
WORK:   execute tasks
    ↓
CHECKPOINT (per task): record to session_checkpoints → close previous checkpoint → update supermemory
    ↓
SHUTDOWN (end of session): consolidate everything → update TOC
```

---

# PART 1 — STARTUP (session opening)

## ⚠️ RULE #1 — BEFORE ANY CURL: Get the service_role_key

The Hermes configuration has `redact_secrets: true`. This means `grep`/`cat`/`read_file`
on `secrets.env` SHOW A REDACTED VERSION with `***`, **not the real value**.

### The mistake you will make if you skip this

You will `grep SUPABASE_SERVICE_ROLE_KEY secrets.env`, see
`sb_secret_***Ilff`, and write in your curl:

```bash
curl -H "Authorization: Bearer ***   # THIS CAUSES PGRST301
```

`$SUPAB...EY` is NOT a defined variable. It is the redacted text
you visually copied. The shell does not expand it → literal value
`Bearer ***` → JWT with 1 part instead of 3 → `PGRST301`.

### The fix (lasts forever)

```bash
# ALWAYS source the file first
source ~/.hermes/secrets.env

# Use the CORRECT variable name — it exists and the shell expands the real value
curl -s "$SUPABASE_URL/rest/v1/session_checkpoints?select=count" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Prefer: count=exact"   # ✅ WORKS
```

### Verification test

```bash
source ~/.hermes/secrets.env
echo "len: ${#SUPABASE_SERVICE_ROLE_KEY} start: ${SUPABASE_SERVICE_ROLE_KEY:0:3} end: ${SUPABASE_SERVICE_ROLE_KEY: -3}"
# Should show ~41 chars, sb_, and 3 real chars without ***
```

---

## When to run

**Always** at the start of every session. First action. Non-negotiable.

⚠️ **ENFORCEMENT RULE (after failure on 05/25):**
- If the user asks a question on the first turn before the scan has been executed,
  I MUST respond EXCLUSIVELY with: "Please wait, I need to run the Supabase scan first."
  and ONLY THEN make the scan tool calls.
- The scan MUST PRECEDE any substantive response.
- NO response to the user before the scan is complete.
- If the user says "What were we working on?" → scan first, answer after.

## Step 1 — General state scan (parallel)

Call ALL of these MCP tools in parallel on the first turn.
**IMPORTANT:** the tool calls MUST be the first content in the response. Do not write text before the calls.

```python
mcp_tech_kb_get_kb_summary()
mcp_code_analyzer_get_code_analyzer_summary()
mcp_product_catalog_list_products()
mcp_escape_catalog_get_catalog_summary()
```

## Step 2 — Fetch pending checkpoints

After sourcing secrets.env, query:

```bash
curl -s "$SUPABASE_URL/rest/v1/session_checkpoints?select=id,project,territory,vector_intent,next_step,status,operating_mode&status=eq.pending&deleted_at=is.null&order=occurred_at.desc&limit=10" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY"
```

Useful fields: `id`, `project`, `territory`, `vector_intent`, `next_step`,
`status`, `operating_mode`, `discovery`, `consolidated_insights`, `tags`

**Note:** `session_checkpoints` supersedes `thoughts` with `entry_type = 'task_checkpoint'`.
`thoughts` is exclusively an input funnel (loose ideas, unclassified).

## Step 3 — Report to the user

```
=== SUPABASE STARTUP ===
📚 tech_kb:     <N> entries (latest: <name>)
🔧 code-analyzer: <N> projects, <N> snapshots
📦 products:     <N> active
🧩 escape rooms: <N> rooms
📋 pending:      <N> open checkpoints (session_checkpoints)
```

If any call fails: report as ⚠️ and continue.

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

## Expected behavior

- **Always** record a checkpoint after completing a task
- **Always** include all 5 identity fields — without them the checkpoint
  is useless for context rehydration
- **Always** include `next_step` — without it the checkpoint provides no direction
- **Always** close the previous pending checkpoint
- **Never** record an empty checkpoint ("I worked" with no content)

---

# PART 3 — SHUTDOWN (end of session)

## When to run

When detecting the session is ending:
- User types `/quit`, `/exit`, `/new`
- User explicitly says "I'll stop here", "see you tomorrow", "good night"
- After prolonged inactivity (session timeout)

## What to do

1. Save checkpoint with all 5 identity fields
2. Close previous pending checkpoint (UPDATE status='completed')
3. Update Supermemory with summary
4. Update TOC in tech_kb if there were structural changes

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

## Integration with regras-de-ouro (golden rules)

- **R22**: executable implementation — Supabase first, always
- **R8**: documented skill covering the domain, validated by the user
- **R4**: visible state checklist before starting
- **R10**: authorization waited for without timeout during scan
- **R24**: multi-system overview before answering about pending items

## Pitfalls

1. **Forgetting to run** — the protocol MUST be the first block of tool calls
2. **Skipping it when the user already gave a specific task** — run the scan first
3. **Assuming you "remember"** — do not trust session memory. Query Supabase.
4. **Checkpoint without `next_step`** — useless. Always fill it in.
5. **Shutdown without consolidating** — at least the last checkpoint was saved.
6. **Supermemory full** — prioritize most recent checkpoint and next_step.
7. **NEVER** `grep/read_file` on secrets.env — the value is redacted.
   ALWAYS `source ~/.hermes/secrets.env` and use `$SUPABASE_SERVICE_ROLE_KEY`
   (which is the REAL variable name, not a redacted text).

## Pitfall of Editing Hermes Config — Consult tech_kb `81c48035`

🔗 **tech_kb entry `81c48035`** — "Hermes Config.yaml + .env Editing
   Protocol — All Pitfalls"
