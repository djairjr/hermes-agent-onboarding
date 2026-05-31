---
name: mbti-guru-hermes
version: 1.0.0
description: >
  Motor de MBTI para Hermes dentro do meta-skill orquestrador (agent-onboarding).
  Administra o teste completo do MBTI Guru em conversa — perguntas A/B, pontuação
  idêntica ao original, descrições dos 16 tipos em português brasileiro.
  4 versões: Rápido (70q), Padrão (93q), Estendido (144q), Profissional (200q).
tags: [mbti, guru, personalidade, teste, conversa, stage-1c, meta-skill]
---

# MBTI Guru Hermes — Motor de Tipagem para Conversa

## Propósito

Esta skill permite que o Hermes administre o teste completo do MBTI Guru
diretamente em conversa. O agente pergunta cada questão em formato A/B,
acumula respostas por dimensão (E/I, S/N, T/F, J/P), calcula o tipo
usando pontuação idêntica ao Guru original, e registra o resultado
em `user_mbti` no Supabase.

## Arquivos da Skill

| Arquivo | Função |
|---------|--------|
| `questions_pt_BR.py` | Banco de 200 perguntas em português (4 versões: 70, 93, 144, 200) |
| `scorer.py` | Pontuação idêntica ao Guru original |
| `types_pt_BR.py` | 16 tipos com descrições em português brasileiro |

---

## PARTE 1 — FLUXO CONVERSACIONAL

### 1. Introdução

```
Você: "Você conhece MBTI? Sabe seu tipo?"
```

**Se conhece:** perguntar o tipo e validar com 4 perguntas rápidas.

**Se não conhece:** explicar as 4 dimensões e oferecer as 4 versões.

### 2. Administração do Teste

Cada pergunta:
```
Questão X/N:
[A] <opção A>
[B] <opção B>

Responda A ou B:
```

### 3. Finalização

Após a última pergunta, exibir resultado com dimensões, pontuações
e descrição completa do tipo.

### 4. Registro no Supabase

Inserir em `user_mbti` com type_code, scores, version, completed_at.

---

## PARTE 2 — PONTUAÇÃO (idêntica ao Guru original)

### Lógica

```python
def calculate_type(answers):
    # 1. Determinar versão pelo número de respostas
    # 2. Para cada dimensão (EI, SN, TF, JP), contar:
    #    - respostas favoráveis ao primeiro polo
    #    - total de perguntas respondidas na dimensão
    # 3. score = (count_primeiro_polo / total) * 100
    # 4. Se score > 50: letra é o primeiro polo
    #    Se score < 50: letra é o segundo polo
    # 5. type_code = EI_letter + SN_letter + TF_letter + JP_letter
    # 6. clarity = abs(score - 50) * 2
```

---

## PARTE 3 — INTEGRAÇÃO COM O META-SKILL

No skill `agent-onboarding`, Stage 1C:

1. Carregar este skill
2. Importar `questions_pt_BR` e `scorer`
3. Executar o fluxo conversacional (Parte 1)
4. Registrar resultado em `user_mbti`

---

## PARTE 4 — EXECUÇÃO AUTÔNOMA (modo prompt / script)

### Função `run_mbti_test()`

A skill pode ser executada sem estabelecer contexto direto com o usuário
atual — por exemplo, para outra pessoa fazer o teste via mensagem
encaminhada, ou para teste batch automatizado.

---

## Verificação

1. Perguntas 1-70 carregam corretamente: `len(get_questions(70)) == 70`
2. Pontuação reproduz resultado do Guru para entradas conhecidas
3. Todos os 16 tipos têm descrições disponíveis
4. Registro em `user_mbti` persiste no Supabase

## Pitfalls

1. **Nunca pular perguntas** — cada pergunta contribui para uma dimensão
2. **Nunca reduzir versões** — 70/93/144/200 são fixas
3. **Nunca interpretar respostas** — aceitar apenas "A" ou "B"
4. **Nunca resumir resultado** — mostrar scores completos + descrição
5. **Não confundir preferência com resposta correta** — não existe resposta certa
