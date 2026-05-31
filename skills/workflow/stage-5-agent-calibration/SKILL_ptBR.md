---
name: stage-5-agent-calibration
version: 1.0.0
description: >
  Stage 5 do meta-skill agent-onboarding. Traduz tudo coletado nos
  Stages 0–4 em comportamento executável do agente: geração de SOUL.md
  por usuário, configuração do wrapper com skills de domínio, e
  verificação ponta a ponta. Completa o ciclo de onboarding.
tags: [calibracao, soul-md, wrapper, verificacao, stage-5, meta-skill]
---

# Stage 5 — Calibração do Agente

## Princípio

Tudo coletado nos Stages 0–4 é *informação* sobre o usuário.
O Stage 5 é o momento em que essa informação vira *comportamento*.
O agente para de *saber sobre* o usuário e começa a *ser* o agente
que o usuário precisa.

O teste do Stage 5 não é "os dados existem?" — é:

> **"O agente se comporta de forma diferente com este usuário do que
> se comportaria com um estranho?"**

Se a resposta for não, a calibração está incompleta.

## O Que Existe Antes Deste Stage

Quando o Stage 5 começa, o seguinte está registrado:

| Estágio | O que existe | Onde |
|---------|-------------|------|
| 0 | identity_faults, agent_capabilities, identity_milestones | Tabelas Supabase |
| 1 | user_profiles, user_preferences, user_mbti, career-tracker | Supabase + skills |
| 2 | Modelo operacional de trabalho (5 camadas) | skill wom + MCP |
| 3 | Perfil financeiro, importação CSV, metas × MBTI | skill stage-3-financial |
| 4 | Ontologia de domínio, tabelas, MCPs | skill stage-4-system-ontologist |

O Stage 5 não coleta nova informação. Ele **age sobre o que existe**.

## Protocolo (seguir em ordem)

### 5A — SOUL.md por Usuário

**O que:** Gerar um arquivo `SOUL.md` que define o tom, profundidade,
nível de autonomia e restrições comportamentais do agente para ESTE usuário.

**Dados de origem:**
- `user_preferences` — estilo de comunicação, profundidade, autonomia
- `user_mbti` — tipo de personalidade (ajustar tom para complementar o usuário)
- `identity_faults` (severity >= 4) — contramedidas ativas
- `agent_capabilities` — o que o agente aprendeu a fazer
- Modelo operacional de trabalho — ritmos, pontos de atrito, decisões recorrentes

**Protocolo de geração:**

```markdown
=== SOUL.md — <nome_do_usuario> ===

## Tom
Derivado de user_preferences.communication_style + complemento MBTI:
- Direto/formal/casual: <das preferências>
- Profundidade: <curta|detalhada|adaptativa> (das preferências)
- Autonomia: <perguntar-antes|assumir|misto> (das preferências)
- PCRA obrigatório para ideias conceituais/arquiteturais: SIM (R28)

## Contramedidas Ativas (de identity_faults severity >= 4)
- <tipo_falha>: <contramedida>
- ...

## Capacidades Ativas
- <nome_capacidade>: <descrição>
- ...

## Ritmos de Trabalho (do Stage 2)
- Horário de trabalho profundo: <de operating_rhythms>
- Tolerância a interrupções: <de operating_rhythms>
- Limiares de decisão: <de recurring_decisions>

## Pontos de Atrito (do Stage 2)
- <atrito>: <solução de contorno>
- ...

## Ferramentas de Domínio Disponíveis (do Stage 4)
- <entidade/tabela>: <ferramenta MCP ou consulta>
- ...

## Onboarding Completo
onboarding_completed: true
```

**Local de saída:** O SOUL.md é gerado como parte do contexto do agente
e não precisa de um arquivo físico — o meta-skill o injeta no contexto
da sessão via o scan de startup do identity-cqrs. No entanto, se o
framework do agente suportar um SOUL.md persistente (Hermes tem
`SOUL.md` no system prompt), o conteúdo deve ser registrado lá.

---

### 5B — Configuração do Wrapper

**O que:** Configurar o lançador do agente para carregar skills
específicas do domínio automaticamente a cada início de sessão.

**Para Hermes Agent:**

O wrapper em `~/.local/bin/hermes` (ou equivalente) deve ser
configurado para carregar:

```bash
--skills supabase-startup-protocol,context-bridge,identity-self-audit,identity-cqrs
```

