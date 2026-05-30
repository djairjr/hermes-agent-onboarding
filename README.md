# Hermes Agent Onboarding

A generative 6-stage meta-skill that transforms a blank Hermes Agent into a customized ecosystem — not for "a firmware engineer," but for **your** work.

All of this was made possible by **NateBJones** and his [OB1](https://github.com/NateBJones-Projects/OB1) project — the Edge Function + MCP pattern that opened the door to building agentic ecosystems on Supabase. Go read his work first. I wouldn't be here without it.

Also inspired by [CLI-KIT-NOVA](https://github.com/MathGALIN/CLI-KIT-NOVA) (MathGALIN) and [MBTI Guru](https://clawhub.ai/effeceee/mbti-guru) (effeceee).

## Why Agent Onboarding Exists

AI agents like Hermes, OpenClaw, and Claude Code are still niche tools — used mostly by AI engineers who already know how to prompt, configure providers, and debug MCP servers. But the underlying capability is universal.

**The agent speaks your language, not code.** You describe what you need in plain words. The agent translates that into file system operations, API calls, database queries — it programs the machine on your behalf. The user interface is conversation, but the engine is automation.

This meta-skill bridges that gap: it makes the agent understand **who you are** before it tries to help you. A writer, a teacher, a chef, and a firmware engineer all need different tools, different data structures, and different communication styles. The onboarding process discovers yours.

## Why an Agent Identity Layer

One of the core problems this project addresses is **agent identity persistence**. LLMs have no inherent memory of who they are between sessions. Every conversation is a fresh start — the model doesn't know what it learned about you last time, what mistakes it made, or how it should behave.

The identity layer (stages 0-1 of this meta-skill) solves this by creating a **persistent record** in Supabase that the agent reads at every session start:

- **identity_faults** — logs every mistake the agent makes in its relationship with the user (premature closure, false agreement, role confusion). Each fault has a countermeasure that becomes a behavior rule.
- **agent_capabilities** — what the agent has learned to do, what skills it has acquired, what patterns it recognizes.
- **identity_milestones** — breakthroughs, protocol establishments, and capacity acquisitions in the agent's own development.

Without this layer, the agent is a blank slate every time. With it, the agent builds a **relational identity** — not a persona, but a documented history of interactions, mistakes, and growth that persists across model swaps, provider changes, and software updates.

**This is not about making the agent seem human.** It is about making the agent **reliably itself** — consistent, self-aware of its limitations, and improving over time. The identity is a framework the user builds with the agent, not a mask the agent wears.

## The 6 Stages

```
STAGE 0 — SETUP VERIFICATION       ← Hermes, provider, Supabase, tables, wrapper
STAGE 1 — USER PROFILE             ← biography = career-tracker + MBTI
STAGE 2 — WORK OPERATING MODEL     ← rhythms, decisions, friction
STAGE 3 — FINANCIAL                ← CSV import, goals × MBTI profile
STAGE 4 — DOMAIN ONTOLOGY          ← discover entities → generate tables + MCPs
STAGE 5 — AGENT CALIBRATION        ← SOUL.md, wrapper, verification
```

## Quick Start

```bash
# 1. Install Hermes (see official docs below)
pip install hermes-agent

# 2. Clone this repo
git clone https://github.com/djairjr/hermes-agent-onboarding
cd hermes-agent-onboarding

# 3. Apply database migrations
supabase db push --linked

# 4. Run the onboarding
hermes --skills agent-onboarding
```

Follow the interview. The agent discovers who you are, how you work, and what you build.

## Prerequisites

- [Hermes Agent](https://hermes-agent.nousresearch.com/docs) installed
- An [Ollama](https://ollama.ai/) or OpenAI-compatible provider configured
- A [Supabase](https://supabase.com/) project (free tier works)
- [Supabase CLI](https://supabase.com/docs/guides/cli) linked to your project

## Identity Tables

6 base tables in `public` schema, RLS-protected (service_role only):

| Table | Purpose |
|-------|---------|
| user_profiles | Identity, family, routines |
| user_preferences | Communication, autonomy, schedule |
| user_mbti | 4 dimensions, type, observed traits |
| user_style | Vocabulary, tone, sentence structure |
| user_relations | Key people: partners, family, clients |
| user_beliefs | Values, principles, non-negotiables |

Plus `identity_faults`, `agent_capabilities`, `identity_milestones` (the agent's own identity record) and `career_tracker.*` (capabilities, solved_problems, milestones — the user's biography layer).

## Architecture

```
user request (natural language)
    ↓
agent-onboarding (orchestrator skill, 6 stages)
    ↓
Supabase (user_profiles, identity_faults, career_tracker, + domain tables)
    ↓
MCP servers (supabase-finance, work-operating-model, + generated CRUD)
    ↓
calibrated Hermes Agent → YOUR domain
           ↓
    The agent speaks your language.
    It programs the machine on your behalf.
```

## My Setup (Reference)

This was built and tested on:

- **Hermes Agent** via WSL2 (Windows Subsystem for Linux)
- **Provider:** Ollama Cloud with `deepseek-v4-flash:cloud`
- **Supabase:** Cloud project, 6 base tables + career-tracker + identity tables
- **Local Backup Server:** Radxa E24C with 250GB NVMe — permanent Supabase
  replica for resilience and offline access
- **21 MCP servers** (13 HTTP Edge Functions + 8 stdio tools), all backed by
  Supabase Edge Functions on the cloud project, with the local Radxa as a
  secondary sync target
- **Ollama launch** wrapper for environment management

## Official Tutorials

| Resource | What it covers |
|----------|---------------|
| [NateBJones/OB1](https://github.com/NateBJones-Projects/OB1) | **Start here.** The Edge Function + MCP pattern this builds on |
| [Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs) | Installation, configuration, providers, skills |
| [Ollama Setup](https://ollama.ai/download) | Local LLM provider on any OS |
| [Supabase CLI Guide](https://supabase.com/docs/guides/cli) | Database migrations, project management |

## Documentation

| File | What it covers |
|------|---------------|
| [docs/02-SUPABASE.md](docs/02-SUPABASE.md) | Creating project, applying migrations, security model |
| [docs/03-RUNNING.md](docs/03-RUNNING.md) | Executing all 6 stages, expected duration, troubleshooting |
| [docs/04-CUSTOMIZING.md](docs/04-CUSTOMIZING.md) | Adding domain-specific tables, multi-user setup |
| [migrations/](migrations/) | SQL schemas for all base tables |

## Security

All GPG-signed commits (key `6B67B080006EFB7F`). Full security protocol in [docs/SECURITY.md](docs/SECURITY.md).

## License

MIT — free to use, adapt, distribute.

Built by **Djair Guilherme** ([github.com/djairjr](https://github.com/djairjr)) with [Hermes Agent](https://hermes-agent.nousresearch.com).  
Thanks to **NateBJones** ([OB1](https://github.com/NateBJones-Projects/OB1)) for the foundation that made this possible.
