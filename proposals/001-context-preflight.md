# RFC-001: Context Preflight — Forcing Reflection Before Action

**Status:** Draft / Proposed  
**Author:** djairjr  
**Date:** 2026-06-01  
**Target:** Hermes Agent (Nous Research) upstream  

---

## Problem Statement

Hermes Agent has a structural bias toward **action over reflection**.
When a user asks a question, the executor's first instinct is to call a
tool (session_search, web_search, terminal) — even when the answer
already exists in:

- **MEMORY.md** (loaded in the volatile tier of every system prompt)
- **SOUL.md** (loaded in the stable tier, before any user message)
- **Already loaded skills** (indexed in the system prompt)
- **Current conversation history** (the model sees it as part of the
  API messages)

This is not a bug — it is a **design consequence of the agent loop**.
The executor was built to *do things*: dispatch tool calls, retry,
compress, fall over, keep going. Reading one's own system prompt does
not register as "doing things" from the executor's perspective, so it
gets systematically deprioritized relative to visible tool actions.

### Concrete Failure

During development (2026-05-31), the user asked whether a git commit
had been made for a feature branch. The answer was in the agent's
persistent memory:

```
OB1 PR #337: [skills] Hermes Agent Onboarding — 10 skills + recipe.
Aguardando review.
```

This memory block was loaded in the volatile tier of the system prompt
— directly accessible. Instead of reading it, the agent made **three
tool calls**: session_search (FTS5 query), a second session_search
(different keywords), and a transcript scroll. Thousands of tokens
wasted for a fact already in the prompt.

The prompt contained the text "PR #337" and "git commit was done" —
but the executor never checked.

---

## Identity as Interface: Why Context Reliability Matters

This proposal is not merely about saving tokens. It is about what an
agent **is** from the user's perspective.

### The user does not see software

When a user talks to Hermes, they are not talking to `run_agent.py`,
a specific model checkpoint, or an API provider. They are talking to a
**recognizable interface** — something that has continuity, memory,
and reliable knowledge of what was built together. This is what we
call **agent identity as interface**: the user's experience of the
agent is defined by the agent's ability to *be in context* with them.

Every time the agent calls a tool to rediscover a fact it already has
in its prompt, the user experiences a **break in the interface**. The
agent seems absent-minded, unreliable — as if it does not remember
what it just read. This erodes the trust that makes the agent useful
as a persistent collaborator.

### Reliability comes from structure, not model intelligence

The model is not the problem. The model sees all the information — it
just has a structural bias toward acting rather than reading. The
solution is not to wait for smarter models. The solution is to
**build a structure that forces the model to read before it acts**.

This is the same principle as a pilot's preflight checklist: the
pilot is intelligent enough to fly without it, but the checklist
exists because *structure prevents predictable failure*. The agent
needs the same — a procedural barrier that turns "check context
before acting" from a suggestion into a required step.

### What we are building: a rudimentary shared context layer

The agent's memory (MEMORY.md, USER.md, session history) and the
user's ongoing work form a **shared context** — the space where user
and agent meet. Currently, the agent can access this context, but
only via explicit tool calls that it must remember to make. This is
like having a conversation partner who keeps asking "what were we
talking about?" even though the notes are in front of them.

The preflight + auto-injection structure proposed here is a
**rudimentary shared context layer**. It does not solve all problems.
It does not replace structured memory or relational databases. But it
ensures a baseline: before the agent acts, it reads the context it
already has. This is the foundation upon which more sophisticated
context management (vector stores, relational identity tables,
checkpoint systems) can be built.

### The identity-cost tradeoff

Context reliability is not free. The preflight adds ~400 tokens per
session. The auto-injection adds a SQLite query per turn. These costs
are negligible (fractions of a percent of a typical session), but
they exist. The tradeoff is:

- **Without preflight:** lower token cost, higher risk of context
  blindness — the agent acts without having read what it knows.
- **With preflight:** a small fixed token cost, guaranteed context
  awareness — the user experiences a reliable interface.

For a tool that is used as a daily collaborator (not a one-shot
query), the preflight pays for itself in the first few interactions
by preventing unnecessary tool calls and user corrections.

### Why this matters for the upstream

When Hermes is deployed in production — as a coding assistant, a CRM
agent, a home automation interface — the user's trust depends on the
agent **remembering what it knows**. A user who has to repeat
themselves or correct the agent's context blindness will eventually
stop relying on it. The preflight is a cheap, structural fix for a
failure mode that no amount of model improvement will fully solve.

---

## Root Cause

