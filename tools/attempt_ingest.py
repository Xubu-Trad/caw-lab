#!/usr/bin/env python3
"""Ingest text attempt logs from history/ into ledger/attempts.jsonl.

- Scans `history/*.txt`
- Emits one JSON object per file with basic metadata
- Optionally updates `history/MANIFEST.sha256`
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def ingest(history_dir: Path, ledger_path: Path, manifest_path: Path, update_manifest: bool) -> int:
    txt_files = sorted(p for p in history_dir.glob("*.txt") if p.is_file())

    records = []
    manifest_lines = []

    for path in txt_files:
        raw = path.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        lines = text.splitlines()
        digest = sha256_bytes(raw)

        records.append(
            {
                "file": str(path.as_posix()),
                "sha256": digest,
                "bytes": len(raw),
                "lines": len(lines),
                "first_line": (lines[0][:160] if lines else ""),
            }
        )
        manifest_lines.append(f"{digest}  {path.as_posix()}")

    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("w", encoding="utf-8", newline="\n") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    if update_manifest:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text("\n".join(manifest_lines) + ("\n" if manifest_lines else ""), encoding="utf-8")

    return len(records)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history", default="history", help="History directory (default: history)")
    parser.add_argument("--ledger", default="ledger/attempts.jsonl", help="Output JSONL ledger")
    parser.add_argument("--manifest", default="history/MANIFEST.sha256", help="Manifest file path")
    parser.add_argument(
        "--no-manifest-update",
        action="store_true",
        help="Do not rewrite MANIFEST.sha256",
    )

    args = parser.parse_args()

    count = ingest(
        history_dir=Path(args.history),
        ledger_path=Path(args.ledger),
        manifest_path=Path(args.manifest),
        update_manifest=not args.no_manifest_update,
    )
    print(f"Ingested {count} history log(s).")


if __name__ == "__main__":
    main()
