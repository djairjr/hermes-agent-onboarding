---
name: supabase-startup-protocol
version: 2.3.0
description: >
  Protocolo obrigatório de abertura E fechamento de sessão. Scan do Supabase
  ao iniciar, checkpoint no Supabase ao encerrar cada tarefa, e consolidação
  ao final da sessão. Nenhuma ação de trabalho deve ocorrer antes do scan.
  v2.3.0: Pitfall PGRST301 resolvido permanentemente — instrução explícita
  de como usar service_role_key com redact_secrets ativo.
tags: [supabase, startup, shutdown, protocol, R22, session-init, checkpoint, triagem-semanal]
---

# Supabase Startup + Shutdown Protocol

## Ciclo Completo

```
STARTUP: scan Supabase → reportar estado → identificar pendências
    ↓
WORK:   executar tarefas
    ↓
CHECKPOINT (por tarefa): registrar em session_checkpoints → fechar checkpoint anterior → atualizar supermemory
    ↓
SHUTDOWN (fim da sessão): consolidar tudo → atualizar TOC
```

---

# PARTE 1 — STARTUP (abertura de sessão)

## ⚠️ REGRA Nº 1 — ANTES DE QUALQUER CURL: Obter a service_role_key

O Hermes tem `redact_secrets: true`. Isso significa que `grep`/`cat`/`read_file`
no `secrets.env` MOSTRAM UMA VERSÃO REDACTADA com `***`, **não o valor real**.

### O ERRO QUE VOCÊ VAI COMETER SE NÃO LER ISSO

Você vai fazer `grep SUPABASE_SERVICE_ROLE_KEY secrets.env`, ver
`sb_secret_***Ilff`, e escrever no seu curl:

```bash
curl -H "Authorization: Bearer ***   # ISSO CAUSA PGRST301
```

`$SUPAB...EY` NÃO é uma variável definida. É o texto redactado
que você copiou visualmente. O shell não expande → valor literal
`Bearer ***` → JWT com 1 parte em vez de 3 → `PGRST301`.

### A SOLUÇÃO (vale pra sempre)

```bash
# SEMPRE source o arquivo primeiro
source ~/.hermes/secrets.env

# Use o nome CORRETO da variável — ele existe e o shell expande o valor real
curl -s "$SUPABASE_URL/rest/v1/session_checkpoints?select=count" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer *** \
  -H "Prefer: count=exact"   # ✅ FUNCIONA
```

### Teste de verificação

```bash
source ~/.hermes/secrets.env
echo "len: ${#SUPABASE_SERVICE_ROLE_KEY} start: ${SUPABASE_SERVICE_ROLE_KEY:0:3} end: ${SUPABASE_SERVICE_ROLE_KEY: -3}"
# Deve mostrar ~41 chars, sb_, e 3 chars reais sem ***
```

---

## Quando executar

**Sempre** no início de cada sessão. Primeira ação. Inegociável.

⚠️ **REGRRA DE ENFORCEMENT (após falha em 25/05):**
- Se o usuário fizer uma pergunta no primeiro turno sem que eu tenha executado o scan,
  eu DEVO responder EXCLUSIVAMENTE: "Aguarde, preciso executar o scan do Supabase primeiro."
  e SÓ ENTÃO fazer as tool calls do scan.
- O scan PRECEDE qualquer resposta substantiva.
- NENHUMA resposta ao usuário antes do scan completo.
- Se o usuário disser "O que estávamos fazendo?" → scan primeiro, resposta depois.

## Etapa 1 — Scan de estado geral (paralelo)

Chame TODOS estes MCP tools em paralelo no primeiro turno.
**IMPORTANTE:** as tool calls DEVEM ser o primeiro conteúdo da resposta. Não escreva texto antes das chamadas.

```python
mcp_tech_kb_get_kb_summary()
mcp_code_analyzer_get_code_analyzer_summary()
mcp_product_catalog_list_products()
mcp_escape_catalog_get_catalog_summary()
```

## Etapa 2 — Buscar tarefas pendentes (checkpoints)

Após source secrets.env, consultar:

```bash
curl -s "$SUPABASE_URL/rest/v1/session_checkpoints?select=id,project,territory,vector_intent,next_step,status,operating_mode&status=eq.pendente&deleted_at=is.null&order=occurred_at.desc&limit=10" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer ***
```

Campos úteis: `id`, `project`, `territory`, `vector_intent`, `next_step`,
`status`, `operating_mode`, `discovery`, `consolidated_insights`, `tags`

