# Thank You Letter to NateBJones

Dear Nate,

I've been meaning to write this for a while. I found OB1 about a month ago, and it completely changed how I think about building with AI agents.

Before OB1, I was struggling with a fundamental problem: every session with an AI agent starts from zero. The model doesn't remember what it learned about me, what tools it built, or what mistakes it made. I had skills and prompts, but no real infrastructure — nothing that persisted meaningfully between conversations.

Your Edge Function + MCP pattern was the missing piece. The idea of exposing database operations through MCP tools, backed by Supabase Edge Functions, is deceptively simple — but it unlocks something huge. Once I understood it, I spent the next month adapting it to my own needs, creating 13 HTTP MCP servers, 283 code analysis snapshots, a full product catalog, a CRM, an escape room database, financial tools — basically my entire workflow running through the agent.

More importantly, it motivated me to build something I hadn't seen anyone do yet: a meta-skill that makes the agent develop its own identity. The idea is simple — the agent logs every mistake it makes with a countermeasure, reads them back at the start of each session, and adjusts its behavior. It's a persistent identity layer that works across model swaps and provider changes.

I turned this into an open-source project called **Hermes Agent Onboarding** (github.com/djairjr/hermes-agent-onboarding). It's a 6-stage meta-skill that takes a brand-new Hermes Agent installation and walks it through discovering who the user is — their personality (MBTI), their work operating model, their finances, their domain ontology — and then calibrates the agent's behavior to match. The whole thing is built on OB1's foundation: Edge Functions, MCP tools, Supabase as the single source of truth.

The most surprising part is that I designed this to help others, not just myself. My wife is a writer, and watching her struggle with the same context-loss problem with her own tools made me realize this isn't a niche issue — it affects anyone who works with an AI agent, regardless of their field. A writer needs different tools, different data structures, and a different agent tone than a firmware engineer does. The onboarding process should discover those differences, not assume them.

I wouldn't have gotten here without OB1. Your YouTube videos were incredibly helpful too — watching someone actually build with this stuff made the concepts click faster than any documentation could.

Thank you for sharing your work so openly. It's rare to find a project that's both practically useful and philosophically inspiring. OB1 was both for me.

Best,

Djair Guilherme
github.com/djairjr
