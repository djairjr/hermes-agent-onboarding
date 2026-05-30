# Running the Onboarding

This guide explains how to execute the 6-stage onboarding process once Hermes and Supabase are configured.

## Quick Start

```bash
# Ensure your secrets are loaded
source ~/.hermes/secrets.env

# Start Hermes with the onboarding skill loaded
hermes --skills agent-onboarding
```

On first run, the orchestrator skill will:
1. Run the startup scan (verify Supabase connection, check tables)
2. Detect that no user profile exists yet
3. Begin Stage 0 (Setup Verification)

## The 6 Stages

### Stage 0 — Setup Verification

The agent checks:
- Is Hermes Agent properly installed? (version check)
- Is an LLM provider configured? (responds to prompt?)
- Is Supabase connected? (API responds?)
- Are the 6 base tables created? (RLS active?)
- Are the wrapper skills loaded? (startup-protocol, identity-audit, etc.)

If anything is missing, the agent guides you through fixing it.
Once verified: "Setup complete. Ready for onboarding."

### Stage 1 — User Profile (biography = career-tracker + MBTI)

**Sub-stages (in conversation, one question at a time):**

1. **Context** — Name, work domain, family, daily routine → `user_profiles`
2. **Preferences** — Communication style, autonomy level, schedule → `user_preferences`
3. **MBTI** — "Do you know MBTI?" → Explain → Quick test (10/20/40 Qs) → `user_mbti`
4. **Career-tracker** — Capabilities, solved problems, milestones, crises → `career_tracker.*`
5. **MindMaze** — "Want me to analyze patterns from your MBTI + career?"

**Expected duration:** 30-60 minutes depending on career depth.

### Stage 2 — Work Operating Model

5-layer interview about your professional workflow:
1. Rhythms — Typical day, deep work windows
2. Decisions — Recurring judgments, thresholds
3. Dependencies — What you need from others
4. Knowledge — What you know that no one else knows
5. Friction — What blocks you, workarounds

Powered by the `work-operating-model` skill (MCP tools).

**Expected duration:** 20-30 minutes.

### Stage 3 — Financial Profile

Not a subjective interview — data-driven analysis:

1. **CSV Import** — "Want me to analyze your bank statements? If yes, share CSV files."
2. **MBTI-based Profile** — Your personality type reveals your relationship with money
   (e.g., INTJ plans strategically, ENFP spends impulsively, ISTJ saves systematically)
3. **Goals** — Short (6mo), medium (2yr), long (5yr+) term objectives
4. **Strategies** — Budgeting, saving, investing — adapted to your MBTI

Powered by the `supabase-finance` MCP extension (17 tools).

**Expected duration:** 15-30 minutes (longer if importing CSVs).

### Stage 4 — Domain Ontology (Generative)

The agent discovers what "things" populate your work:

1. "What things do you create, manage, or transform in your work?"
   - Writer: characters, works, chapters, submissions, publishers
   - Teacher: classes, students, lessons, assessments
   - Engineer: projects, components, versions, clients
2. "How does one thing become another? Lifecycle?"
3. "What do you need to know about each thing?"
4. "How do you measure progress?"

For each entity, the agent proposes a table structure → you validate → it creates tables + optional MCP CRUD tools + optional weekly check-in cron job.

**Expected duration:** 20-40 minutes.

### Stage 5 — Agent Calibration

Everything from stages 1-4 is compiled into the agent's behavior:

1. **Generate SOUL.md** — Personalized identity profile (tone, autonomy, principles)
2. **Configure wrapper** — Add domain-specific skills to the Hermes launcher
3. **Verification** — Does the agent know you? Can it use the tools it built?

**Final checkpoint:** `onboarding_completed = true`

---

## What Happens After Onboarding

Once all 6 stages are complete, your Hermes Agent knows:

- **Who you are** (user_profiles + career-tracker + MBTI)
- **How you work** (work-operating-model + preferences)
- **Your financial reality** (accounts, goals, strategies)
- **Your domain's entities** (custom tables + MCPs)
- **How to communicate** (style, tone, autonomy level)

You can now ask the agent to work on your actual tasks — it has context.

## Resuming Interrupted Sessions

If you need to pause and resume:

```bash
hermes --skills agent-onboarding
```

The agent checks `user_profiles.onboarding_stage` and resumes from where you left off.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| "Supabase not connected" | secrets.env not loaded | `source ~/.hermes/secrets.env` |
| "Tables not found" | Migrations not applied | `cd hermes-agent-onboarding && supabase db push --linked` |
| "No provider responds" | API key missing or wrong | Check `config.yaml` provider settings |
| "RLS blocking access" | Wrong API key (anon vs service_role) | Use service_role key, not anon |
