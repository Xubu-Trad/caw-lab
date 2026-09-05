# R1 determinism status

## Purpose
State exactly what is stable in public canon and exactly what still prevents a fully deterministic public replay.

## Stable canon constants
- R1 transaction ID: `0xfbbcf5338b4a9c35073ac7253afc1a8ee81770d8d3285b80497bbd9c2186ed5b`
- Public short code: `58bZfQ1`
- Public image URL: `https://ibb.co/58bZfQ1`
- Historical target CID: `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV`
- Canonical uploaded APE sha256: `57674107710cdac58fe68b30cb3c05e3334ece55bc0d71deba84ccd2a8fb3575`
- Non-canonical stripped / zip-copy sha256: `ea7c96accf476e389aade152efca89bdb92c4c4852e257cb6fe4da8e05b1d263`
- Enkidu pseudo-hex sha256: `4f4edfdece802b300aeab48932b115d83eb04575753bfd128a3cc47c5cc25b19`
- Manifesto recovered sha256: `e5816ee2a75a1c939543773983f8b6d2b9eb05afee8d4f9ac91336e8ab6c01fa`
- Manifesto English sha256: `836c98641fd1222156d49c68d210d9860319b323f890b5af82860ac14aba366c`

## What is already receipt-backed
- the public anchor
- the historical target CID
- the canonical APE receipt versus the non-canonical stripped family
- the Enkidu pseudo-hex intermediate
- the normalized manifesto family

## Exact determinism gap
The image-to-clues and public-corpus-to-CID steps now reproduce independently, as does the preserved Enkidu-to-English conversion. [Book-cipher receipt](../layers/R1-020_book_cipher_gilgamesh/REPRODUCE.md). A fresh byte-verified live audio retrieval and independent extraction of the preserved Enkidu bytes from canonical APE remain open. Historical audio receipts are retained.

## Why the gap is narrow now
The uploaded receipts fix the target constants. The remaining problem is not "what is the target?" but "which exact public replay recipe reaches the target without relying on historical side knowledge?"

## Reproduced text conversion (2026-09-05)

Run `python3 scripts/reproduce_enkidu.py` from the repository checkout, preserving the committed byte-level line endings. The script verifies the input hash, translates `UVWXYZ` to `fedcba`, hex-decodes, and replaces exactly 60 tab bytes with single spaces. Its 10,596-byte output exactly matches the committed `manifesto.en.txt` hash listed above.

See [the reproduction receipt](../layers/R1-040_deepsound_enkidu/REPRODUCE.md) for the intermediate hash and checks. This recipe was derived by comparing preserved input and target artifacts; it does not establish the historical solver’s method or resolve upstream audio extraction. The separate public book-cipher replay now closes the corpus-to-CID step. R2 remains unsolved.

## Reproduced tablet extraction (2026-09-05)

The original tablet now reproduces both the 46 coordinates and literal poem. [Run the exact image replay](../layers/R1-010_friderici_poem_coords/REPRODUCE.md). This closes the image-to-clues step; the independent audio extraction gap remains open. The public corpus-to-CID recipe now reproduces.
