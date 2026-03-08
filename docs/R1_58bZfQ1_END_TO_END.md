# R1 (58bZfQ1) — end-to-end narrative

## Goal
Explain the first riddle in one place so a new reader can understand the full intended chain before dropping into the per-layer receipts.

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
   - This image is the public artifact from which the hidden poem, coordinates, and follow-on instructions are derived.

3. **Poem / Friderici / coordinate layer**
   - The image yields two kinds of instruction material:
     - visible/overlay text around the “old King / 11 tablets / red herring / song” theme
     - hidden text / metadata / Friderici-style extraction leading to the canonical coordinate list
   - This stage also preserves the “fallback letter-count” rule and mirror/backwards instructions.

4. **Book-cipher stage**
   - The coordinates are applied against a Gilgamesh corpus.
   - This is the stage where corpus cleanliness / offset / trim matter.
   - Historical work says this stage yields the CID `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV`.
   - Public canon must distinguish between:
     - what is historically claimed
     - what is locally reproducible from committed text receipts

5. **IPFS / APE stage**
   - The CID is associated with an APE payload.
   - Community narrative identifies the audio as Leonardo da Vinci / “Tre rebus musicali”.
   - Public canon should preserve exactly what is locally verified and what remains historical-but-not-currently-rebuilt.

6. **DeepSound / Enkidu stage**
   - The audio is said to conceal a hidden file extractable with DeepSound using password `enkidu`.
   - The resulting artifact is `enkidu.txt`.

7. **Final payload stage**
   - `enkidu.txt` is treated as an encoded intermediate that ultimately resolves into the manifesto payload.
   - Public canon must say clearly whether each transform is:
     - fully reproduced,
     - historically attested only,
     - or still unresolved on current artifacts.

## What still needs to be made fully public-canon deterministic
- exact Gilgamesh corpus choice
- exact trim / offset / empty-line handling that makes the book-cipher deterministic
- exact APE retrieval and identity verification path
- exact `enkidu.txt` transform chain that reproduces the final payload on current committed artifacts

## Layer map
- `layers/R1-000_yale_oldking/`
- `layers/R1-010_friderici_poem_coords/`
- `layers/R1-020_book_cipher_gilgamesh/`
- `layers/R1-030_ipfs_ape_audio/`
- `layers/R1-040_deepsound_enkidu/`
- `layers/R1-050_manifesto_final_payload/`

