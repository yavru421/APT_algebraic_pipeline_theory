"""
APT Pipeline: Modular, algebraic pipeline for screenshot and image understanding using external AI APIs.
"""
import os
import json
import glob
import base64
import requests

def base64_encode_image(image_path):
def base64_encode_image(image_path: str) -> str:
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def build_payload(image_b64, apt_prompt, model):
from typing import Any
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

def call_api(payload, api_url, bearer_token):
def call_api(payload: dict[str, Any], api_url: str, bearer_token: str) -> requests.Response:
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(api_url, json=payload, headers=headers)
    return response

def parse_response(response):
def parse_response(response: requests.Response) -> dict[str, Any] | str:
    try:
        return response.json()
    except Exception:
        return response.text
