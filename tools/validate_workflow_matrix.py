#!/usr/bin/env python3
"""
Validate docs/workflow_matrix.tsv.

Checks:
- required columns exist
- source_path exists and sha256 matches
- anchor (if present) occurs in source bytes
- script_path (if present) exists

Doctests:
>>> _is_hex64("a"*64)
True
>>> _is_hex64("nope")
False
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import logging
from pathlib import Path
from typing import Iterable

LOG = logging.getLogger("validate_workflow_matrix")

REQ_COLS = (
    "workflow_id",
    "bundle_ts",
    "source_path",
    "source_sha256",
    "anchor",
    "script_path",
    "status",
)

def _is_hex64(s: str) -> bool:
    if len(s) != 64:
        return False
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

def _sha256_file(p: Path, *, chunk: int = 1024 * 1024) -> str:
    assert p.is_file(), f"not a file: {p}"
    h = hashlib.sha256()
    with p.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def _read_tsv(p: Path) -> Iterable[dict[str, str]]:
    assert p.is_file(), f"missing matrix: {p}"
    with p.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f, delimiter="\t")
        assert r.fieldnames is not None, "missing header row"
        missing = [c for c in REQ_COLS if c not in r.fieldnames]
        assert not missing, f"matrix missing columns: {missing}"
        yield from r

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    ap.add_argument("--matrix", default="docs/workflow_matrix.tsv")
    ap.add_argument("--max-bytes", type=int, default=2_097_152)
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    root = Path(args.root).resolve()
    matrix = (root / args.matrix).resolve()
    assert (root / ".git").exists(), f"not a git repo root: {root}"

    failures = 0
    for i, row in enumerate(_read_tsv(matrix), start=2):
        sp = (root / row["source_path"]).resolve()
        sha = row["source_sha256"].strip()
        anchor = row["anchor"].strip()
        script = row["script_path"].strip()

        if not sp.is_file():
            LOG.error("L%d missing source_path: %s", i, row["source_path"])
            failures += 1
            continue

        if sha and not _is_hex64(sha):
            LOG.error("L%d bad sha256 format: %r", i, sha)
            failures += 1
            continue

        got = _sha256_file(sp)
        if sha and got != sha:
            LOG.error("L%d sha mismatch: %s want=%s got=%s", i, row["source_path"], sha, got)
            failures += 1

        if anchor:
            b = sp.read_bytes()
            if len(b) > args.max_bytes:
                LOG.error("L%d anchor-check blocked (file too big): %s", i, row["source_path"])
                failures += 1
            else:
                if anchor.encode("utf-8", "ignore") not in b:
                    LOG.error("L%d anchor not found in %s", i, row["source_path"])
                    failures += 1

        if script:
            sc = (root / script).resolve()
            if not sc.exists():
                LOG.error("L%d missing script_path: %s", i, script)
                failures += 1

    if failures:
        LOG.error("FAIL: %d failures", failures)
        return 2
    LOG.info("OK: matrix validated: %s", matrix.relative_to(root))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
