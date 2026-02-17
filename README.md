# CAW Lab (Public Canon)

This repository (**Xubu-Trad/caw-lab**) is the **public, evidence-first canon** for the CAW riddles: a reproducible chain of **verified layers** anchored to on-chain artifacts (transactions, contract state, logs) and deterministic cryptographic transforms.

**Canon rule:** if a claim cannot be reproduced deterministically from the referenced inputs, it does **not** belong on `canon`.

## Repos and Roles

### Public: `Xubu-Trad/caw-lab` (this repo)
**Canon only**
- Verified layers with explicit claims + receipts
- Deterministic reproduce steps (`REPRODUCE.md`)
- Evidence references (`EVIDENCE/`) with hashes / minimal receipts (no large binaries)
- Guardrails: manifest verification, no tracked binaries, opsec scans

### Private: `Xubu-Trad/caw-lab-private`
**Working lab**
- Failed attempts, false positives, exploratory tooling
- Raw imports and large artifacts
- Draft placeholders while a path is unverified
- Anything not yet confirmed/reproducible stays private

## How to Use This Repo

- Start at **LAYER_INDEX.md** (generated index of the canon layers).
- Each `layers/<LAYER>/` contains:
  - `SUMMARY.md` — what is proven, outputs, and anchor references
  - `REPRODUCE.md` — exact steps to reproduce
  - `EVIDENCE/` — receipts (hashes, text outputs, and “where it came from” notes)

## Local Integrity Checks (run before PR)

From repo root:

- `bash scripts/verify_manifest.sh`
- `bash scripts/sanitize_audit.sh`
- `python3 scripts/gen_layer_index.py --check`
- `bash scripts/audit_layers.sh`
