#!/usr/bin/env python3
"""
Sanitize logs/transcripts to reduce identity leakage.

Doctest:
>>> s = ("xubutrad@DESKTOP-5SD1CP5:/home/xubutrad$ cd /home/xubutrad/gilg\\n"
...      "C:\\\\Users\\\\Rodney\\\\file.txt")
>>> sanitize_text(s)
'user@host:/home/user$ cd /home/user/gilg\\nC:\\\\Users\\\\REDACTED\\\\file.txt'
"""
from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path

LOG = logging.getLogger("sanitize_logs")

# NOTE: order matters. We sanitize user@host first, then prompt-path, then normal paths.
_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    # prompt "user@host:" prefix
    (re.compile(r"\b[^@\s]+@[^:\s]+:"), "user@host:"),

    # WSL prompt working dir like "/home/<user>$" or "/home/<user>:"
    (re.compile(r"/home/[A-Za-z0-9._-]+(?=[$:\s])"), "/home/user"),

    # normal linux home paths "/home/<user>/..."
    (re.compile(r"/home/[A-Za-z0-9._-]+/"), "/home/user/"),

    # WSL mounted windows paths "/mnt/c/Users/<user>/..."
    (re.compile(r"(?i)/mnt/[a-z]/Users/[^/]+/"), "/mnt/x/Users/REDACTED/"),

    # Windows user paths "C:\Users\<user>\..."
    (re.compile(r"(?i)C:\\\\Users\\\\[^\\\\]+\\\\"), r"C:\\Users\\REDACTED\\"),
    (re.compile(r"\bDESKTOP-[A-Z0-9-]+\b"), "HOST-REDACTED"),

    # emails
    (re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE), "redacted@example"),
]

def sanitize_text(text: str) -> str:
    assert isinstance(text, str)
    out = text
    for rx, repl in _PATTERNS:
        out = rx.sub(repl, out)
    return out

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inp", type=Path, help="input file")
    ap.add_argument("out", type=Path, help="output file")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(levelname)s %(message)s",
    )

    assert args.inp.is_file(), f"missing input: {args.inp}"
    assert args.out != args.inp, "output must differ from input"

    raw = args.inp.read_text(encoding="utf-8", errors="replace")
    san = sanitize_text(raw)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(san, encoding="utf-8")

    LOG.info("sanitized -> %s (bytes=%d)", args.out, len(san.encode("utf-8")))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
