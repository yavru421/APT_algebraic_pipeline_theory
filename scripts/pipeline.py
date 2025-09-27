"""
APT Screenshot Pipeline: Modular, algebraic pipeline for screenshot understanding using Llama Chat Completions API
"""
import os
import json
import glob
import base64
import requests

def base64_encode_image(image_path):
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def build_payload(y_2, apt_prompt, model):
    return {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": apt_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{y_2}"}}
                ],
                "system_instructions": apt_prompt
            }
        ]
    }

def call_api(y_3, api_url, bearer_token):
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(api_url, json=y_3, headers=headers)
    return response

def parse_response(y_4):
    try:
        return y_4.json()
    except Exception:
        return y_4.text

def main():
    examples_dir = "examples"
    results_dir = "results"
    apt_prompt = "Apply Algebraic Pipeline Theory (APT) to this screenshot. Decompose the UI into modular, indexable components (buttons, menus, text fields, icons, etc.), define explicit variables for each, and describe their algebraic and hierarchical relationships (e.g., containment, adjacency, event flow). Output the analysis as an algebraic pipeline trace."
    model = "Llama-4-Scout-17B-16E-Instruct-FP8"
    api_url = "https://api.llama.com/v1/chat/completions"
    bearer_token = os.environ.get('LLAMA_API_KEY')
    if not bearer_token:
        print("Bearer token not provided. Set LLAMA_API_KEY env var.")
        return
    os.makedirs(results_dir, exist_ok=True)
    imgs = glob.glob(os.path.join(examples_dir, '*.*'))
    for img_path in imgs:
        y_2 = base64_encode_image(img_path)
        y_3 = build_payload(y_2, apt_prompt, model)
        # Remove base64 from y_3 for output
        y_3_no_b64 = json.loads(json.dumps(y_3))
        try:
            for msg in y_3_no_b64["messages"]:
                for part in msg["content"]:
                    if part.get("type") == "image_url" and "url" in part["image_url"]:
                        part["image_url"]["url"] = "<base64 omitted>"
        except Exception:
            pass
        y_4 = call_api(y_3, api_url, bearer_token)
        y_5 = parse_response(y_4)
        result = {
            "image": img_path,
            "apt_prompt": apt_prompt,
            "model": model,
            "y_3": y_3_no_b64,
            "y_5": y_5
        }
        out_file = os.path.join(results_dir, os.path.basename(img_path) + "_apt_result.json")
        with open(out_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Processed {img_path} -> {out_file}")

if __name__ == "__main__":
    main()
