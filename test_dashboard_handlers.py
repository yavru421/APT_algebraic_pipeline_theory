"""
Test harness for APT Flet Dashboard handlers (APT Chat Mode, Algebraic Pipeline Theory)

This script tests the main dashboard handlers in isolation:
- new_document_tab
- simulate_pipeline
- send_instruction

Mocks are used for requests and file I/O. No GUI is launched.
"""
import os
import sys
import types
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Patch sys.path so we can import the dashboard file as a module
sys.path.insert(0, os.path.dirname(__file__))

import apt_flet_dashboard as dashboard

def test_new_document_tab():
    # Setup: patch os.makedirs and open to use a temp dir
    temp_dir = tempfile.mkdtemp()
    try:
        with patch("os.makedirs") as makedirs, \
             patch("builtins.open", create=True) as mock_open:
            makedirs.side_effect = lambda path, exist_ok=True: None
            mock_open.return_value.__enter__.return_value.write = MagicMock()
            # Patch os.getcwd to return temp_dir
            with patch("os.getcwd", return_value=temp_dir):
                # Patch workspace_tabs to a MagicMock
                dashboard.workspace_tabs = MagicMock()
                dashboard.chat_counter = {"n": 0}
                dashboard.append_to_result = MagicMock()
                dashboard.refresh_contexts = MagicMock()
                dashboard.new_document_tab()
                # Check that open was called (file write attempted)
                assert mock_open.called, "open() not called in new_document_tab"
    finally:
        shutil.rmtree(temp_dir)

def test_simulate_pipeline():
    dashboard.append_to_result = MagicMock()
    dashboard.pipeline_box = MagicMock()
    dashboard.pipeline_box.value = "y_final = m2(m1(x1))"
    dashboard.m_extract_modules = lambda eq: ["m1", "m2"]
    dashboard.m_simulate_trace = lambda mods: [
        {"output": "y1", "module": "m1", "input": "x1"},
        {"output": "y_final", "module": "m2", "input": "y1"}
    ]
    dashboard.simulate_pipeline()
    # Check that append_to_result was called with a simulation trace
    called = any("# Simulation Trace" in str(call) for call in dashboard.append_to_result.call_args_list)
    assert called, "simulate_pipeline did not append simulation trace"

def test_send_instruction():
    dashboard.append_to_result = MagicMock()
    dashboard.pipeline_box = MagicMock()
    dashboard.pipeline_box.value = "y_final = m2(m1(x1))"
    dashboard.instruction_box = MagicMock()
    dashboard.instruction_box.value = "simulate"
    dashboard.set_status = MagicMock()
    dashboard.save_state = MagicMock()
    dashboard.update_discoveries = MagicMock()
    dashboard.multi_chat_switch = MagicMock()
    dashboard.multi_chat_switch.value = False
    dashboard.chat_counter = {"n": 0}
    dashboard.chat_history = {}
    dashboard.chat_threads = MagicMock()
    # Patch requests.post and requests.get
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        mock_post.return_value.json.return_value = {"apt_equation": "y_final = m2(m1(x1))", "result": "ok"}
        mock_get.return_value.json.return_value = {"discoveries": ["foo"]}
        dashboard.send_instruction(None)
        # Check that set_status and chat_threads.append_message were called
        assert dashboard.set_status.called, "set_status not called in send_instruction"
        assert dashboard.chat_threads.append_message.called, "chat_threads.append_message not called"

if __name__ == "__main__":
    test_new_document_tab()
    print("test_new_document_tab passed")
    test_simulate_pipeline()
    print("test_simulate_pipeline passed")
    test_send_instruction()
    print("test_send_instruction passed")
