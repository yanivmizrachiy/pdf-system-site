#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1

THRESHOLD="85.0"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
tmp="$(mktemp)"
ok=0
total=0
checks=10

yn(){ [ "$1" = "1" ] && echo YES || echo NO; }

printf "%s\n" "<!doctype html><html lang=\"en\" dir=\"rtl\"><head><meta charset=\"utf-8\"/><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"/><title>QA PRO v2 - pdf-system-site</title><style>body{font-family:Arial,Heebo,Assistant,sans-serif;padding:28px;direction:rtl;color:#111}table{border-collapse:collapse;width:100%;margin-top:14px}th,td{border:1px solid #e5e7eb;padding:8px;text-align:center}th{background:#f3f4f6}.card{border:1px solid #e5e7eb;border-radius:12px;padding:14px}</style></head><body><div class=\"card\"><h1>QA PRO v2</h1><div><b>UTC:</b> ${TS}</div><div><b>Threshold:</b> ${THRESHOLD}%</div></div><table><thead><tr><th>Page</th><th>Score</th><th>Notes</th></tr></thead><tbody>" > "$tmp"

for f in pages/page-*.html; do
  [ -f "$f" ] || continue
  s=0
  notes=""

  # 1) @page exists
  grep -q "@page" "$f" && s=$((s+1)) || notes="${notes} no@page;"

  # 2) A4 size
  grep -Eq "size:[[:space:]]*A4" "$f" && s=$((s+1)) || notes="${notes} noA4;"

  # 3) print margin declared (either @page margin or @media print with margin)
  ( grep -Eq "@page[^}]*margin" "$f" || grep -Eq "@media[[:space:]]+print[^}]*margin" "$f" ) && s=$((s+1)) || notes="${notes} noPrintMargin;"

  # 4) RTL
  ( grep -q "dir=\"rtl\"" "$f" || grep -Eq "direction:[[:space:]]*rtl" "$f" ) && s=$((s+1)) || notes="${notes} noRTL;"

  # 5) meta charset
  grep -Eiq "<meta[[:space:]]+charset" "$f" && s=$((s+1)) || notes="${notes} noCharset;"

  # 6) title
  grep -Eiq "<title" "$f" && s=$((s+1)) || notes="${notes} noTitle;"

  # 7) viewport
  grep -Eiq "<meta[[:space:]]+name=\"viewport\"" "$f" && s=$((s+1)) || notes="${notes} noViewport;"

  # 8) font-family declared
  grep -Eq "font-family" "$f" && s=$((s+1)) || notes="${notes} noFontFamily;"

  # 9) MathJax present
  grep -q "MathJax" "$f" && s=$((s+1)) || notes="${notes} noMathJax;"

  # 10) print media exists
  grep -Eq "@media[[:space:]]+print" "$f" && s=$((s+1)) || notes="${notes} noPrintMedia;"

  ok=$((ok+s))
  total=$((total+checks))
  [ -z "$notes" ] && notes="OK"
  printf "%s\n" "<tr><td>$(basename "$f")</td><td>${s}/${checks}</td><td>${notes}</td></tr>" >> "$tmp"
done

percent="0.0"
if [ "$total" -gt 0 ]; then
  percent="$(python -c "print(round(($ok/$total)*100,1))")"
fi

status="PASS"
python - <<PY >/dev/null 2>&1 || status="FAIL"
p=float("$percent"); t=float("$THRESHOLD")
raise SystemExit(0 if p>=t else 1)
PY

printf "%s\n" "</tbody></table><div class=\"card\" style=\"margin-top:14px\"><div><b>Total:</b> ${percent}%</div><div><b>Status:</b> ${status}</div></div></body></html>" >> "$tmp"
cp -f "$tmp" pages/qa.html
rm -f "$tmp"

echo "QA PRO v2 SCORE: ${percent}% (${status})"
[ "$status" = "PASS" ]
