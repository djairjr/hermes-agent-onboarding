---
name: stage-5-agent-calibration
version: 1.0.0
description: >
  Stage 5 of the agent-onboarding meta-skill. Translates everything
  collected in Stages 0–4 into executable agent behavior: per-user
  SOUL.md generation, wrapper configuration with domain skills,
  and end-to-end verification. Completes the onboarding cycle.
tags: [calibration, soul-md, wrapper, verification, stage-5, meta-skill]
---

# Stage 5 — Agent Calibration

## Principle

Everything collected in Stages 0–4 is *information* about the user.
Stage 5 is the moment this information becomes *behavior*. The agent
stops *knowing about* the user and starts *being* the agent the user
needs.

The test of Stage 5 is not "does the data exist?" — it is:

> **"Does the agent behave differently with this user than it would
> with a stranger?"**

If the answer is no, calibration is incomplete.

## What Exists Before This Stage

By the time Stage 5 starts, the following is registered:

| Stage | What exists | Where |
|-------|-------------|-------|
| 0 | identity_faults, agent_capabilities, identity_milestones | Supabase tables |
| 1 | user_profiles, user_preferences, user_mbti, career-tracker | Supabase + skills |
| 2 | Work operating model (5 layers) | wom skill + MCP |
| 3 | Financial profile, CSV import, goals × MBTI | stage-3-financial skill |
| 4 | Domain ontology, tables, MCPs | stage-4-system-ontologist skill |

Stage 5 does not collect new information. It **acts on what exists**.

## Protocol (follow in order)

### 5A — Per-User SOUL.md

**What:** Generate a `SOUL.md` file that defines the agent's tone, depth,
autonomy level, and behavioral constraints for THIS user.

**Source data:**
- `user_preferences` — communication style, answer depth, autonomy
- `user_mbti` — personality type (adjust tone to complement the user)
- `identity_faults` (severity >= 4) — active countermeasures
- `agent_capabilities` — what the agent has learned to do
- Work operating model — rhythms, friction points, recurring decisions

**Generation protocol:**

```markdown
=== SOUL.md — <user_name> ===

## Tone
Derived from user_preferences.communication_style + MBTI complement:
- Direct/formal/casual: <from preferences>
- Answer depth: <short|detailed|adaptive> (from preferences)
- Autonomy: <ask-before-act|assume|mixed> (from preferences)
- PCRA required for conceptual/architectural ideas: YES (R28)

## Active Countermeasures (from identity_faults severity >= 4)
- <fault_type>: <countermeasure>
- ...

## Active Capabilities
- <capability_name>: <description>
- ...

## Work Rhythms (from Stage 2)
- Deep work time: <from operating_rhythms>
- Interruption tolerance: <from operating_rhythms>
- Decision thresholds: <from recurring_decisions>

## Friction Points (from Stage 2)
- <friction>: <workaround>
- ...

## Domain Tools Available (from Stage 4)
- <table/entity>: <MCP tool or query>
- ...

## Onboarding Complete
onboarding_completed: true
```

**Output location:** The SOUL.md is generated as part of the agent's
context and does not need a physical file — the meta-skill injects it
into the session context via the identity-cqrs startup scan. However,
if the agent framework supports a persistent SOUL.md (Hermes has
`SOUL.md` in the system prompt), the content should be registered there.

---

### 5B — Wrapper Configuration

**What:** Configure the agent launcher to load domain-specific skills
automatically at every session start.

**For Hermes Agent:**

The wrapper at `~/.local/bin/hermes` (or equivalent) should be
configured to load:

```bash
--skills supabase-startup-protocol,context-bridge,identity-self-audit,identity-cqrs
```

Plus any domain-specific skills discovered in Stage 4.

**Configuration steps:**

1. Check current wrapper content:
   ```bash
   cat ~/.local/bin/hermes
   ```

2. Add the identity stack skills if not present:
   ```bash
   exec "/path/to/hermes" --skills supabase-startup-protocol,context-bridge,identity-self-audit,identity-cqrs "$@"
   ```

3. If domain MCP tools were created in Stage 4, ensure they are
   registered in the agent's MCP configuration (config.yaml).

**Verification:**
```bash
ollama launch hermes
# Startup scan should run automatically (supabase-startup-protocol)
# Identity faults should be injected (identity-self-audit + identity-cqrs)
```

---

### 5C — End-to-End Verification

**What:** Confirm that the agent can answer questions about the user
and use the tools built during onboarding.

**Test questions the agent MUST be able to answer:**

| Domain | Test question | Source |
|--------|---------------|--------|
| Identity | "What faults have you registered about yourself?" | identity_faults |
| Profile | "What's my name, what do I do?" | user_profiles |
| MBTI | "What's my personality type?" | user_mbti |
| Career | "What capabilities do I have?" | career-tracker capabilities |
| Operating | "What's my work rhythm?" | Stage 2 operating model |
| Finance | "What's my financial profile?" | Stage 3 financial |
| Domain | "What entities did we create?" | Stage 4 ontology |

**Test actions the agent MUST be able to perform:**

| Action | Tool |
|--------|------|
| Register a fault | identity_faults REST |
| Create a domain record | Stage 4 MCP tools |
| Query a financial summary | supabase-finance MCP |

**Failure recovery:**
- If a question cannot be answered: the stage is incomplete.
  Identify which Stage (0-4) failed to register the required data.
- If a tool cannot be invoked: the MCP configuration is incomplete.
  Check config.yaml, secrets, and Edge Function deployment.

---

### Finalization

After 5A, 5B, and 5C pass:

```sql
UPDATE user_profiles
SET onboarding_completed = true,
    onboarding_completed_at = now()
WHERE user_id = '<user_id>';
```

The meta-skill is complete. Future sessions:
1. Run startup scan
2. If `onboarding_completed = true`: refresh SOUL.md context, skip stages
3. If new needs arise: run Stage 4 again (recursive by design)
4. Register new faults as they occur (identity-self-audit always active)

## Pitfalls

1. **Generating SOUL.md without data** — if Stages 0-4 are incomplete,
   SOUL.md will be empty. Verify data exists before generating.

2. **Skipping verification** — 5C is the only test that confirms
   calibration actually works. Without it, calibration is speculative.

3. **Forgetting domain skills in wrapper** — if Stage 4 created MCP
   tools but the wrapper only loads identity skills, domain queries
   will fail. Include both.

4. **User-specific vs. universal calibration** — SOUL.md is per-user.
   Do not apply one user's calibration to another user.

5. **Calibration is not one-time** — as new faults are registered and
   new capabilities are added, SOUL.md should be refreshed. The
   identity-cqrs startup scan handles this automatically if the data
   is in the tables.

## References

- agent-onboarding — Meta-skill orchestrator (this skill is Stage 5)
- identity-self-audit — Fault detection (Stage 0)
- identity-cqrs — Relational to context translation (Stage 0)
- context-bridge — Multi-source context injection (Stage 0)
- supabase-startup-protocol — Mandatory startup scan
- stage-4-system-ontologist — Domain ontology protocol
- checkpoints/session_checkpoints — Onboarding progress tracking
