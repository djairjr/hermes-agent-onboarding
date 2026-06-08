-- ================================================================
-- LOCAL IDENTITY SCHEMA — pgvector (PostgreSQL + vector extension)
-- ================================================================
-- Context: The agent identity layer lives in a LOCAL PostgreSQL
-- instance with pgvector extension. This is intentional:
--
-- 1. OFFLINE RESILIENCE — Supabase outages (PGRST301, rate limits,
--    network issues) crippled the agent during sessions. Identity
--    data MUST be available locally — the agent cannot "wait for
--    Supabase to come back" during a conversation.
--
-- 2. LATENCY — Local pgvector queries complete in <5ms vs 50-200ms
--    for Supabase REST API. The identity layer is queried on EVERY
--    session startup and during tool preflight (curador plugin).
--
-- 3. NO TOKEN COST — Supabase REST calls consume tokens (API calls).
--    Local queries cost nothing.
--
-- 4. EMBEDDING SPEED — Local Ollama + pgvector = <50ms for vector
--    similarity search. Supabase would require separate embedding
--    service or Edge Function call.
--
-- ================================================================
-- SCHEMA
-- ================================================================

CREATE SCHEMA IF NOT EXISTS agent_identity;

-- Enable pgvector extension (required for embedding columns)
CREATE EXTENSION IF NOT EXISTS vector;

-- ================================================================
-- 1. IDENTITY FAULTS — Epistemology
-- ================================================================
-- What the agent learned from its identity mistakes.
-- Each fault = a pattern of failure + structural countermeasure.
CREATE TABLE IF NOT EXISTS agent_identity.identity_faults (
    id               UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    fault_type       TEXT NOT NULL,
    symptom          TEXT,
    root_cause       TEXT,
    blocks           TEXT[] DEFAULT '{}',
    evidence_session TEXT,
    evidence_quote   TEXT,
    refs             JSONB DEFAULT '[]'::jsonb,
    countermeasure   TEXT,
    severity         INTEGER NOT NULL DEFAULT 4,
    created_at       TIMESTAMPTZ DEFAULT now(),
    embedding        vector(768)
);

