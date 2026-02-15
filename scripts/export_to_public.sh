#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C

die(){ echo "[fail] $*" >&2; exit 2; }

PRIV="$(git rev-parse --show-toplevel 2>/dev/null)" || die "not inside a git repo"
PARENT="$(dirname "$PRIV")"
PUB="$PARENT/caw-lab"

test -d "$PUB/.git" || die "public repo not found at: $PUB (clone it first)"
test -z "$(git -C "$PRIV" status --porcelain=v1)" || die "private repo is dirty; commit/push first"
test -z "$(git -C "$PUB"  status --porcelain=v1)" || die "public repo is dirty; commit/stash first"

bpriv="$(git -C "$PRIV" branch --show-current)"
bpub="$(git -C "$PUB"  branch --show-current)"
[[ "$bpriv" == "canon" ]] || die "private branch must be canon (got: $bpriv)"
[[ "$bpub"  == "canon" ]] || die "public branch must be canon (got: $bpub)"

src_sha="$(git -C "$PRIV" rev-parse --short=12 HEAD)"

# ---- copy allowlist only (no history/, no ledger/, no tools/, no scripts/attempts) ----
copy_allowlist() {
  if command -v rsync >/dev/null 2>&1; then
    rsync -a \
      --include='/layers/***' \
      --include='/docs/***' \
      --include='/.github/***' \
      --include='/LAYER_INDEX.md' \
      --include='/MANIFEST.repo.sha256' \
      --include='/README.md' \
      --include='/SECURITY.md' \
      --include='/LICENSE' \
      --include='/.gitignore' \
      --exclude='*' \
      "$PRIV/" "$PUB/"
  else
    # fallback: tar copy only allowlist paths
    ( cd "$PRIV" && tar -cf - \
        layers docs .github \
        LAYER_INDEX.md MANIFEST.repo.sha256 README.md SECURITY.md LICENSE .gitignore \
      ) | ( cd "$PUB" && tar -xf - )
  fi
}

copy_allowlist

# ---- safety checks: ensure no private stuff landed in public ----
# deny-list paths that must NEVER exist in public
for bad in history ledger tools scripts/attempts; do
  if [ -e "$PUB/$bad" ]; then
    die "public export contains forbidden path: $bad"
  fi
done

# quick leak pattern scan
LEAKS="$(mktemp)"
grep -RIna --exclude-dir .git -E '/mnt/c/Users/|C:\\Users\\|/Users/[^/]+/My Drive' "$PUB" >"$LEAKS" || true
if [[ "$(wc -l <"$LEAKS")" != "0" ]]; then
  echo "[fail] leak lines found in public repo:" >&2
  sed -n '1,120p' "$LEAKS" >&2
  rm -f "$LEAKS"
  die "privacy leak detected in public export"
fi
rm -f "$LEAKS"

# ---- commit/push public if changed ----
if [[ -z "$(git -C "$PUB" status --porcelain=v1)" ]]; then
  echo "[ok] public repo already up to date (no changes)."
  exit 0
fi

git -C "$PUB" add -A
msg="${1:-export: sync allowlist from private ${src_sha}}"
git -C "$PUB" commit -m "$msg"
git -C "$PUB" push origin HEAD
echo "[ok] exported to public and pushed"
