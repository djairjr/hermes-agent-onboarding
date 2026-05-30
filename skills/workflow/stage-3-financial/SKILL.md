---
name: stage-3-financial
version: 1.0.0
description: >
  Stage 3 do meta-skill agent-onboarding. Perfil financeiro baseado em MBTI +
  importação de CSV bancário + definição de metas + estratégias adaptadas ao
  tipo de personalidade. Usa as MCP tools supabase-finance + supabase-worklog.
tags: [financial, mbti, csv, goals, stage-3, meta-skill]
---

# Stage 3 — Perfil Financeiro

## Propósito

Este estágio constrói o perfil financeiro do usuário a partir de 4 camadas:
1. **Importação de dados** (CSV bancário → Supabase)
2. **Perfil MBTI × Finanças** (comportamento financeiro por tipo de personalidade)
3. **Metas financeiras** (curto, médio e longo prazo)
4. **Estratégias adaptadas** ao perfil + metas

## Arquivos do Skill

| Arquivo | Função |
|---------|--------|
| `mbti_financial_profiles.py` | 16 perfis financeiros MBTI em pt-BR com assess_financial_personality() |
| `csv_importer.py` | Importador de CSV bancário com detecção automática de formato |

---

## PARTE 1 — FLUXO CONVERSACIONAL

### 3A: Importação de CSV

```
"Quer que eu analise seus extratos bancários?
Posso ler CSVs do Nubank, Itaú, Inter, Caixa.

Se quiser:
1. Exporte seu extrato como CSV
2. Me passe o arquivo (ou cole o conteúdo)
3. Eu mostro um preview e você confirma antes de importar
```

**Preview mode sempre primeiro:**

```
Formato detectado: Nubank
Período: 01/01/2026 a 31/01/2026
Transações: 45
  Receitas: R$ 8.500,00
  Despesas: R$ 5.230,00
  Saldo do período: R$ 3.270,00

Categorias detectadas:
  Alimentação: 12 transações
  Transporte: 8 transações
  Assinaturas: 4 transações

Importar? (s/N):
```

### 3B: Perfil MBTI × Finanças

Após o MBTI estar registrado (do Stage 1C), perguntar:

```
"Seu tipo MBTI é {type_code} — {name_pt_BR}.
Quer que eu analise como isso influencia suas finanças?

Posso te mostrar:
• Seu perfil financeiro baseado no MBTI
• Pontos fortes e fracos com dinheiro
• Como você tende a poupar, gastar e investir
• Recomendações específicas para seu tipo

Vamos?"
```

Usar `mbti_financial_profiles.py`:

```python
from mbti_financial_profiles import get_profile, assess_financial_personality

profile = get_profile(type_code)
# Exibir: strengths, weaknesses, saving_style, spending_style, etc.

# Se o usuário respondeu perguntas financeiras:
result = assess_financial_personality(answers, type_code)
# Exibir observations + recommendations
```

**Perguntas para calibrar o perfil:**
```
1. "Como você poupa? Automático, manual, ou quando sobra?"
2. "Sua tolerância a risco financeiro? Alta, média ou baixa?"
3. "O que mais te faz gastar? Ferramentas, experiências sociais, conforto?"
4. "Qual frase descreve melhor sua relação com dinheiro?
   A) Dinheiro é liberdade
   B) Dinheiro é segurança
   C) Dinheiro é ferramenta
   D) Dinheiro é para viver"
```

### 3C: Metas Financeiras

```
"Agora, vamos definir metas financeiras.

Curto prazo (6 meses): o que você quer realizar?
Médio prazo (2 anos): qual o próximo degrau?
Longo prazo (5+ anos): qual seu horizonte?

Exemplos:
• Curto: quitar dívida do cartão, fundo de emergência de R$ 10.000
• Médio: entrada de um imóvel, trocar de carro
• Longo: independência financeira, aposentadoria aos 55
```

Registrar via MCP `mcp_supabase_finance_add_goal()`.

### 3D: Estratégias Adaptadas

Combinar MBTI + metas em recomendações:

```
"Baseado no seu perfil INTJ (Arquiteto) e suas metas:

✅ O que já funciona para você:
• Planejamento estratégico — você já pensa no longo prazo
• Disciplina para seguir orçamentos

⚠️ O que precisa de atenção:
• Pode ignorar custos emocionais em decisões financeiras
• Gasto impulsivo em projetos de alto impacto

📋 Recomendações:
1. Automatizar 30% da renda para investimentos
2. Fundo de emergência de 12 meses
3. 10% em 'projetos estratégicos'
4. Planilha de patrimônio líquido mensal
5. 5% para 'gasto livre'

Quer que eu implemente alguma dessas estratégias?"
```

Usar `assess_financial_personality()` com as respostas do usuário + type_code.

---

## PARTE 2 — MCP Tools Disponíveis

O Stage 3 usa as seguintes MCP tools da extensão `supabase-finance`:

| Tool | Função |
|------|--------|
| `mcp_supabase_finance_list_accounts` | Listar contas bancárias |
| `mcp_supabase_finance_add_account` | Adicionar conta |
| `mcp_supabase_finance_add_transaction` | Registrar transação |
| `mcp_supabase_finance_list_transactions` | Listar transações com filtros |
| `mcp_supabase_finance_add_goal` | Adicionar meta financeira |
| `mcp_supabase_finance_list_goals` | Listar metas |
| `mcp_supabase_finance_list_categories` | Listar categorias |
| `mcp_supabase_finance_get_dashboard` | Dashboard financeiro |
| `mcp_supabase_finance_set_budget` | Definir orçamento mensal |
| `mcp_supabase_worklog_log_work` | Registrar trabalho com valor |
| `mcp_supabase_worklog_get_month` | Resumo mensal de trabalho + receitas |

---

## PARTE 3 — COMO INVOCAR (do agent-onboarding)

```python
# 1. Carregar este skill
# 2. Seguir fluxo conversacional 3A → 3B → 3C → 3D
# 3. Usar mbti_financial_profiles.py para perfil MBTI × finanças
# 4. Usar csv_importer.py para importar extratos (modo preview → confirm → import)
# 5. Registrar metas via MCP tools
# 6. Salvar em user_profiles.financial_profile_completed = true
```

---

## Verificação

1. Perfil MBTI × Finanças carrega para todos os 16 tipos
2. CSV preview mostra resumo correto antes de importar
3. Transações são importadas via REST API com categorização automática
4. Metas são registradas via MCP tools

## Pitfalls

1. **NUNCA importar CSV sem preview/confirmação do usuário**
2. **NUNCA armazenar CSV bruto no Supabase ou em disco** — processar em memória
3. **NUNCA logar dados financeiros completos** — só resumo
4. **MBTI é orientativo, não determinístico** — o perfil financeiro do usuário pode divergir do tipo
5. **Se usuário não tem conta Supabase configurada, ofertar análise textual em vez de registrar**
