"""
APT Super MCP Server with Interactive Web UI

- On startup, scans context folder and system info, then greets user in browser.
- User can type instructions in a web input box (plain English).
- MCP server interprets and executes instructions (research, screenshot, LLM, etc).
- All actions are modular APT pipeline steps.

Usage:
  uvicorn apt_mcp_server_ui:app --reload

Requires:
  - fastapi
  - pydantic
  - requests
  - jinja2
  - (optional) pillow, pyautogui, plyer
"""

from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
import os
import platform
import datetime
import threading
import time
from typing import Any, Dict, Optional

app = FastAPI()
templates = Jinja2Templates(directory=".")

# --- m1: System/context scan on startup ---
def m1_scan_context(context_folder: str = "context") -> Dict[str, Any]:
    files = []
    if os.path.exists(context_folder):
        for fname in os.listdir(context_folder):
            if fname.endswith(".txt") or fname.endswith(".md"):
                files.append(fname)
    sysinfo = {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "cwd": os.getcwd(),
        "context_files": files
    }
    return sysinfo

# --- m2: Greet user and show input box ---
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    sysinfo = m1_scan_context()
    greeting = f"<b>Hey user, you've started APT MCP Server.</b><br>This is what I see:<br><pre>{sysinfo}</pre>"
    return templates.TemplateResponse("apt_mcp_ui.html", {"request": request, "greeting": greeting, "result": "", "screenshot": None})

# --- m3: Handle user instruction (plain English) ---
@app.post("/", response_class=HTMLResponse)
def handle_instruction(request: Request, instruction: str = Form(...), background_tasks: BackgroundTasks = None):
    # Interpret instruction (very simple, can be replaced with LLM)
    result = ""
    screenshot = None
    if "screenshot" in instruction:
        screenshot = m5_screenshot()
        result = f"Screenshot taken: {screenshot}"
    elif "research" in instruction:
        background_tasks.add_task(m7_research_loop, "context", True)
        result = "Research mode started."
    elif "llama" in instruction or "generate" in instruction:
        # For demo, just echo
        result = "LLM generation not implemented in UI demo."
    else:
        result = f"Instruction received: {instruction} (no matching module)"
    sysinfo = m1_scan_context()
    greeting = f"<b>Hey user, you've started APT MCP Server.</b><br>This is what I see:<br><pre>{sysinfo}</pre>"
    return templates.TemplateResponse("apt_mcp_ui.html", {"request": request, "greeting": greeting, "result": result, "screenshot": screenshot})

# --- m5: Screenshot module ---
def m5_screenshot() -> Optional[str]:
    try:
        from PIL import ImageGrab
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"screenshot_{ts}.png"
        img = ImageGrab.grab()
        img.save(path)
        return path
    except Exception as e:
        return None

# --- m7: Research/think module (background research loop) ---
research_memory = []
research_discoveries = set()

def m7_research_loop(context_folder: str, notify: bool = True):
    while True:
        for fname in os.listdir(context_folder):
            if fname.endswith(".txt") or fname.endswith(".md"):
                with open(os.path.join(context_folder, fname), "r", encoding="utf-8") as f:
                    content = f.read()
                    if content not in research_memory:
                        research_memory.append(content)
                        if "novel" in content or "breakthrough" in content:
                            if content not in research_discoveries:
                                research_discoveries.add(content)
                                # Notification logic could go here
        time.sleep(60)

# --- HTML template (inline for demo) ---
with open("apt_mcp_ui.html", "w", encoding="utf-8") as f:
    f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>APT MCP Server UI</title>
</head>
<body>
    <h2>APT MCP Server</h2>
    <div>{{ greeting|safe }}</div>
    <form method="post">
        <input type="text" name="instruction" style="width:400px" autofocus placeholder="Type your instruction here..."/>
        <input type="submit" value="Send"/>
    </form>
    {% if result %}<div><b>Result:</b> {{ result }}</div>{% endif %}
    {% if screenshot %}<div><img src="/{{ screenshot }}" width="400"/></div>{% endif %}
</body>
</html>
''')

# To run:
# uvicorn apt_mcp_server_ui:app --reload
