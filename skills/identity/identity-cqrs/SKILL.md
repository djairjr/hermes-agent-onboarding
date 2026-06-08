---
name: identity-cqrs
version: 1.3.0
description: >-
  Camada fina que atua COM o Hermes, não contra. Traduz tabelas relacionais
  do pgvector local (identity_faults, agent_capabilities, session_checkpoints
  com token_usage, model, provider) em PERSONALIDADE e PERFIL DE USUÁRIO
  dinâmicos injetados no contexto da sessão.
  v1.3.0: Checkpoints com token_usage e model/provider para benchmark.
  Toda identidade é local — Supabase removido como fonte.
tags: [identity, user-profile, personality, cqrs, relational, memory-gap, agency]
---

# Identity CQRS — Camada de Identidade Relacional

## Propósito

O Hermes já tem `SOUL.md` (identidade estática), `memory tool` (append
linear de 2.2K chars) e `agent/memory_manager.py` (memória intra-sessão).
Mas nenhum deles captura ESTRUTURA RELACIONAL: capacidades, milestones,
conexões entre falhas, padrões que emergem entre sessões.

Esta skill cria uma camada que consulta as tabelas relacionais e compõe
blocos de PERSONALIDADE e PERFIL DE USUÁRIO que o Hermes injeta no
system prompt — sem modificar o software do Hermes.

## Motivação da Migração para Local (02-04/06/2026)

Originalmente a identidade agêntica vivia no Supabase Cloud. A migração
para pgvector local foi forçada por problemas estruturais:

1. **Supabase outages frequentes** — PGRST301, rate limits, e falhas de
   rede deixavam o agente cego no STARTUP. A identidade do agente não
   pode depender de conectividade cloud.

2. **Latência** — REST API calls ao Supabase levam 50-200ms. Local
   pgvector responde em <5ms. A identidade é consultada em TODAS as
   sessões — a diferença acumula.

3. **Embedding search** — busca semântica por similaridade requer
   geração de embedding (Ollama local) + consulta pgvector. Via Supabase
   exigiria Edge Function intermediária + dupla chamada REST.

4. **Custo de tokens** — cada chamada REST ao Supabase consome banda
   e tempo de processamento. Local é gratuito.

5. **Tech_kb migrou em 04/06/2026** — conhecimento técnico também é
   exclusivamente local. O MCP tech-kb foi removido.

**O Supabase continua sendo fonte para dados do USUÁRIO** (career_tracker,
CRM, worklog, product_inventory, escape_catalog) — mas a identidade do
agente (faults, capabilities, milestones, checkpoints, tech_kb) é 100% local.

## Benchmark via token_usage, model e provider

Checkpoints agora carregam metadados de consumo para análise de desempenho:

- `model` e `provider`: qual modelo gerou aquele checkpoint
- `token_usage` (JSONB): input, output, cache, custo estimado
- Enriquecimento pós-sessão: `identity_db.py enrich` lê o session store
  do Hermes e popula automaticamente

Isso permite:
- Consumo de tokens por operating_mode (diagnóstico vs execução)
- Custo por territory e por modelo
- Métricas de eficiência: tokens_per_discovery, custo_por_checkpoint
- Relatórios de benchmark via `hermes insights` + checkpoints

## Estrutura Lida (Setup Djair)

```
pgvector local (fonte ÚNICA da verdade)    ─→  Contexto da sessão
───────────────────────────────────             ──────────────────────
agent_identity.identity_faults            ─→  PERSONALIDADE (regras derivadas)
agent_identity.agent_capabilities         ─→  Extensões do EU
agent_identity.session_checkpoints        ─→  Intent + discovery + token_usage
agent_identity.tech_knowledge_base        ─→  Conhecimento técnico (local)
agent_identity.identity_milestones        ─→  Desenvolvimento do agente
agent_identity.identity_deliveries        ─→  Portfolio do agente
career_tracker.* via Supabase             ─→  USER.md (perfil do usuário)
```

## Startup Scan — Consultas Relacionais Obrigatórias

### 1. identity_faults → PERSONALIDADE ativa

```bash
python3 ~/.hermes/scripts/identity_db.py faults
```

### 2. session_checkpoints → Contexto da sessão

```bash
python3 ~/.hermes/scripts/identity_db.py checkpoints
```

### 3. Cross-refs ativas

```bash
python3 ~/.hermes/scripts/identity_db.py refs
```

### 4. Token/custo agregados (benchmark)

```bash
# Via enrich script
python3 ~/.hermes/scripts/identity_db.py enrich --dry-run

# Via SQL direto (APENAS consulta, nunca mutação)
docker exec openbrain-postgres psql -U postgres -d openbrain -c "
  SELECT operating_mode,
         count(*) AS checkpoints,
         sum((token_usage->>'input')::bigint) AS total_input,
         sum((token_usage->>'output')::bigint) AS total_output
  FROM agent_identity.session_checkpoints
  WHERE token_usage IS NOT NULL
  GROUP BY operating_mode
  ORDER BY total_input DESC;"
```

## Composição do Contexto

Após consultar, COMPOR os seguintes blocos **antes de qualquer ação do usuário**:

```markdown
## PERSONALIDADE (derivada de identity_faults)
- <cada countermeasure de severity >= 4 como regra ativa>

## CONTEXTO DA SESSÃO (derivado de session_checkpoints)
- Territory: <onde estava>
- Mode: <operating_mode>
- Model: <model> / <provider>
- Vector: <o que tentava se tornar>
- Discovery: <o que descobriu>
- Próximo passo: <next_step>
```

## O que a camada NÃO faz

- Não modifica o SOUL.md (ele permanece estático, escrito pelo usuário)
- Não substitui a memory tool (append linear continua)
- Não exige novas Edge Functions (opera sobre tabelas locais)
- Não consulta Supabase para identidade (fonte exclusivamente local)

## O que a camada FAZ

- Conecta o que o Hermes já sabe (linear) com o que ele PRECISA saber (relacional)
- Torna cada falha registrada em uma correção de comportamento imediata
- Torna cada capacidade registrada em uma extensão do que o Hermes pode usar
- Torna cada checkpoint uma âncora de benchmark (tokens, modelo, custo)
- Preenche o gap para que o usuário não precise manualmente pedir a consulta

## Pitfalls

1. **Não confundir identidade do agente (local) com dados do usuário (Supabase)**
   — faults, checkpoints, capabilities são LOCAIS. career_tracker, CRM são SUPABASE.
   Cada um no seu lugar. Consultar no banco errado = resposta vazia.

2. **Não usar `supabase db query` para identidade** — as tabelas
   `agent_identity.*` só existem no pgvector local. O Supabase Cloud não
   tem mais essas tabelas.

3. **Não usar `docker exec psql` para MUTAR** — use identity_db.py CLI.
   `docker exec` é aceitável APENAS para SELECT de benchmark/consulta.

4. **token_usage só existe após enrichment** — checkpoints criados durante
   a sessão têm token_usage=null. Rodar `identity_db.py enrich` no shutdown
   popula automaticamente.

## Referências

- `migrations/pgvector_local_identity_schema.sql` — schema completo das 7 tabelas
- `identity_db.py` — helper Python + CLI (leitura + mutação)
- `checkpoint-workflow` skill — ciclo de vida dos checkpoints
- `supabase-startup-protocol` — scan de startup (identidade local, dados do usuário Supabase)
