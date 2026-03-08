# R2-000 - on-chain zrUfKaKV receipt verification

This layer verifies the committed R2 on-chain receipts only.

## Inputs
- `layers/R2-000_onchain_zrufkakv/EVIDENCE/R2_zrUfKaKV_STATUS.md`
- any `L01_*` or `L02_*` files present in `layers/R2-000_onchain_zrufkakv/EVIDENCE/`

## Run from repo root
    set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C
    find layers/R2-000_onchain_zrufkakv/EVIDENCE -maxdepth 1 -type f -print0 | xargs -0 sha256sum
    for f in layers/R2-000_onchain_zrufkakv/EVIDENCE/*; do
      [ -f "$f" ] || continue
      echo "==== $f ===="
      sed -n '1,40p' "$f"
    done

## Expected result
The committed text receipts hash cleanly and preview the current promoted R2 on-chain status and checksum artifacts.
