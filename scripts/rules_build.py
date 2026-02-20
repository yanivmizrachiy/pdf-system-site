from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime, timezone

OWNER="yanivmizrachiy"
REPO="pdf-system-site"
BASE=f"https://{OWNER}.github.io/{REPO}"
INSTALL=f"{BASE}/?pwa=1#page-1"

REQ_FILES = [
  "docs/index.html",
  "docs/manifest.webmanifest",
  "docs/sw.js",
  "docs/print.css",
  "docs/icons/icon-192.png",
  "docs/icons/icon-512.png",
]

def now_utc():
  return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def exists(p: str) -> bool:
  return Path(p).exists()

def read_manifest():
  p = Path("docs/manifest.webmanifest")
  if not p.exists():
    return None, "missing manifest"
  try:
    return json.loads(p.read_text(encoding="utf-8")), None
  except Exception as e:
    return None, f"manifest json error: {e}"

def list_pages():
  d = Path("docs/pages")
  if not d.exists():
    return []
  return sorted([p.name for p in d.glob("page-*.html")])

def list_pdfs():
  d = Path("docs/pdfs")
  if not d.exists():
    return []
  return sorted([p.name for p in d.glob("*.pdf")])

def write_rules():
  ts = now_utc()
  m, merr = read_manifest()

  start_url = scope = None
  icon_srcs = []
  if m:
    start_url = m.get("start_url")
    scope = m.get("scope")
    icons = m.get("icons") or []
    if isinstance(icons, list):
      for it in icons:
        if isinstance(it, dict) and it.get("src"):
          icon_srcs.append(str(it.get("src")))

  must_start = f"/{REPO}/?pwa=1"
  must_scope  = f"/{REPO}/"
  must_icons  = [f"/{REPO}/icons/icon-192.png", f"/{REPO}/icons/icon-512.png"]

  req_ok = [p for p in REQ_FILES if exists(p)]
  req_miss = [p for p in REQ_FILES if not exists(p)]

  pages = list_pages()
  pdfs  = list_pdfs()

  invariants = f"""<!-- AUTO:INVARIANTS:BEGIN -->
## 🔒 עקרונות שאסור לשבור (מקור אמת יחיד)

### 🎯 מטרה
זה פרויקט של **דפי עבודה להדפסה (A4)**. האתר הוא מעטפת לפתיחה/בחירה/הדפסה, לא מערכת “מתוקשבת” עם לוגיקה חינוכית כבדה.

### 📌 האייקון הקבוע בנייד (אסור לשנות)
האייקון מותקן אך ורק מהקישור הזה, והוא חייב להישאר קבוע לתמיד:
- {INSTALL}

### 🧷 אינבריאנטים של PWA (אסור לשנות)
ב־`docs/manifest.webmanifest`:
- `start_url` חייב להיות בדיוק: `{must_start}`
- `scope` חייב להיות בדיוק: `{must_scope}`
- נתיבי אייקון חייבים לכלול:
  - `{must_icons[0]}`
  - `{must_icons[1]}`

קבצי חובה שלא נוגעים בהם בלי Gate:
- `docs/sw.js`
- `docs/print.css`
- `docs/icons/icon-192.png`
- `docs/icons/icon-512.png`

### ✅ Gate חובה
כל שינוי חייב לעבור Workflow אחד בלבד שמייצר ומעדכן אוטומטית:
- `RULES.md`
- `STATUS.md`
בלי סתירות, בלי כמה Workflows שמתנגשים.

<!-- AUTO:INVARIANTS:END -->"""

  body = f"""# RULES — {REPO}

עודכן אוטומטית: **{ts} (UTC)**

{invariants}

## 📚 מה יש כרגע בריפו (אוטומטי)
### קבצי חובה
- ✅ קיימים: {len(req_ok)}
- ❌ חסרים: {len(req_miss)}

{("\\n".join([f"- ✅ `{p}`" for p in req_ok]) or "- (אין)")}

{("\\n".join([f"- ❌ `{p}`" for p in req_miss]) or "")}

### Manifest מצב
- manifest תקין? **{"כן" if (m and not merr) else "לא"}**
- start_url: `{start_url}`
- scope: `{scope}`
- icons: {", ".join([f"`{s}`" for s in icon_srcs]) if icon_srcs else "(אין)"}

### דפי HTML
- pages: {len(pages)}
{("\\n".join([f"- `{p}`" for p in pages]) or "- (אין pages)")}

### PDFs
- pdfs: {len(pdfs)}
{("\\n".join([f"- `{p}`" for p in pdfs]) or "- (אין PDFs עדיין)")}

## 🧠 מה הדבר הבא בפרויקט (בלי לבצע עדיין)
- להפוך כל `page-*.html` ל־**Print-first** אמיתי: כפתור “PDF/הדפסה”, CSS הדפסה נקי, ומבנה אחיד A4.
- כלי כתיב מתמטי: לבחור מסלול רשמי אחד (MathJax בדפדפן *או* XeLaTeX שמייצר PDF) ולהפסיק ערבוב שמייצר שבירות.

"""
  Path("RULES.md").write_text(body, encoding="utf-8")

def write_status():
  ts = now_utc()
  pages = list_pages()
  pdfs  = list_pdfs()
  miss = [p for p in REQ_FILES if not exists(p)]
  ok = (len(miss) == 0)

  status = f"""# STATUS — pdf-system-site

עודכן אוטומטית: **{ts} (UTC)**

## ✅ יציבות האייקון (PWA)
- קישור התקנה קבוע: {INSTALL}
- קבצי חובה קיימים? **{"כן" if ok else "לא"}**
{("\\n".join([f"- ❌ חסר: `{p}`" for p in miss]) if miss else "- ✅ כל הקבצים קיימים")}

## 📄 מצב דפים להדפסה
- pages קיימים: **{len(pages)}**
- pdfs קיימים: **{len(pdfs)}**

## 📌 הערה חשובה
אם האייקון בנייד עושה 404 — זה כמעט תמיד כי הוא הותקן מכתובת אחרת.
מוחקים את האייקון הישן ומתקינים מחדש **רק** מהקישור הקבוע למעלה.
"""
  Path("STATUS.md").write_text(status, encoding="utf-8")

def main():
  write_rules()
  write_status()
  print("OK: RULES.md + STATUS.md rebuilt")

if __name__ == "__main__":
  main()
