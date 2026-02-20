from pathlib import Path
from datetime import datetime, timezone
import json, os

BASE="https://yanivmizrachiy.github.io/pdf-system-site"
INSTALL=f"{BASE}/?pwa=1#page-1"

now=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

tex=list(Path("sources").glob("*.tex")) if Path("sources").exists() else []
pdf=list(Path("docs/pdfs").glob("*.pdf")) if Path("docs/pdfs").exists() else []

pwa_ok=True
manifest_path=Path("docs/manifest.webmanifest")
if manifest_path.exists():
    try:
        m=json.loads(manifest_path.read_text())
        if m.get("start_url")!="/pdf-system-site/?pwa=1":
            pwa_ok=False
        if m.get("scope")!="/pdf-system-site/":
            pwa_ok=False
    except:
        pwa_ok=False
else:
    pwa_ok=False

progress=0
if pwa_ok: progress+=30
if tex: progress+=30
if pdf: progress+=30
progress+=10

rules=f"""# RULES — pdf-system-site

עודכן: {now}

## מצב מערכת
PWA תקין: {pwa_ok}
קבצי TEX: {len(tex)}
קבצי PDF: {len(pdf)}
התקדמות כללית: {progress}%

## אייקון קבוע (לא לשנות)
{INSTALL}
"""

Path("RULES.md").write_text(rules,encoding="utf-8")

status=f"""# STATUS — pdf-system-site
עודכן: {now}
התקדמות: {progress}%
"""

Path("STATUS.md").write_text(status,encoding="utf-8")

print("OK RULES+STATUS rebuilt")
