# RULES — pdf-system-site

<!-- AUTO:GOVERNANCE:BEGIN -->
## 🔒 Governance Iron Mode (חוק ברזל)
- RULES.md הוא מקור אמת יחיד.
- אין קומיט בלי עדכון RULES.md (נאכף מקומית ע״י pre-commit + נאכף ב-CI).
- Gate מקומי: `.githooks/pre-commit` (core.hooksPath מוגדר לריפו).
- Gate ב-CI: `.github/workflows/governance_gate.yml`
Last enforcement update (UTC): 2026-02-24T06:08:02Z
<!-- AUTO:GOVERNANCE:END -->


\1 2026-02-24 05:43:05 UTC

## מצב מערכת
PWA תקין: True
קבצי TEX: 1
קבצי PDF: 0
התקדמות כללית: 70%

## אייקון קבוע (לא לשנות)
https://yanivmizrachiy.github.io/pdf-system-site/?pwa=1#page-1

## רצות תרגול
- רצה 2: משוואות ריבועיות (בסיסי/בינוני) — עמודים page-4..page-6 (HTML נפרד לכל עמוד). CSS נפרד (docs/print.css). בכל עמוד נטען a4_paginate.js.
- מנגנון יצירת PDF (Playwright) הוקשח: לא נופל אם .item לא מופיע בזמן, וממתין לטעינת דף/MathJax.

## יצירת PDF (Build PDFs)
- מנגנון יצירת PDF לא מסתמך יותר על `.item` (כי לא כל העמודים מכילים אותו). במקום זה יש המתנה חכמה: DOM+networkidle+פונטים+MathJax ואז `.page`/`body`/`mjx-container`.
- אם עמוד אחד נכשל, הריצה ממשיכה ולא מפילה את הכל (כדי ש-page-4 ומעלה עדיין יווצרו).

## GitHub Pages + PDFs
- Pages מוגדר לשרת מהשורש (path=/). לכן ה-PDFים חייבים להיות בתיקייה /pdfs בשורש הריפו (ולא docs/pdfs).
- Build PDFs (Playwright) מייצר כעת קבצים ל-pdfs/page-N.pdf ומבצע commit+push אוטומטית.