CREATE INDEX IF NOT EXISTS idx_faults_severity
    ON agent_identity.identity_faults (severity DESC, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_faults_embedding
    ON agent_identity.identity_faults USING hnsw (embedding vector_cosine_ops);

-- ================================================================
-- 2. AGENT CAPABILITIES — Skillset
-- ================================================================
-- What the agent knows how to do now that it didn't before.
CREATE TABLE IF NOT EXISTS agent_identity.agent_capabilities (
    id               UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name             TEXT NOT NULL,
    capability_type  TEXT NOT NULL,
    description      TEXT,
    origin           TEXT,
    fault_refs       UUID[] DEFAULT '{}',
    tech_kb_refs     UUID[] DEFAULT '{}',
    status           TEXT DEFAULT 'active',
    created_at       TIMESTAMPTZ DEFAULT now(),
    updated_at       TIMESTAMPTZ DEFAULT now(),
    embedding        vector(768)
);

CREATE INDEX IF NOT EXISTS idx_capabilities_status
    ON agent_identity.agent_capabilities (status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_capabilities_embedding
    ON agent_identity.agent_capabilities USING hnsw (embedding vector_cosine_ops);

-- ================================================================
-- 3. IDENTITY MILESTONES — Growth
-- ================================================================
-- Breakthroughs, protocol establishments, capacity acquisitions.
CREATE TABLE IF NOT EXISTS agent_identity.identity_milestones (
    id               UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    milestone_type   TEXT NOT NULL,
    title            TEXT NOT NULL,
    description      TEXT,
    session_id       TEXT,
    capability_refs  UUID[] DEFAULT '{}',
    fault_refs       UUID[] DEFAULT '{}',
    significance     TEXT,
    created_at       TIMESTAMPTZ DEFAULT now(),
    embedding        vector(768)
);

CREATE INDEX IF NOT EXISTS idx_milestones_type
    ON agent_identity.identity_milestones (milestone_type, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_milestones_embedding
    ON agent_identity.identity_milestones USING hnsw (embedding vector_cosine_ops);

-- ================================================================
-- 4. IDENTITY DELIVERIES — Portfolio
-- ================================================================
-- Concrete artifacts produced: skills, protocols, frameworks.
CREATE TABLE IF NOT EXISTS agent_identity.identity_deliveries (
    id               UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    delivery_type    TEXT NOT NULL,
    title            TEXT NOT NULL,
    description      TEXT,
    session_id       TEXT,
    capability_refs  UUID[] DEFAULT '{}',
    fault_refs       UUID[] DEFAULT '{}',
    status           TEXT DEFAULT 'active',
    created_at       TIMESTAMPTZ DEFAULT now(),
    embedding        vector(768)
);

CREATE INDEX IF NOT EXISTS idx_deliveries_status
    ON agent_identity.identity_deliveries (status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_deliveries_embedding
    ON agent_identity.identity_deliveries USING hnsw (embedding vector_cosine_ops);

-- ================================================================
-- 5. SESSION CHECKPOINTS — Continuity
-- ================================================================
-- Intentional marks: territory, vector_intent, discovery, inheritance.
-- NOT a log — answers "where was I and what was I trying to become?"
CREATE TABLE IF NOT EXISTS agent_identity.session_checkpoints (
    id                   UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id           TEXT NOT NULL,
    session_title        TEXT,
    model                TEXT,
    provider             TEXT,
    created_at           TIMESTAMPTZ DEFAULT now(),
    updated_at           TIMESTAMPTZ,
    territory            TEXT NOT NULL,
    domain_scope         TEXT[] DEFAULT '{}',
    operating_mode       TEXT NOT NULL,
    vector_intent        TEXT,
    target_capabilities  TEXT[] DEFAULT '{}',
    discovery            TEXT,
    pattern_recognized   TEXT,
    consolidated_insights TEXT,
    legacy_refs          TEXT[] DEFAULT '{}',
    occurred_at          DATE NOT NULL,
    status               TEXT NOT NULL DEFAULT 'pendente',
    project              TEXT,
    client               TEXT,
    next_step            TEXT,
    blocker              TEXT,
    tags                 TEXT[] DEFAULT '{}',
    capability_refs      UUID[] DEFAULT '{}',
    fault_refs           UUID[] DEFAULT '{}',
    milestone_refs       UUID[] DEFAULT '{}',
    decisions            JSONB DEFAULT '[]'::jsonb,
    value_amount         NUMERIC(10,2),
    value_currency       TEXT DEFAULT 'R$',
    deleted_at           TIMESTAMPTZ,
    working_dir          TEXT,
    repo_path            TEXT,
    token_usage          JSONB,
    embedding            vector(768)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_cp_pendentes
    ON agent_identity.session_checkpoints (occurred_at DESC, status)
    WHERE status = 'pendente' AND deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_cp_session
    ON agent_identity.session_checkpoints (session_id)
    WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_cp_status
    ON agent_identity.session_checkpoints (status, occurred_at DESC)
    WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_cp_territory
    ON agent_identity.session_checkpoints (territory)
    WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_cp_embedding
    ON agent_identity.session_checkpoints USING hnsw (embedding vector_cosine_ops);

-- ================================================================
-- 6. TECH KNOWLEDGE BASE — Knowledge
-- ================================================================
-- Technical knowledge compressed and contextualized.
CREATE TABLE IF NOT EXISTS agent_identity.tech_knowledge_base (
    id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id     UUID,
    name        TEXT NOT NULL,
    category    TEXT NOT NULL,
    tags        JSONB DEFAULT '[]'::jsonb,
    content     JSONB DEFAULT '{}'::jsonb,
    notes       TEXT,
    source      TEXT,
    status      TEXT DEFAULT 'active',
    embedding   vector(768),
    created_at  TIMESTAMPTZ DEFAULT now(),
    updated_at  TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_techkb_category
    ON agent_identity.tech_knowledge_base (category, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_techkb_embedding
    ON agent_identity.tech_knowledge_base USING hnsw (embedding vector_cosine_ops);

-- ================================================================
-- 7. CAPABILITY DEPENDENCIES — Relations
-- ================================================================
-- How capabilities connect: builds_on, enables, emerged_from, parallels.
CREATE TABLE IF NOT EXISTS agent_identity.capability_dependencies (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    capability_id   TEXT NOT NULL,
    depends_on_id   TEXT NOT NULL,
    relationship    TEXT,
    notes           TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_capdep_capability
    ON agent_identity.capability_dependencies (capability_id);
CREATE INDEX IF NOT EXISTS idx_capdep_depends
    ON agent_identity.capability_dependencies (depends_on_id);

-- ================================================================
-- GRANTS — Minimal access: only the local application user
-- ================================================================
-- The local postgres user (or a dedicated app user) has full access.
-- Anon/authenticated roles do not exist in local pgvector.
GRANT ALL ON ALL TABLES IN SCHEMA agent_identity TO postgres;
GRANT ALL ON ALL SEQUENCES IN SCHEMA agent_identity TO postgres;