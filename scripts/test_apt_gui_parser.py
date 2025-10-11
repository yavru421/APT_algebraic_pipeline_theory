#!/usr/bin/env python3
"""
Test the APT GUI algebraic parsing functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.apt_gui_v2 import APTGUIApp

def test_rapt_parsing():
    """Test RAPT file parsing and component extraction"""

    # Test RAPT content from current file
    test_rapt = """# APT .RAPT DSL example
# Define input bindings (optional)
x1 = "netlify-llama-proxy-openapi.yaml"
x2 = "demo_image.png"

# Equation with per-call env annotations
Y = m4(base_url=m0(openapi_file=x1) @ venvA, path="/chat/completions", payload=m2(image_b64=m1(image_path=x2) @ venvA, apt_prompt="Describe the image briefly.", model="demo-model") @ venvA, dry_run=true) @ venvA"""

    app = APTGUIApp()
    app.current_rapt_content = test_rapt

    # Test parsing
    equation_match = app.current_rapt_content
    import re
    equation_match = re.search(r'Y\s*=\s*(.+)', test_rapt)

    if equation_match:
        equation = equation_match.group(1).strip()
        print(f"📐 Extracted equation: {equation}")

        components = app.parse_equation_components(equation)
        print(f"\n🔧 Parsed {len(components)} components:")

        for i, comp in enumerate(components):
            print(f"  {i+1:2d}. {comp['type']:8s} -> '{comp['text']}'")

        # Count clickable elements
        modules = [c for c in components if c['type'] == 'module']
        variables = [c for c in components if c['type'] == 'variable']

        print(f"\n🎯 Interactive Elements:")
        print(f"   📦 Modules: {len(modules)} -> {[m['text'] for m in modules]}")
        print(f"   📋 Variables: {len(variables)} -> {[v['text'] for v in variables]}")

        return True
    else:
        print("❌ No equation found in RAPT content")
        return False

if __name__ == "__main__":
    print("🚀 APT GUI Parser Test")
    print("=" * 50)

    success = test_rapt_parsing()

    print("=" * 50)
    print(f"✅ Test {'PASSED' if success else 'FAILED'}")

    # Module mapping test
    print(f"\n📂 Expected module files:")
    modules = ['m0', 'm1', 'm2', 'm4']
    for mod in modules:
        file_path = f"APT_MODULES/{mod}.py"
        exists = os.path.exists(file_path)
        print(f"   {mod} -> {file_path} {'✅' if exists else '❌'}")