"""Demo runner: simulates the pipeline end-to-end without network.

- Enables APT_TRACE
- Creates a small dummy image file
- Runs base64_encode_image -> build_payload -> simulated call_api -> process_stream
- Prints the generated results/apt_trace.ndjson and output.txt
"""
import os
import json
import sys
from pathlib import Path

# Ensure repo root is on sys.path when running this script directly
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

# Enable tracing for this demo
os.environ["APT_TRACE"] = "1"

# Import pipeline primitives and runtime process
from apt_pipeline_pkg.pipeline import base64_encode_image, build_payload
from apt_curl_3 import m_3_process_stream

# Prepare demo inputs
demo_image = Path("demo_image.png")
# write a tiny file (not a real PNG; base64 encode still works for demo)
demo_image.write_bytes(b"demo-image-bytes")
prompt = "Summarize the following demo image content in one sentence."
model = "demo-model"

# Run m1
image_b64 = base64_encode_image(str(demo_image))
print("[demo] image_b64 length:", len(image_b64))

# Run m2
payload = build_payload(image_b64, prompt, model)
print("[demo] built payload keys:", list(payload.keys()))

# Simulate a streaming response (SSE-like)
class FakeResponse:
    def __init__(self, lines):
        self._lines = lines
    def iter_lines(self):
        for l in self._lines:
            yield l

# Create two fake SSE events with 'progress' deltas
events = [
    {"event": {"event_type": "progress", "delta": {"text": "Hello "}}},
    {"event": {"event_type": "progress", "delta": {"text": "World"}}},
]
lines = [b"data: " + json.dumps(e).encode("utf-8") + b"\n" for e in events]
resp = FakeResponse(lines)

# Ensure results dir is clean
results_dir = Path("results")
results_dir.mkdir(exist_ok=True)
trace_file = results_dir / "apt_trace.ndjson"
if trace_file.exists():
    trace_file.unlink()

# Run m3/process_stream to write output.txt and debug file and snapshots
m_3_process_stream(resp, out_path="output.txt", debug_path="output_debug.txt")

# Print outputs
print("\n--- output.txt ---")
print(Path("output.txt").read_text(encoding="utf-8"))
print("\n--- output_debug.txt ---")
print(Path("output_debug.txt").read_text(encoding="utf-8"))
print("\n--- results/apt_trace.ndjson (lines) ---")
if trace_file.exists():
    for line in trace_file.read_text(encoding="utf-8").splitlines():
        print(line)
else:
    print("(no trace file found)")
