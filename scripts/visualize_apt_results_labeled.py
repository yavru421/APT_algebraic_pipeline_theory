"""
Enhanced APT Screenshot Output Visualization
- Displays full variable/component names on graph nodes
- Adds a legend mapping variables to descriptions
- Produces improved graph images and a PDF report
"""
import os
import json
import glob
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import re

def extract_labels_and_graph(apt_text):
    """Extracts variable labels and relationships from APT output text."""
    labels = {}
    nodes = set()
    edges = []
    # Extract variable definitions (e.g., - **Editor Window**: \(E\))
    for match in re.findall(r'- \*\*([^:]+)\*\*: \\?\(([^)]+)\\?\)', apt_text):
        label, var = match
        var = var.strip()
        label = label.strip()
        if var and label:
            labels[var] = label
            nodes.add(var)
    # Fallback: also extract variables from equations
    for match in re.findall(r'\\\(([^)]+)\\\)', apt_text):
        for var in re.split(r',| ', match):
            var = var.strip()
            if var and len(var) <= 3 and var.isalnum():
                nodes.add(var)
    # Find relationships (e.g., X -> E, Adj(X, E))
    for match in re.findall(r'([A-Za-z0-9_]+) ?[\\\-\\\>]+ ?([A-Za-z0-9_]+)', apt_text):
        edges.append((match[0], match[1]))
    for match in re.findall(r'Adj\\\(([^,]+), ([^)]+)\\\)', apt_text):
        edges.append((match[0], match[1]))
    return labels, list(nodes), edges

def visualize_graph_labeled(nodes, edges, labels, title, outpath):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    plt.figure(figsize=(10,7))
    pos = nx.spring_layout(G, seed=42)
    node_labels = {n: f"{labels.get(n, n)}\n({n})" for n in nodes}
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_color='skyblue', node_size=1800, font_size=11, edge_color='gray', arrows=True)
    plt.title(title)
    # Draw legend
    if labels:
        legend_text = "Legend:\n" + "\n".join([f"{v}: {l}" for v, l in labels.items()])
        plt.gcf().text(0.01, 0.01, legend_text, fontsize=9, va='bottom', ha='left', bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray'))
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def main():
    results_dir = "results"
    out_pdf = "apt_screenshot_visualizations_labeled.pdf"
    result_files = glob.glob(os.path.join(results_dir, '*_apt_result.json'))
    pdf = PdfPages(out_pdf)
    for rf in result_files:
        with open(rf, 'r') as f:
            data = json.load(f)
        apt_text = data["y_5"]["completion_message"]["content"]["text"]
        labels, nodes, edges = extract_labels_and_graph(apt_text)
        img_title = os.path.basename(data["image"])
        img_out = rf.replace(".json", "_graph_labeled.png")
        visualize_graph_labeled(nodes, edges, labels, f"APT Graph: {img_title}", img_out)
        # Add to PDF
        plt.figure(figsize=(10,7))
        plt.imshow(plt.imread(img_out))
        plt.axis('off')
        plt.title(f"APT Graph: {img_title}")
        pdf.savefig()
        plt.close()
    pdf.close()
    print(f"Enhanced visualization complete. See {out_pdf} and *_graph_labeled.png in results/.")

if __name__ == "__main__":
    main()
