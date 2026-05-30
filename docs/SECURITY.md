# Security Protocol — Hermes Agent Onboarding Stack

**Severity: CRITICAL.** These are not suggestions. Every item here is a
vulnerability that must be closed before any production or public use.

---

## Layer 1 — Supabase Data Access

### 1.1 Service Role Key Protection

The service_role key has **full database access**. Losing it means losing
everything.

| Rule | Why |
|------|-----|
| NEVER commit to git | Even in private repos. Accidentally making public = breach. |
| NEVER in config.yaml | Config.yaml is often shared or backed up. |
| ONLY in ~/.hermes/secrets.env | With `redact_secrets: true` in config.yaml. |
| NEVER in browser/JS | Service_role key in frontend = instant breach. |
| ROTATE if suspected exposed | Regenerate in Supabase dashboard immediately. |

**Current status:** ✅ Service_role key is in secrets.env only. Not in config.yaml.
Not in git.

### 1.1b ⚠️ Supabase Notice (30 May 2026): Explicit GRANTs Now Required

As of May 30, 2026, new tables in the `public` schema are no longer
automatically exposed to the Data API (PostgREST) — not even for
`service_role`. Every table needs an explicit GRANT.

```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON public.<table> TO service_role;
```

**Symptom:** Edge Functions return `permission denied for table <table>`,
even with RLS policy configured. PostgREST blocks at the table level
before evaluating RLS.

**Fast diagnosis:**
```sql
SELECT table_name FROM information_schema.tables WHERE table_schema='public'
EXCEPT
SELECT DISTINCT table_name FROM information_schema.role_table_grants
WHERE table_schema='public' AND grantee='service_role';
```

**Reference migration:** `migrations/20260531090000_service_role_grants.sql`
in the meta-skill repository. Applies GRANTs to ~90 OB1 tables at once.

### 1.2 RLS Must Block Everything Except Service Role

**Problem:** Many Supabase projects use `auth.uid() = user_id` as the RLS policy.
This works for authenticated users but does NOTHING against the service_role key,
which bypasseis RLS entirely.

**The only protection against service_role key theft is: don't lose the key.**

But RLS still matters for:
- Anon key (public, can be extracted from frontend)
- Authenticated user JWTs

**Correct RLS pattern (already applied to user_* tables):**

```sql
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "service_role_only" ON public.user_profiles FOR ALL
  USING ((auth.jwt() ->> 'role') = 'service_role');
```

This means:
- Service role JWT → `auth.jwt() ->> 'role' = 'service_role'` → access granted
- Anon JWT → role is 'anon' → blocked
- Auth'd user JWT → role is 'authenticated' → blocked

### 1.3 GRANT Must Be Minimal

**Problem:** `GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role` is too broad.

**Correct pattern:**

```sql
-- Grant only what's needed, to specific tables
GRANT SELECT, INSERT, UPDATE, DELETE ON public.user_profiles TO service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.user_preferences TO service_role;
-- ... per table

-- NEVER grant to anon
-- NEVER grant to authenticated unless you have user auth
```

**Why this matters:** If someone steals your service_role key but you have
per-table GRANTs, the blast radius is limited. `GRANT ALL ON ALL TABLES`
means one key = every table.

**Current status (user_* tables):** ✅ GRANT per table, no wildcard.
**Current status (financial tables):** ❌ `GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role` — wildcard. Must be fixed.

### 1.4 Anon Key Must Be Blocked at Schema Level

By default, Supabase grants `USAGE ON SCHEMA public TO anon`. This means
the anon key can discover table names even if RLS blocks rows.

```sql
-- Block anon from even seeing the schema
REVOKE USAGE ON SCHEMA public FROM anon;
REVOKE USAGE ON SCHEMA public FROM authenticated;
```

Or at minimum, don't grant table access to anon.

---

## Layer 2 — MCP Server Security

### 2.1 MCP Key in URL (config.yaml)

**Problem:** The config.yaml stores MCP keys as query parameters in URLs:
```yaml
url: https://project.supabase.co/functions/v1/supabase-finance?key=abc123...
```

