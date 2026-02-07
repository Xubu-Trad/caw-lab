#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C

usage() {
  cat <<EOF
usage: $0 --tag <layer-tag> --public-path <path-to-caw-canon> [--dry-run]
  Example:
    $0 --tag layer-R1-030 --public-path ../caw-canon --dry-run
EOF
}

TAG=""
PUB=""
DRY=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --tag) TAG="${2:-}"; shift 2;;
    --public-path) PUB="${2:-}"; shift 2;;
    --dry-run) DRY=1; shift 1;;
    -h|--help) usage; exit 0;;
    *) echo "unknown arg: $1" >&2; usage; exit 2;;
  esac
done

[[ -n "$TAG" && -n "$PUB" ]] || { usage; exit 2; }

# Preconditions
git rev-parse --show-toplevel >/dev/null
ROOT="$(git rev-parse --show-toplevel)"
BR="$(git rev-parse --abbrev-ref HEAD)"
[[ "$BR" == "canon" ]] || { echo "must run from caw-lab branch 'canon' (current: $BR)" >&2; exit 2; }

git diff --quiet || { echo "dirty working tree in caw-lab; commit/stash first" >&2; exit 2; }

git show-ref --tags --verify --quiet "refs/tags/$TAG" || { echo "missing tag: $TAG" >&2; exit 2; }
SRC_COMMIT="$(git rev-list -n 1 "$TAG")"

# Verify manifest before publishing
if [[ -f scripts/verify_manifest.sh ]]; then
  bash scripts/verify_manifest.sh
fi

# Public repo checks
[[ -d "$PUB/.git" ]] || { echo "public-path is not a git repo: $PUB" >&2; exit 2; }

pushd "$PUB" >/dev/null
git diff --quiet || { echo "dirty working tree in public repo; commit/stash first" >&2; exit 2; }

# Add local remote to caw-lab if missing
if ! git remote get-url lab >/dev/null 2>&1; then
  git remote add lab "$ROOT"
fi
git fetch --tags lab

# Ensure tag exists locally after fetch
git show-ref --tags --verify --quiet "refs/tags/$TAG" || { echo "tag not fetched into public repo: $TAG" >&2; exit 2; }

# Cherry-pick the tagged commit
echo "[info] promoting $TAG ($SRC_COMMIT) into public repo"
if [[ "$DRY" -eq 1 ]]; then
  echo "[dry-run] would run: git cherry-pick $TAG"
  echo "[dry-run] would tag+push: $TAG"
  popd >/dev/null
  exit 0
fi

git cherry-pick "$TAG"

# Signed annotated tag in public
git tag -s "$TAG" -m "Promoted $TAG from caw-lab@$SRC_COMMIT"

git push origin HEAD:main
git push origin "$TAG"
popd >/dev/null

echo "[ok] published $TAG to public repo"
