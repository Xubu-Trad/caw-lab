# R1-000 details

## Scope
This layer is the first-riddle public anchor and provenance layer. Its job is to state the public entrypoint family clearly, without over-claiming later decode stages.

## Proven receipts
- The first riddle begins from an on-chain short-code trailhead associated with the CAW deployer's self-message pattern.
- The public short code for R1 is `58bZfQ1`.
- That short code resolves to the public image clue commonly referred to as the Yale / OldKing / first-clue tablet image.
- This layer is intentionally limited to the entrypoint and its provenance role. It does not claim poem extraction, coordinate extraction, corpus selection, CID derivation, APE decoding, or manifesto recovery. Those belong to later layers.

## Why this layer exists
The public repo should not force readers to infer where R1 starts. This layer exists so an auditor can understand that the puzzle has a public trailhead before any stego or corpus work begins.

## Evidence in this layer
- `EVIDENCE/00_inputs.txt` — public-anchor receipt text
- `EVIDENCE/README.md` — short description of evidence scope

## Boundaries
Not claimed here:
- no full poem claim
- no coordinate claim
- no book-cipher claim
- no CID claim
- no APE / DeepSound / manifesto claim
