# R1-040 details

## Scope
This layer covers the DeepSound / Enkidu stage that follows the APE payload lane.

## Proven receipts
- Canon now includes `enkidu.stage0.txt`.
- Canon now includes `enkidu.txt`.
- Private working notes describe this stage as: DeepSound password `enkidu` -> `Enkidu.txt`.
- Those same notes describe `Enkidu.txt` as pseudo-hex / broken-hex style material that resolves only after the intended transform logic is applied.

## Why this layer matters
This is the transition from media/container work back into text/encoding work.
A reader should understand here:
- that DeepSound is part of the claimed R1 chain
- that the password handoff is `enkidu`
- that the resulting text is not plain English but an encoded intermediate artifact

## Evidence in this layer
- `EVIDENCE/enkidu.stage0.txt`
- `EVIDENCE/enkidu.txt`
- `EVIDENCE/README.md`

## Boundaries
This layer records the Enkidu-stage receipts. The manifesto recovery itself belongs in R1-050.
