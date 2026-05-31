---
name: supabase-startup-protocol
version: 2.3.0
description: >
  Protocolo obrigatório de abertura E fechamento de sessão. Scan do Supabase
  ao iniciar, checkpoint no Supabase ao encerrar cada tarefa, e consolidação
  ao final da sessão. Nenhuma ação de trabalho deve ocorrer antes do scan.
  v2.3.0: Pitfall PGRST301 resolvido permanentemente — instruções explícitas
  para uso de service_role_key com redact_secrets ativado.
tags: [supabase, startup, shutdown, protocolo, R22, inicio-sessao, checkpoint, triagem-semanal]
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

## PARTE 1 — STARTUP (abertura de sessão)

### Quando executar

**Sempre** no início de cada sessão. Primeira ação. Inegociável.

### Etapa 1 — Scan de estado geral (paralelo)

Chamar TODOS os MCPs em paralelo no primeiro turno.

### Etapa 2 — Buscar tarefas pendentes

Consultar `session_checkpoints` com service_role.

### Etapa 3 — Reportar ao usuário

```
=== SUPABASE STARTUP ===
📚 tech_kb:     <N> entries (última: <nome>)
🔧 code-analyzer: <N> projetos, <N> snapshots
📦 produtos:     <N> ativos
🧩 escape rooms: <N> salas
📋 pendências:   <N> tarefas abertas
📊 thoughts:     <N> total
```

---

## PARTE 2 — CHECKPOINT (por tarefa concluída)

Ao final de CADA tarefa ou sub-tarefa significativa, registrar
checkpoint com:

- content, entry_type='task_checkpoint', occurred_at
- refs: status, projeto, cliente, proximo_passo, bloqueio, tech_kb_ref, valor

---

## PARTE 3 — SHUTDOWN (fim da sessão)

1. Consolidar checkpoints da sessão
2. Salvar thought de sessão (entry_type='session_end')
3. Atualizar supermemory
4. Atualizar TOC (tech_kb entry 84add9d6) se houver mudanças estruturais

---

## PARTE 4 — TRIAGEM SEMANAL DE THOUGHTS

Toda **segunda-feira**: classificar thoughts crus, consolidar em estrutura
correta, remover da tabela thoughts. Thoughts é funil de ENTRADA, não de
ARMAZENAMENTO.

---

## Verificação pós-configuração

Iniciar sessão: `ollama launch hermes` → scan deve rodar automaticamente.

## Integração com regras-de-ouro

- **R22**: implementação executável — Supabase primeiro, sempre
- **R8**: skill documentado que cobre o domínio, validado pelo usuário
- **R4**: checklist visível de estado antes de começar
- **R24**: panorama multi-sistema antes de responder sobre pendências

## Pitfalls

1. **Esquecer de executar** — o protocolo DEVE ser o primeiro bloco de tool calls da sessão
2. **Pular quando o usuário já deu tarefa específica** — mesmo assim, execute o scan primeiro
3. **Achar que "lembra"** — não confie na memória de sessão. Consulte o Supabase.
4. **Checkpoint sem próximo_passo** — inútil. Sempre preencher.
5. **Shutdown sem consolidar** — se a sessão terminar abruptamente, pelo menos o último checkpoint foi salvo.
6. **Supermemory lotada** — se não couber o resumo, priorizar o checkpoint mais recente.
7. **Pitfall de Chave Secreta** — NUNCA grep/read_file no secrets.env. Source + variável de ambiente é o único caminho.
8. **Consulte tech_kb entry 81c48035** antes de editar config.yaml ou secrets.env.
