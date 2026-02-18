#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'; LC_ALL=C

out="OUT/layer_audit/$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$out"

fail=0
warn=0

echo "[audit] scanning top-level layers under ./layers" | tee "$out/summary.txt"
mapfile -t layers_dirs < <(find layers -mindepth 1 -maxdepth 1 -type d ! -name TEMPLATE | LC_ALL=C sort)

# patterns we consider “anchors present”
anchor_re='0x[a-fA-F0-9]{40}|0x[a-fA-F0-9]{64}|etherscan|58bZfQ1|zrUfKaKV|ipfs|Qm[1-9A-HJ-NP-Za-km-z]{44}'

for d in "${layers_dirs[@]}"; do
  echo "== $d ==" | tee -a "$out/summary.txt"

  # Required files for a “professional canon layer”
  for f in SUMMARY.md REPRODUCE.md; do
    if [ ! -f "$d/$f" ]; then
      echo "  [MISS] $f" | tee -a "$out/summary.txt"
      fail=1
    fi
  done

  # Recommended evidence folder + README
  if [ ! -d "$d/EVIDENCE" ]; then
    echo "  [WARN] missing EVIDENCE/ folder" | tee -a "$out/summary.txt"
    warn=1
  else
    if [ ! -f "$d/EVIDENCE/README.md" ]; then
      echo "  [WARN] missing EVIDENCE/README.md" | tee -a "$out/summary.txt"
      warn=1
    fi
    # Evidence folder should contain something besides README (or explain why not)
    nfiles="$(find "$d/EVIDENCE" -type f 2>/dev/null | wc -l | tr -d ' ')"
    if [ "$nfiles" -le 1 ]; then
      echo "  [WARN] EVIDENCE has no files beyond README (add receipts or explain)" | tee -a "$out/summary.txt"
      warn=1
    fi
  fi

  # Anchor presence check (should be in SUMMARY/REPRODUCE at minimum)
  if ! ( [ -f "$d/SUMMARY.md" ] && grep -qiE "$anchor_re" "$d/SUMMARY.md" ) \
     && ! ( [ -f "$d/REPRODUCE.md" ] && grep -qiE "$anchor_re" "$d/REPRODUCE.md" ); then
    echo "  [WARN] no obvious onchain/IPFS anchor text found in SUMMARY/REPRODUCE" | tee -a "$out/summary.txt"
    warn=1
  fi
done

echo
echo "[audit] report: $out/summary.txt"
if [ "$fail" -ne 0 ]; then
  echo "[fail] missing required layer files (SUMMARY/REPRODUCE). Fix before calling canon “professional”." >&2
  exit 1
fi

if [ "$warn" -ne 0 ]; then
  echo "[warn] audit completed with warnings (anchors/receipts professionalism)." >&2
else
  echo "[ok] audit clean." >&2
fi
