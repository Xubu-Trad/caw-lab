#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class LayerEntry:
    riddle_num: int
    riddle_slug: str
    # For grouped layout: Lxx numeric; for flat layout: layer numeric (e.g., 000)
    layer_num: int
    layer_id: str  # e.g. "L02" or "R1-010"
    title: str
    relpath: str   # posix, trailing "/"


_RIDDLE_DIR_RE = re.compile(r"^R(?P<rnum>\d+)[_-](?P<slug>.+)$")
_GROUP_LAYER_RE = re.compile(r"^L(?P<lnum>\d{1,3})(?:__|[_-])(?P<rest>.*)$")
_FLAT_LAYER_RE = re.compile(r"^R(?P<rnum>\d+)[_-](?P<lnum>\d{3})(?:[_-](?P<rest>.*))?$")


def _posix_rel(p: Path, root: Path) -> str:
    return p.relative_to(root).as_posix().rstrip("/") + "/"


def parse_riddle_dir(name: str) -> Optional[tuple[int, str]]:
    """
    >>> parse_riddle_dir("R2_zrUfKaKV")
    (2, 'zrUfKaKV')
    >>> parse_riddle_dir("R1-58bZfQ1")
    (1, '58bZfQ1')
    >>> parse_riddle_dir("layers")
    """
    m = _RIDDLE_DIR_RE.match(name)
    if not m:
        return None
    return int(m.group("rnum")), m.group("slug")


def parse_group_layer_dir(name: str) -> Optional[tuple[int, str]]:
    """
    >>> parse_group_layer_dir("L02__zru_merge_receipts_20260215T033000Z")
    (2, 'zru_merge_receipts_20260215T033000Z')
    >>> parse_group_layer_dir("L1__x")
    (1, 'x')
    >>> parse_group_layer_dir("R1-000_yale_oldking")
    """
    m = _GROUP_LAYER_RE.match(name)
    if not m:
        return None
    return int(m.group("lnum")), m.group("rest")


def parse_flat_layer_dir(name: str) -> Optional[tuple[int, int, str]]:
    """
    >>> parse_flat_layer_dir("R1-010_friderici_poem_coords")
    (1, 10, 'friderici_poem_coords')
    >>> parse_flat_layer_dir("R2_000")
    (2, 0, '')
    >>> parse_flat_layer_dir("R2_zrUfKaKV")
    """
    m = _FLAT_LAYER_RE.match(name)
    if not m:
        return None
    rnum = int(m.group("rnum"))
    lnum = int(m.group("lnum"))
    rest = (m.group("rest") or "").strip()
    return rnum, lnum, rest


def _read_title(layer_dir: Path) -> str:
    for fn in ("SUMMARY.md", "README.md"):
        p = layer_dir / fn
        if not p.is_file():
            continue
        txt = p.read_text(encoding="utf-8", errors="replace")
        for line in txt.splitlines():
            line = line.rstrip()
            if line.startswith("# "):
                return line[2:].strip()
        for line in txt.splitlines():
            s = line.strip()
            if s:
                return s.lstrip("#").strip()
    return ""


