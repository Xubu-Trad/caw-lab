# R1-020 - book-cipher receipt verification

This layer verifies the committed book-cipher receipts only.

## Inputs
- `layers/R1-020_book_cipher_gilgamesh/EVIDENCE/full_coords_from_history.txt`
- `layers/R1-020_book_cipher_gilgamesh/EVIDENCE/cids.txt`
- `layers/R1-020_book_cipher_gilgamesh/EVIDENCE/history_extracted_cids.tsv`

## Run from repo root
    set -Eeuo pipefail; IFS=$'\n\t'; LC_ALL=C
    sha256sum \
      layers/R1-020_book_cipher_gilgamesh/EVIDENCE/full_coords_from_history.txt \
      layers/R1-020_book_cipher_gilgamesh/EVIDENCE/cids.txt \
      layers/R1-020_book_cipher_gilgamesh/EVIDENCE/history_extracted_cids.tsv
    sed -n '1,20p' layers/R1-020_book_cipher_gilgamesh/EVIDENCE/full_coords_from_history.txt
    sed -n '1,20p' layers/R1-020_book_cipher_gilgamesh/EVIDENCE/cids.txt
    sed -n '1,20p' layers/R1-020_book_cipher_gilgamesh/EVIDENCE/history_extracted_cids.tsv

## Expected result
The committed text receipts hash cleanly and preview the coordinate and CID-candidate state currently promoted into canon for the book-cipher layer.
