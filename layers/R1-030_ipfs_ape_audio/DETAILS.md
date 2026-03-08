# R1-030 details

## Scope
This layer covers the CID-to-payload stage: the point where the R1 book-cipher handoff yields an IPFS payload associated with Monkey's Audio artifacts.

## Proven receipts
- Canon now includes the ffprobe receipt for the APE stage.
- Canon now includes APE-check receipts.
- Canon now includes stripped-path receipt text for the APE lane.
- Private working notes identify this stage as the IPFS payload handoff and recommend making one canonical payload decision among the `.ape`, `.zip`, and related derived artifacts.

## Why this layer matters
This is the first hard file-format confirmation after the book-cipher lane.
A good public reader should learn here:
- what payload family the CID led to
- what format evidence was observed
- which artifact is being treated as primary vs derived
- what uncertainties remain around derived copies or repackaged payloads

## Evidence in this layer
- `EVIDENCE/ffprobe_ape.txt`
- `EVIDENCE/ape_checks.txt`
- `EVIDENCE/ape_stripped_paths.txt`
- `EVIDENCE/README.md`

## Boundaries
This layer does not itself prove the DeepSound extraction. That belongs in R1-040.
