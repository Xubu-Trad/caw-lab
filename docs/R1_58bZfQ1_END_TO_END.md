# R1 (58bZfQ1) - end-to-end narrative

## Goal
Explain the first riddle in one place so a new reader can understand the full chain, while also seeing exactly which parts are receipt-backed, which parts are historically stable, and which parts still need a fully public deterministic replay.

## Public anchors
- R1 transaction: `0xfbbcf5338b4a9c35073ac7253afc1a8ee81770d8d3285b80497bbd9c2186ed5b`
- Public image slug: `58bZfQ1`
- Image URL: `https://ibb.co/58bZfQ1`
- Historical IPFS CID: `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV`
- DeepSound password: `enkidu`

## Canon chain
1. **On-chain anchor**
   - The short code `58bZfQ1` is emitted on-chain and serves as the public entrypoint to the first riddle.

2. **Image entrypoint**
   - `58bZfQ1` resolves to the Yale / OldKing tablet image.
   - This image is the public artifact from which the poem, coordinates, and follow-on instructions are derived.

3. **Poem / Friderici / coordinate layer**
   - This stage yields the poem, the coordinate list, the fallback letter-count note, and the mirror / backwards hints.
   - These receipts are public-canon stable.

4. **Book-cipher stage**
   - Preserved receipts show a stable historical target CID: `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV`.
   - The current public repo does **not yet** make that CID fall out deterministically from the committed corpus with one bounded replay.
   - The unresolved part is the exact cleaned corpus / trim / offset / indexing combination for the archive-oriented Gilgamesh text.

5. **IPFS / APE stage**
   - Preserved receipts show that the target CID corresponds to a real APE-stage artifact.
   - `ffprobe` receipts identify a Monkey's Audio stream of duration `135.231583` seconds at `48000 Hz`, stereo.
   - Preserved stripped-copy receipts document at least two binary variants of the same APE family:
     - `8968236` bytes, sha256 `57674107710cdac58fe68b30cb3c05e3334ece55bc0d71deba84ccd2a8fb3575`
     - `8968098` bytes, sha256 `ea7c96accf476e389aade152efca89bdb92c4c4852e257cb6fe4da8e05b1d263`
   - Public canon treats the audio stage as locally verified from receipts, but not yet one-command rebuilt from public text artifacts alone.

6. **DeepSound / Enkidu stage**
   - Public evidence preserves both the nibble-sub / hex-like `enkidu.txt` artifact and the more legible stage text `enkidu.stage0.txt`.
   - This proves the riddle passes through an Enkidu intermediate text lane.
   - Public canon does **not yet** claim that the current repo alone reruns the original DeepSound extraction end to end.

7. **Final manifesto stage**
   - Public evidence preserves both a historically recovered manifesto text and a normalized English rendering.
   - This shows the manifesto payload family is real and stable.
   - Public canon still stops short of claiming a one-command replay from the currently committed Enkidu evidence to the final normalized English text.

## Current honest status
R1 is now receipt-backed from public anchor through manifesto family. The remaining gap is not whether the chain exists, but whether every step can be replayed deterministically from the public repo alone with exact corpus and transform rules.

## What still needs to be made fully public-canon deterministic
- exact Gilgamesh corpus artifact and normalization
- exact trim / offset / blank-line handling for the book cipher
- exact public replay path from CID receipts to APE identity
- exact public replay of the Enkidu extraction lane
- exact public replay from Enkidu-stage receipts to normalized manifesto text

## Determinism note
- `docs/R1_DETERMINISM_STATUS.md`

## Layer map
- `layers/R1-000_yale_oldking/`
- `layers/R1-010_friderici_poem_coords/`
- `layers/R1-020_book_cipher_gilgamesh/`
- `layers/R1-030_ipfs_ape_audio/`
- `layers/R1-040_deepsound_enkidu/`
- `layers/R1-050_manifesto_final_payload/`
