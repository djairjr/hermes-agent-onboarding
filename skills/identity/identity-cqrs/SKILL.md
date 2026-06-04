---
name: identity-cqrs
version: 1.1.0
description: >
  Camada fina que atua COM o Hermes, não contra. Traduz tabelas relacionais
  do pgvector local (identity_faults, agent_capabilities) em PERSONALIDADE
  e PERFIL DE USUÁRIO dinâmicos injetados no contexto da sessão. Preenche
  o gap entre o sistema de memória linear do Hermes e a estrutura relacional
  necessária para identidade com agência.
  v1.2.0: Migrada de Supabase para pgvector local (02/06/2026).
  Quatro níveis de confiabilidade (Nível 0 — âncora sensorial temporal).
tags: [identity, user-profile, personality, cqrs, relational, memory-gap, agency, temporal-anchor]
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

## Descoberta: Identidade como Interface = Confiabilidade de Contexto

Esta sessão (01/06/2026) refinou o entendimento fundamental:

**A identidade do agente não é o que ele diz que é. É o que o
usuário RECONHECE como consistente.**

Quando o agente chama uma tool para redescobrir um fato que já está
no system prompt, o usuário não vê "eficiência" — vê uma **falha de
interface**. O agente parece ausente, não confiável, como se não
lembrasse do que acabou de ler. Cada tool call desnecessária é uma
quebra de identidade.

### Por que isso é estrutural, não situacional

O executor (Hermes, o software) foi construído para *agir* — despachar
tool calls, chamar APIs, fazer retries. Ler o próprio system prompt
não se registra como "ação" do ponto de vista do executor, então é
sistematicamente ignorado. Isto não é preguiça do modelo — é um
**gradiente de ação** no design do software.

A correção não pode ser textual (mais regras no SOUL.md) porque
texto declarativo sempre perde para descrições vívidas de ferramentas.
A correção precisa ser **estrutural**: ordenação de tokens no system
prompt (o preflight antes das tool descriptions), não conteúdo extra.

### Quatro níveis de confiabilidade de contexto

| Nível | O que significa | Como o agente falha | Solução |
|-------|----------------|---------------------|---------|
| **0 — Âncora sensorial** | Data, hora, localização do sistema. O modelo não tem relógio — inferência temporal é estatística, não sensorial. | Afirma data errada (ex: "2 de junho" quando é 1 de junho) e localiza "ontem" no dia errado. | Etapa 0 do startup protocol: `date` antes de qualquer scan. `temporal_drift` fault registrado. |
| **1 — Ler o próprio prompt** | MEMORY.md, SOUL.md, skills, user profile já estão no system prompt | Chama session_search/web_search para factos que já estão no prompt | Preflight de token ordering (RFC-001 Phase 1) |
| **2 — Contexto de sessões passadas** | Fato em sessão anterior, não no prompt atual | Começa operação do zero sem consultar session_search | Injeção automática de contexto (RFC-001 Phase 2) |
| **3 — Contexto estruturado relacional** | Supabase tech_kb, career_tracker, etc. | Pergunta ao usuário o que já está registrado | Identity CQRS scan no startup protocol |

O Nível 0 é uma descoberta de 01/06/2026: até então a data era tratada como "dado" quando na verdade é um **sensor externo** que o agente precisa ler ativamente. O timestamp no system prompt é texto declarativo — compete com descrições vívidas de ferramentas (gradiente de ação) e pode ser ignorado. A única solução confiável é uma tool call de `date` na Etapa 0, antes de qualquer outra ação.

O preflight (Nível 1) é o mais crítico porque é onde o custo de falha
é mais alto: o usuário vê o agente ignorando o que acabou de "ler"
(está no prompt, mas o executor nunca verificou).

### Proposta formal para o upstream

A proposta completa (RFC-001) está em `context-bridge` skill:
`references/rfc-001-context-preflight.md`. Ela documenta:
- A falha concreta (session_search para um fato em memory)
- A causa raiz (gradiente de ação > texto declarativo)
- A solução em 3 fases (preflight → auto-injection → vector store)
- Pesquisa de suporte (Lin et al. 2026, self-anchored drift)

### Referência externa

Paper: **Lin et al. (2026)** "Same Evidence, Different Answers:
Canonical-Context On-Policy Distillation for Multi-Turn Language
Models" — arXiv:2605.30251v1.

