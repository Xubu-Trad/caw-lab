# R1-010 — Tablet PNG → EXIF receipts (text-only)

This layer produces *text receipts* from the tablet PNG without committing any binary files.

## Inputs (not tracked)

- `IN/tablet.png` (downloaded locally; only its SHA-256 is committed)

Known host of the tablet PNG (direct hotlink):

- `https://i.ibb.co/9TQPCxp/Proposalforadecentralizedcoupfortehpplbytehppl.png`

## Outputs (tracked)

- `layers/R1-010/EVIDENCE/tablet.png.sha256`
- `layers/R1-010/EVIDENCE/exiftool.txt`
- `layers/R1-010/EVIDENCE/full_coords.txt`
- `layers/R1-010/EVIDENCE/poem.txt`
- `layers/R1-010/EVIDENCE/fallback_lettercount.txt`

Optional (only after extraction is reproducible):

- `layers/R1-010/EVIDENCE/exif_rawprofile.hex`
- `layers/R1-010/EVIDENCE/exif_rawprofile.bin.sha256`
- `layers/R1-010/EVIDENCE/exif_rawprofile.bin.head.txt`

## Paste (safe: no heredocs)

```bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C
set +H 2>/dev/null || true
stty -ixon -ixoff 2>/dev/null || true

cd "$(git rev-parse --show-toplevel)"

mkdir -p IN layers/R1-010/EVIDENCE

# 1) Acquire input (do NOT commit the PNG)
curl -L --fail -o IN/tablet.png \
  "https://i.ibb.co/9TQPCxp/Proposalforadecentralizedcoupfortehpplbytehppl.png"

sha256sum IN/tablet.png | tee layers/R1-010/EVIDENCE/tablet.png.sha256

# 2) EXIF receipt
command -v exiftool >/dev/null
exiftool -a -u -g1 IN/tablet.png | tee layers/R1-010/EVIDENCE/exiftool.txt >/dev/null

# 3) Refresh manifest + run canon gate
bash scripts/make_manifest.sh
bash scripts/check_canon.sh

git status --porcelain
```

