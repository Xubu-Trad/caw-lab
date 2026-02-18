#!/usr/bin/env python3
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable, Iterator, Optional, Tuple, List

PLACEHOLDER_PATTERNS = [
    r"\bscaffold\b",
    r"\bplaceholder\b",
    r"Put the layer narrative here",
    r"Replace with real receipts",
    r"\bTODO\b",
]

OPSEC_PATTERNS = [
    r"/home/[A-Za-z0-9._-]+",      # unix home path
    r"\\Users\\[^\\\s]+",          # windows user dir
    r"DESKTOP-[A-Z0-9]+",          # hostnames that leak
]

REQUIRED_FILES = [
    "SUMMARY.md",
    "REPRODUCE.md",
    "EVIDENCE/README.md",
]

@dataclasses.dataclass(frozen=True)
class Issue:
    layer: str
    severity: str   # "ERROR" | "WARN" | "INFO"
    kind: str
    detail: str
    path: str = ""

def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _parse_sha256_line(line: str) -> Optional[Tuple[str, str]]:
    """
    Accepts common sha256sum formats:
      <hash>  <path>
      <hash> *<path>

    >>> _parse_sha256_line("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  foo.txt")
    ('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'foo.txt')
    >>> _parse_sha256_line("notahash  foo.txt") is None
    True
    """
    s = line.strip()
    if not s or s.startswith("#"):
        return None
    m = re.match(r"^([0-9a-fA-F]{64})\s+[* ]?(.*\S)\s*$", s)
    if not m:
        return None
    return (m.group(1).lower(), m.group(2))

def _read_text(p: Path, limit: int = 200_000) -> str:
    # bounded read to avoid huge files
    b = p.read_bytes()
    if len(b) > limit:
        b = b[:limit]
    try:
        return b.decode("utf-8", errors="replace")
    except Exception:
        return b.decode("latin-1", errors="replace")

def _find_layers(repo_root: Path) -> List[Path]:
    layers_dir = repo_root / "layers"
    if not layers_dir.is_dir():
        return []
    # only first-level layer dirs
    out: List[Path] = []
    for p in sorted(layers_dir.iterdir()):
        if p.is_dir() and not p.name.startswith("."):
            out.append(p)
    return out

def _extract_status(summary_text: str) -> str:
    # Accept: "Status: <anything>"
    m = re.search(r"(?im)^\s*Status:\s*(.+?)\s*$", summary_text)
    return (m.group(1).strip() if m else "")

def _has_anchor(summary_text: str) -> bool:
    # Minimal: heading "Anchor" must exist OR a known anchor token exists.
    if re.search(r"(?im)^\s*##\s*Anchor\b", summary_text):
        return True
    if "58bZfQ1" in summary_text or "zrUfKaKV" in summary_text:
        return True
    return False

