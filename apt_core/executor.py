"""Minimal APT executor.

Purpose: interpret a small declarative pipeline spec (list of steps), compose an
algebraic expression for the pipeline, execute steps using functions in
`apt_core.pipeline`, and emit snapshots via `apt_core.snapshot`.

This is methodology-first: no network calls are made by the executor itself unless
the step function performs them. The demo uses simulated steps.
"""
from __future__ import annotations

from typing import Any, Dict, List
from apt_core import pipeline
from apt_core.snapshot import snapshot, enabled as trace_enabled


def _resolve_arg(val: Any, outputs: Dict[str, Any]) -> Any:
    """Resolve an argument value. If val is a string starting with '$', treat
    it as a reference to a prior step output: '$step_name'."""
    if isinstance(val, str) and val.startswith("$"):
        key = val[1:]
        return outputs.get(key)
    return val


def build_expression(step_names: List[str]) -> str:
    # use pipeline helper for readable expression
    return pipeline.build_pipeline_expression(step_names)


def execute(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a pipeline spec.

    Spec format:
      {
        "steps": [
           {"name": "m1", "fn": "base64_encode_image", "args": {"image_path": "demo.png"}},
           {"name": "m2", "fn": "build_payload", "args": {"image_b64": "$m1", "apt_prompt": "...", "model": "demo"}},
        ]
      }

    Returns a dict with outputs keyed by step name.
    """
    steps = spec.get("steps", [])
    outputs: Dict[str, Any] = {}

    # Build expression and snapshot it
    step_names = [s.get("name") for s in steps]
    expr = build_expression(step_names)
    if trace_enabled():
        snapshot(0, "pipeline_expression", "expr", expr)

    for idx, step in enumerate(steps, start=1):
        name = step.get("name")
        fn_name = step.get("fn")
        args = step.get("args", {}) or {}

        # Resolve arguments that reference previous outputs
        resolved_args = {k: _resolve_arg(v, outputs) for k, v in args.items()}

        # Snapshot inputs
        if trace_enabled():
            snapshot(idx, name, "inputs", resolved_args)

        # Call function from pipeline module
        fn = getattr(pipeline, fn_name, None)
        if fn is None:
            raise RuntimeError(f"Unknown pipeline function: {fn_name}")

        out = fn(**resolved_args)

        # Save output under step name
        outputs[name] = out

        # Snapshot output
        if trace_enabled():
            snapshot(idx, name, "output", out)

    return outputs
