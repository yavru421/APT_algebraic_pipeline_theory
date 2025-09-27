import os
import threading
import json
import flet
from flet import Page, TextField, ElevatedButton, Column, Row, Text, Card, ProgressBar

from pathlib import Path

# Import pipeline functions
from apt_curl_3 import m_1_build_payload, m_2_call_api


def run_pipeline(api_key, endpoint, instruction, paragraph, out_ctrl, debug=False):
    headers = {
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    user_content = f"{instruction}\nParagraph: {paragraph}"
    payload = m_1_build_payload(
        "You are an algebraic pipeline executor. Structure responses as execution logs.", user_content
    )
    resp = m_2_call_api(endpoint, headers, payload)
    if resp is None:
        out_ctrl.value += "\n[ERROR] API call failed or returned no response."
        out_ctrl.update()
        return

    for line in resp.iter_lines():
        if not line:
            continue
        try:
            decoded = line.decode("utf-8")
        except Exception:
            continue
        # Update debug if needed
        if decoded.startswith("data:"):
            decoded = decoded[5:].strip()
        try:
            obj = json.loads(decoded)
            ev = obj.get("event")
            if isinstance(ev, dict) and ev.get("event_type") == "progress":
                text = ev.get("delta", {}).get("text", "")
                if text:
                    out_ctrl.value += text
                    out_ctrl.update()
        except Exception:
            # Append raw line
            out_ctrl.value += decoded + "\n"
            out_ctrl.update()


def main(page: Page):
    page.title = "APT Flet GUI"
    page.vertical_alignment = "start"

    api_key_field = TextField(label="LLAMA_API_KEY", width=600, password=True)
    endpoint_field = TextField(label="Endpoint", value=os.getenv("LLAMA_ENDPOINT", "https://api.llama.com/v1/chat/completions"), width=600)
    instruction_field = TextField(label="Instruction", multiline=True, value="Analyze the paragraph for key arguments.", width=600, height=80)
    paragraph_field = TextField(label="Paragraph", multiline=True, value="Paste paragraph here...", width=600, height=160)
    output_text = Text(value="", selectable=True)

    def on_run(e):
        api_key = api_key_field.value or os.getenv("LLAMA_API_KEY")
        if not api_key:
            output_text.value = "[ERROR] Provide LLAMA_API_KEY"
            output_text.update()
            return
        endpoint = endpoint_field.value
        instruction = instruction_field.value
        paragraph = paragraph_field.value

        output_text.value = "[LOG] Starting run...\n"
        output_text.update()

        t = threading.Thread(target=run_pipeline, args=(api_key, endpoint, instruction, paragraph, output_text), daemon=True)
        t.start()

    run_btn = ElevatedButton(text="Run", on_click=on_run)

    page.add(
        Column([
            api_key_field,
            endpoint_field,
            instruction_field,
            paragraph_field,
            Row([run_btn]),
            Card(content=Column([Text("Output:"), output_text]), width=800)
        ])
    )


if __name__ == "__main__":
    flet.app(target=main)
