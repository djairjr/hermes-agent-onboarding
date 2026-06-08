"""Curator plugin — agent identity layer preflight guard.

Intercepts tool calls before execution (pre_tool_call hook), queries the
agent identity layer (pgvector local) and blocks tools that match known
identity faults. Logs all tool calls to tool_call_log for async consolidation.

Hooks:
  pre_tool_call  — consult pgvector (faults, checkpoints, tech_kb)
  post_tool_call — log tool execution to tool_call_log

Dependencies:
  - Local PostgreSQL with pgvector (openbrain-postgres:5433)
  - Ollama with nomic-embed-text-v2-moe for embeddings
  - Tables: agent_identity.identity_faults, session_checkpoints,
            tech_knowledge_base, tool_call_log
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from . import preflight, logger as _logger_mod

logger = logging.getLogger(__name__)

# Track whether pgvector is available (checked once on register)
_pgvector_available = None


def _check_pgvector() -> bool:
    """Check if pgvector is accessible. Cached after first check."""
    global _pgvector_available
    if _pgvector_available is not None:
        return _pgvector_available

    try:
        from .queries import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        _pgvector_available = True
        logger.info("pgvector available — curator active")
    except Exception as e:
        _pgvector_available = False
        logger.warning("pgvector unavailable — curator inactive: %s", e)
    return _pgvector_available


def register(ctx):
    """Register curator hooks. Fails open if pgvector is unavailable."""
    if not _check_pgvector():
        return

    ctx.register_hook("pre_tool_call", _on_pre_tool_call)
    ctx.register_hook("post_tool_call", _on_post_tool_call)
    logger.info("curator hooks registered")


def _on_pre_tool_call(tool_name: str = None, args: dict = None,
                       session_id: str = None, task_id: str = None,
                       tool_call_id: str = None, **kwargs) -> Dict | None:
    """pre_tool_call handler."""
    result = preflight.check(
        tool_name=tool_name,
        args=args,
        session_id=session_id,
        task_id=task_id,
        tool_call_id=tool_call_id,
    )

    # Store context for post hook
    if tool_call_id:
        fault_ref = result.get("fault_ref") if isinstance(result, dict) else None
        _logger_mod.set_context(tool_call_id, fault_ref=fault_ref)

    return result


def _on_post_tool_call(tool_name: str = None, args: dict = None,
                        result: str = None, success: bool = True,
                        duration_ms: float = 0.0, session_id: str = None,
                        task_id: str = None, tool_call_id: str = None,
                        **kwargs) -> None:
    """post_tool_call handler."""
    _logger_mod.log(
        tool_name=tool_name,
        args=args,
        result=result,
        success=success,
        duration_ms=duration_ms,
        session_id=session_id,
        task_id=task_id,
        tool_call_id=tool_call_id,
    )
