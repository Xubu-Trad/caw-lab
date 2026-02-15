#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C
git rev-parse --is-inside-work-tree >/dev/null

# Files allowed to contain placeholder examples:
allow_re='^(docs/SAFE_DISCLOSURE\.md|docs/STYLE\.md)$'

mapfile -t files < <(git ls-files)

bad=0
for f in "${files[@]}"; do
  [[ "$f" =~ $allow_re ]] && continue

  # scan only text-ish files (skip obvious non-text via extension)
  case "$f" in
    *.hex|*.b64|*.txt|*.md|*.yml|*.yaml|*.py|*.sh|*.tsv|*.json) ;;
    *) continue ;;
  esac

  # leaked linux home path (allow /home/user or /home/REDACTED)
  if grep -nE '/home/(?!user\b|REDACTED\b)[^/[:space:]]+' "$f" >/dev/null 2>&1; then
    echo "[fail] leaked /home/<user> path in $f (use /home/user or /home/REDACTED)"
    grep -nE '/home/(?!user\b|REDACTED\b)[^/[:space:]]+' "$f" || true
    bad=1
  fi

  # leaked windows user path (allow C:\Users\REDACTED\\Users\\(?!REDACTED\b)[^\\[:space:]]+' "$f" >/dev/null 2>&1; then
    echo "[fail] leaked C:\\Users\\<name> path in $f (use C:\\Users\\REDACTED)"
    grep -nE 'C:\\Users\\(?!REDACTED\b)[^\\[:space:]]+' "$f" || true
    bad=1
  fi

  # leaked hostnames (allow HOST-REDACTED)
  if grep -nE '\bDESKTOP-[A-Z0-9-]+\b' "$f" | grep -v 'HOST-REDACTED' >/dev/null 2>&1; then
    echo "[fail] leaked DESKTOP-* hostname in $f (use HOST-REDACTED)"
    grep -nE '\bDESKTOP-[A-Z0-9-]+\b' "$f" || true
    bad=1
  fi
done

if (( bad )); then exit 1; fi
echo "[ok] forbidden scan passed"
