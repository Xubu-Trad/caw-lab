#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C

die(){ echo "[fail] $*" >&2; exit 2; }

cd "$(git rev-parse --show-toplevel 2>/dev/null)" || die "not inside a git repo"
mkdir -p history/inbox ledger

test -x ./scripts/ingest_inbox_and_push.sh || die "missing ./scripts/ingest_inbox_and_push.sh"
test -f ./tools/work_history_extract_v1.py || die "missing ./tools/work_history_extract_v1.py"

python3 -m py_compile ./tools/work_history_extract_v1.py || die "extractor does not compile"

RAW_BACKUP_DIR="${RAW_BACKUP_DIR:-$HOME/gilg/_raw_uploads}"
mkdir -p "$RAW_BACKUP_DIR"

resolve_path() {
  local a="$1"
  # Convert Windows-style paths if supplied
  if [[ "$a" =~ ^[A-Za-z]:\\ ]]; then
    command -v wslpath >/dev/null 2>&1 || die "wslpath not found (can't convert Windows paths)"
    a="$(wslpath -u "$a")"
  fi
  printf '%s' "$a"
}

collect_files() {
  local -a out=()
  local a rp
  for a in "$@"; do
    rp="$(resolve_path "$a")"
    if [[ -d "$rp" ]]; then
      # non-recursive *.txt
      while IFS= read -r -d '' f; do out+=("$f"); done < <(find "$rp" -maxdepth 1 -type f -name '*.txt' -print0)
    elif [[ -f "$rp" ]]; then
      out+=("$rp")
    else
      echo "[skip] not found: $a" >&2
    fi
  done

  if (( ${#out[@]} == 0 )); then
    die "no valid files to ingest"
  fi

  # print as NUL-separated list
  printf '%s\0' "${out[@]}"
}

LEDGER_RAW="ledger/raw_uploads.tsv"
test -f "$LEDGER_RAW" || printf "ts\tsha256\traw_backup\torig_base\n" > "$LEDGER_RAW"

tmpnul="$(mktemp)"
collect_files "$@" > "$tmpnul"

count=0
while IFS= read -r -d '' src; do
  base="$(basename "$src")"
  safe="$(echo "$base" | tr -cs 'A-Za-z0-9._-' '_' | sed 's/^_\+//; s/_\+$//')"
  ts="$(date -u +%Y%m%dT%H%M%SZ)"
  bak="$RAW_BACKUP_DIR/${ts}__${safe}"

  cp -f "$src" "$bak"
  chmod 0644 "$bak" || true
  sha="$(sha256sum "$bak" | awk '{print $1}')"
  printf "%s\t%s\t%s\t%s\n" "$ts" "$sha" "$(basename "$bak")" "$base" >> "$LEDGER_RAW"

  echo "[ok] raw backup -> $bak  sha256=$sha"

  # Extract curated attempt blocks into history/inbox (redacted)
  WHX_MAX_BLOCKS="${WHX_MAX_BLOCKS:-60}" \
    python3 tools/work_history_extract_v1.py "$bak" --out history/inbox

  count=$((count+1))
done < "$tmpnul"
rm -f "$tmpnul"

echo "[ok] processed raw file(s): $count"
./scripts/ingest_inbox_and_push.sh
