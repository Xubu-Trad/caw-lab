#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

fail=0

echo "[audit] layer structure checks"
for d in layers/R1-*; do
  [[ -d "$d" ]] || continue
  for f in SUMMARY.md REPRODUCE.md; do
    if [[ ! -f "$d/$f" ]]; then
      echo "[fail] missing $d/$f"
      fail=1
    fi
  done
  if [[ ! -d "$d/EVIDENCE" ]]; then
    echo "[fail] missing $d/EVIDENCE/"
    fail=1
  fi
done

echo
echo "[audit] empty evidence files (should be none)"
if find layers -type f -path '*/EVIDENCE/*' -size 0 -print | grep -q .; then
  find layers -type f -path '*/EVIDENCE/*' -size 0 -print
  fail=1
else
  echo "[ok] none"
fi

echo
echo "[audit] untracked files under layers/docs/scripts (should be none)"
if git ls-files --others --exclude-standard layers docs scripts | grep -q .; then
  git ls-files --others --exclude-standard layers docs scripts
  fail=1
else
  echo "[ok] none"
fi

echo
if [[ "$fail" -ne 0 ]]; then
  echo "[fail] audit_completeness failed"
  exit 1
fi
echo "[ok] audit_completeness passed"
