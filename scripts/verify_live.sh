#!/usr/bin/env bash
set -euo pipefail

OWNER="yanivmizrachiy"
REPO="pdf-system-site"
SITE="https://yanivmizrachiy.github.io/pdf-system-site"

echo "=== A) LOCAL HEAD ==="
git log -1 --oneline

echo
echo "=== B) CHECK SITE ROOT ==="
curl -I -s --max-time 20 "$SITE/" | head -n 1 || echo "❌ site root not reachable"

echo
echo "=== C) CHECK BUILD STAMP (cache-bust) ==="
u="$SITE/build_stamp.txt?fresh=$(date +%s)"
code="$(curl -s -o /dev/null -w "%{http_code}" "$u" || true)"
echo "build_stamp.txt => $code  $u"
if [ "$code" = "200" ]; then
  echo "STAMP:"
  curl -s --max-time 20 "$u" | head -n 5 || true
else
  echo "⚠️ stamp not reachable yet (may need next Pages deploy)"
fi

echo
echo "=== D) CHECK HTML PAGES (1..6) ==="
for n in 1 2 3 4 5 6; do
  h="$SITE/pages/page-$n.html?fresh=$(date +%s)"
  c="$(curl -s -o /dev/null -w "%{http_code}" "$h" || true)"
  echo "page-$n.html => $c  $h"
done

echo
echo "=== E) CHECK PDF PAGES (1..6) ==="
ok=1
for n in 1 2 3 4 5 6; do
  p="$SITE/pdfs/page-$n.pdf"
  c="$(curl -s -o /dev/null -w "%{http_code}" "$p" || true)"
  echo "page-$n.pdf  => $c  $p"
  [ "$c" = "200" ] || ok=0
done

echo
if [ "$ok" = "1" ]; then
  echo "✅ ALL PDFs 1..6 ARE PUBLIC (200)"
else
  echo "⚠️ SOME PDFs NOT 200 YET (Pages cache/deploy may lag)"
fi

echo
echo "=== F) OPEN SITE (cache-bust) ==="
termux-open-url "$SITE/?fresh=$(date +%s)" >/dev/null 2>&1 || true
echo "DONE"
