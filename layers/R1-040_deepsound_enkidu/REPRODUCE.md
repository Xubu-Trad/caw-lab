# R1-040 - DeepSound / Enkidu receipt verification

This layer verifies the committed Enkidu-stage receipts only.

## Inputs
- `layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.stage0.txt`
- `layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.txt`

## Run from repo root
    set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C
    sha256sum \
      layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.stage0.txt \
      layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.txt
    sed -n '1,40p' layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.stage0.txt
    sed -n '1,40p' layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.txt

## Expected result
The committed text receipts hash cleanly and preview the tracked Enkidu-stage content promoted into canon for this layer.
