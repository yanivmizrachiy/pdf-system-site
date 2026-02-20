from pathlib import Path
import json, re, sys

need = [
  "docs/index.html",
  "docs/print.css",
  "docs/manifest.webmanifest",
  "docs/sw.js",
  "docs/icons/icon-192.png",
  "docs/icons/icon-512.png",
]
missing = [f for f in need if not Path(f).exists()]
if missing:
  raise SystemExit("MISSING: " + ", ".join(missing))

# pages must exist
pages = sorted(Path("docs/pages").glob("page-*.html"))
if not pages:
  raise SystemExit("MISSING: docs/pages/page-*.html")

# forbid inline CSS in page files (שלא יתפוצץ עיצוב אחיד)
for p in pages:
  s = p.read_text(encoding="utf-8", errors="ignore")
  if "<style" in s or "style=" in s:
    raise SystemExit(f"INLINE_CSS_FORBIDDEN: {p}")

# manifest must point to correct scope/start_url and icon paths
m = json.loads(Path("docs/manifest.webmanifest").read_text(encoding="utf-8"))
if m.get("scope") != "/pdf-system-site/":
  raise SystemExit("BAD_MANIFEST_SCOPE")
if m.get("start_url") != "/pdf-system-site/?pwa=1":
  raise SystemExit("BAD_MANIFEST_START_URL")

icons = m.get("icons", [])
srcs = [i.get("src","") for i in icons]
if "/pdf-system-site/icons/icon-192.png" not in srcs or "/pdf-system-site/icons/icon-512.png" not in srcs:
  raise SystemExit("BAD_MANIFEST_ICONS")

# index must reference manifest + sw (ליציבות אייקון)
idx = Path("docs/index.html").read_text(encoding="utf-8", errors="ignore")
if "manifest.webmanifest" not in idx:
  raise SystemExit("INDEX_MISSING_MANIFEST_LINK")
if "navigator.serviceWorker" not in idx:
  raise SystemExit("INDEX_MISSING_SW_REGISTER")

print("OK validate_site")