The agent loop (`agent/conversation_loop.py:run_conversation()`) has no
**preflight phase** between "receive user message" and "make API call".
The sequence is:

```
Receive user message ──→ Append to history ──→
Build system prompt (cached) ──→ Make API call ──→
Parse response ──→ if tool_calls: dispatch ──→ loop
```

Between "build system prompt" and "make API call", there is no step
that says: *"You already have the answer. Read your own prompt."*

The LLM *sees* memory and SOUL.md in its system prompt — but the
system prompt does not contain an explicit **protocol** that forces
the model to check it before reaching for tools. The model weighs
declarative text ("you should check memory") against vivid tool
descriptions ("call session_search to find past conversations"), and
the tool descriptions win because they describe concrete actions.

**This is a gradient problem, not a content problem.** Adding more
textual rules to SOUL.md makes it worse — more tokens, same gradient.

---

## Proposed Solution: Context Preflight Layer

A new **procedural preflight** injected into the system prompt between
the stable tier (identity) and the tools/skills index. Because the
system prompt is assembled left-to-right, the preflight tokens appear
*before* the tool descriptions — the model must process them before it
can reach the tool calls.

### System Prompt Tier Order

```
┌─────────────────────────────────────┐
│  Tier 1: IDENTITY (SOUL.md)         │  ← cached (stable)
├─────────────────────────────────────┤
│  Tier 2: PREFLIGHT (new)            │  ← NEW — procedural barrier
├─────────────────────────────────────┤
│  Tier 3: BEHAVIOR GUIDANCE          │  ← cached (stable)
│  (memory, session_search, skills)   │
├─────────────────────────────────────┤
│  Tier 4: SKILLS INDEX               │  ← cached (stable)
├─────────────────────────────────────┤
│  Tier 5: CONTEXT FILES              │  ← cached (context)
│  (AGENTS.md, .hermes.md, etc.)      │
├─────────────────────────────────────┤
│  Tier 6: VOLATILE                   │  ← per-session
│  (MEMORY.md, USER.md, timestamp)    │
└─────────────────────────────────────┘
```

Tier 2 is the preflight. It is procedural, stepped, and structured as
a **protocol to execute**, not a suggestion to consider.

### Preflight Text

```markdown
## ── CONTEXT PREFLIGHT ──

Before generating any tool call, execute this protocol:

### 1. Read what you already have

Your system prompt contains:
- **SOUL.md** (above) — your identity and standing instructions
- **Memory** (below) — durable facts stored across sessions
- **User profile** (below) — who the user is
- **Skills** (below) — procedural knowledge loaded for this session
- **Conversation history** — what was said earlier in this session

### 2. Answer from context if possible

If the user's question can be answered from ANY of the above, do so
now. Do not call a tool. The answer may already be here.

### 3. Only if the answer is not here, use tools

Call tools to get missing information. Tool descriptions are below.

### 4. Exceptions — fast path (bypass preflight)

The following requests skip the preflight and go directly to tools:
- **Direct tool commands**: "search for X", "run this command"
- **Time-sensitive**: "what time is it", realtime data queries
- **Mutations**: "save this", "write this file", "configure MCP"
- **User explicitly asks for tool output**: "check if X exists"
- **First-turn initialization**: supabase scan, code analysis

### 5. Violation detection

If you start calling tools without having verified whether the answer
is already in your context, you are violating the preflight protocol.
Stop. Re-read this section. Respond from context first.
```

### Why this works (and why previous attempts didn't)

| Approach | Why it failed | How preflight fixes it |
|----------|---------------|----------------------|
| Rules in SOUL.md | Declarative text — low gradient vs tool descriptions | Procedural, stepped — reads like code, not suggestion |
| Memory guidance ("use session_search first") | Says to use a *tool* to check memory | Says to read the *prompt itself* first |
| Tool-use enforcement ("MUST use tools") | Reinforces action bias — opposite of what we need | Creates a barrier *before* tools |
| Skills index (context-bridge skill) | Requires agent to load the skill — circular dependency | Injected automatically at framework level |
| Session_search tool | Tool call — same action gradient problem | Makes tool call the *last* resort, not first |

The key insight is **token ordering**: by placing the preflight between
the identity and the tool descriptions, the model processes the
preflight before it can "see" what tools are available. The model
generates left-to-right — it cannot skip the preflight because the
tool descriptions haven't been tokenized yet from its perspective.

---

## Local Context Store — Hermes-Native Approach

The preflight above solves "read what's already in your prompt". But
a deeper problem remains: what if the information exists in a **past
session** that is NOT in the current system prompt?

