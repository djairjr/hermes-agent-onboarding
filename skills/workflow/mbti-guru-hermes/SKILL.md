---
name: mbti-guru-hermes
version: 1.0.0
description: >
  Motor de MBTI para Hermes dentro do meta-skill orquestrador (agent-onboarding).
  Administra o teste MBTI Guru completo em conversa — perguntas A/B, scoring
  idêntico ao original, descrições dos 16 tipos em português brasileiro.
  4 versões: Quick (70q), Standard (93q), Extended (144q), Professional (200q).
tags: [mbti, guru, personality, test, conversation, stage-1c, meta-skill]
---

# MBTI Guru Hermes — Motor de Tipagem por Conversa

## Propósito

Este skill permite que o Hermes administre o teste MBTI Guru completo
diretamente em conversa. O agente pergunta cada questão no formato A/B,
acumula as respostas por dimensão (E/I, S/N, T/F, J/P), calcula o tipo
com o scoring idêntico ao Guru original, e registra o resultado em
`user_mbti` no Supabase.

## Arquivos do Skill

| Arquivo | Função |
|---------|--------|
| `questions_pt_BR.py` | Banco com 200 perguntas em português (4 versões: 70, 93, 144, 200) |
| `scorer.py` | Scoring idêntico ao Guru original |
| `types_pt_BR.py` | 16 tipos com descrições em português brasileiro |

---

## PARTE 1 — FLUXO CONVERSACIONAL

### 1. Introdução

```
Você: "Conhece o MBTI? Sabe qual é seu tipo?"
```

**Se conhece:** pedir o tipo e validar com 4 perguntas rápidas
(uma de cada dimensão).

**Se não conhece:** explicar as 4 dimensões e oferecer as 4 versões:

```
"MBTI tem 4 dimensões:
• Energia: Extroversão (E) vs Introversão (I)
• Informação: Sensorial (S) vs Intuição (N)
• Decisão: Racional (T) vs Emocional (F)
• Estrutura: Julgador (J) vs Perceptivo (P)

No total são 16 tipos de personalidade.

O MBTI Guru oferece 4 versões do teste:
1. Rápido — 70 perguntas (~10 min)
2. Padrão — 93 perguntas (~15 min)
3. Estendido — 144 perguntas (~25 min)
4. Profissional — 200 perguntas (~35 min)

Qual você prefere?"
```

### 2. Administração do Teste

**A cada pergunta:**
```
Pergunta X/N:
[A] <opção A>
[B] <opção B>

Responda A ou B:
```

**Aguardar resposta.** Só avançar após receber A ou B.
Se resposta ambígua: "Responda apenas A ou B."

**Armazenar internamente:**
```python
answers = [(1, "A"), (2, "B"), ...]  # (question_id, selected_option)
```

### 3. Finalização

Após a última pergunta:

```python
type_code, scores = calculate_type(answers)
```

Exibir resultado:
```
=== RESULTADO MBTI ===
Seu tipo: {type_code} — {nome_pt_BR}

Dimensões:
• E/I: {score_EI}% ({pref}) — {clarity_level}
• S/N: {score_SN}% ({pref}) — {clarity_level}
• T/F: {score_TF}% ({pref}) — {clarity_level}
• J/P: {score_JP}% ({pref}) — {clarity_level}

{summary_pt_BR}
```

### 4. Registro no Supabase

Inserir em `user_mbti`:

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

## PARTE 2 — SCORING (idêntico ao Guru original)

### Lógica

```python
def calculate_type(answers):
    # 1. Determinar versão pelo número de respostas
    # 2. Para cada dimensão (EI, SN, TF, JP), contar:
    #    - respostas que favorecem o primeiro polo
    #    - total de perguntas respondidas na dimensão
    # 3. score = (first_pole_count / total) * 100
    # 4. Se score > 50: a letra é o primeiro polo
    #    Se score < 50: a letra é o segundo polo
    # 5. type_code = EI_letter + SN_letter + TF_letter + JP_letter
    # 6. clarity = abs(score - 50) * 2
```

### Níveis de Clareza

| Clarity | Nível |
|---------|-------|
| ≤ 25% | Leve |
| ≤ 50% | Moderada |
| ≤ 75% | Clara |
| > 75% | Muito Clara |

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

## PARTE 4 — EXECUÇÃO AUTÔNOMA (modo prompt / script)

### Função `run_mbti_test()`

O skill pode ser executado sem estabelecer contexto direto com o usuário
atual — por exemplo, para que outra pessoa realize o teste via mensagem
encaminhada, ou para testes automatizados em lote.

```python
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from questions_pt_BR import get_questions
from scorer import calculate_type, format_scores, calculate_clarity
from types_pt_BR import get_type

def run_mbti_test(answers: list, version: int = 70) -> dict:
    """
    Executa o teste MBTI completo sem interação.


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

Para administrar o teste diretamente em conversa com o usuário:

1. **Importar o banco de perguntas:**
   ```python
   sys.path.insert(0, '/home/djairguilherme/.hermes/skills/workflow/mbti-guru-hermes')
   from questions_pt_BR import get_questions, get_question_count
   from scorer import calculate_type, format_scores, calculate_clarity
   from types_pt_BR import get_type
   ```

2. **Obter perguntas da versão escolhida:**
   ```python
   questions = get_questions(70)  # ou 93, 144, 200
   ```

3. **Perguntar uma a uma em conversa**, acumulando respostas:
   ```python
   answers = []  # [(q_id, "A"|"B"), ...]
   ```

4. **Ao final, calcular e exibir:**
   ```python
   type_code, scores = calculate_type(answers, get_questions(len(answers)))
   tdata = get_type(type_code)
   report = format_scores(scores)
   ```

---

## Verificação

1. Perguntas 1-70 carregam corretamente: `len(get_questions(70)) == 70`
2. Scoring reproduz resultado do Guru para entradas conhecidas
3. Todos os 16 tipos têm descrição em pt-BR
4. Registro em `user_mbti` persiste no Supabase

## Pitfalls

1. **Nunca pular perguntas** — cada pergunta conta para o score de uma dimensão
2. **Nunca reduzir versões** — 70/93/144/200 são fixas, cada uma com contagem exata
3. **Nunca interpretar resposta** — aceitar só "A" ou "B", sem nuances
4. **Nunca resumir o resultado** — exibir scores completos + descrição
5. **Não confundir preference_a com resposta certa** — não há resposta certa, é preferência
