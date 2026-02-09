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

# Canonical anchors (from attached report; receipts-first)
CAW_TOKEN_CONTRACT = "0xf3b9569f82b18aef890de263b84189bd33ebe452"
CAW_DEPLOYER       = "0x36B59455AfeEdf0866FE6E775FE7651bbBe3e005"
INTERMEDIARY       = "0x81A0daaab45dBbcE68b11E7AEdDd6A0D1970bdeA"
SHIB_DEPLOYER      = "0xB8f226dDb7bC672E27dffB67e4adAbFa8c0dFA08"

FUNDING_TX_IN      = "0xb5b81a63c957fcc33469d59f9c969e860d24574bb72d8b2fc482c7232cb13062"
FUNDING_TX_OUT     = "0xbfed9c9fe98cf7705b6668afbe9f01c81310f062ae5853b2ac31efd2847f44f0"
# NOTE: this is the create *tx* from the report (your older script accidentally used a different hex)
CAW_CREATE_TX      = "0x4d160fb54fbfbf23725f03cc0b780b6666a66c9884f6d1024ef1287321c22515c"

RIDDLE_WALLET      = "0xbaeEDcCcbFB112d4a921dAa635AC2276307A1705"
RIDDLE1_TX         = "0xfbbcf5338b4a9c35073ac7253afc1a8ee81770d8d3285b80497bbd9c2186ed5b"
RIDDLE2_TX         = "0xcae4b15350b3ccc2b37fec5caa718560241ec181bc49741d5d1199d1d32412d4"

IBB_IMAGE_R1       = "https://ibb.co/58bZfQ1"
PASTEBIN_SLUG_R2   = "yhcajZq0"

IPFS_CID_R1        = "QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV"
DEEPSOUND_PASSWORD = "enkidu"

# Match the report’s folder naming (so repo == report)
LAYERS = [
    "R1-000_yale_oldking",
    "R1-010_friderici_poem_coords",
    "R1-020_book_cipher_gilgamesh",
    "R1-030_ipfs_ape_audio",
    "R1-040_deepsound_enkidu",
    "R1-050_manifesto_final_payload",
    "R2-000_onchain_zrufkakv",
    "R2-010_pastebin_payload",
]

def _nl(s: str) -> str:
    assert isinstance(s, str)
    return s.rstrip("\n") + "\n"

def _replace_block(text: str, begin: str, end: str, block: str) -> str:
    """Replace or append a marked block delimited by begin/end markers.

    >>> _replace_block("a\\n", "<b>", "</b>", "X\\n")
    'a\\n<b>\\nX\\n</b>\\n'
    >>> _replace_block("a\\n<b>\\nOLD\\n</b>\\n", "<b>", "</b>", "NEW\\n")
    'a\\n<b>\\nNEW\\n</b>\\n'
    """
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
    """Build the README/LAYER_INDEX insert block.

    >>> b = index_block()
    >>> ("docs/ONCHAIN_TRACE.md" in b) and ("layers/R2-010_pastebin_payload/" in b)
    True
    """
    return _nl(
        "## Riddle progress\n\n"
        "- Progress overview: `docs/RIDDLE_PROGRESS.md`\n"
        "- On-chain provenance: `docs/ONCHAIN_TRACE.md`\n"
        "- What these facts do (and do not) prove: `docs/WHAT_THE_FACTS_PROVE.md`\n"
        "- R1 end-to-end: `docs/R1_58bZfQ1_END_TO_END.md`\n"
        "- R2 status: `docs/R2_zrUfKaKV_STATUS.md`\n\n"
        "## Layer index (chronological)\n" +
        "".join([f"- `layers/{d}/`\n" for d in LAYERS])
    )

def doc_riddle_progress() -> str:
    return _nl(
        "# Riddle progress (canon)\n\n"
        "Updated: 2026-02-09 (America/New_York)\n\n"
        "This repo is a reproducible evidence pack for the CAW “A Hunter’s Dream” riddles.\n\n"
        "## Docs index\n"
        "- `docs/ONCHAIN_TRACE.md`\n"
        "- `docs/WHAT_THE_FACTS_PROVE.md`\n"
        "- `docs/R1_58bZfQ1_END_TO_END.md`\n"
        "- `docs/R2_zrUfKaKV_STATUS.md`\n\n"
        "## Layer index\n" +
        "".join([f"- `layers/{d}/`\n" for d in LAYERS]) +
        "\n"
        "## Notes\n"
        f"- R1 image host (reported): {IBB_IMAGE_R1}\n"
        f"- R1 known CID (reported): {IPFS_CID_R1}\n"
        f"- R2 Pastebin slug (reported): {PASTEBIN_SLUG_R2}\n"
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
        f"- https://etherscan.io/tx/{RIDDLE2_TX}\n\n"
        "## Important limitation\n"
        "“Deployer” labels are on-chain roles/attribution, not verified identity.\n"
    )