## PDF Build Mode
- בניית PDF כעת נעשית מקומית (file://) מתוך הריפו עצמו.
- אין תלות ב-GitHub Pages בזמן build.
- קבצי PDF נוצרים ב-/pdfs בשורש הריפו.

## רצות תרגול
- רצה 2: משוואות ריבועיות (בסיסי/בינוני) — נוספו עמודים page-5..page-6 (HTML נפרד לכל עמוד), CSS נפרד (docs/print.css), ובכל עמוד נטען a4_paginate.js.

<!-- AUTO:MASTERPLAN:BEGIN -->
# 🧠 MASTERPLAN — pdf-system-site (קבוע ומחייב)

## עקרונות־על (לא נשברים)
- הקישור הקבוע לאתר: https://yanivmizrachiy.github.io/pdf-system-site/  (לא משתנה לעולם)
- איכות גרפיקה/טיפוגרפיה: A4 פרימיום, RTL, MathJax תקין, ריווח ויישור יציבים
- `RULES.md` הוא מקור אמת יחיד: כל שינוי/ריצה -> מתועד כאן
- כל build שמייצר PDFs חייב להעלות אותם ל־Pages ולהיות נגישים ב־200

## מה כבר קיים (נכון להיום)
- Pages פעיל, תיקיית /pages עם page-1..page-6
- PDFs ב־/pdfs ומסונכרנים גם ל־/docs/pdfs
- Workflow build_pdfs.yml שמייצר PDFs אוטומטית

## מה מבצעים עכשיו (אימות + הוכחה שזה מתעדכן באמת)
- הוספת build_stamp.txt כדי להוכיח איזו גרסה חיה כרגע ב־Pages
- הוספת scripts/verify_live.sh לבדיקת אתר+HTML+PDFים (200) עם cache-bust
- כל ריצה/תקלה/תיקון: מתווסף ליומן בתוך RULES.md

## מה אחר כך (שדרוגים קיצוניים בלי לשבור)
- שדרוג עיצוב הדפים (כותרת פרימיום, גריד יציב, ריווח אחיד) תוך שמירה על RTL
- הוספת “עמוד בית” עם כפתורי ניווט לדפים + הורדות PDF
- הוספת בדיקות איכות (lint לתבניות, בדיקת MathJax טעינה, בדיקת A4 overflow)
<!-- AUTO:MASTERPLAN:END -->


## יומן שינוי (אוטומטי)
-  — bump VERSION= + build_stamp + Live Badge בדף הבית (גרסה+חותמת).

<!-- AUTO:STRATEGY:BEGIN -->
# 📌 pdf-system-site — דף כללים מרכזי (מקור אמת)

## ✅ קישור קבוע (לא משתנה לעולם)
- אתר: https://yanivmizrachiy.github.io/pdf-system-site/

## 🧱 מה כבר קיים (נבנה ועובד בפועל)
- GitHub Pages פעיל על `main` (source: `main /`)
- דפי HTML להדפסה:
  - `/pages/page-1.html` … `/pages/page-6.html`
- קבצי PDF ציבוריים:
  - `/pdfs/page-1.pdf` … `/pdfs/page-6.pdf`
- הוכחת עדכון (Live Proof):
  - `/build_stamp.txt` (חותמת build ציבורית)
  - `/VERSION.txt` (מספר גרסה ציבורי)
- בדיקת תקינות (HTTP 200):
  - בדיקות שורש האתר + stamp + version + כל דפי HTML + כל קבצי PDF
- דף בית כולל “Live Badge” שמציג גרסה וחותמת build מתוך הקבצים הציבוריים (cache-bust)

## 🧠 עקרונות־על (חוקים שלא נשברים)
- הקישור נשאר קבוע תמיד (לא יוצרים “קישור חדש”)
- איכות הדפסה: A4 פרימיום, RTL אמיתי, טיפוגרפיה עקבית, MathJax יציב
- כל שינוי חייב להיות מתועד ב־`RULES.md` (זה מקור האמת)
- אין “דמו”. רק משהו שעובד בפועל: 200 לכל מה שחייב להיות ציבורי
- לא שוברים קיימים: שדרוגים רק בצורה תואמת אחורה

## 🎯 היעד הגדול (מה אנחנו בונים)
להפוך את האתר ממקום שמציג דפים — ל״מנוע ייצור דפי עבודה״ ברמה הגבוהה ביותר:
- יצירה חכמה של תרגילים (לפי רמות/תבניות)
- בדיקת נכונות מתמטית אוטומטית
- איכות הדפסה ברמה מקצועית (אפס גלישות, מרווחים מדויקים)
- QA אוטומטי לכל build
- תיעוד גרסאות תוכן/מנוע

## 🚀 תוכנית עבודה שאפתנית (מסודר, בלי קשקושים)

### A) מנוע יצירה (Quadratic Engine)
- יצירת שאלות לפי רמות קושי (פירוק/טרינום/נוסחה/פרמטר/מילוליות)
- מניעת כפילויות (Hash מתמטי)
- תוצר: JSON של תרגילים + דפי HTML/PDF שנבנים מזה

### B) בדיקת נכונות מתמטית (Math Validation)
- פתרון סימבולי/בדיקות שורשים/דיסקרימיננטה
- אם תרגיל נכשל — הוא לא נכנס לדף (build נכשל או מסמן אדום בדוח)

### C) איכות הדפסה A4 (Print Quality)
- בדיקות overflow אוטומטיות
- סטנדרט מרווחים/כותרות/גודל נוסחאות
- הגדרה קשיחה של margins + safe print zone

### D) QA אוטומטי (CI Quality Gate)
- בדיקת טעינת MathJax
- בדיקת RTL
- בדיקת 200 לכל המשאבים הציבוריים
- דוח איכות אוטומטי שמצורף לכל build

### E) ניהול גרסאות ותיעוד
- הפרדה בין:
  - גרסת תוכן (CONTENT)
  - גרסת מנוע (ENGINE)
- CHANGELOG מסודר
- “Proof” בדף הבית נשאר תמיד גלוי וברור

## ✅ מה עושים עכשיו (המשך מיידי)
- להבטיח ש־VERSION/STAMP תמיד נוצרים גם ב־root וגם ב־docs (כדי למנוע 404 עתידי)
- ✅ נוצר דוח איכות ציבורי: `/pages/health.html` + קיים כפתור בדף הבית (HEALTH).
- לחבר pipeline שמייצר תרגילים מ־JSON ולא ידנית

<!-- AUTO:STRATEGY:END -->


## 🧾 יומן שינוי (אוטומטי)
- 2026-02-23T11:52:44Z — עדכון אסטרטגי מלא ל־RULES (מצב קיים + תוכנית עבודה + חוקים מחייבים).
- 2026-02-24T05:43:05Z — HEALTH פורסם בפועל (pages+docs) + RULES עודכן באותו קומיט לפי חוק ברזל.\n- 2026-02-24T06:08:02Z — הופעל Governance Iron Mode (pre-commit + CI gate) ונרשם ב-RULES.md לפי חוק ברזל.
- 2026-02-24T06:09:16Z — sync+verify run: pull/rebase + LIVE check initiated.

- 2026-02-24T12:47:58Z - QA report published: /pages/qa.html ; generator: scripts/qa_generate.sh ; RULES required for any change.

- 2026-02-24T16:13:34Z - QA report published: /pages/qa.html ; mirrored: /docs/pages/qa.html ; generator: scripts/qa_generate.sh ; RULES required for any change.

- 2026-02-24T16:17:23Z - QA report published: /pages/qa.html ; generator: scripts/qa_generate.sh ; publish_root=/ ; RULES required for any change.

- 2026-02-24T16:19:03Z - Governance: QA is mandatory. Run scripts/qa_generate.sh after any change and verify /pages/qa.html returns 200.

- 2026-02-24T16:31:57Z - QA PRO active. Threshold 85% required.

- 2026-02-24T16:55:03Z - Auto-fix applied to pages/page-*.html to satisfy QA PRO v2 (A4/RTL/Print/Meta/MathJax).

- 2026-02-24T19:11:31Z - QA PRO v2 PASS=100%. Auto-fix injected into all pages/page-*.html via scripts/qa_autofix_pages.py. QA: bash scripts/qa_generate.sh.

- 2026-02-24T19:12:37Z - QA Gate enabled: GitHub Actions runs scripts/qa_generate.sh (must PASS). QA report: /pages/qa.html. Auto-fix: python scripts/qa_autofix_pages.py.

- 2026-02-24T21:29:38Z - PDF Production Engine enabled (CI builds real A4 PDFs via Chromium + QA gate).

- 2026-02-24T21:30:48Z - PDF Production Engine enabled (CI renders real A4 PDFs via Chromium + QA gate).

- 2026-02-24T21:33:44Z - PDF Production Engine enabled (CI renders real A4 PDFs via Chromium + QA gate).

- 2026-02-24T21:35:15Z - Normalized pages to page-000 numbering (page-001.html...). QA PASS required.

- 2026-02-24T22:24:05Z - Fixed compiler/build.mjs (clean ESM generator). Rebuild -> autofix -> QA PASS required. Pages output: page-###.html.

- 2026-02-24T22:24:29Z - Fixed compiler/build.mjs (clean ESM generator). Rebuild -> autofix -> QA PASS required. Pages output: page-###.html.
