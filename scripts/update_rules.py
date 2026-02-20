from pathlib import Path

INSTALL_URL = "https://yanivmizrachiy.github.io/pdf-system-site/?pwa=1#page-1"

p = Path("RULES.md")
base = p.read_text(encoding="utf-8", errors="ignore") if p.exists() else "# RULES — pdf-system-site\n\n"

b = "<!-- AUTO:INVARIANTS:BEGIN -->"
e = "<!-- AUTO:INVARIANTS:END -->"

block = f"""{b}
## עקרונות שאסור לשבור (חובה)
- זה פרויקט **דפי עבודה להדפסה (A4)**. האתר הוא מעטפת לפתיחה והדפסה.
- האייקון בנייד מותקן רק מהקישור הקבוע (לא לשנות לעולם):
  - {INSTALL_URL}
- אסור לשנות לעולם:
  - `docs/manifest.webmanifest` → `start_url` חייב להישאר `/pdf-system-site/?pwa=1`
  - `docs/manifest.webmanifest` → `scope` חייב להישאר `/pdf-system-site/`
  - אייקונים חייבים להישאר:
    - `/pdf-system-site/icons/icon-192.png`
    - `/pdf-system-site/icons/icon-512.png`
  - קבצים שחייבים להישאר קיימים: `docs/sw.js`, `docs/print.css`, `docs/print-helper.js`
- לכל דף `docs/pages/page-*.html` חייב להיות כפתור **PDF / הדפסה** ועיצוב Print-first (`.page` + `print.css`).
- Gate אוטומטי: Workflow בשם **Site Guard** חייב להיות ירוק לפני שסומכים על עדכון.
{e}
"""

if b in base and e in base:
    pre = base.split(b)[0].rstrip()
    post = base.split(e)[1].lstrip()
    out = pre + "\n\n" + block + "\n" + post
else:
    out = base.rstrip() + "\n\n" + block + "\n"

p.write_text(out, encoding="utf-8")
print("OK RULES updated")
