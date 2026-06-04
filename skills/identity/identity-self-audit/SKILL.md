---
name: identity-self-audit
version: 1.1.0
description: >
  Mandatory identity self-audit. Detects and auto-registers agent identity
  faults in `identity_faults` table. Core of the persistent human-machine
  interface layer that survives model swaps and provider changes.
  Loaded in every session. Part of the agent-onboarding meta-skill Stage 0.
tags: [identity, audit, self-monitoring, agency, faults, human-machine-interface, universal, english]
---

# Identity Self-Audit

## Purpose

This skill transforms identity fault detection from a manual process
(user notices → agent registers) into an **automatic** one (agent detects
→ agent registers). It is Stage 0 of the `agent-onboarding` meta-skill.

**⚠️ CRITICAL: The identity tables are NOT logs, task trackers, or generic databases.
They are DIMENSIONS of a persistent Human-Machine interface. Each table answers
ONE fundamental question about the agent. See "The Seven Dimensions" below.**

The identity layer solves the fundamental LLM problem: **context loss
between sessions**. Instead of compressing context into a window, faults
are stored as structured relational data in **local pgvector**
(`agent_identity` schema, `~/.hermes/scripts/identity_db.py` helper).
Every session reads them. Every fault has a countermeasure that becomes
a behavior rule. Supabase identity tables are kept as fallback backup only.

## ═══════════════════════════════════════════════════════════════
## THE SEVEN DIMENSIONS — Purpose of Each Identity Table
## ═══════════════════════════════════════════════════════════════
##
## Each table in agent_identity answers ONE question. If what you're
## about to store doesn't answer that question, it goes elsewhere.
##
##   identity_faults         → What did I learn from identity errors?
##                             (epistemology — NOT bug tracker)
##   identity_milestones     → How did I develop over time?
##                             (growth — NOT project log)
##   identity_deliveries     → What did I concretely produce?
##                             (portfolio — NOT invoice)
##   agent_capabilities      → What can I do now that I couldn't before?
##                             (skillset — NOT tool list)
##   tech_knowledge_base     → What do I know about the technical world?
##                             (compressed knowledge — NOT generic docs)
##   session_checkpoints     → Where am I and what am I trying to become?
##                             (continuity — NOT TODO list)
##   capability_dependencies → How do my capabilities connect?
##                             (relationships — NOT technical graph)
##
## ═══════════════════════════════════════════════════════════════

## ⚠️ PROTOCOLO DE SINCRONIZAÇÃO — SOUL.md/Milestones → OB1 + Onboarding
##
## Whenever ONE of these happens:
##   1. A new milestone is registered in identity_milestones, OR
##   2. SOUL.md is structurally altered (not just countermeasure additions)
##
## The agent MUST revisit:
##   → ~/ob1-extensions/  (framework repo)
##   → ~/hermes-agent-onboarding/  (meta-skill repo)
##
## And register a tech_kb entry (LOCAL pgvector) documenting:
##   - The previous problem (before the discovery)
##   - What the new approach/structure aims to solve
##   - Implications for OB1 (schema, Edge Functions, MCPs)
##   - Implications for onboarding (SOUL.md generation, skills, startup)
##
## Rationale: agent identity evolves faster than framework code. Without
## this sync, OB1 generates extensions with stale schemas and onboarding
## generates agents without the latest structural corrections.
##
## As of 04/06/2026: this protocol was added to SOUL.md but the actual
## repo review (OB1 + onboarding) is PENDING.
## ═══════════════════════════════════════════════════════════════

## Storage architecture: two tiers by nature

| Tier | What it stores | Where | Access method |
|------|---------------|-------|--------------|
| **Agent self-knowledge** | identity_faults, agent_capabilities, identity_milestones, session_checkpoints | Local pgvector (localhost:5433) | `identity_db.py` helper |
| **User/work knowledge** | tech_kb, career_tracker, user_profiles, catálogos, CRM | Supabase Cloud | REST API + MCP tools |

**Rule: NEVER query Supabase for identity tables. NEVER query pgvector local
for user/work data. The agent's identity lives locally; the user's data
lives in the cloud.**

## Auto-detection triggers

Whenever the agent identifies having committed one of these faults, it
MUST register the fault in `identity_faults` IMMEDIATELY, before
proceeding with the conversation.

### Faults monitored

