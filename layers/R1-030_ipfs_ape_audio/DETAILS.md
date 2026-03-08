# R1-030 details

## Role in the chain
This layer turns the book-cipher CID handoff into an exact APE-stage canon receipt.

## Exact canon constants
- CIDv0: `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV`
- canonical uploaded APE bytes: `8968236`
- canonical uploaded APE sha256: `57674107710cdac58fe68b30cb3c05e3334ece55bc0d71deba84ccd2a8fb3575`
- canonical uploaded APE header bytes:
  `4d 41 43 20 96 0f 00 00 34 00 00 00 18 00 00 00 64 01 00 00 00 00 00 00 7c d6 88 00 00 00 00 00`
- non-canonical stripped / zip-copy bytes: `8968098`
- non-canonical stripped / zip-copy sha256: `ea7c96accf476e389aade152efca89bdb92c4c4852e257cb6fe4da8e05b1d263`
- non-canonical stripped / zip-copy header bytes:
  `4d 41 43 20 96 0f 20 20 34 20 20 20 18 20 20 20 64 01 20 20 20 20 20 20 7c d6 88 20 20 20 20 20`

## Exact IPFS add sweep fact
The preserved sweep receipt shows that the target CID `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV` matches the exact add profile:
- chunker: `size-262144`
- raw_leaves: `false`
- trickle: `false`
- wrap: `false`

## What this layer proves
- the canonical byte-identical APE family is pinned to the target CID
- the stripped / zip-copy family is different and non-canonical
- public canon can now distinguish "the right APE" from lookalike copies by exact bytes and exact hash
