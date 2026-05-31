---
name: mbti-guru-hermes
version: 1.0.0
description: >
  MBTI engine for Hermes within the orchestrator meta-skill (agent-onboarding).
  Administers the full MBTI Guru test in conversation — A/B questions, scoring
  identical to the original, descriptions of all 16 types in English.
  4 versions: Quick (70q), Standard (93q), Extended (144q), Professional (200q).
tags: [mbti, guru, personality, test, conversation, stage-1c, meta-skill]
---

# MBTI Guru Hermes — Typing Engine for Conversation

## Purpose

This skill enables Hermes to administer the full MBTI Guru test
directly in conversation. The agent asks each question in A/B format,
accumulates responses by dimension (E/I, S/N, T/F, J/P), calculates
the type using scoring identical to the original Guru, and records
the result in `user_mbti` in Supabase.

## Skill Files

| File | Role |
|---------|--------|
| `questions_pt_BR.py` | Database of 200 questions in Portuguese (4 versions: 70, 93, 144, 200) |
| `scorer.py` | Scoring identical to the original Guru |
| `types_pt_BR.py` | 16 types with descriptions in Brazilian Portuguese |

---

## PART 1 — CONVERSATIONAL FLOW

### 1. Introduction

```
You: "Do you know MBTI? Do you know your type?"
```

**If they know:** ask for their type and validate with 4 quick questions
(one per dimension).

**If they don't know:** explain the 4 dimensions and offer the 4 versions:

```
"MBTI has 4 dimensions:
• Energy: Extraversion (E) vs Introversion (I)
• Information: Sensing (S) vs Intuition (N)
• Decision: Thinking (T) vs Feeling (F)
• Structure: Judging (J) vs Perceiving (P)

There are 16 personality types in total.

MBTI Guru offers 4 test versions:
1. Quick — 70 questions (~10 min)
2. Standard — 93 questions (~15 min)
3. Extended — 144 questions (~25 min)
4. Professional — 200 questions (~35 min)

Which one would you like?"
```

### 2. Test Administration

**Each question:**
```
Question X/N:
[A] <option A>
[B] <option B>

Reply A or B:
```

**Wait for response.** Only proceed after receiving A or B.
If ambiguous: "Reply only A or B."

**Store internally:**
```python
answers = [(1, "A"), (2, "B"), ...]  # (question_id, selected_option)
```

### 3. Finalization

After the last question:

```python
type_code, scores = calculate_type(answers)
```

Display result:
```
=== MBTI RESULT ===
Your type: {type_code} — {name}

Dimensions:
• E/I: {score_EI}% ({pref}) — {clarity_level}
• S/N: {score_SN}% ({pref}) — {clarity_level}
• T/F: {score_TF}% ({pref}) — {clarity_level}
• J/P: {score_JP}% ({pref}) — {clarity_level}

{summary}
```

### 4. Registration in Supabase

Insert into `user_mbti`:

```json
{
  "type_code": "INTJ",
  "ei_score": 65.2,
  "sn_score": 72.1,
  "tf_score": 80.5,
  "jp_score": 58.3,
  "version": "professional_test",
  "completed_at": "2026-05-31T..."
}
```

---

## PART 2 — SCORING (identical to original Guru)

### Logic

```python
def calculate_type(answers):
    # 1. Determine version by number of answers
    # 2. For each dimension (EI, SN, TF, JP), count:
    #    - answers favoring the first pole
    #    - total questions answered in that dimension
    # 3. score = (first_pole_count / total) * 100
    # 4. If score > 50: letter is the first pole
    #    If score < 50: letter is the second pole
    # 5. type_code = EI_letter + SN_letter + TF_letter + JP_letter
    # 6. clarity = abs(score - 50) * 2
```

### Clarity Levels

| Clarity | Level |
|---------|-------|
| ≤ 25% | Slight |
| ≤ 50% | Moderate |
| ≤ 75% | Clear |
| > 75% | Very Clear |

---

## PARTE 3 — INTEGRAÇÃO COM O META-SKILL

### Como invocar

No skill `agent-onboarding`, Stage 1C:

1. Carregar este skill com `skill_load('mbti-guru-hermes')`
2. Importar `questions_pt_BR` e `scorer`
3. Executar o fluxo conversacional (Parte 1)
4. Registrar resultado em `user_mbti`

### Tabela `user_mbti`

