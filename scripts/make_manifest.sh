#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C

git rev-parse --show-toplevel >/dev/null 2>&1 || { echo "not in git repo" >&2; exit 2; }

OUT="${1:-MANIFEST.repo.sha256}"

mapfile -t FILES < <(git ls-files \
  README.md LAYER_INDEX.md SECURITY.md LICENSE .gitignore \
  docs scripts layers .github \
  ':!lab_notes' ':!experiments' ':!private_evidence' \
  | LC_ALL=C sort)

[[ "${#FILES[@]}" -gt 0 ]] || { echo "no tracked files found (did you git add/commit?)" >&2; exit 2; }

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

sha256sum "${FILES[@]}" > "$tmp"
mv -f "$tmp" "$OUT"
echo "[ok] wrote $OUT (${#FILES[@]} files)"
