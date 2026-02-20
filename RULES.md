# RULES — pdf-system-site

עודכן אוטומטית: **2026-02-20T14:35:35Z (UTC)**

<!-- AUTO:INVARIANTS:BEGIN -->
## עקרונות שאסור לשבור (חובה)

### 🎯 מטרה
- הפרויקט הזה הוא **דפי עבודה להדפסה (A4)**. האתר הוא מעטפת פתיחה/בחירה/הדפסה בלבד.

### 📌 אייקון קבוע בנייד (אסור שיתקלקל)
- מתקינים אייקון **רק** מהקישור הקבוע (לא משתנה לעולם):
  - https://yanivmizrachiy.github.io/pdf-system-site/?pwa=1#page-1

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


## היסטוריית שינויים
- (האוטומציה תוסיף כאן כשנרצה)
