# R2 (zrUfKaKV) — status and triage narrative

## Goal
State the second-riddle chain clearly, using only what is presently preserved in public canon receipts.

## Public anchors
- R2 transaction: `0xcae4b15350b3ccc2b37fec5caa718560241ec181bc49741d5d1199d1d32412d4`
- Public short code: `zrUfKaKV`

## Current public canon
Public canon does not claim a complete end-to-end R2 solve. It preserves the on-chain anchor, checksum/status receipts, and the strongest recovered-payload triage observations.

## Strongest preserved observations
1. Three text-origin payload candidates were decoded into JPEG-like outputs and preserved in `decoded_files.tsv`.
2. Two outputs — `cleaned_hex_ready` and `revised_output_hex` — produced valid JPEG heads and ended with distinct EOI offsets, but shared the same 1773-byte trailer payload family.
3. The shared trailer family is preserved by the trailer report and is currently the strongest repeated structural signal in the public R2 payload lane.
4. A third output — `manifesto_replicate_output_4.3_AUDIO_HEX` — preserved as JPEG-like data but lacked a valid EOI in the current receipt set.
5. Numeric anchors are preserved as a separate receipt family:
   `21000000`, `10500000`, `5250000`, `2625000`, `1312500`, and `120`.

## What this means
R2 is currently best understood as an anchored payload-triage problem, not a solved plaintext problem. The public repo now tells a reader:
- where R2 starts
- which recovered payloads are strongest
- which repeated structures were actually observed
- which values are preserved for follow-on work

## What public canon still does not claim
- no final plaintext
- no final container identity for the shared trailer family
- no fully deterministic replay from on-chain anchor to solved payload

## Most useful next public-facing questions
1. What exact upstream decode steps produced each of the three JPEG-like outputs?
2. Is the shared 1773-byte trailer a real embedded payload, padding family, or transform artifact?
3. How do the numeric anchors map onto the strongest recovered lane?
4. Which lane should be treated as primary public replay work?

## Layer map
- `layers/R2-000_onchain_zrufkakv/`
- `layers/R2-010_pastebin_payload/`
