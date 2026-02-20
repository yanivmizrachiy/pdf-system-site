from pathlib import Path
from datetime import datetime, timezone
import json, re, sys

BASE = "https://yanivmizrachiy.github.io/pdf-system-site"
INSTALL = BASE + "/?pwa=1#page-1"

def exists(p): return Path(p).exists()

# quick health
core = {
  "index": exists("docs/index.html"),
  "print_css": exists("docs/print.css"),
  "manifest": exists("docs/manifest.webmanifest"),
  "sw": exists("docs/sw.js"),
  "icon192": exists("docs/icons/icon-192.png"),
  "icon512": exists("docs/icons/icon-512.png"),
}

pages = sorted(Path("docs/pages").glob("page-*.html"))
pages_n = len(pages)

pwa_ok = core["manifest"] and core["sw"] and core["icon192"] and core["icon512"]
a4_ok = core["print_css"] and pages_n > 0

# progress: תשתית (לא תוכן פדגוגי)
progress = 0
if core["index"]: progress += 10
if a4_ok: progress += 45
if pwa_ok: progress += 35
if core["print_css"]: progress += 10
progress = min(progress, 100)

now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

# STATUS.md
status_md = []
status_md.append("# STATUS — pdf-system-site")
status_md.append("")
status_md.append(f"- עודכן: **{now}**")
status_md.append(f"- התקדמות תשתית (A4+PWA): **{progress}%**")
status_md.append("")
status_md.append("## קישורים קבועים")
status_md.append(f"- אתר (Viewer): {BASE}/")
status_md.append(f"- התקנת אייקון קבוע (זה בלבד): {INSTALL}")
status_md.append("")
status_md.append("## מצב רכיבים")
for k,v in core.items():
  status_md.append(f"- {k}: {✅ if v else ❌}")
status_md.append(f"- pages count: **{pages_n}**")
if pages_n:
  status_md.append("  - דפים: " + ", ".join([p.name for p in pages[:20]]))
status_md.append("")
Path("STATUS.md").write_text("\n".join(status_md).strip() + "\n", encoding="utf-8")

# RULES.md: insert/replace AUTO block
rules_path = Path("RULES.md")
if not rules_path.exists():
  rules_path.write_text("# RULES\n\n", encoding="utf-8")

rules = rules_path.read_text(encoding="utf-8", errors="ignore")

begin = "<!-- AUTO:STATUS:BEGIN -->"
end   = "<!-- AUTO:STATUS:END -->"
block = "\n".join([
  begin,
  "## 📌 מצב והתקדמות (אוטומטי)",
  f"- עודכן: **{now}**",
  f"- התקדמות תשתית (A4+PWA): **{progress}%**",
  f"- Viewer: {BASE}/",
  f"- התקנת אייקון קבוע: {INSTALL}",
  f"- מספר דפים: **{pages_n}**",
  end,
]) + "\n"

if begin in rules and end in rules:
  rules = re.sub(re.escape(begin) + r".*?" + re.escape(end) + r"\n?", block, rules, flags=re.S)
else:
  # add near top
  if rules.startswith("#"):
    parts = rules.split("\n", 2)
    if len(parts) >= 2:
      rules = parts[0] + "\n\n" + block + (parts[2] if len(parts) == 3 else "")
    else:
      rules = rules + "\n" + block
  else:
    rules = block + "\n" + rules

rules_path.write_text(rules, encoding="utf-8")
print("OK update_status (progress=%d%%, pages=%d)" % (progress, pages_n))