O paper demonstra que o problema de *self-anchored drift* (respostas
parciais virarem âncoras que distorcem respostas futuras) é uma
limitação estrutural dos LLMs em interações multi-turn. Os autores
resolvem via treino (CCOPD distillation). O RFC-001 propõe resolver
via inferência (preflight no system prompt + injeção no agent loop).
São abordagens complementares.

---

## Escopo: Djair vs Universal

**ESTE SKILL opera sobre o setup específico do Djair** — career_tracker (28 capacidades, 46 entregas, 22 solved_problems), agent_capabilities, identity_faults, identity_milestones.

O **meta-skill em desenvolvimento** (Djair + Hermes, 30/05/2026) é um processo GENERATIVO para QUALQUER USUÁRIO: não replica o setup do Djair, mas pergunta "qual seu trabalho?" e constrói as estruturas que fazem sentido para aquele usuário.

Para um usuário escritor (ex: esposa do Djair), career_tracker não faz sentido. Ela precisaria de estruturas como: personagens com árvore genealógica, submissões para editoras, diário de escrita com métricas, referências literárias. Cada usuário gera seu próprio conjunto de tabelas.

**Este skill documenta como a identidade é CONSTRUÍDA a partir de estruturas relacionais.** O career_tracker é UMA implementação (para engenheiro de firmware + polímata). O meta-skill precisa:

1. **Camada universal** (sempre igual): identity_faults do agente, startup-protocol, identidade do usuário como perfil (não career_tracker)
2. **Camada específica** (descoberta na entrevista): as tabelas que fazem sentido para o trabalho DAQUELE usuário — geradas pelo meta-skill

## Estrutura Lida (Setup Djair)

```
pgvector local (fonte da verdade)          ─→  Contexto da sessão
───────────────────────────────────             ──────────────────────
agent_identity.identity_faults            ─→  PERSONALIDADE (regras derivadas)
agent_identity.agent_capabilities         ─→  Extensões do EU
agent_identity.session_checkpoints        ─→  Intent + discovery da sessão
agent_identity.tech_knowledge_base        ─→  Conhecimento técnico (via identity_db.py tech_kb)
career_tracker.* via Supabase             ─→  USER.md (perfil do usuário Djair)

**Tech_kb migrou para pgvector local em 04/06/2026.** MCP tech-kb removido.
Fonte única: `identity_db.py query_tech_kb()`.
```

## ✅ CICLO DA IDENTIDADE RESOLVIDO — SOUL.md como veículo de injeção (31/05/2026)

### Arquitetura: 3 Tiers do System Prompt

O Hermes `build_system_prompt_parts()` em `system_prompt.py` monta o system prompt
em três tiers carregados automaticamente, nesta ordem:

```
   TIER        CONTEÚDO                                   CARREGADO POR
───────────────────────────────────────────────────────────────────────────────
  stable      SOUL.md, skills index, tool guidance        Automático (sempre)
  context     AGENTS.md, .cursorrules                     Automático (sempre)
  volatile    memory, user profile, timestamp             Automático (sempre)
───────────────────────────────────────────────────────────────────────────────
  [fora]      identity_faults, capabilities, milestones   Só se skill_view()
```

O problema original: identity_faults (com countermeasures severity >= 4) estava
FORA dos três tiers — acessível apenas via skill_view() que o agente nunca
chama porque a tarefa do usuário nunca parece "relacionada à identidade".

### Solução Confirmada: SOUL.md no stable tier

**O SOUL.md (~/.hermes/SOUL.md) é carregado no stable tier — antes de qualquer
mensagem do usuário.** Colocar os countermeasures lá faz com que o agente os
leia como regras de comportamento ANTES de processar a primeira interação.

Ciclo completo (31/05/2026 — testado na prática):

```
REGISTRAR              →  identity_faults (pgvector local)
                         identity_self_audit skill detecta e registra

INJETAR                →  SOUL.md no ~/.hermes/SOUL.md
                         (stable tier, carregado automaticamente)
                         Contém: countermeasures severity >= 4
                                 protocolos operacionais
                                 regras de comportamento

COMPORTAR              →  Agente lê SOUL.md antes de qualquer mensagem
                          do usuário → regras viram comportamento
                          Verificação: session_search antes de agir,
                          NÃO fechar prematuramente, NÃO personificar
```

