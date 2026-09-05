# Independent R2 audit

`verification.json` and `character_map.csv` are a matched pair from the public standard-library scatter implementation. The CSV has LF line endings; every output byte names both zero-based input hex positions. Its SHA-256 is recorded in the receipt.

`fresh_source_receipt.json` records the second live download. `independent_receipt.json` also establishes that the complete supplied article hex matches it. `article_claim_checks.json` distinguishes a reproducible UTF-16 conversion from an unsupported translation. `discovery_search_summary.json` records how the ordering was first found.

Replay from the repository root:

```sh
python3 scripts/verify_r2_independent.py layers/R2-020_hex_transposition/EVIDENCE/zrUfKaKV.hex --out-dir replay-independent --rank
```

The rank is a heuristic check across affine stride/parity classes, with circular byte rotations grouped. It does not select the sentence boundary. Input/output hashes, complete coherence and the exact inverse are separate checks. The small decoder and the full outputs permit external review without trusting the narrative.

The historical article is preserved as a source, not silently corrected. No global-first discovery, author identity, contract claim or final end to the whole riddle is established here.