def audit_repo(repo_root: Path, strict: bool, verify_hashes: bool) -> Tuple[List[Issue], List[dict]]:
    issues: List[Issue] = []
    rows: List[dict] = []

    layers = _find_layers(repo_root)
    if not layers:
        issues.append(Issue(layer="", severity="ERROR", kind="NO_LAYERS_DIR", detail="missing layers/ directory", path=str(repo_root)))
        return issues, rows

    # scan per layer
    for layer_dir in layers:
        lname = layer_dir.name

        missing = []
        empty = []
        placeholders = 0
        opsec_hits = 0
        hash_fail = 0
        hash_checked = 0

        # required files
        for rf in REQUIRED_FILES:
            p = layer_dir / rf
            if not p.exists():
                missing.append(rf)
            else:
                if p.is_file() and p.stat().st_size == 0:
                    empty.append(rf)

        # scan text files for placeholders + opsec
        for md in list(layer_dir.rglob("*.md")):
            if not md.is_file():
                continue
            txt = _read_text(md)
            for pat in PLACEHOLDER_PATTERNS:
                if re.search(pat, txt, flags=re.IGNORECASE):
                    placeholders += 1
                    break
            for pat in OPSEC_PATTERNS:
                if re.search(pat, txt):
                    opsec_hits += 1
                    issues.append(Issue(lname, "ERROR", "OPSEC_LEAK", f"pattern hit {pat}", str(md.relative_to(repo_root))))

        # summary checks
        summary_p = layer_dir / "SUMMARY.md"
        status = ""
        if summary_p.exists() and summary_p.is_file():
            stxt = _read_text(summary_p)
            status = _extract_status(stxt)
            if not status:
                issues.append(Issue(lname, "WARN" if not strict else "ERROR", "MISSING_STATUS", "SUMMARY.md missing `Status:` line", str(summary_p.relative_to(repo_root))))
            if not _has_anchor(stxt):
                issues.append(Issue(lname, "WARN" if not strict else "ERROR", "MISSING_ANCHOR", "SUMMARY.md missing Anchor section/token", str(summary_p.relative_to(repo_root))))
        else:
            issues.append(Issue(lname, "ERROR", "MISSING_SUMMARY", "SUMMARY.md not found", str(summary_p.relative_to(repo_root))))

        # verify hashes if present
        if verify_hashes:
            for mf in layer_dir.rglob("*.sha256"):
                if not mf.is_file():
                    continue
                mtxt = _read_text(mf)
                for line in mtxt.splitlines():
                    parsed = _parse_sha256_line(line)
                    if not parsed:
                        continue
                    exp, rel = parsed
                    hash_checked += 1
                    rel = rel.strip()
                    if os.path.isabs(rel):
                        hash_fail += 1
                        issues.append(Issue(lname, "ERROR", "ABS_PATH_IN_MANIFEST", f"absolute path in {mf.name}: {rel}", str(mf.relative_to(repo_root))))
                        continue
                    target = (mf.parent / rel).resolve()
                    try:
                        target.relative_to(repo_root.resolve())
                    except Exception:
                        hash_fail += 1
                        issues.append(Issue(lname, "ERROR", "MANIFEST_PATH_ESCAPE", f"path escapes repo root: {rel}", str(mf.relative_to(repo_root))))
                        continue
                    if not target.exists() or not target.is_file():
                        hash_fail += 1
                        issues.append(Issue(lname, "ERROR", "MISSING_MANIFEST_FILE", f"missing referenced file: {rel}", str(mf.relative_to(repo_root))))
                        continue
                    got = _sha256_file(target)
                    if got != exp:
                        hash_fail += 1
                        issues.append(Issue(lname, "ERROR", "HASH_MISMATCH", f"{rel}: expected {exp} got {got}", str(mf.relative_to(repo_root))))

        # record missing/empty
        for m in missing:
            issues.append(Issue(lname, "ERROR", "MISSING_REQUIRED", f"missing {m}", str((layer_dir / m).relative_to(repo_root))))
        for e in empty:
            issues.append(Issue(lname, "WARN" if not strict else "ERROR", "EMPTY_FILE", f"empty {e}", str((layer_dir / e).relative_to(repo_root))))

        # placeholder policy
        if placeholders:
            sev = "WARN" if not strict else "ERROR"
            issues.append(Issue(lname, sev, "PLACEHOLDER_TEXT", f"{placeholders} md file(s) contain placeholder/scaffold/TODO text", str(layer_dir.relative_to(repo_root))))

        rows.append({
            "layer": lname,
            "status": status,
            "missing_required": len(missing),
            "empty_required": len(empty),
            "placeholders": placeholders,
            "opsec_hits": opsec_hits,
            "hash_checked": hash_checked,
            "hash_fail": hash_fail,
        })

    return issues, rows

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path.cwd(), help="repo root (default: cwd)")
    ap.add_argument("--out", type=Path, default=Path("OUT/layer_audit"), help="output dir")
    ap.add_argument("--strict", action="store_true", help="treat placeholders/empties as errors (good for public)")
    ap.add_argument("--no-hash", action="store_true", help="skip *.sha256 verification")
    args = ap.parse_args()

    repo = args.repo.resolve()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    issues, rows = audit_repo(repo, strict=args.strict, verify_hashes=(not args.no_hash))

    # write machine outputs
    (out / "issues.jsonl").write_text("\n".join(json.dumps(dataclasses.asdict(i), sort_keys=True) for i in issues) + ("\n" if issues else ""), encoding="utf-8")
    (out / "layers.json").write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # TSV summary
    tsv = ["layer\tstatus\tmissing_required\tempty_required\tplaceholders\topsec_hits\thash_checked\thash_fail"]
    for r in rows:
        tsv.append(f"{r['layer']}\t{r['status']}\t{r['missing_required']}\t{r['empty_required']}\t{r['placeholders']}\t{r['opsec_hits']}\t{r['hash_checked']}\t{r['hash_fail']}")
    (out / "layers.tsv").write_text("\n".join(tsv) + "\n", encoding="utf-8")

    # Human report
    sev = Counter(i.severity for i in issues)
    status_counts = Counter((r.get("status") or "(missing)") for r in rows)

    lines = []
    lines.append(f"# Layer audit report")
    lines.append("")
    lines.append(f"Repo: `{repo}`")
    lines.append(f"Strict: `{args.strict}`  |  Hash verify: `{not args.no_hash}`")
    lines.append("")
    lines.append("## Issue counts")
    lines.append("")
    lines.append(f"- ERROR: {sev.get('ERROR',0)}")
    lines.append(f"- WARN:  {sev.get('WARN',0)}")
    lines.append(f"- INFO:  {sev.get('INFO',0)}")
    lines.append("")
    lines.append("## Status distribution (from SUMMARY.md `Status:` lines)")
    lines.append("")
    for k, v in sorted(status_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Top issues (first 200)")
    lines.append("")
    for i in issues[:200]:
        p = f" ({i.path})" if i.path else ""
        lines.append(f"- **{i.severity}** `{i.layer}` {i.kind}: {i.detail}{p}")
    lines.append("")

    (out / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")

    # exit nonzero if strict and any errors, else if any errors
    has_err = any(i.severity == "ERROR" for i in issues)
    return 1 if has_err else 0

if __name__ == "__main__":
    raise SystemExit(main())
