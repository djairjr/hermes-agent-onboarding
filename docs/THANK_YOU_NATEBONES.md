# Thank You Letter to NateBJones (AI Tipline Format)

**What does it do?**

A 6-stage generative meta-skill that makes any AI agent (Hermes, Claude, Codex) develop a persistent identity layer — learning who the user is, how they work, their personality (MBTI), their finances, and their domain ontology — and calibrating agent behavior to match. Instead of starting from zero every session, the agent remembers mistakes, applies countermeasures, and uses tools built specifically for that user's work.

**What does it need?**

Hermes Agent (or any skill-capable agent), a Supabase project, and one LLM provider. All 6 stages run through conversation — no CLI, no custom code for the user. The agent itself writes the migrations, creates the MCP tools, and configures the wrapper.

**Estimated difficulty:** Medium. The meta-skill is ready to use, but the user needs a working Hermes Agent + Supabase setup first (~30 min). After that, the agent handles everything.

**Do you have this working already?**

Yes. Running on my WSL2 Hermes instance since late April 2026. The agent built 13 HTTP MCP servers, 283 code analysis snapshots, a full product catalog, CRM, escape room database, and financial tools during the onboarding process. All on top of OB1's Edge Function + MCP foundation.

**The backstory:**

I found OB1 about a month ago, and it completely changed how I think about building with AI agents. The Edge Function + MCP pattern was the missing piece I had been searching for — the idea of exposing database operations through MCP tools, backed by Supabase Edge Functions, unlocks something huge. Once I understood it, I spent the next month adapting it to my own needs, creating the entire ecosystem mentioned above.

More importantly, OB1 motivated me to build something I hadn't seen anyone do yet: a meta-skill that makes the agent develop its own identity. The core insight is simple — the agent logs every mistake it makes with a countermeasure, reads them back at the start of each session, and adjusts its behavior. It's a persistent identity layer that works across model swaps and provider changes. My wife is a writer, and watching her struggle with the same context-loss problem with her own tools made me realize this isn't a niche issue — it affects anyone who works with an AI agent, regardless of their field.

The breakthrough came when I discovered that countermeasures in a database don't automatically become behavior rules. The missing piece was **SOUL.md** — a physical file that the Hermes Agent framework loads automatically as the first element of the system prompt (system_prompt.py), before any user message or skill. By placing active countermeasures (severity >= 4) there, behavior correction happens at generation time without requiring the agent to "decide" to follow rules. This completed the identity cycle: REGISTER (faults in Supabase) → INJECT (SOUL.md in stable tier) → BEHAVE (automatic correction). I've been calling this the **identity layer** — it's now fully documented in the meta-skill's Stage 5.

The whole thing is built on OB1's foundation: Edge Functions, MCP tools, Supabase as the single source of truth.

Repo: [github.com/djairjr/hermes-agent-onboarding](https://github.com/djairjr/hermes-agent-onboarding)

---

Best,

Djair Guilherme
github.com/djairjr
