"""Curator plugin configuration."""

# pgvector local connection
PG_HOST = "localhost"
PG_PORT = 5433
PG_DB = "openbrain"
PG_USER = "postgres"
PG_PASS = "4ut0l1b3r4c40"

# Ollama embedding
OLLAMA_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "nomic-embed-text-v2-moe"

# Similarity thresholds
FAULT_THRESHOLD = 0.80     # identity_faults match → block tool
CP_THRESHOLD = 0.75        # session_checkpoints match → annotate, don't block
TECHKB_THRESHOLD = 0.70    # tech_kb match → annotate, don't block

# Cache
LRU_SIZE = 128
LRU_TTL_SECONDS = 60

# Tool call log
TOOL_CALL_LOG_TABLE = "agent_identity.tool_call_log"

# Which tools to skip (always let through)
SKIP_TOOLS = {"browser_navigate", "browser_snapshot", "browser_click",
              "browser_type", "terminal", "read_file", "search_files",
              "memory", "todo", "session_search"}
