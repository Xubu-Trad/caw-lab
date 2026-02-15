#!/usr/bin/env python3
"""Build docs/ATTEMPT_MATRIX.md from ledger/attempts_full.jsonl.

Doctest:
>>> validate_status("PASS")
'PASS'
>>> validate_status("PLACEHOLDER")
'PLACEHOLDER'
>>> esc_md("a|b\\nc")     # actual newline inside the string
'a\\\\|b c'
>>> esc_md("a|b\\\\nc")   # literal backslash + n
'a\\\\|b\\\\\\\\nc'
"""
from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Literal

Status = Literal["PASS", "FAIL", "PLACEHOLDER"]

log = logging.getLogger("matrix_full_build")

REQUIRED_KEYS = [
    "attempt_id","layer_id","status","claim","intent","source_artifact","transform_tool",
    "command_line","input_sha256","output_sha256","output_paths","expected_output",
    "what_failed","notes","next_tests"
]

def validate_status(x: str) -> Status:
    if x not in ("PASS", "FAIL", "PLACEHOLDER"):
        raise ValueError(f"invalid status: {x}")
    return x  # type: ignore[return-value]

def esc_md(v: Any) -> str:
    # Deterministic markdown escaping.
    s = str(v)
    s = s.replace("\\", "\\\\")   # escape backslashes first
    s = s.replace("|", "\\|")
    s = s.replace("\n", " ")
    return s.strip()

@dataclass(frozen=True)
class Row:
    attempt_id: str
    layer_id: str
    status: Status
    claim: str
    intent: str
    source_artifact: str
    transform_tool: str
    command_line: str
    input_sha256: str
    output_sha256: str
    output_paths: List[str]
    expected_output: str
    what_failed: str
    notes: str
    next_tests: str

def load_rows(path: Path) -> List[Row]:
    assert path.exists(), f"missing ledger file: {path}"
    raw = path.read_text(encoding="utf-8", errors="strict")
    lines = [ln for ln in raw.splitlines() if ln.strip()]
    assert lines, f"ledger empty: {path}"

    rows: List[Row] = []
    for i, line in enumerate(lines, 1):
        obj = json.loads(line)
        for k in REQUIRED_KEYS:
            if k not in obj:
                raise SystemExit(f"[fail] missing key {k} at {path}:{i}")

        rows.append(Row(
            attempt_id=str(obj["attempt_id"]),
            layer_id=str(obj["layer_id"]),
            status=validate_status(str(obj["status"])),
            claim=str(obj["claim"]),
            intent=str(obj["intent"]),
            source_artifact=str(obj["source_artifact"]),
            transform_tool=str(obj["transform_tool"]),
            command_line=str(obj["command_line"]),
            input_sha256=str(obj["input_sha256"]),
            output_sha256=str(obj["output_sha256"]),
            output_paths=list(obj["output_paths"]),
            expected_output=str(obj["expected_output"]),
            what_failed=str(obj["what_failed"]),
            notes=str(obj["notes"]),
            next_tests=str(obj["next_tests"]),
        ))
    return rows

def render(rows: List[Row]) -> str:
    out: List[str] = []
    out.append("# Attempt Matrix (All Attempts)\n\n")
    out.append("Generated from `ledger/attempts_full.jsonl`.\n\n")
    out.append("| LayerID | AttemptID | Status | Claim | Intent | Source | Tool/Stub | Cmd | InSHA256 | OutSHA256 | Outputs |\n")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|\n")

    for r in sorted(rows, key=lambda x: (x.layer_id, x.attempt_id)):
        out.append(
            "| {layer} | {aid} | {status} | {claim} | {intent} | {src} | {tool} | {cmd} | `{insha}` | `{outsha}` | {outs} |\n".format(
                layer=esc_md(r.layer_id),
                aid=esc_md(r.attempt_id),
                status=esc_md(r.status),
                claim=esc_md(r.claim),
                intent=esc_md(r.intent),
                src=esc_md(r.source_artifact),
                tool=esc_md(r.transform_tool),
                cmd=esc_md(r.command_line),
                insha=esc_md(r.input_sha256),
                outsha=esc_md(r.output_sha256),
                outs=esc_md(",".join(r.output_paths)),
            )
        )
    return "".join(out)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", default="ledger/attempts_full.jsonl")
    ap.add_argument("--out", default="docs/ATTEMPT_MATRIX.md")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(level=(logging.DEBUG if args.verbose else logging.INFO),
                        format="%(levelname)s:%(name)s:%(message)s")

    ledger = Path(args.ledger)
    out = Path(args.out)

    rows = load_rows(ledger)
    rendered = render(rows)

    if args.check:
        current = out.read_text(encoding="utf-8") if out.exists() else ""
        if current != rendered:
            raise SystemExit(f"[fail] {out} is stale. Rebuild.")
        print(f"[ok] {out} is up to date.")
        return

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"[ok] wrote {out} rows={len(rows)}")

if __name__ == "__main__":
    main()
