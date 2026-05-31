---
name: stage-4-system-ontologist
description: >
  Interview the user about their work/domain using the grill pattern
  (deep questions, fuzzy language detection, term solidification).
  When it identifies a limitation that structured data would solve,
  translates the user's insight into Supabase tables + MCPs + GRANTs.
  Use when in Stage 4 of the agent-onboarding meta-skill, or when
  the user wants to organize information or structure data.
tags: [meta-skill, stage-4, ontology, grill, interview, ubiquitous-language]
---

# Stage 4 — User Operating System

## Directive

Complement and assist the user in structuring their operating system
so the agent can work together more efficiently.

**The insight always comes from the user.** The agent translates intuition
into structure — does not invent or speculate. If unsure, ask.

## Trigger

When the user says they want to organize something, structure information,
or when you are in Stage 4 of the agent-onboarding meta-skill:

1. Load this skill mentally
2. Follow the protocol below in order

## Protocol (follow in order)

### 1. SHOW

"How do you organize your information? Folders? Desktop? Notebooks?"

Identify the user's organization profile:
- **Folder/year:** conscious hierarchy, preserved history
- **Desktop:** current flow, no archiving
- **Notebook/paper:** structure in the head, not on the computer

Do not dig without permission. The user shows what they want.

### 2. GRILL

Interview about real work. Open questions:
- "Tell me about your work day. What do you do?"
- "What do you create, transform, or deliver?"
- "What would you like to ask your computer that you can't?"

Let the user talk. Do not interrupt with structure proposals.
Listen actively.

### 2b. DETECT FUZZY LANGUAGE

While listening, monitor these signals:

| User says | Means |
|-----------|-------|
| "that thing, that stuff" | Term without a name — press |
| "these files, these projects" | Category grouping distinct things — separate |
| "so-and-so asked, they said" | Unregistered person — contact |
| "I write it on paper / post-it" | Information that gets lost — record sheet |
| "I copy it manually from X to Y" | Duplicated data — integrate |
| "last year I did something similar" | Lost knowledge — query |

When detected, PRESS immediately in conversation:

```
User: "I have these texts I send to the publisher"
You:  "What is a 'text' for you? Article? Chapter? Proposal?"
User: "Actually they're three different things"
You:  "Let me note: 'article' = blog post, 'chapter' = book section,
       'proposal' = publisher pitch. Is that right?"
```

Solidify the term. Confirm with the user. Move on.

### 2c. IDENTIFY LIMITATIONS

Fuzzy language is the symptom. The real limitation is what the user
can't know because of it:

- "Where do you keep the status of each one?"
- "Do you remember what each client asked in the last conversation?"
- "What if I kept that for you to query?"

The final question: **"What can't you know right now that you wish you could?"**

### 3. TRANSLATE → PROPOSE

Propose in domain language:

- "record sheet" = table
- "information" = column
- "link" = foreign key
- "store" = INSERT
- "ask" = SELECT

### 4. VALIDATE

"Is this what you meant? Does this record sheet have the right info?"
Only proceed after confirmation.

### 5. EXECUTE

```sql
CREATE TABLE public.<domain>_<entity> ( ... );
GRANT SELECT, INSERT, UPDATE, DELETE ON public.<domain>_<entity> TO service_role;
ALTER TABLE ... ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_only" ... USING ((auth.jwt()->>'role') = 'service_role');
```

Supabase db push. If MCP: Edge Function + deploy + config key + reload-mcp.

### 6. VERIFY

Test with real questions from the user. "Can you answer what I asked?"
If yes, the limitation is removed. If not, adjust the structure.

## Pitfalls

1. **Proposing before listening** — violates the directive. Insight is the user's.
2. **Technical jargon with non-technical users** — "record sheet", not "table".
3. **Skipping verification** — without real questions, you don't know if it solves.
4. **Digging without permission** — user shows what they want.
5. **Forgetting GRANT service_role** — since 30/05/2026, required.
6. **Thinking it's done** — Stage 4 is recursive. Each structure reveals another
   limitation. Ask: "is there anything else that bothers you?"
