#!/usr/bin/env bash
set -euo pipefail
BASE="${1:-}"; HEAD="${2:-}"
if [ -z "$BASE" ] || [ -z "$HEAD" ]; then
  echo "INFO: guard needs BASE and HEAD sha. Skipping."
  exit 0
fi
changed="$(git diff --name-only "$BASE" "$HEAD" || true)"
touchChanged="0"; srcChanged="0"
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if [[ "$f" =~ ^pages/page-.*\.html$ ]]; then touchChanged="1"; fi
  if [[ "$f" =~ ^content/ ]] || [[ "$f" =~ ^compiler/ ]] || [[ "$f" =~ ^layout/ ]]; then srcChanged="1"; fi
done <<< "$changed"
if [ "$touchChanged" = "1" ] && [ "$srcChanged" = "0" ]; then
  echo "❌ Policy violation: pages/page-*.html changed without content/compiler/layout changes."
  echo "$changed"
  exit 2
fi
echo "OK: generated pages guard passed."
