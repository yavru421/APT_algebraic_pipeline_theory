"""flet_gui_llama_autoreorganze

Purpose:
  Standalone APT helper script to automatically reorganize / normalize a pipeline equation
  using the existing MCP parse_instruction endpoint (LLM) and then persist the updated
  equation plus a simulation trace.

Algebraic Modules:
  m1_load_state:   (x_path) -> y_state (loads existing dashboard state if present)
  m2_extract_eq:   (y_state) -> y_eq0   (baseline equation or fallback default)
  m3_llm_rewrite:  (y_eq0) -> y_eq1     (LLM normalized / reorganized equation)
  m4_sim_trace:    (y_eq1) -> y_trace   (simulated execution trace)
  m5_persist:      (y_state, y_eq1, y_trace) -> y_state' (writes updated files)

Pipeline Equation:
  y_state' = m5(m4(m3(m2(m1(x_path)))))

Usage:
  python flet_gui_llama_autoreorganze.py [--equation "y_final = m2(m1(x1))"]

Outputs:
  - Updates .apt_dashboard_state.json pipeline_equation field if present
  - Writes ./archive/auto_reorg/<timestamp>/ with equation.txt and trace.json

Contract:
  Inputs: optional CLI equation override
  Outputs: printed new equation path, trace path
  Errors: non-zero exit on hard failures (network or file IO)
"""
from __future__ import annotations
import os, json, argparse, datetime, sys
import requests

# Use unified APT modules
from apt_pipeline_pkg.apt_modules import m1_load_state, m2_extract_eq, m3_llm_rewrite, m4_sim_trace, m5_persist

STATE_FILE = ".apt_dashboard_state.json"
PARSE_URL = "http://localhost:8000/v1/parse_instruction"






def main():
    parser = argparse.ArgumentParser(description='Auto reorganize APT pipeline equation via LLM parse endpoint.')
    parser.add_argument('--equation', type=str, help='Override equation to reorganize')
    args = parser.parse_args()


    # Unified algebraic pipeline
    # y_state' = m5(m4(m3(m2(m1(x_path), x_override))))
    state = m1_load_state(STATE_FILE)
    eq0 = m2_extract_eq(state, args.equation)
    eq1 = m3_llm_rewrite(eq0)
    trace = m4_sim_trace(eq1)
    out_dir = m5_persist(state, eq1, trace)

    print('Original Equation:', eq0)
    print('Rewritten Equation:', eq1)
    print('Output Directory:', out_dir)

    if eq1 != eq0:
        print('Equation changed.')
    else:
        print('Equation unchanged.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
