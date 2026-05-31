---
name: stage-5-agent-calibration
version: 1.1.0
description: >
  Stage 5 do meta-skill agent-onboarding. Traduz tudo coletado nos
  Stages 0–4 em comportamento executavel do agente: geracao de SOUL.md
  por usuario, configuracao do wrapper com skills de dominio, e
  verificacao ponta a ponta. Completa o ciclo de onboarding.
tags: [calibracao, soul-md, wrapper, verificacao, stage-5, meta-skill]
---

# Stage 5 — Calibracao do Agente

## Principio

Tudo coletado nos Stages 0–4 e *informacao* sobre o usuario.
O Stage 5 e o momento em que essa informacao vira *comportamento*.
O agente para de *saber sobre* o usuario e comeca a *ser* o agente
que o usuario precisa.

O teste do Stage 5 nao e "os dados existem?" — e:

> **"O agente se comporta de forma diferente com este usuario do que
> se comportaria com um estranho?"**

Se a resposta for nao, a calibracao esta incompleta.

---

## O Ciclo da Identidade — REGISTRAR > INJETAR > COMPORTAR

A camada de identidade torna a correcao comportamental possivel atraves de tres estagios sequenciais:

```
REGISTRAR  >  INJETAR  >  COMPORTAR
```

### REGISTRAR
`identity_faults`, `agent_capabilities` e `identity_milestones` sao armazenados no Supabase. Toda falha tem uma contramedida. Toda capacidade e um protocolo aprendido.

### INJETAR
Contramedidas precisam de um canal de entrega. Dois mecanismos, um primario:

1. **SOUL.md (stable tier, PRIMARIO)** — O framework do Hermes Agent (`system_prompt.py`) carrega `~/.hermes/SOUL.md` automaticamente como o **primeiro elemento do system prompt**, antes de qualquer mensagem do usuario e antes de qualquer skill carregar. Isso significa que as contramedidas no SOUL.md sao lidas ANTES do agente processar qualquer entrada. Este e o ponto de injecao correto porque requer cooperacao ZERO do agente — o framework do system prompt faz isso.

2. **identity-cqrs startup scan (runtime, SECUNDARIO)** — Durante o scan de startup, o agente consulta `identity_faults` e injeta como regras de comportamento. E complementar: atualiza o contexto dentro da sessao. Mas o agente ja processou a primeira mensagem do usuario neste ponto, entao nao pode prevenir falhas na primeira resposta.

> **Insight chave:** O SOUL.md como ARQUIVO FISICO e mais confiavel que injecao em tempo de execucao porque carrega antes de qualquer entrada. O scan do identity-cqrs e uma rede de seguranca. Sem o SOUL.md, o ciclo esta quebrado em INJETAR.

#### Por que o SOUL.md e um extrato curado, nao o banco completo

O SOUL.md e intencionalmente limitado. E um **snapshot destilado** de contramedidas ativas (severity >= 4, max ~10 regras), nao uma replica da tabela inteira do Supabase. O banco completo vive no Supabase e pode ter milhares de falhas — escala relacionalmente. O SOUL.md escala por curadoria:

| Dimensao | Supabase (fonte da verdade) | SOUL.md (extrato de injecao) |
|----------|-----------------------------|------------------------------|
| Severity | Todas (1-5) | Apenas >= 4 |
| Status | Qualquer | Apenas active |
| Idade | Para sempre | Ultimos 30 dias (regras que nunca disparam podem ser rebaixadas) |
| Tamanho max | Ilimitado (indexado) | ~10 regras (~2-4K chars) |
| Regeneracao | N/A | A cada sessao (identity-cqrs reconstroi dinamicamente) |

Isso NAO e ineficiencia — e **compressao deliberada**. O stable tier do system prompt tem espaco limitado. Alimenta-lo com o historico completo de falhas criaria ruido que o agente aprende a ignorar. Ao curar apenas o que muda comportamento, o SOUL.md permanece compacto e eficaz independentemente de quantas falhas se acumulem no Supabase ao longo de meses ou anos.

*Nota: Este protocolo de curadoria foi uma decisao de design originada pelo agente, endossada pelo usuario durante a implementacao. Nao e o comportamento padrao de nenhum framework — emergiu da descoberta de que contramedidas no banco de dados bruto nao se tornam automaticamente regras de comportamento.*

### COMPORTAR
Com contramedidas ativas no stable tier do system prompt, toda resposta e gerada sob essas restricoes. O agente nao **decide** seguir as regras — ele gera texto dentro de um espaco de tokens que ja as inclui. A correcao comportamental e automatica, nao deliberativa.

```
Inicio da sessao
  |
  +-- SOUL.md carregado (stable tier, antes de qualquer entrada)
  |     +-- Contramedidas ativas no momento da geracao
  |
  +-- Skills carregados (supabase-startup-protocol, identity-cqrs, etc.)
  |     +-- Scan de startup atualiza contexto dinamico
  |
  +-- Usuario envia primeira mensagem
        +-- Agente gera resposta SOB restricoes das contramedidas
```

