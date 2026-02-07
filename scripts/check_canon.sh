set -Eeuo pipefail; LC_ALL=C
cd "$(git rev-parse --show-toplevel)"

test -f MANIFEST.repo.sha256 || { echo "[fail] MANIFEST.repo.sha256 missing"; exit 1; }
test -x scripts/no_tracked_binaries.sh || { echo "[fail] scripts/no_tracked_binaries.sh missing"; exit 1; }
test -x scripts/verify_manifest.sh || { echo "[fail] scripts/verify_manifest.sh missing"; exit 1; }

bash scripts/no_tracked_binaries.sh

# Reject empty evidence receipts anywhere under layers/**/EVIDENCE
bad=$(find layers -type f -path "*/EVIDENCE/*" -size 0c -print 2>/dev/null || true)
if test -n "$bad"; then
  echo "[fail] empty evidence files found (0 bytes):"
  printf "%s\n" "$bad" | sed "s/^/ - /"
  echo "[hint] replace with real receipts or a placeholder text (never 0-byte)"
  exit 1
fi

bash scripts/verify_manifest.sh
echo "[ok] canon checks passed"
