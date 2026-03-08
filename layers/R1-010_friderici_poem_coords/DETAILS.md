# R1-010 details

## Scope
This layer covers the image-side hidden-text and coordinate receipts that bridge the public clue image into the book-cipher stage.

## Proven receipts
- The image contains a hidden textual layer that yields the poem / verse instructions.
- The committed canon evidence includes the poem text itself.
- The committed canon evidence includes the 46-coordinate list.
- The committed canon evidence includes the fallback letter-count note that explains how to proceed when a LINE:WORD lookup fails.
- The committed canon evidence includes the EXIF rebuild receipt text from prior work.

## Why this layer matters
This is the instruction layer. It is where the public image stops being "just an image" and starts behaving like a cipher carrier:
- it introduces mirror / backwards procedure
- it frames corpus choice problems
- it hands off the coordinate material used in the next layer

## Evidence in this layer
- `EVIDENCE/poem.txt`
- `EVIDENCE/full_coords.txt`
- `EVIDENCE/fallback_lettercount.txt`
- `EVIDENCE/png_exif_rebuild_v1/exiftool.txt`

## Auditor notes
A reader inspecting this layer should be able to answer:
1. What was extracted from the image?
2. What coordinate list is being treated as canon?
3. What fallback rule is documented for insufficient word counts?
4. What image-metadata receipt text was preserved?

## Boundaries
This layer does not itself prove which Gilgamesh corpus slice is final. That belongs in R1-020.
