"""Map a subset of the OpenAPI YAML to an APT executor spec and run it.

This script does not depend on PyYAML; it uses simple text search to find
operationIds/paths and demonstrates how the OpenAPI document can drive the APT
executor. It shows the bigger picture: the spec (YAML) → declarative pipeline
spec → executor runs → algebraic expression + snapshots.
"""
from pathlib import Path
import sys
import json

# Make repo importable
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from apt_pipeline_pkg.executor import execute

OPENAPI = Path("docs") / "llama-chat-completions.yaml"


def find_operation(target_op: str = "uploadImageAndAsk") -> str | None:
    text = OPENAPI.read_text(encoding="utf-8")
    if f"operationId: {target_op}" in text:
        return target_op
    # fallback: look for chat completion
    if "operationId: createChatCompletion" in text:
        return "createChatCompletion"
    return None


def build_spec_for_operation(op: str) -> dict:
    """Map an operationId to a small executor spec.

    For `uploadImageAndAsk` we map to:
      m1: base64_encode_image(image_path)
      m2: build_payload(image_b64=$m1, apt_prompt=question, model=model)

    For `createChatCompletion` we map to a prompt-only flow.
    """
    if op == "uploadImageAndAsk":
        # demo image and params
        demo_image = Path("demo_yaml_image.bin")
        demo_image.write_bytes(b"yaml-demo")
        return {
            "steps": [
                {"name": "m1", "fn": "base64_encode_image", "args": {"image_path": str(demo_image)}},
                {"name": "m2", "fn": "build_payload", "args": {"image_b64": "$m1", "apt_prompt": "Question: what's in the image?", "model": "demo-model"}},
            ]
        }
    else:
        # createChatCompletion: prompt-only
        return {
            "steps": [
                {"name": "m1", "fn": "build_payload", "args": {"image_b64": "", "apt_prompt": "Summarize X", "model": "demo-model"}},
            ]
        }


def main():
    op = find_operation()
    if not op:
        print("No known operationId found in YAML; aborting demo.")
        return
    print(f"Found operationId: {op} — building executor spec")
    spec = build_spec_for_operation(op)
    print("Spec to run:\n", json.dumps(spec, indent=2))
    outputs = execute(spec)
    print("\nExecutor outputs:")
    print(json.dumps({k: (v if isinstance(v, (str, int, float, dict)) else str(type(v))) for k, v in outputs.items()}, indent=2))
    print("\nTrace file (last 20 lines):")
    trace = Path("results") / "apt_trace.ndjson"
    if trace.exists():
        lines = trace.read_text(encoding="utf-8").splitlines()
        for l in lines[-20:]:
            print(l)
    else:
        print("(no trace file)")


if __name__ == "__main__":
    main()
