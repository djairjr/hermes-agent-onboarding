# Hermes Agent Onboarding — Manual de Configuração do Agente

Um meta-skill generativo de 6 estágios que transforma uma instalação limpa do Hermes Agent em um ecossistema personalizado adaptado ao SEU trabalho — não ao meu.

## O que é isso?

O Hermes Agent é um executor de IA poderoso. Mas instalá-lo não diz a ele quem você é, como trabalha ou o que constrói.

Este meta-skill é um **processo de onboarding estruturado** que entrevista você, descobre seu domínio, constrói suas estruturas de dados e calibra o agente para trabalhar COM você — de forma genérica.

Inspirado por:
- **NateBJones/OB1** — Padrão Edge Function + MCP para ecossistemas de agentes extensíveis
- **MathGALIN/CLI-KIT-NOVA** — Extração de espírito digital através de markdown estruturado
- **effeceee/MBTI Guru** — Perfil de personalidade para interação calibrada

## Os 6 Estágios

```
ESTÁGIO 0 — SETUP (verificar Hermes, modelo, Supabase)
ESTÁGIO 1 — PERFIL DO USUÁRIO (biografia = career-tracker + MBTI)
ESTÁGIO 2 — MODELO OPERACIONAL (ritmos, decisões, fricções)
ESTÁGIO 3 — FINANCEIRO (perfil + metas + estratégias × MBTI)
ESTÁGIO 4 — ONTOLOGIA DO DOMÍNIO (descobrir entidades, gerar tabelas + MCPs)
ESTÁGIO 5 — CALIBRAÇÃO DO AGENTE (SOUL.md, wrapper, verificação)
```

Cada estágio é um skill invocado em ordem. O skill orquestrador `agent-onboarding` gerencia o fluxo e os checkpoints entre estágios.

## Início Rápido

```bash
# 1. Instalar Hermes Agent
pip install hermes-agent

# 2. Clonar este repositório
git clone https://github.com/djairguilherme/hermes-agent-onboarding
cd hermes-agent-onboarding

# 3. Executar o onboarding
hermes --skills agent-onboarding
# → Siga a entrevista. O agente descobre seu domínio,
#   constrói suas tabelas, configura seus MCPs, se calibra.
```

## Pré-requisitos

- Python 3.11+ ou Node.js 20+
- Um projeto Supabase (plano gratuito funciona)
- Um provedor de LLM (OpenAI, Anthropic, Ollama ou qualquer API compatível com OpenAI)

## Documentação

| Documento | O que cobre |
|-----------|-------------|
| [Instalação](docs/00-INSTALLATION_ptBR.md) | Instalar Hermes em qualquer SO |
| [Configuração](docs/01-CONFIGURATION_ptBR.md) | Provedores, modelos, secrets |
| [Setup Supabase](docs/02-SUPABASE_ptBR.md) | Criar projeto, aplicar migrations |
| [Executando Onboarding](docs/03-RUNNING_ptBR.md) | Executar o processo de 6 estágios |
| [Personalizando](docs/04-CUSTOMIZING_ptBR.md) | Adaptar para seu domínio |
| [Segurança](docs/SECURITY_ptBR.md) | Protocolo de segurança do stack |

## Arquitetura

```
requisição do usuário
    ↓
agent-onboarding (skill orquestrador)
    ├── Estágio 0: Verificação de Setup
    │   └── supabase-startup-protocol (scan, checkpoint)
    ├── Estágio 1: Perfil do Usuário
    │   ├── career-mapping skill (capacidades, marcos)
    │   └── MBTI Guru adaptado (teste de 70/93/144/200 perguntas)
    ├── Estágio 2: Modelo Operacional
    │   └── work-operating-model skill + MCP
    ├── Estágio 3: Financeiro
    │   └── supabase-finance MCP (contas, transações, metas)
    ├── Estágio 4: Ontologia do Domínio
    │   └── Generativo: entidades → tabelas → MCPs
    └── Estágio 5: Calibração do Agente
        └── user_preferences → SOUL.md → wrapper
            ↓
Hermes Agent personalizado pronto para SEU trabalho
```

## Camada de Dados (Supabase)

6 tabelas base + schema career-tracker, todas no schema `public`, protegidas por RLS (service_role only):

| Tabela | Propósito |
|--------|-----------|
| user_profiles | Identidade, família, rotinas |
| user_preferences | Tom, autonomia, agenda, rastreamento financeiro |
| user_mbti | 4 dimensões, tipo, características observadas |
| user_style | Comunicação: tamanho de frase, vocabulário, tom |
| user_relations | Pessoas-chave: parceiros, família, clientes |
| user_beliefs | Valores, princípios, não-negociáveis |

Mais `career_tracker.*` (capabilities, solved_problems, milestones, deliveries) — a camada de biografia.

## Licença

MIT — livre para usar, adaptar e distribuir.

Construído por **Djair Guilherme** com Hermes Agent.
