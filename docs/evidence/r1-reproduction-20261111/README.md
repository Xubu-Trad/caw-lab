# R1 independent reproduction reference (2026-11-11)

Download [the complete reproduction files](R1-Ten-Reproduction-20261111-v3.zip) using GitHub's raw/download button. Check [the archive SHA-256](SHA256SUMS.txt), extract it, and follow its README. Python, FFmpeg and cryptography reproduce audio extraction; Pillow verifies the caption pixel views. Original bytes and receipts are included. No private workflow or messages are included.

## Verified locally

- The 8,968,236-byte APE computes the book-derived CID QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV under the documented UnixFS settings.
- Fresh audio extraction produces the exact 21,192-byte enkidu.txt (SHA-256 4f4edfdece802b300aeab48932b115d83eb04575753bfd128a3cc47c5cc25b19).
- The decoded manifesto is 10,596 bytes. Replacing 60 tabs with spaces, using CRLF line endings and omitting the final newline produces the reported Wayback-copy digest 5e03b441cc8dc10874f9ac956bf9c7c0574fc94e0387b3ef186661505044738b at exactly 10,749 bytes. No wording changes. This is a hash-matching reconstruction, not a new Wayback retrieval.

See [the exact manifesto comparison](MANIFESTO_COMPARISON.md). Hex-encoding the differently formatted Wayback copy does not reproduce the exact audio-extracted Enkidu bytes without restoring the original formatting.

## Still unresolved

See [the direct-pixel caption review](CAPTION_REVIEW.md). Lines 4-6 remain unverified; a historical transcription is not substituted for unreadable pixels. The separate IEND-encoded poem is not the raster caption. [Original pixel enlargement](caption-original-10x.png) and [low-bit view](caption-red-lsb-8x.png) are provided for inspection.

Historical custody, authorship, continuous IPFS availability and terminal riddle completion are not established by these tests. The R2 archival gap is outside this review. Independent replay by another researcher is still requested.

The archive's preparation notes describe its local creation stage; this index records its subsequent public publication. Scripts and artifacts retain their original verification boundaries.
