# CAW Lab (Public Canon)

> **Not official. Receipts only. Forks encouraged.**
> This repo is a **reproducible evidence ledger**: hashes + steps + gates.
> If you disagree, **fork and publish receipts**.


This repository is a **public, receipts-first “canon”** for CAW riddle hunting:
- reproducible layer-by-layer evidence
- deterministic hashing/manifests
- objective gates (CI) instead of personality/authority

**Not official. No leaders. Forks encouraged.**  
If anything here conflicts with the on-chain record, the chain wins.

## Quick verify (what CI runs)

From repo root:

```bash
bash scripts/check_canon.sh
```

This enforces:
- no tracked binary blobs
- manifest matches canonical computation
- no empty evidence files (sanity for reproducibility)

## Repo structure

- `LAYER_INDEX.md` — high-level index across layers
- `layers/` — each layer folder contains:
  - `SUMMARY.md` (what we learned, with citations/receipts)
  - `REPRODUCE.md` (exact commands/workflow)
  - `EVIDENCE/` (inputs + logs + hashes)
- `docs/` — hunter guidance, sanitized notes, conventions
- `scripts/` — verification + helper tooling used by CI

Start here:
- `LAYER_INDEX.md`
- `docs/HUNTERS.md`
- then any specific layer `layers/**/REPRODUCE.md`

## Layers (directories)

- [R1-000_yale_oldking](layers/R1-000_yale_oldking/)
- [R1-010](layers/R1-010/)
- [TEMPLATE](layers/TEMPLATE/)

## Deployer / maintainer status (for the CAWmmunity)

- Public canon repo owner: **@Xubu-Trad**
- Private scratchpad repo: `Xubu-Trad/caw-lab-private` (experiments; not canon)

**Invitation sent to @cawdevelopment (private scratchpad):**
- invitee: `cawdevelopment`
- created_at (UTC): `2026-02-08T05:01:45Z`
- created_at (America/New_York): `Sunday, 2026-02-08 12:01:45 AM EST`
- status: *pending until accepted* (collaborator list will not show invitees until acceptance)

At this moment, **the only maintainership we trust is the owner of `cawdevelopment` (the CAW deployer) once/if they accept and prove custody**.

## Maintainers (leaderless-by-design, but receipts-required)

There are **no community maintainers** besides the repo owner today.

If you want to be considered as a maintainer candidate:
- submit a PR that **solves a layer** or provides a **significant new finding**
- include full receipts: commands, hashes, and reproducible steps
- no off-repo “trust me” handoffs; everything must be verifiable here

## Anti-scam + anonymity

- This repo will never ask you to run mystery executables.
- Do not trust DMs. Prefer PRs/issues so everything stays public and reviewable.
- We keep methods transparent while stripping accidental identity leaks where possible.

Run the local scans before you publish new logs:
```bash
bash scripts/anonymity_scan.sh
bash scripts/audit_completeness.sh
```



## Maintainer candidates (receipts required)

There are **no community maintainers** today.

If you want to be considered as a maintainer candidate:
- submit a PR that **solves a layer** or provides a **significant new finding**
- include full receipts: commands, hashes, reproducible steps
- keep everything reviewable in public (no DM “trust me” handoffs)

Until the CAW deployer confirms custody via **@cawdevelopment**, this repo remains receipts-first and fork-friendly.