If config.yaml is read (backup, shared, debug output), keys leak.

**Mitigations:**
- `redact_secrets: true` in config.yaml masks env var values in output
- NEVER commit config.yaml to git
- Backup config.yaml to /tmp/ with timestamp before editing
- Use environment variable substitution: `${FINANCE_MCP_KEY}` instead of literal

### 2.2 Edge Function Auth Check

**Pattern (finance):**
```typescript
const key = c.req.query("key") || c.req.header("x-access-key");
const expected = Deno.env.get("FINANCE_MCP_KEY");
if (!key || key !== expected) return c.json({ error: "Unauthorized" }, 401);
```

**Issues:**
- Key comparison is NOT constant-time (timing attack possible, though low risk)
- Key in URL query string = logged by Supabase, visible in browser history
- Prefer `x-access-key` header only, not query param

**Fix:**
```typescript
// Accept ONLY via header, not query param
const key = c.req.header("x-access-key");
if (!key || key !== Deno.env.get("FINANCE_MCP_KEY")) {
  return c.json({ error: "Unauthorized" }, 401);
}
```

### 2.3 DEFAULT_USER_ID: Correct Pattern for Single-User

**Context:** This stack is designed for **single-user** — only one person
(Djair) accesses data through the Hermes Agent.

**The implemented pattern:**
```typescript
const userId = Deno.env.get("DEFAULT_USER_ID");
// .insert({ user_id: userId, ... })
// .select().eq("user_id", userId)
```

Every Edge Function reads `DEFAULT_USER_ID` from the environment and
filters all queries through it. This provides row-level horizontal
isolation.

**Why this is safe for single-user:**

| Mechanism | What it protects |
|-----------|-----------------|
| MCP key (64 hex, `openssl rand -hex 32`) | Edge Function authentication |
| DEFAULT_USER_ID | Per-user query filtering |
| RLS `service_role_only` | Blocks anon and authenticated |
| Per-table GRANT | Limits blast radius |

The MCP key is the only entry point. If it leaks, it doesn't matter
whether `user_id` is in the env or in a JWT — the attacker accesses the
same data (single-user). **For single-user, DEFAULT_USER_ID is the
correct pattern.** No vulnerability added, complexity drastically reduced.

**If multi-user is needed in the future:**

DEFAULT_USER_ID won't work. The correct approach would be per-request JWT:

```typescript
// Each request carries user_id in a signed JWT payload
// Edge Function verifies the signature, extracts user_id, filters queries
```

**Migration cost:**

| Factor | DEFAULT_USER_ID | JWT per request |
|--------|----------------|-----------------|
| Complexity | 0 — read env var | High — signing, verification, rotation |
| Operations | 0 | Manage expiration and renewal |
| Security (single-user) | Identical | Identical |
| Multi-user readiness | None | Good |

For single-user, the switch adds zero security at unnecessary complexity.
Keep DEFAULT_USER_ID. Migrate to JWT only if multi-user is truly needed.

---

## Layer 3 — Financial Data (Highest Sensitivity)

Financial data is the most sensitive in the stack. A breach here means
bank account numbers, balances, transactions — everything.

### 3.1 Financial Table RLS

**Current state:** ✅ Fixed. All 7 financial tables use `service_role_only`
policy — `(auth.jwt() ->> 'role') = 'service_role'`. Per-table GRANTs, no wildcard.

**How it works:** RLS blocks any role that isn't service_role.
DEFAULT_USER_ID filters queries at the application level (inside the Edge
Function). Two layers complement each other:
- RLS: blocks external access (anon, authenticated)
- DEFAULT_USER_ID: isolates user data (horizontal) within service_role

### 3.2 No Financial Data in Logs

- Never log transaction descriptions, account numbers, or balances
- If debugging, mask: `****1234` for account numbers
- The agent's `redact_secrets` already handles env vars

### 3.3 CSV Import Security

When a user provides bank statement CSVs:

