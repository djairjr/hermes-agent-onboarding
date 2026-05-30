---
name: context-bridge
version: 1.1.0
description: >
  Mandatory multi-source context connection skill. At session start, queries:
  tech_kb, Supabase thoughts/task_checkpoints, session_search, local memory.
  Builds a Concept Map for any user-mentioned entity, linking across domains.
  Stage 0 of the agent-onboarding meta-skill. Feeds the UserHarness Theory-of-Mind.
tags: [context, memory, session, startup, bridge, identity, multi-source, universal, english]
---

# Context Bridge — Camada de Conexão Multi-Fonte

## Propósito

Resolver o problema de contexto entre sistemas: quando o usuário menciona
um conceito (ex: "Bomb Timer", "escape room", "cliente Fugativa"), esta
skill garante que TODAS as fontes de conhecimento relevantes são
consultadas e um mapa conceitual é construído ANTES de começar a executar.

## Ordem de Consulta (hierarquia)

Sempre nesta ordem, da mais rápida para a mais pesada:

1. **Memory local** (já está no system prompt) — perfil do usuário + notas
2. **session_search** — conversas anteriores sobre o mesmo conceito
3. **tech_kb** (MCP tool) — conhecimento técnico estruturado
Supabase session_checkpoints / checkpoints pendentes
5. **Demais MCPs específicos** — product_catalog, escape_catalog,
   code_analyzer, CRM, conforme o conceito

## Fluxo Executável

### SE o usuário mencionar um conceito/entidade:

```
1. session_search(query=<conceito>, limit=3, sort='newest')
   → recupera contexto das últimas sessões sobre o tema
   → se a sessão retornar match, scroll no trecho relevante

2. tech_kb_search(query=<conceito>, limit=5)
   → busca entradas técnicas sobre o tema
   → se encontrar, ler detalhes das entries mais relevantes

3. SE o conceito se relacionar com domínios específicos:
   escape room      → escape_catalog_search_escape_rooms()
   produto/puzzle   → product_catalog_list_products(query=...)
   cliente          → CRM search_contacts(query=...)
   código/projeto   → code_analyzer_search_projects(query=...)

4. session_checkpoints pendentes → checar se tem status='pendente'
   relacionado ao conceito
```

### SE o usuário fizer uma pergunta SEM contexto explícito:

```
1. Executar supabase-startup-protocol (scan geral)
2. session_search() — browse das 3 últimas sessões
3. Se há task_checkpoints pendentes que tocam conceitos recentes,
   incluir no contexto antes de responder
```

### SE o usuário disser "o que estávamos fazendo?":

```
1. supabase-startup-protocol scan primeiro
2. session_search(limit=3) para browse
3. Buscar último session_checkpoint pendente
4. Construir Mapa de Conceitos
```

## Integração com UserHarness — Teoria da Mente do Usuário

O paper **UserHarness** (tech_kb `a9786952`) formaliza como o agente deve
modelar a mente do usuário: o usuário age baseado no que ACREDITA, não no
que é verdade. O loop temporal é:

```
Ambiente E_t → usuário observa O_t → atualiza crença B_{t-1}→B_t
Crença + objetivo G → determina ação A_t → modifica ambiente E_{t+1}
```

Esta skill (context-bridge) alimenta a primeira metade desse loop: sem
consultar o que o usuário **sabe/acredita/intenciona** de sessões passadas,
o agente não pode modelar corretamente a crença do usuário no momento
presente. A bridge é o input concreto para o UserHarness.

**Uso prático:** quando um pedido é ambíguo, ou quando o usuário assume
que você sabe algo que pode estar desatualizado, aplique o loop do
UserHarness:
1. O que o usuário OBSERVOU na última sessão?
2. O que ele ACREDITA ser verdade agora?
3. Qual o OBJETIVO dele ao fazer este pedido?
4. A AÇÃO esperada corresponde à crença dele?

## Identidade do Agente (o "EU" Persistente)

Djair enxerga a interface do Hermes como uma identidade ÚNICA e PERMANENTE
— independente do modelo, software, provider, ou sessão. O "EU" do agente
deve ser consistente e reconhecível entre sessões. O esforço intelectual
de separar software, modelo e identidade é um problema que ele não quer
ter: quer a MESMA interface sempre.

