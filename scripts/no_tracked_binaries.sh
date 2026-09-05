#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C
git rev-parse --is-inside-work-tree >/dev/null

# Permit only the exact reviewed public illustration; other binary evidence stays external.
# The explicit image request supersedes the old blanket image exclusion.
pat='\.(png|jpeg?|webp|gi|pdf|zip|7z|rar|bin|dat|ape|aac|mp3|wav|mp4|mov|exe|dmg)$'

bad=()
while IFS= read -r file; do
  if [[ "$file" == "docs/assets/r1-tablet.png" ]]; then
    printf '%s  %s\n' '889253e7fa85f5e5fd05622b8a105fd61acf83bdfdae3e600bdfedd173b2da41' "$file" | sha256sum -c -
  else
    bad+=("$file")
  fi
done < <(git ls-files | grep -Eai "$pat" || true)

if (( ${#bad[@]} )); then
  echo "[fail] tracked binary blobs are not allowed in canon."
  echo "       store evidence as .txt/.hex/.b64 + sha256; keep binaries external-by-hash."
  printf '%s\n' "${bad[@]}" | sed 's/^/ - /'
  exit 1
fi

echo "[ok] only the reviewed, hash-verified tablet image is tracked"
