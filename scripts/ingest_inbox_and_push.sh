#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C

die() { echo "[fail] $*" >&2; exit 2; }

cd "$(git rev-parse --show-toplevel 2>/dev/null)" || die "not inside a git repo"
mkdir -p history/inbox history/ingested ledger

LEDGER="ledger/history_ingest.tsv"
test -f "$LEDGER" || printf "ts\tsha256\tdst\tsrc\n" > "$LEDGER"

shopt -s nullglob
files=(history/inbox/*)
if (( ${#files[@]} == 0 )); then
  echo "[ok] inbox empty: history/inbox/"
  exit 0
fi

count=0
for src in "${files[@]}"; do
  test -f "$src" || continue
  base="$(basename "$src")"
  safe="$(echo "$base" | tr -cs 'A-Za-z0-9._-' '_' | sed 's/^_\+//; s/_\+$//')"
  ts="$(date -u +%Y%m%dT%H%M%SZ)"
  dst="history/ingested/${ts}__${safe}"

  mv -f "$src" "$dst"
  chmod 0644 "$dst" || true
  sha="$(sha256sum "$dst" | awk '{print $1}')"
  printf "%s\t%s\t%s\t%s\n" "$ts" "$sha" "$dst" "$base" >> "$LEDGER"
  echo "[ok] moved -> $dst  sha256=$sha"
  count=$((count+1))
done

./scripts/update_attempts_and_push.sh "attempts: ingest inbox (${count} file(s))"
