# R2: the message behind the hex

**2,884 characters. 273 words. A decode anyone can check.**

*XUBU research · 5 September 2026*

The hex at `zrUfKaKV` now resolves into a complete English message. It opens with “the lp was relocked.” It goes on to describe community development, a GitHub project, peer review and contracts that leave their deployers without special privileges. The full wording is preserved, including its errors. [Read the recovered message](https://github.com/Xubu-Trad/caw-lab/blob/canon/layers/R2-020_hex_transposition/MESSAGE.md).

This is a reproducible decode of the entire supplied ciphertext. Whether the message conceals another instruction remains open. Those are two different claims, and the evidence supports only the first so far.

## The source was already in the record

A fresh request to the [public Pastebin](https://pastebin.com/raw/zrUfKaKV) on 5 September returned 2,884 hex characters. They match the complete ciphertext embedded in the preserved `riddle medium.txt`, at line 10,748. The saved article therefore already contains every character needed for this result. Its earlier interpretation can be questioned without losing its underlying evidence.

The exact source fingerprint is:

```text
18f043170bc47a7d3aa9ee6989fe964803d240c90d62717b7fb7ad16539acd76
```

That SHA-256 fingerprint identifies the bytes. It does not prove who wrote them, when every historical copy was captured, or whether the message's factual claims are true. The [preserved input and source receipt](https://github.com/Xubu-Trad/caw-lab/tree/canon/layers/R2-020_hex_transposition/EVIDENCE) let another researcher start from the same material.

## How the message was found

Reading pairs of hex characters normally produces 1,442 largely unintelligible bytes. The useful change was to investigate the order of the hex digits themselves. A digit carries half a byte; the two halves did not need to have remained paired correctly.

The discovery search first held each byte's high half in place and shifted the low halves around the full 1,442-position circle. It tested every shift in both forward and reversed order: **2,884 candidates**. A simple score, trained on an already preserved R1 manifesto variant, ranked a forward shift of **320** first. That intermediate output was still unreadable.

The second search tested **612 invertible byte strides and 128 rectangular reorderings** of that candidate. Stride **641** produced the complete paragraph sequence. The combined operation then simplified to one exact permutation of the original 2,884 hex characters. The historical search settings and results are retained; the final decoder does not need a language model, a password or the target paragraph to operate.

For a nontechnical reader: imagine numbered slots around a circle. Starting at slot 4, place each successive source digit nine slots farther around, wrapping at the end. Read the completed slots as ordinary hex. Every slot is filled once. The technical form and the declared starting position are below.

## The exact rule

Call the original hex string `C`, with positions numbered from zero. Construct a second hex string:

```text
P[j] = C[(641 × j) mod 2884]
```

Decode `P` as hex. It starts with `e lp was relocked.` and ends with `gl anons. th`. Moving those last two bytes, `th`, to the front gives the natural reading copy. This boundary is chosen from the sentence structure and is disclosed. No words, spelling, punctuation or whitespace are repaired.

The reading copy can also be produced directly:

```text
R[j] = C[(320 + 641 × j) mod 2884]
```

The arithmetic explains the nine-slot rule: `9 × 641 = 2 × 2884 + 1`. Applying the inverse to the reading copy restores the source exactly:

```text
C[j] = R[(4 + 9 × j) mod 2884]
```

Here `R` is the reading copy expressed as hex. Both forms of the output are preserved in the [reproduction guide](https://github.com/Xubu-Trad/caw-lab/blob/canon/layers/R2-020_hex_transposition/REPRODUCE.md).

## What was independently checked

A separate implementation placed source digits into destination slots instead of copying digits out by stride 641. It produced the same 1,442 bytes. A fresh download reproduced the same fingerprints. An accompanying map traces every output character back to its two source hex positions.

The check also ranked **all 1,224 invertible hex strides in both digit-pairing parities**: 2,448 classes after grouping equivalent circular byte rotations. The recovered ordering ranked first under both the earlier manifesto model and a second model built from unrelated Python documentation. The second model had no CAW text in its training material. These scores support the result; they are not probabilities of truth.

A reversible permutation alone would prove very little: even leaving the original gibberish unchanged is reversible. The stronger evidence is the combination of a simple complete rule, coherent text throughout, every source character accounted for, exact inverse checks and a separately implemented replay. These are independent computational checks within this research session. External peer review is still welcome. [Run the independent audit](https://github.com/Xubu-Trad/caw-lab/blob/canon/scripts/verify_r2_independent.py).

## What the message says—and what it cannot prove

Its instruction is practical: put up a GitHub, develop against the manifesto, review the work together and remove lasting developer privileges. It expressly returns to the manifesto. Calling the manifesto a discarded decoy would go beyond these words.

The passage also asserts that liquidity was relocked and that there is no financial incentive. Decoding those assertions does not verify a lock, a contract, an author's identity or anyone's motives. Those questions require their own evidence.

No explicit next URL, password or ciphertext appears in the recovered text. That makes this a complete recovery of the supplied message, without establishing that its author intended it to be the last puzzle.

## Revisiting the unusual wording

The capitalization, spacing, line endings and misspellings were preserved for further checks. R2's uppercase letters read `TITITOCAW`. Initial-letter and final-letter streams did not yield a verified instruction. Its spaces include seven double runs and one triple run, so a simple single-space/double-space binary rule does not fit the complete input without an additional justified rule.

The original audio-derived R1 manifesto was checked before its 60 tabs were normalized to spaces. All 60 tabs are leading indentation. All 2,327 alphabetic symbols in the preceding pseudohex use uppercase `U–Z`; there is no mixed-case choice in that source to extract as bits.

One older typo claim fails a direct source check. The proposed `YALE AND ME` extraction requires an N from `moonning`. The authenticated manifesto contains `mooning`, correctly spelled. That exact recipe has no source for its N. This rules out that recipe on these bytes; it does not rule out every possible use of the real errors.

The saved article's UTF-16-to-UTF-8 conversion can also be reproduced mechanically. Its translated poem is not established by that conversion or its hash. A later candidate beginning `787e2963` is a different, odd-length string. Neither should be substituted for the authenticated R2 input.

No further cipher was verified in this pass. The full exploratory outputs and failed approaches remain in the private research record so another researcher can see exactly what was tried.

## How new is this?

Eight distinctive phrases from the recovered message had no matches in the previously indexed 13,003 Telegram and research records, after case and whitespace normalization. Fresh public searches also returned no matching publication of this plaintext in the results checked; the [search log](https://github.com/Xubu-Trad/caw-lab/blob/canon/layers/R2-020_hex_transposition/EVIDENCE/audit_2026-09-05/public_search_log.json) records the scope. Other historical [claims of an R2 “solve”](https://note.com/yamasan666/n/n4dbe7f011887) exist; that alone does not establish the same byte-level result.

The defensible statement is **newly recovered in this research record**. A claim that nobody has ever published it anywhere would require evidence this search cannot provide.

## Where the riddles stand

| Question | Evidence-based answer |
| --- | --- |
| Is this the full content of the supplied R2 hex? | **Yes.** All 2,884 digits become 1,442 bytes: 273 whitespace-delimited words. Nothing is discarded. |
| Is R2's hex cipher solved? | **Yes, for the authenticated current payload.** The exact transformation and inverse reproduce. |
| Is the whole R2 trail definitively finished? | **Not established.** No further layer has been verified, and there is no authenticated completion signal. |
| Is R1 completely solved? | **Not established.** The preserved tablet/book-cipher and audio-to-manifesto steps reproduce; live CID-to-audio custody and any further layer remain open. |

The next useful advance needs an actual extraction rule or a primary clue that constrains one. A word that can be made to appear after choosing corrections, rearrangements or anagrams is a lead to test, not a finished layer.

## Proof desk

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Exact source hex | 2,884 | `18f043170bc47a7d3aa9ee6989fe964803d240c90d62717b7fb7ad16539acd76` |
| Decoded text before reading rotation | 1,442 | `f8aeadf1d0f7933a5ae87ccc22ca4d0ad41ee038da85f785bb7a15feb7f8a12f` |
| Reading copy, final `th` moved to front | 1,442 | `2a77d034354b3ee698dd0266f93dfd5627e033cb8f79ec891498b80b7eab0e52` |

From the public repository, run:

```sh
python3 scripts/verify_r2_independent.py layers/R2-020_hex_transposition/EVIDENCE/zrUfKaKV.hex --out-dir replay-independent --rank
```

This uses Python's standard library. It writes the exact text, the complete character map and a verification receipt. The optional ranking uses the installed Python documentation, whose fingerprint is recorded because versions can differ.

[Full message](https://github.com/Xubu-Trad/caw-lab/blob/canon/layers/R2-020_hex_transposition/MESSAGE.md) · [Original decoder](https://github.com/Xubu-Trad/caw-lab/blob/canon/scripts/reproduce_r2_transposition.py) · [Audit evidence](https://github.com/Xubu-Trad/caw-lab/tree/canon/layers/R2-020_hex_transposition/EVIDENCE/audit_2026-09-05) · [R1 replay](https://github.com/Xubu-Trad/caw-lab/blob/canon/layers/R1-040_deepsound_enkidu/REPRODUCE.md)
