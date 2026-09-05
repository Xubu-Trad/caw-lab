# What these facts do (and do not) prove

## These exhibits support (based only on receipts shown)

1. The CAW contract is not presenting a typical upgradeable/proxy admin control surface.
- Proxy admin slot = 0x0 and proxy implementation slot = 0x0 (EIP-1967 slot reads).
- delegatecall behavior flagged false (receipt-backed checks in this repo).
- push-aware runtime opcode scan shows executed counts of 0 for:
  - the call-family, and
  - CREATE / CREATE2 / SELFDESTRUCT

2. The origin trail and creation flow exist as a sequence of on-chain receipts.
- SHIB deployer → intermediary: `0xb5b81a63c957fcc33469d59f9c969e860d24574bb72d8b2fc482c7232cb13062`
- intermediary → CAW deployer: `0xbfed9c9fe98cf7705b6668afbe9f01c81310f062ae5853b2ac31efd2847f44f0`
- CAW contract creation tx: `0x4d160fb54fbfbf23725f03cc0b780b6666a66c9884f6d1024ef1287321c22515c`

## What this does not prove
- Identity: on-chain deployer roles do not prove who a person is.
- Intent: receipts alone do not prove motivations.
- Control today: provenance does not imply an individual retains control now.

## Riddle artifact checks (2026-09-05)

The pinned R1 tablet reproduces its coordinates and poem. The pinned public OCR edition reproduces the historical CID. The canonical APE now independently yields the complete Enkidu pseudohex, whose deterministic text conversion reproduces `manifesto.en.txt`. [R1 verification status](R1_DETERMINISM_STATUS.md) and [audio extraction receipt](../layers/R1-040_deepsound_enkidu/EVIDENCE/ape_to_enkidu_replay.json).

These are checks of artifact bytes and transformations. They do not establish fresh live IPFS custody, identify the author or operator, verify the manifesto's assertions, or prove that no later riddle layer exists. A password shared with a character or account name is not evidence of a person's identity.
