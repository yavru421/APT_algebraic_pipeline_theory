#!/usr/bin/env python3
"""
Simple Markdown cleanup utility for repo docs/ folder.

Fixes applied (deterministic, conservative):
 - Convert emphasis-only lines like "**Heading**" to "# Heading"
 - Remove leading spaces before headings so headings start at column 0
 - Convert lines starting with a dash+space to asterisk list markers at column 0
 - Ensure a single blank line precedes each heading
 - Skip changes inside fenced code blocks (```)

Run from repo root: python scripts/md_cleanup.py
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'

def clean_file(p: Path) -> bool:
    text = p.read_text(encoding='utf-8')
    lines = text.splitlines()
    out = []
    in_fence = False
    changed = False
    for i, line in enumerate(lines):
        orig = line
        # detect fence start/end
        if re.match(r"^```", line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        # Convert emphasis-only headings: **Heading** -> # Heading
        m = re.match(r"^\s*\*\*(.+?)\*\*\s*$", line)
        if m:
            new = '# ' + m.group(1).strip()
            if new != line:
                line = new
                changed = True

        # Remove leading spaces before headings (ensure heading starts at col 0)
        if re.match(r"^\s+#", line):
            new = re.sub(r"^\s+(#.*)$", r"\1", line)
            if new != line:
                line = new
                changed = True

        # Convert ' - ' list markers at line start to '* '
        if re.match(r"^\s*-\s+", line):
            new = re.sub(r"^\s*-\s+", '* ', line)
            if new != line:
                line = new
                changed = True

        out.append(line)

    # Ensure blank line before headings
    final = []
    for idx, line in enumerate(out):
        if re.match(r"^#{1,6} ", line):
            if idx > 0 and final and final[-1].strip() != '':
                final.append('')
                changed = True
        final.append(line)

    if changed:
        p.write_text('\n'.join(final) + '\n', encoding='utf-8')
    return changed

def main():
    if not DOCS.exists():
        print('No docs/ folder found; aborting')
        return
    files = list(DOCS.rglob('*.md'))
    touched = []
    for f in files:
        try:
            if clean_file(f):
                touched.append(str(f.relative_to(ROOT)))
        except Exception as e:
            print('Error processing', f, e)
    print('Files modified:', len(touched))
    for t in touched:
        print('- ', t)

if __name__ == '__main__':
    main()
