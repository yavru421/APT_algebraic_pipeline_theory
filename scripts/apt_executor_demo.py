"""Demo for the APT executor.

Runs a small declarative pipeline to demonstrate the APT methodology executor.
"""
import os
import json
from pathlib import Path
import sys

# Ensure repo root importable
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

os.environ.setdefault("APT_TRACE", "1")

from apt_pipeline_pkg.executor import execute
from apt_pipeline_pkg.pipeline import base64_encode_image

# Create a tiny demo image
demo_image = Path("demo_executor_image.bin")
demo_image.write_bytes(b"executor-demo")

spec = {
    "steps": [
        {"name": "m1", "fn": "base64_encode_image", "args": {"image_path": str(demo_image)}},
        {"name": "m2", "fn": "build_payload", "args": {"image_b64": "$m1", "apt_prompt": "Demo prompt", "model": "demo-model"}},
    ]
}

outputs = execute(spec)

print("Executor outputs:")
print(json.dumps({k: (v if isinstance(v, (str, int, float, dict)) else str(type(v))) for k, v in outputs.items()}, indent=2))

print("\nTrace file contents:")
trace_file = Path("results") / "apt_trace.ndjson"
if trace_file.exists():
    for line in trace_file.read_text(encoding="utf-8").splitlines():
        print(line)
else:
    print("(no trace file)")
