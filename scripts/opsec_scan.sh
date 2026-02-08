#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

echo "[opsec] scanning tracked files for common secret/PII patterns..."
FILES="$(git ls-files)"

echo
echo "[opsec] tokens / private keys"
git grep -nI -E -e '-----BEGIN (OPENSSH|RSA|EC|DSA) PRIVATE KEY-----|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|AIzaSy[0-9A-Za-z_-]{20,}|AKIA[0-9A-Z]{16}' -- $FILES || true

echo
echo "[opsec] email addresses (review anything not @users.noreply.github.com)"
git grep -nI -E -e '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' -- $FILES || true

echo
echo "[opsec] local paths / usernames (review)"
git grep -nI -E -e '/mnt/c/Users/|/home/[A-Za-z0-9._-]+/|DESKTOP-[A-Z0-9-]+' -- $FILES || true

echo
echo "[opsec] IP addresses (review)"
git grep -nI -E -e '([0-9]{1,3}\.){3}[0-9]{1,3}' -- $FILES || true

echo
echo "[ok] opsec_scan complete (review hits, then decide sanitize vs keep)"
