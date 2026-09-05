# What these facts do (and do not) prove

## These exhibits support (based only on receipts shown)

1. The CAW contract is not presenting a typical upgradeable/proxy admin control surface.
- Proxy admin slot = 0x0 and proxy implementation slot = 0x0 (EIP-1967 slot reads).
- delegatecall behavior flagged false (receipt-backed checks in this repo).
- the preserved push-aware static runtime scan reports 0 opcode occurrences (not an execution trace) for:
  - the call-family, and
  - CREATE / CREATE2 / SELFDESTRUCT

2. The CAW creation account and the riddle announcement account have distinct, verifiable roles.

- [The CAW creation transaction](https://etherscan.io/tx/0x4d160f76cdacbffc4f7302d4fb180317e15d19080cbbaded4ef0197e71ba515c) identifies `0x36b59455afeedf0866fe6e775fe7651bbbe3e005` as sender. Its successful receipt records contract `0xf3b9569f82b18aef890de263b84189bd33ebe452`.
- [R1](https://etherscan.io/tx/0xfbbcf5338b4a9c35073ac7253afc1a8ee81770d8d3285b80497bbd9c2186ed5b) and [R2](https://etherscan.io/tx/0xcae4b15350b3ccc2b37fec5caa718560241ec181bc49741d5d1199d1d32412d4) are self-transactions from `0xbaeedcccbfb112d4a921daa635ac2276307a1705`. Their entire inputs are `58bZfQ1` and `zrUfKaKV`, respectively.
- [The October 31 whitehat message](https://etherscan.io/tx/0x7903adbb7ab03521da9951d63cc9050ee005dfa871ba3f6d3e20d0bb941f5c37) comes from the same `36b594…` account that created CAW and explicitly links the manifesto destination and `cawdevelopment` GitHub. This establishes that account's endorsement of those destinations; it does not establish R2 authorship or common control of both addresses.

**Correction — 2026-09-05:** the former creation hash beginning `0x4d160fb54…` was malformed and has been replaced with the verified hash above. The [preserved verification receipt](evidence/endpoint_2026-09-05/endpoint_verification.json) checks transaction, successful receipt, and containing block for all four anchors. Earlier funding-path references remain listed with their separate evidence limits in [on-chain provenance](ONCHAIN_TRACE.md); this correction does not reverify them.

## What this does not prove
- Identity: on-chain deployer roles do not prove who a person is.
- Intent: receipts alone do not prove motivations.
- Control today: provenance does not imply an individual retains control now.
- Shared control: the riddle announcement address and contract creation address are different; the verified transactions do not prove they share a human controller.
- Financial conclusions: transfer amounts and message claims do not establish a person's wealth, profit, or wrongdoing.

## Riddle artifact checks (2026-09-05)

The pinned R1 tablet reproduces its coordinates and poem. The pinned public OCR edition reproduces the historical CID. The canonical APE now independently yields the complete Enkidu pseudohex, whose deterministic text conversion reproduces `manifesto.en.txt`. [R1 verification status](R1_DETERMINISM_STATUS.md) and [audio extraction receipt](../layers/R1-040_deepsound_enkidu/EVIDENCE/ape_to_enkidu_replay.json).

These are checks of artifact bytes and transformations. They do not establish fresh live IPFS custody, identify the author or operator, verify the manifesto's assertions, or prove that no later riddle layer exists. A password shared with a character or account name is not evidence of a person's identity.
