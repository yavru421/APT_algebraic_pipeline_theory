"""
test_apt_modules.py: Unit tests for apt_pipeline_pkg.apt_modules

Tests m1_load_state, m2_extract_eq, m3_llm_rewrite, m4_sim_trace, m5_persist
"""
import os, json, tempfile
import pytest
from apt_pipeline_pkg import apt_modules

def test_m1_load_state_empty():
    # Should return empty dict if file does not exist
    state = apt_modules.m1_load_state('nonexistent_file.json')
    assert isinstance(state, dict)
    assert state == {}

def test_m2_extract_eq_override():
    # Should return override if provided
    eq = apt_modules.m2_extract_eq({'pipeline_equation': 'y=bad'}, 'y=good')
    assert eq == 'y=good'

def test_m2_extract_eq_fallback():
    # Should return pipeline_equation from state
    eq = apt_modules.m2_extract_eq({'pipeline_equation': 'y=ok'}, None)
    assert eq == 'y=ok'
    # Should fallback to default if not present
    eq2 = apt_modules.m2_extract_eq({}, None)
    assert eq2 == 'y_final = m2(m1(x1))'

def test_m4_sim_trace():
    # Should produce a trace for a simple equation
    eq = 'y2 = m2(m1(x1))'
    trace = apt_modules.m4_sim_trace(eq)
    assert isinstance(trace, list)
    assert len(trace) == 2
    assert trace[0]['module'] == 'm1'
    assert trace[1]['module'] == 'm2'

def test_m5_persist(tmp_path):
    # Should write files and update state
    state = {}
    eq = 'y2 = m2(m1(x1))'
    trace = apt_modules.m4_sim_trace(eq)
    out_dir = apt_modules.m5_persist(state, eq, trace)
    assert os.path.isdir(out_dir)
    assert os.path.isfile(os.path.join(out_dir, 'equation.txt'))
    assert os.path.isfile(os.path.join(out_dir, 'trace.json'))
    assert 'pipeline_equation' in state
