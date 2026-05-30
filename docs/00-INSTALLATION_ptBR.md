# Instalação do Hermes Agent

Este guia cobre a instalação do Hermes Agent em qualquer sistema operacional. O Hermes roda em Linux, macOS e Windows (via WSL2).

## Pré-requisitos

- **Python 3.11+** (recomendado) ou **Node.js 20+**
- **Git** para clonar repositórios
- **Supabase CLI** (opcional, para migrations personalizadas)

## Opção A: Instalar via pip (recomendado)

```bash
pip install hermes-agent
```

Verificar instalação:
```bash
hermes --version
```

## Opção B: Instalar via npx

```bash
npx hermes-agent --version
```

Nota: npx instala temporariamente. Para uso persistente, prefira pip.

## Opção C: Docker

```bash
docker pull hermesagent/hermes-agent
docker run -it hermesagent/hermes-agent
```

## Pós-Instalação

Após instalar o Hermes, você precisa:

1. **Um provedor de LLM** — Crie uma conta em um destes:
   - [OpenRouter](https://openrouter.ai/) (recomendado — uma chave para muitos modelos)
   - [Anthropic](https://console.anthropic.com/) (modelos Claude)
   - [OpenAI](https://platform.openai.com/) (modelos GPT)
   - Ou rode [Ollama](https://ollama.ai/) localmente para modelos gratuitos offline

2. **Um projeto Supabase** — Crie uma conta gratuita em [supabase.com](https://supabase.com/).

3. **Chaves de API** — Você precisará de ao menos:
   - Chave de API do provedor LLM (ex: OpenRouter)
   - URL do projeto Supabase + chave service_role

## Notas sobre WSL2 (Windows)

Se usar Windows, instale o Hermes dentro do WSL2:

```bash
# Dentro do WSL2 Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip git
pip install hermes-agent
```

O sistema de arquivos do Windows é acessível em `/mnt/c/` (unidade C:), `/mnt/d/` (unidade D:), etc.

## Verificando a Instalação

```bash
# Verificar versão
hermes --version

# Verificar skills disponíveis
hermes --help

# Verificar se Ollama está rodando (se usar modelos locais)
curl http://localhost:11434/api/tags
```

Se todas as verificações passarem, prossiga para [Configuração](01-CONFIGURATION_ptBR.md).
