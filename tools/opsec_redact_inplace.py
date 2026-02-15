#!/usr/bin/env python3
"""
Deterministic OPSEC redaction for imported text bundles.

Only touches "text-like" extensions.

Doctest:
>>> _redact('rodez@DESKTOP-5SD1CP5:~/gilg')
'<USER>@DESKTOP-<HOST>:/home/<USER>/gilg'
"""
from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path
from typing import Iterable

LOG = logging.getLogger("opsec_redact")

TEXT_EXT = {
    ".txt", ".md", ".tsv", ".log", ".csv", ".json", ".yml", ".yaml", ".py", ".sh", ".html"
}

RX = [
    (re.compile(r"DESKTOP-[A-Za-z0-9-]+"), "DESKTOP-<HOST>"),
    (re.compile(r"/mnt/c/Users/[^/]+/"), "/mnt/c/Users/<USER>/"),
    (re.compile(r"/Users/[^/]+/"), "/Users/<USER>/"),
    (re.compile(r"/home/[^/]+/"), "/home/<USER>/"),
    (re.compile(r"\b[^@\s:]+@DESKTOP-[A-Za-z0-9-]+\b"), "<USER>@DESKTOP-<HOST>"),
    (re.compile(r"~\/"), "/home/<USER>/"),
]

def _redact(s: str) -> str:
    for r, repl in RX:
        s = r.sub(repl, s)
    return s

def _iter_files(root: Path) -> Iterable[Path]:
    assert root.exists(), f"missing root: {root}"
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in TEXT_EXT:
            yield p

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="folder to redact (in place)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    root = Path(args.root)
    assert root.is_dir(), f"not a directory: {root}"

    changed = 0
    for p in _iter_files(root):
        raw = p.read_text(encoding="utf-8", errors="ignore")
        red = _redact(raw)
        if red != raw:
            p.write_text(red, encoding="utf-8", newline="\n")
            changed += 1
            LOG.info("redacted: %s", p)

    LOG.info("done: changed=%d", changed)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
