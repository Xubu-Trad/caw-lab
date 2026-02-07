#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C
git rev-parse --is-inside-work-tree >/dev/null

mapfile -t files < <(git ls-files 'layers/**/EVIDENCE/**' 2>/dev/null || true)

bad=()
for f in "${files[@]}"; do
  case "$f" in
    */.keep|*.keep) continue ;;
  esac
  if [[ ! -s "$f" ]]; then
    bad+=("$f")
  fi
done

if (( ${#bad[@]} )); then
  echo "[fail] empty evidence files found. receipts must be non-empty or replaced with a .keep placeholder."
  printf ' - %s\n' "${bad[@]}"
  exit 1
fi

echo "[ok] no empty evidence files"