def doc_what_facts_prove() -> str:
    return _nl(
        "# What these facts do (and do not) prove\n\n"
        "## These exhibits support (based only on receipts shown)\n\n"
        "1. The CAW contract is not presenting a typical upgradeable/proxy admin control surface.\n"
        "- Proxy admin slot = 0x0 and proxy implementation slot = 0x0 (EIP-1967 slot reads).\n"
        "- delegatecall behavior flagged false (receipt-backed checks in this repo).\n"
        "- push-aware runtime opcode scan shows executed counts of 0 for:\n"
        "  - the call-family, and\n"
        "  - CREATE / CREATE2 / SELFDESTRUCT\n\n"
        "2. The origin trail and creation flow exist as a sequence of on-chain receipts.\n"
        f"- SHIB deployer → intermediary: `{FUNDING_TX_IN}`\n"
        f"- intermediary → CAW deployer: `{FUNDING_TX_OUT}`\n"
        f"- CAW contract creation tx: `{CAW_CREATE_TX}`\n\n"
        "## What this does not prove\n"
        "- Identity: on-chain deployer roles do not prove who a person is.\n"
        "- Intent: receipts alone do not prove motivations.\n"
        "- Control today: provenance does not imply an individual retains control now.\n"
    )

def doc_r1_end_to_end() -> str:
    return _nl(
        "# Riddle 1 (58bZfQ1) — end-to-end\n\n"
        f"Anchor tx: `{RIDDLE1_TX}`\n\n"
        "Reported chain (treat as claims until reproduced with hashes):\n"
        f"on-chain marker → image ({IBB_IMAGE_R1}) → poem/coords → book cipher (Gilgamesh) → CID `{IPFS_CID_R1}` → "
        f"`.ape` audio → DeepSound password `{DEEPSOUND_PASSWORD}` → `enkidu.txt` → reconstruction.\n\n"
        "Reported mechanics to preserve in-layer:\n"
        "- Poem hints inversion/mirror/backwards.\n"
        "- Coordinate list is ~46 entries (LINE:WORD) with fallback to letter-count when word index exceeds line length.\n"
        "- Hex-like stage uses U/V/W/X/Y/Z as substituted a–f nibbles (mapping captured in evidence).\n"
    )

def doc_r2_status() -> str:
    return _nl(
        "# Riddle 2 (zrUfKaKV) — status\n\n"
        f"Anchor tx: `{RIDDLE2_TX}`\n\n"
        "Reported trail:\n"
        f"- On-chain key points to Pastebin slug `{PASTEBIN_SLUG_R2}` (historic deletion).\n\n"
        "Current technical constraint (per your progress notes):\n"
        "- The recovered paste decodes into a zlib stream requiring a preset dictionary (FDICT). "
        "Without the correct dictionary bytes, decompression is blocked.\n"
    )

def layer_stub(name: str) -> Tuple[str, str, str]:
    assert name in set(LAYERS), name
    summary = _nl(
        f"# {name}\n\n"
        "Status: scaffold.\n\n"
        "Put the layer narrative here and link to evidence artifacts under `EVIDENCE/`.\n"
    )
    reproduce = _nl(
        f"# Reproduce: {name}\n\n"
        "## Preconditions\n"
        "- Run from repo root.\n"
        "- Record tool versions.\n"
        "- Hash every artifact saved under `EVIDENCE/`.\n\n"
        "## Steps\n"
        "- [ ] Add exact commands\n"
        "- [ ] Save outputs under `EVIDENCE/`\n"
        "- [ ] Record sha256 for every output\n"
    )
    evidence_readme = _nl(
        f"# Evidence for {name}\n\n"
        "Store non-empty evidence artifacts here (scripts, logs, extracted blobs, hashes).\n"
    )
    return summary, reproduce, evidence_readme

@dataclass(frozen=True)
class RepoSync:
    root: Path

    def __post_init__(self) -> None:
        assert self.root.is_dir(), f"repo root missing: {self.root}"
        chk = self.root / "scripts" / "check_canon.sh"
        assert chk.exists(), f"expected repo marker missing: {chk}"

    def render(self) -> Dict[str, str]:
        files: Dict[str, str] = {}
        files["docs/RIDDLE_PROGRESS.md"] = doc_riddle_progress()
        files["docs/ONCHAIN_TRACE.md"] = doc_onchain_trace()
        files["docs/WHAT_THE_FACTS_PROVE.md"] = doc_what_facts_prove()
        files["docs/R1_58bZfQ1_END_TO_END.md"] = doc_r1_end_to_end()
        files["docs/R2_zrUfKaKV_STATUS.md"] = doc_r2_status()

        for d in LAYERS:
            base = f"layers/{d}"
            s, r, e = layer_stub(d)
            files[f"{base}/SUMMARY.md"] = s
            files[f"{base}/REPRODUCE.md"] = r
            files[f"{base}/EVIDENCE/README.md"] = e
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
        for fname in ["README.md", "LAYER_INDEX.md"]:
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
    ap.add_argument("--apply", action="store_true", help="write changes to disk")
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    args = ap.parse_args(list(argv) if argv is not None else None)

    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    rs = RepoSync(Path(args.root).resolve())
    if not args.apply:
        LOG.info("dry-run only; use --apply to write files")
        return 0

    written, unchanged = rs.apply()
    LOG.info("apply complete: written=%d unchanged=%d", written, unchanged)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
