from pathlib import Path
import re

PAGES = sorted(Path("pages").glob("page-*.html"))

STYLE = """<style id="qa-pro-fix">
@page { size: A4; margin: 12mm; }
@media print { html, body { margin: 0 !important; } }
body { font-family: Arial, Heebo, Assistant, sans-serif; direction: rtl; }
</style>"""

MATHJAX = """<script>
window.MathJax = { tex: { inlineMath: [["$","$"], ["\\\\(","\\\\)"]] } };
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>"""

def ensure_html_dir_rtl(s):
    m = re.search(r"<html\b[^>]*>", s, re.I)
    if not m:
        return s
    tag = m.group(0)
    if re.search(r'\bdir\s*=\s*["\']rtl["\']', tag, re.I):
        return s
    new_tag = tag[:-1] + ' dir="rtl">'
    return s[:m.start()] + new_tag + s[m.end():]

def split_head(s):
    h1 = re.search(r"<head\b[^>]*>", s, re.I)
    h2 = re.search(r"</head\s*>", s, re.I)
    if not (h1 and h2 and h2.start() > h1.end()):
        return None
    return s[:h1.start()], h1.group(0), s[h1.end():h2.start()], s[h2.start():]

def inject_meta(head, title):
    out = head
    if not re.search(r"<meta\s+charset=", out, re.I):
        out = '<meta charset="utf-8"/>\n' + out
    if not re.search(r"<meta\s+name=[\"\']viewport[\"\']", out, re.I):
        out = '<meta name="viewport" content="width=device-width,initial-scale=1"/>\n' + out
    if not re.search(r"<title\b", out, re.I):
        safe = re.sub(r"[^0-9A-Za-z_\-\. ]+", "", title)
        out = f"<title>{safe}</title>\n" + out
    return out

def ensure_style(head):
    if 'id="qa-pro-fix"' in head:
        return head
    need = (
        "@page" not in head
        or not re.search(r"size\s*:\s*A4", head, re.I)
        or not re.search(r"@media\s+print", head, re.I)
        or "font-family" not in head
        or "direction: rtl" not in head
    )
    return head + ("\n" + STYLE + "\n" if need else "")

def ensure_mathjax(full, head):
    if "MathJax" in full:
        return head
    if "cdn.jsdelivr.net/npm/mathjax@3" in head:
        return head
    return head + "\n" + MATHJAX + "\n"

changed = 0
for p in PAGES:
    full = p.read_text(encoding="utf-8", errors="ignore")
    full2 = ensure_html_dir_rtl(full)
    sp = split_head(full2)
    if not sp:
        continue
    pre, head_open, head_inner, tail = sp
    head2 = inject_meta(head_inner, p.name)
    head2 = ensure_style(head2)
    head2 = ensure_mathjax(full2, head2)
    out = pre + head_open + head2 + tail
    if out != full:
        p.write_text(out, encoding="utf-8")
        changed += 1

print("CHANGED_PAGES:", changed, "TOTAL_PAGES:", len(PAGES))
