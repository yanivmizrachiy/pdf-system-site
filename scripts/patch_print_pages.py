from pathlib import Path
import re

pages = sorted(Path("docs/pages").glob("page-*.html"))
if not pages:
    raise SystemExit("NO pages found: docs/pages/page-*.html")

BTN = (
    "<button class=\"no-print\" onclick=\"window.print()\" "
    "style=\"position:fixed;left:12px;top:12px;z-index:9999;"
    "padding:10px 14px;border:0;border-radius:10px;"
    "font-weight:700;box-shadow:0 6px 16px rgba(0,0,0,.18);"
    "background:#0b4aa2;color:#fff\">PDF / הדפסה</button>"
)

def ensure_print_css(html: str) -> str:
    if "print.css" in html:
        return html
    return re.sub(r"</head>", "  <link rel=\"stylesheet\" href=\"../print.css\">\\n</head>", html, flags=re.I)

def ensure_button(html: str) -> str:
    if "window.print()" in html:
        return html
    return re.sub(r"(<body[^>]*>)", r"\\1\\n  " + BTN + "\\n", html, flags=re.I)

def ensure_page_wrapper(html: str) -> str:
    if "class=\"page\"" in html:
        return html
    html = re.sub(r"(<body[^>]*>)", r"\\1\\n  <div class=\"page\">", html, flags=re.I)
    html = re.sub(r"</body>", "  </div>\\n</body>", html, flags=re.I)
    return html

changed = 0
for p in pages:
    s = p.read_text(encoding="utf-8", errors="ignore")
    s2 = ensure_page_wrapper(ensure_button(ensure_print_css(s)))
    if s2 != s:
        p.write_text(s2, encoding="utf-8")
        changed += 1

print(f"OK patched pages={len(pages)} changed={changed}")
