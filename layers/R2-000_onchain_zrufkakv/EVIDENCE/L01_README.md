# L01 — ZRU merge series (curated)

## Claim
Curated receipts for R2 (zrUfKaKV) “zru merge” exploration from a single imported bundle.

## Inputs (provenance)
Source bundle: history/chatgpt_uploads/20260215T001500Z/
Validate bundle manifest:
  (cd history/chatgpt_uploads/20260215T001500Z && sed -E '/ (MANIFEST\.sha256|MANIFEST\.tsv)$/d' MANIFEST.sha256 | sha256sum -c -)

## Transform
Copy-only curation (history → layers) performed in repo root:
  TS=20260215T001500Z
  L=layers/R2_zrUfKaKV/L01__zru_merge_series_${TS}
  cp -a history/chatgpt_uploads/$TS/manifesto_replicate_*zru_merge* $L/src/

## Outputs
See SHA256SUMS.txt for the curated file hashes.

## Validation
(cd layers/R2_zrUfKaKV/L01__zru_merge_series_20260215T001500Z && sha256sum -c SHA256SUMS.txt)

## Notes
- This layer is receipts-only; it does not claim the underlying cryptanalytic step is solved.
- Any interpretation must be reproducible from these sources + scripts.
