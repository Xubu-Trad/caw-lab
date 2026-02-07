#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C
git rev-parse --is-inside-work-tree >/dev/null

# Disallow tracked binary blobs in canon.
# Evidence must be committed as text: .txt/.hex/.b64 + sha256 (binaries stay external-by-hash).
pat='\.(png|jpeg?|webp|gi|pdf|zip|7z|rar|bin|dat|ape|aac|mp3|wav|mp4|mov|exe|dmg)$'

mapfile -t bad < <(git ls-files | grep -Eai "$pat" || true)

if (( ${#bad[@]} )); then
  echo "[fail] tracked binary blobs are not allowed in canon."
  echo "       store evidence as .txt/.hex/.b64 + sha256; keep binaries external-by-hash."
  printf '%s\n' "${bad[@]}" | sed 's/^/ - /'
  exit 1
fi

echo "[ok] no tracked binary blobs"
