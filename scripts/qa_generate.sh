#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
tmp="$(mktemp)"
ok=0; total=0
yn(){ [ "$1" = 1 ] && echo YES || echo NO; }

printf "%s\n" "<!doctype html><html lang=\"en\" dir=\"rtl\"><head><meta charset=\"utf-8\"/><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"/><title>QA - pdf-system-site</title><style>body{font-family:Arial,Heebo,Assistant,sans-serif;padding:28px;direction:rtl;color:#111}table{border-collapse:collapse;width:100%;margin-top:14px}th,td{border:1px solid #e5e7eb;padding:10px;text-align:center}th{background:#f9fafb}.card{border:1px solid #e5e7eb;border-radius:14px;padding:14px}</style></head><body><div class=\"card\"><h1 style=\"margin:0 0 6px 0\">QA Report - pdf-system-site</h1><div><b>UTC:</b> $TS</div></div><table><thead><tr><th>Page</th><th>MathJax</th><th>RTL</th><th>A4</th><th>Meta</th><th>Title</th><th>Score</th></tr></thead><tbody>" > "$tmp"

for f in pages/page-*.html; do
  [ -f "$f" ] || continue
  math=0; rtl=0; a4=0; meta=0; title=0
  grep -q "MathJax" "$f" && math=1 || true
  grep -q "dir=\"rtl\"" "$f" && rtl=1 || true
  grep -Eq "direction:[[:space:]]*rtl" "$f" && rtl=1 || true
  grep -q "@page" "$f" && a4=1 || true
  grep -Eq "size:[[:space:]]*A4" "$f" && a4=1 || true
  grep -qi "<meta charset" "$f" && meta=1 || true
  grep -qi "<title" "$f" && title=1 || true
  score=$((math+rtl+a4+meta+title))
  ok=$((ok+score))
  total=$((total+5))
  printf "%s\n" "<tr><td>$(basename "$f")</td><td>$(yn $math)</td><td>$(yn $rtl)</td><td>$(yn $a4)</td><td>$(yn $meta)</td><td>$(yn $title)</td><td>${score}/5</td></tr>" >> "$tmp"
done

percent="0.0"
if [ "$total" -gt 0 ]; then
  percent="$(python -c "print(round(($ok/$total)*100,1))")"
fi

printf "%s\n" "</tbody></table><div class=\"card\" style=\"margin-top:14px\"><div><b>Total:</b> ${percent}%</div><div><b>Checks:</b> ${ok}/${total}</div></div></body></html>" >> "$tmp"
mkdir -p pages docs/pages
cp -f "$tmp" pages/qa.html
cp -f "$tmp" docs/pages/qa.html
rm -f "$tmp" >/dev/null 2>&1 || true
echo "QA SCORE: ${percent}% (${ok}/${total})"
