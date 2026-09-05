# R1 determinism status

The tablet clues, book cipher, audio extraction and Enkidu text conversion reproduce against pinned inputs. Fresh byte-verified retrieval of the audio through the historical IPFS CID remains separate. These results do not establish a terminal riddle answer.

## Stable artifact constants
- R1 transaction ID: `0xfbbcf5338b4a9c35073ac7253afc1a8ee81770d8d3285b80497bbd9c2186ed5b`
- Public short code: `58bZfQ1`
- Public image URL: `https://ibb.co/58bZfQ1`
- Historical target CID: `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV`
- Canonical uploaded APE sha256: `57674107710cdac58fe68b30cb3c05e3334ece55bc0d71deba84ccd2a8fb3575`
- Non-canonical stripped / zip-copy sha256: `ea7c96accf476e389aade152efca89bdb92c4c4852e257cb6fe4da8e05b1d263`
- Enkidu pseudo-hex sha256: `4f4edfdece802b300aeab48932b115d83eb04575753bfd128a3cc47c5cc25b19`
- Manifesto recovered sha256: `e5816ee2a75a1c939543773983f8b6d2b9eb05afee8d4f9ac91336e8ab6c01fa`
- Manifesto English sha256: `836c98641fd1222156d49c68d210d9860319b323f890b5af82860ac14aba366c`


The recovered/English manifesto hashes identify separate preserved variants. The reproducible text conversion produces the English hash `836c9864…`.

## Reproduced steps

| Step | Result | Replay |
| --- | --- | --- |
| Tablet | Exact 46 coordinates and literal poem | [Image extraction](../layers/R1-010_friderici_poem_coords/REPRODUCE.md) |
| Book cipher | Exact historical CID from the pinned OCR edition; no fallback | [Corpus selection](../layers/R1-020_book_cipher_gilgamesh/REPRODUCE.md) |
| Canonical APE | Exact 21,192-byte Enkidu pseudohex; password verifier, declared length and footer checked | [Audio extraction](../layers/R1-040_deepsound_enkidu/REPRODUCE.md#canonical-ape-to-enkidu-2026-09-05) |
| Enkidu text | Translate `UVWXYZ` to `fedcba`, hex-decode, replace exactly 60 tabs with single spaces | [Text conversion](../layers/R1-040_deepsound_enkidu/REPRODUCE.md#enkidu-text-to-manifesto) |

The audio replay uses normal-quality DeepSound LSB decoding and AES-256-ECB with ASCII `enkidu` zero-padded to 32 bytes. It reads the file length from the decrypted header before checking the expected output. [Machine-readable receipt](../layers/R1-040_deepsound_enkidu/EVIDENCE/ape_to_enkidu_replay.json).

## Remaining boundary

The independent APE-to-Enkidu extraction gap is closed. This run used preserved APE bytes with the recorded canonical hash; it did not establish fresh live IPFS retrieval or the historical chain of custody. Historical CID hashing receipts remain evidence of their own checks.

The replay verifies transformations between artifacts. It does not establish who authored them, authenticate every historical claim, or prove that no further layer exists. Follow [current riddle progress](RIDDLE_PROGRESS.md) for work beyond these reproduced R1 stages.
