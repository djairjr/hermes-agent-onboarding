---
name: stage-3-financial
version: 1.0.0
description: >
  Stage 3 of the meta-skill agent-onboarding. Financial profile based on MBTI +
  bank CSV import + goal setting + strategies adapted to
  personality type. Uses MCP tools supabase-finance + supabase-worklog.
tags: [financial, mbti, csv, goals, stage-3, meta-skill]
---

# Stage 3 — Financial Profile

## Purpose

This stage builds the user's financial profile from 4 layers:
1. **Data import** (bank CSV → Supabase)
2. **MBTI × Finance profile** (financial behavior by personality type)
3. **Financial goals** (short, medium, and long term)
4. **Adapted strategies** tailored to profile + goals

## Skill Files

| File | Function |
|------|---------|
| `mbti_financial_profiles.py` | 16 MBTI financial profiles in English with assess_financial_personality() |
| `csv_importer.py` | Bank CSV importer with automatic format detection |

---

## PART 1 — CONVERSATIONAL FLOW

### 3A: CSV Import

```
"Would you like me to analyze your bank statements?
I can read CSVs from Nubank, Itaú, Inter, Caixa.

If you want to:
1. Export your statement as CSV
2. Send me the file (or paste the content)
3. I'll show a preview and you confirm before importing
```

**Preview mode always first:**

```
Detected format: Nubank
Period: 01/01/2026 to 01/31/2026
Transactions: 45
  Income: R$ 8,500.00
  Expenses: R$ 5,230.00
  Period balance: R$ 3,270.00

Detected categories:
  Food: 12 transactions
  Transportation: 8 transactions
  Subscriptions: 4 transactions

Import? (y/N):
```

### 3B: MBTI × Finance Profile

After MBTI is registered (from Stage 1C), ask:

```
"Your MBTI type is {type_code} — {name_en_US}.
Would you like me to analyze how this influences your finances?

I can show you:
• Your financial profile based on MBTI
• Strengths and weaknesses with money
• How you tend to save, spend, and invest
• Specific recommendations for your type

Shall we?"
```

Use `mbti_financial_profiles.py`:

```python
from mbti_financial_profiles import get_profile, assess_financial_personality

profile = get_profile(type_code)
# Display: strengths, weaknesses, saving_style, spending_style, etc.

# If the user answered financial questions:
result = assess_financial_personality(answers, type_code)
# Display observations + recommendations
```

**Questions to calibrate the profile:**
```
1. "How do you save? Automatically, manually, or when there's leftover?"
2. "Your financial risk tolerance? High, medium, or low?"
3. "What makes you spend the most? Tools, social experiences, comfort?"
4. "Which phrase best describes your relationship with money?
   A) Money is freedom
   B) Money is security
   C) Money is a tool
   D) Money is for living"
```

### 3C: Financial Goals

```
"Now, let's set financial goals.

Short term (6 months): what do you want to achieve?
Medium term (2 years): what's the next step?
Long term (5+ years): what's your horizon?

Examples:
• Short: pay off credit card debt, R$ 10,000 emergency fund
• Medium: down payment on a property, change cars
• Long: financial independence, retirement at 55
```

Register via MCP `mcp_supabase_finance_add_goal()`.

### 3D: Adapted Strategies

Combine MBTI + goals into recommendations:

```
"Based on your INTJ profile (Architect) and your goals:

✅ What already works for you:
• Strategic planning — you already think long term
• Discipline to follow budgets

⚠️ What needs attention:
• You may ignore emotional costs in financial decisions
• Impulsive spending on high-impact projects

📋 Recommendations:
1. Automate 30% of income toward investments
2. 12-month emergency fund
3. 10% for 'strategic projects'
4. Monthly net worth spreadsheet
5. 5% for 'free spending'

Would you like me to implement any of these strategies?"
```

Use `assess_financial_personality()` with the user's answers + type_code.

---

## PART 2 — AVAILABLE MCP TOOLS

Stage 3 uses the following MCP tools from the `supabase-finance` extension:

| Tool | Function |
|------|---------|
| `mcp_supabase_finance_list_accounts` | List bank accounts |
| `mcp_supabase_finance_add_account` | Add account |
| `mcp_supabase_finance_add_transaction` | Register transaction |
| `mcp_supabase_finance_list_transactions` | List transactions with filters |
| `mcp_supabase_finance_add_goal` | Add financial goal |
| `mcp_supabase_finance_list_goals` | List goals |
| `mcp_supabase_finance_list_categories` | List categories |
| `mcp_supabase_finance_get_dashboard` | Financial dashboard |
| `mcp_supabase_finance_set_budget` | Set monthly budget |
| `mcp_supabase_worklog_log_work` | Log work with value |
| `mcp_supabase_worklog_get_month` | Monthly work + income summary |

---

## PART 3 — HOW TO INVOKE (from agent-onboarding)

```python
# 1. Load this skill
# 2. Follow conversational flow 3A → 3B → 3C → 3D
# 3. Use mbti_financial_profiles.py for MBTI × finance profile
# 4. Use csv_importer.py to import statements (preview → confirm → import)
# 5. Register goals via MCP tools
# 6. Save user_profiles.financial_profile_completed = true
```

---

## Verification

1. MBTI × Finance profile loads for all 16 types
2. CSV preview shows correct summary before importing
3. Transactions are imported via REST API with automatic categorization
4. Goals are registered via MCP tools

## Pitfalls

1. **NEVER import CSV without user preview/confirmation**
2. **NEVER store raw CSV in Supabase or on disk** — process in memory only
3. **NEVER log full financial data** — summary only
4. **MBTI is guidance, not deterministic** — the user's financial profile may differ from type
5. **If user has no Supabase account configured, offer text-based analysis instead of registering**
