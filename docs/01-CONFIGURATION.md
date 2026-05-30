# Hermes Configuration

After installing Hermes Agent, you need to configure at least one LLM provider and a Supabase project.

## Configuration File

Hermes stores its configuration in `~/.hermes/config.yaml`. On first run, a default config is created.

## Step 1: Set Up an LLM Provider

### Option A: OpenRouter (recommended for beginners)

```bash
# Set your API key
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"

# Create a basic config
hermes config set provider openrouter
hermes config set model "anthropic/claude-sonnet-4"
```

### Option B: Ollama (local, free)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull gemma3:12b

# Configure Hermes to use it
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

### Option C: OpenAI / Anthropic directly

```bash
export OPENAI_API_KEY="sk-your-key"
hermes config set provider openai
hermes config set model "gpt-4o"
```

## Step 2: Create a Supabase Project

1. Go to [supabase.com](https://supabase.com/) and create a free account
2. Create a new project (any name, any region)
3. From your project dashboard, go to **Project Settings → API**
4. Copy:
   - **Project URL** (e.g., `https://abc123.supabase.co`)
   - **service_role key** (NOT the anon key — keep this secret!)

## Step 3: Set Environment Variables

Create `~/.hermes/secrets.env`:

```bash
cat > ~/.hermes/secrets.env << 'EOF'
# LLM Provider
OPENROUTER_API_KEY="sk-or-v1-your-key"

# Supabase
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
EOF
```

## Step 4: Apply Supabase Migrations

```bash
# Install Supabase CLI
npm install -g supabase
# or: brew install supabase/tap/supabase

# Login and link your project
supabase login
supabase link --project-ref your-project-ref

# Apply the onboarding migrations
# Clone this repo first, then:
cd hermes-agent-onboarding
supabase db push --linked
```

This creates the 6 base tables: `user_profiles`, `user_preferences`, `user_mbti`, `user_style`, `user_relations`, `user_beliefs`.

## Step 5: Verify Everything Works

```bash
# Test LLM
hermes chat "Hello, are you configured?"

# Test Supabase
source ~/.hermes/secrets.env
curl -s "$SUPABASE_URL/rest/v1/" -H "apikey: $SUPABASE_SERVICE_ROLE_KEY"
```

## Next Steps

Proceed to [Supabase Setup](02-SUPABASE.md) for detailed database configuration,
or jump to [Running Onboarding](03-RUNNING.md) to start the meta-skill.
