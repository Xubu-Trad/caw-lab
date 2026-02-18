#!/usr/bin/env python3
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

STATUS_RE = re.compile(r"^Status:\s*(.+?)\s*$", re.MULTILINE)
MD_LINK_RE = re.compile(r"\]\(([^)]+)\)")  # markdown links: ](path)

@dataclasses.dataclass(frozen=True)
class Issue:
    level: str   # ERROR/WARN/INFO
    layer: str
    code: str
    msg: str
    path: Path

def _sha256_file(p: Path) -> str:
    assert p.is_file(), f"not a file: {p}"
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def _parse_sha256_line(line: str) -> Optional[Tuple[str, str]]:
    """
    Accepts: "<hex>  <path>" or "<hex> *<path>"

    >>> _parse_sha256_line("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  foo.txt")
    ('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'foo.txt')
    >>> _parse_sha256_line("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 *bar.bin")
    ('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'bar.bin')
    >>> _parse_sha256_line("notahash  foo.txt") is None
    True
    """
    s = line.strip()
    if not s or s.startswith("#"):
        return None
    m = re.match(r"^([0-9a-fA-F]{64})\s+\*?(.+)$", s)
    if not m:
        return None
    return m.group(1).lower(), m.group(2).strip()

def _read_text(p: Path) -> str:
    assert p.is_file(), f"missing file: {p}"
    return p.read_text("utf-8", errors="replace")

def _read_status(summary_md: Path) -> Optional[str]:
    txt = _read_text(summary_md)
    m = STATUS_RE.search(txt)
    return m.group(1).strip() if m else None

def _find_layers(repo: Path) -> List[Path]:
    layers = repo / "layers"
    assert layers.is_dir(), f"missing layers/: {layers}"
    return sorted([p for p in layers.iterdir() if p.is_dir()])

def _evidence_files(evd: Path) -> List[Path]:
    if not evd.is_dir():
        return []
    return sorted([p for p in evd.rglob("*") if p.is_file()])

def _manifest(evd: Path) -> Optional[Path]:
    m = evd / "MANIFEST.sha256"
    return m if m.is_file() else None

def _manifest_entries(mp: Path) -> Dict[str, str]:
    """
    Returns map: relpath -> sha256
    """
    entries: Dict[str, str] = {}
    for line in _read_text(mp).splitlines():
        parsed = _parse_sha256_line(line)
        if not parsed:
            continue
        h, rel = parsed
        entries[rel] = h
    return entries

def _extract_md_paths(txt: str) -> List[str]:
    """
    Extracts markdown link targets.

    >>> _extract_md_paths("See [x](EVIDENCE/foo.bin) and [y](http://example.com).")
    ['EVIDENCE/foo.bin', 'http://example.com']
    """
    return [m.group(1).strip() for m in MD_LINK_RE.finditer(txt)]

def _is_local_rel_path(s: str) -> bool:
    if s.startswith(("http://", "https://", "ipfs://")):
        return False
    if s.startswith("#"):
        return False
    return True

