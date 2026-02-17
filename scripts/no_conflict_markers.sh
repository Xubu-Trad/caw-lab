#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'; LC_ALL=C

cd "$(git rev-parse --show-toplevel)"

if grep -RInE '^(<<<<<<<|=======|>>>>>>>)' README.md docs layers >/dev/null; then
  echo "[fail] merge conflict markers found (<<<<<<< ======= >>>>>>>)"
  grep -RInE '^(<<<<<<<|=======|>>>>>>>)' README.md docs layers | head -n 200
  exit 1
fi

echo "[ok] no merge conflict markers"
