#!/usr/bin/env python3
"""
Generate/refresh docs + layer scaffolds for the CAW riddle progress pack.

Usage:
  python3 scripts/sync_riddle_report.py --apply
  python3 -m doctest -v scripts/sync_riddle_report.py
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple
import argparse
import logging

LOG = logging.getLogger("sync_riddle_report")

DOC_BEGIN = "<!-- RIDDLE_PROGRESS_BEGIN -->"
DOC_END   = "<!-- RIDDLE_PROGRESS_END -->"

# Canonical anchors (receipts-first)
CAW_TOKEN_CONTRACT = "0xf3b9569f82b18aef890de263b84189bd33ebe452"
CAW_DEPLOYER       = "0x36B59455AfeEdf0866FE6E775FE7651bbBe3e005"
INTERMEDIARY       = "0x81A0daaab45dBbcE68b11E7AEdDd6A0D1970bdeA"
SHIB_DEPLOYER      = "0xB8f226dDb7bC672E27dffB67e4adAbFa8c0dFA08"

FUNDING_TX_IN      = "0xb5b81a63c957fcc33469d59f9c969e860d24574bb72d8b2fc482c7232cb13062"
FUNDING_TX_OUT     = "0xbfed9c9fe98cf7705b6668afbe9f01c81310f062ae5853b2ac31efd2847f44f0"
CAW_CREATE_TX      = "0x4d160f76cdacbffc4f7302d4fb180317e15d19080cbbaded4ef0197e71ba515c"

RIDDLE_WALLET      = "0xbaeEDcCcbFB112d4a921dAa635AC2276307A1705"
RIDDLE1_TX         = "0xfbbcf5338b4a9c35073ac7253afc1a8ee81770d8d3285b80497bbd9c2186ed5b"
RIDDLE2_TX         = "0xcae4b15350b3ccc2b37fec5caa718560241ec181bc49741d5d1199d1d32412d4"

IPFS_CID_R1        = "QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV"
DEEPSOUND_PASSWORD = "enkidu"

LAYERS = [
    "R1-000_yale_oldking",
    "R1-010_poem_coords",
    "R1-020_book_cipher",
    "R1-030_cid_audio",
    "R1-040_deepsound",
    "R1-050_manifesto_rebuild",
    "R2-000_anchor",
    "R2-010_pastebin_recovery",
]

def _nl(s: str) -> str:
    assert isinstance(s, str)
    return s.rstrip("\n") + "\n"

def _replace_block(text: str, begin: str, end: str, block: str) -> str:
    assert begin and end and begin != end
    assert block.endswith("\n")
    if begin in text and end in text:
        pre, rest = text.split(begin, 1)
        _, post = rest.split(end, 1)
        return pre + begin + "\n" + block + end + post
    if not text.endswith("\n"):
        text += "\n"
    return text + begin + "\n" + block + end + "\n"

def index_block() -> str:
    return _nl(
        "## Riddle progress\n\n"
        "- Progress overview: `docs/RIDDLE_PROGRESS.md`\n"
        "- On-chain provenance: `docs/ONCHAIN_TRACE.md`\n"
        "- R1 end-to-end: `docs/R1_58bZfQ1_END_TO_END.md`\n"
        "- R2 status: `docs/R2_zrUfKaKV_STATUS.md`\n\n"
        "## Layer index\n" +
        "".join([f"- `layers/{d}/`\n" for d in LAYERS])
    )

def doc_riddle_progress() -> str:
    return _nl(
        "# Riddle progress (canon)\n\n"
        "Updated: 2026-02-09 (America/New_York)\n\n"
        "This repo is a reproducible evidence pack for the CAW “A Hunter’s Dream” riddles.\n\n"
        "## High-level (receipts-first)\n"
        "- R1: on-chain marker → image → poem/coords → book cipher → IPFS CID → audio → DeepSound → `enkidu.txt` → reconstruction.\n"
        "- R2: on-chain marker → Pastebin trail (historic deletion) → recovery/verification in progress.\n"
    )

def doc_onchain_trace() -> str:
    return _nl(
        "# On-chain provenance\n\n"
        "## Core anchors\n"
        f"- CAW token contract: `{CAW_TOKEN_CONTRACT}`\n"
        f"- CAW deployer (Etherscan-labeled): `{CAW_DEPLOYER}`\n"
        f"- Intermediary: `{INTERMEDIARY}`\n"
        f"- SHIB deployer: `{SHIB_DEPLOYER}`\n\n"
        "## Funding chain (timed receipts)\n"
        f"- SHIB deployer → intermediary: `{FUNDING_TX_IN}`\n"
        f"- intermediary → CAW deployer: `{FUNDING_TX_OUT}`\n"
        f"- CAW contract creation tx: `{CAW_CREATE_TX}`\n\n"
        "## Riddle self-transactions\n"
        f"- R1 tx (0.666 ETH): `{RIDDLE1_TX}` (wallet `{RIDDLE_WALLET}`)\n"
        f"- R2 tx (0.999 ETH): `{RIDDLE2_TX}` (wallet `{RIDDLE_WALLET}`)\n\n"
        "## Links\n"
        f"- https://etherscan.io/address/{CAW_TOKEN_CONTRACT}\n"
        f"- https://etherscan.io/address/{CAW_DEPLOYER}\n"
        f"- https://etherscan.io/address/{INTERMEDIARY}\n"
        f"- https://etherscan.io/address/{SHIB_DEPLOYER}\n"
        f"- https://etherscan.io/tx/{FUNDING_TX_IN}\n"
        f"- https://etherscan.io/tx/{FUNDING_TX_OUT}\n"
        f"- https://etherscan.io/tx/{CAW_CREATE_TX}\n"
        f"- https://etherscan.io/tx/{RIDDLE1_TX}\n"
        f"- https://etherscan.io/tx/{RIDDLE2_TX}\n"
    )

def doc_r1_end_to_end() -> str:
    return _nl(
        "# Riddle 1 (58bZfQ1) — end-to-end\n\n"
        f"Known CID (reported): `{IPFS_CID_R1}`\n\n"
        "Chain (as reported; treat as claims until fully reproduced with hashes):\n"
        "on-chain marker → image → poem/coords → book cipher (Gilgamesh) → CID → `.ape` audio → "
        f"DeepSound password `{DEEPSOUND_PASSWORD}` → `enkidu.txt` → reconstruction.\n"
    )

def doc_r2_status() -> str:
    return _nl(
        "# Riddle 2 (zrUfKaKV) — status\n\n"
        f"Anchor tx: `{RIDDLE2_TX}`\n\n"
        "Pastebin trail existed historically and was deleted; canonical recovery still needs full reproducible hashing.\n"
    )

def layer_stub(name: str) -> Tuple[str, str]:
    summary = _nl(f"# {name}\n\nStatus: scaffold only. Fill with exact reproduction steps + hashes.\n")
    reproduce = _nl(
        f"# Reproduce: {name}\n\n"
        "## Preconditions\n"
        "- Run from repo root.\n"
        "- Record tool versions.\n"
        "- Hash every artifact saved under `EVIDENCE/`.\n"
    )
    return summary, reproduce

@dataclass(frozen=True)
class RepoSync:
    root: Path

    def __post_init__(self) -> None:
        assert self.root.is_dir(), f"missing root dir: {self.root}"
        # repo marker you already use
        assert (self.root / "scripts" / "check_canon.sh").exists(), "expected scripts/check_canon.sh"

    def render(self) -> Dict[str, str]:
        files: Dict[str, str] = {
            "docs/RIDDLE_PROGRESS.md": doc_riddle_progress(),
            "docs/ONCHAIN_TRACE.md": doc_onchain_trace(),
            "docs/R1_58bZfQ1_END_TO_END.md": doc_r1_end_to_end(),
            "docs/R2_zrUfKaKV_STATUS.md": doc_r2_status(),
        }
        for layer in LAYERS:
            base = f"layers/{layer}"
            summary, reproduce = layer_stub(layer)
            files[f"{base}/SUMMARY.md"] = summary
            files[f"{base}/REPRODUCE.md"] = reproduce
            files[f"{base}/EVIDENCE/README.md"] = _nl(f"# Evidence for {layer}\n")
        return files

    def apply(self) -> Tuple[int, int]:
        rendered = self.render()
        written = unchanged = 0
        for rel, content in rendered.items():
            fp = self.root / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            prev = fp.read_text(encoding="utf-8", errors="replace") if fp.exists() else None
            if prev == content:
                unchanged += 1
                continue
            fp.write_text(content, encoding="utf-8")
            written += 1
            LOG.info("wrote %s", rel)

        self._update_index_files()
        return written, unchanged

    def _update_index_files(self) -> None:
        block = index_block()
        for fname in ("README.md", "LAYER_INDEX.md"):
            fp = self.root / fname
            if not fp.exists():
                continue
            t = fp.read_text(encoding="utf-8", errors="replace")
            t2 = _replace_block(t, DOC_BEGIN, DOC_END, block)
            if t2 != t:
                fp.write_text(_nl(t2), encoding="utf-8")
                LOG.info("updated %s index block", fname)

def main(argv: Iterable[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--root", default=".")
    args = ap.parse_args(list(argv) if argv is not None else None)

    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    rs = RepoSync(Path(args.root).resolve())
    if not args.apply:
        LOG.info("dry-run (use --apply)")
        return 0
    w, u = rs.apply()
    LOG.info("apply complete: written=%d unchanged=%d", w, u)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
