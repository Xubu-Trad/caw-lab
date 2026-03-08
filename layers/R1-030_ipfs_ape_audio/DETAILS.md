# R1-030 details

## Role in the chain
This layer turns the book-cipher CID handoff into a concrete audio-payload claim.

## What this layer proves
- the target CID is tied to a real APE-family artifact preserved in receipts
- local verification receipts identify a valid Monkey's Audio stream
- multiple preserved stripped copies exist, and at least two binary variants are documented
- the APE stage is not speculative; it is receipt-backed

## Stable receipt facts
- `EVIDENCE/ffprobe_ape.txt` identifies an APE stream with:
  - duration `00:02:15.23`
  - sample rate `48000 Hz`
  - stereo channels
  - codec `ape`
- `EVIDENCE/ape_checks.txt` preserves archived stripped-copy checks
- `EVIDENCE/ape_stripped_paths.txt` preserves the archived-copy family in sanitized logical form

## Recorded stripped-copy variants
- Variant A:
  - bytes `8968236`
  - sha256 `57674107710cdac58fe68b30cb3c05e3334ece55bc0d71deba84ccd2a8fb3575`
- Variant B:
  - bytes `8968098`
  - sha256 `ea7c96accf476e389aade152efca89bdb92c4c4852e257cb6fe4da8e05b1d263`

## What is not yet claimed
Public canon does **not** currently claim that the public repo alone can fetch or rebuild the exact APE blob from scratch with one bounded command. The repo preserves text-only verification of the stage, not the binary payload itself.

## Evidence in this layer
- `EVIDENCE/ffprobe_ape.txt`
- `EVIDENCE/ape_checks.txt`
- `EVIDENCE/ape_stripped_paths.txt`

## Reader handoff
Continue to `../R1-040_deepsound_enkidu/DETAILS.md`.
## Cross-reference
See `../../docs/R1_DETERMINISM_STATUS.md` for the current public determinism gap summary.

