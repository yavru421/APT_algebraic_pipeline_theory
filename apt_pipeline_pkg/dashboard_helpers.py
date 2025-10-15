"""Dashboard helper utilities for APT Flet MCP Dashboard.

Algebraic modules:
- m_extract_modules: parse module identifiers from a pipeline equation preserving left-to-right order.
- m_simulate_trace: build an algebraic placeholder execution trace from an ordered module list.
- m_build_snapshot: assemble snapshot artifacts prior to disk write (returns dicts ready for serialization).

Each function is pure and testable.
"""
from __future__ import annotations
import re, platform, datetime
from typing import List, Dict, Any

# m_extract_modules
# Contract:
#  Inputs: equation: str
#  Output: modules: List[str] (ordered by first appearance, duplicates removed after first occurrence)
#  Errors: none (returns [])
#  Algebraic: modules = m_extract_modules(equation)

def m_extract_modules(equation: str) -> List[str]:
    if not equation:
        return []
    found = re.findall(r'm\d+', equation)
    ordered = []
    seen = set()
    for m in found:
        if m not in seen:
            ordered.append(m)
            seen.add(m)
    return ordered

# m_simulate_trace
# Contract:
#  Inputs: modules: List[str]
#  Output: trace: List[Dict[str,str]] with keys module,input,output,ts
#  Errors: none
#  Algebraic: trace = m_simulate_trace(modules)

def m_simulate_trace(modules: List[str]) -> List[Dict[str, str]]:
    trace = []
    x_in = "x0"
    for idx, mi in enumerate(modules, start=1):
        y_out = f"y{idx}"
        trace.append({
            "module": mi,
            "input": x_in,
            "output": y_out,
            "ts": datetime.datetime.now().isoformat()
        })
        x_in = y_out
    return trace

# m_build_snapshot
# Contract:
#  Inputs: equation:str, modules:List[str], selected_context:str|None, multi_chat:bool
#          chat_history:Dict[str, List[Dict]], trace:List[Dict]
#  Output: manifest:Dict[str,Any]
#  Errors: none
#  Algebraic: manifest = m_build_snapshot(equation, modules, selected_context, multi_chat, env, trace)

def m_build_snapshot(equation: str, modules: List[str], selected_context: str | None, multi_chat: bool, chat_history: Dict[str, Any], trace: List[Dict[str, Any]]) -> Dict[str, Any]:
    manifest = {
        "timestamp": datetime.datetime.now().isoformat(),
        "pipeline_equation": equation,
        "modules": modules,
        "selected_context": selected_context,
        "multi_chat": multi_chat,
        "env": {"python": platform.python_version(), "platform": platform.platform()},
        "trace_len": len(trace),
        "threads": list(chat_history.keys())
    }
    return manifest
