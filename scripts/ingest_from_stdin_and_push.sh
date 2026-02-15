#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C

die(){ echo "[fail] $*" >&2; exit 2; }

cd "$(git rev-parse --show-toplevel 2>/dev/null)" || die "not inside a git repo"
mkdir -p history/inbox

name="${1:-}"
test -n "$name" || die "usage: $0 <name_like_chatlog.txt>   (then paste, then Ctrl-D)"

safe="$(echo "$name" | tr -cs 'A-Za-z0-9._-' '_' | sed 's/^_\\+//; s/_\\+$//')"
ts="$(date -u +%Y%m%dT%H%M%SZ)"
dst="history/inbox/${ts}__${safe}"

echo "[ok] paste now. finish with Ctrl-D."
cat > "$dst"
chmod 0644 "$dst" || true
echo "[ok] wrote -> $dst"

./scripts/ingest_inbox_and_push.sh
