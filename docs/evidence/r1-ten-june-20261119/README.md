# What the hunters reported on June 9, 2022

Ten found a Wayback capture of the hunters’ original Twitter thread. The May 9 tablet already identifies the exact audio through its book cipher and IPFS content address (CID). The June thread adds something the fingerprint alone cannot tell us. The hunters described downloading the file, recognizing its format and opening the hidden text. A dated archive of the audio download itself is still missing.

## The archived thread

The opening post’s ID, `1534892255730966529`, gives **June 9, 2022 at 13:36:45.342 UTC**. Wayback captured the thread page at **13:37:26 UTC**, about 41 seconds later. The captured page includes the CID, a gateway link to that same CID, and the follow-up posts. In post 13 the hunters describe receiving an extensionless file and identifying it as APE. Posts 15–19 describe using DeepSound with the password `enkidu`, opening `enkidu.txt`, reversing the letter substitution and reaching the manifesto. This is a contemporary account of a successful retrieval. The dated page preserves what the hunters said. The file that the gateway served was not part of that page. [June 9 Wayback capture](https://web.archive.org/web/20220609133726id_/https://twitter.com/CommunityCaw/status/1534892255730966529) · [Hunters’ download post](https://x.com/CommunityCaw/status/1534892358713724930) · [Earlier May archive records](../r1-independent-review-20261118/README.md)

Raw archived HTML: 719,771 bytes, SHA-256 `dd951b0886fab4b18053a92d416494422dcc08f174e18b69f6a643c4cb7d3731`.

## Ten’s independent audio check

Ten decoded the November 11 package’s `canonical.ape` with FFmpeg on his own node. His SHA-256 matches the full decoded sample stream and its final 500 bytes. Starting at byte **25,963,964** (counting from zero), a 244-byte RIFF LIST/INFO block is followed by a 256-byte ID3 block. They sit inside the samples compressed by the APE. The CID recovered from the [archived May 9 tablet](https://web.archive.org/web/20220509164829id_/https://i.ibb.co/9TQPCxp/Proposalforadecentralizedcoupfortehpplbytehppl.png) therefore covers the tags too. [Audio identity and extraction bundle](../r1-reproduction-20261111/README.md)

| Bytes checked | Size | SHA-256 |
| --- | ---: | --- |
| Decoded stereo PCM, 48 kHz, signed 16-bit little-endian | 25,964,464 | `9a50dfecbbe8612b6470f804e6a752d2d98ad43c2daae126fd80fc4bf094086d` |
| Final 500 bytes | 500 | `bdae1720729520529d098b2ee8d7e504b9e1e69350b2c70f4fb87d38e207c2e4` |

Both comment fields (`ICMT` and `COMM`) contain “CAW Is a decentralized social clearing house of trustless interaction”, including the capital `Is` and a trailing space. The manifesto inside the same recording opens with “A Manifesto on a Decentralized Social Clearing House ...(AKA) CAW”. The full comment does not occur in the manifesto. Both sets of tags also carry the artist `nobody` and the genre `hoof dovoi`. The ID3 software label reads `RYO OS 0.43`; the RIFF version adds `(libsndfile-1.0.31)`. The identity of the person who supplied these words remains open. [Manifesto text](../../../layers/R1-050_manifesto_final_payload/EVIDENCE/manifesto.en.txt) · [Software-field replay](../r1-upper-strip-20261118/README.md)

## One spelling correction and two caption readings

**Embedded verse.** The decoded opening line is `The archievest speaks truest of the orginal 11, but not the 12th`. Replacing `orginal` with `original` changes the source. Ten caught this in an article quoting the verse. The repository’s original 273-byte poem already has both spellings, `archievest` and `orginal`, and the hunters’ post 8(a) also has `orginal`. [Preserved poem](../../../layers/R1-010_friderici_poem_coords/EVIDENCE/poem.txt) · [Post 8(a)](https://x.com/CommunityCaw/status/1534892316095401984)

**Visible caption.** The tiny lettering on the tablet is a separate source. These are two reported readings of its ending:

| Source | Ending as transcribed |
| --- | --- |
| Hunters’ June 9 thread, post 6 | `only the, his lover may hear` |
| Later article transcription quoted in Ten’s follow-up | `only the his true lover may hear` |

The first has a comma after `the`. The second includes `true`. The available pixels do not settle the disputed wording. Lines 4–6 remain unresolved. [June caption post](https://x.com/CommunityCaw/status/1534892306360414209) · [Original pixel comparison](../r1-reproduction-20261111/CAPTION_REVIEW.md)

## What the cipher test shows

Ten tested all 25 nonzero Caesar shifts and all 311 non-identity invertible affine maps of the 26-letter alphabet. The 25 shifts are included in the 311. An English first word can occur: with `a=0, …, z=25`, replacing each letter value `x` with `(19x + 24) mod 26` turns `hoof dovoi` into **`beep deheu`**. This corrects the first-word claim. Neither this output nor any proposed reading reviewed here establishes a meaning for the whole phrase. In particular, the word `beep` supplies no independent evidence of an audio clue.

## Repeat the checks

Download the linked raw Wayback HTML and the November 11 bundle. The example assumes the extracted `canonical.ape` and downloaded `june9.html` are in the working directory. Run from the repository root. The FFmpeg output is raw PCM without a WAV header.

```sh
ffmpeg -v error -i canonical.ape -map 0:a:0 -c:a pcm_s16le -f s16le june9-review.pcm
python3 docs/evidence/r1-ten-june-20261119/replay.py june9.html docs/assets/r1-tablet.png june9-review.pcm
```
