# CAW riddle research

A public reference for reproducible CAW riddle steps, evidence, and clearly stated limits. Start here; use the linked receipts when checking a claim.

## Current state

| Riddle | Reproduced step / current limit | Read next |
| --- | --- | --- |
| R1 — 58bZfQ1 | The preserved Enkidu pseudohex converts exactly to the English manifesto. The full image → book cipher → CID → audio extraction chain remains incomplete. | [R1 status](docs/R1_DETERMINISM_STATUS.md) |
| R2 — zrUfKaKV | Unsolved. Existing anchors and historical receipts do not establish a final decoded answer. | [R2 status](docs/R2_zrUfKaKV_STATUS.md) |

## Find the evidence

- **Understand the sequence:** [Riddle progress](docs/RIDDLE_PROGRESS.md) → [layer index](LAYER_INDEX.md).
- **Reproduce the verified text step:** [Enkidu instructions and hashes](layers/R1-040_deepsound_enkidu/REPRODUCE.md).
- **Trace R1:** [end-to-end narrative and remaining gaps](docs/R1_58bZfQ1_END_TO_END.md).
- **Check provenance claims:** [on-chain receipts](docs/ONCHAIN_TRACE.md) and [what the facts do and do not prove](docs/WHAT_THE_FACTS_PROVE.md).
- **Find a layer's inputs:** open its `SUMMARY.md`, `REPRODUCE.md`, and `EVIDENCE/` folder from the layer index.

A preserved receipt is not automatically a solved layer. Treat only exact, independently checkable transformations as reproduced. Historical reports and unresolved status notes retain their limitations.

## Verify or contribute

Run `python3 scripts/reproduce_enkidu.py` for the bounded text replay. Run `bash scripts/check_canon.sh`, `bash scripts/audit_completeness.sh`, and `bash scripts/opsec_scan.sh` for repository checks; inspect any privacy-scan findings.

For a proposed solved step, provide exact inputs, commands, output hashes and limits. Follow [the layer template](layers/TEMPLATE/), update the repository manifest, and submit a pull request to `canon`. Keep private correspondence, credentials, personal paths and unsupported identity claims out of public evidence.

## Project background

[Original mission, community acknowledgements and project policies](docs/PROJECT_BACKGROUND.md) · [Hunters](docs/HUNTERS.md) · [Security](SECURITY.md) · [License](LICENSE).
