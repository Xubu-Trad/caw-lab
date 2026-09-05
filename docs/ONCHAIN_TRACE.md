# On-chain provenance

The R1 and R2 announcements share one address. The CAW contract creation and later manifesto endorsement share another. These are verified address relationships; they do not identify a person or establish that both addresses have the same controller.

**Correction — 2026-09-05:** the previous CAW creation reference beginning `0x4d160fb54…` was malformed, with an odd number of hex digits. It has been replaced with `0x4d160f76cdacbffc4f7302d4fb180317e15d19080cbbaded4ef0197e71ba515c`, verified against the transaction, successful receipt, and containing block. See the [preserved verification receipt](evidence/endpoint_2026-09-05/endpoint_verification.json).

## Verified accounts

| Role | Address | Evidence |
|---|---|---|
| CAW token contract | `0xf3b9569f82b18aef890de263b84189bd33ebe452` | Contract address in the creation receipt |
| Contract creator; later whitehat-message sender | `0x36b59455afeedf0866fe6e775fe7651bbbe3e005` | Creation transaction sender and October 31 message sender |
| R1 and R2 announcement sender | `0xbaeedcccbfb112d4a921daa635ac2276307a1705` | Sender and recipient of both self-transactions |

## Primary anchors

| Event | Time (UTC) | Exact result |
|---|---|---|
| [CAW creation](https://etherscan.io/tx/0x4d160f76cdacbffc4f7302d4fb180317e15d19080cbbaded4ef0197e71ba515c) | 2022-04-14 04:41:34 | `36b594…` creates the CAW contract above, with nonce zero and a successful receipt |
| [R1 announcement](https://etherscan.io/tx/0xfbbcf5338b4a9c35073ac7253afc1a8ee81770d8d3285b80497bbd9c2186ed5b) | 2022-05-09 06:30:41 | `baeed…` self-transfer of 0.666 ETH; entire input is 7 ASCII bytes: `58bZfQ1` |
| [R2 announcement](https://etherscan.io/tx/0xcae4b15350b3ccc2b37fec5caa718560241ec181bc49741d5d1199d1d32412d4) | 2022-07-17 03:18:35 | `baeed…` self-transfer of 0.999 ETH; entire input is 8 ASCII bytes: `zrUfKaKV` |
| [Manifesto and development links](https://etherscan.io/tx/0x7903adbb7ab03521da9951d63cc9050ee005dfa871ba3f6d3e20d0bb941f5c37) | 2022-10-31 03:02:35 | The contract creator `36b594…` sends a 122-byte message linking `pastebin.com/yhcajZq0` and `github.com/cawdevelopment` |

The October message directly supports the creator account's endorsement of those destinations. It does not declare R2 solved or authenticate a shared controller for the creator and announcement accounts. The self-transfer values are recorded amounts; they do not establish a person's finances or independently determine a cipher rule.

The [verification receipt](evidence/endpoint_2026-09-05/endpoint_verification.json) records matching transaction, receipt, and block fields for all four anchors. These are checks of preserved public RPC responses, not a claim of independently operating an Ethereum consensus node.

## Historical funding references

The earlier research also records the following proposed funding path. These two transfers were not reverified by the correction above; their sender labels and broader interpretation require their own supporting receipts.

- SHIB-deployer-labeled address `0xb8f226ddb7bc672e27dffb67e4adabfa8c0dfa08` → intermediary `0x81a0daaab45dbbce68b11e7aeddd6a0d1970bdea`: [recorded transaction](https://etherscan.io/tx/0xb5b81a63c957fcc33469d59f9c969e860d24574bb72d8b2fc482c7232cb13062).
- Intermediary → CAW creator: [recorded transaction](https://etherscan.io/tx/0xbfed9c9fe98cf7705b6668afbe9f01c81310f062ae5853b2ac31efd2847f44f0).

A transfer path, even when verified, does not by itself prove common ownership, collaboration, intent, or current control.
