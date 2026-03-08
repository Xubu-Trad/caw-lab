# R1-050 details

## Role in the chain
This is the final text-payload layer for R1. It records the preserved recovered manifesto text and the cleaner English-normalized form.

## Exact canon constants
- recovered text file: `EVIDENCE/manifesto.recovered.txt`
- recovered text bytes: `10596`
- recovered text sha256: `e5816ee2a75a1c939543773983f8b6d2b9eb05afee8d4f9ac91336e8ab6c01fa`
- English text file: `EVIDENCE/manifesto.en.txt`
- English text bytes: `10596`
- English text sha256: `836c98641fd1222156d49c68d210d9860319b323f890b5af82860ac14aba366c`

## Relationship to the Enkidu layer
The upstream Enkidu pseudo-hex body is preserved in:
- `../R1-040_deepsound_enkidu/EVIDENCE/enkidu.full_pseudohex.txt`
- `../R1-040_deepsound_enkidu/HEX_FULL.md`

This layer preserves the two text outputs currently promoted into public canon:
- the recovered text form
- the cleaner English-normalized text form

## What this layer proves
- the final promoted payload family is the manifesto
- both preserved downstream text forms are explicitly tied back to the full Enkidu pseudo-hex layer
- public canon distinguishes preserved text receipts from a not-yet-fully-bounded public replay

## Evidence in this layer
- `EVIDENCE/manifesto.recovered.txt`
- `EVIDENCE/manifesto.en.txt`

## Reader handoff
See `../../docs/R1_58bZfQ1_END_TO_END.md` and `../../docs/R1_DETERMINISM_STATUS.md`.
