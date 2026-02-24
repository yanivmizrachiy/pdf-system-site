#!/usr/bin/env bash
set -euo pipefail

mode="${1:-local}"

if [ "$mode" = "ci" ]; then
  base="origin/main"
  git rev-parse --verify origin/main >/dev/null 2>&1 || base="HEAD~1"

  changed="$(git diff --name-only "$base"...HEAD || true)"
  if [ -z "${changed// /}" ]; then
    echo "OK: no changes detected (ci)"
    exit 0
  fi

  # if anything besides RULES.md changed, RULES.md must also be in changed set
  if echo "$changed" | grep -vqE "^(RULES\.md)$"; then
    if echo "$changed" | grep -qE "^(RULES\.md)$"; then
      echo "OK: RULES.md updated (ci gate pass)"
      exit 0
    else
      echo "❌ GOVERNANCE FAIL: changes detected but RULES.md not updated."
      echo "Changed files:"
      echo "$changed"
      exit 2
    fi
  fi

  echo "OK: only RULES.md changed (ci)"
  exit 0
fi

staged="$(git diff --cached --name-only || true)"
if [ -z "${staged// /}" ]; then
  echo "OK: nothing staged"
  exit 0
fi

if echo "$staged" | grep -vqE "^(RULES\.md)$"; then
  if echo "$staged" | grep -qE "^(RULES\.md)$"; then
    echo "OK: RULES.md staged"
    exit 0
  else
    echo "❌ BLOCKED: You are committing changes but RULES.md is not staged."
    echo "Staged files:"
    echo "$staged"
    echo
    echo "Fix: update RULES.md + git add RULES.md"
    exit 3
  fi
fi

echo "OK: only RULES.md staged"
