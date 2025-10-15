"""
test_cli_llama_scad_chat.py

Contract:
  Tests m2_build_payload and m4_parse_response for happy path and edge case.
"""
from APT_OpenSCAD.cli_llama_scad_chat import m2_build_payload, m4_parse_response

def test_m2_build_payload_happy():
    prompt = "Draw a cube"
    model_id = "Llama-3.3-70B-Instruct"
    payload = m2_build_payload(prompt, model_id)
    assert payload["model"] == model_id
    assert payload["messages"][0]["content"] == prompt
    assert payload["stream"] is False

def test_m4_parse_response_happy():
    response = {"choices": [{"message": {"content": "cube([1,1,1]);"}}]}
    result = m4_parse_response(response)
    assert result == "cube([1,1,1]);"

def test_m4_parse_response_edge():
    # Edge: malformed response
    response = {"unexpected": True}
    result = m4_parse_response(response)
    assert result is not None and "unexpected" in result
