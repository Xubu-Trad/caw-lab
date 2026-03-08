# R2-010 details

## Role in the chain
This layer records the recovered-payload triage for the second riddle.

## Exact canon constants
- decoded-file receipt entries:
  - `INPUT/cleaned_hex_ready.txt` -> bytes `3129`, sha256 `158e412566e1b318b86de33e19aba3fe714d6a0adabbbd13585d75fde1994701`, head hex `ffd8ffe000104a464946000101000001`
  - `INPUT/revised_output_hex.txt` -> bytes `3251`, sha256 `67588723e6398a7e920f3a0f4ad05ea4d565960fe1921b0827fa0314c2497fdb`, head hex `ffd8ffe000104a464946000101000001`
  - `INPUT/manifesto_replicate_output_4.3_AUDIO_HEX.txt` -> bytes `3251`, sha256 `44f8e88920f1646cc9c9ac399aac5f62e62afc5c625ab5f684a0eef0684ae3c7`, head hex `ffd8ffe000104a464946000101000001`

- trailer-family receipt entries:
  - `cleaned_hex_ready.jpg` -> eoi_offset `1354`, trailer_bytes `1773`, head_sha256 `1c177ef0d80173583038459325e918279ef61ff165924dac25455a629508f359`, trailer_sha256 `b469e9872446c65a7d0a0b93f425e8df5720e59f01b2d946f433b3e1a4ef28ab`
  - `revised_output_hex.jpg` -> eoi_offset `1476`, trailer_bytes `1773`, head_sha256 `b8920a338a2e9015a7ea96579c2e6fcb9238ff1ae2a1638d0531661ace8c737f`, trailer_sha256 `b469e9872446c65a7d0a0b93f425e8df5720e59f01b2d946f433b3e1a4ef28ab`
  - `manifesto_replicate_output_4.3_AUDIO_HEX.jpg` -> eoi_offset `-1`, trailer_bytes `0`, head_sha256 `44f8e88920f1646cc9c9ac399aac5f62e62afc5c625ab5f684a0eef0684ae3c7`

- numeric anchor receipt family:
  - `21000000`
  - `10500000`
  - `5250000`
  - `2625000`
  - `1312500`
  - `120`
  - `21000000:10500000:5250000:2625000:1312500`
  - `21000000-10500000-5250000-2625000-1312500`

## What this layer proves
- three preserved decoded payload candidates exist
- two of them converge on the exact same trailer hash `b469e9872446c65a7d0a0b93f425e8df5720e59f01b2d946f433b3e1a4ef28ab`
- the shared-trailer pair is the strongest current public replay lane
- the numeric anchor family is preserved independently and must remain attached to this lane

## What this layer still does not prove
- no final plaintext
- no final interpretation of the shared trailer family
- no single deterministic end-to-end replay yet
