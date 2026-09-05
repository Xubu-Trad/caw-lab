# R2 · the hex message now reproduces

**Verified on 2026-09-05:** the current public `zrUfKaKV` payload decodes through an exact step-9 hex transposition. [Read the message](../layers/R2-020_hex_transposition/MESSAGE.md) · [Replay every byte](../layers/R2-020_hex_transposition/REPRODUCE.md).

The source is 2,884 hex characters, SHA-256 `18f043170bc47a7d3aa9ee6989fe964803d240c90d62717b7fb7ad16539acd76`. Ordinary hex decoding yields the familiar 1,442-byte `a7f4839f…` candidate. Reordering the hex characters by stride 641 modulo 2884 produces coherent text. Moving the final two bytes to the front establishes the declared reading origin. Both forms re-encode exactly.

The text discusses the liquidity lock and building a decentralized CAW implementation without privileged developer control. These are the message's words, not an audit of any contract. The recovered text contains no explicit new URL, password or ciphertext. The full supplied cipher is solved, and the evidence favors this development message as its intended output. No further layer has been verified. [Endpoint assessment](ENDPOINT_ASSESSMENT.md).

## Provenance

- Historical on-chain trailhead: `0xcae4b15350b3ccc2b37fec5caa718560241ec181bc49741d5d1199d1d32412d4`, marker `zrUfKaKV`.
- [Current public Pastebin source](https://pastebin.com/raw/zrUfKaKV) returned HTTP 200; full source bytes match the preserved local candidate and saved page.
- `yhcajZq0` is a separate historical reference. Its connection to this payload is not established.

## Superseded research branches

Earlier JPEG-like files, repeated trailers, numeric anchors, XOR scans and syntactic zlib headers were candidate observations. They are not validated steps from the live input. The exact hex transposition supersedes their role as the main R2 route. Historical receipts are preserved so failed approaches remain auditable; none should be described as a recovered picture or audio layer without an independent parser and provenance chain.
