"""Minimal APT executor.

Purpose: interpret a small declarative pipeline spec (list of steps), compose an
algebraic expression for the pipeline, execute steps using functions in
`apt_pipeline_pkg.pipeline`, and emit snapshots via `apt_pipeline_pkg.snapshot`.

This is methodology-first: no network calls are made by the executor itself unless
the step function performs them. The demo uses simulated steps.
"""
from __future__ import annotations

from typing import Any, Dict, List
from importlib import import_module
from apt_pipeline_pkg import pipeline
from apt_pipeline_pkg.snapshot import snapshot, enabled as trace_enabled
from apt_pipeline_pkg import env as apt_env
import json
import os
import subprocess
from pathlib import Path


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


def _resolve_callable(fn_name: str, module_path: str | None = None):
    """Resolve a callable given a function name, with optional module path.

    Supports:
      - explicit module path via `module_path`
      - `fn` as "module.sub:func"
      - fallback to apt_pipeline_pkg.pipeline
    """
    # If fn contains module delimiter, split it
    if ":" in fn_name:
        mod_name, func = fn_name.split(":", 1)
        mod = import_module(mod_name)
        return getattr(mod, func)
    # Else use provided module path if any
    if module_path:
        mod = import_module(module_path)
        return getattr(mod, fn_name)
    # Fallback to default pipeline module
    return getattr(pipeline, fn_name)


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
    steps: List[Dict[str, Any]] = spec.get("steps", [])  # type: ignore[assignment]
    outputs: Dict[str, Any] = {}

    # Build expression and snapshot it
    step_names: List[str] = [str(s["name"]) for s in steps if "name" in s]
    expr = build_expression(step_names)
    if trace_enabled():
        snapshot(0, "pipeline_expression", "expr", expr)

    for idx, step in enumerate(steps, start=1):
        name: str | None = step.get("name")
        fn_name: str | None = step.get("fn")
        args: Dict[str, Any] = step.get("args", {}) or {}
        module_path: str | None = step.get("module")  # optional explicit module path
        env_name: str | None = step.get("env")  # optional environment name

        if not name or not fn_name:
            raise RuntimeError(f"Step {idx} is missing required 'name' or 'fn': {step}")

        # Prepare environment (no-op if None)
        if env_name:
            apt_env.prepare_env(env_name)

        # Resolve arguments that reference previous outputs
        resolved_args: Dict[str, Any] = {str(k): _resolve_arg(v, outputs) for k, v in args.items()}

        # Snapshot inputs
        if trace_enabled():
            snapshot(idx, name, "inputs", resolved_args)

        # Optionally execute via PowerShell invoker to ensure env python is used
        use_ps = os.getenv("APT_USE_PS", "0") not in ("0", "false", "False", "off")
        if use_ps and env_name:
            invoker = Path("scripts") / "Invoke-AptStep.ps1"
            if not invoker.exists():
                raise RuntimeError(f"Invoker script not found: {invoker}")
            cmd = [
                "pwsh", "-NoProfile", "-File", str(invoker),
                "-EnvName", env_name,
                "-Module", module_path or "apt_pipeline_pkg.pipeline",
                "-Function", fn_name,
                "-ArgsJson", json.dumps(resolved_args, ensure_ascii=False),
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            if proc.returncode != 0:
                raise RuntimeError(f"Step {name} failed: {proc.stderr}")
            try:
                out = json.loads(proc.stdout)
            except Exception:
                out = proc.stdout
        else:
            # In-process execution path
            try:
                fn = _resolve_callable(fn_name, module_path)
            except Exception as e:
                raise RuntimeError(f"Unable to resolve function '{fn_name}' (module={module_path!r}): {e}")
            out = fn(**resolved_args)

        # Save output under step name
        outputs[name] = out

        # Snapshot output
        if trace_enabled():
            snapshot(idx, name, "output", out)

    return outputs