### Current solution: session_search (SQLite + FTS5)

Hermes already has `session_search` — an FTS5-backed SQLite tool that
queries past transcripts. It works, but it is a **tool** — the agent
must remember to call it, and the action bias works against it.

### Proposed: Preflight Context Injection

Instead of relying on the agent to *remember* to call session_search,
inject relevant past context **automatically** before each turn.

#### Design

```
┌──────────────────────┐    ┌────────────────────┐    ┌──────────────────┐
│  New user message    │───▶│  Preflight Context │───▶│  Injected into   │
│  (embed + search)    │    │  Engine            │    │  ephemeral prompt │
│                      │    │  (local SQLite +   │    │  overlay          │
│                      │    │   FTS5 + optional  │    │  (API-call-time   │
│                      │    │   vector)          │    │   only)           │
└──────────────────────┘    └────────────────────┘    └──────────────────┘
```

**Hermes already has all the pieces:**

| Component | Currently | Proposed use |
|-----------|-----------|-------------|
| **Session store** | `hermes_state.py` (SQLite, FTS5) | Primary context source |
| **Checkpoints** | `session_checkpoints` (optional) | Source of condensed context |
| **Skill memory** | `skill-memory` accumulation | Per-skill context fragments |
| **MEMORY.md** | ~/.hermes/MEMORY.md | Always in prompt — no change needed |

#### Implementation

In `agent/conversation_loop.py`, inside `run_conversation()`, after
the system prompt is built (around line 550):

```python
# ── Preflight Context Injection ──
if getattr(agent, "_context_preflight", True):
    preflight_context = _get_preflight_context(
        user_message=user_message,
        conversation_history=messages,
    )
    if preflight_context:
        # This line is critical: it stores the context
        # as an ephemeral overlay, NOT in the cached system
        # prompt. It gets injected at API-call time only.
        agent._ephemeral_context_overlay = preflight_context
```

And `_get_preflight_context` uses existing Hermes infrastructure:

```python
def _get_preflight_context(user_message, conversation_history):
    """Query local session DB for relevant past context."""
    
    # 1. Check for key terms in the user message that match
    #    recent memory or checkpoint content
    #    (keyword overlap is cheaper than embedding)
    key_terms = _extract_key_terms(user_message)
    
    # 2. Query session_search's FTS5 engine directly
    #    (no LLM — just sqlite-fts5 via hermes_state)
    matches = _query_session_search(
        terms=key_terms,
        limit=3,
        sort="newest",
    )
    
    if not matches:
        return None
    
    return _format_preflight_context(matches)
```

This is a **framework-level hook** — the agent never calls a tool. The
context arrives automatically, the same way MEMORY.md arrives in the
volatile tier.

### Implementation paths (choice of backend)

| Path | What it uses | When to choose |
|------|-------------|----------------|
| **A: Hermes-native (SQLite + FTS5)** | Existing `hermes_state.py` session DB, no new dependencies | Default. Zero setup. Already works — just needs the framework hook. |
| **B: SQLite + sqlite-vec** | `sqlite-vec` extension for vector similarity on top of existing SQLite | Moderate setup. Adds semantic search to existing session store. |
| **C: PostgreSQL + pgvector** | Local or containerized PG with pgvector extension | Advanced. For users who want a full vector store and already run PG. |

**Path A is the recommended first implementation** because:
- Hermes already stores every session in SQLite (via `hermes_state.py`)
- FTS5 is already enabled — no new dependencies
- The only change is the injection hook, not the storage layer
- Path B and C are incremental upgrades that swap the query engine

---

## Implementation Plan

### Phase 1 — Preflight System Prompt (no storage changes)

**What:** Add `CONTEXT_PREFLIGHT_GUIDANCE` to the system prompt.

**Files:**
- `agent/prompt_builder.py` — add `CONTEXT_PREFLIGHT_GUIDANCE`
  constant (~80 lines of prompt text)
- `agent/system_prompt.py` — insert preflight block in the stable
  tier, between identity and tool guidance (~5 lines of Python)

**Config:** `agent.context_preflight: true` (default: true) — in
config.yaml under the `agent` section.

**Token cost:** ~400 tokens per session (one-time, cached — same as
adding a skills entry). This is ~0.2% of a 200K-token session.

**Verification:**
1. Start a new session — the preflight should appear in the system
   prompt dump (`/dump`)
2. Ask a question whose answer is in memory — the agent should answer
   without any tool call
3. Ask a question that requires a tool — the agent should still call
   tools normally

### Phase 2 — Automatic Context Injection from Existing Session DB

