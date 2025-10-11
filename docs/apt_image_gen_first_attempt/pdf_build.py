import sys
from pathlib import Path
import markdown

INPUT_MD = Path('APT_Image_Generation_Tests.md')
OUTPUT_HTML = Path('APT_Image_Generation_Tests.html')
OUTPUT_PDF = Path('APT_Image_Generation_Report.pdf')

if not INPUT_MD.exists():
    print(f"Missing {INPUT_MD}")
    sys.exit(1)

md_text = INPUT_MD.read_text(encoding='utf-8')
html = markdown.markdown(md_text, extensions=['fenced_code', 'tables', 'toc', 'attr_list'])

# Wrap with basic HTML and inline CSS for print
full_html = ('<!doctype html>\n'
             '<html>\n'
             '<head>\n'
             '<meta charset="utf-8">\n'
             '<title>APT Image Generation Tests</title>\n'
             '<style>\n'
             'body { font-family: Arial, Helvetica, sans-serif; padding: 24px; color: #111 }\n'
             'h1,h2,h3 { color: #222 }\n'
             'img { max-width: 100%; height: auto; display:block; margin: 12px 0 }\n'
             '.code { background:#f6f8fa; padding:8px; border-radius:4px }\n'
             '</style>\n'
             '</head>\n'
             '<body>\n') + html + '\n</body>\n</html>\n'

OUTPUT_HTML.write_text(full_html, encoding='utf-8')
print(f"Wrote {OUTPUT_HTML}")

# Attempt to use weasyprint if available
try:
    from weasyprint import HTML
    HTML(string=full_html, base_url=str(Path('.').resolve())).write_pdf(OUTPUT_PDF)
    print(f"Wrote {OUTPUT_PDF}")
except Exception as e:
    print("WeasyPrint not available or failed to render PDF:", e)
    print("You can convert the generated HTML to PDF using your browser or install WeasyPrint (pip install weasyprint).")
