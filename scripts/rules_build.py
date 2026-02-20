from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import json

OWNER="yanivmizrachiy"
REPO="pdf-system-site"
BASE=f"https://{OWNER}.github.io/{REPO}"
INSTALL=f"{BASE}/?pwa=1#page-1"

def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""

def write(p: Path, s: str):
    p.write_text(s, encoding="utf-8")

def upsert_block(text: str, begin: str, end: str, block: str) -> str:
    if begin in text and end in text:
        pre = text.split(begin)[0].rstrip()
        post = text.split(end, 1)[1].lstrip()
        return pre + "\n\n" + block.strip() + "\n\n" + post
    return (text.rstrip() + "\n\n" + block.strip() + "\n")

def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # --- RULES.md ---
    rules_p = Path("RULES.md")
    rules = read(rules_p) or "# RULES — pdf-system-site\n\n"

    begin="<!-- AUTO:INVARIANTS:BEGIN -->"
    end="<!-- AUTO:INVARIANTS:END -->"

    block = f"""{begin}
## עקרונות שאסור לשבור (חובה)

### 🎯 מטרה
- הפרויקט הזה הוא **דפי עבודה להדפסה (A4)**. האתר הוא מעטפת פתיחה/בחירה/הדפסה בלבד.

### 📌 אייקון קבוע בנייד (אסור שיתקלקל)
- מתקינים אייקון **רק** מהקישור הקבוע (לא משתנה לעולם):
  - {INSTALL}

### 🔒 קבועים טכניים שאסור לשנות
- :
  -  חייב להיות: 
  -  חייב להיות: 
  -  חייב לכלול בדיוק את:
    - 
    - 
- קבצי חובה שקיימים תמיד:
  - 
  - 
  - 
  - 
  - 

### 🖨️ הדפסה (Print-First)
- כל דף עבודה אמיתי יהיה **PDF** (או דף HTML שמודפס A4 בצורה נקייה) עם כפתור **PDF / הדפסה** ברור.
- לא בונים “מערכת מתוקשבת”. כל מה שלא קשור להדפסה — לא נכנס.

### ✅ ניהול פרויקט בלי סתירות
- מקור אמת יחיד:  + 
- כל שינוי שמבוצע חייב להשתקף כאן (אוטומטית דרך workflow).
{end}
"""

    rules = upsert_block(rules, begin, end, block)
    if "## היסטוריית שינויים" not in rules:
        rules += "\n## היסטוריית שינויים\n- (האוטומציה תוסיף כאן כשנרצה)\n"

    write(rules_p, rules)

    # --- STATUS.md ---
    status_p = Path("STATUS.md")
    status = f"""# STATUS — pdf-system-site

עודכן אוטומטית: **{now}**

## קישורים חשובים
- אתר: {BASE}/
- התקנת אייקון (קבוע): {INSTALL}
- RULES: https://github.com/{OWNER}/{REPO}/blob/main/RULES.md
- STATUS: https://github.com/{OWNER}/{REPO}/blob/main/STATUS.md

## מצב קריטי (חייב תמיד להיות תקין)
- PWA/אייקון: start_url/scope/icons **לא משתנים**
- המרה/הדפסה: הפרויקט = דפי עבודה להדפסה (A4)

## מה יש כרגע
- דפי HTML קיימים: docs/pages/page-*.html
- נכסי PWA: manifest + sw + icons + print.css
"""
    write(status_p, status)

if __name__ == "__main__":
    main()
