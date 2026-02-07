#!/usr/bin/env python3
from __future__ import annotations
import re
import sys
from pathlib import Path

HEXPAIR = re.compile(r"[0-9a-fA-F]{2}")

def extract_rawprofile_hex(exiftool_text: str) -> str:
    """
    Extract the "Raw Profile Type Exif" bytes from exiftool -a -u -g1 output.

    Returns lowercase hex (no spaces, no 0x), newline-terminated.

    The block can appear as:
      Raw Profile Type Exif : 45786966...
    or as a multi-line hex dump. We collect hexpairs until the next tag-like line.

    >>> extract_rawprofile_hex("Raw Profile Type Exif : 45 78 69 66\\nOther : 00\\n")[:8]
    '45786966'
    """
    lines = exiftool_text.splitlines()
    out: list[str] = []
    in_block = False

    for ln in lines:
        if not in_block:
            if re.search(r"^\s*Raw Profile Type Exif\s*:", ln, flags=re.IGNORECASE):
                in_block = True
                # grab hexpairs on the same line after ':'
                after = ln.split(":", 1)[1]
                out.extend(HEXPAIR.findall(after))
            continue

        # stop on next "Tag : value" line (but allow indented hex rows)
        if re.search(r"^\S.*\s:\s", ln) and not re.search(r"^\s*[0-9A-Fa-f]{4}\b", ln):
            break

        # collect all hexpairs from this line (works for both "00 11" and "0011" styles)
        out.extend(HEXPAIR.findall(ln))

    if not out:
        raise ValueError("Raw Profile Type Exif block not found or contained no hexpairs")

    return "".join(x.lower() for x in out) + "\n"

def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"usage: {argv[0]} <exiftool.txt> <out.hex>", file=sys.stderr)
        return 2

    inp = Path(argv[1])
    outp = Path(argv[2])
    if not inp.is_file():
        print(f"[fail] missing input: {inp}", file=sys.stderr)
        return 2

    txt = inp.read_text(encoding="utf-8", errors="replace")
    hexs = extract_rawprofile_hex(txt)

    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(hexs, encoding="utf-8", newline="\n")
    print(f"[ok] wrote {outp} ({(len(hexs.strip())//2)} bytes)")

    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
