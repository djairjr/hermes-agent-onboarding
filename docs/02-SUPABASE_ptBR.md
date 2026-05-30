# Setup do Supabase

Este guia cobre a criação do seu projeto Supabase e aplicação das migrations de banco de dados necessárias para o meta-skill de onboarding.

## Criando um Projeto

1. Acesse [supabase.com](https://supabase.com/) → **Start your project**
2. Dê um nome (ex: "hermes-onboarding")
3. Defina uma senha segura para o banco (salve-a!)
4. Escolha uma região próxima a você
5. Clique em **Create new project**
6. Aguarde ~2 minutos para o banco provisionar

## Obtendo Suas Credenciais

Quando o projeto estiver pronto:

1. Vá em **Project Settings** (ícone de engrenagem) → **API**
2. Em **Project URL**, copie a URL (formato: `https://xxxxx.supabase.co`)
3. Em **Project API keys**, copie a **chave service_role** (NÃO a anon)
   - A chave service_role começa com `eyJhbGciOi...` e tem acesso total
   - **Nunca compartilhe esta chave** nem a envie para o versionamento

## Instalando o Supabase CLI

```bash
# Usando npm (recomendado)
npm install -g supabase

# Usando Homebrew (macOS)
brew install supabase/tap/supabase

# Usando apt (Linux)
# Baixe de: https://github.com/supabase/cli/releases
```

Verificar:
```bash
supabase --version
# Deve mostrar: 2.x.x
```

## Vinculando ao Seu Projeto

```bash
# Fazer login no Supabase
supabase login

# Será solicitado um Personal Access Token (PAT)
# Acesse: https://supabase.com/dashboard/account/tokens
# Crie um token e cole quando solicitado

# Vincular seu ambiente local ao projeto
supabase link --project-ref SEU_PROJECT_REF
```

Seu project ref é a parte da URL antes de `.supabase.co`:
```
URL:  https://abcdefghijklm.supabase.co
REF:  abcdefghijklm
```

## Aplicando Migrations

A partir do diretório do repositório `hermes-agent-onboarding`:

```bash
cd hermes-agent-onboarding
supabase db push --linked
```

Isso executa todas as migrations em `migrations/`, criando as 6 tabelas base:

- `user_profiles` — identidade, família, rotinas
- `user_preferences` — tom, autonomia, rastreamento financeiro
- `user_mbti` — 4 dimensões, tipo, características
- `user_style` — estilo de comunicação
- `user_relations` — pessoas-chave
- `user_beliefs` — valores e princípios

## Verificando as Tabelas

```bash
# Listar tabelas no schema public
supabase db query --linked "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'user_%'"

# Verificar se RLS está ativo
supabase db query --linked "SELECT tablename, rowsecurity FROM pg_catalog.pg_tables WHERE tablename LIKE 'user_%'"
```

Saída esperada: 6 tabelas, todas com `rowsecurity = true`.

## Modelo de Segurança

Todas as tabelas de onboarding usam Row-Level Security (RLS) com o seguinte modelo:

- **Chave service_role**: Acesso total (SELECT, INSERT, UPDATE, DELETE)
- **Chave anon**: Sem acesso (bloqueada por política RLS)
- **Usuários autenticados**: Sem acesso (bloqueado por política RLS)

A política verifica a claim do JWT:
```sql
(auth.jwt() ->> 'role') = 'service_role'
```

Isso garante que apenas o Hermes Agent (usando a chave service_role) possa ler ou escrever dados do usuário.

## Próximos Passos

Prossiga para [Executando o Onboarding](03-RUNNING_ptBR.md).
