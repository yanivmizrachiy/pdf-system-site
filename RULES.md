# RULES — pdf-system-site

עודכן: 2026-02-21 22:46 UTC

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
