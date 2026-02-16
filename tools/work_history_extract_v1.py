#!/usr/bin/env python3
"""
work_history_extract_v1.py

Extract only *puzzle-solving* attempt blocks from mixed work-history text files,
redact local identifiers (usernames/host paths/emails), and write curated
snippets into history/inbox/ for later ingestion.

YES:
- tool outputs + verdict logs (zsteg/exif/binwalk, sha256sum outputs, offsets, dictid, CID/Qm, ACCEPTED/REJECTED)
- terminal command blocks with real outputs

NO:
- paste aborts / broken heredocs / scripting & repo wiring (git/ssh/bn/chmod/.bashrc/etc)

Usage:
  python3 tools/work_history_extract_v1.py /path/to/log1.txt [/path/to/log2.txt ...]
  python3 tools/work_history_extract_v1.py /path/to/dir_with_txts

Env:
  WHX_MAX_BLOCKS=60   # cap curated blocks per input (default 60)

Doctests:
>>> sanitize_filename("chatgpt first riddle 3.txt")
'chatgpt_first_riddle_3.txt'
>>> strip_prompt("prefix:~/gilg$ zsteg -a suspect.png")
'$ zsteg -a suspect.png'
>>> redact_text("path /home/USER/gilg and addr a[at]b[dot]com")
'path ~/gilg and addr <EMAIL_REDACTED>'
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import os
import re
import sys
from pathlib import Path
from typing import List, Sequence, Tuple


PROMPT_RE = re.compile(r'^(?:[A-Za-z0-9_.-]+@[^:\s]+:[^\n]*?)?[$#]\s+|^\$\s+|^#\s+')

# "Puzzle" signals (tools, artifacts, outputs)
PUZZLE_KW = (
    "zsteg", "exiftool", "binwalk", "pngcheck", "xxd", "hexdump", "strings", "file ",
    "ffprobe", "ffmpeg", "ipfs", "cid", "qm", "deep sound", "deepsound",
    "gpg", "pgp", "openssl", "zlib", "adler", "dictid", "offset", "iend", "itxt", "ztxt",
    "gilgamesh", "enkidu", "friderici", "aperisolve", "ape", "monkey", "mac ",
    "log_verdict", "accepted", "rejected", "sha256", "rows=", "out/",
)

# "Infra" signals (setup / repo chores)
INFRA_KW = (
    "cat > scripts/", "chmod +x", "bash -n", "python3 -m doctest", ".bashrc",
    "ssh-agent", "ssh-add", "git commit", "git push", "git status", "git clone",
    "enumerating objects", "delta compression", "to github.com",
    "write_text(", "mkdir -p scripts",
)

MARKER_RE = re.compile(
    r'(log_verdict|ACCEPTED|REJECTED|offset\s*=\s*0x[0-9a-fA-F]+|DICTID|CID\b|Qm[1-9A-HJ-NP-Za-km-z]{20,}|sha256(?:sum)?\b)',
    re.IGNORECASE,
)

# "Real output" signals (avoid capturing pure instructions)
OUTPUT_RE = re.compile(
    r'^(?:'
    r'\[[a-z]+\]|INFO:|ERROR:|WARNING:|TOKENS\s+\+|log_verdict\b|'
    r'deduped entries:|accepted unique values:|kept ACCEPTED entries:|'
    r'file:\s+|[0-9a-f]{64}\s+|'
    r'\s*Aperi\'?Solve\b|\s*ExifTool\b|'
    r'[A-Z][A-Za-z0-9 /()\'-]{2,}\t'
    r')',
    re.IGNORECASE,
)


def sanitize_filename(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")
    return s or "unnamed"


def strip_prompt(line: str) -> str:
    """Reduce noisy PS1 prefixes to a stable '$ cmd' form."""
    s = line.rstrip("\n")

    if "$ " in s and not s.lstrip().startswith("$"):
        _pre, cmd = s.split("$ ", 1)
        if cmd.strip():
            return "$ " + cmd.strip()

    if "# " in s and not s.lstrip().startswith("#"):
        _pre, cmd = s.split("# ", 1)
        if cmd.strip():
            return "# " + cmd.strip()

    if s.lstrip().startswith("$ ") or s.lstrip().startswith("# "):
        return s.strip()

    return s


def _sha256_hex(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def redact_text(text: str) -> str:
    """Redact local identifiers while keeping forensic meaning."""
    t = text

    # home dirs -> ~
    t = re.sub(r"/home/[^/\s]+/gilg\b", "~/gilg", t)
    t = re.sub(r"/home/[^/\s]+\b", "~", t)

    # WSL mounts -> generic
    t = re.sub(r"/mnt/[a-z]/Users/[^/\s]+", "/mnt/<drive>/Users/<USER>", t, flags=re.IGNORECASE)

    # Windows paths -> generic (covers both \ and /)
    t = re.sub(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+", r"C:\\Users\\<USER>", t)

    # hostnames like DESKTOP-<HOST> -> generic
    t = re.sub(r"\bDESKTOP-[A-Za-z0-9]+\b", "DESKTOP-<HOST>", t)

    # emails
    t = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "<EMAIL_REDACTED>", t)
    # bracketed pseudo-emails like a[at]b[dot]com
    t = re.sub(
        r"\b[A-Za-z0-9._%+-]+\[at\][A-Za-z0-9.-]+\[dot\][A-Za-z]{2,}\b",
        "<EMAIL_REDACTED>",
        t,
        flags=re.IGNORECASE,
    )

    return t


def _score(text: str) -> Tuple[int, int, int]:
    low = text.lower()
    p = sum(low.count(k.lower()) for k in PUZZLE_KW)
    i = sum(low.count(k.lower()) for k in INFRA_KW)
    m = 1 if MARKER_RE.search(text) else 0
    return p, i, m


def _looks_like_command(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if PROMPT_RE.match(s):
        return True
    return bool(
        re.match(
            r"^(sudo\s+)?(python3?|zsteg|binwalk|exiftool|pngcheck|xxd|strings|file|ffprobe|ffmpeg|ipfs|gpg|openssl|grep|rg|jq)\b",
            s,
        )
    )


def _looks_like_output(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if _looks_like_command(s):
        return False
    return bool(OUTPUT_RE.search(s))


def _extract_prompt_blocks(lines: Sequence[str], max_block_lines: int = 250) -> List[Tuple[int, int]]:
    blocks: List[Tuple[int, int]] = []
    i = 0
    n = len(lines)
    while i < n:
        if PROMPT_RE.match(lines[i]):
            s = i
            i += 1
            while i < n and not PROMPT_RE.match(lines[i]) and (i - s) < max_block_lines:
                i += 1
            blocks.append((s, i))
        else:
            i += 1
    return blocks


def _extract_marker_windows(lines: Sequence[str], before: int = 18, after: int = 70, limit_hits: int = 600) -> List[Tuple[int, int]]:
    hits = []
    for idx, ln in enumerate(lines):
        if MARKER_RE.search(ln) or OUTPUT_RE.search(ln):
            hits.append(idx)
            if len(hits) >= limit_hits:
                break
    blocks = []
    for h in hits:
        s = max(0, h - before)
        e = min(len(lines), h + after)
        blocks.append((s, e))
    return blocks


def _merge_blocks(blocks: List[Tuple[int, int]], max_merged_lines: int = 420) -> List[Tuple[int, int]]:
    if not blocks:
        return []
    blocks = sorted(blocks)
    merged: List[List[int]] = []
    for s, e in blocks:
        if not merged:
            merged.append([s, e])
            continue
        ps, pe = merged[-1]
        if s <= pe:
            if (max(pe, e) - ps) <= max_merged_lines:
                merged[-1][1] = max(pe, e)
            else:
                merged.append([s, e])
        else:
            merged.append([s, e])
    return [(a, b) for a, b in merged]


def _trim_block(lines: Sequence[str], s: int, e: int, max_lines: int = 180) -> List[str]:
    block = [strip_prompt(l) for l in lines[s:e]]
    if len(block) <= max_lines:
        return block
    head = block[:60]
    tail = block[-60:]
    skipped = len(block) - len(head) - len(tail)
    return head + [f"... [snip {skipped} line(s)] ..."] + tail


@dataclasses.dataclass(frozen=True)
class Extracted:
    src: Path
    raw_sha256: str
    tag: str
    idx: int
    start: int
    end: int
    puzzle_score: int
    infra_score: int
    has_marker: int
    lines: List[str]

    def content(self) -> str:
        hdr = [
            "# work_history_extract_v1",
            f"# src_base: {self.src.name}",
            f"# raw_sha256: {self.raw_sha256}",
            f"# tag: {self.tag}",
            f"# block: {self.idx:03d}",
            f"# range: L{self.start+1}-L{self.end}",
            f"# score: puzzle={self.puzzle_score} infra={self.infra_score} marker={self.has_marker}",
            "",
        ]
        return "\n".join(hdr + [redact_text("\n".join(self.lines))]).rstrip() + "\n"


def _tag_for_text(text: str, src_name: str) -> str:
    low = (src_name + "\n" + text).lower()
    if "zrufkakv" in low or "zruf" in low:
        return "R2"
    if "58bzfq1" in low or "first riddle" in low or "gilgamesh" in low or "enkidu" in low:
        return "R1"
    return "GEN"


def _iter_inputs(args: Sequence[str]) -> List[Path]:
    out: List[Path] = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            out.extend(sorted([q for q in p.glob("*.txt") if q.is_file()]))
        else:
            out.append(p)
    # de-dup
    seen = set()
    uniq: List[Path] = []
    for p in out:
        rp = p.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        uniq.append(p)
    return uniq


def extract_file(src: Path, out_dir: Path) -> List[Extracted]:
    if not src.exists() or not src.is_file():
        return []
    if src.stat().st_size == 0:
        return []

    raw = src.read_text(errors="replace")
    tag = _tag_for_text(raw, src.name)
    raw_sha = _sha256_hex(src)
    max_blocks_per_file = int(os.environ.get("WHX_MAX_BLOCKS", "60"))

    lines = raw.splitlines()
    cand: List[Tuple[int, int]] = []
    cand.extend(_extract_prompt_blocks(lines))
    cand.extend(_extract_marker_windows(lines))
    blocks = _merge_blocks(cand)

    extracted: List[Extracted] = []
    bi = 0
    for s, e in blocks:
        trimmed = _trim_block(lines, s, e)
        block_text = "\n".join(trimmed)
        pscore, iscore, marker = _score(block_text)

        has_out = any(_looks_like_output(x) for x in trimmed)
        if not has_out:
            continue

        has_cmd = any(_looks_like_command(x) for x in trimmed[:10])
        if (not has_cmd) and marker == 0:
            continue

        if iscore > max(4, pscore + 3) and marker == 0:
            continue
        if pscore < 2 and marker == 0:
            continue

        bi += 1
        extracted.append(
            Extracted(
                src=src,
                raw_sha256=raw_sha,
                tag=tag,
                idx=bi,
                start=s,
                end=e,
                puzzle_score=pscore,
                infra_score=iscore,
                has_marker=marker,
                lines=trimmed,
            )
        )

    extracted_sorted = sorted(
        extracted,
        key=lambda x: (x.has_marker, x.puzzle_score - x.infra_score, x.puzzle_score),
        reverse=True,
    )

    uniq: List[Extracted] = []
    seen_sha = set()
    for ex in extracted_sorted:
        body = ex.content()
        sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
        if sha in seen_sha:
            continue
        seen_sha.add(sha)
        uniq.append(ex)
        if len(uniq) >= max_blocks_per_file:
            break

    ts = __import__("datetime").datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    base = sanitize_filename(src.stem)
    for ex in uniq:
        body = ex.content()
        sha16 = hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]
        name = f"{ts}__WHX__{ex.tag}__{base}__b{ex.idx:03d}__{sha16}.txt"
        (out_dir / name).write_text(body, encoding="utf-8")

    return uniq


def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", help="file(s) or directory(ies) containing .txt logs")
    ap.add_argument("--out", default="history/inbox", help="output directory (default: history/inbox)")
    ns = ap.parse_args(list(argv))

    # ensure inside repo
    root = Path.cwd()
    while root != root.parent and not (root / ".git").exists():
        root = root.parent
    if not (root / ".git").exists():
        print("[fail] run from inside your git repo", file=sys.stderr)
        return 2

    out_dir = (root / ns.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    inputs = _iter_inputs(ns.paths)
    if not inputs:
        print("[fail] no inputs", file=sys.stderr)
        return 2

    total_blocks = 0
    for src in inputs:
        ex = extract_file(src, out_dir=out_dir)
        if ex:
            print(f"[ok] {src.name}: wrote {len(ex)} curated block(s)")
            total_blocks += len(ex)
        else:
            print(f"[skip] {src}: no extractable blocks")
    print(f"[ok] total curated blocks: {total_blocks}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
