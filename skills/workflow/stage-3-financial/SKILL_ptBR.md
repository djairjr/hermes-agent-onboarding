---
name: stage-3-financial
version: 1.0.0
description: >
  Stage 3 do meta-skill agent-onboarding. Perfil financeiro baseado em MBTI +
  importação de CSV bancário + definição de metas + estratégias adaptadas ao
  tipo de personalidade. Usa ferramentas MCP supabase-finance + supabase-worklog.
tags: [financeiro, mbti, csv, metas, stage-3, meta-skill]
---

# Stage 3 — Perfil Financeiro

## Propósito

Este stage constrói o perfil financeiro do usuário em 4 camadas:
1. **Importação de dados** (CSV bancário → Supabase)
2. **Perfil MBTI × Finanças** (comportamento financeiro por tipo de personalidade)
3. **Metas financeiras** (curto, médio e longo prazo)
4. **Estratégias adaptadas** ao perfil + metas

## Arquivos da Skill

| Arquivo | Função |
|---------|--------|
| `mbti_financial_profiles.py` | 16 perfis financeiros MBTI em português com assess_financial_personality() |
| `csv_importer.py` | Importador de CSV bancário com detecção automática de formato |

---

## PARTE 1 — FLUXO CONVERSACIONAL

### 3A: Importação CSV

Oferecer análise de extratos bancários em CSV. Detectar formato
automaticamente. Mostrar prévia. Confirmar antes de importar.

### 3B: MBTI × Perfil Financeiro

Após MBTI conhecido (Stage 1C), mostrar perfil financeiro do tipo:
forças, fraquezas, saving_style, spending_style, risk_profile.
Fazer 4 perguntas de calibração. Chamar assess_financial_personality().

### 3C: Metas Financeiras

Curto prazo (6 meses), Médio prazo (2 anos), Longo prazo (5+ anos).
Registrar via MCP mcp_supabase_finance_add_goal().

### 3D: Estratégias Adaptadas

Combinar perfil MBTI + metas em recomendações acionáveis:
regras automáticas de poupança, alocação de investimentos,
meta de fundo de emergência, guardrails de gastos.

---

## PARTE 2 — FERRAMENTAS MCP DISPONÍVEIS

Stage 3 usa: mcp_supabase_finance_list_accounts, add_account,
add_transaction, list_transactions, add_goal, list_goals,
list_categories, get_dashboard, set_budget, mcp_supabase_worklog_log_work,
mcp_supabase_worklog_get_month.

---

## PARTE 3 — COMO INVOCAR (a partir do agent-onboarding)

Seguir fluxo conversacional 3A → 3B → 3C → 3D.
Usar mbti_financial_profiles.py para perfil MBTI × finanças.
Usar csv_importer.py para importar extratos (prévia → confirmar → importar).
Registrar metas via MCP tools. Salvar user_profiles.financial_profile_completed = true.

## Verificação

1. Perfil MBTI × Finanças carrega para todos os 16 tipos
2. Prévia CSV mostra resumo correto antes de importar
3. Transações importadas via REST API com categorização automática
4. Metas registradas via MCP tools

## Pitfalls

1. **NUNCA importar CSV sem prévia/confirmação do usuário**
2. **NUNCA armazenar CSV bruto no Supabase ou em disco** — processar em memória apenas
3. **NUNCA logar dados financeiros completos** — apenas resumo
4. **MBTI é orientação, não determinístico** — o perfil financeiro pode diferir do tipo
5. **Se usuário não tem conta Supabase configurada, oferecer análise baseada em texto**
