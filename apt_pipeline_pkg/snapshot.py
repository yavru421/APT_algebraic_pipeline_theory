"""Snapshot utilities for APT execution traces.

This module writes newline-delimited JSON (ndjson) snapshots to `results/apt_trace.ndjson`
when the environment variable `APT_TRACE` is set to a truthy value. Each snapshot records
step index, step name, variable name, a compact representation of the value, and a timestamp.
"""
from __future__ import annotations

import os
import json
import time
from pathlib import Path
from typing import Any

TRACE_ENV = "APT_TRACE"
DEFAULT_OUT = Path("results") / "apt_trace.ndjson"
MAX_VALUE_LEN = 1024


def _compact_value(v: Any, max_len: int = MAX_VALUE_LEN) -> Any:
    try:
        # Try to produce a JSON-serializable compact representation
        if isinstance(v, (str, bytes)):
            s = v.decode("utf-8") if isinstance(v, bytes) else v
            if len(s) > max_len:
                return {"__truncated__": True, "length": len(s), "preview": s[: max_len // 2]}
            return s
        # For dict/list/primitive attempt json.dumps; fall back to repr
        if isinstance(v, (dict, list, int, float, bool, type(None))):
            js = json.dumps(v, default=str)
            if len(js) > max_len:
                return {"__truncated__": True, "length": len(js), "preview": js[: max_len // 2]}
            return v
        s = repr(v)
        if len(s) > max_len:
            return {"__truncated__": True, "length": len(s), "preview": s[: max_len // 2]}
        return s
    except Exception:
        return {"__repr__": repr(v)}


def enabled() -> bool:
    v = os.getenv(TRACE_ENV, "0")
    return v not in ("", "0", "false", "False", "off")


def snapshot(step: int, name: str, var: str, value: Any, out_path: Path | str | None = None, max_len: int = MAX_VALUE_LEN) -> None:
    """Append a snapshot record as one JSON line to the trace file.

    Non-blocking and safe: if the results directory cannot be created or written,
    the function logs to stderr but does not raise.
    """
    if not enabled():
        return

    out = Path(out_path) if out_path else DEFAULT_OUT
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "ts": time.time(),
            "step": step,
            "name": name,
            "var": var,
            "value": _compact_value(value, max_len),
        }
        with out.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, default=str) + "\n")
    except Exception as e:
        # Best-effort: do not raise during snapshotting
        try:
            print(f"[snapshot:error] {e}")
        except Exception:
            pass
