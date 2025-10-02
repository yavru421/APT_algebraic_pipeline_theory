"""
APT Pipeline: Modular, algebraic pipeline for screenshot and image understanding using external AI APIs.
"""
import base64
from typing import Any

def build_pipeline_expression(steps: list[str]) -> str:
    """Return a human-readable algebraic expression for the pipeline.

    Example: ['m1', 'm2', 'm3'] -> 'y = m3(m2(m1(x)))'
    """
    if not steps:
        return "y = x"
    expr = "x"
    for s in steps:
        expr = f"{s}({expr})"
    return f"y = {expr}"

def base64_encode_image(image_path: str) -> str:
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def build_payload(image_b64: str, apt_prompt: str, model: str) -> dict[str, Any]:
    return {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": apt_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
                ],
                "system_instructions": apt_prompt
            }
        ]
    }