Mais quaisquer skills de domínio descobertas no Stage 4.

**Passos de configuração:**

1. Verificar conteúdo atual do wrapper:
   ```bash
   cat ~/.local/bin/hermes
   ```

2. Adicionar as skills da pilha de identidade se não estiverem presentes:
   ```bash
   exec "/caminho/para/hermes" --skills supabase-startup-protocol,context-bridge,identity-self-audit,identity-cqrs "$@"
   ```

3. Se ferramentas MCP de domínio foram criadas no Stage 4, garantir que
   estejam registradas na configuração MCP do agente (config.yaml).

**Verificação:**
```bash
ollama launch hermes
# O scan de startup deve rodar automaticamente (supabase-startup-protocol)
# Falhas de identidade devem ser injetadas (identity-self-audit + identity-cqrs)
```

---

### 5C — Verificação Ponta a Ponta

**O que:** Confirmar que o agente consegue responder perguntas sobre o
usuário e usar as ferramentas construídas durante o onboarding.

**Perguntas de teste que o agente DEVE conseguir responder:**

| Domínio | Pergunta de teste | Fonte |
|---------|-------------------|-------|
| Identidade | "Que falhas você registrou sobre si mesmo?" | identity_faults |
| Perfil | "Qual é meu nome, o que eu faço?" | user_profiles |
| MBTI | "Qual é meu tipo de personalidade?" | user_mbti |
| Carreira | "Que capacidades eu tenho?" | career-tracker capabilities |
| Operacional | "Qual é meu ritmo de trabalho?" | Stage 2 operating model |
| Financeiro | "Qual é meu perfil financeiro?" | Stage 3 financial |
| Domínio | "Que entidades criamos?" | Stage 4 ontology |

**Ações de teste que o agente DEVE conseguir executar:**

| Ação | Ferramenta |
|------|-----------|
| Registrar uma falha | identity_faults REST |
| Criar um registro de domínio | Stage 4 MCP tools |
| Consultar resumo financeiro | supabase-finance MCP |

**Recuperação de falha:**
- Se uma pergunta não puder ser respondida: o estágio está incompleto.
  Identificar qual Stage (0-4) falhou em registrar o dado necessário.
- Se uma ferramenta não puder ser invocada: a configuração MCP está
  incompleta. Verificar config.yaml, secrets e deploy da Edge Function.

---

### Finalização

Após 5A, 5B e 5C passarem:

```sql
UPDATE user_profiles
SET onboarding_completed = true,
    onboarding_completed_at = now()
WHERE user_id = '<user_id>';
```

O meta-skill está completo. Sessões futuras:
1. Executar scan de startup
2. Se `onboarding_completed = true`: atualizar contexto SOUL.md, pular estágios
3. Se novas necessidades surgirem: executar Stage 4 novamente (recursivo por design)
4. Registrar novas falhas conforme ocorrerem (identity-self-audit sempre ativo)

## Pitfalls

1. **Gerar SOUL.md sem dados** — se Stages 0-4 estiverem incompletos,
   o SOUL.md ficará vazio. Verificar se os dados existem antes de gerar.

2. **Pular a verificação** — 5C é o único teste que confirma que a
   calibração realmente funciona. Sem ele, a calibração é especulativa.

3. **Esquecer skills de domínio no wrapper** — se o Stage 4 criou
   ferramentas MCP mas o wrapper só carrega skills de identidade,
   consultas de domínio falharão. Incluir ambos.

4. **Calibração de usuário vs. universal** — SOUL.md é por usuário.
   Não aplicar a calibração de um usuário a outro.

5. **Calibração não é única** — conforme novas falhas são registradas
   e novas capacidades são adicionadas, o SOUL.md deve ser atualizado.
   O scan de startup do identity-cqrs lida com isso automaticamente
   se os dados estiverem nas tabelas.

## Referências

- agent-onboarding — Orquestrador do meta-skill (este skill é Stage 5)
- identity-self-audit — Detecção de falhas (Stage 0)
- identity-cqrs — Tradução relacional para contexto (Stage 0)
- context-bridge — Injeção de contexto multi-fonte (Stage 0)
- supabase-startup-protocol — Scan de startup obrigatório
- stage-4-system-ontologist — Protocolo de ontologia de domínio
- checkpoints/session_checkpoints — Acompanhamento de progresso do onboarding
