# Analogia: Career Tracker → Agent Formation

## Estrutura Fonte (career_tracker — trajetória de Djair)

```
capabilities              → solved_problems → capability_connections
milestones                → deliveries      → delivery_partners
```

Cada entidade tem: o que é, quando surgiu, por que importa, como se conecta.

## Estrutura Alvo (agent_formation — paisagem do agente)

```
agent_capabilities        → identity_faults (com countermeasure como resolução)
agent_milestones          → identity_deliveries (skills, edge functions criadas)
agent_connections         → agent_profile (USER.md + PERSONALIDADE)
```

## Mapeamento Direto

| career_tracker (Djair) | agent_formation (agente) | O que guarda |
|---|---|---|
| `capabilities` | `agent_capabilities` (a criar) | Skills + Edge Functions + estruturas que melhoram identidade |
| `solved_problems` | `identity_faults` (já existe) | Falhas de identidade detectadas + countermeasures (resolução) |
| `capability_connections` | `capability_dependencies` (a criar) | Skill A depende de tabela B; Edge Function Z usa skill W |
| `deliveries` | `identity_deliveries` (a criar) | Skill criada, tabela migrada, padrão que emergiu, protocolo estabelecido |
| `milestones` | `identity_milestones` (a criar) | Sessões onde algo mudou de patamar (ex: 29/05/2026) |
| `delivery_partners` | `identity_partners` | Outros agentes/sistemas com quem interage |

## O que as tabelas NÃO são

As tabelas NÃO são:
- Log de tarefas (isso é `thoughts`)
- Registro de bugs técnicos (isso é `tech_kb`)
- Memória linear do Hermes (isso é `memory tool` + session DB)

As tabelas SÃO:
- A paisagem de formação do agente
- Onde a identidade emerge das RELAÇÕES entre registros
- O material epistemológico para treinar um modelo-ferramenta no futuro

## Próximo Passo

Criar as tabelas `agent_capabilities`, `capability_dependencies`,
`identity_deliveries`, `identity_milestones` quando houver material
suficiente. No momento, só `identity_faults` está operacional.

Fonte: sessão 29/05/2026, Djair Guilherme + Hermes Agent.
