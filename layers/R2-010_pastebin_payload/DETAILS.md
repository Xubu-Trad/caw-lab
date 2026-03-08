# R2-010 details

## Role in the chain
This layer records the recovered-payload triage for the second riddle.

## Strongest preserved observations
- `decoded_files.tsv` preserves three decoded text-origin inputs that emitted JPEG-like outputs.
- `cleaned_hex_ready` preserved as a 3129-byte JPEG-like file.
- `revised_output_hex` preserved as a 3251-byte JPEG-like file.
- `manifesto_replicate_output_4.3_AUDIO_HEX` preserved as a 3251-byte JPEG-like file, but without a valid EOI in the current trailer receipt.
- `cleaned_hex_ready` and `revised_output_hex` share the same 1773-byte trailer family.
- the shared trailer sha256 preserved in public receipts is:
  `b469e9872446c65a7d0a0b93f425e8df5720e59f01b2d946f433b3e1a4ef28ab`
- numeric anchors preserved in this layer are:
  `21000000`, `10500000`, `5250000`, `2625000`, `1312500`, `120`

## Why this matters
The repeated trailer family is the strongest current structural signal in public R2 payload work. It is stronger than a one-off malformed output because it repeats across two independently preserved JPEG-like results.

## Evidence in this layer
- `EVIDENCE/decoded_files.tsv`
- `EVIDENCE/jpeg_report.tsv`
- `EVIDENCE/trailer_report.tsv`
- `EVIDENCE/r2_numeric_anchors.txt`

## What this layer proves
- recovered payload triage produced stable text receipts
- two outputs converge on the same trailer family
- numeric anchors were preserved separately from the JPEG receipts
- public canon can now describe the strongest current R2 lane without pretending the riddle is solved

## What this layer does NOT prove
- the final meaning of the shared trailer
- a final plaintext
- the exact winning decode chain from anchor to final output

## Best current public-next-step framing
Treat the shared-trailer pair as the primary public replay lane, and treat the malformed no-EOI output as a secondary comparative lane.

## Reader handoff
See `../../docs/R2_zrUfKaKV_STATUS.md`.
