#!/usr/bin/env bash
set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C
cd "$(git rev-parse --show-toplevel)"

# These three evidence files were published on canon in 7a8ac262ce2b.
evidence_dir=docs/evidence/r1-reproduction-20261111
declare -Ar pinned=(
  [docs/assets/r1-tablet.png]=889253e7fa85f5e5fd05622b8a105fd61acf83bdfdae3e600bdfedd173b2da41
  ["$evidence_dir/R1-Ten-Reproduction-20261111-v3.zip"]=748de57f61df4a6c8c7749dc091dd9305a703fd6c6182785a49f85a427f41fbf
  ["$evidence_dir/caption-original-10x.png"]=f8dff0722c7f29b758ae43fc4ea6fb8af2a691a7eec1eb3bdd35a1bb059d3405
  ["$evidence_dir/caption-red-lsb-8x.png"]=2a134586dd0e7c11da9ac0f060a1666aa77ff9e38c208ea9c9a842ab7d08c876
)

for file in "${!pinned[@]}"; do
  git ls-files --error-unmatch -- "$file" >/dev/null
  if [[ ! -f "$file" || -L "$file" ]]; then
    printf '[fail] expected a regular evidence file: %s\n' "$file" >&2
    exit 1
  fi
  printf '%s  %s\n' "${pinned[$file]}" "$file" | sha256sum --check --strict -
done

bad=()
pat='\.(png|jpeg?|webp|gi|pdf|zip|7z|rar|bin|dat|ape|aac|mp3|wav|mp4|mov|exe|dmg)$'
while IFS= read -r -d '' file; do
  if [[ ${file,,} =~ $pat && -z ${pinned[$file]+yes} ]]; then
    bad+=("$file")
  fi
done < <(git ls-files -z)

if (( ${#bad[@]} )); then
  echo "[fail] tracked binary blobs are not allowed in canon."
  echo "       store evidence as .txt/.hex/.b64 + sha256; keep binaries external-by-hash."
  printf '%s\n' "${bad[@]}" | sed 's/^/ - /'
  exit 1
fi

echo "[ok] all pinned evidence files match and no additional tracked binary matched the filter"