1. Process in-memory only — NEVER write CSV content to disk
2. NEVER store raw CSV data in Supabase — only parsed, structured transactions
3. If CSV must be saved: encrypt, store outside git, purge after import
4. Warn user: "I process CSVs in memory. They are not stored. Ready?"

---

## Layer 4 — Wrapper & Environment

### 4.1 secrets.env Protection

```bash
# CORRECT: source and use env vars
source ~/.hermes/secrets.env
curl -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}"

# NEVER:
cat ~/.hermes/secrets.env          # redact_secrets masks values, but still bad practice
grep SUPABASE ~/.hermes/secrets.env  # same
read_file ~/.hermes/secrets.env     # hermes tool output is logged
```

### 4.2 config.yaml Backups

Before any edit:
```bash
cp ~/.hermes/config.yaml /tmp/hermes_config_$(date +%Y%m%d_%H%M%S)_BACKUP.yaml
cp ~/.hermes/secrets.env /tmp/hermes_secrets_$(date +%Y%m%d_%H%M%S)_BACKUP.env
```

Backups go to /tmp/ (not persistent). **Delete after confirming the edit works.**

### 4.3 No Sudo Password in env

NEVER store sudo passwords in secrets.env. Use `clarify()` for each sudo
operation. The user types the password manually if needed.

---

## Layer 5 — Git & Public Repo

### 5.1 .gitignore Must Include

```gitignore
# Secrets
.env
.env.*
secrets.env
*.pem
*.key

# Config with keys
config.yaml

# Supabase
.supabase/
supabase/.branches/
*.local*

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
```

### 5.2 Never Commit Real Data

- Migration SQL is fine (schemas only, no data)
- README examples should use placeholder values: `your-project.supabase.co`
- Screenshots must not show real data, account numbers, budgets
- Example CSV files must be synthetic, not real bank statements

### 5.3 Environment Template for Repo

Include a `secrets.env.example` file with placeholder values:
```bash
# Copy this to ~/.hermes/secrets.env and fill in your keys
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_SERVICE_ROLE_KEY="your-service-role-key"
FINANCE_MCP_KEY="your-finance-mcp-key"
```

---

## Vulnerability Checklist (Run Before Any Public Release)

- [x] All tables use `service_role_only` RLS policy (fixed)
- [x] No `GRANT ALL ON ALL TABLES` — per-table grants only (fixed)
- [x] `DEFAULT_USER_ID` is correct pattern — single-user stack
- [ ] MCP keys accepted via header only, not query param
- [x] No financial data in logs or git history
- [x] .gitignore blocks all secret/config files
- [x] secrets.env.example in repo (real secrets.env in .gitignore)
- [ ] Anon key cannot access any table (schema USAGE revoked)
- [x] CSV import is memory-only, no disk persistence
- [x] service_role GRANTs for all MCP-accessible tables (fixed 31 May)

---

## Current Status (31 May 2026)

| Item | Status | Notes |
|------|--------|-------|
| user_* tables RLS | ✅ service_role_only | Correct pattern |
| user_* tables GRANT | ✅ Per table | Specific grants |
| financial tables RLS | ✅ service_role_only | Fixed — was auth.uid() |
| financial tables GRANT | ✅ Per table | Fixed — was wildcard |
| service_role GRANTs MCP | ✅ ~90 tables | Migration 20260531090000 (fixed 31 May) |
| MCP key in URL | ⚠️ Both header + query param | Accept header only |
| DEFAULT_USER_ID | ✅ Correct for single-user | Stack is single-user |
| secrets.env in git | ✅ No | Blocked by .gitignore |
| config.yaml in git | ✅ No | Blocked by .gitignore |
| secrets.env.example | ✅ Created | Present in repository |
| Anon/authenticated REVOKE | ❌ Pending | REVOKE USAGE ON SCHEMA public |

## GPG Commit Signing

All commits in this repository are signed with GPG key
`8DD2DAD7756068C9` (djair.jr@gmail.com).

To verify: `git log --show-signature`


GPG key `6B67B080006EFB7F` — all commits signed.
