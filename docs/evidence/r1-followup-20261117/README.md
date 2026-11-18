# R1 follow-up · November 17, 2026

The original recording contains CAW-related text beyond the recovered Enkidu file. Its last 125 stereo sample frames hold two audio tags. Both give the genre as `hoof dovoi`. Its spelling and the identity of the music can be checked independently. The origin and meaning of the genre are still open.

## The recording

The 500-byte suffix starts at decoded sample byte 25,963,964. Its SHA-256 is `bdae1720729520529d098b2ee8d7e504b9e1e69350b2c70f4fb87d38e207c2e4`. The RIFF INFO and ID3 records both list the title as `Gilgamesh's Lover`, the album as `Teh eyes to see.` (followed by a space), the artist as `nobody`, and the track as 7. All 89 compressed-frame checksums matched the decoded samples. Removing the 500 bytes changes the final checksum. The two copies of the genre come from one recording.

On June 9, 2022, the hunters published the exact content address that the preserved recording still computes. Their thread identifies the music and describes extracting Enkidu and applying an alphabet mirror. We found no explanation of the genre in the thread or in the readable text of their slides. The stored year, 2020, cannot date the file’s preparation. The software field also names libsndfile 1.0.31, released in January 2021. [Hunters’ thread](https://threadreaderapp.com/thread/1534892255730966529.html) · [Slides](https://docs.google.com/presentation/d/1MogotX537LcmEKuzjysjBM6dknClFFPUbMJQQsAMDLM/htmlpresent) · [Library release history](https://libsndfile.github.io/libsndfile/)

Five four-second passages from the commercial preview aligned with the puzzle audio at a consistent offset of about 104.989 seconds. Their normalized correlations ranged from 0.98582 to 0.99644. The strongest absolute correlation for the five backward controls was 0.34526. The catalog identifies the performance as Massimo Lonardi and Renata Fusco’s *Tre rebus musicali*, track 14, genre Classical. The arranger’s published Italian texts contain no `hoof dovoi`. The comparison covers the sampled passage. It leaves open who supplied the puzzle copy’s labels. [Catalog and preview](https://music.apple.com/us/song/426173147) · [Arranger’s notes](https://vision.unipv.it/events/expo2015/music-descr.pdf) · [Measured offsets](music-match.txt)

## “Between the melody” and “walk backwards”

The 48 kHz tests covered the left and right channels, their sum and difference, and normal and swapped stereo. Across both time directions and four byte alignments, only ordinary forward stereo yielded the known DeepSound file. The reversed marker came from reading the same header backwards. No backward speech was independently verified. At two loudness thresholds the pauses appeared to divide the music into twelve sections. In both cases the apparent final section was the pulse produced by the metadata. Omitting those 500 bytes turned the preceding pause into trailing silence.

Reversing word order gives `dovoi hoof`. Reading each word backwards gives `fooh iovod`. Mirroring the alphabet gives `sllu wlelr`. The restricted substitution that recovers the manifesto from Enkidu leaves invalid hexadecimal when applied to the genre. We also checked whether any one-to-one letter substitution could turn the two words into adjacent words from the pinned Gilgamesh book, the manifesto or R2. No pair matched their lengths and repeated-letter pattern in the four word and letter orders tested. [Reading controls and counts](reading-controls.json)

## The tablet and the twelfth coordinate

The detached “the” is centered at (186, 95) in the 640 × 776 tablet image, counting from zero. Only coordinate 12 spans column 186. Its digits and colon occupy columns 178–194. That coordinate, `110:13`, selects “savage” in “the savage man.” The preceding line names Enkidu, the known audio password. The horizontal projection was explored after inspecting the layout. Reflecting height alone maps row 95 to 680, which crosses the twelfth printed group, “the.” Rows 91–97 also reach the word, and row 680 crosses several other words. The exact choice of height, the proposed reading `le` beneath the mark, and the designer’s intent remain unresolved. [Riddle image](../../assets/r1-tablet.png) · [Unmarked photograph](https://github.com/GITenberg/An-Old-Babylonian-Version-of-the-Gilgamesh-Epic_11000/blob/5b22b9b87ba0cf6b97021db247987487d0bf27f1/11000-h/images/frontispiece.jpg) · [Book-cipher replay](../../../layers/R1-020_book_cipher_gilgamesh/REPRODUCE.md)

## Replay the genre fields

From the repository root, use Python 3, FFmpeg and unzip. This checks the canonical sample hash and both genre fields against the published receipt. The recording is already in the November 11 public package.

```sh
out=$(mktemp -d)
unzip -p docs/evidence/r1-reproduction-20261111/R1-Ten-Reproduction-20261111-v3.zip canonical.ape > "$out/canonical.ape"
ffmpeg -v error -n -i "$out/canonical.ape" -map_metadata -1 -c:a pcm_s16le "$out/native.wav"
python3 scripts/reproduce_r1_audio_genre.py "$out/native.wav" > "$out/genre.json"
diff -u docs/evidence/r1-followup-20261117/genre.json "$out/genre.json"
```

The [original Enkidu replay](../../../layers/R1-040_deepsound_enkidu/REPRODUCE.md) supplies the positive control for the mirror rule. For the word-pair check, split each pinned source into lowercase runs of ASCII letters. Take each consecutive pair of the right lengths and compare the order of first occurrence of each letter across both words. For example, `hoof dovoi` has the pattern `ABBC DBEBF`. Repeat for the full reversal, reversed word order, and reversal within each word. The [reading receipt](reading-controls.json) gives the input hashes and eligible counts for each case.

To repeat the music comparison, look up track ID `426173147` through the US iTunes lookup endpoint and use its public preview. Its byte hash is in the [measurement log](music-match.txt). Decode both signals to mono at 8,000 Hz. At each of the five listed preview times take a four-second window, subtract its mean, and search the puzzle recording for the strongest absolute normalized cross-correlation, subtracting the local mean at each candidate position. Repeat with the sample order reversed within each preview window. An unchanged four-second puzzle window starting at 17 seconds supplies the positive control.

A dated copy carrying the genre before the R1 puzzle was prepared would help establish where the wording entered the recording’s history.
