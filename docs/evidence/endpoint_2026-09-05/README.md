# Endpoint evidence · September 5, 2026

Read the [assessment](../../ENDPOINT_ASSESSMENT.md) for conclusions and limits.

| Receipt | Reproducible observation |
| --- | --- |
| [Manifesto history](manifesto_history_receipt.json) | Three pinned historical Git bodies match the recovered normalized manifesto exactly. |
| [Chain consistency](endpoint_verification.json) | Four public transaction/receipt/block checks; riddle-marker and contract-creator accounts are distinguished. |
| [Source wrapper](wrapper_audit.json) | Exact R2 text node, lowercase hex, no authored whitespace or additional displayed instruction in checked copies. |
| [APE inventory](ape_inventory.json) | Declared regions end exactly at physical EOF. |
| [PNG inventory](png_inventory.json) and [unused regions](png_unused_receipt.json) | Chunk, zlib and metadata boundaries. |
| [Low-bit regions](bitplane_receipt.json) | Separate raster text and tiny mark explicitly retained as limits. |
| [Public context](primary_context.json) | Source links and bounded interpretations for the community walkthrough and fish recipe. |

From the repository root:

```sh
git clone https://github.com/cawdevelopment/manifesto upstream-manifesto
python3 scripts/compare_manifesto_history.py upstream-manifesto layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.full_pseudohex.txt --output replay-history.json
python3 docs/evidence/endpoint_2026-09-05/chain/verify_endpoint.py
```

The first command downloads the public source history. The comparison strips only its first heading line and replaces the decoded manifesto's 60 tabs with single spaces. The chain script verifies the preserved full public RPC responses in its own directory; it writes a fresh receipt there. It checks response consistency, not Ethereum consensus with a locally synchronized node. Source transaction URLs are recorded in the assessment so readers can retrieve independent copies.

The existing tablet, book, Enkidu and R2 replay instructions remain the underlying cipher proofs. The R1 CID reproduction is documented in [R1 determinism status](../../R1_DETERMINISM_STATUS.md). Carrier-analysis scripts, exact derived raster images, research attempts and the reviewed context ledger are preserved in the private research journal. No raw Telegram export, identity mapping or service page HTML is included in this public package. A negative scan is bounded by its documented input and method.
