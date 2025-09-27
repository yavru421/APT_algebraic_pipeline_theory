"""
APT Image Methods Test Suite
- Runs APT modular analysis on all images in examples/
- Extracts and saves algebraic variables, modules, and relationships
- Outputs results for APT method evaluation
"""
import os
import json
import glob
from pipeline import base64_encode_image, build_payload

def extract_apt_variables(text):
    """Extracts candidate APT variables/components from model output text."""
    # Simple heuristic: look for key phrases, bullet points, or bolded items
    import re
    variables = set()
    # Find bolded or starred items
    variables.update(re.findall(r'\*\*([A-Za-z0-9 _-]+)\*\*', text))
    variables.update(re.findall(r'\* ([A-Za-z0-9 _-]+):', text))
    # Find capitalized words at start of lines
    variables.update(re.findall(r'^([A-Z][A-Za-z0-9 _-]+):', text, re.MULTILINE))
    return list(variables)

def main():
    examples_dir = "examples"
    graph_path = "apt_graph.json"
    output_path = "apt_methods_results.json"
    # Load graph outputs
    with open(graph_path, 'r') as f:
        graph = json.load(f)
    results = []
    for node in graph["nodes"]:
        image = node["image"]
        output = node["output"]
        text = output["completion_message"]["content"]["text"]
        variables = extract_apt_variables(text)
        results.append({
            "image": image,
            "variables": variables,
            "raw_text": text
        })
        print(f"Image: {image}\nAPT Variables: {variables}\n---\n{text}\n{'='*40}")
    # Save results
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nAPT method extraction complete. Results saved to {output_path}.")

if __name__ == "__main__":
    main()