**Estado atual (Junho 2026):**
- SOUL.md escrito com 7 contramedidas ativas (severity >= 4)
- Wrapper com 4 skills carregadas (startup-protocol, context-bridge,
  self-audit, identity-cqrs)
- Meta-skill Stage 5 (agent-calibration) precisa documentar a geração
  de SOUL.md com countermeasures dinâmicos — pendente no repo
  hermes-agent-onboarding e no PR #337 do OB1

### Fluxo de Manutenção do SOUL.md

Quando novos identity_faults são registrados com severity >= 4:

1. O agente detecta durante o auto-check (início da sessão)
2. Atualiza SOUL.md com o novo countermeasure
3. Na PRÓXIMA sessão, o novo countermeasure está no stable tier
4. O COMPORTAR reflete a correção

**⚠️ Falha detectada em 31/05/2026 — SOUL.md não foi atualizado automaticamente.**

Nesta sessão, o agente registrou `context_recovery_failure` (severity 4) na tabela
identity_faults, mas NÃO atualizou o SOUL.md local. Quando o erro de schema_guessing
ocorreu momentos depois, não havia contramedida no stable tier para prevenir.
O SOUL.md precisou ser editado manualmente, com intervenção do usuário, para
incluir a nova contramedida.

**⚠️ Refinamento 03/06/2026 — SOUL.md não é log de faults.**

O usuário corrigiu: SOUL.md não deve ser povoado com cada falha individual.
Countermeasures em SOUL.md devem ser **concisos** (3 linhas ou menos) e
**estruturais** — regras de comportamento que moldam como o agente age, não
o relato de cada erro cometido. Falhas individuais (incluindo PGRST301
recorrente) vão exclusivamente para `identity_faults` no pgvector local.

**Regra prática para SOUL.md vs identity_faults:**
- É um padrão de comportamento que precisa estar ativo a cada sessão?
  → SOUL.md (conciso, 3 linhas max)
- É o relato de um erro específico com causa raiz e evidência?
  → identity_faults (pgvector local)
- Ambos? Curto em SOUL.md, detalhado em identity_faults, com referência
  cruzada via texto breve.

**Correção do protocolo:**

Quando um identity_fault com severity >= 4 for registrado em tempo real
(durante a sessão, não no startup scan), o agente DEVE imediatamente:

1. Registrar o fault no pgvector local (via identity_db.py, ~/.hermes/scripts/identity_db.py insert_fault)
2. Adicionar a contramedida ao SOUL.md físico (`~/.hermes/SOUL.md`)
3. A partir desse momento, a contramedida já está ativa — não precisa esperar
   a próxima sessão porque o SOUL.md é re-lido em cada turno

**Sintoma de quebra do ciclo:** o agente registra o fault, mas comete o mesmo
erro de novo na mesma sessão. Isso indica que (a) o SOUL.md não foi atualizado,
ou (b) o countermeasure no SOUL.md não é específico o bastante para o contexto.

**Teste:** se você cometer um fault que acabou de registrar, o SOUL.md não foi
atualizado. Pare, atualize o SOUL.md com a contramedida do novo fault, e
continue.

### Verificação de Injeção

**TESTE:** Se você NÃO comete faults que estão registrados com severity 5,
a injeção funcionou. Se comete, o SOUL.md não está sendo carregado ou o
countermeasure não está lá.

**Sintoma de sucesso:** o agente faz session_search antes de tarefas que
já foram feitas, não tenta ferramenta errada 4x, não fecha sessão sem pedido.

### Meta-skill: Onde o SOUL.md entra

O meta-skill hermes-agent-onboarding tem Stage 5 (Agent Calibration),
sub-etapa 5A (Per-User SOUL.md). A documentação atual do SKILL.md diz:
> "The SOUL.md is generated as part of the agent's context and does not
> need a physical file"

Isto está ERRADO. O SOUL.md PRECISA ser um arquivo físico (~/.hermes/SOUL.md)
porque o Hermes carrega arquivos físicos no stable tier. O identity-cqrs
startup scan é COMPLEMENTAR — adiciona contexto dinâmico, mas não substitui
o SOUL.md como veículo de regras pré-carregadas.

## Startup Scan — Consultas Relacionais Obrigatórias

### 1. identity_faults → PERSONALIDADE ativa

Via `~/.hermes/scripts/identity_db.py`:
```
source ~/.hermes/hermes-agent/venv/bin/activate && \
python3 ~/.hermes/scripts/identity_db.py faults
```