def _humanize(rest: str) -> str:
    s = rest.strip().strip("_-")
    s = s.replace("__", "_")
    s = s.replace("-", " ")
    s = re.sub(r"_+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _collect_grouped(layers_dir: Path, root: Path) -> list[LayerEntry]:
    out: list[LayerEntry] = []
    for rdir in sorted([p for p in layers_dir.iterdir() if p.is_dir()], key=lambda p: p.name):
        pr = parse_riddle_dir(rdir.name)
        if not pr:
            continue
        rnum, rslug = pr
        # only immediate children that look like Lxx__...
        for ldir in sorted([p for p in rdir.iterdir() if p.is_dir()], key=lambda p: p.name):
            pl = parse_group_layer_dir(ldir.name)
            if not pl:
                continue
            lnum, rest = pl
            layer_id = f"L{lnum:02d}"
            title = _read_title(ldir) or _humanize(rest) or ldir.name
            out.append(
                LayerEntry(
                    riddle_num=rnum,
                    riddle_slug=rslug,
                    layer_num=lnum,
                    layer_id=layer_id,
                    title=title,
                    relpath=_posix_rel(ldir, root),
                )
            )
    return out


def _collect_flat(layers_dir: Path, root: Path) -> list[LayerEntry]:
    out: list[LayerEntry] = []
    for ldir in sorted([p for p in layers_dir.iterdir() if p.is_dir()], key=lambda p: p.name):
        pf = parse_flat_layer_dir(ldir.name)
        if not pf:
            continue
        rnum, lnum, rest = pf
        layer_id = f"R{rnum}-{lnum:03d}"
        title = _read_title(ldir) or _humanize(rest) or ldir.name
        out.append(
            LayerEntry(
                riddle_num=rnum,
                riddle_slug="",
                layer_num=lnum,
                layer_id=layer_id,
                title=title,
                relpath=_posix_rel(ldir, root),
            )
        )
    return out


def collect_layers(root: Path) -> list[LayerEntry]:
    layers_dir = root / "layers"
    assert layers_dir.is_dir(), f"missing layers/ directory at {layers_dir}"

    grouped = _collect_grouped(layers_dir, root)
    flat = _collect_flat(layers_dir, root)

    # de-dupe by relpath (in case someone has mixed layouts)
    seen: set[str] = set()
    all_entries: list[LayerEntry] = []
    for e in grouped + flat:
        if e.relpath in seen:
            continue
        seen.add(e.relpath)
        all_entries.append(e)

    all_entries.sort(key=lambda e: (e.riddle_num, e.layer_num, e.relpath))
    return all_entries


def render_index(root: Path, entries: list[LayerEntry]) -> str:
    assert entries, "no layer directories found under layers/"

    # Prefer a non-empty slug for each riddle if present anywhere
    slug_by_riddle: dict[int, str] = {}
    for e in entries:
        if e.riddle_slug and not slug_by_riddle.get(e.riddle_num):
            slug_by_riddle[e.riddle_num] = e.riddle_slug

    lines: list[str] = []
    lines.append("# LAYER INDEX (CANON TIMELINE)")
    lines.append("")
    lines.append("> GENERATED from the current `layers/` tree via `scripts/gen_layer_index.py`.")
    lines.append("> Do not edit by hand — change layer folders (and their `SUMMARY.md`) then re-run the generator.")
    lines.append("")

    # Per-riddle sections
    current_r: Optional[int] = None
    for e in entries:
        if current_r != e.riddle_num:
            current_r = e.riddle_num
            slug = slug_by_riddle.get(current_r, "")
            if slug:
                lines.append(f"## R{current_r} ({slug})")
            else:
                lines.append(f"## R{current_r}")
            lines.append("")
        lines.append(f"- **{e.layer_id}**: {e.title} — [{e.relpath}]({e.relpath})")
    lines.append("")

    # Optional docs links (only include what exists)
    docs_candidates = [
        "docs/RIDDLE_PROGRESS.md",
        "docs/CANON_RULES.md",
        "docs/REPRO_GUIDE.md",
        "docs/README.md",
    ]
    docs_present = [p for p in docs_candidates if (root / p).is_file()]
    if docs_present:
        lines.append("## Riddle progress")
        lines.append("")
        for p in docs_present:
            lines.append(f"- [{p}]({p})")
        lines.append("")

    # Chronological index (deterministic sort already applied)
    lines.append("## Layer index (chronological)")
    lines.append("")
    for e in entries:
        lines.append(f"- [{e.relpath}]({e.relpath})")
    lines.append("")

    return "\n".join(lines)


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Generate LAYER_INDEX.md from layers/ tree.")
    ap.add_argument("--repo-root", default=None, help="Repo root (defaults to parent of scripts/).")
    ap.add_argument("--out", default="LAYER_INDEX.md", help="Output markdown path (relative to repo root).")
    ap.add_argument("--check", action="store_true", help="Fail if output differs from generated content.")
    ap.add_argument("--write", action="store_true", help="Write output file (default behavior if neither --check nor stdout).")
    args = ap.parse_args(argv)

    root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[1]
    entries = collect_layers(root)
    content = render_index(root, entries)

    outp = (root / args.out).resolve()

    if args.check:
        if not outp.is_file():
            print(f"[FAIL] missing {args.out}. Run: python3 scripts/gen_layer_index.py --write", file=sys.stderr)
            return 2
        cur = outp.read_text(encoding="utf-8", errors="replace")
        if cur != content:
            print(f"[FAIL] {args.out} is out of date. Run: python3 scripts/gen_layer_index.py --write", file=sys.stderr)
            return 1
        print(f"[ok] {args.out} matches generated output")
        return 0

    # default: write (or explicit --write)
    outp.write_text(content, encoding="utf-8")
    print(f"[ok] wrote {outp.relative_to(root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
