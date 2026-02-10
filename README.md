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
<!-- RIDDLE_PROGRESS_BEGIN -->
## Riddle progress

- Progress overview: `docs/RIDDLE_PROGRESS.md`
- On-chain provenance: `docs/ONCHAIN_TRACE.md`
- What these facts do (and do not) prove: `docs/WHAT_THE_FACTS_PROVE.md`
- R1 end-to-end: `docs/R1_58bZfQ1_END_TO_END.md`
- R2 status: `docs/R2_zrUfKaKV_STATUS.md`

## Layer index (chronological)
- `layers/R1-000_yale_oldking/`
- `layers/R1-010_friderici_poem_coords/`
- `layers/R1-020_book_cipher_gilgamesh/`
- `layers/R1-030_ipfs_ape_audio/`
- `layers/R1-040_deepsound_enkidu/`
- `layers/R1-050_manifesto_final_payload/`
- `layers/R2-000_onchain_zrufkakv/`
- `layers/R2-010_pastebin_payload/`
<!-- RIDDLE_PROGRESS_END -->

<!-- CAW_TRUTHS_BEGIN -->

## What CAW is (truths, not hype)

**CAW: A Hunter's Dream** is not "just a ticker." It's an **on-chain artifact + community hunt** where the "product" is the trail itself: contracts, transactions, files, ciphers, and a manifesto narrative that only makes sense when you **verify receipts**.

This repo exists to keep the work **auditable**:
- reproducible steps (scripts + exact commands),
- hashes + manifests,
- no "trust me bro",
- clear separation between **facts** and **hypotheses**.

### What we can say as facts (receipts-first)
- There is a real CAW token contract on-chain: `0xf3b9569f82b18aef890de263b84189bd33ebe452`.
- The riddle trail is anchored by identifiable on-chain activity and artifacts that can be re-derived by independent readers.
- This repo is organized as a **layered evidence pack** (R1 and R2), designed to be checked and reproduced.
- The "no-admin-control-surface" claim is treated as a **verifiable exhibit** in this repo (see `docs/WHAT_THE_FACTS_PROVE.md`).

### What we should NOT pretend we know (yet)
- The real-world identity behind any handle(s).
- Whether any "builder" is one person or many.
- The full intended ending of R2 until it is independently reproduced end-to-end.

---

## What's needed to finish the riddles (current completion definition)

**Completion means:** an independent reader can start from the anchors, reproduce each layer, and end at the same outputs (matching hashes/manifests) **without private context**.

### R1 (58bZfQ1) — finish criteria
- Reproduce end-to-end from: **Yale/OldKing image → Friderici/coords → book-cipher → CID → APE → DeepSound (enkidu) → final payload**.
- Publish the **exact corpus/offset/trim** method that makes the book-cipher deterministic for everyone.
- Ensure every step has:
  - commands in `REPRODUCE.md`,
  - outputs hashed into `MANIFEST.repo.sha256`,
  - and receipts pinned in the relevant `layers/R1-*` folders.

### R2 (zrUfKaKV) — finish criteria
- Reproduce the on-chain anchor and recovery path into a stable decoded payload.
- Document the decode pipeline so that:
  - byte-for-byte outputs match,
  - alternative decode branches are labeled as hypotheses,
  - and only verified branches graduate into canon.

---

## A plea from Xubu (XT)

> "I'm asking the community to do something harder and more honest: review the evidence and trust yourself." — XT

---

## OG hunters (living list)
See `docs/HUNTERS.md` for the maintained list.  
Additions requested:
- Enkidu's gf*

<!-- CAW_TRUTHS_END -->
