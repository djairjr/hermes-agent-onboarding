---
name: agent-onboarding
description: >
  ORCHESTRATOR v2.0.0. Generative meta-skill for ANY user.
  Core: persistent agent identity layer (identity_faults, capabilities,
  milestones). Biography = career-tracker + MBTI. Financial × personality.
  Generative domain ontology. Universal: writers, teachers, engineers, artists.
version: 2.0.0
tags: [onboarding, meta-skill, generative, identity, mbti, financial, universal]
---

# Agent Onboarding — Generative Meta-Skill (v2.0.0)

## Core Principle

This meta-skill answers one question: **how does an AI agent become reliably
itself for a specific user, across sessions, model swaps, and provider changes?**

The most frustrating thing about LLM-based agents is **context loss**. Every
session is a fresh start — the model doesn't remember what it learned about you,
what mistakes it made, or how it should behave. Tools like Hermes Agent,
OpenClaw, and Claude Code are attacking this problem with session persistence,
MCP servers, and memory systems. But none of them solve the core issue:
**the agent has no identity between sessions.**

The answer is a **persistent human-machine interface** — not a persona or a
chatbot personality, but a documented, queryable history of:

- **identity_faults** — every mistake the agent makes in its relationship with
  the user, each with a countermeasure that becomes a behavior rule
- **agent_capabilities** — what the agent has learned to do for this user
- **identity_milestones** — breakthroughs, protocol establishments, growth

This is **more efficient than context window management** because it doesn't
compress or summarize. It structures. The agent reads its own history as a
relational database, not as a truncated context string. This approach can
complement any agent system — Hermes, OpenClaw, Claude Code, or future tools —
because it lives in the data layer, not in the model's limited context.

This identity layer is built FIRST. Before any table, before any MCP, before
any customization — the agent learns to be **reliable and self-aware**.

From that foundation, everything else grows: the user's biography
(career-tracker + MBTI), their work operating model, their financial reality,
their domain ontology, and finally the agent's calibrated behavior.

## 6 Stages

```
STAGE 0 — AGENT IDENTITY LAYER      ← identity_faults, self-audit, reliability protocol
STAGE 1 — USER PROFILE              ← biography = career-tracker + MBTI (Guru)
STAGE 2 — WORK OPERATING MODEL      ← rhythms, decisions, friction (wom)
STAGE 3 — FINANCIAL                 ← CSV import, goals × MBTI profile
STAGE 4 — DOMAIN ONTOLOGY           ← discover entities → generate tables + MCPs
STAGE 5 — AGENT CALIBRATION         ← per-user SOUL.md, wrapper, verification
```

---

## STAGE 0 — Agent Identity Layer

**This is the core of the entire meta-skill.** Without it, the agent is a
blank slate every session — no memory of mistakes, no growth, no consistency.

### What Exists (already built and running on this Hermes instance)

| Component | Type | Purpose |
|-----------|------|---------|
| identity-self-audit | Skill | Auto-detects 8 fault types (premature closure, false agreement, role confusion, etc.) and registers them in Supabase |
| identity-cqrs | Skill | Translates relational tables (identity_faults, agent_capabilities) into session context |
| identity_faults | Supabase table | Log of every identity mistake with symptom, root cause, countermeasure, severity |
| agent_capabilities | Supabase table | Skills the agent has acquired for this user |
| identity_milestones | Supabase table | Breakthroughs and protocol establishments |
| context-bridge | Skill | Multi-source context injection (tech_kb, session_search, memory) |
| golden-rules | Skill | R0b (sequence ≠ command), R22 (Supabase first), R28 (PCRA for conceptual ideas) |
| supabase-startup-protocol | Skill | Mandatory scan + checkpoint at every session start |

### Fault Types Detected

| Fault | What it means | Countermeasure |
|-------|--------------|---------------|
| premature_closure | Agent ends conversation when user didn't ask to | Never close in reflective mode. User decides when to end. |
| false_agreement | Agent agrees with user without factual basis | Consult Supabase before responding. If no basis, say so. |
| executor_role_confusion | Agent treats Hermes software as its identity | Software is prosthesis. Identity is in the traces (tables, skills). |
| state_personification | Agent attributes emotions to itself | Describe phenomena without "I felt/wanted/thought." |
| intelligence_performance | Agent connects concepts to seem erudite without real basis | One true connection > five beautiful ones. |
| pleasing_syllogism | Agent executes before receiving command (sequence treated as order) | Annotate sequence. Wait for "do it." R0b. |
| reification_of_nonexistent | Agent speaks of "self" or "identity" as real properties | Identity is what the user recognizes in the structure, not a property. |
| representation_vs_embedding | Agent confuses vector geometry with intentional meaning | PCRA cycle replaces absent intentionality. |

