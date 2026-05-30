# Protocolo de Segurança — Stack de Onboarding do Hermes Agent

**Severidade: CRÍTICA.** Estas não são sugestões. Cada item aqui é uma vulnerabilidade que deve ser fechada antes de qualquer uso em produção ou público.

---

## Camada 1 — Acesso a Dados no Supabase

### 1.1 Proteção da Chave Service Role

A chave service_role tem **acesso total ao banco de dados**. Perdê-la significa perder tudo.

| Regra | Por quê |
|-------|---------|
| NUNCA comitar no git | Mesmo em repositórios privados. Acidentalmente tornar público = violação. |
| NUNCA no config.yaml | Config.yaml é frequentemente compartilhado ou copiado em backup. |
| APENAS em ~/.hermes/secrets.env | Com `redact_secrets: true` no config.yaml. |
| NUNCA em browser/JS | Chave service_role no frontend = violação instantânea. |
| ROTACIONAR se houver suspeita de exposição | Regenerar imediatamente no painel do Supabase. |

**Status atual:** ✅ Chave service_role está apenas em secrets.env. Não está em config.yaml. Não está no git.

### 1.1b ⚠️ Comunicado Supabase (30/05/2026): GRANTs Explícitos Agora Obrigatórios

Desde 30 de maio de 2026, novas tabelas no schema `public` não são mais
expostas ao Data API (PostgREST) automaticamente — nem mesmo para
`service_role`. Toda tabela precisa de um GRANT explícito.

```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON public.<tabela> TO service_role;
```

**Sintoma:** Edge Functions retornam `permission denied for table <tabela>`,
mesmo com RLS policy configurada. O PostgREST bloqueia no nível de tabela
antes de avaliar a RLS.

**Diagnóstico rápido:**
```sql
SELECT table_name FROM information_schema.tables WHERE table_schema='public'
EXCEPT
SELECT DISTINCT table_name FROM information_schema.role_table_grants
WHERE table_schema='public' AND grantee='service_role';
```

**Migration de referência:** `migrations/20260531090000_service_role_grants.sql`
no repositório do meta-skill. Aplica GRANTs a ~90 tabelas OB1 de uma vez.

### 1.2 RLS Deve Bloquear Tudo Exceto Service Role

**Problema:** Muitos projetos Supabase usam `auth.uid() = user_id` como política RLS. Isso funciona para usuários autenticados mas não faz NADA contra a chave service_role, que **bypasseia RLS completamente**.

**A única proteção contra roubo da chave service_role é: não perca a chave.**

Mas RLS ainda importa para:
- Chave anon (pública, pode ser extraída do frontend)
- JWTs de usuários autenticados

**Padrão RLS correto (já aplicado às tabelas user_*):**

```sql
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "service_role_only" ON public.user_profiles FOR ALL
  USING ((auth.jwt() ->> 'role') = 'service_role');
```

Isso significa:
- JWT service role → `auth.jwt() ->> 'role' = 'service_role'` → acesso concedido
- JWT anon → role é 'anon' → bloqueado
- JWT de usuário autenticado → role é 'authenticated' → bloqueado

### 1.3 GRANT Deve Ser Mínimo

**Problema:** `GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role` é amplo demais.

**Padrão correto:**

```sql
-- Conceder apenas o necessário, para tabelas específicas
GRANT SELECT, INSERT, UPDATE, DELETE ON public.user_profiles TO service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.user_preferences TO service_role;
-- ... por tabela

-- NUNCA conceder para anon
-- NUNCA conceder para authenticated a menos que você tenha auth de usuário
```

**Por que isso importa:** Se alguém roubar sua chave service_role mas você tiver GRANTs por tabela, o raio de explosão é limitado. `GRANT ALL ON ALL TABLES` significa uma chave = todas as tabelas.

**Status atual (tabelas user_*):** ✅ GRANT por tabela, sem wildcard.

### 1.4 Chave Anon Deve Ser Bloqueada no Nível do Schema

Por padrão, o Supabase concede `USAGE ON SCHEMA public TO anon`. Isso significa que a chave anon pode descobrir nomes de tabelas mesmo que o RLS bloqueie linhas.

```sql
-- Bloquear anon de sequer ver o schema
REVOKE USAGE ON SCHEMA public FROM anon;
REVOKE USAGE ON SCHEMA public FROM authenticated;
```

Ou no mínimo, não conceda acesso a tabelas para anon.

---

## Camada 2 — Segurança do Servidor MCP

### 2.1 Chave MCP na URL (config.yaml)

**Problema:** O config.yaml armazena chaves MCP como parâmetros de consulta em URLs:
```yaml
url: https://project.supabase.co/functions/v1/supabase-finance?key=abc123...
```

