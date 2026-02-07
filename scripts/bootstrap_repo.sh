#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C

MODE="${1:-lab}"  # lab|canon
[[ "$MODE" == "lab" || "$MODE" == "canon" ]] || { echo "usage: $0 [lab|canon]" >&2; exit 2; }

git rev-parse --show-toplevel >/dev/null 2>&1 || { echo "not in a git repo" >&2; exit 2; }

mkdir -p layers docs scripts .github/workflows
if [[ "$MODE" == "lab" ]]; then
  mkdir -p lab_notes experiments private_evidence
fi

cat > .gitignore <<'EOF'
# Never commit local forensic workspace
OUT/
IN/
.cache/
__pycache__/
*.pyc
*.swp

# Large/binary evidence must be external-by-hash unless explicitly approved
*.png
*.jpg
*.jpeg
*.webp
*.gif
*.pdf
*.zip
*.7z
*.rar
*.bin
*.dat
*.ape
*.aac
*.mp3
*.wav

# Secrets
.env
*.key
*.pem
id_ed25519*
*.p12

# OS / editor
.DS_Store
Thumbs.db
.vscode/
EOF

cat > SECURITY.md <<'EOF'
# SECURITY / SAFETY RULES

Do NOT commit:
- API keys, tokens, cookies, auth headers, seed phrases
- Raw corpora that may be copyrighted (store externally by hash)
- Unsanitized terminal logs that contain usernames/hostnames/home paths
- Images/PDFs with EXIF/metadata unless stripped

If you find a sensitive leak, open a private issue in caw-lab and notify maintainers.
EOF

cat > README.md <<'EOF'
# CAW Riddle Research (lab)

This repo is the private source-of-truth for CAW riddle research.

- `main` = lab work (experiments allowed)
- `canon` = approved/promotable layers ONLY (no lab_notes, no experiments)

Publishing:
- Canon layers are reviewed in PRs into `canon`
- After approval, use `scripts/publish_to_public.sh` to promote into `caw-canon`
EOF

cat > LAYER_INDEX.md <<'EOF'
# LAYER INDEX (CANON TIMELINE)

> This file is generated/maintained as layers are approved.
> Each layer lives in `layers/<LAYER_ID>/` with SUMMARY + REPRODUCE + EVIDENCE + MANIFEST.

## R1 (58bZfQ1)
- R1-000: (placeholder) onchain pointer + first clue tablet provenance
- R1-010: (placeholder) stego outputs: poem + coords
- R1-020: (placeholder) book-cipher → CID
- R1-030: (placeholder) IPFS payload (.APE) retrieval + hashes
- R1-040: (placeholder) DeepSound → Enkidu decode chain

## R2 (zrUfKaKV)
- R2-000: (placeholder) onchain pointer + pastebin provenance
- R2-010: (placeholder) zlib/FDICT streams → dictID(s) + offsets
EOF

cat > LICENSE <<'EOF'
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
EOF

cat > .github/pull_request_template.md <<'EOF'
## Layer submission (required)

**Layer ID:**  
**Claim (one sentence):**  

### Evidence (required)
- Artifacts (hashes/CIDs/txids/URLs):
- Where stored in repo (`layers/<LAYER_ID>/EVIDENCE/...`):
- External artifacts (by hash only):

### Reproduction (required)
Paste the exact commands (copy/paste runnable), including:
- Inputs (path + sha256 + size)
- Transform command/script
- Outputs (path + sha256 + size)
- Validator used

### Anonymity/Safety check (required)
- [ ] Logs sanitized (no username/host/home paths)
- [ ] No EXIF/metadata leaks
- [ ] No tokens/keys
- [ ] No raw copyrighted corpus committed

### Reviewer notes
EOF

cat > .github/CODEOWNERS <<'EOF'
# Require designated reviewers for canon changes
/layers/ @CAW-development
/docs/   @CAW-development
/scripts/ @CAW-development
/LAYER_INDEX.md @CAW-development
EOF

cat > .github/workflows/ci.yml <<'EOF'
name: ci
on:
  pull_request:
    branches: [ "canon" ]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Basic forbidden-pattern scan
        run: |
          set -Eeuo pipefail
          ! rg -n "C:\\\\Users\\\\|/home/[^/]+/|DESKTOP-[A-Z0-9-]+|BEGIN (RSA|OPENSSH) PRIVATE KEY" .
      - name: Verify manifest (if present)
        run: |
          set -Eeuo pipefail
          if [[ -f scripts/verify_manifest.sh ]]; then bash scripts/verify_manifest.sh; fi
EOF

# layer skeleton helper
mkdir -p layers/TEMPLATE/EVIDENCE
cat > layers/TEMPLATE/SUMMARY.md <<'EOF'
# SUMMARY

- What was proven (facts only)
- What remains open
EOF
cat > layers/TEMPLATE/REPRODUCE.md <<'EOF'
# REPRODUCE

## Preconditions
## Commands
## Expected outputs (hashes)
## Validators
EOF
cat > layers/TEMPLATE/MANIFEST.sha256 <<'EOF'
# Put external artifact hashes here (one per line):
# sha256  <filename-or-label>
EOF

chmod +x scripts/bootstrap_repo.sh
echo "[ok] bootstrap complete: mode=$MODE"
