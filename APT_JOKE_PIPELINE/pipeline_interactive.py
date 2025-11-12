import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'APT_MODULES')))
from m6_context_manager import m6_context_manager, load_context
"""
APT Joke Generator Pipeline (Interactive)

Pipeline equation:
y_joke_n = m5(m4(m3(m2(m1(m0(x0_n)), x2))))
Contract:
  Inputs: x0_n: audio (microphone, n-th input), x2: llama API config
  Outputs: y_joke_n: str (final joke)
  Loop: After joke, listen to user reaction (x0_{n+1}), use as next prompt
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'APT_MODULES')))
from m0_speech_to_text import m0_speech_to_text
import requests
import pyttsx3

LLAMA_API_URL = "https://llama-universal-netlify-project.netlify.app/.netlify/functions/llama-proxy?path=/chat/completions"
MODEL = "Llama-3.3-8B-Instruct"

def m1_preprocess_input(x1):
    return x1.strip() if x1 else None

def m2_build_payload(x1, x2):
    # Load context for system instructions
    from m6_context_manager import load_context
    context = load_context()
    previous_jokes = [entry["joke"] for entry in context if "joke" in entry]
    system_prompt = (
        "You are a world-class joke-telling assistant. "
        "Always respond with a joke, even if the user doesn't explicitly ask for one. "
        "Never repeat any previous jokes. "
        f"Here are previous jokes to avoid: {previous_jokes}. "
        "If the user seems bored or doesn't react, try a new style or topic. "
        "If the user asks for another, give a fresh joke. "
        "If the user gives a conversational input, respond with a joke relevant to their context."
    )
    return {
        "model": x2["model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": x1}
        ]
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

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    x2 = {"model": MODEL}
    print("Welcome to the APT Llama Joke Generator!")
    y_context = load_context()
    prompt = None
    while True:
        if prompt:
            print("Listening to your reaction for the next joke...")
        else:
            print("Please say your joke topic or prompt:")
        x0 = m0_speech_to_text()
        x1 = m1_preprocess_input(x0)
        payload = m2_build_payload(x1, x2)
        api_response = m3_call_llama_api(payload)
        joke = m4_parse_response(api_response)
        y_joke = m5_postprocess_joke(joke)
        print(y_joke)
        speak_text(joke)
        # Update context after each joke
        y_context = m6_context_manager(y_context, x1, joke)
        prompt = joke  # Use joke or reaction as next prompt

if __name__ == "__main__":
    main()
