#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Assembled literal to reduce accidental copy/paste leakage.
DENYLIST_DOMAIN = "smartproperty" + "solar.com"

EXCLUDE_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip", ".gz",
    ".7z", ".rar", ".exe", ".bin", ".dat", ".mp3", ".mp4", ".wav",
}

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("denylist_domain", re.compile(re.escape(DENYLIST_DOMAIN), re.IGNORECASE)),
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
]

def sha256_16(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()[:16]

def tracked_files() -> list[Path]:
    """
    Prefer git-tracked files to avoid scanning generated junk.
    Fallback to repo walk if git metadata is unavailable.
    """
    try:
        out = subprocess.check_output(["git", "ls-files"], cwd=REPO_ROOT, text=True)
        rels = [ln.strip() for ln in out.splitlines() if ln.strip()]
        files: list[Path] = []
        for rel in rels:
            p = REPO_ROOT / rel
            if p.is_file():
                files.append(p)
        return files
    except Exception:
        files: list[Path] = []
        for p in REPO_ROOT.rglob("*"):
            if not p.is_file():
                continue
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            if p.suffix.lower() in EXCLUDE_SUFFIXES:
                continue
            files.append(p)
        return files

def main() -> int:
    findings: list[tuple[str, int, str, str]] = []

    for path in tracked_files():
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in EXCLUDE_SUFFIXES:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        rel = path.relative_to(REPO_ROOT).as_posix()

        for lineno, line in enumerate(text.splitlines(), start=1):
            for name, rx in PATTERNS:
                m = rx.search(line)
                if not m:
                    continue

                # Never print raw match; only hashed token.
                token_hash = sha256_16(m.group(0))
                findings.append((rel, lineno, name, token_hash))

                # Fast-fail on denylist, still without leaking raw line.
                if name == "denylist_domain":
                    print(f"{rel}:{lineno}:{name} sha256_16={token_hash}")
                    print("Privacy guard failed (denylist).")
                    return 1

    if findings:
        for rel, lineno, name, token_hash in findings:
            print(f"{rel}:{lineno}:{name} sha256_16={token_hash}")
        print(f"Privacy guard failed with {len(findings)} finding(s).")
        return 1

    print("Privacy guard passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