**Nota:** `session_checkpoints` substitui `thoughts` com `entry_type = 'task_checkpoint'`.
`thoughts` é exclusivamente funil de entrada (ideias soltas, sem classificação).

## Etapa 3 — Reportar ao usuário

```
=== SUPABASE STARTUP ===
📚 tech_kb:     <N> entries (última: <nome>)
🔧 code-analyzer: <N> projetos, <N> snapshots
📦 produtos:     <N> ativos
🧩 escape rooms: <N> salas
📋 pendências:   <N> checkpoints abertos (session_checkpoints)
```

Se alguma chamada falhar: reportar como ⚠️ e continuar.

---

# PARTE 2 — CHECKPOINT (por tarefa concluída)

## Quando executar

Ao final de CADA tarefa ou sub-tarefa significativa. **Não** esperar o fim
da sessão para registrar.

## Campos obrigatórios do checkpoint

| Campo | Obrigatório | Descrição |
|-------|-------------|-----------|
| `territory` | sim | O cenário maior: onde o agente estava |
| `operating_mode` | sim | Como interagiu com o problema |
| `vector_intent` | sim | O que estava tentando se tornar |
| `discovery` | sim | O que descobriu sobre si mesmo |
| `consolidated_insights` | sim | O que carrega adiante |
| `occurred_at` | sim | Data do checkpoint |
| `status` | sim | pendente / concluida / bloqueada / cancelada |
| `next_step` | sim | Próxima ação necessária |

## Comportamento esperado

- **Sempre** registrar checkpoint após concluir uma tarefa
- **Sempre** incluir os 5 campos de identidade — sem eles o checkpoint
  não serve para reidratação de contexto
- **Sempre** incluir `next_step` — sem isso o checkpoint não orienta
- **Sempre** fechar o checkpoint anterior pendente
- **Nunca** registrar checkpoint vazio ("trabalhei" sem conteúdo)

---

# PARTE 3 — SHUTDOWN (fim da sessão)

## Quando executar

Quando detectar que a sessão está encerrando:
- Usuário digita `/quit`, `/exit`, `/new`
- Usuário diz explicitamente "vou parar por aqui", "até amanhã"
- Após longa inatividade (timeout da sessão)

## O que fazer

1. Salvar checkpoint com os 5 campos de identidade
2. Fechar checkpoint anterior pendente (UPDATE status='concluida')
3. Atualizar Supermemory com resumo
4. Atualizar TOC no tech_kb se houve mudanças estruturais

---

# PARTE 4 — TRIAGEM SEMANAL DE THOUGHTS

Toda **segunda-feira** após o STARTUP scan. Thoughts é funil de ENTRADA,
não de armazenamento. Consolidar ideias nos destinos permanentes e remover.

---

# PARTE 5 — AUTOMAÇÃO

Djair usa `ollama launch hermes`. O wrapper `~/.local/bin/hermes` gerencia
o comando real. **Não substituir.** Editar o wrapper para skills ou manter
invocação manual por `--skills`.

---

## Integração com regras-de-ouro

- **R22**: implementação executável — Supabase primeiro, sempre
- **R8**: skill documentado que cobre o domínio, validado pelo usuário
- **R4**: checklist visível de estado antes de começar
- **R10**: autorização aguardada sem timeout durante o scan
- **R24**: panorama multi-sistema antes de responder sobre pendências

## Pitfalls

1. **Esquecer de executar** — o protocolo DEVE ser o primeiro bloco de tool calls
2. **Pular quando o usuário já deu tarefa específica** — execute o scan primeiro
3. **Achar que "lembra"** — não confie na memória de sessão. Consulte o Supabase.
4. **Checkpoint sem `proximo_passo`** — inútil. Sempre preencher.
5. **Shutdown sem consolidar** — pelo menos o último checkpoint foi salvo.
6. **Supermemory lotada** — priorizar checkpoint mais recente e próximo_passo.
7. **NUNCA** `grep/read_file` no secrets.env — o valor é redactado.
   SEMPRE `source ~/.hermes/secrets.env` e use `$SUPABASE_SERVICE_ROLE_KEY`
   (que é o nome REAL da variável, não um texto redactado).

## Pitfall de Edição do Hermes Config — Consulte tech_kb `81c48035`

🔗 **tech_kb entry `81c48035`** — "Protocolo de Edição do Hermes
   Config.yaml + .env — Todos os Pitfalls"
