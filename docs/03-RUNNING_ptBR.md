# Executando o Onboarding

Este guia explica como executar o processo de onboarding de 6 estágios, uma vez que o Hermes e o Supabase estejam configurados.

## Início Rápido

```bash
# Garanta que suas secrets estão carregadas
source ~/.hermes/secrets.env

# Inicie o Hermes com o skill de onboarding carregado
hermes --skills agent-onboarding
```

Na primeira execução, o skill orquestrador irá:
1. Executar o scan de inicialização (verificar conexão Supabase, checar tabelas)
2. Detectar que nenhum perfil de usuário existe ainda
3. Iniciar o Estágio 0 (Verificação de Setup)

## Os 6 Estágios

### Estágio 0 — Verificação de Setup

O agente verifica:
- O Hermes Agent está instalado corretamente? (verificação de versão)
- Um provedor LLM está configurado? (responde a prompts?)
- O Supabase está conectado? (API responde?)
- As 6 tabelas base foram criadas? (RLS ativo?)
- Os skills do wrapper estão carregados? (startup-protocol, identity-audit, etc.)

Se algo estiver faltando, o agente guia você na correção.
Quando verificado: "Setup completo. Pronto para o onboarding."

### Estágio 1 — Perfil do Usuário (biografia = career-tracker + MBTI)

**Sub-estágios (em conversa, uma pergunta de cada vez):**

1. **Contexto** — Nome, domínio de trabalho, família, rotina diária → `user_profiles`
2. **Preferências** — Estilo de comunicação, nível de autonomia, agenda → `user_preferences`
3. **MBTI** — "Você conhece MBTI?" → Explicar → Teste rápido (70/93/144/200 perguntas) → `user_mbti`
4. **Career-tracker** — Capacidades, problemas resolvidos, marcos, crises → `career_tracker.*`
5. **MindMaze** — "Quer que eu analise padrões do seu MBTI + carreira?"

**Duração esperada:** 30-60 minutos dependendo da profundidade da carreira.

### Estágio 2 — Modelo Operacional de Trabalho

Entrevista em 5 camadas sobre seu fluxo de trabalho profissional:
1. Ritmos — Dia típico, janelas de trabalho profundo
2. Decisões — Julgamentos recorrentes, limites
3. Dependências — O que você precisa dos outros
4. Conhecimento — O que você sabe que ninguém mais sabe
5. Fricção — O que te bloqueia, soluções alternativas

Powered pelo skill `work-operating-model` (ferramentas MCP).

**Duração esperada:** 20-30 minutos.

### Estágio 3 — Perfil Financeiro

Não é uma entrevista subjetiva — análise orientada a dados:

1. **Importação CSV** — "Quer que eu analise seus extratos bancários? Se sim, compartilhe arquivos CSV."
2. **Perfil baseado em MBTI** — Seu tipo de personalidade revela sua relação com dinheiro
   (ex: INTJ planeja estrategicamente, ENFP gasta impulsivamente, ISTJ poupa sistematicamente)
3. **Metas** — Objetivos de curto (6 meses), médio (2 anos) e longo prazo (5+ anos)
4. **Estratégias** — Orçamento, poupança, investimento — adaptadas ao seu MBTI

Powered pela extensão MCP `supabase-finance` (17 ferramentas).

**Duração esperada:** 15-30 minutos (mais se importar CSVs).

### Estágio 4 — Ontologia do Domínio (Generativa)

O agente descobre quais "coisas" povoam seu trabalho:

1. "Que coisas você cria, gerencia ou transforma no seu trabalho?"
   - Escritor: personagens, obras, capítulos, submissões, editoras
   - Professor: turmas, alunos, lições, avaliações
   - Engenheiro: projetos, componentes, versões, clientes
2. "Como uma coisa se transforma em outra? Ciclo de vida?"
3. "O que você precisa saber sobre cada coisa?"
4. "Como você mede progresso?"

Para cada entidade, o agente propõe uma estrutura de tabela → você valida → ele cria tabelas + ferramentas MCP opcionais + cron job de check-in semanal opcional.

**Duração esperada:** 20-40 minutos.

### Estágio 5 — Calibração do Agente

Tudo dos estágios 1-4 é compilado no comportamento do agente:

1. **Gerar SOUL.md** — Perfil de identidade personalizado (tom, autonomia, princípios)
2. **Configurar wrapper** — Adicionar skills específicas do domínio ao lançador do Hermes
3. **Verificação** — O agente te conhece? Consegue usar as ferramentas que construiu?

**Checkpoint final:** `onboarding_completed = true`

---

## O que Acontece Após o Onboarding

Quando todos os 6 estágios estiverem completos, seu Hermes Agent sabe:

- **Quem você é** (user_profiles + career-tracker + MBTI)
- **Como você trabalha** (work-operating-model + preferências)
- **Sua realidade financeira** (contas, metas, estratégias)
- **As entidades do seu domínio** (tabelas personalizadas + MCPs)
- **Como se comunicar** (estilo, tom, nível de autonomia)

Você pode agora pedir ao agente para trabalhar nas suas tarefas reais — ele tem contexto.

## Retomando Sessões Interrompidas

Se precisar pausar e retomar:

```bash
hermes --skills agent-onboarding
```

O agente verifica `user_profiles.onboarding_stage` e retoma de onde parou.

## Solução de Problemas

| Sintoma | Causa Provável | Correção |
|---------|---------------|----------|
| "Supabase não conectado" | secrets.env não carregado | `source ~/.hermes/secrets.env` |
| "Tabelas não encontradas" | Migrations não aplicadas | `cd hermes-agent-onboarding && supabase db push --linked` |
| "Nenhum provedor responde" | Chave de API ausente ou errada | Verifique as configurações do provedor em `config.yaml` |
| "RLS bloqueando acesso" | Chave de API errada (anon vs service_role) | Use a chave service_role, não a anon |
