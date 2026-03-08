# R2-010 details

## Role in the chain
This layer records the recovered-payload triage for the second riddle.

## What this layer proves
- decoded-file receipts exist
- JPEG-head / JPEG-trailer structure was observed and preserved
- numeric anchors were extracted and committed
- this layer is analysis-state canon, not solved-state canon

## Evidence in this layer
- `EVIDENCE/decoded_files.tsv`
- `EVIDENCE/jpeg_report.tsv`
- `EVIDENCE/trailer_report.tsv`
- `EVIDENCE/r2_numeric_anchors.txt`

## What still needs to be explicit here
- what each decoded file came from
- which outputs are strongest candidates for the real payload
- which observations are red herrings vs promising lanes
- how this triage connects back to the on-chain anchor and forward into lane work

## Reader handoff
See `../../docs/R2_zrUfKaKV_STATUS.md`.

