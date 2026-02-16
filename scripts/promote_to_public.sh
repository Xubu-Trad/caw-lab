#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

PRIV="${PRIV:-$HOME/gilg/caw-lab-private}"
PUB="${PUB:-$HOME/gilg/caw-lab}"

test -d "$PRIV/.git" || { echo "[FAIL] missing private repo: $PRIV"; exit 2; }
test -d "$PUB/.git"  || { echo "[FAIL] missing public repo:  $PUB"; exit 2; }

cd "$PRIV"
git fetch origin --prune
git switch -C canon origin/canon

cd "$PUB"
git fetch origin --prune
git switch -C canon origin/canon
git reset --hard origin/canon
git clean -fd

rsync -a --delete \
  --include='/layers/***' \
  --include='/docs/***' \
  --include='/scripts/***' \
  --include='/tools/***' \
  --include='/LAYER_INDEX.md' \
  --include='/README.md' \
  --include='/LICENSE' \
  --include='/SECURITY.md' \
  --exclude='/**/.git' \
  --exclude='/**/history/***' \
  --exclude='/**/ledger/***' \
  --exclude='/**/LAB/***' \
  --exclude='*' \
  "$PRIV/" "$PUB/"

cd "$PUB"
test ! -e history || { echo "[FAIL] history/ leaked into public"; exit 3; }

git add -A
git status -sb
git commit -m "sync: promote allowlisted canon layers/docs/tools/scripts" || true
git push -v origin canon
