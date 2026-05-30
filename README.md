# Hermes Agent Onboarding

A generative 6-stage meta-skill that transforms a blank Hermes Agent into a customized ecosystem — not for "a firmware engineer," but for **your** work.

All of this was made possible by **NateBJones** and his [OB1](https://github.com/NateBJones-Projects/OB1) project — the Edge Function + MCP pattern that opened the door to building agentic ecosystems on Supabase. Go read his work first. I wouldn't be here without it.

Also inspired by [CLI-KIT-NOVA](https://github.com/MathGALIN/CLI-KIT-NOVA) (MathGALIN) and [MBTI Guru](https://clawhub.ai/effeceee/mbti-guru) (effeceee).

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

## My Setup (Reference)

This was built and tested on:

- **Hermes Agent** via WSL2 (Windows Subsystem for Linux)
- **Provider:** Ollama Cloud with `deepseek-v4-flash:cloud`
- **Supabase:** Cloud project, 6 base tables + career-tracker schema
- **21 MCP servers** (13 HTTP Edge Functions + 8 stdio tools)
- **Ollama launch** wrapper for environment management

Your setup will differ — the meta-skill adapts accordingly.

## Official Tutorials (more current than anything in this repo)

| Resource | What it covers |
|----------|---------------|
| [NateBJones/OB1](https://github.com/NateBJones-Projects/OB1) | **Start here.** The Edge Function + MCP pattern this all builds on |
| [Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs) | Installation, configuration, providers, skills |
| [Ollama Setup](https://ollama.ai/download) | Local LLM provider on any OS |
| [Supabase CLI Guide](https://supabase.com/docs/guides/cli) | Database migrations, project management |

## Data Layer

6 base tables in `public` schema, RLS-protected (service_role only):

| Table | Purpose |
|-------|---------|
| user_profiles | Identity, family, routines |
| user_preferences | Communication, autonomy, schedule |
| user_mbti | 4 dimensions, type, observed traits |
| user_style | Vocabulary, tone, sentence structure |
| user_relations | Key people: partners, family, clients |
| user_beliefs | Values, principles, non-negotiables |

Plus `career_tracker.*` (capabilities, solved_problems, milestones) — the biography layer.

## Documentation

| File | What it covers |
|------|---------------|
| [docs/02-SUPABASE.md](docs/02-SUPABASE.md) | Creating project, applying migrations, security model |
| [docs/03-RUNNING.md](docs/03-RUNNING.md) | Executing all 6 stages, expected duration, troubleshooting |
| [docs/04-CUSTOMIZING.md](docs/04-CUSTOMIZING.md) | Adding domain-specific tables, multi-user setup |
| [migrations/](migrations/) | SQL schemas for all base tables |

## Architecture

```
user request
    ↓
agent-onboarding (orchestrator skill, 6 stages)
    ↓
Supabase (user_profiles, career_tracker, + domain tables)
    ↓
MCP servers (supabase-finance, work-operating-model, + generated CRUD)
    ↓
calibrated Hermes Agent → YOUR domain
```

## License

MIT — free to use, adapt, distribute.

Built by **Djair Guilherme** ([github.com/djairjr](https://github.com/djairjr)) with [Hermes Agent](https://hermes-agent.nousresearch.com).  
Thanks to **NateBJones** ([OB1](https://github.com/NateBJones-Projects/OB1)) for the foundation that made this possible.