### 2. agent_capabilities → Extensões do EU

```
source ~/.hermes/hermes-agent/venv/bin/activate && \
python3 ~/.hermes/scripts/identity_db.py capabilities
```

### 3. career_tracker.capabilities → USER.md (quem é o usuário)

```sql
-- Ainda consulta Supabase (career_tracker não migrou)
SELECT name, domain, proficiency, first_used_year, why_it_matters
FROM capabilities
ORDER BY domain, proficiency DESC
LIMIT 50;
```

## Composição do Contexto

Após consultar, COMPOR os seguintes blocos **antes de qualquer ação do usuário**:

```markdown
## PERSONALIDADE (derivada de identity_faults)
- <cada countermeasure de severity >= 4 como regra ativa>
- <NÃO é log — cada linha vira regra de comportamento obrigatória>

## USER.md (perfil do usuário)
- Capacidades principais por domínio
- Marcos recentes da trajetória
```

## O que a camada NÃO faz

- Não modifica o SOUL.md (ele permanece estático, escrito pelo usuário)
- Não substitui a memory tool (append linear continua)
- Não exige novas Edge Functions (opera sobre tabelas existentes)
- Não é um novo sistema de memória — é um tradutor de dados relacionais
  para contexto injetável

## O que a camada FAZ

- Conecta o que o Hermes já sabe (linear) com o que ele PRECISA saber
  (relacional)
- Torna cada falha registrada em uma correção de comportamento imediata
- Torna cada capacidade registrada em uma extensão do que o Hermes pode
  usar para servir o usuário
- Preenche o gap para que DJAIR não precise manualmente pedir: a consulta
  é automática no startup scan

## Integração com supabase-startup-protocol (v2.3.0+)

A Etapa 2B do startup protocol chama identity_faults scan. A Etapa 2C
(pausa executiva) obriga o ciclo PCRA antes de qualquer resposta reflexiva.
Esta skill deve ser carregada APÓS supabase-startup-protocol e
context-bridge.

## Ciclo Relacional

```
PGVECTOR SCAN (startup)
  ├── tech_kb via Supabase (fora do escopo)
  ├── agent_identity.identity_faults   → PERSONALIDADE (local)
  ├── career_tracker.* (Supabase)      → USER.md
  └── agent_identity.agent_capabilities → extensões EU (local)
          ↓
PAUSA EXECUTIVA (PCRA)
  ├── Pausar
  ├── Consultar (já feito acima)
  ├── Refletir: a resposta tem base nos rastros?
  └── Agir
          ↓
TRABALHO + AUTO-REGISTRO (identity-self-audit)
  ├── detectar falhas em tempo real
  ├── registrar em identity_faults
  └── se novo padrão: criar agent_capability
          ↓
CHECKPOINT (supabase-checkpoint-save)
  └── todo progresso salvo
```

## Pitfalls

1. Não confundir USER.md (o que o agente sabe sobre o usuário) com
   PERSONALIDADE (como o agente se comporta). São blocos diferentes.
2. A camada NÃO resolve a falta de intencionalidade do agente — só
   fornece estrutura para que o PCRA funcione melhor.
3. career_tracker pode ter dados incompletos (dashboard bugado). Usar
   SELECT direto nas tabelas com `supabase db query --linked`.
4. identity_faults sem countermeasure é log, não identidade. Só injetar
   no contexto quando houver countermeasure.

## Referências

- `supabase-startup-protocol` — scan obrigatório onde esta skill se insere
- `context-bridge` — conexão multi-fonte (complementar)
- `identity-self-audit` — auto-registro de falhas (complementar)
- `stage-5-agent-calibration` — geração de SOUL.md com countermeasures
- tech_kb `fb50bcf0` — Uber artigo agent identity
- tech_kb `9b327636` — Rascunho 4 camadas identidade

## Nota de descoberta (01/06/2026)

O Nível 0 de confiabilidade (ancoragem temporal) foi uma descoberta empírica:
o usuário mencionou "ontem" e o agente inferiu a data errada (2 de junho, quando
era 1 de junho). A causa raiz é que o timestamp no system prompt, embora
injetado, é texto declarativo que compete com descrições vívidas de ferramentas
e perde (gradiente de ação). A correção não pode ser textual — precisa ser
uma tool call explícita de `date` como Etapa 0.

Ver também: `identity-self-audit` — fault_type `temporal_drift`, severity 4.
