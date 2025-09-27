import json
import io
from apt_curl_3 import m_1_build_payload, m_3_process_stream


def test_build_payload_contains_system_and_user():
    system = "SYS"
    user = "Do X"
    payload = m_1_build_payload(system, user)
    assert "messages" in payload
    assert payload["messages"][0]["content"] == system
    assert payload["messages"][1]["content"] == user


def test_process_stream_parses_sse(tmp_path, monkeypatch):
    # Build a fake SSE stream with two data events
    events = [
        {"event": {"event_type": "progress", "delta": {"text": "Hello "}}},
        {"event": {"event_type": "progress", "delta": {"text": "World"}}}
    ]
    lines = []
    for e in events:
        lines.append(b"data: " + json.dumps(e).encode("utf-8") + b"\n")

    class FakeResponse:
        def __init__(self, lines):
            self._lines = lines

        def iter_lines(self):
            for l in self._lines:
                yield l

    out_file = tmp_path / "output.txt"
    debug_file = tmp_path / "output_debug.txt"

    # Patch filenames inside module via monkeypatch of globals
    monkeypatch.setenv("TEST_OUTPUT_PATH", str(out_file))
    # Call process_stream with fake response
    resp = FakeResponse(lines)
    # m_3_process_stream writes to default files; ensure it runs without exception
    m_3_process_stream(resp)
    # Check files exist and contain expected concatenated text
    with open("output.txt", "r", encoding="utf-8") as f:
        data = f.read()
    assert "Hello World" in data
