#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C

die() { echo "[fail] $*" >&2; exit 2; }

cd "$(git rev-parse --show-toplevel 2>/dev/null)" || die "not inside a git repo"
mkdir -p history/ingested

src="${1:-}"
test -n "$src" || die "usage: $0 /path/to/file"
test -f "$src" || die "not a file: $src"

base="$(basename "$src")"
safe="$(echo "$base" | tr -cs 'A-Za-z0-9._-' '_' | sed 's/^_\+//; s/_\+$//')"
ts="$(date -u +%Y%m%dT%H%M%SZ)"
dst="history/ingested/${ts}__${safe}"

cp -a "$src" "$dst"
sha="$(sha256sum "$dst" | awk '{print $1}')"

echo "[ok] copied -> $dst"
echo "[ok] sha256  -> $sha"

./scripts/update_attempts_and_push.sh "attempts: ingest ${safe} (${ts})"