def verify_repo(repo: Path, strict: bool, verbose: bool = False) -> Tuple[List[Issue], List[str]]:
    """
    Returns (issues, per-layer state lines).
    """
    assert repo.is_dir(), f"missing repo: {repo}"
    issues: List[Issue] = []
    state_lines: List[str] = []

    for layer_dir in _find_layers(repo):
        layer = layer_dir.name
        summary = layer_dir / "SUMMARY.md"
        reproduce = layer_dir / "REPRODUCE.md"
        evd = layer_dir / "EVIDENCE"
        not_exec = evd / "NOT_EXECUTED.md"

        if not summary.is_file():
            issues.append(Issue("ERROR", layer, "MISSING_SUMMARY", "SUMMARY.md missing", summary))
            continue

        status = _read_status(summary)

        mp = _manifest(evd) if evd.is_dir() else None
        has_not_exec = not_exec.is_file()

        # Determine whether evidence artifacts exist (excluding README/NOT_EXECUTED/manifests)
        artifacts: List[Path] = []
        for f in _evidence_files(evd):
            name = f.name
            if name in ("README.md", "NOT_EXECUTED.md", "MANIFEST.sha256"):
                continue
            if name.endswith(".sha256"):
                continue
            artifacts.append(f)

        # Strict Evidence State enforcement for public canon
        if strict:
            if has_not_exec:
                if artifacts:
                    issues.append(Issue(
                        "ERROR", layer, "STATE_CONFLICT",
                        f"NOT_EXECUTED.md present but found {len(artifacts)} artifact(s) in EVIDENCE/",
                        not_exec
                    ))
                state_lines.append(f"- `{layer}` STATE=NOT_EXECUTED")
            else:
                if mp is None:
                    issues.append(Issue(
                        "ERROR", layer, "MISSING_MANIFEST",
                        "No NOT_EXECUTED.md and no EVIDENCE/MANIFEST.sha256; layer must be explicitly NOT_EXECUTED or receipted",
                        evd / "MANIFEST.sha256"
                    ))
                    state_lines.append(f"- `{layer}` STATE=UNKNOWN(no NOT_EXECUTED, no MANIFEST)")
                else:
                    if not artifacts:
                        issues.append(Issue(
                            "ERROR", layer, "EMPTY_EVIDENCE",
                            "MANIFEST.sha256 exists but no artifacts found in EVIDENCE/",
                            evd
                        ))
                        state_lines.append(f"- `{layer}` STATE=RECEIPTED(empty artifacts)")
                    else:
                        state_lines.append(f"- `{layer}` STATE=RECEIPTED({len(artifacts)} artifacts)")
        else:
            # Non-strict: just report state
            if has_not_exec:
                state_lines.append(f"- `{layer}` STATE=NOT_EXECUTED")
            elif mp is None and not artifacts:
                state_lines.append(f"- `{layer}` STATE=EMPTY")
            else:
                state_lines.append(f"- `{layer}` STATE=HAS_EVIDENCE(manifest={mp is not None}, artifacts={len(artifacts)})")

        # Verify manifest hashes if present
        if mp is not None:
            entries = _manifest_entries(mp)
            for rel, want in entries.items():
                fp = (mp.parent / rel)
                if not fp.exists():
                    issues.append(Issue("ERROR" if strict else "WARN", layer, "HASH_MISSING_FILE",
                                        f"manifest references missing file: {rel}", mp))
                    continue
                if fp.is_dir():
                    continue
                got = _sha256_file(fp)
                if got != want:
                    issues.append(Issue("ERROR", layer, "HASH_MISMATCH",
                                        f"sha256 mismatch for {rel}: got {got} want {want}", mp))

        # Verify markdown links in SUMMARY/REPRODUCE to local files exist; if under EVIDENCE, require manifest in strict.
        for doc in (summary, reproduce):
            if not doc.is_file():
                continue
            txt = _read_text(doc)
            for target in _extract_md_paths(txt):
                if not _is_local_rel_path(target):
                    continue
                # normalize layer-relative references
                # allow "EVIDENCE/x" or "layers/<layer>/EVIDENCE/x"
                if target.startswith("layers/"):
                    relp = Path(target)
                else:
                    relp = (layer_dir / target).relative_to(repo)
                abs_path = repo / relp
                if not abs_path.exists():
                    issues.append(Issue("ERROR" if strict else "WARN", layer, "BROKEN_LINK",
                                        f"broken link target: {target}", doc))
                    continue
                # if it points into EVIDENCE/, enforce it appears in manifest when strict and no NOT_EXECUTED
                if strict and ("EVIDENCE" in relp.parts) and (mp is not None):
                    rel_to_evd = str(Path(*relp.parts[relp.parts.index("EVIDENCE")+1:]))
                    if rel_to_evd not in _manifest_entries(mp) and abs_path.is_file():
                        issues.append(Issue("ERROR", layer, "UNHASHED_EVIDENCE",
                                            f"linked evidence file not in MANIFEST.sha256: {rel_to_evd}", doc))

        if verbose:
            _ = status  # keep for debugging later if needed

    return issues, state_lines

def write_report(out_dir: Path, repo: Path, strict: bool, issues: Sequence[Issue], states: Sequence[str]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    md = out_dir / "RECEIPTS_REPORT_V2.md"

    counts: Dict[str, int] = {"ERROR": 0, "WARN": 0, "INFO": 0}
    for i in issues:
        counts[i.level] = counts.get(i.level, 0) + 1

    lines: List[str] = []
    lines.append("# Layer receipts verification (v2)\n\n")
    lines.append(f"Repo: `{repo}`\n\n")
    lines.append(f"Strict: `{strict}`\n\n")
    lines.append("## Issue counts\n\n")
    lines.append(f"- ERROR: {counts.get('ERROR',0)}\n")
    lines.append(f"- WARN:  {counts.get('WARN',0)}\n")
    lines.append(f"- INFO:  {counts.get('INFO',0)}\n\n")

    lines.append("## Layer states\n\n")
    lines.extend([s + "\n" for s in states])
    lines.append("\n## Findings\n\n")
    for i in issues:
        rel = i.path.relative_to(repo) if i.path.is_absolute() else i.path
        lines.append(f"- **{i.level}** `{i.layer}` {i.code}: {i.msg} ({rel})\n")

    md.write_text("".join(lines), encoding="utf-8")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    out = Path(args.out).resolve()

    issues, states = verify_repo(repo, strict=args.strict, verbose=args.verbose)
    write_report(out, repo, args.strict, issues, states)

    if args.strict and any(i.level == "ERROR" for i in issues):
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
