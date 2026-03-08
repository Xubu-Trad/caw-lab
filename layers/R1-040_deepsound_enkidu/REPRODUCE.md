# R1-040 — Enkidu receipt verification

## Inputs
- `layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.full_pseudohex.txt`
- `layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.stage0.txt`

## Run from repo root
    set -u
    IFS=$'\n\t'
    LC_ALL=C
    sha256sum                   layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.full_pseudohex.txt                   layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.stage0.txt
    sed -n '1,20p' layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.full_pseudohex.txt
    printf '\n[tail]\n'
    tail -n 5 layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.full_pseudohex.txt
    printf '\n[stage0]\n'
    sed -n '1,40p' layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.stage0.txt

## Expected result
The full pseudo-hex body and the stage text both hash cleanly and are visibly present inside the layer.