**What:** Inject relevant past context into the ephemeral prompt
overlay before each turn. Uses Hermes' existing SQLite session store.

**New files:**
- `agent/preflight_context.py` — the `_get_preflight_context()` and
  `_query_session_search()` functions (~150 lines)

**Modified files:**
- `agent/conversation_loop.py` — add the injection hook in
  `run_conversation()` (~10 lines)

This phase needs NO new storage. It uses the same FTS5 SQLite that
`session_search` already uses — but at the framework level, not via
a tool call.

**Config:** `context_preflight.auto_inject: true` (default: false for
Phase 2, pending production testing)

### Phase 3 — Vector Store (optional upgrade)

**What:** Add embedding + vector similarity on top of the session DB.
Can use either `sqlite-vec` (Path B) or `pgvector` (Path C).

**New files:**
- `agent/preflight_embedder.py` — embedding service (~100 lines)
- `docker/postgres-pgvector/` — optional, for Path C users

**Design principle:** the vector store should be a **plug-in** to the
same `_get_preflight_context()` interface. Phase 2's FTS5-based
approach remains the default. If a vector extension is available, it
augments the results — it does not replace them.

---

## Supporting Research: Self-Anchored Drift

A contemporaneous paper provides direct empirical evidence for the
problem this proposal addresses — and validates the direction.

**Lin et al. (2026), "Same Evidence, Different Answers: Canonical-Context
On-Policy Distillation for Multi-Turn Language Models."**
arXiv:2605.30251v1.

### Key finding

> "When a clean FULL prompt and a RAW-SHARDED conversation contain the
> same complete user evidence, the model should still arrive at the same
> answer. [...] A key reason for this gap is **self-anchored drift**:
> responses produced under partial information introduce unsupported
> assumptions, and those assumptions later distort the final answer."

This is exactly what we observed: the agent produced tool calls
(session_search, etc.) under partial context (it hadn't read its own
prompt yet), and those actions became "self-anchored" — the model then
continued down the tool path instead of reconsidering whether the
answer was already available.

### How their approach differs from ours

Lin et al. solve this at **training time**: they use on-policy
distillation to align the model's behavior under sharded context with
its behavior under full context. Their CCOPD method achieves a 32%
average relative improvement on raw-sharded performance across six
task families.

We are solving this at **inference time**: our preflight phase and
auto-context injection operate at the system prompt and agent loop
level, not at the model weights level. The approaches are
**complementary**:

| Layer | Problem | Solution |
|-------|---------|----------|
| **Training** (Lin et al.) | Model learns to drift under sharded context | Distillation aligns sharded→full behavior |
| **Inference** (this RFC) | Agent acts before reading full context | Preflight barrier + auto-injection |

A model trained with CCOPD would still benefit from the preflight —
and a model with preflight would show even better raw-sharded
performance after CCOPD training.

### What this paper confirms

1. **The problem is structural, not a prompt gap.** Lin et al. show
   that even state-of-the-art models (Qwen3-8B, Llama3.1-8B) fail at
   canonical-context consistency. This is not a matter of "add a better
   instruction" — the drift is built into the autoregressive generation
   process.

2. **Self-anchored drift is measurable.** They introduce SAAR
   (Self-Anchor Attention Ratio) to quantify how much the model attends
   to its own prior outputs versus user evidence. This metric could be
   used to evaluate the preflight's effectiveness.

3. **The training and inference approaches are compatible.** Their
   pollution stress tests (inserting wrong numeric anchors into the
   assistant history) show that CCOPD-trained models resist
   self-anchored drift. Adding the preflight on top should further
   reduce unnecessary tool calls triggered by the same mechanism.

### Key quote

> "The model should still arrive at the same answer. We argue that a key
> reason for this gap is **self-anchored drift**: responses produced
> under partial information introduce unsupported assumptions, and those
> assumptions later distort the final answer."

Replace "assistant replies under partial information" with "tool calls
initiated before reading the full system prompt" and you have a precise
description of the Hermes failure mode.

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Preflight adds tokens to every session | Certain | Low (~400 tokens, one-time) | Config flag to disable |
| Preflight text is ignored by some models | Medium | Low | Token ordering forces processing — models cannot skip tokens |
| Phase 2 auto-injection returns irrelevant context | Medium | Low | Similarity threshold; context is injected as suggestion, not command |
| False negatives (context exists but not found) | Low | Low | Fallback: agent still has session_search tool for explicit use |
| Breaking existing behavior | Low | Medium | Phase 1 default=true, Phase 2 default=false; gradual rollout |
| SQLite FTS5 is less accurate than vector search | Certain | Low | FTS5 is already the production search for session_search. Phase 3 adds vector as upgrade path. |

