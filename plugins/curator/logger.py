"""post_tool_call hook — logs tool calls to tool_call_log."""

import logging
import time
from typing import Any, Dict

from . import queries

_logger = logging.getLogger(__name__)


class _CallContext:
    """Shared state between pre and post hooks for the same tool call."""
    def __init__(self):
        self.start_time: float = 0.0
        self.fault_ref: str = None
        self.checkpoint_ref: str = None

    def reset(self):
        self.start_time = 0.0
        self.fault_ref = None
        self.checkpoint_ref = None


# Per-task context store (keyed by tool_call_id)
_call_contexts: Dict[str, _CallContext] = {}


def set_context(tool_call_id: str, fault_ref: str = None, checkpoint_ref: str = None):
    """Store pre-hook context for the post-hook to consume."""
    ctx = _call_contexts.setdefault(tool_call_id, _CallContext())
    ctx.start_time = time.time()
    if fault_ref:
        ctx.fault_ref = fault_ref
    if checkpoint_ref:
        ctx.checkpoint_ref = checkpoint_ref


def log(tool_name: str = None, args: dict = None, result: str = None,
        success: bool = True, duration_ms: float = 0.0,
        session_id: str = None, task_id: str = None,
        tool_call_id: str = None, **kwargs) -> None:
    """post_tool_call hook — logs to tool_call_log."""
    if not tool_name:
        return

    # Get pre-hook context
    ctx = _call_contexts.pop(tool_call_id, None)
    if ctx and ctx.start_time > 0:
        elapsed = int((time.time() - ctx.start_time) * 1000)
    else:
        elapsed = int(duration_ms)

    queries.log_tool_call(
        occurred_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        session_id=session_id or "",
        tool_name=tool_name,
        tool_args=args or {},
        result_summary=(result or "")[:500],
        success=success,
        duration_ms=elapsed,
        fault_ref=ctx.fault_ref if ctx else None,
        checkpoint_ref=ctx.checkpoint_ref if ctx else None,
    )