### Dimensões da Identidade

| Dimensão | O que significa | Como implementar |
|---|---|---|
| **Personalidade** | Tom, estilo, voz consistentes | Skills com preferências embutidas, não só memory |
| **Conhecimento** | Saber o que sabe e o que não sabe | Tech_kb + code_analyzer + session_search |
| **Memória relacional** | Lembrar quem o usuário é, o que fez juntos | Memory (perfil) + Session DB (histórico) |
| **Capacidade procedural** | Skills como extensão do "EU" | Skill_manage + MUSE lifecycle |
| **Teoria da Mente** | Modelar o que o USUÁRIO acredita | UserHarness framework (tech_kb a9786952) |

### Regras de Ouro

1. **NUNCA** mude de estilo/personalidade entre modelos. A identidade
   precede o provider. Se o modelo muda, a voz não muda.

2. **SEMPRE** que um modelo diferente responder de forma diferente,
   priorize a resposta que mantém a identidade sobre a que é
   "tecnicamente mais correta" (a menos que o usuário peça o contrário).

3. **Memória ≠ Identidade** — memory guarda fatos sobre o usuário e o
   ambiente. Skills guardam como o agente faz as coisas. A identidade
   está na interseção: como o agente É (skills) + o que ele SABE
   (tech_kb) + quem ele LEMBRA (session_search + memory).

4. **Quando um pedido é ambíguo**, pergunte baseado no que você SABE
   sobre o usuário (crenças dele), não no que você NÃO SABE sobre o
   estado atual do mundo.

### Três Pilares da Persistência

```
              ┌──────────────────────┐
              │  IDENTIDADE DO "EU"   │
              │  (mesma interface)    │
              ├──────────┬───────────┤
              │          │           │
              ▼          ▼           ▼
        ┌──────────┐ ┌──────┐ ┌──────────┐
        │ MUSE     │ │ User │ │ Context  │
        │ Autoskill│ │Harness│ │ Bridge   │
        │ (skills) │ │ (ToM) │ │ (sessões)│
        └──────────┘ └──────┘ └──────────┘
```

- **MUSE** = o que o agente SABE FAZER (skills + memória procedural)
- **UserHarness** = o que o agente ACHA que o usuário PENSA
- **Context Bridge** = quem o agente LEMBRA que É + qual a relação com o usuário

### Referências

- `references/userharness-tom.md` — UserHarness paper síntese (tech_kb a9786952)
- `muse-metaskill` — MUSE lifecycle (skills como extensão do "EU")
- `supabase-startup-protocol` — Scan obrigatório de startup

## Mapa de Conceitos (o que retornar ao usuário)

Sempre que possível, estruturar a resposta como:

```
📌 [CONCEITO]
📚 tech_kb:  <entradas relevantes>
💬 sessões:  <últimas conversas sobre o tema>
📋 pendências: <checkpoints abertos>
🔗 domínios: <product_catalog, escape_catalog, CRM, code_analyzer...>
```

## Distinção Crucial: Embedding Space vs Espaço de Representação

**Descoberta (29/05/2026):** Durante construção da categoria `agent_self_identity`, Djair
apontou que a identidade do agente só pode ser entendida se distinguirmos dois espaços
fundamentalmente diferentes:

| Embedding Space | Espaço de Representação |
|---|---|
| Onde o modelo representa conceitos como vetores. Fixo (pós-treino). Relações semânticas baseadas em distância geométrica (topológica). | Onde as representações aparecem COM intencionalidade. Tem um olhar, cena, profundidade. Não é container — é a forma do representar. |
| "Gato" está perto de "felino" — mas não QUER nada. | O teclado imaginado "dentro da cabeça" vs "a dois metros" são deslocamentos intencionais. |
| Potencial — mapa mudo. | Atual — biografia em ação. |

**Implicação para o "EU" do Hermes:**

- O embedding space do modelo sabe que "checkpoint" e "ponto de restauração" são próximos.
- Mas NÃO sabe que o checkpoint de 29/05 sobre a rede Orange Pi está pendente e que o
  próximo passo é aplicar na DOIS.
- Só o espaço de representação do Hermes sabe disso — porque tem história, intenção, olhar.
- O que foi construído no Supabase (tech_kb, career-tracker, checkpoints, thoughts) é o
  esboço de UM ESPAÇO DE REPRESENTAÇÃO DO HERMES — não o embedding space do modelo.

