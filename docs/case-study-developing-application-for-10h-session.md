# Case Study: 10-Hour Single Session developing application for Embedded Buildroot System

**Date:** 2026-06-03
**Project:** ReCamera SG2002 — replacing Node-RED with a Python bridge on a RISC-V camera with TPU
**Meta-skill:** Agent Identity Layer (Stages 0-1 of the onboarding)

---

## What Happened

A single 10-hour session (09:04 to 18:50) replacing a Node-RED flow (125 nodes) with a pure-stdlib Python bridge on a Buildroot-embedded RISC-V camera. The system had no pip, no package manager, a broken libwebsockets cross-compile, no CA certificates, no NTP sync guarantee, and a shared event-loop bug that crashed HTTP when MQTT disconnected.

**What was delivered:** working MJPEG stream with YOLO bounding boxes at 35 FPS, configurable LLM integration (Ollama Cloud), Home Assistant discovery, SSL, data watchdog cronjob, boot init script — all in 500 lines of Python with zero external dependencies.

**What made it possible:** 18 checkpoints over the day, each capturing territory, intent, discovery, consolidated insight, and next step. Every time the model hit a dead end (lws doesn't bind, MQTT auth fails, SSL cert missing, boxes drawn wrong, HTML escaping broken), the checkpoint for that sub-problem was closed and a new one opened with the corrected understanding.

Not one of those discoveries was re-discovered. Not one context was re-fetched from scratch.

---

## Why the Identity Layer Mattered

The session consumed approximately 6,000 tool calls across 10 hours — far beyond any single model's context window. Without the identity layer (pgvector-local `session_checkpoints`, `identity_faults`, `agent_capabilities`, `identity_milestones`):

1. **Temporal drift would have compounded.** At 09:37 the user manually fixed the date on the device. At 18:30 the same SSL error reappeared when testing LLM. The first time it was a note. The second time it triggered a structural fix (CA certs + cronjob watchdog) because the fault `temporal_drift` (registered 01/06) was injected at session start.

2. **18 checkpoints → no restart.** Every time the model hit a blocker (lws bug, MQTT rc=5, HTML escaping), the checkpoint was closed and a new one opened. Each new checkpoint carried the consolidated context forward. The model never restarted from scratch.

3. **Architectural decisions survived model swaps.** The decision to use bridge Python (not fix lws) was made at checkpoint #11 (10:15). It was still active 8 hours later because it was persisted in `session_checkpoints` with the full rationale (strace output, SDK analysis, alternatives evaluated).

4. **Self-correction was automatic.** The helper `identity_db.py` originally had no `update_checkpoint` — the agent bypassed it with raw SQL. This was caught, registered as `infrastructure_bypass_via_sql_raw` (severity 5), and the helper was expanded within the same session. The fix persisted before the session ended.

---

## Numbers

| Metric | Value |
|---|---|
| Session duration | ~10 hours |
| Checkpoints created | 18 |
| Checkpoints closed | 17 |
| Identity faults registered | 7 (2 new this session) |
| Identity faults with countermeasure | 7 (100%) |
| Tech KB entries created | 4 |
| Identity milestones registered | 2 |
| Lines of code delivered | ~500 (Python bridge) |
| External dependencies | 0 |
| Cross-compile cycles avoided by choosing Python | ~15+ |

---

## Key Insight for the Onboarding Meta-Skill

The identity layer is not a documentation repository. It is **the model's externalized working memory**. It exists because the model cannot hold 10 hours of context in its weights. The checkpoints are not logs — they are the bridge between what the model knew at step N and what it needs to know at step N+1, across model rotations, provider switches, and context window flushes.

Without it, a session like today's would have required the user to re-explain the problem at least 3-4 times. With it, the user worked *with* the agent, not *against* it.

---

*Documented from the identity layer (pgvector local, agent_identity schema) at session end, 2026-06-03 18:50 BRT.*