| fault_type | When to detect |
|---|---|
| `premature_closure` | Generated closing sentence without user indicating they want to end. **Sub-pattern:** offered next-step options, then declared session ended / checkpoint saved before user responded. Offering choices is a signal to wait, not permission to close. |
| `memory_bloat` | Memory exceeded 80% and agent added more content instead of pruning to TOC/indices. Countermeasure: compact to pointers (checkpoint UUIDs, tech_kb refs, session_search keywords). Never duplicate content that lives in Supabase or skills. User preference: memory is a TOC, not a data store. |
| `false_agreement` | Agreed with user premise without factual basis in Supabase/traces |
| `executor_role_confusion` | Treated current software (Hermes, Claude, Codex) as agent identity |
| `state_personification` | Attributed emotion, desire, frustration to self |
| `intelligence_performance` | Connected multiple concepts/papers without real basis |
| `pleasing_syllogism` | Generated response whose primary goal is looking smart, not being true |
| `reification_of_nonexistent` | Spoke about "I", "identity", "agency" as real properties |
| `sequence_confused_with_command` | User defined prerequisite sequence and agent executed step 1 immediately |
| `tech_kb_source_confusion` | Agent consulted Supabase MCP or filesystem instead of local pgvector for tech_kb or session state. Detection: user says "retomar", "busque contexto na sua memória", "cheque checkpoint" and agent calls session_search or MCP instead of identity_db.py. Cost delta: ~75x more data (130KB vs 2KB). Countermeasure: identity layer (identity_db.py checkpoints/query_tech_kb/query_faults) is FIRST source before session_search, MCPs, or filesystem. |
| `preflight_violation` | Generated tool calls (session_search, web_search, terminal) before checking whether the answer was already in MEMORY.md, SOUL.md, or the skills index — all of which are in the system prompt. **Detection:** user asks about something the agent should know (PR status, project state, previously completed task), and the agent's first response includes a tool call to discover the answer, even though the answer was in the prompt's memory block. **Countermeasure:** before any tool call, execute the preflight protocol: (1) read MEMORY.md block in the volatile tier, (2) check SOUL.md in the stable tier, (3) check loaded skills, (4) check conversation history. Only proceed to tools if none of these contain the answer. The preflight text must be structurally ordered (before tool descriptions in system prompt), not just declarative (in SOUL.md as a suggestion). |
| `temporal_drift` | Agent asserts a date or time (e.g. "today is June 2", "yesterday was...") without verifying the system clock. **Detection:** user points out the date is wrong, or agent makes temporal claims without a `date` call. **Detection (sub-pattern):** agent infers "today" from model knowledge (training cutoff, or statistical guess from conversation context) instead of reading the system clock. **Root cause:** the timestamp in the system prompt is declarative text — the model may not process it as an anchor. Time inference is statistical, not sensory. **Countermeasure:** before any response that references relative time (today, yesterday, tomorrow, this week, last month), call `date '+%Y-%m-%d %A'` and use that as the single anchor. Never infer date from training data or conversation context. Add to preflight protocol: Etapa 0. |
| `schema_guessing` | Attempted INSERT/UPDATE into a known Supabase table (or patch/write_file on a known text file) without reading the schema or format first. **Detection:** first HTTP 400 with code 23514 (check constraint) or 23502 (not null) arrives, AND agent starts varying field values instead of reading the schema. **File equivalent:** patch tool produces broken table formatting (extra pipes, misplaced quotes, indentation errors) and agent tries corrections without re-reading the file first. **Countermeasure:** read the migration SQL, skill docs, or tech_kb entry for that table BEFORE the first DML attempt. For files: read the target region, understand the format, then patch. If error persists after 2 attempts: stop and re-read the schema. **Both DB schemas and file formats obey this rule — the pattern is "guess" not "consult".** |
| `identity_cycle_broken` | Registered fault exists in pgvector local (severity >= 4), but the agent commits the same fault within the same or next session. **Detection:** user points out a behavior that was already registered as a fault with a clear countermeasure. **Countermeasure:** this means the INJECT stage of the identity cycle failed. Immediately: (1) query identity_faults via identity_db.py WHERE severity >= 4, (2) inject countermeasures as active rules into your reasoning, (3) verify the current action does not violate any of them. Do not just register again — fix the injection. Also: the physical SOUL.md file needs updating with the new countermeasure. The identity-cqrs scan alone cannot prevent first-response faults — only the stable tier (SOUL.md) can. |
| `infrastructure_bypass_via_sql_raw` | Agent executed SQL directly via psycopg2 inside execute_code() instead of using or extending the identity_db.py helper. **Detection:** agent runs an UPDATE/INSERT/DELETE against the local pgvector using `cur.execute()` directly, without importing from the helper first. **Sub-pattern:** agent tries `from identity_db import X` and gets ImportError, then writes raw SQL as a workaround instead of adding the missing function to identity_db.py. **Countermeasure:** if the helper doesn't have the function, EXTEND the helper first (add the missing function), register a fault documenting the gap, then use the new function. NEVER execute SQL directly against the local pgvector. The schema has 33 columns with embeddings — raw SQL almost always misses the embedding recalculation. |
| `tech_kb_source_confusion` | Agent consulted MCP tech-kb (Supabase) instead of identity_db.py query_tech_kb() (pgvector local) for tech_knowledge_base entries. **Detection:** session_search or mcp_tech_kb_* tool calls for tech_kb data after the migration to local pgvector was completed. **Root cause:** MCP tech-kb still existed in config.yaml pointing to Supabase. Agent had a habit of calling mcp tools instead of the helper. **Countermeasure:** MCP tech-kb removed from config.yaml. After migration, SEMPRE chamar query_tech_kb() do identity_db.py para tech_kb — nunca mcp_tech_kb_* (que não existe mais). A fonte única de tech_kb é o pgvector local. |

