# RULES — pdf-system-site

עודכן אוטומטית: **2026-02-20T14:34:56Z (UTC)**

<!-- AUTO:INVARIANTS:BEGIN -->
## 🔒 עקרונות שאסור לשבור (מקור אמת יחיד)

### 🎯 מטרה
זה פרויקט של **דפי עבודה להדפסה (A4)**. האתר הוא מעטפת לפתיחה/בחירה/הדפסה, לא מערכת “מתוקשבת” עם לוגיקה חינוכית כבדה.

### 📌 האייקון הקבוע בנייד (אסור לשנות)
האייקון מותקן אך ורק מהקישור הזה, והוא חייב להישאר קבוע לתמיד:
- https://yanivmizrachiy.github.io/pdf-system-site/?pwa=1#page-1

### 🧷 אינבריאנטים של PWA (אסור לשנות)
ב־`docs/manifest.webmanifest`:
- `start_url` חייב להיות בדיוק: `/pdf-system-site/?pwa=1`
- `scope` חייב להיות בדיוק: `/pdf-system-site/`
- נתיבי אייקון חייבים לכלול:
  - `/pdf-system-site/icons/icon-192.png`
  - `/pdf-system-site/icons/icon-512.png`

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

<!-- AUTO:INVARIANTS:END -->

## 📚 מה יש כרגע בריפו (אוטומטי)
### קבצי חובה
- ✅ קיימים: 6
- ❌ חסרים: 0

- ✅ `docs/index.html`\n- ✅ `docs/manifest.webmanifest`\n- ✅ `docs/sw.js`\n- ✅ `docs/print.css`\n- ✅ `docs/icons/icon-192.png`\n- ✅ `docs/icons/icon-512.png`



### Manifest מצב
- manifest תקין? **כן**
- start_url: `/pdf-system-site/?pwa=1`
- scope: `/pdf-system-site/`
- icons: `/pdf-system-site/icons/icon-192.png`, `/pdf-system-site/icons/icon-512.png`

### דפי HTML
- pages: 3
- `page-1.html`\n- `page-2.html`\n- `page-3.html`

### PDFs
- pdfs: 0
- (אין PDFs עדיין)

## 🧠 מה הדבר הבא בפרויקט (בלי לבצע עדיין)
- להפוך כל `page-*.html` ל־**Print-first** אמיתי: כפתור “PDF/הדפסה”, CSS הדפסה נקי, ומבנה אחיד A4.
- כלי כתיב מתמטי: לבחור מסלול רשמי אחד (MathJax בדפדפן *או* XeLaTeX שמייצר PDF) ולהפסיק ערבוב שמייצר שבירות.

