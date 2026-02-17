#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail() { printf "\n[FAIL] %s\n" "$*" >&2; exit 1; }
ok()   { printf "[ok] %s\n" "$*"; }

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || fail "not a git repo"

# ---- 1) Forbid tracking raw/scratch/private material
forbidden_re='(^|/)(_raw_uploads|OUT|OUTD|OUT_[^/]+|\.ssh|\.gnupg|\.aws|\.kube|node_modules|__pycache__|\.venv|\.env)(/|$)|\.(pem|key|p12|pfx|kdbx)$'
bad_paths="$(git ls-files | grep -nE "$forbidden_re" || true)"
[ -z "$bad_paths" ] || fail "tracked forbidden paths/files:\n$bad_paths"
ok "no forbidden tracked paths"

# ---- 2) Block REAL host paths / machine ids leaking into tracked text
# IMPORTANT: detect *real* usernames/hosts only (won't match placeholders like <USER>, <HOST>, <drive>)
# - /mnt/<drive>/Users/[A-Za-z0-9._-]+/...  (real)
# - <DRIVE>:\Users\<USER>\...      (real)
# - /Users/[A-Za-z0-9._-]+/...        (real mac)
# - DESKTOP-<HOST>         (real)
host_re='(/mnt/[a-z]/Users/[A-Za-z0-9._-]+/|C:\\Users\\[A-Za-z0-9._-]+\\|/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|DESKTOP-[A-Za-z0-9-]{4,})'
host_leaks="$(git grep -nI -E "$host_re" -- layers docs history ledger || true)"
if [ -n "$host_leaks" ]; then
  OUT="${OUT:-OUT/opsec_audit}"
  mkdir -p "$OUT"
  f="$OUT/host_leaks.txt"
  printf "%s
" "$host_leaks" >"$f"
  headn="${SANITIZE_AUDIT_HEAD:-80}"
  fail "host paths / machine ids found in tracked text (showing first ${headn} lines; full saved to $f):
$(printf "%s
" "$host_leaks" | head -n "$headn")"
fi
ok "no host paths / machine ids leaked"

# ---- 3) Optional max file size guard (public repo can set MAX_BYTES low)
MAX_BYTES="${MAX_BYTES:-0}"
if [ "$MAX_BYTES" -gt 0 ]; then
  big="$(git ls-files -z | xargs -0 -I{} bash -lc 's=$(wc -c <"{}"); if [ "$s" -gt "'"$MAX_BYTES"'" ]; then echo "{}:$s"; fi' || true)"
  [ -z "$big" ] || fail "tracked files exceed MAX_BYTES=$MAX_BYTES:\n$big"
  ok "no files exceed MAX_BYTES"
fi

# ---- 4) Duplicate layer guard (history/ingested exact-content duplicates)
if [ -d "history/ingested" ]; then
  dups="$(
    python3 - <<'PY'
from __future__ import annotations
from pathlib import Path
import hashlib
p = Path("history/ingested")
if not p.is_dir():
    raise SystemExit(0)
hmap: dict[str, list[str]] = {}
for f in sorted(p.rglob("*")):
    if not f.is_file():
        continue
    b = f.read_bytes()
    h = hashlib.sha256(b).hexdigest()
    hmap.setdefault(h, []).append(str(f))
dups = [(h, files) for h, files in hmap.items() if len(files) > 1]
for h, files in sorted(dups, key=lambda x: (-len(x[1]), x[0])):
    print(h)
    for f in files:
        print("  " + f)
PY
  )"
  [ -z "$dups" ] || fail "duplicate layer content in history/ingested (sha256 groups):\n$dups"
  ok "no duplicate layer content in history/ingested"
else
  ok "history/ingested not present (skip dup check)"
fi


