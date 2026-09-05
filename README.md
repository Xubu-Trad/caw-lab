![XUBU — CAW research. Verified steps. Open questions.](docs/assets/lab-banner.svg)

# CAW riddle research

Two on-chain trailheads. A record of what can be reproduced, and what remains open.

**[Read the trail](docs/VISUAL_GUIDE.md)** · **[Check the evidence](LAYER_INDEX.md)** · **[Replay the tablet](layers/R1-010_friderici_poem_coords/REPRODUCE.md)**

<table><tr><td width="34%">
<a href="docs/assets/r1-tablet.png"><img src="docs/assets/r1-tablet.png" width="250" alt="The original R1 tablet image, containing the 46 coordinates and a literal poem." /></a>
</td><td>
<h3>The first trailhead</h3>
<p><code>58bZfQ1</code> leads to this tablet image. Its RGB pixel bits yield 46 coordinates. A separate insertion in the final PNG checksum yields the mirror/backwards poem.</p>
<p>Both now reproduce from the preserved image. The next gap is the exact book-cipher recipe that produces the historical IPFS identifier.</p>
<p><a href="layers/R1-010_friderici_poem_coords/REPRODUCE.md">Method, hashes and limits →</a></p>
</td></tr></table>

## Where we stand

| Trail | Reproduced | Still open |
| --- | --- | --- |
| **R1 · 58bZfQ1** | Image → coordinates and poem. Preserved Enkidu pseudohex → English manifesto. | Exact corpus/indexing → CID; independent audio-to-Enkidu extraction. |
| **R2 · zrUfKaKV** | Public anchor and bounded source receipts. | Input provenance and a validated decode. **Unsolved.** |

An archived claim is a lead. A replay is evidence. Neither alone proves the whole riddle is finished.

## Choose a route

- **New to the hunt:** [visual guide](docs/VISUAL_GUIDE.md) → [riddle progress](docs/RIDDLE_PROGRESS.md).
- **Checking a result:** [tablet replay](layers/R1-010_friderici_poem_coords/REPRODUCE.md) · [Enkidu replay](layers/R1-040_deepsound_enkidu/REPRODUCE.md).
- **Tracing the gaps:** [R1 narrative](docs/R1_58bZfQ1_END_TO_END.md) · [R2 status](docs/R2_zrUfKaKV_STATUS.md).
- **Checking provenance:** [on-chain receipts](docs/ONCHAIN_TRACE.md) · [what the facts prove](docs/WHAT_THE_FACTS_PROVE.md).

## Reproduce or contribute

```sh
python3 scripts/reproduce_tablet.py
python3 scripts/reproduce_enkidu.py
bash scripts/check_canon.sh
```

For a proposed step, provide exact inputs, commands, output hashes and limits. Use the [layer template](layers/TEMPLATE/) and update the manifest. Public evidence excludes private correspondence, credentials and unsupported identity claims.

[Mission and acknowledgements](docs/PROJECT_BACKGROUND.md) · [Hunters](docs/HUNTERS.md) · [Privacy](docs/PUBLICATION_PRIVACY.md) · [Security](SECURITY.md) · [License](LICENSE)
