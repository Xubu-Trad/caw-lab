# R1 caption pixel review — 2026-11-11

## Source and method

FACT: the preserved public tablet PNG has SHA-256 `889253e7fa85f5e5fd05622b8a105fd61acf83bdfdae3e600bdfedd173b2da41`. The complete original file is included unchanged. This turn used that preserved file, not a newly retrieved historical capture. Matching an existing local hash is not independent proof of its 2022 archive date.

The caption region is x=295..421, y=662..741 (zero-based; crop box right/bottom exclusive: 295,662,422,742). It is only 127 by 80 source pixels. The supplied views use nearest-neighbor enlargement, grayscale autocontrast, fixed grayscale thresholds 8/16/24/32/48/64 and the exact red least-significant-bit plane. No generative enhancement, letter repair, OCR-based substitution or historical transcription was used to fill gaps. The threshold views are alternatives, not cumulative processing.

## Findings

FACT: direct visual inspection confirms a small, seven-row raster text region in the original pixels. Several character shapes remain fragmented even after enlargement. The original-color crop, autocontrast view, threshold 8/16 views and red-bit-plane enlargement were visually inspected; all nine saved views have pixel-reproduction checks.

UNRESOLVED: lines 4, 5 and 6 cannot be transcribed character-for-character with defensible confidence from the inspected pixels. None is promoted to verified. This review also does not independently certify complete spelling, punctuation or capitalization of the other four lines. Historical readings remain candidate transcriptions, not fresh pixel-confirmed text. No new full transcription is supplied because that would fill gaps from prior expectations.

The separate 273-byte IEND-embedded poem beginning `The archievest` is a different data channel. Its reproducible decoding must not be used as verification of this raster caption. The package's audio, CID and manifesto-formatting results remain unchanged by this negative caption result.

## What remains unverified

- Exact raster-caption wording, particularly lines 4–6; any interpretation relying on disputed words remains conditional.
- Independent historical custody/date of the preserved image and audio. Ten's reported archive match is not independently re-established here.
- Independently fetched Wayback bytes for Ten's manifesto: v2 reconstructed the exact reported digest, not a fresh capture.
- Ten's own independent audio/DeepSound replay, pending his result; our local extraction and CID replay are supplied, not a substitute for his review.
- Riddle authorship and whether further layers exist; no terminal-solve claim follows.
- R2's previously identified archival interval is outside this R1 check and remains unaddressed.

## Next useful evidence

Ask Ten to compare this exact PNG hash and crop with his retained Wayback image. An independently preserved higher-resolution version or contemporaneous source caption could help, but must be linked to this image by provenance. A clearer-looking generated image would not establish the original letters. A historical slide transcription alone cannot close direct-pixel verification.

Run `python3 scripts/verify_caption_views.py` from the extracted package (Python 3 plus Pillow). A pass authenticates the source hash and deterministic pixel transforms only, not our ability to read the letters.
