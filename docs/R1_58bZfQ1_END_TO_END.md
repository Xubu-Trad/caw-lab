# R1 (58bZfQ1) — end-to-end narrative

## Goal
Explain the first riddle with full canon identifiers, full hashes, full URLs, and exact receipt-backed boundaries.

## Public anchors
- R1 transaction ID: `0xfbbcf5338b4a9c35073ac7253afc1a8ee81770d8d3285b80497bbd9c2186ed5b`
- Public short code: `58bZfQ1`
- Public image URL: `https://ibb.co/58bZfQ1`
- Historical IPFS CIDv0 handoff: `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV`
- DeepSound password: `enkidu`

## Canon chain
1. **On-chain anchor**
   - The first-riddle trailhead is the self-message transaction `0xfbbcf5338b4a9c35073ac7253afc1a8ee81770d8d3285b80497bbd9c2186ed5b`.
   - The promoted public short code is `58bZfQ1`.
   - The promoted public image URL is `https://ibb.co/58bZfQ1`.

2. **Image entrypoint**
   - The historical URL `https://ibb.co/58bZfQ1` identifies the Yale / OldKing / first-clue tablet image family; the replay pins the preserved image bytes.
   - That image is the public artifact from which the poem, coordinate, mirror, and downstream handoff material are historically derived.

3. **Poem / coordinate layer**
   - The canonical tablet independently reproduces the 46 coordinates and literal poem. The successful book recipe uses no fallback; older fallback attempts remain historical evidence.
   - Promoted receipt hashes from the determinism packet:
     - `H00243__full_coords.txt` -> `476f7fb5ccffd86fdf306c8a627feeacf8f087afcc22e3ad4b23fa76055c78ea`
     - `H00030__cids.txt` -> `0973232b8f8db5b2a7883a0d353ead07eb855eea4f496b99785fc08286ba0892`

4. **Book-cipher stage**
   - The target historical CID preserved across receipts is `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV`.
   - The exact public OCR edition and deterministic recipe now reproduce this CID. See [book-cipher replay](../layers/R1-020_book_cipher_gilgamesh/REPRODUCE.md).

5. **IPFS / APE stage**
   - The canonical uploaded APE receipt is:
     - filename: `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV.ape`
     - bytes: `8968236`
     - sha256: `57674107710cdac58fe68b30cb3c05e3334ece55bc0d71deba84ccd2a8fb3575`
     - ipfs-only-hash CID: `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV`
   - The non-canonical stripped / zip-copy family preserved in receipts is:
     - filename: `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV.ape.NONCANON_zipcopy`
     - bytes: `8968098`
     - sha256: `ea7c96accf476e389aade152efca89bdb92c4c4852e257cb6fe4da8e05b1d263`
     - ipfs-only-hash CID: `QmYRZiiGvVqbQgzuCLPWzWyZvrpWSh2VN7pCNDm91Lvt1M`
   - The currently preserved exact sweep match for the canonical CID is:
     - chunker=`size-262144`
     - raw_leaves=`false`
     - trickle=`false`
     - wrap=`false`
     - cid=`QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV`

6. **DeepSound / Enkidu stage**
   - The canonical APE now independently yields the exact Enkidu file. Normal-quality LSB decoding exposes `DSCF`; the padded `enkidu` key matches its SHA-1 verifier; AES-256-ECB yields `DSSF`, the filename, declared size and complete payload. [Exact replay](../layers/R1-040_deepsound_enkidu/REPRODUCE.md#canonical-ape-to-enkidu-2026-09-05).
   - The promoted pseudo-hex Enkidu artifact is preserved in full as `layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.full_pseudohex.txt`.
   - This is the full preserved pseudo-hex body, not just a prefix excerpt.
   - The exact uploaded pseudo-hex receipt hash is:
     - bytes: `21192`
     - sha256: `4f4edfdece802b300aeab48932b115d83eb04575753bfd128a3cc47c5cc25b19`
   - Its exact leading prefix is:
     - `41204W616V69666573746U206U6V206120446563656V7472616X697Z656420536U6369616X20436X656172696V6720486U757365202V2V2V28414Y412920434157`
   - The public decoding helper family preserved in uploaded receipts applies the mapping:
     - `U -> f`
     - `V -> e`
     - `W -> d`
     - `X -> c`
     - `Y -> b`
     - `Z -> a`

7. **Final manifesto stage**
   - The uploaded normalized stage-2 clean manifesto receipt is:
     - bytes: `10596`
     - sha256: `2ce02dffb32577a38ad646be06cb705782b0c4344271ed528aa252c08bca8944`
   - The promoted public-canon manifesto receipts are:
     - `manifesto.recovered.txt` -> `e5816ee2a75a1c939543773983f8b6d2b9eb05afee8d4f9ac91336e8ab6c01fa`
     - `manifesto.en.txt` -> `836c98641fd1222156d49c68d210d9860319b323f890b5af82860ac14aba366c`

## Remaining custody and completion questions
- The book cipher reproduces the CID, and preserved canonical APE bytes reproduce Enkidu. Fresh live retrieval of those exact audio bytes through that CID remains a separate check.
- Artifact replay does not authenticate historical authorship or prove that the manifesto is a terminal answer.
- The audio extraction gap is closed; historical source custody and a new downstream layer are separate questions.

## Layer map
- `layers/R1-000_yale_oldking/`
- `layers/R1-010_friderici_poem_coords/`
- `layers/R1-020_book_cipher_gilgamesh/`
- `layers/R1-030_ipfs_ape_audio/`
- `layers/R1-040_deepsound_enkidu/`
- `layers/R1-050_manifesto_final_payload/`

- The promoted pseudo-hex Enkidu artifact is preserved in full as `layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.full_pseudohex.txt`.
- The full body is also surfaced directly in `layers/R1-040_deepsound_enkidu/HEX_FULL.md`.

## Reproduced text step (2026-09-05)
`python3 scripts/reproduce_enkidu.py` reproduces the committed `manifesto.en.txt` exactly by the mapping above, hex decoding, and replacing 60 tabs with single spaces. See `layers/R1-040_deepsound_enkidu/REPRODUCE.md` for intermediate hashes and limits. The separate audio replay now closes APE-to-Enkidu extraction. These checks do not establish live IPFS custody or a terminal riddle solve.

## Reproduced image step (2026-09-05)
`python3 scripts/reproduce_tablet.py` independently recovers the 46 coordinate pairs from RGB low bits and the known poem from the IEND CRC insertion. Both match the existing normalized receipts. See [the tablet replay](../layers/R1-010_friderici_poem_coords/REPRODUCE.md). The image-to-text, public corpus-to-CID and canonical APE-to-Enkidu steps now reproduce. Live IPFS retrieval remains separate.

## Reproduced audio step (2026-09-05)

`python3 scripts/reproduce_ape_to_enkidu.py canonical.ape canonical.wav` verifies the original APE and decoded PCM hashes, then extracts the complete Enkidu file. The output hash matches the pseudohex above. The 32-byte file header, 21,192-byte payload and 8-byte footer occupy exactly 21,232 ciphertext bytes; no unaccounted AES padding or second framed file was found in the bounded check. [Extraction receipt](../layers/R1-040_deepsound_enkidu/EVIDENCE/ape_to_enkidu_replay.json).