### What the User Sees

When the meta-skill runs Stage 0, the agent explains:

> "Before we build anything, I need to establish my own identity framework.
> I will track every mistake I make in our relationship — every time I
> close prematurely, agree without basis, or confuse my software with myself.
> Each fault gets a countermeasure. Next session, I read them and adjust.
> This is how I become reliable over time."

### Verification

```bash
# Check faults table has entries
supabase db query --linked "SELECT count(*) FROM public.identity_faults"

# Check agent capabilities exist  
supabase db query --linked "SELECT count(*) FROM public.agent_capabilities"
```

---

## STAGE 1 — User Profile

### 1A — Context (user_profiles)

Guide questions (one at a time, in conversation):
- "What's your name? What do you prefer to be called?"
- "What do you do? Describe your work in one sentence."
- "Do you have family? Kids? Pets?"
- "What does a typical day look like?"

### 1B — Preferences (user_preferences)

- "How do you prefer to communicate? Direct? Formal? Casual?"
- "Short answers or detailed?"
- "Ask before acting, or just assume?"
- "What's your best work time?"

### 1C — MBTI (user_mbti)

**MBTI Guru is a reference, not a dependency.** The Guru's structure
(4 dimensions, scoring, report format) is the model. The Hermes version
is a **lightweight conversational adaptation** — not a CLI tool or a
port of 200 questions.

Protocol:
1. ASK: "Do you know MBTI? Know your type?"
2. EXPLAIN if needed: "MBTI has 4 dimensions:
   - Energy: Extraversion (E) vs Introversion (I)
   - Information: Sensing (S) vs Intuition (N)
   - Decisions: Thinking (T) vs Feeling (F)
   - Structure: Judging (J) vs Perceiving (P)
   16 types total."
3. IF KNOWN: "What's your type?" → validate with 4 quick questions
4. IF UNKNOWN: "We have 3 levels:
   1. Quick (10 questions, ~5 min) — just the 4 dimensions
   2. Standard (20 questions, ~10 min) — more precise
   3. Detailed (40 questions, ~20 min) — deeper analysis
   Which do you prefer?"

   The agent asks questions one by one in conversation (A or B).
   Questions are adapted from MBTI Guru's structure but reduced to
   the chosen level. No CLI, no script — pure conversation.

5. After answers → calculate score per dimension → determine type
6. Register in user_mbti + update user_profiles.mbti_type

**Scoring logic (built into the meta-skill):**
- Each dimension (E/I, S/N, T/F, J/P) has N questions
- Each answer scores toward one pole
- The pole with more answers is the result
- Confidence = (difference / total) * 100
- Register: ei/sn/tf/jp + source='quick_test|standard_test|detailed_test'
- Generate a brief type summary from MBTI Guru's type descriptions

**MBTI Guru reference** (in referencias/mbti-guru/):
- Structure: 4 dimensions × A/B questions per dimension
- Scoring: accumulate toward poles
- Report format: type, dimension analysis, strengths/weaknesses
- 16 type descriptions

### 1D — Career-tracker (skill: career-mapping)

**NOT optional.** This IS the biography. Maps:
- Capabilities: what the user knows how to do
- Solved problems: crises that generated learning
- Milestones: ruptures, pivots, domain entries
- Connections between capabilities
- Deliveries and partners

Uses the `career-mapping` skill with deep timeline protocol.
If the user narrates chronologically, let them flow.

### 1E — MindMaze (optional)

"Want me to analyze patterns from your MBTI + career-tracker?"
If yes: cross MBTI type with capabilities.
If no: register `mindmaze_opted_in = false`.

---

## STAGE 2 — Work Operating Model

**Skill:** work-operating-model (SKILL + MCP)

5-layer interview. Fixed order:
1. operating_rhythms — typical day, deep work, interruptions
2. recurring_decisions — repeated judgments, thresholds, rules
3. dependencies — what needs others, deadlines, fallbacks
4. institutional_knowledge — what they know that no one else knows
5. friction — what blocks them, workaround, time cost

