from pathlib import Path
from datetime import datetime

BASE="https://yanivmizrachiy.github.io/pdf-system-site"
INSTALL=f"{BASE}/?pwa=1#page-1"

now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

rules = f"""# RULES — pdf-system-site

עודכן אוטומטית: {now}

## עקרונות שאסור לשבור

- הפרויקט הוא דפי עבודה להדפסה (A4)
- האייקון הקבוע:
  {INSTALL}

## קבועים טכניים
- start_url = /pdf-system-site/?pwa=1
- scope = /pdf-system-site/
- icons:
  - /pdf-system-site/icons/icon-192.png
  - /pdf-system-site/icons/icon-512.png

## ניהול
- מקור אמת יחיד: RULES.md + STATUS.md
"""

Path("RULES.md").write_text(rules, encoding="utf-8")

status = f"""# STATUS — pdf-system-site

עודכן: {now}

אייקון קבוע:
{INSTALL}
"""

Path("STATUS.md").write_text(status, encoding="utf-8")

print("OK rebuilt")
