# R1-030 - IPFS / APE receipt verification

This layer verifies the committed APE-stage receipts only.

## Inputs
- `layers/R1-030_ipfs_ape_audio/EVIDENCE/ffprobe_ape.txt`
- `layers/R1-030_ipfs_ape_audio/EVIDENCE/ape_checks.txt`
- `layers/R1-030_ipfs_ape_audio/EVIDENCE/ape_stripped_paths.txt`

## Run from repo root
    set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C
    sha256sum \
      layers/R1-030_ipfs_ape_audio/EVIDENCE/ffprobe_ape.txt \
      layers/R1-030_ipfs_ape_audio/EVIDENCE/ape_checks.txt \
      layers/R1-030_ipfs_ape_audio/EVIDENCE/ape_stripped_paths.txt
    sed -n '1,40p' layers/R1-030_ipfs_ape_audio/EVIDENCE/ffprobe_ape.txt
    sed -n '1,40p' layers/R1-030_ipfs_ape_audio/EVIDENCE/ape_checks.txt
    sed -n '1,40p' layers/R1-030_ipfs_ape_audio/EVIDENCE/ape_stripped_paths.txt

## Expected result
The committed text receipts hash cleanly and preview the tracked APE-audio identification and triage state for this layer.
