# R2-000 details

## Role in the chain
This is the public entrypoint and status layer for R2.

## Public anchors
- R2 tx: `0xcae4b15350b3ccc2b37fec5caa718560241ec181bc49741d5d1199d1d32412d4`
- Public short code: `zrUfKaKV`

## What this layer proves
- there is a stable public anchor for the second riddle
- public canon preserves the current status note and checksum receipts
- public canon explicitly treats R2 as incomplete

## Evidence in this layer
- `EVIDENCE/R2_zrUfKaKV_STATUS.md`
- `EVIDENCE/L01_README.md`
- `EVIDENCE/L01_SHA256SUMS.txt`
- `EVIDENCE/L02_SHA256SUMS.txt`

## What the checksum packs mean in plain English
- `L01` preserves an earlier grouped series of R2 lane receipts
- `L02` preserves a later grouped set of R2 merge / receipt artifacts
- together they act as provenance and integrity anchors for the current public R2 state

## What this layer does NOT prove
- no final decoded plaintext
- no completed end-to-end replay
- no single canonical winning lane yet

## Reader handoff
Continue to `../R2-010_pastebin_payload/DETAILS.md` and `../../docs/R2_zrUfKaKV_STATUS.md`.
