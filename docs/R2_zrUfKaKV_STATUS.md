# R2 (zrUfKaKV) — status and triage narrative

## Goal
State the second-riddle chain with full canon identifiers, full tx IDs, full hashes, full numeric anchors, and full public references where they are actually promoted.

## Public anchors
- R2 transaction ID: `0xcae4b15350b3ccc2b37fec5caa718560241ec181bc49741d5d1199d1d32412d4`
- Public short code: `zrUfKaKV`
- Historical tooling mentioned `yhcajZq0`; its relationship to R2 is unverified. The on-chain marker is `zrUfKaKV`.

## Current public canon
Public canon does not claim a complete end-to-end R2 solve. It preserves the anchor, the status/checksum packs, and the strongest recovered-payload triage receipts.

## Strongest preserved observations
1. Three text-origin inputs were preserved in decoded-file receipts:
   - `INPUT/cleaned_hex_ready.txt`
   - `INPUT/revised_output_hex.txt`
   - `INPUT/manifesto_replicate_output_4.3_AUDIO_HEX.txt`

2. Their exact decoded-file receipt facts are:
   - `INPUT/cleaned_hex_ready.txt`
     - bytes: `3129`
     - sha256: `158e412566e1b318b86de33e19aba3fe714d6a0adabbbd13585d75fde1994701`
     - head hex: `ffd8ffe000104a464946000101000001`
     - type: `jpeg`
   - `INPUT/revised_output_hex.txt`
     - bytes: `3251`
     - sha256: `67588723e6398a7e920f3a0f4ad05ea4d565960fe1921b0827fa0314c2497fdb`
     - head hex: `ffd8ffe000104a464946000101000001`
     - type: `jpeg`
   - `INPUT/manifesto_replicate_output_4.3_AUDIO_HEX.txt`
     - bytes: `3251`
     - sha256: `44f8e88920f1646cc9c9ac399aac5f62e62afc5c625ab5f684a0eef0684ae3c7`
     - head hex: `ffd8ffe000104a464946000101000001`
     - type: `jpeg`

3. The strongest repeated structural signal is the shared trailer family:
   - `cleaned_hex_ready.jpg`
     - bytes: `3129`
     - eoi_offset: `1354`
     - trailer_bytes: `1773`
     - head_sha256: `1c177ef0d80173583038459325e918279ef61ff165924dac25455a629508f359`
     - trailer_sha256: `b469e9872446c65a7d0a0b93f425e8df5720e59f01b2d946f433b3e1a4ef28ab`
   - `revised_output_hex.jpg`
     - bytes: `3251`
     - eoi_offset: `1476`
     - trailer_bytes: `1773`
     - head_sha256: `b8920a338a2e9015a7ea96579c2e6fcb9238ff1ae2a1638d0531661ace8c737f`
     - trailer_sha256: `b469e9872446c65a7d0a0b93f425e8df5720e59f01b2d946f433b3e1a4ef28ab`
   - `manifesto_replicate_output_4.3_AUDIO_HEX.jpg`
     - bytes: `3251`
     - eoi_offset: `-1`
     - trailer_bytes: `0`
     - head_sha256: `44f8e88920f1646cc9c9ac399aac5f62e62afc5c625ab5f684a0eef0684ae3c7`

4. The preserved numeric anchor family is:
   - `21000000`
   - `10500000`
   - `5250000`
   - `2625000`
   - `1312500`
   - `120`
   - `21000000:10500000:5250000:2625000:1312500`
   - `21000000-10500000-5250000-2625000-1312500`

## What public canon now says clearly
- the exact R2 starting point
- the exact recovered payload candidates
- the exact repeated trailer hash that currently matters most
- the exact numeric anchors that must be preserved for replay work

## What public canon still does not claim
- no finished end-to-end plaintext
- no final container identity for the shared trailer family
- no single fully deterministic replay from `zrUfKaKV` to final solved payload
