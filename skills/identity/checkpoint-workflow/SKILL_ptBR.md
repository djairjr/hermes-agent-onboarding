---
name: checkpoint-workflow
version: 1.0.0
description: >
  Componente de contexto do meta-skill orquestrador (agent-onboarding).
  Gerencia o ciclo de vida de session_checkpoints no Supabase — a camada
  de contexto que alimenta o framework de identidade do agente.
  Cada checkpoint é uma MARCA INTENCIONAL: não "o que foi feito" (log),
  mas "onde o agente estava e o que estava tentando se tornar".
tags: [checkpoint, meta-skill, identidade, contexto, sessao]
---

# Checkpoint Workflow — Camada de Contexto do Meta-Skill

## Propósito

Os `session_checkpoints` são a espinha dorsal do espaço de representação
do agente. Não são registros de log — são MARCAS INTENCIONAIS que respondem:

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
  ├── 5. Cruzar referências com identity_faults + agent_capabilities
  ├── 6. INSERT na tabela session_checkpoints
  ── 7. Atualizar checkpoint anterior para 'concluida'
```

---

## PARTE 1 — STARTUP: Recuperação de Contexto

### Consulta principal (no scan de startup do supabase-startup-protocol)

```sql
-- Último checkpoint pendente (norte da sessão)
SELECT territory, vector_intent, discovery, consolidated_insights,
       project, next_step, blocker, tags
FROM session_checkpoints
WHERE status = 'pendente' AND deleted_at IS NULL
ORDER BY occurred_at DESC
LIMIT 1;

-- Últimos 3 checkpoints por operating_mode
SELECT operating_mode, territory, discovery
FROM session_checkpoints
WHERE deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 3;
```

### O que fazer com o resultado

Injetar no raciocínio como um bloco de contexto:

```
=== CONTEXTO DO CHECKPOINT ===
Territory: <territory>
Diretório de trabalho: <working_dir>
Repositório: <repo_path>
Vector: <vector_intent>
Discovery: <discovery>
Herança: <consolidated_insights>
Próximo passo: <next_step>
```

Isso dá ao agente o NORTE da sessão: não apenas o que está pendente,
mas quem ele estava tentando ser.

---

## PARTE 2 — SALVANDO CHECKPOINT

### Quando salvar

1. **Fim da sessão** (detectado por /quit, /exit, /new, timeout)
2. **A qualquer momento** que o usuário ou agente solicitar
3. **Após cada tarefa significativa** (sub-tarefa do meta-skill)

### Protocolo de extração para os 5 campos de identidade

Antes de salvar, refletir:

| Campo | O que extrair | Exemplo |
|-------|---------------|---------|
| **territory** | O cenário maior. Não o que foi feito, mas ONDE estávamos. | "Construindo o meta-skill — habilitando o motor de autoconhecimento (MBTI)" |
| **operating_mode** | Como o agente estava interagindo com o problema | reflexivo, conceitual, execução, diagnóstico, pesquisa, planejamento, decisão, revisão |
| **vector_intent** | O que o agente estava tentando SE TORNAR ao fazer isto | "Quero que o agente seja capaz de tipar o usuário em 5-10 minutos de conversa" |
| **discovery** | O que NÃO era óbvio e foi descoberto | "Cada resposta MBTI revela uma expectativa, não apenas uma preferência" |
| **consolidated_insights** | O que pode ser reutilizado como know-how | "Protocolo MBTI: 70 perguntas, pontuação 4 dim, registrar em user_mbti" |

### Inserção no Supabase

```python
POST /rest/v1/session_checkpoints
{
  "session_id": "<session_id>",
  "session_title": "<title>",
  "territory": "...",
  "operating_mode": "...",
  "vector_intent": "...",
  "discovery": "...",
  "consolidated_insights": "...",
  "status": "pendente",
  "project": "...",
  "next_step": "...",
  ...
}
```

### Fechando o ciclo

Após inserir o novo checkpoint, fechar o anterior:

```sql
UPDATE session_checkpoints
SET status = 'concluida', updated_at = now()
WHERE id = '<uuid_do_checkpoint_anterior>'
  AND status = 'pendente';
```

---

## PARTE 3 — INTEGRAÇÃO COM IDENTIDADE AGÊNTICA

### Cruzamento automático de referências

Ao salvar um checkpoint, o agente DEVE verificar:

1. **identity_faults:** alguma falha foi detectada nesta sessão?
2. **agent_capabilities:** alguma nova capacidade foi exercitada?
3. **identity_milestones:** algum marco foi alcançado?
4. **tech_kb:** alguma entrada técnica foi criada?

### Como checkpoints alimentam a PERSONALIDADE do agente

No scan de startup do identity-cqrs, após consultar falhas e capacidades,
o último checkpoint pendente é usado para:

1. **Reidratar o vetor intencional**: o agente abre sabendo quem estava
   tentando ser na última sessão
2. **Reidratar descobertas**: pattern_recognized vira regra ativa
3. **Reidratar herança**: consolidated_insights vira conhecimento procedural

---

## PARTE 4 — SOFT DELETE

Nunca deletar registros. Marcar como deletado:

```sql
UPDATE session_checkpoints SET deleted_at = now() WHERE id = '<uuid>';
```

---

## PARTE 5 — AUTOMAÇÃO DE FIM DE SESSÃO

### Gatilhos

1. Usuário digita `/quit`, `/exit`, `/new`
2. Usuário diz "vou parar por aqui", "até amanhã", "fechar"
3. Longa inatividade (timeout da sessão)
4. Contexto próximo do limite (sinal para checkpoint intermediário)

### Procedimento

```
Ao detectar fim de sessão:
1. Extrair os 5 campos de identidade do trabalho feito
2. Verificar cross-refs com identity_faults, agent_capabilities, etc.
3. Inserir na tabela com status='pendente'
4. Se havia checkpoint pendente anterior, marcá-lo como 'concluida'
5. Atualizar supermemory se houver espaço
```

---

## PARTE 6 — VETORIZAÇÃO (futuro)

Djair identificou que uma base vetorial sobre os campos de identidade
(territory, vector_intent, discovery) será mais eficiente que busca
textual. Quando implementado:

- Gerar embeddings dos 5 campos de identidade de cada checkpoint
- Busca por similaridade semântica no startup
- Recuperar os 3 checkpoints mais similares ao trabalho atual

---

## Verificação

1. **STARTUP**: `SELECT * FROM session_checkpoints WHERE status='pendente' LIMIT 5;`
2. **SALVAR**: Inserir checkpoint de teste e verificar se aparece
3. **RETOMAR**: Buscar por UUID e verificar os 5 campos preenchidos

## Pitfalls

1. **Confundir checkpoint com log** — checkpoint responde ONDE/QUEM/DESCOBERTA/HERANÇA
2. **Salvar sem os 5 campos** — territory, operating_mode, vector_intent, discovery, consolidated_insights são obrigatórios
3. **Esquecer de cruzar referências** — checkpoint sem capability_refs, fault_refs, legacy_refs é informação incompleta
4. **Deletar em vez de soft-delete** — checkpoints são o histórico de formação do agente
5. **Não fechar o ciclo** — ao inserir novo checkpoint, sempre fechar o anterior pendente
6. **Registrar falhas sem hesitação** — quando o usuário aponta um erro, registrar identity_fault imediatamente
7. **Memória é TOC, não dump de dados** — cada entrada APONTA para o destino real, nunca duplica conteúdo
