# caw-lab — reproducible riddle forensics for the cawmmunity

> **Mission:** restore momentum by solving the CAW riddles **as intended**, **fully and reproducibly**, with **receipts** the entire **cawmmunity** can verify.

This repo is a public lab notebook: a canon timeline of layers, evidence, and exact reproduce steps. It exists because the cawmmunity has spent years stalled in noise, personality wars, and “leader” narratives. The chain doesn’t lie — but people do, and even good people get distracted.

## What Xubu believes (working principles)

- **Truth over trust.** Receipts before stories. If it can’t be reproduced, it isn’t canon.
- **No leaders.** We don’t need figureheads; we need verifiable work.
- **Respect the riddles.** Follow the intended path (including mirror/backwards instructions) and stop chasing red herrings.
- **Open hands.** Findings belong to the cawmmunity — not gatekeepers.
- **Humility.** “I don’t know yet” is allowed. Pretending is what breaks hunts.

## What this repo is (and is not)

✅ This repo **is**:
- A canon “layer index” for the riddles (approved layers only)
- Step-by-step reproduce instructions with hashes
- Evidence artifacts in *text form* (hex/base64) + checksums
- Scripts that enforce discipline (manifest verification, no-binaries policy)

❌ This repo is **not**:
- A hype page, price prediction, or “official” anything
- A place for unverifiable claims
- A dumping ground for binary blobs

## Riddles tracked

- **R1 (58bZfQ1)** — image/tablet → stego outputs → coords → book-cipher → CID → IPFS payload → DeepSound chain  
- **R2 (zrUfKaKV)** — onchain/paste provenance → zlib/FDICT streams → dictIDs + offsets → decode lanes

See **LAYER_INDEX.md** for the canon timeline.

## Repo structure

- `LAYER_INDEX.md` — canon timeline of approved layers
- `layers/<LAYER_ID>/`
  - `SUMMARY.md` — what this layer proves (and does not prove)
  - `REPRODUCE.md` — copy/paste commands to reproduce
  - `EVIDENCE/` — text artifacts + hashes (no binaries)
  - `MANIFEST.sha256` — sha256 list for that layer directory
- `scripts/` — repo discipline tools (manifest, sanitize, publish)
- `.github/` — CI + CODEOWNERS

## “No binaries” policy (important)

Canon branch rejects tracked binary blobs (png/pdf/zip/bin/audio/etc).  
Instead commit:
- `.sha256` checksums
- `.hex` or `.b64` encodings
- exact retrieval + reconstruction commands in `REPRODUCE.md`

## How to contribute (PRs)

1. Create a new layer folder from `layers/TEMPLATE/`.
2. Fill out SUMMARY + REPRODUCE with exact commands and expected hashes.
3. Put evidence in `EVIDENCE/` as text encodings + checksums.
4. Run:
   - `bash scripts/make_manifest.sh`
   - `bash scripts/verify_manifest.sh`
5. Open a PR into `canon`.

## Dedication: the original 2022 hunters

This repo is dedicated to the early hunters who moved the hunt forward in 2022 and beyond — including (non-exhaustive; handles as seen in archived chats):  
**Joop, Opti, Andy, Zenek, kachoperro, Peter Pan, Gorden, Asa||ANyONe, Binh N, Enkidu, Winter, KimDamyun**, and everyone else who contributed real receipts.  
If you should be listed (or a name is misspelled), open a PR to update this section.

## Reward stance

There may or may not be a reward for solving these riddles.  
If a reward exists and I receive a portion, **I donate my portion to be spread amongst holders who have held CAW for more than a year at any point**, unless the CAW deployer explicitly reinterprets/redirects that distribution.

## License

MIT (see LICENSE). DYOR / NFA.


## Deployer invite status

Invitation sent to **@cawdevelopment** (private scratchpad repo) for coordination and verification.

- created_at (UTC): `2026-02-08T05:01:45Z`
- created_at (America/New_York): `Sunday, 2026-02-08 12:01:45 AM EST`
- status: pending until accepted (invites do not appear in collaborator list until accepted)
