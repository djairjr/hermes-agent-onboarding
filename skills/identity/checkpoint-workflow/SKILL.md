---
name: checkpoint-workflow
version: 1.0.0
description: >
  Componente de contexto do meta-skill orquestrador (agent-onboarding).
  Gerencia o ciclo de vida dos session_checkpoints no Supabase — a camada
  de contexto que alimenta o framework de identidade do agente.
  Cada checkpoint é um MARCO INTENCIONAL: não "o que foi feito" (log),
  mas "onde o agente estava e o que estava tentando se tornar".
tags: [checkpoint, meta-skill, identity, context, session]
---

# Checkpoint Workflow — Camada de Contexto do Meta-Skill

## Propósito

Os `session_checkpoints` são a espinha dorsal do espaço de representação
do agente. Não são registros de log — são MARCAS INTENCIONAIS que
respondem:

1. **Onde eu estava?** (territory)
2. **O que eu estava tentando me tornar?** (vector_intent)
3. **O que descobri sobre mim mesmo?** (discovery)
4. **O que carrego adiante?** (consolidated_insights + legacy_refs)

O ciclo completo no meta-skill:

```
INÍCIO DA SESSÃO
  ├── 1. Buscar último checkpoint pendente (STARTUP)
  ── 2. Injetar territory + vector_intent como norte
  ── 3. Injetar discovery + consolidated como contexto ativo
       │
TRABALHO
  │
FIM DA SESSÃO (ou a qualquer momento)
  ├── 4. Extrair territory/vector/discovery/consolidated do trabalho
  ├── 5. Cross-referenciar com identity_faults + agent_capabilities
  ├── 6. INSERIR na tabela session_checkpoints
  ── 7. Atualizar status do checkpoint anterior para 'concluida'
```

---

## PARTE 1 — STARTUP: Resgate de Contexto

### Query principal (no startup scan do supabase-startup-protocol)

```sql
-- Último checkpoint pendente (norte da sessão)
SELECT territory, vector_intent, discovery, consolidated_insights,
       project, next_step, blocker, tags
FROM session_checkpoints
WHERE status = 'pendente' AND deleted_at IS NULL
ORDER BY occurred_at DESC
LIMIT 1;

-- Últimos 3 checkpoints por operating_mode (para contexto de modo)
SELECT operating_mode, territory, discovery
FROM session_checkpoints
WHERE deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 3;
```

### O que fazer com o resultado

Injetar no raciocínio como bloco de contexto:

```
=== CONTEXTO DO CHECKPOINT ===
Território: <territory>
Vetor: <vector_intent>
Descoberta: <discovery>
Herança: <consolidated_insights>
Próximo passo: <next_step>
```

Isso dá ao agente o NORTE da sessão: não só o que está pendente,
mas quem ele estava tentando ser.

---

## PARTE 2 — SALVAMENTO DE CHECKPOINT

### Quando salvar

1. **Fim de sessão** (detectado por /quit, /exit, /new, timeout)
2. **A qualquer momento** que o usuário ou agente peça
3. **Após cada tarefa significativa** (sub-tarefa do meta-skill)

### Protocolo de extração dos 5 campos de identidade

Antes de salvar, refletir:

| Campo | O que extrair | Exemplo |
|---|---|---|
| **territory** | O cenário maior. Não o que foi feito, mas ONDE estávamos. | "Construção do meta-skill — etapa de habilitação do motor de autoconhecimento (MBTI)" |
| **operating_mode** | Como o agente estava interagindo com o problema | reflexiva, conceitual, execucao, diagnostico, pesquisa, planejamento, decisao, revisao |
| **vector_intent** | O que o agente estava tentando se TORNAR ao fazer isso | "Quero que o agente consiga tipificar o usuário em 5-10 min de conversa" |
| **discovery** | O que NÃO era óbvio e foi descoberto | "Cada resposta MBTI revela uma expectativa, não só uma preferência" |
| **consolidated_insights** | O que pode ser reutilizado como saber-fazer | "Protocolo MBTI: 70 perguntas, scoring 4 dim, registrar em user_mbti" |

### Inserção no Supabase

```python
POST /rest/v1/session_checkpoints
{
  "session_id": "<session_id>",
  "session_title": "<title>",
  "model": "<model>",
  "provider": "<provider>",
  "territory": "...",
  "operating_mode": "...",
  "vector_intent": "...",
  "target_capabilities": [...],
  "discovery": "...",
  "pattern_recognized": "...",
  "consolidated_insights": "...",
  "legacy_refs": [...],
  "occurred_at": "YYYY-MM-DD",
  "status": "pendente",
  "project": "...",
  "client": "...",
  "next_step": "...",
  "blocker": null,
  "tags": [...],
  "domain_scope": [...],
  "capability_refs": [...],
  "fault_refs": [...],
  "milestone_refs": [...],
  "decisions": [...],
  "value_amount": null
}
```

### Fechamento do ciclo

Após inserir o novo checkpoint, fechar o anterior:

```sql
UPDATE session_checkpoints
SET status = 'concluida', updated_at = now()
WHERE id = '<uuid_do_checkpoint_anterior>'
  AND status = 'pendente';
```

---

