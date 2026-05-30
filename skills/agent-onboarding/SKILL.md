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
| context-bridge | Skill | Multi-source context injection (tech_kb, session_search, memory, session_checkpoints) |
| checkpoint-workflow | Skill | Session checkpoint lifecycle — STARTUP reidratation, SAVE with 5 identity fields, SHUTDOWN close cycle |
| session_checkpoints | Supabase table | Intentional marks in the agent's representation space: territory, operating_mode, vector_intent, discovery, consolidated_insights. Not logs — identity structure that rehydrates next session. |
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

Runs the **full MBTI Guru test** — all questions, all levels, identical
content to the original. The only difference is the delivery channel:
OpenClaw runs it via CLI (`mbti.py`), Hermes runs it in conversation.

Protocol:
1. ASK: "Do you know MBTI? Know your type?"
2. EXPLAIN if needed: "MBTI has 4 dimensions:
   - Energy: Extraversion (E) vs Introversion (I)
   - Information: Sensing (S) vs Intuition (N)
   - Decisions: Thinking (T) vs Feeling (F)
   - Structure: Judging (J) vs Perceiving (P)
   16 types total."
3. IF KNOWN: "What's your type?" → validate with 4 quick questions
4. IF UNKNOWN: "MBTI Guru offers 4 test versions:
   1. Quick (70 questions, ~10 min)
   2. Standard (93 questions, ~15 min)
   3. Extended (144 questions, ~25 min)
   4. Professional (200 questions, ~35 min)
   Which do you prefer?"

   **MBTI Guru Hermes** (`skills/workflow/mbti-guru-hermes/`) — Stage 1C:
- `questions_pt_BR.py` — 200 perguntas em português (4 versões: 70, 93, 144, 200)
- `scorer.py` — scoring idêntico ao Guru original (proporção por dimensão, clarity = abs(score-50)*2)
- `types_pt_BR.py` — 16 tipos com descrições completas em pt-BR
- `run_mbti_test.py` — módulo autônomo para execução sem interação conversacional
- SKILL.md — protocolo conversacional + modo autônomo

**How to invoke in conversation:**
```python
import sys
sys.path.insert(0, '/home/djairguilherme/.hermes/skills/workflow/mbti-guru-hermes')
from questions_pt_BR import get_questions, get_question_count
from scorer import calculate_type, format_scores, calculate_clarity
from types_pt_BR import get_type

questions = get_questions(70)  # or 93, 144, 200
# Ask one by one, accumulate [(q_id, "A"|"B"), ...]
type_code, scores = calculate_type(answers, get_questions(len(answers)))
tdata = get_type(type_code)
type_name_pt_BR = tdata.get("name_pt_BR", type_code)
```

No CLI, no script — pure conversation with the Hermes agent
acting as the test administrator.

5. After answers → calculate score per dimension → determine type
6. **pt-BR is required for type descriptions.** The Guru's original files
   have only `_cn` and `_en` fields. You MUST present type descriptions in
   **Brazilian Portuguese** during the conversation. The `types_pt_BR.py`
   file has every type with `name_pt_BR`, `summary_pt_BR`, `strengths_pt_BR`,
   `weaknesses_pt_BR`, and `careers_pt_BR`. Use `get_type().get("field", "")`
   to retrieve them.
   English or Chinese output alone is a format violation for this user.
7. Register in user_mbti + update user_profiles.mbti_type

**Scoring logic (identical to MBTI Guru):**
- Each dimension (E/I, S/N, T/F, J/P) has N questions
- Each answer scores toward one pole
- The pole with more answers is the result
- Confidence = (difference / total) * 100
- Register: ei/sn/tf/jp + source='quick_test|standard_test|extended_test|professional_test'
- Generate full type summary from MBTI Guru's type descriptions

**MBTI Guru** (in referencias/mbti-guru/):
- SKILL.md — original skill documentation
- DESIGN.md — question distribution by version and dimension
- mbti.py — CLI entry point (OpenClaw version, not used by Hermes)
- lib/questions/ — all 200 questions by version and dimension
- lib/scoring/ — scoring and type determination

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

**Skill:** `stage-3-financial` (skills/workflow/stage-3-financial/)

Data-driven stage: CSV import → MBTI-based profile → goals → strategies.

### What Exists (built and running)

| Component | Type | Location |
|-----------|------|----------|
| `mbti_financial_profiles.py` | Python module | 16 perfis financeiros MBTI em pt-BR com assess_financial_personality() |
| `csv_importer.py` | Python module | Importador de CSV bancário (Nubank, Itaú, Inter, Caixa, genérico) |
| SKILL.md | Skill doc | Protocolo conversacional completo para Stage 3 |
| supabase-finance MCP | 17 MCP tools | Contas, transações, categorias, metas, orçamentos |
| supabase-worklog MCP | Work log tools | Registro de trabalho com valor financeiro |

### 3A — CSV Import (csv_importer.py)

1. ASK: "Want me to analyze your bank statements in CSV?"
2. Detect format automatically by header (Nubank, Itaú/Inter, Caixa, Generic)
3. SHOW preview: format detected, period, summary, expense breakdown
4. CONFIRM before importing to Supabase via REST API
5. Categorize transactions automatically using keyword matching (word-boundary)

### 3B — MBTI × Financial Profile (mbti_financial_profiles.py)

After MBTI is known (Stage 1C):

1. "Your type is {type_code} — {name_pt_BR}. Want to see how this affects your finances?"
2. Show profile: strengths, weaknesses, saving_style, spending_style, risk_profile
3. Ask 4 calibration questions about financial behavior
4. Call `assess_financial_personality(answers, type_code)` for observations + recommendations

### 3C — Goals

1. Short (6mo), Medium (2yr), Long (5yr+)
2. Register via `mcp_supabase_finance_add_goal()`
3. Show progress indicators for each goal type

### 3D — Adapted Strategies

Combine MBTI profile + goals into actionable recommendations:
- Automated saving rules
- Investment allocation suggestions
- Emergency fund targets
- Spending guardrails (e.g., "sleep on it" rule for ENFPs)

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

2. **MBTI Guru runs complete** — All 70/93/144/200 questions, identical to
   the original. The only change is the execution channel: conversation
   (Hermes) instead of CLI (OpenClaw). Read questions from
   referencias/mbti-guru/lib/questions/.

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
- checkpoint-workflow — Checkpoint lifecycle protocol
- session_checkpoints — Table in Supabase
- golden-rules — R0b, R22, R28
- **mbti-guru-hermes** (`skills/workflow/mbti-guru-hermes/`) — Stage 1C full implementation
- career-mapping — Stage 1D (biography interview)
- work-operating-model — Stage 2 (operational interview)
- supabase-finance — Stage 3 (17 MCP tools)
- **stage-3-financial** (`skills/workflow/stage-3-financial/`) — Stage 3 full implementation
  - mbti_financial_profiles.py (16 profiles × MBTI in pt-BR)
  - csv_importer.py (4 bank formats, preview → confirm → import)
- SECURITY.md — RLS/GRANT/auth.jwt() protocol
