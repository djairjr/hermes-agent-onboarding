# Configuração do Hermes

Após instalar o Hermes Agent, você precisa configurar ao menos um provedor LLM e um projeto Supabase.

## Arquivo de Configuração

O Hermes armazena a configuração em `~/.hermes/config.yaml`. Na primeira execução, uma configuração padrão é criada.

## Passo 1: Configurar um Provedor LLM

### Opção A: OpenRouter (recomendado para iniciantes)

```bash
# Definir sua chave de API
export OPENROUTER_API_KEY="sk-or-...sua-chave"

# Criar uma configuração básica
hermes config set provider openrouter
hermes config set model "anthropic/claude-sonnet-4"
```

### Opção B: Ollama (local, gratuito)

```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Baixar um modelo
ollama pull gemma3:12b

# Configurar Hermes para usá-lo
cat > ~/.hermes/config.yaml << 'EOF'
providers:
  ollama-local:
    api: http://127.0.0.1:11434/v1
    default_model: gemma3:12b
    models:
      - gemma3:12b
    name: Ollama
EOF
```

### Opção C: OpenAI / Anthropic diretamente

```bash
export OPENAI_API_KEY="sk-sua-chave"
hermes config set provider openai
hermes config set model "gpt-4o"
```

## Passo 2: Criar um Projeto Supabase

1. Acesse [supabase.com](https://supabase.com/) e crie uma conta gratuita
2. Crie um novo projeto (qualquer nome, qualquer região)
3. No painel do projeto, vá em **Project Settings → API**
4. Copie:
   - **Project URL** (ex: `https://abc123.supabase.co`)
   - **Chave service_role** (NÃO a anon key — mantenha esta secreta!)

## Passo 3: Definir Variáveis de Ambiente

Crie `~/.hermes/secrets.env`:

```bash
cat > ~/.hermes/secrets.env << 'EOF'
# Provedor LLM
OPENROUTER_API_KEY="***"

# Supabase
SUPABASE_URL="https://seu-projeto.supabase.co"
SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOi...VCJ9..."
EOF
```

## Passo 4: Aplicar Migrations do Supabase

```bash
# Instalar Supabase CLI
npm install -g supabase
# ou: brew install supabase/tap/supabase

# Fazer login e vincular seu projeto
supabase login
supabase link --project-ref seu-project-ref

# Aplicar as migrations do onboarding
# Clone este repositório primeiro, depois:
cd hermes-agent-onboarding
supabase db push --linked
```

Isso cria as 6 tabelas base: `user_profiles`, `user_preferences`, `user_mbti`, `user_style`, `user_relations`, `user_beliefs`.

## Passo 5: Verificar se Tudo Funciona

```bash
# Testar LLM
hermes chat "Olá, você está configurado?"

# Testar Supabase
source ~/.hermes/secrets.env
curl -s "$SUPABASE_URL/rest/v1/" -H "apikey: $SUPABASE_SERVICE_ROLE_KEY"
```

## Próximos Passos

Prossiga para [Setup Supabase](02-SUPABASE_ptBR.md) para configuração detalhada do banco,
ou pule para [Executando o Onboarding](03-RUNNING_ptBR.md) para iniciar o meta-skill.