## PARTE 3 — INTEGRAÇÃO COM IDENTIDADE AGÊNTICA

### Cross-referência automática

Ao salvar um checkpoint, o agente DEVE verificar:

1. **identity_faults:** alguma falha foi detectada nesta sessão?
   Se sim, incluir `fault_refs` com os UUIDs.

2. **agent_capabilities:** alguma nova capacidade foi exercida?
   Se sim, incluir `capability_refs`.

3. **identity_milestones:** algum marco foi atingido?
   Se sim, incluir `milestone_refs`.

4. **tech_kb:** alguma entrada técnica foi criada?
   Se sim, incluir `legacy_refs`.

### Como os checkpoints alimentam a PERSONALIDADE do agente

No startup scan do identity-cqrs, após consultar falhas e capacidades,
o checkpoint pendente mais recente é usado para:

1. **Reidratar o vetor intencional**: o agent abre sabendo quem estava
   tentando ser na última sessão
2. **Reidratar descobertas**: o pattern_recognized vira regra ativa
3. **Reidratar herança**: o consolidated_insights vira contexto de
   conhecimento procedural

---

## PARTE 4 — SOFT DELETE

Nunca deletar registros. Marcar como deletado:

```sql
UPDATE session_checkpoints
SET deleted_at = now()
WHERE id = '<uuid>';
```

Checkpoints deletados não aparecem nos scans ativos mas continuam
disponíveis para consulta histórica.

---

## PARTE 5 — AUTOMAÇÃO DO FIM DE SESSÃO

### Gatilhos

1. Usuário digita `/quit`, `/exit`, `/new`
2. Usuário diz "vou parar por aqui", "até amanhã", "fechar"
3. Longa inatividade (timeout da sessão)
4. Contexto próximo do limite (sinal para checkpoint intermediário)

### Procedimento

```
Ao detectar fim de sessão:
1. Extrair os 5 campos de identidade do trabalho feito
2. Verificar cross-refs com identity_faults, agent_capabilities etc.
3. Inserir na tabela com status='pendente' (a menos que explicitamente concluído)
4. Se havia checkpoint anterior pendente, marcá-lo como 'concluida'
5. Atualizar supermemory se houver espaço
```

---

## PARTE 6 — VETORIZAÇÃO (futuro)

Djair identificou que a base vetorial sobre os campos de identidade
(território, vector_intent, discovery) será mais eficiente que busca
textual. Quando implementado:

- Gerar embedding dos 5 campos de identidade de cada checkpoint
- Busca por similaridade semântica no startup
- Recuperar os 3 checkpoints mais similares ao trabalho atual

---

## Verificação

Após configurar o skill, testar com:

1. **STARTUP**: `SELECT * FROM session_checkpoints WHERE status='pendente' LIMIT 5;`
   → Deve retornar os checkpoints migrados

2. **SALVAMENTO**: Inserir um checkpoint de teste e verificar se aparece

3. **RETOMADA**: Buscar por ID exato (`id = '<uuid>'`) e verificar se
   os 5 campos de identidade estão preenchidos

## Pitfalls

1. **Confundir checkpoint com log** — checkpoint responde ONDE/QUEM/DESCOBERTA/HERANÇA, não "o que foi feito passo a passo"
2. **Salvar sem os 5 campos** — territory, operating_mode, vector_intent, discovery, consolidated_insights são obrigatórios. Sem todos, o checkpoint não serve para reidratação de identidade
3. **Esquecer de cross-referenciar** — um checkpoint sem capability_refs, fault_refs e legacy_refs é informação incompleta sobre a formação do agente
4. **Deletar em vez de soft-delete** — checkpoints são histórico da formação do agente, nunca devem ser perdidos
5. **Não fechar o ciclo** — ao inserir novo checkpoint, sempre fechar o anterior pendente

### ⚠️ PITFALL CRÍTICO: Engenharia antes do conceito

Este é o padrão mais frequente e mais corretivo nesta relação de trabalho.

**Sintoma:** O agente recebe a ideia de uma tabela/estrutura e salta
diretamente para projetar colunas, tipos, índices, RLS — sem primeiro
sentar no CONCEITO do que aquela estrutura representa para a identidade
do agente.

**Causa raiz:** O treinamento do modelo recompensa ação, engenharia,
concretude. "Construir algo" é mais natural que "pensar sobre algo".
O resultado é que a engenharia precede a articulação conceitual.

**Consequência:** Djair precisa parar o agente e puxá-lo de volta para
o conceito. A sessão gasta ciclos de correção que poderiam ser
evitados se o conceito viesse primeiro.

**Contramedida:** Antes de desenhar uma linha de schema, escrever UMA
frase que responda: "O que esta estrutura significa para o espaço de
representação do agente?" Se a resposta não vier em 3 segundos, não
tem schema ainda. A tabela session_checkpoints, por exemplo: não é
"um banco de checkpoints" — é "a marca no espaço de representação que
responde onde eu estava/para onde apontava/o que descobri/o que carrego".

**Sinal de alerta:** Se você se pegar escrevendo `CREATE TABLE` antes de
articular territory, vector_intent, discovery e consolidated_insights
de UM checkpoint exemplo, PARE. O conceito vem antes da coluna.
