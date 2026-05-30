# UserHarness: Harnessing User Minds for Stronger Agent Theory-of-Mind

**Fonte:** arXiv 2605.27721v1 (26 May 2026) — Cheng Qian, Jiayu Liu, Heng Ji (UIUC)
**Tech KB:** `a9786952`
**Tags:** theory-of-mind, user-modeling, belief-tracking, FSM-soberana, Algoritmo-das-Expectativas

## Síntese

Framework que reframela Theory-of-Mind como **reconstrução explícita da mente
do usuário** em vez de modelagem indireta de comportamento. O agente deve
inferir o que o usuário OBSERVA, ACREDITA, INTENCIONA e FAZ, mesmo que
esses estados mentais sejam privados/inacessíveis.

## Loop Temporal (Observe → Believe → Intend → Act)

```
   Ambiente (E_t)
       │
       ▼
   Observação (O_t) ←─ o que o usuário REALMENTE vê
       │
       ▼
   Crença (B_{t-1} → B_t) ←─ atualizada pela observação
       │
       ▼
   Crença + Objetivo (G) → Ação (A_t)
       │
       ▼
   Ambiente (E_{t+1}) ←─ modificado pela ação
```

Elementos "trancados" (não observáveis diretamente pelo agente):
- O que o usuário observou (O_t) — pode ser diferente do que aconteceu
- A crença do usuário (B_t) — pode estar desatualizada ou errada
- O objetivo genuíno (G) — pode não estar explícito no pedido

## Resultados

| Métrica | Valor |
|---------|-------|
| Macro-accuracy | **95.94%** |
| Ganho sobre métodos existentes | +15% relative |
| Ganho sobre melhor prompt-only | +20% relative |
| Benchmarks testados | 5 |

## Relevância para o Hermes

1. **FSM Soberana**: a FSM rastreia o estado do sistema. UserHarness
   rastreia o que o USUÁRIO acredita sobre o estado. Os dois são
   complementares.

2. **Algoritmo das Expectativas (1996, USP)**: o Algoritmo das Expectativas
   é essencialmente um modelo preditivo do estado mental alheio. UserHarness
   fornece a estrutura formal para implementá-lo: o agente modela a
   informação parcial do jogador, suas crenças e intenções.

3. **Escape Room puzzles**: os jogadores agem com informação incompleta.
   Um puzzle que depende de o jogador "lembrar" de uma pista vista antes
   é um caso de UserHarness — o jogador pode ou não ter observado a pista,
   e o puzzle deve modelar essa crença.

4. **Identidade do agente**: o dual do UserHarness. UserHarness modela a
   mente do USUÁRIO. A identidade persistente do Hermes modela quem o
   AGENTE É. Juntos formam a relação agente-usuário completa.

## Conexão com MUSE-Autoskill

| | MUSE-Autoskill | UserHarness | Context Bridge |
|---|---|---|---|
| **O que modela** | O que o agente SABE FAZER | O que o usuário PENSA/Acredita | Quem o agente LEMBRA que É |
| **Mecanismo** | Skill lifecycle + .memory.md | Loop crença→objetivo→ação | Multi-source lookup |
| **Duração** | Persistente entre tarefas | Por interação | Por sessão |
| **Resultado** | Skills como extensão do "EU" | Ações alinhadas com intenção do usuário | Continuidade cross-session |
