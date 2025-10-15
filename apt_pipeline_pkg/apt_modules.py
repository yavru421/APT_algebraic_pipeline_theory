"""
apt_modules.py: Unified APT module registry for algebraic pipeline workflows.

Each module is pure, testable, and has an explicit contract and algebraic equation.

Modules:
- m1_load_state
- m2_extract_eq
- m3_llm_rewrite
- m4_sim_trace
- m5_persist

"""
import os, json, datetime, requests
from apt_pipeline_pkg.dashboard_helpers import m_extract_modules, m_simulate_trace, m_build_snapshot

STATE_FILE = ".apt_dashboard_state.json"
PARSE_URL = "http://localhost:8000/v1/parse_instruction"

def m1_load_state(path: str):
    """
    m1_load_state
    Contract:
      Inputs: path: str
      Outputs: state: dict[str, any]
      Errors: returns empty dict on failure
      Algebraic: y1 = m1(x1)
    """
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}  # type: dict[str, any]
    return {}  # type: dict[str, any]

def m2_extract_eq(state: dict, override: str | None):
        """
        m2_extract_eq
        Contract:
            Inputs: state: dict[str, any], override: str|None
            Outputs: eq: str
            Errors: returns fallback equation on failure
            Algebraic: y2 = m2(y1, x2)
        """
        if override:
                return override
        return state.get('pipeline_equation') or 'y_final = m2(m1(x1))'

def m3_llm_rewrite(eq: str):
    """
    m3_llm_rewrite
    Contract:
      Inputs: eq: str
      Outputs: new_eq: str
      Errors: returns input eq on failure
      Algebraic: y3 = m3(y2)
    """
    prompt = f"Normalize and reorganize this APT pipeline equation if needed: {eq}"
    try:
        r = requests.post(PARSE_URL, json={'prompt': prompt}, timeout=15)
        if r.status_code == 200:
            data = r.json()
            new_eq = data.get('apt_equation') or eq
            return new_eq
    except Exception:
        pass
    return eq

def m4_sim_trace(eq: str):
        """
        m4_sim_trace
        Contract:
            Inputs: eq: str
            Outputs: trace: list[dict[str, str]]
            Errors: returns empty list on failure
            Algebraic: y4 = m4(y3)
        """
        modules = m_extract_modules(eq)
        return m_simulate_trace(modules)

def m5_persist(state: dict, eq: str, trace: list[dict]):
    """
    m5_persist
    Contract:
      Inputs: state: dict[str, any], eq: str, trace: list[dict[str, str]]
      Outputs: out_dir: str
      Errors: prints warning on state file update failure
      Algebraic: y5 = m5(y1, y3, y4)
    """
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out_dir = os.path.join('archive', 'auto_reorg', ts)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'equation.txt'), 'w', encoding='utf-8') as fe:
        fe.write(eq)
    with open(os.path.join(out_dir, 'trace.json'), 'w', encoding='utf-8') as ft:
        json.dump(trace, ft, indent=2)
    state['pipeline_equation'] = eq
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as fs:
            json.dump(state, fs, indent=2)
    except Exception as ex:
        print(f"Warning: failed to update state file: {ex}")
    manifest = m_build_snapshot(eq, m_extract_modules(eq), state.get('selected_context'), state.get('multi_chat', False), state.get('chat_history', {}), trace)
    with open(os.path.join(out_dir, 'manifest.json'), 'w', encoding='utf-8') as fm:
        json.dump(manifest, fm, indent=2)
    return out_dir
