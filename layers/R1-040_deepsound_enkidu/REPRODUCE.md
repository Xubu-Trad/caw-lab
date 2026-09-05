# Reproduce the audio extraction and Enkidu text

## Enkidu text to manifesto

Run from a checkout with the evidence bytes unchanged (disable automatic line-ending conversion):

```sh
python3 scripts/reproduce_enkidu.py
```

The script verifies the input hash, translates U,V,W,X,Y,Z to f,e,d,c,b,a respectively, hex-decodes, then replaces each tab byte (09) with one space byte (20). There is no byte reversal, word replacement or general whitespace collapse. Exactly 60 tabs are replaced.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| enkidu.full_pseudohex.txt | 21192 | 4f4edfdece802b300aeab48932b115d83eb04575753bfd128a3cc47c5cc25b19 |
| Decoded before tab normalization | 10596 | 03fa37cfe06c7d06d590020e9fcf8c67b4131671c10d48a6f1ef0283df8cfb22 |
| Normalized output, exact manifesto.en.txt | 10596 | 836c98641fd1222156d49c68d210d9860319b323f890b5af82860ac14aba366c |

Verified on 2026-09-05 against the committed input and target blobs. The transformation was derived by comparing the preserved artifacts, then checked over all bytes; it does not establish the historical solver's method. The older U=b / Y=f description does not reproduce this target.

This text conversion reproduces the preserved pseudohex-to-English step. The separate audio replay below now extracts the exact pseudohex from canonical APE bytes. Neither result proves historical authorship, live IPFS custody, or that the manifesto is a terminal answer. The stored stage0 and manifesto.recovered variants remain separate.

## Plain-hex corroboration

A separately supplied 21,192-byte plain-hex copy was checked on 2026-09-05 (SHA-256 `31344ddefad096833a41368212e22ba6bfda180fa4f273899038b289b4ad6c3c`). Direct hex decoding produces the exact intermediate hash above; replacing its 60 tabs produces the exact normalized output. It corroborates this preserved stage. It is a corroborating plain-hex copy. The audio replay below independently recovers the pseudohex input; this copy alone does not establish that extraction or a new layer.

## Canonical APE to Enkidu (2026-09-05)

The exact 8,968,236-byte APE now yields the committed 21,192-byte `enkidu.full_pseudohex.txt`. The extraction was reproduced from preserved audio bytes, without running DeepSound or consulting the expected plaintext to locate the file.

Requirements: FFmpeg, Python 3 and the Python `cryptography` package. Tested with FFmpeg 4.4.2 and `cryptography` 50.0.1. Given the pinned `canonical.ape`, run from the repository root:

```sh
ffmpeg -v error -nostdin -i canonical.ape -c:a pcm_s16le -n canonical.wav
python3 scripts/reproduce_ape_to_enkidu.py canonical.ape canonical.wav --output extracted-enkidu.txt
```

The script checks the APE and decoded PCM hashes, reads the DeepSound file header, takes the payload length from that header, decrypts only the bounded file, checks its footer, and compares the recovered SHA-256 with the preserved evidence. The output must be a new file.

| Step | Exact value |
| --- | --- |
| APE SHA-256 | `57674107710cdac58fe68b30cb3c05e3334ece55bc0d71deba84ccd2a8fb3575` |
| PCM | 48,000 Hz; stereo; signed 16-bit little-endian; 6,491,116 frames |
| PCM SHA-256 | `9a50dfecbbe8612b6470f804e6a752d2d98ad43c2daae126fd80fc4bf094086d` |
| One decoded LSB byte | `((pcm[4*i] & 15) << 4) | (pcm[4*i+2] & 15)` |
| Container | `DSCF`, mode 4, encrypted flag 1, starting at PCM byte 0 |
| Password/key | ASCII `enkidu`, zero-padded to 32 bytes |
| Password verifier | SHA-1 of that padded key: `13ac6a5c147142b32ece842d02453f46710c90b9` |
| Cipher | AES-256-ECB; ciphertext begins at decoded container byte 26 |
| Decrypted record | `DSSF`, zero-padded filename `enkidu.txt`, declared length 21,192 |
| Consumed ciphertext | 21,232 bytes: 32 header + 21,192 payload + 8 footer |
| Footer | `0000000044535346` |
| Output SHA-256 | `4f4edfdece802b300aeab48932b115d83eb04575753bfd128a3cc47c5cc25b19` |

[Exact extraction receipt](EVIDENCE/ape_to_enkidu_replay.json). [Bounded remainder check](EVIDENCE/ape_container_remainder.json). The filename and reserved fields contain the expected zero fill. The record ends on an AES block boundary with no unaccounted padding. A scan of the normal-quality LSB stream at four byte alignments finds one `DSCF`; full aligned ECB decryption finds only the opening and closing `DSSF` for this file. No additional framed file was found. Other possible audio encodings have not been exhausted.

The nibble ordering and header fields follow [Openwall's DeepSound parser](https://github.com/openwall/john/blob/bleeding-jumbo/run/deepsound2john.py). Its [dynamic format 1529](https://github.com/openwall/john/blob/bleeding-jumbo/run/dynamic.conf) specifies the zero-padded password verifier. The AES mode and exact record layout were derived from this artifact and validated over the complete extracted file. This is a strict replay for these bytes, not a general DeepSound format specification. [AES API reference](https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/).

This closes the canonical-audio-to-Enkidu extraction gap. Fresh retrieval of the same audio through the historical IPFS CID remains a separate custody check. The replay does not prove a new layer or that all riddles end at the manifesto.
