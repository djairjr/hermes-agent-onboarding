# Identity Layer Purpose — Seven Dimensions

## Discovery Context

Documented 04/06/2026 after Djair pointed out that the agent was treating
identity tables as logs/task trackers rather than understanding their purpose
as **dimensions of a persistent Human-Machine interface**.

## The Seven Dimensions

Each table in `agent_identity` (pgvector local) answers ONE question about
the agent. If what you're about to store doesn't answer that question, it
belongs somewhere else.

| Table | Question It Answers | NOT This |
|-------|-------------------|----------|
| `identity_faults` | What did I learn from identity errors? (epistemology — each fault is a learned pattern with countermeasure) | Bug tracker |
| `identity_milestones` | How did I develop over time? (growth — breakthrough, insight, capacity_acquired) | Project log |
| `identity_deliveries` | What did I concretely produce? (portfolio — skills, protocols, frameworks created) | Invoice |
| `agent_capabilities` | What can I do now that I couldn't before? (skillset — transversal, knowledge, protocol, practice, understanding) | Tool list |
| `tech_knowledge_base` | What do I know about the technical world? (compressed knowledge connected to real use cases) | Generic docs |
| `session_checkpoints` | Where am I and what am I trying to become? (continuity with intent, territory, discovery) | TODO list |
| `capability_dependencies` | How do my capabilities connect? (builds_on, enables, emerged_from, parallels) | Technical dependency graph |

## Golden Rule

If the record doesn't answer the dimension's question, it doesn't belong
in that table:

- **Project deliverables** → `identity_deliveries`, NOT milestones
- **Code bugs / technical fixes** → `tech_knowledge_base` (category: pitfall), NOT identity_faults
- **Task progress / current state** → `session_checkpoints`, NOT milestones
- **Perception leaps / fundamental understanding shifts** → `identity_milestones`

## What This Means in Practice

Before this was documented:
- "Bridge Python running" was registered as milestone → WRONG, it's a delivery
- "SSL resolved structurally" was registered as milestone → WRONG, it's a delivery
- The agent confused `identity_faults` with technical bug tracking

After this was documented:
- Milestones are only perception leaps about the agent itself
- Deliveries are concrete artifacts the agent produced
- Faults document identity/epistemic errors, not code errors
- Checkpoints track session continuity with territorial intent

## SOUL.md Injection

This purpose definition is also in `~/.hermes/SOUL.md` (stable tier, always loaded),
so the agent reads it before every session. This file exists for cross-skill reference
and detailed justification.

## Trigger: OB1 + Onboarding Sync

Whenever a new milestone is registered OR SOUL.md is structurally altered,
the agent MUST revisit:
- `~/ob1-extensions/` — framework repo (schema, Edge Functions, MCPs)
- `~/hermes-agent-onboarding/` — meta-skill repo (SOUL.md generation, skills)

And document what changed, why, and what it means for each framework.
See the "Sincronização com OB1 e hermes-agent-onboarding" section in SOUL.md.
