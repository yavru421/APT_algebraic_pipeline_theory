import requests
import os
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from apt_pipeline_pkg import pipeline
from apt_pipeline_pkg.snapshot import snapshot, enabled as trace_enabled

# Explicit variable definitions (APT style)
# Note: runtime values (like API key) are loaded inside main(), not at import time
DEFAULT_ENDPOINT = "https://api.llama.com/v1/chat/completions"
DEFAULT_HEADERS_TEMPLATE = {
    "Accept": "text/event-stream",
    "Content-Type": "application/json",
}
DEFAULT_SYSTEM_INSTRUCTIONS = (
    "You are an algebraic pipeline executor. "
    "Interpret all tasks as modular pipeline steps, with explicit variable definitions, "
    "dependency resolution, and algebraic notation. "
    "Structure responses as algebraic pipeline definitions and execution logs."
)

# Modular pipeline step: build payload
def m_1_build_payload(system_instructions: str, user_message: str) -> dict:
    # y_1 = m_1(x_4, x_5)
    return {
        "messages": [
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_message}
        ],
        "model": "Llama-4-Maverick-17B-128E-Instruct-FP8",
        "repetition_penalty": 1,
        "temperature": 0.6,
        "top_p": 0.9,
        "max_completion_tokens": 2048,
        "stream": True
    }
    # snapshot payload (if enabled)
    if trace_enabled():
        try:
            snapshot(1, "m_1_build_payload", "payload", {
                "model": "Llama-4-Maverick-17B-128E-Instruct-FP8",
                "system": system_instructions,
            })
        except Exception:
            pass

# Modular pipeline step: call API
def m_2_call_api(endpoint: str, headers: dict, payload: dict, timeout: int = 30, max_retries: int = 3):
    # y_2 = m_2(x_2, x_3, y_1)
    session = requests.Session()
    retries = Retry(total=max_retries, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    try:
        response = session.post(endpoint, headers=headers, json=payload, stream=True, timeout=timeout)
        response.raise_for_status()
        if trace_enabled():
            try:
                snapshot(2, "m_2_call_api", "response_meta", {"status_code": response.status_code})
            except Exception:
                pass
        return response
    except Exception as e:
        print(f"[ERROR] API call failed: {e}")
        return None

# Modular pipeline step: process stream
import json

def m_3_process_stream(response, out_path: str = "output.txt", debug_path: str = "output_debug.txt") -> None:
    # y_3 = m_3(y_2)
    if response is None:
        print("[ERROR] No response to process.")
        return
    with open(out_path, "w", encoding="utf-8") as f, open(debug_path, "w", encoding="utf-8") as debug_f:
        for line in response.iter_lines():
            if line:
                try:
                    decoded = line.decode("utf-8")
                except Exception:
                    # skip binary/invalid lines
                    continue
                debug_f.write(decoded + "\n")
                # Correct extraction for event stream format
                try:
                    if decoded.startswith('data:'):
                        decoded = decoded[5:].strip()
                    if not decoded:
                        continue
                    obj = json.loads(decoded)
                    ev = obj.get("event")
                    if isinstance(ev, dict) and ev.get("event_type") == "progress":
                        delta = ev.get("delta", {})
                        text = delta.get("text", "")
                        if text:
                            f.write(text)
                            f.flush()
                            if trace_enabled():
                                try:
                                    snapshot(3, "m_3_process_stream", "last_chunk", text)
                                except Exception:
                                    pass
                except Exception as e:
                    # Write parse errors to debug and continue
                    debug_f.write(f"[PARSE_ERROR] {e}\n")
                    continue

# Algebraic pipeline execution log
def main():
    api_key = os.getenv("LLAMA_API_KEY")
    if not api_key:
        print("[ERROR] LLAMA_API_KEY not set in environment")
        return
    endpoint = os.getenv("LLAMA_ENDPOINT", DEFAULT_ENDPOINT)
    headers = dict(DEFAULT_HEADERS_TEMPLATE)
    headers["Authorization"] = f"Bearer {api_key}"

    print("[LOG] API key loaded")
    print("[LOG] Endpoint set")
    print("[LOG] Headers composed")

    # If tracing enabled, write the algebraic expression of the pipeline
    if trace_enabled():
        try:
            expr = pipeline.build_pipeline_expression(["m_1_build_payload", "m_2_call_api", "m_3_process_stream"])
            snapshot(0, "pipeline_expression", "expr", expr)
        except Exception:
            pass

    # Simple example run
    instruction = os.getenv("APT_INSTRUCTION") or (
        "Analyze the following paragraph for key arguments, map them to their supporting evidence, and create a concise summary suitable for a research briefing."
    )
    paragraph = os.getenv("APT_PARAGRAPH") or (
        "Artificial intelligence is transforming multiple industries by automating routine tasks, "
        "enabling new forms of human-computer collaboration, and providing unprecedented data insights. "
        "However, ethical concerns about bias, privacy, and accountability are increasingly critical. "
        "Researchers advocate for transparency in algorithms and careful monitoring of AI impacts."
    )
    user_content = f"{instruction}\nParagraph: {paragraph}"
    payload = m_1_build_payload(DEFAULT_SYSTEM_INSTRUCTIONS, user_content)
    print("[LOG] Payload built")
    response = m_2_call_api(endpoint, headers, payload)
    print("[LOG] API response received")
    m_3_process_stream(response)
    print("[LOG] Stream processed")


if __name__ == "__main__":
    main()