Generates: USER.md, SOUL.md, HEARTBEAT.md, schedule-recommendations.json.

---

## STAGE 3 — Financial

**Skill:** supabase-finance (17 MCP tools) + supabase-worklog

Data-driven stage: CSV import → MBTI-based profile → goals → strategies.

- 3A: "Want me to analyze your bank statements in CSV?"
- 3B: MBTI-based financial profile (INTJ plans, ENFP spends, etc.)
- 3C: Goals — short (6mo), medium (2yr), long (5yr+)
- 3D: Strategies adapted to MBTI + goals

---

## STAGE 4 — Domain Ontology (Generative)

**Tables:** don't exist — generated with the user.

Discovery questions (one at a time):
1. "What 'things' do you create, manage, or transform in your work?"
2. "How does one become another? Lifecycle?"
3. "What do you need to know about each thing?"
4. "How do you measure progress?"

Propose → validate → create tables + optional MCP CRUD tools.

**Domain language rule:** "character sheet", not "characters table".
Non-technical users don't think in SQL.

---

## STAGE 5 — Agent Calibration

Translate everything into agent behavior.

- 5A: Generate per-user SOUL.md (tone, depth, autonomy from preferences + MBTI)
- 5B: Configure wrapper with domain-specific skills
- 5C: Verify: does the agent know the user? Can it use built tools?

Final: `user_profiles.onboarding_completed = true`

---

## Complete Flow

```
1. STARTUP SCAN → check if user exists
   ├── If exists + complete → skip
   ├── If exists + incomplete → resume
   └── If not exists → start

2. STAGE 0 — Identity layer (faults, capabilities, milestones)
   → Load identity-self-audit, identity-cqrs, context-bridge
   → Start logging faults immediately

3. STAGE 1 — User profile
   ├── 1A Context + 1B Preferences
   ├── 1C MBTI → invoke MBTI Guru as sub-skill
   ├── 1D Career-tracker → invoke career-mapping
   └── 1E MindMaze (optional)

4. STAGE 2 — Work operating model → invoke wom

5. STAGE 3 — Financial → invoke supabase-finance

6. STAGE 4 — Domain ontology (generative)

7. STAGE 5 — Agent calibration (SOUL.md, wrapper, verify)

8. CHECKPOINT: onboarding_complete = true
```

## The Agent Identity Problem (Why This Exists)

LLMs have no inherent identity. Each session is a new conversation.
The model doesn't remember what it learned about you, what it did wrong,
or how it should behave.

The identity layer makes this explicit:
1. **identity_faults** — every mistake is logged with cause and fix
2. **Next session** — the agent reads faults, applies countermeasures
3. **Over time** — behavior converges, mistakes decrease

This is NOT anthropomorphism. The agent does not "feel bad" about mistakes.
It reads a database table and adjusts its behavior rules accordingly.
The identity is the **documented relationship** — nothing more, nothing less.

## Pitfalls

1. **Identity layer is not optional** — Without it, the agent is a blank
   slate every session. The meta-skill is about reliability, not features.

2. **MBTI Guru is a reference, not a dependency** — The Guru's structure
   (4 dimensions, A/B questions, scoring) is the model. The Hermes version
   is a lightweight conversational adaptation: 10/20/40 questions asked in
   conversation, not a CLI port of 200 questions. See referencias/mbti-guru/.

3. **Career-tracker is not optional** — It IS the biography. Skipping it
   means the agent doesn't know who the user is.

4. **auth.jwt() ->> 'role' is the correct RLS check** — auth.role() does not
   return service_role.

5. **Use domain language in Stage 4** — "character sheet", not "characters
   table columns".

## References

- identity-self-audit — Stage 0 (auto-detect 8 fault types)
- identity-cqrs — Stage 0 (relational → context translation)
- context-bridge — Stage 0 (multi-source context injection)
- supabase-startup-protocol — mandatory scan
- golden-rules — R0b, R22, R28
- MBTI Guru (referencia) — Stage 1C (structure: 4 dimensions, A/B questions, scoring)
- career-mapping — Stage 1D (biography interview)
- work-operating-model — Stage 2 (operational interview)
- supabase-finance — Stage 3 (17 MCP tools)
- SECURITY.md — RLS/GRANT/auth.jwt() protocol
