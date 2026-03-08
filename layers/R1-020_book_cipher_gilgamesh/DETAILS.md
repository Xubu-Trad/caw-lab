# R1-020 details

## Role in the chain
This layer applies the coordinate list to a Gilgamesh corpus to derive the CID handoff.

## Public anchors
- Historical CID: `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV`

## What this layer proves
- book-cipher work was attempted and logged
- coordinate and CID candidate receipts exist
- the corpus-selection / trimming issue is real and must be made deterministic for public canon

## Core question for this layer
Which exact corpus text, trim, offset, and empty-line behavior make the coordinate application yield the historical CID?

## Evidence in this layer
- `EVIDENCE/full_coords_from_history.txt`
- `EVIDENCE/cids.txt`
- `EVIDENCE/history_extracted_cids.tsv`

## What still needs to be explicit here
- the exact corpus artifact used
- the exact coordinate interpretation rules
- whether the historical CID is:
  - fully reproduced from committed artifacts, or
  - preserved as historical ground truth pending full deterministic replay

## Reader handoff
Continue to `../R1-030_ipfs_ape_audio/DETAILS.md`.

