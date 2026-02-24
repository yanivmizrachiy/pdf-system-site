#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
tmp="$(mktemp)"
ok=0; total=0

yn(){ [ "$1" = 1 ] && echo YES || echo NO; }

printf "%s\n" "<!doctype html><html lang=\"en\" dir=\"rtl\"><head><meta charset=\"utf-8\"/><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"/><title>QA PRO - pdf-system-site</title><style>body{font-family:Arial,Heebo,Assistant,sans-serif;padding:28px;direction:rtl;color:#111}table{border-collapse:collapse;width:100%;margin-top:14px}th,td{border:1px solid #e5e7eb;padding:8px;text-align:center}th{background:#f3f4f6}.card{border:1px solid #e5e7eb;border-radius:12px;padding:14px}</style></head><body><div class=\"card\"><h1>QA PRO REPORT</h1><div><b>UTC:</b> $TS</div></div><table><thead><tr><th>Page</th><th>Score</th></tr></thead><tbody>" > "$tmp"

for f in pages/page-*.html; do
  [ -f "$f" ] || continue
  score=0; checks=12

  grep -q "@page" "$f" && score=$((score+1))
  grep -Eq "size:[[:space:]]*A4" "$f" && score=$((score+1))
  grep -Eq "margin" "$f" && score=$((score+1))
  grep -q "dir=\"rtl\"" "$f" && score=$((score+1))
  grep -Eq "direction:[[:space:]]*rtl" "$f" && score=$((score+1))
  grep -q "MathJax" "$f" && score=$((score+1))
  grep -q "tex:" "$f" && score=$((score+1))
  grep -qi "<meta charset" "$f" && score=$((score+1))
  grep -qi "<title" "$f" && score=$((score+1))
  ! grep -Eq "width:[[:space:]]*[0-9]+px" "$f" && score=$((score+1))
  ! grep -Eq "overflow-x" "$f" && score=$((score+1))
  ! grep -Eq "font-size:[[:space:]]*[0-9]+px" "$f" && score=$((score+1))

  ok=$((ok+score))
  total=$((total+checks))

  printf "%s\n" "<tr><td>$(basename "$f")</td><td>${score}/${checks}</td></tr>" >> "$tmp"
done

percent="0"
if [ "$total" -gt 0 ]; then
  percent="$(python -c "print(round(($ok/$total)*100,1))")"
fi

status="PASS"
[ "$(printf "%.0f" "$percent")" -lt 85 ] && status="FAIL"

printf "%s\n" "</tbody></table><div class=\"card\" style=\"margin-top:14px\"><div><b>Total:</b> ${percent}%</div><div><b>Status:</b> ${status}</div></div></body></html>" >> "$tmp"

cp -f "$tmp" pages/qa.html
rm -f "$tmp"
echo "QA PRO SCORE: ${percent}% (${status})"
