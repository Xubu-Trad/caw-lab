# R1-040 details

## Role in the chain
This layer preserves the exact Enkidu-stage handoff between the APE / DeepSound branch and the final manifesto branch.

## Exact canon constants
- DeepSound password: `enkidu`
- full pseudo-hex file: `EVIDENCE/enkidu.full_pseudohex.txt`
- `enkidu.full_pseudohex.txt` bytes: `21192`
- `enkidu.full_pseudohex.txt` sha256: `4f4edfdece802b300aeab48932b115d83eb04575753bfd128a3cc47c5cc25b19`
- `enkidu.stage0.txt` bytes: `10596`
- `enkidu.stage0.txt` sha256: `ef7d07f8ca22cddf5b791a0fdfc85b2dfdd71b8284b18f5f030a4cc678a974e4`

## Full pseudo-hex receipt
The full preserved pseudo-hex body is now surfaced directly in this layer in:
- `HEX_FULL.md`
- `EVIDENCE/enkidu.full_pseudohex.txt`

## What this layer proves
- the riddle passes through an Enkidu-stage pseudo-hex text lane
- the exact preserved pseudo-hex body is now directly carried in this layer
- the more legible stage text is preserved beside it as `enkidu.stage0.txt`

## What this layer still does not prove
- Historical custody and a fresh CID-to-audio network retrieval are separate from byte-level reproduction.
- The terminal answer or absence of another layer is not established.

The [public replay](REPRODUCE.md) now independently extracts Enkidu from the canonical APE, then converts the pseudohex to the exact normalized manifesto.

## Evidence in this layer
- `EVIDENCE/enkidu.full_pseudohex.txt`
- `EVIDENCE/enkidu.stage0.txt`

## Reader handoff
Continue to `../R1-050_manifesto_final_payload/DETAILS.md`.