```sql
CREATE TABLE user_mbti (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES user_profiles(id),
  type_code TEXT NOT NULL,            -- "INTJ"
  ei_score NUMERIC, sn_score NUMERIC,
  tf_score NUMERIC, jp_score NUMERIC,
  ei_clarity TEXT, sn_clarity TEXT,
  tf_clarity TEXT, jp_clarity TEXT,
  version TEXT NOT NULL,              -- quick|standard|extended|professional
  completed_at TIMESTAMPTZ DEFAULT now(),
  mbti_data JSONB                    -- raw answers + full scores
);
```

---

## PART 4 — AUTONOMOUS EXECUTION (prompt / script mode)

### `run_mbti_test()` function

The skill can be executed without establishing direct context with the current
user — for example, so another person can take the test via forwarded message,
or for automated batch testing.

```python
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from questions_pt_BR import get_questions
from scorer import calculate_type, format_scores, calculate_clarity
from types_pt_BR import get_type

def run_mbti_test(answers: list, version: int = 70) -> dict:
    """
    Runs the complete MBTI test without interaction.


    Args:
        answers: lista de (question_id, "A"|"B")
        version: 70, 93, 144, ou 200

    Returns:
        {
            "type_code": "INTJ",
            "name_pt_BR": "O Arquiteto",
            "scores": {"EI": 65.2, "SN": 72.1, ...},
            "clarity": {"EI": "Moderada", ...},
            "summary_pt_BR": "...",
            "strengths": [...],
            "weaknesses": [...]
        }
    """
    questions = get_questions(version)
    type_code, scores = calculate_type(answers, questions)
    tdata = get_type(type_code)

    clarities = {}
    for dim in ["EI", "SN", "TF", "JP"]:
        _, level = calculate_clarity(scores.get(dim, 50))
        clarities[dim] = level

    return {
        "type_code": type_code,
        "name_pt_BR": tdata.get("name_pt_BR", type_code),
        "scores": scores,
        "clarity": clarities,
        "summary_pt_BR": tdata.get("summary_pt_BR", ""),
        "strengths": tdata.get("strengths_pt_BR", []),
        "weaknesses": tdata.get("weaknesses_pt_BR", []),
        "careers": tdata.get("careers_pt_BR", [])
    }
```

### Exemplo de uso via terminal (CLI)

```bash
cd ~/.hermes/skills/workflow/mbti-guru-hermes
python3 -c "
from questions_pt_BR import get_questions
from types_pt_BR import get_type
# Gerar respostas simuladas
qs = get_questions(70)
answers = [(q['id'], 'A' if q['id'] % 2 == 0 else 'B') for q in qs]
import run_mbti_test
result = run_mbti_test.run_mbti_test(answers, 70)
print(f\"Tipo: {result['type_code']} — {result['name_pt_BR']}\")
print(''.join(result['summary_pt_BR']))
"
```

### Como usar em conversa

To administer the test directly in conversation with the user:

1. **Importar o banco de perguntas:**
   ```python
   sys.path.insert(0, '<hermes_skills_dir>/workflow/mbti-guru-hermes')
   from questions_pt_BR import get_questions, get_question_count
   from scorer import calculate_type, format_scores, calculate_clarity
   from types_pt_BR import get_type
   ```

2. **Get questions from the chosen version:**
   ```python
   questions = get_questions(70)  # or 93, 144, 200
   ```

3. **Ask one by one in conversation**, accumulating answers:
   ```python
   answers = []  # [(q_id, "A"|"B"), ...]
   ```

4. **At the end, calculate and display:**
   ```python
   type_code, scores = calculate_type(answers, get_questions(len(answers)))
   tdata = get_type(type_code)
   report = format_scores(scores)
   ```

---

## Verification

1. Questions 1-70 load correctly: `len(get_questions(70)) == 70`
2. Scoring reproduces the Guru result for known inputs
3. All 16 types have descriptions available (e.g. `types_pt_BR.py` for pt-BR locale)
4. Registration in `user_mbti` persists in Supabase

## Pitfalls

1. **Never skip questions** — each question contributes to a dimension score
2. **Never reduce versions** — 70/93/144/200 are fixed, each with exact counts
3. **Never interpret answers** — accept only "A" or "B", no nuances
4. **Never summarize the result** — show full scores + description
5. **Do not confuse preference_a with correct answer** — there is no correct answer, it's preference
