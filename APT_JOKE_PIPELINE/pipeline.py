"""
APT Joke Generator Pipeline

Pipeline equation:
y_joke = m5(m4(m3(m2(m1(m0(x0)), x2))))
Contract:
    Inputs: x0: audio (microphone), x2: llama API config
    Outputs: y_joke: str (final joke)
"""

import sys
sys.path.append('../APT_MODULES')
from m0_speech_to_text import m0_speech_to_text
import requests

LLAMA_API_URL = "https://llama-universal-netlify-project.netlify.app/.netlify/functions/llama-proxy?path=/chat/completions"
MODEL = "Llama-3.3-8B-Instruct"

def m1_preprocess_input(x1):
    # Simple preprocessing: wrap as prompt
    return x1.strip() if x1 else None

def m2_build_payload(x1, x2):
    return {
        "model": x2["model"],
        "messages": [{"role": "user", "content": x1}]
    }

def m3_call_llama_api(payload):
    resp = requests.post(LLAMA_API_URL, json=payload)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"API error: {resp.text}")
        return None

def m4_parse_response(api_response):
    if api_response and "completion_message" in api_response:
        return api_response["completion_message"]["content"]["text"]
    return "No joke returned."

def m5_postprocess_joke(joke):
    return f"Joke: {joke}\n🦙💻"

def main():
    x0 = None
    x1 = m0_speech_to_text()
    if not x1:
        print("No input transcribed.")
        return
    x1 = m1_preprocess_input(x1)
    x2 = {"model": MODEL}
    payload = m2_build_payload(x1, x2)
    api_response = m3_call_llama_api(payload)
    joke = m4_parse_response(api_response)
    y_joke = m5_postprocess_joke(joke)
    print(y_joke)

if __name__ == "__main__":
    main()