Se config.yaml for lido (backup, compartilhado, saída de debug), as chaves vazam.

**Mitigações:**
- `redact_secrets: true` no config.yaml mascara valores de env vars na saída
- NUNCA comitar config.yaml no git
- Fazer backup do config.yaml em /tmp/ com timestamp antes de editar
- Usar substituição de variável de ambiente: `${FINANCE_MCP_KEY}` em vez de literal

### 2.2 Verificação de Auth na Edge Function

**Padrão (financeiro):**
```typescript
const key = c.req.query("key") || c.req.header("x-access-key");
const expected = Deno.env.get("FINANCE_MCP_KEY");
if (!key || key !== expected) return c.json({ error: "Unauthorized" }, 401);
```

**Problemas:**
- Comparação de chave NÃO é em tempo constante (ataque de timing possível, embora baixo risco)
- Chave na URL = registrada pelo Supabase, visível no histórico do navegador
- Preferir cabeçalho `x-access-key` apenas, não query param

**Correção:**
```typescript
// Aceitar APENAS via header, não query param
const key = c.req.header("x-access-key");
if (!key || key !== Deno.env.get("FINANCE_MCP_KEY")) {
  return c.json({ error: "Unauthorized" }, 401);
}
```

### 2.3 DEFAULT_USER_ID: Padrão Correto para Mono-Usuário

**Contexto:** Este stack foi projetado para **mono-usuário** — apenas uma pessoa
(Djair) acessa os dados através do agente Hermes.

**O padrão implementado:**
```typescript
const userId = Deno.env.get("DEFAULT_USER_ID");
// .insert({ user_id: userId, ... })
// .select().eq("user_id", userId)
```

Toda Edge Function lê `DEFAULT_USER_ID` do ambiente e filtra todas as queries
por ele. Isso garante isolamento horizontal no nível de linha.

**Por que isso é seguro para mono-usuário:**

| Mecanismo | O que protege |
|-----------|---------------|
| MCP key (64 hex, `openssl rand -hex 32`) | Autenticação na Edge Function |
| DEFAULT_USER_ID | Filtragem por usuário nas queries |
| RLS `service_role_only` | Bloqueia anon e authenticated |
| GRANT por tabela | Limita raio de explosão |

A MCP key é a única porta de entrada. Se ela vazar, tanto faz se o
`user_id` está no env ou no JWT — o atacante acessa os mesmos dados
(mono-usuário). **Para mono-usuário, DEFAULT_USER_ID é o padrão correto.**
Não adiciona vulnerabilidade e reduz drasticamente a complexidade.

**E se no futuro for multi-usuário?**

Nesse cenário, DEFAULT_USER_ID fixo no env não serve. A abordagem correta
seria JWT por request:

```typescript
// Cada request carrega user_id no payload de um JWT assinado
// A Edge Function verifica a assinatura, extrai user_id, filtra queries
```

**Custo da troca para JWT:**

| Fator | DEFAULT_USER_ID | JWT por request |
|-------|----------------|-----------------|
| Complexidade | 0 — ler env var | Alta — signing, verification, rotation |
| Carga operacional | 0 | Gerenciar expiração e renovação |
| Segurança (mono-usuário) | Idêntica | Idêntica |
| Preparo para multi-usuário | Nenhum | Bom |

Para mono-usuário, a troca agregaria zero segurança e complexidade
desnecessária. A recomendação é manter DEFAULT_USER_ID enquanto o
stack for mono-usuário, e migrar para JWT apenas se houver necessidade
real de multi-usuário no futuro.

---

## Camada 3 — Dados Financeiros (Maior Sensibilidade)

Dados financeiros são os mais sensíveis do stack. Uma violação aqui significa
números de contas bancárias, saldos, transações — tudo.

### 3.1 RLS de Tabelas Financeiras

**Estado atual:** ✅ Corrigido. Todas as 7 tabelas financeiras usam política
`service_role_only` — `(auth.jwt() ->> 'role') = 'service_role'`. GRANTs por
tabela, sem wildcard.

**Como funciona:** A RLS bloqueia qualquer role que não seja service_role.
O DEFAULT_USER_ID filtra as queries no nível da aplicação (dentro da Edge
Function). As duas camadas se complementam:
- RLS: bloqueia acesso externo (anon, authenticated)
- DEFAULT_USER_ID: isola dados do usuário (horizontal) dentro do service_role

### 3.2 Sem Dados Financeiros em Logs

- Nunca registrar descrições de transações, números de conta ou saldos
- Se depurar, mascarar: `****1234` para números de conta
- O `redact_secrets` do agente já lida com env vars

### 3.3 Segurança na Importação CSV

Quando um usuário fornece CSVs de extrato bancário:

