import matplotlib.patches as mpatches
import matplotlib.image as mpimg

def visualize_annotated_image(json_data, apt_text, title, outpath_base, pdf=None):
    # Load screenshot image
    img_path = json_data.get("image")
    if not img_path:
        return
    img_path_full = os.path.join(os.path.dirname(__file__), img_path.replace("\\", os.sep))
    if not os.path.exists(img_path_full):
        return
    img = mpimg.imread(img_path_full)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(img)
    ax.axis('off')
    # Parse component definitions
    component_types = {
        'Menus': 'tab:blue',
        'Buttons': 'tab:green',
        'Icons': 'tab:orange',
        'Text Fields': 'tab:red',
        'Other Components': 'tab:purple'
    }
    # Find components in apt_text
    comp_map = {}
    current_type = None
    for line in apt_text.splitlines():
        line = line.strip()
        if line.startswith('*') and 'Menus' in line:
            current_type = 'Menus'
        elif line.startswith('*') and 'Buttons' in line:
            current_type = 'Buttons'
        elif line.startswith('*') and 'Icons' in line:
            current_type = 'Icons'
        elif line.startswith('*') and 'Text Fields' in line:
            current_type = 'Text Fields'
        elif line.startswith('*') and 'Other Components' in line:
            current_type = 'Other Components'
        elif line.startswith('+') and current_type:
            # e.g., + $M_1$: File
            m = re.match(r'\$([A-Za-z0-9_]+)\$: (.+)', line)
            if m:
                comp_map[m.group(1)] = (m.group(2), current_type)
    # Place boxes/labels for each component type
    # Use plausible regions: Menus (top), Buttons (left), Icons (center), Text Fields (top right), Other (bottom)
    regions = {
        'Menus': (0.05, 0.05, 0.9, 0.08),
        'Buttons': (0.01, 0.15, 0.15, 0.7),
        'Icons': (0.45, 0.45, 0.1, 0.1),
        'Text Fields': (0.8, 0.05, 0.15, 0.08),
        'Other Components': (0.7, 0.8, 0.25, 0.15)
    }
    img_h, img_w = img.shape[0], img.shape[1]
    type_counts = {k:0 for k in component_types}
    for comp, (desc, ctype) in comp_map.items():
        color = component_types.get(ctype, 'gray')
        # Place in region for type, offset by count
        rx, ry, rw, rh = regions[ctype]
        # Offset for each component
        offset = type_counts[ctype]
        max_per_row = 6
        x = rx + (rw/max_per_row)*(offset%max_per_row)
        y = ry + (rh//max_per_row)*(offset//max_per_row)
        rect = mpatches.Rectangle((x*img_w, y*img_h), rw*img_w/max_per_row, rh*img_h//max_per_row, linewidth=2, edgecolor=color, facecolor=color, alpha=0.3)
        ax.add_patch(rect)
        ax.text(x*img_w+5, y*img_h+15, f"{comp}: {desc}", color='black', fontsize=12, weight='bold', bbox=dict(facecolor=color, alpha=0.5, boxstyle='round,pad=0.2'))
        type_counts[ctype] += 1
    # Add legend
    legend_patches = [mpatches.Patch(color=c, label=t) for t, c in component_types.items()]
    ax.legend(handles=legend_patches, loc='lower right', fontsize=12)
    plt.title(f"{title} - Annotated Components")
    plt.tight_layout()
    out_img = f"{outpath_base}_annotated.png"
    print(f"[APT] Saving annotated image: {out_img}")
    plt.savefig(out_img)
    if os.path.exists(out_img):
        print(f"[APT] Annotated image saved: {out_img}")
    else:
        print(f"[APT] ERROR: Annotated image NOT saved: {out_img}")
    if pdf is not None:
        pdf.savefig(fig)
    plt.close(fig)
import os
import json
import glob

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import numpy as np
import re

def extract_graph_from_apt_text(apt_text):
    # Only extract variables, dependencies, equations for table/heatmap/outliner. No node-based graph code remains.
    variables = set()
    dependencies = []
    equations = []
    eq_matches = re.findall(r'([A-Za-z0-9_]+) ?= ?([A-Za-z0-9_]+)\\?\(([^)]*)\\?\)', apt_text)
    for target, func, args in eq_matches:
        sources = [a.strip() for a in args.split(',') if a.strip()]
        variables.add(target)
        variables.update(sources)
        dependencies.append((target, sources))
        equations.append(f"{target} = {func}({', '.join(sources)})")
    for match in re.findall(r'\\\(([^)]+)\\\)', apt_text):
        for var in re.split(r',| ', match):
            var = var.strip()
            if var and len(var) <= 3 and var.isalnum():
                variables.add(var)
    for match in re.findall(r'([A-Za-z0-9_]+) ?[\\\-\\\>]+ ?([A-Za-z0-9_]+)', apt_text):
        variables.add(match[0])
        variables.add(match[1])
        dependencies.append((match[1], [match[0]]))
    for match in re.findall(r'Adj\\\(([^,]+), ([^)]+)\\\)', apt_text):
        variables.add(match[0])
        variables.add(match[1])
        dependencies.append((match[1], [match[0]]))
    return sorted(variables), dependencies, equations


def visualize_table_and_heatmap(variables, dependencies, equations, title, outpath_base, pdf=None):
    # Build dependency table
    dep_table = []
    for target, sources in dependencies:
        dep_table.append({"Variable": target, "Depends On": ', '.join(sources) if sources else "-"})
    df = pd.DataFrame(dep_table)
    # Build dependency matrix
    var_idx = {v: i for i, v in enumerate(variables)}
    matrix = np.zeros((len(variables), len(variables)), dtype=int)
    for target, sources in dependencies:
        for s in sources:
            if s in var_idx and target in var_idx:
                matrix[var_idx[target], var_idx[s]] = 1
    # Plot table
    fig, ax = plt.subplots(figsize=(max(6, len(variables)), 0.5*len(variables)+2))
    ax.axis('off')
    tbl = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1.2, 1.2)
    plt.title(f"{title} - Dependency Table")
    plt.tight_layout()
    table_img = f"{outpath_base}_table.png"
    print(f"[APT] Saving table image: {table_img}")
    plt.savefig(table_img)
    if os.path.exists(table_img):
        print(f"[APT] Table image saved: {table_img}")
    else:
        print(f"[APT] ERROR: Table image NOT saved: {table_img}")
    if pdf is not None:
        pdf.savefig(fig)
    plt.close(fig)
    # Plot heatmap
    fig, ax = plt.subplots(figsize=(max(6, len(variables)), max(6, len(variables))))
    im = ax.imshow(matrix, cmap='Blues', interpolation='nearest')
    ax.set_xticks(np.arange(len(variables)))
    ax.set_yticks(np.arange(len(variables)))
    ax.set_xticklabels(variables, rotation=90)
    ax.set_yticklabels(variables)
    plt.xlabel('Depends On')
    plt.ylabel('Variable')
    plt.title(f"{title} - Dependency Matrix Heatmap")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()
    heatmap_img = f"{outpath_base}_heatmap.png"
    print(f"[APT] Saving heatmap image: {heatmap_img}")
    plt.savefig(heatmap_img)
    if os.path.exists(heatmap_img):
        print(f"[APT] Heatmap image saved: {heatmap_img}")
    else:
        print(f"[APT] ERROR: Heatmap image NOT saved: {heatmap_img}")
    if pdf is not None:
        pdf.savefig(fig)
    plt.close(fig)
    # (Optional) Render equations as text
    if equations:
        fig, ax = plt.subplots(figsize=(max(6, len(equations)), 1+0.5*len(equations)))
        ax.axis('off')
        eq_text = '\n'.join(equations)
        ax.text(0.01, 0.99, eq_text, fontsize=14, va='top', ha='left', family='monospace')
        plt.title(f"{title} - Equations")
        plt.tight_layout()
        eq_img = f"{outpath_base}_equations.png"
        print(f"[APT] Saving equations image: {eq_img}")
        plt.savefig(eq_img)
        if os.path.exists(eq_img):
            print(f"[APT] Equations image saved: {eq_img}")
        else:
            print(f"[APT] ERROR: Equations image NOT saved: {eq_img}")
        if pdf is not None:
            pdf.savefig(fig)
        plt.close(fig)

def extract_outliner_from_apt_text(apt_text):
    """Extracts a simple outliner (indented text) from the APT output text."""
    lines = []
    in_components = False
    in_relationships = False
    for line in apt_text.splitlines():
        if line.strip().startswith('### Component Definitions'):
            in_components = True
            in_relationships = False
            continue
        if line.strip().startswith('### Algebraic Relationships'):
            in_components = False
            in_relationships = True
            continue
        if line.strip().startswith('###'):
            in_components = False
            in_relationships = False
        if in_components:
            if line.strip().startswith('*') or line.strip().startswith('+'):
                lines.append(line.strip())
            elif line.strip().startswith('$'):
                lines.append('  ' + line.strip())
        if in_relationships:
            if line.strip().startswith('*') or line.strip().startswith('+'):
                lines.append(line.strip())
            elif line.strip().startswith('$'):
                lines.append('  ' + line.strip())
    return '\n'.join(lines)

def visualize_outliner(apt_text, title, outpath_base, pdf=None):
    outline = extract_outliner_from_apt_text(apt_text)
    # Save as plain text
    outline_txt = f"{outpath_base}_outline.txt"
    print(f"[APT] Saving outline text: {outline_txt}")
    with open(outline_txt, 'w', encoding='utf-8') as f:
        f.write(f"{title}\n\n{outline}\n")
    if os.path.exists(outline_txt):
        print(f"[APT] Outline text saved: {outline_txt}")
    else:
        print(f"[APT] ERROR: Outline text NOT saved: {outline_txt}")
    # Also render as a PDF page (monospace text)
    fig, ax = plt.subplots(figsize=(10, min(20, 2+0.3*outline.count('\n'))))
    ax.axis('off')
    ax.text(0.01, 0.99, outline, fontsize=13, va='top', ha='left', family='monospace')
    plt.title(f"{title} - Outliner")
    plt.tight_layout()
    outline_img = f"{outpath_base}_outline.png"
    print(f"[APT] Saving outline image: {outline_img}")
    plt.savefig(outline_img)
    if os.path.exists(outline_img):
        print(f"[APT] Outline image saved: {outline_img}")
    else:
        print(f"[APT] ERROR: Outline image NOT saved: {outline_img}")
    if pdf is not None:
        pdf.savefig(fig)
    plt.close(fig)

def main():
    results_dir = "results"
    out_pdf = "apt_screenshot_visualizations.pdf"
    result_files = glob.glob(os.path.join(results_dir, '*_apt_result.json'))
    pdf = PdfPages(out_pdf)
    for rf in result_files:
        with open(rf, 'r') as f:
            data = json.load(f)
            apt_text = data["y_5"]["completion_message"]["content"]["text"]
            variables, dependencies, equations = extract_graph_from_apt_text(apt_text)
            img_title = os.path.basename(data["image"])
            outpath_base = rf.replace(".json", "_viz")
            # Annotated image visualization
            visualize_annotated_image(data, apt_text, f"APT: {img_title}", outpath_base, pdf=pdf)
            # Outliner visualization
            visualize_outliner(apt_text, f"APT: {img_title}", outpath_base, pdf=pdf)
            # Table/heatmap as before
            visualize_table_and_heatmap(variables, dependencies, equations, f"APT: {img_title}", outpath_base, pdf=pdf)
    pdf.close()
    print(f"Visualization complete. See {out_pdf} and *_viz_*.png and *_viz_outline.txt in results/.")

if __name__ == "__main__":
    main()
