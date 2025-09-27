"""
APT Image Methods Pipeline
- Runs true APT modular analysis on all images in examples/
- Applies APT system instructions for algebraic decomposition and variable extraction
- Saves and prints results for each image
"""
import os
import json
import glob
from pipeline import base64_encode_image, build_payload, call_api, parse_response

def main():
    examples_dir = "examples"
    output_path = "apt_image_methods_results.json"
    question = "Apply Algebraic Pipeline Theory (APT) to this image. Decompose the visual content into modular, indexable components, define explicit variables for each region or object, and describe their algebraic relationships. Output the analysis as an algebraic pipeline trace."
    model = "Llama-4-Scout-17B-16E-Instruct-FP8"
    api_url = "https://api.llama.com/v1/chat/completions"
    bearer_token = os.environ.get('LLAMA_API_KEY')
    if not bearer_token:
        print("Bearer token not provided. Set LLAMA_API_KEY env var.")
        return
    # Set APT system instructions
    os.environ["APT_SYSTEM_INSTRUCTIONS"] = question
    imgs = glob.glob(os.path.join(examples_dir, '*.*'))
    results = []
    for x_2 in imgs:
        y_2 = base64_encode_image(x_2)
        y_3 = build_payload(y_2, question, model)
        y_4 = call_api(y_3, api_url, bearer_token)
        y_5 = parse_response(y_4)
        results.append({
            "image": x_2,
            "question": question,
            "model": model,
            "y_2": "<base64 omitted>",
            "y_3": y_3,
            "y_5": y_5
        })
        print(f"Image: {x_2}\nAPT Output (y_5):\n{json.dumps(y_5, indent=2) if isinstance(y_5, dict) else y_5}\n{'='*40}")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nAPT image methods pipeline complete. Results saved to {output_path}.")

if __name__ == "__main__":
    main()
