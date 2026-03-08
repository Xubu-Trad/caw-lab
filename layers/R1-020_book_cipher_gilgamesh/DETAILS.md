# R1-020 details

## Role in the chain
This layer applies the canonical coordinate list to a Gilgamesh corpus in order to produce the CID handoff into the audio stage.

## What this layer proves
- the coordinate set is preserved as a stable historical receipt
- the CID candidate family is preserved as a stable historical receipt
- the target CID `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV` appears repeatedly in preserved logs
- the missing piece is not "whether a CID exists", but "which exact public corpus normalization and offset recipe reproduces it deterministically"

## What is publicly receipt-backed right now
- `EVIDENCE/full_coords_from_history.txt` preserves the historical coordinate list
- `EVIDENCE/cids.txt` preserves the broader CID candidate family and includes the target CID
- `EVIDENCE/history_extracted_cids.tsv` shows the target CID recurring in preserved extraction history

## What is not yet claimed
Public canon does **not** currently claim that a reader can take the committed public corpus, run one exact documented command, and deterministically reproduce the target CID with no ambiguity. That corpus/offset recipe is still the unresolved public-determinism gap.

## Why this matters
The book-cipher lane is now honest: the CID target is stable, but the exact public replay still needs the final corpus-normalization recipe to be spelled out.

## Evidence in this layer
- `EVIDENCE/full_coords_from_history.txt`
- `EVIDENCE/cids.txt`
- `EVIDENCE/history_extracted_cids.tsv`

## Reader handoff
Continue to `../R1-030_ipfs_ape_audio/DETAILS.md`.
## Cross-reference
See `../../docs/R1_DETERMINISM_STATUS.md` for the current public determinism gap summary.