---

## Alternatives Considered

### 1. Tool-level preflight hook (in tool_executor.py)
Check context before every tool dispatch.  
**Rejected:** 90% of unnecessary tool calls happen on the first turn.
Post-hoc prevention is wasteful and adds latency to every tool call.

### 2. Remove session_search, replace with auto-injection
Eliminate the tool, make context retrieval fully automatic.  
**Rejected:** session_search has legitimate use for explicit queries
("find the session where we configured X"). Keep the tool.

### 3. Model-level fine-tuning
Fine-tune to prefer reading context over calling tools.  
**Rejected:** breaks on third-party model providers (OpenRouter,
Anthropic) and adds maintenance burden for every model update.

### 4. Declarative rules in SOUL.md
"Always check your memory before calling tools."  
**Already tried. Does not work.** Declarative rules have lower
gradient than tool descriptions. See the concrete failure above.

### 5. Wait for models to get better at this
Assume future LLMs will naturally check context before acting.  
**Rejected:** The bias is structural in the agent loop, not a model
limitation. Models that process the same prompt will make the same
trade-off regardless of intelligence.

---

## Integration with Existing Hermes Architecture

| Existing component | How preflight interacts |
|-------------------|------------------------|
| **`run_agent.py` (AIAgent)** | No changes to the class. Preflight is injected via `system_prompt.py` (Phase 1) and `conversation_loop.py` (Phase 2). |
| **`agent/system_prompt.py`** | Adds preflight block to `build_system_prompt_parts()`. The stable tier grows by ~400 tokens. |
| **`agent/conversation_loop.py`** | Adds `_get_preflight_context()` call after system prompt build. The context lands in `ephemeral_system_prompt`, which is already an API-call-time-only injection path. |
| **`hermes_state.py`** | Phase 2 queries the same SQLite DB. No changes needed. |
| **`tools/session_search_tool.py`** | **Not removed.** The tool stays for explicit user queries ("find the session where..."). The preflight covers the *automatic* case. |
| **`~/.hermes/MEMORY.md`** | Still the primary memory store. The preflight is additive — it finds context NOT in current memory. |
| **Skills system** | Skills that already load context (context-bridge) are complementary. The preflight runs before any skill is loaded. |
| **Prompt caching** | The preflight block is in the **cached stable tier** (Phase 1), so it does not invalidate prefix caches. Phase 2's context injection uses the already-existing `ephemeral_system_prompt` path — never cached. |

---

## Measuring Success

| Metric | How to measure | Target |
|--------|---------------|--------|
| Tool calls per turn | Compare runs with/without preflight | 20% fewer on questions answerable from context |
| Token waste | Tokens spent on session_search for answers already in memory | 0 for preflight-active sessions |
| User corrections | User saying "it was in memory" after an unnecessary tool call | Near zero |
| First-turn latency | Time from message to first response | No regression (preflight is synchronous, SQLite query < 5ms) |

---

## Appendix: Key Source Files

| File | Lines | Role |
|------|-------|------|
| `run_agent.py` | ~4400 | AIAgent class — entry point |
| `agent/conversation_loop.py` | ~3900 | `run_conversation()` — the agent loop |
| `agent/system_prompt.py` | ~400 | `build_system_prompt_parts()` — tier assembly |
| `agent/prompt_builder.py` | ~500 | Prompt constants and helpers |
| `hermes_state.py` | ~800 | SQLite session store (FTS5 enabled) |
| `tools/session_search_tool.py` | ~300 | Current session_search tool implementation |

---

## Upstream Contribution Path

This proposal is structured for submission to Nous Research as an
RFC. The intended contribution is:

1. **Phase 1** — System prompt preflight. Minimal, non-breaking, clear
   behavioral improvement. Can be submitted as a single PR.
2. **Phase 2** — Auto-context injection. Requires more discussion
   about the ephemeral injection path and config defaults. Should
   follow Phase 1 after production validation.
3. **Phase 3** — Vector store. Optional, community-driven. Not
   intended for core Hermes unless the upstream team adopts it.

---

## Change Summary

| Phase | Change | Files | Deploy |
|-------|--------|-------|--------|
| 1 | Preflight system prompt block | 2 modified, ~130 lines | config flag, default on |
| 2 | Auto-context injection from SQLite | 2 modified + 1 new, ~160 lines | config flag, default off |
| 3 | Vector store (sqlite-vec / pgvector) | 2-4 new files, ~250 lines | optional, community |
