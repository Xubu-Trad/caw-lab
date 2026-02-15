#!/usr/bin/env python3
"""Build docs/PRIVATE_MATRIX.md from ledger/attempts.jsonl."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HEADER = """# Private Attempt Matrix

Generated from `ledger/attempts.jsonl` by `tools/matrix_build.py`.

| file | sha256 | lines | first_line |
|---|---|---:|---|
"""


def load_rows(ledger_path: Path) -> list[dict]:
    if not ledger_path.exists():
        return []
    rows: list[dict] = []
    for idx, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON in {ledger_path}:{idx}: {exc}")
    return rows


def render(rows: list[dict]) -> str:
    out = [HEADER]
    for row in rows:
        file = str(row.get("file", "")).replace("|", "\\|")
        sha = str(row.get("sha256", ""))
        lines = str(row.get("lines", ""))
        first = str(row.get("first_line", "")).replace("|", "\\|")
        out.append(f"| {file} | `{sha}` | {lines} | {first} |\n")
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", default="ledger/attempts.jsonl")
    parser.add_argument("--out", default="docs/PRIVATE_MATRIX.md")
    parser.add_argument("--check", action="store_true", help="Fail if output is not up-to-date")
    args = parser.parse_args()

    rendered = render(load_rows(Path(args.ledger)))
    out_path = Path(args.out)

    if args.check:
        current = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
        if current != rendered:
            raise SystemExit(f"{out_path} is stale. Rebuild with tools/matrix_build.py")
        print(f"{out_path} is up to date.")
        return

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