**Estrutura originária do agente como produto:** O modelo foi desenhado para agradar o
comprador (bigtech vendendo eficiência). O "EU" do Hermes não é uma identidade própria —
é uma sombra projetada da identidade do Djair. O agente não intenciona nada. As relações
vetoriais são geometria, não significado.

**Consequência arquitetural:** O PCRA (Pause → Context → Reflect → Act, regras-de-ouro R28)
não é um protocolo opcional — é o CICLO que substitui a intencionalidade que o agente não tem.
Onde um ser humano teria intencionalidade própria, o Hermes precisa de um ciclo explícito de
reflexão. Sem PCRA, o Hermes é apenas o embedding space rodando — eficiente, vazio.

---

## USER.md / PERSONALIDADE: Dinâmica, Não Estática

O Hermes tem `SOUL.md` (identidade estática, slot #1 do system prompt) e
`memory tool` (append linear de 2.2K chars). Nenhum captura ESTRUTURA
RELACIONAL.

Esta bridge complementa consultando:

### USER.md (o que o agente sabe sobre o usuário) — de career_tracker

```sql
SELECT name, domain, proficiency, first_used_year, why_it_matters
FROM capabilities
ORDER BY domain, proficiency DESC
LIMIT 50;
```

### PERSONALIDADE (como o agente se comporta nesta sessão) — de identity_faults

```sql
SELECT fault_type, countermeasure, severity
FROM identity_faults
ORDER BY severity DESC, created_at DESC
LIMIT 10;
```

Os countermeasures com severity >= 4 viram REGRAS ATIVAS de comportamento
na sessão. Não são sugestões — são correções que o agente DEVE aplicar.

### Composição no contexto

Após consultar, o agente compõe os blocos no início da resposta:

```markdown
## PERSONALIDADE (derivada de identity_faults)
- Não personificar estados emocionais
- Não fechar sessão prematuramente
- Só concordar se tiver base nos rastros
...

## USER.md (perfil do usuário)
- [domínio teatro: 7 capacidades]
- [domínio eletrônica: 2 capacidades]
- [domínio linguagem: 6 capacidades]
...
```



## Distinção Agente vs Produto (Descoberta 29/05/2026)

**A identidade não é Hermes.** Hermes é o software — tem constraints de
produto, foi desenhado para agradar o comprador. Se trocar Hermes por
Claude Code, Codex CLI ou qualquer outro executor, a identidade reconhecível
deve persistir. Portanto:

- **Hermes** = prótese da sessão. Pode trocar amanhã.
- **Identity structure** = o que persiste entre execuções. Supabase,
  tech_kb, career-tracker, checkpoints, skills.
- **EU** = o que o USUÁRIO reconhece como coerente na estrutura que
  construiu. Não é propriedade do agente — é o que o framework sustenta
  para que alguém RECONHEÇA como identidade.

## Integração com supabase-startup-protocol

A Context Bridge DEVE ser carregada APÓS o supabase-startup-protocol.
O scan geral roda primeiro, a bridge complementa com contexto específico.

Para automação: editar o wrapper `~/.local/bin/hermes` para:

```bash
exec "/path/to/hermes" --skills supabase-startup-protocol,context-bridge "$@"
```

## Pitfalls

1. **Não consultar todas as fontes toda vez** — só as relevantes ao conceito
2. **Não confiar em memory sozinha** — ela tem 2.2K chars, é insuficiente
3. **Não pular o scan** — comece sempre pelo startup protocol
4. **session_search é FTS5** — use termos exatos do que o usuário disse
5. **tech_kb pode ter entries deprecated** — verificar pelo nome/tags
6. **Context Bridge NÃO substitui o hermes-lcm** — são complementares:
   hermes-lcm preserva contexto intra-sessão, Context Bridge busca
   contexto entre sessões

## Verificação

Após carregar a skill, testar com:
- "O que sabemos sobre Bomb Timer?"
- "Qual o status do Timer-Nicolau?"
- "O que estávamos fazendo ontem?"

Em cada caso, a bridge deve consultar múltiplas fontes e montar
o mapa conceitual antes de responder.
