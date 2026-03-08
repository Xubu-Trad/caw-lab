# R1-050 - manifesto payload receipt verification

This layer verifies the committed manifesto-payload receipts only.

## Inputs
- `layers/R1-050_manifesto_final_payload/EVIDENCE/manifesto.recovered.txt`
- `layers/R1-050_manifesto_final_payload/EVIDENCE/manifesto.en.txt`

## Run from repo root
    set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C
    sha256sum \
      layers/R1-050_manifesto_final_payload/EVIDENCE/manifesto.recovered.txt \
      layers/R1-050_manifesto_final_payload/EVIDENCE/manifesto.en.txt
    sed -n '1,40p' layers/R1-050_manifesto_final_payload/EVIDENCE/manifesto.recovered.txt
    sed -n '1,40p' layers/R1-050_manifesto_final_payload/EVIDENCE/manifesto.en.txt

## Expected result
The committed text receipts hash cleanly and preview the manifesto payload state currently promoted into canon.