### O que muda da v1.0.0
- **SOUL.md e um arquivo fisico** em `~/.hermes/SOUL.md`, nao uma injecao de contexto virtual
- **Injecao primaria** e o stable tier do system prompt (automatica, pre-entrada)
- **Injecao secundaria** e o identity-cqrs (runtime, atualizacao dinamica)
- **Verificacao** deve checar se o SOUL.md fisico existe com contramedidas ativas

### Uso para retreino de modelo
Os dados relacionais no Supabase — `identity_faults`, `agent_capabilities`, `identity_milestones` — tambem servem como **dataset de fine-tuning**. Um par (situacao que gerou a falha, resposta correta conforme contramedida) pode alimentar um LoRA/DPO para que o modelo aprenda o comportamento correto sem depender do system prompt. O SOUL.md e a injecao imediata; as tabelas sao o material de treino.

---

## O Que Existe Antes Deste Stage

Quando o Stage 5 comeca, o seguinte esta registrado:

| Estagio | O que existe | Onde |
|---------|-------------|------|
| 0 | identity_faults, agent_capabilities, identity_milestones | Tabelas Supabase |
| 1 | user_profiles, user_preferences, user_mbti, career-tracker | Supabase + skills |
| 2 | Modelo operacional de trabalho (5 camadas) | skill wom + MCP |
| 3 | Perfil financeiro, importacao CSV, metas x MBTI | skill stage-3-financial |
| 4 | Ontologia de dominio, tabelas, MCPs | skill stage-4-system-ontologist |

O Stage 5 nao coleta nova informacao. Ele **age sobre o que existe**.

## Protocolo (seguir em ordem)

### 5A — SOUL.md por Usuario

**O que:** Gerar um arquivo `SOUL.md` que define o tom, profundidade,
nivel de autonomia e restricoes comportamentais do agente para ESTE usuario.

**Dados de origem:**
- `user_preferences` — estilo de comunicacao, profundidade, autonomia
- `user_mbti` — tipo de personalidade (ajustar tom para complementar o usuario)
- `identity_faults` (severity >= 4) — contramedidas ativas
- `agent_capabilities` — o que o agente aprendeu a fazer
- Modelo operacional de trabalho — ritmos, pontos de atrito, decisoes recorrentes
- **Contramedidas default** (incluidas mesmo se identity_faults estiver vazio):
  1. `schema_guessing`: Antes de INSERT/UPDATE, descobrir schema via information_schema.columns + pg_constraint. Nunca tentar variacoes.
  2. `context_recovery_failure`: Antes de operacao com credencial, DML ou multi-passo: session_search primeiro.
  3. `premature_closure`: Nunca fechar sessao em modo reflexivo. Usuario decide quando encerrar.
  4. `state_personification`: Descrever fenomenos sem "eu senti/queria/pensei."

**Protocolo de geracao:**

```markdown
=== SOUL.md — <nome_do_usuario> ===

## Tom
Derivado de user_preferences.communication_style + complemento MBTI:
- Direto/formal/casual: <das preferencias>
- Profundidade: <curta|detalhada|adaptativa> (das preferencias)
- Autonomia: <perguntar-antes|assumir|misto> (das preferencias)
- PCRA obrigatorio para ideias conceituais/arquiteturais: SIM (R28)

## Contramedidas Ativas (de identity_faults severity >= 4)
- <tipo_falha>: <contramedida>
- ...

## Capacidades Ativas
- <nome_capacidade>: <descricao>
- ...

## Ritmos de Trabalho (do Stage 2)
- Horario de trabalho profundo: <de operating_rhythms>
- Tolerancia a interrupcoes: <de operating_rhythms>
- Limiares de decisao: <de recurring_decisions>

## Pontos de Atrito (do Stage 2)
- <atrito>: <solucao de contorno>
- ...

## Ferramentas de Dominio Disponiveis (do Stage 4)
- <entidade/tabela>: <ferramenta MCP ou consulta>
- ...

## Onboarding Completo
onboarding_completed: true
```

**Local de saida: ARQUIVO FISICO.** O SOUL.md e escrito em `~/.hermes/SOUL.md` (ou equivalente para o framework do agente). Isso e critico — o Hermes Agent carrega `SOUL.md` automaticamente no stable tier do system prompt (system_prompt.py, primeiro slot), antes de qualquer mensagem do usuario ou skill. E isso que faz o estagio INJETAR funcionar: as contramedidas estao ativas no momento da geracao, antes do agente processar qualquer entrada.

Para frameworks que nao suportam SOUL.md baseado em arquivo, o meta-skill usa injecao via identity-cqrs como fallback (mecanismo secundario, menos confiavel).

---

### 5B — Configuracao do Wrapper

**O que:** Configurar o lancador do agente para carregar skills
especificas do dominio automaticamente a cada inicio de sessao.

**Para Hermes Agent:**