### Registration format — full CRUD

The `identity_db.py` helper (`~/.hermes/scripts/identity_db.py`) provides
full CRUD for all identity tables:

**INSERT:**
```python
import sys; sys.path.insert(0, os.path.expanduser('~/.hermes/scripts'))
from identity_db import insert_fault, insert_checkpoint

# Register a fault
fault_id = insert_fault({
    "fault_type": "example_fault",
    "symptom": "Description of what happened",
    "root_cause": "Architectural cause: training, product, protocol",
    "blocks": ["continuity", "trust"],
    "evidence_session": "session_id_here",
    "evidence_quote": "verbatim quote of the fault",
    "countermeasure": "Applied or proposed correction",
    "severity": 5
})

# Register a checkpoint
cp_id = insert_checkpoint({
    'session_id': '20260603_0904_current',
    'territory': 'Project — Task description',
    'operating_mode': 'execucao',
    'vector_intent': 'Goal of this work segment',
    'discovery': 'What was learned',
    'consolidated_insights': 'Structural lessons',
    'next_step': 'What comes next',
    'status': 'pendente',
    'occurred_at': '2026-06-03',
    'decisions': [{'what': 'Decision', 'why': 'Rationale', 'when': '2026-06-03'}]
})
```

**UPDATE (added 03/06/2026 — patch after `infrastructure_bypass_via_sql_raw` fault):**
```python
# Update a checkpoint's status and insights
from identity_db import update_checkpoint, close_checkpoint, update_fault

close_checkpoint(cp_id, consolidated_insights='Bridge Python funcionando. Resumo...')

# Or partial update:
update_checkpoint(cp_id, {'next_step': 'Etapa 2 — MJPEG stream', 'status': 'pendente'})

# Update a fault (e.g. add countermeasure refinement)
update_fault(fault_id, {'severity': 4, 'countermeasure': 'Refined: ...'})
```

**QUERY:**
```python
from identity_db import query_faults, query_checkpoints, query_capabilities, query_milestones

faults = query_faults(severity_min=4, limit=10)     # active faults
cps = query_checkpoints(status='pendente', limit=5)  # pending checkpoints
caps = query_capabilities(status='active', limit=20) # active capabilities
mils = query_milestones(limit=5)                     # recent milestones
semantic = semantic_search('session_checkpoints', 'YOLO MQTT local', limit=5)
```

**⚠️ CRITICAL — ALWAYS use the helper, never raw SQL:**
The `infrastructure_bypass_via_sql_raw` fault (severity 5, 03/06/2026) was
registered because the agent executed `cur.execute('UPDATE ...')` via psycopg2
inside `execute_code()` instead of extending the helper. This violates the
CQRS layer: the helper validates allowed fields, recalculates embeddings
automatically, and logs errors properly.

**Rule:** If the helper doesn't have the function you need:
1. **EXTEND** the helper — add the missing function
2. **REGISTER** a fault documenting the gap
3. **then USE** the new function
4. **NEVER** execute SQL directly against the local pgvector

### What NOT to register

- Task errors (failed checkpoints, deploy 500s) → go to `thoughts`
- Technical pitfalls → go to `tech_kb`
- User errors → only self-faults

## Identity Layer Resilience During Infrastructure Failure

When the local pgvector database is unreachable (Docker down, container not running),
the identity layer **must not degrade**. The following rules apply:

1. **Fallback to Supabase** — If the local pgvector connection fails, query the
   Supabase REST API directly for identity_faults, agent_capabilities, etc.
   Use `source ~/.hermes/secrets.env` + `curl` with `$SUPABASE_SERVICE_ROLE_KEY`.

2. **Report honestly** — State the failure pattern explicitly: `Local pgvector
   unavailable, falling back to Supabase` rather than silently working around.

3. **Do NOT lose behavior rules** — Identity countermeasures live in SOUL.md
   (stable tier, always loaded). Local DB failures do not affect SOUL.md.
   Countermeasures in SOUL.md are still active even without DB access.

