# caw-lab — reproducible riddle forensics for the cawmmunity

Mission: solve the CAW riddles as intended — fully reproducibly, with receipts anyone can verify.

This repo is **public canon**: layers, evidence, and exact reproduce steps. It is designed to reduce “leader” narratives: **process over personality**.

## Start here
- `LAYER_INDEX.md` (map of layers)
- `layers/R1-*/SUMMARY.md` (what we believe + what we do NOT claim)
- `layers/R1-*/REPRODUCE.md` (exact commands)
- `layers/R1-*/EVIDENCE/` (inputs, logs, hashes, receipts)

## Canon gates (enforced by CI)
- No tracked binary blobs
- Deterministic manifest: `MANIFEST.repo.sha256`
- No empty evidence files

## Verify locally
```bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C
bash scripts/check_canon.sh
bash scripts/audit_completeness.sh
bash scripts/opsec_scan.sh
```

## Scratchpad repo policy (IMPORTANT)
`caw-lab-private` is a **SCRATCHPAD ONLY** repo.
It may contain experiments, failed attempts, and unsanitized logs.

Nothing there is “canon.” Only sanitized, reproducible artifacts should be promoted into this public repo with hashes + reproduce steps.

## Deployer invite status (community reference)
Invitations are pending until accepted.

- PUBLIC repo invite → **@cawdevelopment** (permission: write)
  - created_at (UTC): `2026-02-08T06:29:46Z`
  - created_at (America/New_York): `Sunday, 2026-02-08 01:29:46 AM EST`

- PRIVATE scratchpad invite → **@cawdevelopment** (permission: write)
  - created_at (UTC): `2026-02-08T05:01:45Z`
  - created_at (America/New_York): `Sunday, 2026-02-08 12:01:45 AM EST`

## Trust model (current)
The only maintainer we treat as authoritative is **@cawdevelopment** (manifesto repo owner). Until acceptance happens, this repo stays receipts-first: anyone can fork and verify.

## OPSEC (anonymity + safety)
Methods stay transparent. We avoid publishing secrets or doxxing data.

If OPSEC issues are found, report with redactions + hashes, not raw secrets.