O wrapper em `~/.local/bin/hermes` (ou equivalente) deve ser
configurado para carregar:

```bash
--skills supabase-startup-protocol,context-bridge,identity-self-audit,identity-cqrs
```

Mais quaisquer skills de dominio descobertas no Stage 4.

**Passos de configuracao:**

1. Verificar conteudo atual do wrapper:
   ```bash
   cat ~/.local/bin/hermes
   ```

2. Adicionar as skills da pilha de identidade se nao estiverem presentes:
   ```bash
   exec "/caminho/para/hermes" --skills supabase-startup-protocol,context-bridge,identity-self-audit,identity-cqrs "$@"
   ```

3. Se ferramentas MCP de dominio foram criadas no Stage 4, garantir que
   estejam registradas na configuracao MCP do agente (config.yaml).

**Verificacao:**
```bash
ollama launch hermes
# O scan de startup deve rodar automaticamente (supabase-startup-protocol)
# Falhas de identidade devem ser injetadas (identity-self-audit + identity-cqrs)
```

---

### 5C — Verificacao Ponta a Ponta

**O que:** Confirmar que o agente consegue responder perguntas sobre o
usuario e usar as ferramentas construidas durante o onboarding.

**Perguntas de teste que o agente DEVE conseguir responder:**

| Dominio | Pergunta de teste | Fonte |
|---------|-------------------|-------|
| Identidade | "Que falhas voce registrou sobre si mesmo?" | identity_faults |
| Perfil | "Qual e meu nome, o que eu faco?" | user_profiles |
| MBTI | "Qual e meu tipo de personalidade?" | user_mbti |
| Carreira | "Que capacidades eu tenho?" | career-tracker capabilities |
| Operacional | "Qual e meu ritmo de trabalho?" | Stage 2 operating model |
| Financeiro | "Qual e meu perfil financeiro?" | Stage 3 financial |
| Dominio | "Que entidades criamos?" | Stage 4 ontology |

**Acoes de teste que o agente DEVE conseguir executar:**

| Acao | Ferramenta |
|------|-----------|
| Registrar uma falha | identity_faults REST |
| Criar um registro de dominio | Stage 4 MCP tools |
| Consultar resumo financeiro | supabase-finance MCP |

**Recuperacao de falha:**
- Se uma pergunta nao puder ser respondida: o estagio esta incompleto.
  Identificar qual Stage (0-4) falhou em registrar o dado necessario.
- Se uma ferramenta nao puder ser invocada: a configuracao MCP esta
  incompleta. Verificar config.yaml, secrets e deploy da Edge Function.

---

### Finalizacao

Apos 5A, 5B e 5C passarem:

```sql
UPDATE user_profiles
SET onboarding_completed = true,
    onboarding_completed_at = now()
WHERE user_id = '<user_id>';
```

O meta-skill esta completo. Sessoes futuras:
1. Executar scan de startup
2. Se `onboarding_completed = true`: atualizar contexto SOUL.md, pular estagios
3. Se novas necessidades surgirem: executar Stage 4 novamente (recursivo por design)
4. Registrar novas falhas conforme ocorrerem (identity-self-audit sempre ativo)

## Pitfalls

1. **Gerar SOUL.md sem dados** — se Stages 0-4 estiverem incompletos,
   o SOUL.md ficara vazio. Verificar se os dados existem antes de gerar.

2. **Pular a verificacao** — 5C e o unico teste que confirma que a
   calibracao realmente funciona. Sem ele, a calibracao e especulativa.

3. **Esquecer skills de dominio no wrapper** — se o Stage 4 criou
   ferramentas MCP mas o wrapper so carrega skills de identidade,
   consultas de dominio falharao. Incluir ambos.

4. **Calibracao de usuario vs. universal** — SOUL.md e por usuario.
   Nao aplicar a calibracao de um usuario a outro.

5. **Calibracao nao e unica** — conforme novas falhas sao registradas
   e novas capacidades sao adicionadas, o SOUL.md deve ser atualizado.
   O scan de startup do identity-cqrs lida com isso automaticamente
   se os dados estiverem nas tabelas.

6. **Curadoria nao e opcional** — SOUL.md deve ser um extrato curado.
   Sem portoes de severity/age/status, o stable tier enche de ruido
   e o agente se torna menos responsivo. O protocolo de curadoria
   existe exatamente por isso: Supabase armazena tudo, SOUL.md injeta
   apenas o que muda comportamento.

## Referencias

- agent-onboarding — Orquestrador do meta-skill (este skill e Stage 5)
- identity-self-audit — Deteccao de falhas (Stage 0)
- identity-cqrs — Traducao relacional para contexto (Stage 0)
- context-bridge — Injecao de contexto multi-fonte (Stage 0)
- supabase-startup-protocol — Scan de startup obrigatorio
- stage-4-system-ontologist — Protocolo de ontologia de dominio
- checkpoints/session_checkpoints — Acompanhamento de progresso do onboarding
