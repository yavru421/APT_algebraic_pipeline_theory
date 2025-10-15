"""
cli_llama_scad_chat.py

Contract:
  Inputs: x1: user prompt (str), x2: OpenSCAD view state (object), x3: OpenAPI spec (dict), x4: model_id (str)
  Outputs: y_final: None (side effects: chat, OpenSCAD view update)
  Errors: Handles network, parsing, and OpenSCAD errors
Algebraic: y_final = m6(m5(m4(m3(m2(m1(x1), x4), x3)), x2))

Usage:
  python APT-OpenSCAD/cli_llama_scad_chat.py --model Llama-3.3-70B-Instruct

Requires:
  - requests
  - (optional) openscad or solidpython for OpenSCAD rendering
"""

import sys
import requests
import argparse
import os
from typing import Any

# --- m1: CLI input handler ---
def m1_get_user_prompt():
    try:
        return input("You: ")
    except (EOFError, KeyboardInterrupt):
        print("\nExiting chat.")
        sys.exit(0)

# --- m2: Build Llama API payload ---
def m2_build_payload(prompt: str, model_id: str, system_prompt: str = None, max_tokens: int = 4096) -> dict[str, Any]:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    return {
        "model": model_id,
        "messages": messages,
        "stream": False,
        "max_tokens": max_tokens
    }

# --- m3: Call Llama API (Netlify proxy or MCP server) ---
def m3_call_llama_api(payload: dict[str, Any], proxy_url: str, mcp_server: str = None) -> dict[str, Any] | None:
    if mcp_server:
        url = f"{mcp_server.rstrip('/')}/v1/chat/completions"
    else:
        url = f"{proxy_url}/?path=/chat/completions"
    try:
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ERROR] API call failed: {e}")
        return None

# --- m4: Parse Llama response ---
def m4_parse_response(response: dict[str, Any] | None) -> str | None:
    if not response:
        return None
    # Try OpenAI-style, else Netlify Llama proxy style
    try:
        # OpenAI-style
        return response["choices"][0]["message"]["content"]
    except Exception:
        try:
            # Netlify Llama proxy style
            return response["completion_message"]["content"]["text"]
        except Exception:
            return str(response)

# --- m5: Update OpenSCAD view ---
import datetime

import re

def m5_update_openscad_view(scad_code: str, project: str = "default") -> None:
    # Only save if a code block is found
    match = re.search(r"```scad(.*?)```", scad_code, re.DOTALL | re.IGNORECASE)
    if not match:
        print("[WARNING] No OpenSCAD code block found in model output. No .scad file written.")
        return
    code = match.group(1).strip()
    # Ensure project folder exists
    folder = os.path.join("scad_projects", project)
    os.makedirs(folder, exist_ok=True)
    # Save with timestamp
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    scad_file = os.path.join(folder, f"llama_{ts}.scad")
    with open(scad_file, "w", encoding="utf-8") as f:
        f.write(code)
    # Try to preview with OpenSCAD CLI (if installed)
    png_file = os.path.join(folder, f"llama_{ts}.png")
    if os.system(f"openscad -o {png_file} {scad_file}") == 0:
        print(f"[OpenSCAD] View updated ({png_file})")
    else:
        print(f"[OpenSCAD] .scad file written at {scad_file}, but preview failed (is OpenSCAD installed?)")

# --- m6: Loop/trace ---
def m6_chat_loop(proxy_url: str, model_id: str, project: str = "default", system_prompt: str = None, max_tokens: int = 4096) -> None:
    print(f"[Llama CLI Chat] Model: {model_id}\nType 'exit' to quit.")
    while True:
        x1: str = m1_get_user_prompt()
        if x1.strip().lower() == "exit":
            print("Exiting chat.")
            break
        y2: dict[str, Any] = m2_build_payload(x1, model_id, system_prompt, max_tokens)
        y3: dict[str, Any] | None = m3_call_llama_api(y2, proxy_url, mcp_server=args.mcp_server)
        y4: str | None = m4_parse_response(y3)
        print(f"Llama: {y4}")
        # If response contains OpenSCAD code, update view
        if y4 and ("module" in y4 or "cube(" in y4 or "cylinder(" in y4):
            m5_update_openscad_view(y4, project)
        # Optionally, log each step
        # snapshot.log_step(...)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Llama CLI Chat with OpenSCAD view")
    parser.add_argument("--proxy-url", default="https://llama-universal-netlify-project.netlify.app/.netlify/functions/llama-proxy", help="Netlify Llama Proxy URL (default if --mcp-server not set)")
    parser.add_argument("--mcp-server", default=None, help="MCP server base URL (if set, overrides proxy for completions)")
    parser.add_argument("--model", default="Llama-3.3-70B-Instruct", help="Llama model ID")
    parser.add_argument("--project", default="default", help="Project name for saving OpenSCAD files")
    parser.add_argument(
        "--system-prompt",
        default="You are an expert in Algebraic Pipeline Theory (APT) and OpenSCAD. When given a prompt, always return only valid OpenSCAD code in a markdown code block (```scad ... ```), with modular structure, clear variable definitions, and a short algebraic pipeline header as a comment. Do not include explanations, just the code.",
        help="System prompt to guide the Llama model for OpenSCAD code generation in strict APT modular format."
    )
    parser.add_argument("--max-tokens", type=int, default=4096, help="Maximum tokens for Llama completion (use higher for more complete code)")
    parser.add_argument("--prompt-file", default=None, help="Path to a file to use as the prompt instead of interactive input")
    args = parser.parse_args()

    if args.prompt_file:
        # Read prompt from file and run one-shot generation
        with open(args.prompt_file, "r", encoding="utf-8") as f:
            file_prompt = f.read()
        y2 = m2_build_payload(file_prompt, args.model, args.system_prompt, args.max_tokens)
        y3 = m3_call_llama_api(y2, args.proxy_url, mcp_server=args.mcp_server)
        y4 = m4_parse_response(y3)
        print(f"Llama: {y4}")
        if y4 and ("module" in y4 or "cube(" in y4 or "cylinder(" in y4):
            m5_update_openscad_view(y4, args.project)
    else:
        global args
        m6_chat_loop(args.proxy_url, args.model, args.project, args.system_prompt, args.max_tokens)