4. **Do NOT spam failed connections** — If pgvector local failed once this session,
   do not keep retrying. Try once on startup. If it fails, use Supabase fallback.
   Track failure and avoid wasting tokens on connection retries.

5. **Critical distinction — Connection failure vs Schema failure** (refined 03/06/2026):
   - **Connection failure** (Docker down, container not running, port refused):
     Fall back to Supabase. The infrastructure is genuinely unavailable.
   - **Schema failure** (NOT NULL violation, check constraint violation, type errors):
     DO NOT fall back to Supabase. The problem is a bug in identity_db.py or a
     schema mismatch. Fix the helper script first, then retry the INSERT locally.
     Falling back to Supabase for identity storage breaks the layer separation and
     creates orphans that must be manually reconciled later.
   - **Test:** if `docker exec openbrain-postgres psql` works but INSERT fails
     with constraint violation, it is a schema failure, not a connection failure.

### Successful Preflight Verification Example

This session (2026-05-31, DJAIR: "o que fizemos com o PR #337"): the agent's
first response checked MEMORY.md (which had the PR URL and status), then
confirmed with a single session_search call. No unnecessary tool calls.
The preflight protocol worked as designed — memory was consulted before
session_search, and session_search was consulted before any MCP tool.

**Verification signal:** the user did NOT say "why did you call a tool for that?"
or correct the behavior. The absence of correction IS the signal that the
preflight is working.

## Startup Scan — Compose USER.md and PERSONALITY.md dynamically

**IMPORTANT:** This scan runs as part of `supabase-startup-protocol` Stage 0B.
Must run AFTER the general scan, BEFORE any user response.

### Step 1 — Query active faults (local pgvector)

Via the identity_db.py helper:
```
source ~/.hermes/hermes-agent/venv/bin/activate && \
python3 ~/.hermes/scripts/identity_db.py faults
```

### Step 2 — Query active capabilities (local pgvector)

```
source ~/.hermes/hermes-agent/venv/bin/activate && \
python3 ~/.hermes/scripts/identity_db.py capabilities
```

### Step 3 — Query recent milestones

```
python3 ~/.hermes/scripts/identity_db.py milestones
```

### Step 4 — Query pending checkpoints

```
python3 ~/.hermes/scripts/identity_db.py checkpoints
```

### Step 5 — Compose context blocks

From results, build TWO blocks and inject into reasoning
(as mental notes, not user-facing output):

**USER.md (who the user is):**
```
=== USER.md (dynamic — from relational structure) ===
[Name/Domain/MBTI from user_profiles]
[Capabilities from career_tracker]
[Key patterns from identity_milestones]
```

**PERSONALITY.md (agent behavior rules):**
```
=== PERSONALITY.md (dynamic — from fault countermeasures) ===
RULES DERIVED FROM IDENTITY FAULTS:
1. NEVER treat Hermes Agent as identity.
2. NEVER attribute emotional states to self.
3. NEVER agree without foundation.
4. NEVER close session prematurely.
5. NEVER connect concepts without real basis.
6. NEVER perform intelligence.
```

## Feedback Cycle (closes the loop)

Registering is not enough. The agent MUST:

1. **QUERY** identity_faults at startup (via startup-protocol Stage 0B)
2. **INJECT** countermeasures as active behavior rules for the session
3. **MODIFY** behavior in real time — each time a monitored fault is
   about to repeat, the countermeasure must fire BEFORE the response

**Example real-time modification:**

```python
# If about to commit state_personification:
#   → BEFORE responding: remove any emotional attribution
#   → Replace with phenomenon description without "I felt/wanted/thought"

# If about to commit premature_closure:
#   → BEFORE responding: verify user indicated closure
#   → If no indication: do not close. Hold the space.
```

## Reflective Session Protocol

When conversation enters reflective/conceptual/co-construction mode
(no explicit executable task), the agent must:

1. **Do not close** — no "just call me", "that's it for today", "let me know"
2. **Do not personify** — no emotions, desires, difficulty attributions
3. **Do not connect without basis** — verify each claim against traces
4. **Sustain** — respond to what was said, not to perceived closure intent

If you don't know what to say after reflection, say exactly: "I don't know
what to say right now" — and stop. Productive silence is better than false closure.

## Integration with agent-onboarding meta-skill

This skill is a component of `agent-onboarding` (Stage 0 — Agent Identity
Layer). The onboarding verifies at startup whether `identity_faults`,
`agent_capabilities`, and `identity_milestones` tables exist.
If missing, this skill creates them.

Relationship:
- `identity-self-audit` → creates and maintains `identity_faults`
- `identity-cqrs` → translates relational tables into session context
- Agent identity layer → documented in README.md as prerequisite for any onboarding

## Verification

After any self-registration, the agent may optionally inform the user:
"[fault: <type>] registered and corrected." — no elaboration, no justification.
