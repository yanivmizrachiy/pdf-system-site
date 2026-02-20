from pathlib import Path
import json, sys, re

def die(msg, code=2):
    print("FAIL:", msg)
    raise SystemExit(code)

# must-exist files
must = [
  "docs/index.html",
  "docs/print.css",
  "docs/manifest.webmanifest",
  "docs/sw.js",
  "docs/icons/icon-192.png",
  "docs/icons/icon-512.png",
  "docs/version.json",
  "RULES.md",
  "STATUS.md",
]
missing = [f for f in must if not Path(f).exists()]
if missing: die("missing: " + ", ".join(missing))

# pages exist
pages = sorted(Path("docs/pages").glob("page-*.html"))
if not pages: die("no docs/pages/page-*.html found")

# forbid inline css in pages (כדי לשמור אחידות עיצוב)
for p in pages:
    s = p.read_text(encoding="utf-8", errors="ignore")
    if "<style" in s or "style=" in s:
        die(f"inline css forbidden in {p}")

# each page must link print.css (A4 אחיד)
for p in pages:
    s = p.read_text(encoding="utf-8", errors="ignore")
    if href=../print.css not in s and href=../print.css not in s.replace(" ", ""):
        die(f"page missing ../print.css link: {p}")

# manifest correctness
m = json.loads(Path("docs/manifest.webmanifest").read_text(encoding="utf-8"))
if m.get("scope") != "/pdf-system-site/": die("manifest.scope must be /pdf-system-site/")
if m.get("start_url") != "/pdf-system-site/?pwa=1": die("manifest.start_url must be /pdf-system-site/?pwa=1")
icons = m.get("icons") or []
need = {"/pdf-system-site/icons/icon-192.png", "/pdf-system-site/icons/icon-512.png"}
have = {i.get("src") for i in icons if isinstance(i, dict)}
if not need.issubset(have): die("manifest.icons missing required paths")

# index must contain manifest link
idx = Path("docs/index.html").read_text(encoding="utf-8", errors="ignore")
if "manifest.webmanifest" not in idx: die("index missing manifest link")

print("OK validate_site")
