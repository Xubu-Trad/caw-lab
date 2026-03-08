# R1-000 - public anchor receipt verification

This layer verifies the committed text receipt only.

## Inputs
- `layers/R1-000_yale_oldking/EVIDENCE/00_inputs.txt`

## Run from repo root
    set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C
    sha256sum layers/R1-000_yale_oldking/EVIDENCE/00_inputs.txt
    sed -n '1,80p' layers/R1-000_yale_oldking/EVIDENCE/00_inputs.txt

## Expected result
The file hashes cleanly and previews as the tracked public-anchor provenance receipt for the first-riddle entrypoint layer.