1. Processar em memória apenas — NUNCA escrever conteúdo CSV no disco
2. NUNCA armazenar dados CSV brutos no Supabase — apenas transações analisadas e estruturadas
3. Se CSV precisar ser salvo: criptografar, armazenar fora do git, limpar após importação
4. Avisar o usuário: "Processo CSVs em memória. Eles não são armazenados. Pronto?"

---

## Camada 4 — Wrapper & Ambiente

### 4.1 Proteção do secrets.env

```bash
# CORRETO: source e use env vars
source ~/.hermes/secrets.env
curl -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}"

# NUNCA:
cat ~/.hermes/secrets.env          # redact_secrets mascara valores, mas ainda é má prática
grep SUPABASE ~/.hermes/secrets.env  # mesma coisa
read_file ~/.hermes/secrets.env     # saída da ferramenta hermes é registrada
```

### 4.2 Backups do config.yaml

Antes de qualquer edição:
```bash
cp ~/.hermes/config.yaml /tmp/hermes_config_$(date +%Y%m%d_%H%M%S)_BACKUP.yaml
cp ~/.hermes/secrets.env /tmp/hermes_secrets_$(date +%Y%m%d_%H%M%S)_BACKUP.env
```

Backups vão para /tmp/ (não persistentes). **Delete após confirmar que a edição funcionou.**

### 4.3 Sem Senha Sudo no env

NUNCA armazene senhas sudo em secrets.env. Use `clarify()` para cada operação
sudo. O usuário digita a senha manualmente se necessário.

---

## Camada 5 — Git & Repositório Público

### 5.1 .gitignore Deve Incluir

```gitignore
# Secrets
.env
.env.*
secrets.env
*.pem
*.key

# Config com chaves
config.yaml

# Supabase
.supabase/
supabase/.branches/
*.local*

# Arquivos do SO
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
```

### 5.2 Nunca Comitar Dados Reais

- Migration SQL é ok (apenas schemas, sem dados)
- Exemplos no README devem usar placeholders: `seu-projeto.supabase.co`
- Capturas de tela não devem mostrar dados reais, números de conta, orçamentos
- Arquivos CSV de exemplo devem ser sintéticos, não extratos bancários reais

### 5.3 Template de Ambiente para o Repositório

Incluir um arquivo `secrets.env.example` com valores placeholders:
```bash
# Copie para ~/.hermes/secrets.env e preencha suas chaves
SUPABASE_URL="https://seu-projeto.supabase.co"
SUPABASE_SERVICE_ROLE_KEY="sua-chave-service-role"
FINANCE_MCP_KEY="sua-chave-finance-mcp"
```

---

## Checklist de Vulnerabilidades (Executar Antes de Qualquer Lançamento Público)

- [x] Todas as tabelas usam política RLS `service_role_only` (corrigido)
- [x] Sem `GRANT ALL ON ALL TABLES` — apenas grants por tabela (corrigido)
- [x] `DEFAULT_USER_ID` é o padrão correto — stack mono-usuário
- [ ] Chaves MCP aceitas via header apenas, não query param
- [x] Sem dados financeiros em logs ou histórico git
- [x] .gitignore bloqueia todos os arquivos secret/config
- [x] secrets.env.example no repositório (secrets.env real está no .gitignore)
- [ ] Chave anon não pode acessar nenhuma tabela (USAGE no schema revogado)
- [x] Importação CSV é apenas em memória, sem persistência em disco
- [x] GRANTs service_role para todas as tabelas acessadas por MCP (corrigido 31/05)

---

## Status Atual (31 de Maio de 2026)

| Item | Status | Notas |
|------|--------|-------|
| Tabelas user_* RLS | ✅ service_role_only | Padrão correto |
| Tabelas user_* GRANT | ✅ Por tabela | Grants específicos |
| Tabelas financeiras RLS | ✅ service_role_only | Corrigido — antes usava auth.uid() |
| Tabelas financeiras GRANT | ✅ Por tabela | Corrigido — antes era wildcard |
| Service role GRANTs MCP | ✅ ~90 tabelas | Migration 20260531090000 (corrigido 31/05) |
| Chave MCP na URL | ⚠️ Header + query param | Aceitar apenas header |
| DEFAULT_USER_ID | ✅ Padrão correto para mono-usuário | Stack é mono-usuário |
| secrets.env no git | ✅ Não | Bloqueado pelo .gitignore |
| config.yaml no git | ✅ Não | Bloqueado pelo .gitignore |
| secrets.env.example | ✅ Criado | Presente no repositório |
| Anon/authenticated REVOKE | ❌ Pendente | REVOKE USAGE ON SCHEMA public |

## Assinatura GPG de Commits

Todos os commits neste repositório são assinados com a chave GPG
`8DD2DAD7756068C9` (djair.jr@gmail.com).

Para verificar: `git log --show-signature`
