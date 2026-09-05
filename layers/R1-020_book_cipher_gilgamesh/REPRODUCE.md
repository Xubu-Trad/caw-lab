# Reproduce the R1 book cipher

The 46 tablet coordinates reproduce the historical CID from one exact public OCR edition.

Download [eog_djvu.txt](https://archive.org/download/TheEpicofGilgamesh_201606/eog_djvu.txt) unchanged. Required SHA256: `b66cfab2ac8fa274638036caeb9e06518f03798c84661601c95abcfccf50e33f` (109,187 bytes).

From the repository root:

```sh
python3 scripts/reproduce_tablet.py
python3 scripts/reproduce_book_cipher.py /path/to/eog_djvu.txt
```

1. Decode UTF-8 and drop blank lines. Retain the source title/header; 1,196 nonempty lines remain.
2. Use each coordinate as a one-based line and one-based word index.
3. Split the line on whitespace. Strip non-ASCII-alphanumeric characters at token edges; discard empty tokens.
4. Emit the selected token's first character with its existing case. Convert number words zero through nine to their digit instead.

Every coordinate selects an in-range word. No fallback, line shift, case fitting, fabricated header or expected-answer character substitution is needed for this source.

Result: `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV`.

[Receipt and character trace](EVIDENCE/public_book_replay.json). The expected CID is checked only after selection. Another similarly titled OCR edition does not reproduce this output under the same recipe. Full source books are not redistributed here.

This reproduces a historically known step. It does not establish historical novelty, live IPFS availability, or independent APE-to-Enkidu extraction. Preserve older unsuccessful recipes as bounded negative results; this method adds punctuation handling and number-word conversion to the earlier initial-only checks.
