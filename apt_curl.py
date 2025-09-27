import requests
import os

"""
Lightweight example showing how to call the Llama endpoint.
This file is kept for historical reasons — prefer `apt_curl_3.py` which is safer and
parameterized.

Usage:
  Set environment variable `LLAMA_API_KEY` and run `python apt_curl_3.py`
"""

def main():
    api_key = os.getenv("LLAMA_API_KEY")
    if not api_key:
        print("[ERROR] LLAMA_API_KEY not set. See README or run.ps1 for instructions.")
        return
    endpoint = os.getenv("LLAMA_ENDPOINT", "https://api.llama.com/v1/chat/completions")
    headers = {
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    apt_system_instructions = (
        "You are an algebraic pipeline executor. "
        "Interpret all tasks as modular pipeline steps, with explicit variable definitions, "
        "dependency resolution, and algebraic notation. "
        "Structure responses as algebraic pipeline definitions and execution logs."
    )
    payload = {
        "messages": [
            {"role": "system", "content": apt_system_instructions},
        ],
        "model": "Llama-4-Maverick-17B-128E-Instruct-FP8",
        "repetition_penalty": 1,
        "temperature": 0.6,
        "top_p": 0.9,
        "max_completion_tokens": 2048,
        "stream": True
    }
    response = requests.post(endpoint, headers=headers, json=payload, stream=True)
    for line in response.iter_lines():
        if line:
            print(line.decode("utf-8"))


if __name__ == "__main__":
    main()