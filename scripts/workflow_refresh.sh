#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'; LC_ALL=C

cd "$(git rev-parse --show-toplevel)"

# 0) (Optional) show dirty state but don't block
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "[WARN] uncommitted changes present"
fi

# 1) Re-generate derived docs/index
python3 scripts/gen_layer_index.py --write

# 2) IMPORTANT: rebuild manifest AFTER all files exist
bash scripts/make_manifest.sh MANIFEST.repo.sha256
bash scripts/verify_manifest.sh

# 3) Re-run local gates
bash scripts/sanitize_audit.sh
python3 scripts/gen_layer_index.py --check
bash scripts/audit_layers.sh

echo "[ok] workflow_refresh complete"
