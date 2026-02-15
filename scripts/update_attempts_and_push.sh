#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C

die() {
  echo "[fail] $*" >&2
  exit 2
}

cd "$(git rev-parse --show-toplevel 2>/dev/null)" || die "not inside a git repo"

test -d history || die "missing history/"
test -d tools   || die "missing tools/"

# 1) rebuild derived artifacts
python3 tools/attempts_full_bootstrap.py --force
python3 tools/matrix_full_build.py
python3 tools/matrix_full_build.py --check

# 2) privacy guard
python3 tools/privacy_guard.py

# 3) leak grep (extra belt)
LEAKS="$(mktemp)"
grep -RIna --exclude-dir .git -E '/mnt/c/Users/|C:\\Users\\|/Users/[^/]+/My Drive' history docs ledger >"$LEAKS" || true
if [[ "$(wc -l <"$LEAKS")" != "0" ]]; then
  echo "[fail] leak lines found:" >&2
  sed -n '1,80p' "$LEAKS" >&2
  rm -f "$LEAKS"
  die "privacy leak detected"
fi
rm -f "$LEAKS"

# IMPORTANT: include untracked files in the "no changes" check
if [[ -z "$(git status --porcelain=v1)" ]]; then
  echo "[ok] no changes to commit."
  exit 0
fi

git add -A
msg="${1:-attempts: ingest history + rebuild matrix}"
git commit -m "$msg"
git push origin HEAD
echo "[ok] pushed"
