#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C

MAN="${1:-MANIFEST.repo.sha256}"
[[ -f "$MAN" ]] || { echo "missing manifest: $MAN" >&2; exit 2; }

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

bash scripts/make_manifest.sh "$tmp" >/dev/null

if ! diff -u "$MAN" "$tmp"; then
  echo "[fail] manifest mismatch: $MAN" >&2
  exit 1
fi
echo "[ok] manifest verified: $MAN"
