"""pre_tool_call hook logic for the identity curator."""

import hashlib
import json
import logging
import threading
import time
from typing import Any, Dict, Optional

from . import config, queries

logger = logging.getLogger(__name__)

# Thread-safe LRU cache for embeddings
_cache = {}
_cache_lock = threading.Lock()


def _cache_key(tool_name: str, tool_args: dict) -> str:
    """Generate cache key from tool name + args."""
    raw = f"{tool_name} | {json.dumps(tool_args, sort_keys=True, default=str)}"
    return hashlib.sha256(raw.encode()).hexdigest()


def _get_cached(key: str) -> Optional[list]:
    """Get cached embedding if not expired."""
    with _cache_lock:
        entry = _cache.get(key)
        if entry and (time.time() - entry["ts"]) < config.LRU_TTL_SECONDS:
            return entry["emb"]
        if entry:
            del _cache[key]
    return None


def _set_cache(key: str, embedding: list):
    """Store embedding in cache."""
    with _cache_lock:
        if len(_cache) >= config.LRU_SIZE:
            # Evict oldest
            oldest = min(_cache.keys(), key=lambda k: _cache[k]["ts"])
            del _cache[oldest]
        _cache[key] = {"emb": embedding, "ts": time.time()}


def check(tool_name: str, args: dict, session_id: str = None,
          task_id: str = None, tool_call_id: str = None, **kwargs) -> Optional[Dict]:
    """Pre-tool-call hook. Returns None to allow, dict to block.

    The returned dict for a block has:
        {"block": True, "message": "...", "fault_ref": "uuid"}
    """
    # Skip tools that should always pass through
    if tool_name in config.SKIP_TOOLS:
        return None

    # Generate embedding (with cache)
    cache_key = _cache_key(tool_name, args or {})
    emb = _get_cached(cache_key)
    if emb is None:
        text = f"{tool_name} | {json.dumps(args, sort_keys=True, default=str)}"
        emb = queries.make_embedding(text)
        if emb:
            _set_cache(cache_key, emb)
        else:
            return None  # embedding failed, let through

    # 1. Check identity_faults — block if similar
    faults = queries.search_faults(emb)
    if faults:
        f = faults[0]
        logger.info(
            "blocked tool=%s sim=%.2f fault=%s",
            tool_name, f["similarity"], f["fault_type"],
        )
        return {
            "block": True,
            "message": (
                f"[CURATOR] Tool `{tool_name}` blocked — matches identity fault "
                f"`{f['fault_type']}` (similarity={f['similarity']:.2f}).\n"
                f"Countermeasure: {f['countermeasure']}"
            ),
            "fault_ref": str(f["id"]),
        }

    # 2. Check checkpoints — annotate but don't block
    checkpoints = queries.search_checkpoints(emb)
    cp_ref = None
    if checkpoints:
        cp = checkpoints[0]
        cp_ref = str(cp["id"])
        logger.info(
            "context-match tool=%s sim=%.2f territory=%s",
            tool_name, cp["similarity"], cp["territory"],
        )

    return None  # allow
