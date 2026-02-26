#!/usr/bin/env bash
set -euo pipefail

echo "=== QA PRE: BUILD GENERATED PAGES ==="
if [ -f compiler/build.mjs ]; then node compiler/build.mjs; fi


echo "=== QA PRE: AUTOFIX (after build) ==="
python scripts/qa_autofix_pages.py

if [ -f compiler/build.js ]; then node compiler/build.js; fi

set -euo pipefail
cd "$(dirname "$0")/.." || exit 1
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
THRESHOLD="85.0"
tmp="$(mktemp)"
ok=0; total=0

# helpers (internal)
has(){ grep -Eq "$1" "$2" 2>/dev/null; }
has_i(){ grep -Eiq "$1" "$2" 2>/dev/null; }

printf "%s\n" "<!doctype html><html lang=\"en\" dir=\"rtl\"><head><meta charset=\"utf-8\"/><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"/><title>QA PRO v2 - pdf-system-site</title><style>body{font-family:Arial,Heebo,Assistant,sans-serif;padding:28px;direction:rtl;color:#111}table{border-collapse:collapse;width:100%;margin-top:14px}th,td{border:1px solid #e5e7eb;padding:8px;text-align:center}th{background:#f3f4f6}.card{border:1px solid #e5e7eb;border-radius:12px;padding:14px}</style></head><body><div class=\"card\"><h1 style=\"margin:0 0 6px 0\">QA PRO v2</h1><div><b>UTC:</b> $TS</div><div><b>Threshold:</b> $THRESHOLD%</div></div><table><thead><tr><th>Page</th><th>Score</th><th>Missing</th></tr></thead><tbody>" > "$tmp"

found_any=0
for f in pages/page-*.html; do
  [ -f "$f" ] || continue
  found_any=1
  score=0; checks=9; miss=""

  # A4 + print rules
  has "@page" "$f" && score=$((score+1)) || miss="${miss}no@page;"
  has "size:[[:space:]]*A4" "$f" && score=$((score+1)) || miss="${miss}noA4;"
  has "margin" "$f" && score=$((score+1)) || miss="${miss}noMargin;"
  has "@media[[:space:]]+print" "$f" && score=$((score+1)) || miss="${miss}noPrintMedia;"

  # RTL
  (has "dir=\\\"rtl\\\"" "$f" || has "direction:[[:space:]]*rtl" "$f") && score=$((score+1)) || miss="${miss}noRTL;"

  # meta
  has_i "<meta[[:space:]]+charset" "$f" && score=$((score+1)) || miss="${miss}noCharset;"
  has_i "<meta[[:space:]]+name=\\\"viewport\\\"" "$f" && score=$((score+1)) || miss="${miss}noViewport;"
  has_i "<title" "$f" && score=$((score+1)) || miss="${miss}noTitle;"

  # math
  has "MathJax" "$f" && score=$((score+1)) || miss="${miss}noMathJax;"

  ok=$((ok+score)); total=$((total+checks))
  [ -n "$miss" ] || miss="OK"
  printf "%s\n" "<tr><td>$(basename "$f")</td><td>${score}/${checks}</td><td>${miss}</td></tr>" >> "$tmp"
done

if [ "$found_any" -eq 0 ]; then
  printf "%s\n" "<tr><td colspan=\"3\">No pages/page-*.html found</td></tr>" >> "$tmp"
fi

percent="0.0"
if [ "$total" -gt 0 ]; then
  percent="$(python -c "print(round(($ok/$total)*100,1))")"
fi

status="PASS"
python - <<PY >/dev/null 2>&1 || status="FAIL"
p=float("$percent"); t=float("$THRESHOLD")
raise SystemExit(0 if p>=t else 1)
PY

printf "%s\n" "</tbody></table><div class=\"card\" style=\"margin-top:14px\"><div><b>Total:</b> ${percent}%</div><div><b>Status:</b> ${status}</div><div><b>Checks:</b> ${ok}/${total}</div></div></body></html>" >> "$tmp"
cp -f "$tmp" pages/qa.html
rm -f "$tmp" >/dev/null 2>&1 || true
echo "QA PRO v2 SCORE: ${percent}% (${status})"
[ "$status" = "PASS" ]
