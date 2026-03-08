# R1-020 details

## Role in the chain
This layer applies the preserved coordinate family to a Gilgamesh corpus and hands off into the CID stage.

## Exact canon constants
- Historical target CID: `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV`
- `H00243__full_coords.txt` sha256: `476f7fb5ccffd86fdf306c8a627feeacf8f087afcc22e3ad4b23fa76055c78ea`
- `H00030__cids.txt` sha256: `0973232b8f8db5b2a7883a0d353ead07eb855eea4f496b99785fc08286ba0892`
- `history_extracted_cids.tsv` sha256: `9b9349fab12a6b6441c9ff8cee8a47979d3c70f76d51ec057fa310faf6823a58`

## What this layer proves
- the coordinate family and CID candidate family are preserved as stable text receipts
- the target CID is not folklore only; it is present in multiple preserved receipt families
- the remaining issue is exact public replay, not target identification

## What still must be made explicit for full public determinism
- the exact corpus artifact
- the exact trim / offset rule
- the exact fallback indexing rule
- the exact order that turns the preserved coords into the target CID
