> Historical receipt. The current verified R2 decode is documented in [R2 status](../../docs/R2_zrUfKaKV_STATUS.md). Candidate containers below are not steps in that decode.

# R2-010 - Pastebin payload receipt verification

This layer verifies the committed recovered-payload triage receipts only.

## Inputs
- `layers/R2-010_pastebin_payload/EVIDENCE/decoded_files.tsv`
- `layers/R2-010_pastebin_payload/EVIDENCE/jpeg_report.tsv`
- `layers/R2-010_pastebin_payload/EVIDENCE/trailer_report.tsv`
- `layers/R2-010_pastebin_payload/EVIDENCE/r2_numeric_anchors.txt`

## Run from repo root
    set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C
    sha256sum \
      layers/R2-010_pastebin_payload/EVIDENCE/decoded_files.tsv \
      layers/R2-010_pastebin_payload/EVIDENCE/jpeg_report.tsv \
      layers/R2-010_pastebin_payload/EVIDENCE/trailer_report.tsv \
      layers/R2-010_pastebin_payload/EVIDENCE/r2_numeric_anchors.txt
    sed -n '1,40p' layers/R2-010_pastebin_payload/EVIDENCE/decoded_files.tsv
    sed -n '1,40p' layers/R2-010_pastebin_payload/EVIDENCE/jpeg_report.tsv
    sed -n '1,40p' layers/R2-010_pastebin_payload/EVIDENCE/trailer_report.tsv
    sed -n '1,40p' layers/R2-010_pastebin_payload/EVIDENCE/r2_numeric_anchors.txt

## Expected result
The committed text receipts hash cleanly and preview the current promoted state of the recovered Pastebin-payload triage.
