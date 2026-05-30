# Hermes Agent Installation

This guide covers installing Hermes Agent on any OS. Hermes runs on Linux, macOS, and Windows (via WSL2).

## Prerequisites

- **Python 3.11+** (recommended) or **Node.js 20+**
- **Git** for cloning repositories
- **Supabase CLI** (optional, for custom migrations)

## Option A: Install via pip (recommended)

```bash
pip install hermes-agent
```

Verify installation:
```bash
hermes --version
```

## Option B: Install via npx

```bash
npx hermes-agent --version
```

Note: npx installs temporarily. For persistent use, prefer pip.

## Option C: Docker

```bash
docker pull hermesagent/hermes-agent
docker run -it hermesagent/hermes-agent
```

## Post-Installation

After installing Hermes, you need:

1. **An LLM provider** — Create an account at one of:
   - [OpenRouter](https://openrouter.ai/) (recommended — one API key for many models)
   - [Anthropic](https://console.anthropic.com/) (Claude models)
   - [OpenAI](https://platform.openai.com/) (GPT models)
   - Or run [Ollama](https://ollama.ai/) locally for free, offline models

2. **A Supabase project** — Create a free account at [supabase.com](https://supabase.com/).

3. **API keys** — You'll need at least:
   - LLM provider API key (e.g., OpenRouter)
   - Supabase project URL + service_role key

## WSL2 Notes (Windows)

If using Windows, install Hermes inside WSL2:

```bash
# Inside WSL2 Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip git
pip install hermes-agent
```

The Windows filesystem is accessible at `/mnt/c/` (C: drive), `/mnt/d/` (D: drive), etc.

## Verifying Installation

```bash
# Check version
hermes --version

# Check skills are available
hermes --help

# Check if Ollama is running (if using local models)
curl http://localhost:11434/api/tags
```

If all checks pass, proceed to [Configuration](01-CONFIGURATION.md).
