# Exact comparison with Ten's reported Wayback manifesto

## Result

FACT: the audio-derived manifesto is 10,596 bytes, SHA-256 `03fa37cfe06c7d06d590020e9fcf8c67b4131671c10d48a6f1ef0283df8cfb22`.

FACT: applying the three explicit formatting operations below produces 10,749 bytes and SHA-256 `5e03b441cc8dc10874f9ac956bf9c7c0574fc94e0387b3ef186661505044738b`, exactly the length and hash supplied by Ten for his Wayback copy.

1. Replace each of the 60 TAB bytes (09) with one SPACE byte (20). Byte count unchanged. `tab-positions.json` records every position in the decoded original.
2. Replace all 155 LF line endings (0A) with CRLF (0D 0A). Adds 155 bytes.
3. Remove the final CRLF. Removes 2 bytes. Result has 154 CRLF line separators and no final newline.

Arithmetic: 10,596 + 155 - 2 = 10,749. Reversing the line-ending changes gives exact byte equality with our tab-to-space version. No other transformation is used. The check includes a one-bit negative control.

## Meaning and the Enkidu claim

INFERENCE: these changes do not alter the manifesto's prose or requirements. Words, numbers, punctuation, misspellings and capitalization are identical. Tabs versus spaces can affect visual alignment, and exact whitespace could matter for a hypothetical formatting-based cipher; this comparison does not dismiss that separate possibility. Both byte forms are retained.

FACT: Ten's text is not byte-identical to the audio-derived original. Hexing and Atbash-encoding the 10,749-byte form produces 21,498 characters, rather than the extracted 21,192-byte Enkidu. Matching head and tail excerpts therefore does not prove full Enkidu equality. The formatting operations explain the difference without a wording disagreement. Converting line endings back and restoring the 60 recorded tabs recovers our exact original; the space-normalized copy alone does not identify those tab positions.

## Provenance boundary

The file `ten-reported-hash-reconstruction.txt` was generated locally from freshly extracted Enkidu bytes. It is NOT labeled as an independently retrieved Wayback download. Its SHA-256 matches the value Ten supplied in the conversation; this is strong byte-identity evidence relative to that reported digest. Ten should confirm that digest directly on his retained file, or run the comparison against it. The match does not authenticate an archive timestamp, historical custody, authorship or terminal riddle completion. No Wayback capture URL/date has been independently established by this comparison.

## Reproduce

From the package root: `python3 scripts/compare_ten_manifesto.py`.
Ten can additionally compare his own retained file directly with `comparison/ten-reported-hash-reconstruction.txt`, without opening/resaving either in an editor that changes line endings.
