# What Ten and Hossein verified about the CAW riddles

The strongest new date is **May 9, 2022, at 16:48:29 UTC**. The tablet image archived at that moment already points to the exact R1 recording that contains `hoof dovoi` and `RYO OS 0.43`. Early hunters can now look for a file from *before* that recording was exported. The person who chose the words and what they meant remain open questions. [Archived tablet PNG](https://web.archive.org/web/20220509164829id_/https://i.ibb.co/9TQPCxp/Proposalforadecentralizedcoupfortehpplbytehppl.png)

## What the reviewers checked

**Ten** wrote his own code to read the hidden coordinates, rebuild the audio’s IPFS content identifier (CID), and extract the encrypted file. All 46 coordinates lead to the CID of the preserved 8,968,236-byte APE. Using the password `enkidu`, he recovered all 21,192 bytes of `enkidu.txt`. He also worked backwards from the archived manifesto, restoring the original line endings and the 60 recorded tab positions, to reproduce that file byte for byte. This follow-up completes the audio steps left open in his earlier public article. [Ten’s earlier field report](https://caw-japan.com/58bzfq1-verification/) · [Reviewed bundle at commit 7a8ac26](https://github.com/Xubu-Trad/caw-lab/tree/7a8ac26/docs/evidence/r1-reproduction-20261111)

**Hossein** reports a separate Node.js decryption of the preserved audio. He confirmed that the genre and software labels each appear twice in its final 500 decoded bytes, once in each of two WAV metadata formats. He also replayed the published repository checks, compared the 878 dark positions in the circled strip with the earlier tablet photograph, and checked the reversible 1,442-byte R2 decoding. His report distinguishes the failed gateway attempt from the later successful extraction using the bundle. His protocol assessment is outside the scope of these riddle results. [Audio and dot evidence](../r1-upper-strip-20261118/README.md) · [R2 replay](../../../layers/R2-020_hex_transposition/REPRODUCE.md)

## The May archive dates

| UTC | What the record establishes |
| --- | --- |
| May 9, 2022, 06:30:41 | The Ethereum transaction contains the seven characters `58bZfQ1`. They identify the image-host page. [Transaction](https://etherscan.io/tx/0xfbbcf5338b4a9c35073ac7253afc1a8ee81770d8d3285b80497bbd9c2186ed5b) |
| May 9, 16:48:04 and 16:48:29 | Wayback captured the landing page, then the PNG it links. The archived PNG matches the preserved image byte for byte. Its coordinates, read against the pinned book, spell the CID of the complete puzzle audio. This dates both labels. Evidence of a successful IPFS download in 2022 would answer a separate question about distribution. [Landing page](https://web.archive.org/web/20220509164804id_/https://ibb.co/58bZfQ1) · [Image](https://web.archive.org/web/20220509164829id_/https://i.ibb.co/9TQPCxp/Proposalforadecentralizedcoupfortehpplbytehppl.png) · [Book-cipher replay](../../../layers/R1-020_book_cipher_gilgamesh/REPRODUCE.md) |
| May 12, 2022, 00:49:17 | The archived Pastebin page contains the manifesto in its text box. Its 10,595 bytes use spaces and LF line endings, with no final newline. Adding one LF reproduces the lab’s 10,596-byte spaces copy. [May 12 page](https://web.archive.org/web/20220512004917id_/https://pastebin.com/yhcajZq0) |
| November 7, 2022, 21:40:26 | The raw Pastebin capture contains 10,749 bytes. Converting the May page’s 154 existing line breaks to CRLF reproduces it exactly. The words, punctuation and spelling agree. The June 15 date previously cited for the **raw** URL resolves to this November capture. [November raw response](https://web.archive.org/web/20221107214026id_/https://pastebin.com/raw/yhcajZq0) |

R2 has its own timeline. The July 26, 2022 archived page returned 404. The first successful **raw R2** capture found in the Wayback index we checked was August 22, 2025. The May dates above apply to R1. [July 2022 page](https://web.archive.org/web/20220726135501id_/https://pastebin.com/zrUfKaKV) · [August 2025 raw R2](https://web.archive.org/web/20250822025050id_/https://pastebin.com/raw/zrUfKaKV)

## Corrections to carry forward

- The poem inserted at the end of the PNG begins **“The archievest”**, including the capital T and the original spelling. Its first hex byte is `54`. The first digit occupies the position normally reserved for the last checksum byte. Starting after that position loses the initial T and gives the earlier 272-byte reading. The complete poem is **273 bytes**. [Tablet replay](../../../layers/R1-010_friderici_poem_coords/REPRODUCE.md)
- The published comparison photograph shows the **reverse of Yale tablet YBC 2178**. The identification as British Museum K.3375 on pages 4 and 6 of Hossein’s report needs correction. The detached word near the top closely matches **“the”** at the end of caption line 2. Ten could read lines 2 and 7 from the pixels. The full wording of lines 4–6 remains unresolved. [Tablet catalogue and images](https://seal.huji.ac.il/index.php/node/1831) · [Original caption and pixel evidence](../r1-reproduction-20261111/CAPTION_REVIEW.md)
- The R1 recording carries `2020` in a year field. A tag can be inherited or entered during editing. Its value cannot date the export. The two copies of each unusual label are fields in the same recording. Seeing both establishes their spelling. It leaves authorship and meaning unresolved. [Software-field replay](../r1-upper-strip-20261118/README.md)

## What the audio comparison adds

The full 135.200-second track 14, *Tre rebus musicali*, matched the BDI 103 release through two CD-rip verification databases after allowing for different track boundaries. Neither label occurs in either complete CD-aligned sample stream. The measured FLAC lists its genre as `Classique` and carries no reported software tag. That FLAC was deposited in 2026. Its tags cannot establish which tags an earlier digital copy had. [2004 CD catalogue](https://id.sbn.it/bid/DDS0979909) · [FLAC deposit record](https://archive.org/metadata/reservierte-musik-2004/metadata) · [CUETools record](https://db.cue.tools/api/fetch?id=9499012) · [AccurateRip record](https://www.accuraterip.com/accuraterip/1/9/5/dBAR-027-003a5591-046b3256-510e951b.bin)

There is a reproducible explanation for where the words sit. Inspection of DeepSound 2.0 showed that its WAV-to-APE reader can continue past the declared music into the WAV’s trailing tags. A controlled model fed those same 500 bytes to the encoder as 125 extra stereo frames. Giving it an unrelated footer produced a different ending. This explains how existing tags could survive conversion. The original editor project and export history are still missing. [DeepSound 2.0 release](https://github.com/Jpinsoft/DeepSound/releases/tag/v2.0.0.32372)

The known Enkidu extraction uses only the first 0.443 seconds of decoded audio. In separate tests, removing the final 500 bytes or replacing both occurrences of either label preserved the exact Enkidu digest. Changing one contributing bit inside the encrypted payload changed that digest. These checks leave the possibility of an intentional word clue open.

## What early hunters can contribute

If you saved the **WAV from before the DeepSound export**, an audio-editor project or backup, or a dated metadata template for this recording, please preserve it untouched. A WAV with one label, both labels, or neither could tell us *when* each first appeared. A dated attachment or download record for the known APE would help trace how the puzzle circulated.

Open a [caw-lab issue](https://github.com/Xubu-Trad/caw-lab/issues) with the filename, byte count, SHA-256, how you obtained it, and the date and time zone shown by the source. Include an original public permalink or independent archive capture if available. A file’s local modification time alone gives a weak date. Keep private chats, contact details and copyrighted audio out of the issue. Reviewers can start with the hash and provenance.

## Replay the archive comparison

Save the original responses from the May 9 **image**, May 12 **page HTML**, and November 7 **raw text** links above. Use the downloaded response bodies directly. Opening the text in an editor can change its line endings. From the repository root, run the following, substituting your three filenames.

```sh
python3 docs/evidence/r1-independent-review-20261118/verify_archives.py tablet.png may-page.html november-raw.txt
```

This checks the archived image and text. To continue from the image to the audio, use the [book-cipher instructions](../../../layers/R1-020_book_cipher_gilgamesh/REPRODUCE.md) and the [preserved audio bundle](../r1-reproduction-20261111/README.md). To compare the 60 tab locations, use the [manifesto formatting replay](../r1-reproduction-20261111/MANIFESTO_COMPARISON.md).

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| May 9 tablet PNG | 536,397 | `889253e7fa85f5e5fd05622b8a105fd61acf83bdfdae3e600bdfedd173b2da41` |
| R1 audio named by its coordinates | 8,968,236 | `57674107710cdac58fe68b30cb3c05e3334ece55bc0d71deba84ccd2a8fb3575` |
| PNG poem | 273 | `c1dfa2443b0a167034ae06ea67bcac44f1c3714d54a8c671d971b9613f5de19a` |
| Extracted `enkidu.txt` | 21,192 | `4f4edfdece802b300aeab48932b115d83eb04575753bfd128a3cc47c5cc25b19` |
| Manifesto decoded from audio, 60 tabs and final LF | 10,596 | `03fa37cfe06c7d06d590020e9fcf8c67b4131671c10d48a6f1ef0283df8cfb22` |
| May 12 textarea, spaces and no final LF | 10,595 | `1addb740a13ae52274aff829cc3b627e95eee190c3cb2540c3c30bc6be2b2338` |
| November 7 raw manifesto | 10,749 | `5e03b441cc8dc10874f9ac956bf9c7c0574fc94e0387b3ef186661505044738b` |
