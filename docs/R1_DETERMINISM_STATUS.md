# R1 determinism status

## Purpose
This note explains exactly what remains between the current public R1 canon and a fully deterministic public replay.

## What is now stable
The public canon is no longer just narrative. It is backed by preserved receipts showing:

- a stable historical target CID:
  `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV`
- an APE-stage handoff verified in preserved receipts
- an Enkidu-stage intermediate preserved as text artifacts
- a final manifesto family preserved as recovered and normalized text

## What is still missing for full public determinism
The remaining gap is now narrow and specific:

1. **Exact book-cipher corpus recipe**
   - exact corpus artifact
   - exact cleaning / trimming
   - exact offset handling
   - exact indexing behavior

2. **Exact public APE replay**
   - a bounded public method that moves from CID receipts to the verified APE-stage artifact

3. **Exact Enkidu-to-manifesto replay**
   - a bounded public method that moves from the committed Enkidu-stage receipts to the final normalized manifesto text

## Honest current public claim
The R1 chain is receipt-backed end to end as a historical and locally verified artifact family.
What the public repo still does not claim is a single one-command deterministic replay for every step.

## Where this connects
- `docs/R1_58bZfQ1_END_TO_END.md`
- `layers/R1-020_book_cipher_gilgamesh/`
- `layers/R1-030_ipfs_ape_audio/`
- `layers/R1-040_deepsound_enkidu/`
- `layers/R1-050_manifesto_final_payload/`
