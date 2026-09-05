# R1-010 — replay the tablet

**Result:** the preserved public PNG independently yields the existing 46 coordinates and mirror/backwards poem. This closes the image-to-text receipt gap; the book-cipher step remains open.

```sh
python3 scripts/reproduce_tablet.py
```

Python 3 standard library only. The script checks the exact image hash, validates the 70 chunks before IEND, reverses PNG row filters, extracts the RGB low bits, and compares normalized outputs with the existing receipts.

## Exact input

[`docs/assets/r1-tablet.png`](../../docs/assets/r1-tablet.png) — 536397 bytes, SHA-256 `889253e7fa85f5e5fd05622b8a105fd61acf83bdfdae3e600bdfedd173b2da41`.

## Coordinates

Read pixels left to right, top to bottom. Take bit 0 from R, then G, then B; omit alpha. Pack each eight bits most-significant first. The prefix before the first NUL is 290 bytes containing 46 `line:word` pairs.

Raw coordinate SHA-256: `cd8b7360f4363064f6c0719d1658e859b546dc5d95a10aa026a68b268ed53998`.

To match the pre-existing [`full_coords.txt`](EVIDENCE/full_coords.txt), add a comma after every row except the last and a final newline. This formatting change is explicit; the coordinates are unchanged.

## Literal poem

The IEND chunk starts at zero-based offset 535563. Its expected CRC is `ae426082`, but the source contains `ae426035`: the first ASCII hex digit occupies the fourth CRC position.

Read the 818 ASCII bytes at offset 535574, ending immediately before the deferred `82` byte at offset 536392. Hex-decode them to 273 bytes of poem text. Raw poem SHA-256: `c1dfa2443b0a167034ae06ea67bcac44f1c3714d54a8c671d971b9613f5de19a`.

To match the existing [`poem.txt`](EVIDENCE/poem.txt), strip trailing spaces on each line and append a final newline. The original PNG remains unchanged. Reading only after the nominal IEND boundary drops the first hex digit.

## Limits

These are known clues, now reproducible from the image. Neither this result nor the Telegram discussion establishes a newly discovered layer. The fallback letter-count rule is a historical claim; the exact corpus, normalization and indexing that produce the CID still need reproduction.

[`tablet_replay.json`](EVIDENCE/tablet_replay.json) records the machine-checkable result. [PNG structure reference](https://www.w3.org/TR/png-3/) defines the chunk and CRC layout.
