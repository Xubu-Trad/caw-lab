# Reproduce the Enkidu text transformation

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

This reproduces only the preserved pseudohex-to-English step. It does not independently extract Enkidu from the APE, derive the IPFS CID from the book cipher, authenticate the original extraction, prove the manifesto is the riddle's terminal answer, or solve R2. The stored stage0 and manifesto.recovered variants are not silently rewritten.
