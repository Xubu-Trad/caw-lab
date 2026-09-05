#!/usr/bin/env python3
"""Replay the original tablet PNG to its coordinates and literal poem. Stdlib only."""
from pathlib import Path
import argparse, hashlib, json, re, struct, zlib

ROOT = Path(__file__).resolve().parents[1]
SHA256 = '889253e7fa85f5e5fd05622b8a105fd61acf83bdfdae3e600bdfedd173b2da41'

def paeth(a, b, c):
    p = a + b - c
    distances = (abs(p-a), abs(p-b), abs(p-c))
    return (a, b, c)[distances.index(min(distances))]

def reproduce(path):
    source = path.read_bytes()
    if hashlib.sha256(source).hexdigest() != SHA256:
        raise ValueError('Input hash differs: do not mix image variants.')
    assert source[:8] == b'\x89PNG\r\n\x1a\n'
    offset, compressed, checked = 8, bytearray(), 0
    while offset + 12 <= len(source):
        size = int.from_bytes(source[offset:offset+4], 'big')
        kind = source[offset+4:offset+8]
        payload = source[offset+8:offset+8+size]
        crc_offset = offset + 8 + size
        if kind == b'IEND':
            assert size == 0
            break
        assert zlib.crc32(kind+payload) & 0xffffffff == int.from_bytes(source[crc_offset:crc_offset+4], 'big')
        checked += 1
        if kind == b'IHDR':
            width, height, depth, color, compression, filtering, interlace = struct.unpack('>IIBBBBB', payload)
            assert (width, height, depth, color, compression, filtering, interlace) == (640, 776, 8, 6, 0, 0, 0)
        elif kind == b'IDAT':
            compressed.extend(payload)
        offset = crc_offset + 4
    assert kind == b'IEND'

    # The ASCII hex interrupts the IEND CRC between its third and fourth bytes.
    expected_crc = (zlib.crc32(b'IEND') & 0xffffffff).to_bytes(4, 'big')
    assert source[crc_offset:crc_offset+3] == expected_crc[:3]
    text_start = crc_offset + 3
    text_end = source.index(expected_crc[3:], text_start)
    encoded = source[text_start:text_end]
    assert re.fullmatch(rb'[0-9a-fA-F]{2}(?: [0-9a-fA-F]{2})*', encoded)
    poem = bytes.fromhex(encoded.decode('ascii'))

    # Decode the noninterlaced RGBA PNG without relying on a permissive image library.
    raw = zlib.decompress(compressed)
    stride = width * 4
    assert len(raw) == height * (stride+1)
    previous = bytearray(stride)
    pixels = bytearray()
    for y in range(height):
        start = y * (stride+1)
        filter_type = raw[start]
        assert filter_type in range(5)
        row = bytearray(raw[start+1:start+1+stride])
        for x in range(stride):
            left = row[x-4] if x >= 4 else 0
            up = previous[x]
            upper_left = previous[x-4] if x >= 4 else 0
            predictor = (0, left, up, (left+up)//2, paeth(left, up, upper_left))[filter_type]
            row[x] = (row[x] + predictor) & 255
        pixels.extend(row)
        previous = row
    decoded = bytearray()
    value = count = 0
    for i, channel in enumerate(pixels):
        if i % 4 == 3:
            continue
        value = (value << 1) | (channel & 1)
        count += 1
        if count == 8:
            decoded.append(value)
            value = count = 0
    coords = bytes(decoded).split(b'\0', 1)[0]
    assert re.fullmatch(rb'[0-9]+:[0-9]+(?:\n[0-9]+:[0-9]+){45}', coords)
    evidence = ROOT / 'layers/R1-010_friderici_poem_coords/EVIDENCE'
    normalized_coords = ',\n'.join(coords.decode().splitlines()) + '\n'
    normalized_poem = '\n'.join(line.rstrip() for line in poem.decode().splitlines()) + '\n'
    assert normalized_coords == (evidence/'full_coords.txt').read_text(encoding='utf8')
    assert normalized_poem == (evidence/'poem.txt').read_text(encoding='utf8')
    return {
        'attempt_id': 'R1-20260905-TABLET-REPLAY-001',
        'input_sha256': SHA256, 'input_bytes': len(source),
        'preceding_valid_crc_chunks': checked, 'iend_offset': offset,
        'observed_iend_crc': source[crc_offset:crc_offset+4].hex(),
        'expected_iend_crc': expected_crc.hex(),
        'poem_hex_offset': text_start, 'poem_hex_bytes': len(encoded),
        'deferred_crc_byte_offset': text_end,
        'poem_bytes': len(poem), 'poem_sha256': hashlib.sha256(poem).hexdigest(),
        'coordinate_pairs': 46, 'coordinate_bytes': len(coords),
        'coordinates_sha256': hashlib.sha256(coords).hexdigest(),
        'coordinate_method': 'PNG unfilter; RGB channel LSBs; row-major; pack MSB first; prefix before first NUL',
        'normalized_existing_receipts_match': True,
        'limits': 'Reproduces known coordinates and poem. Does not solve the corpus-to-CID step or establish historical novelty.'
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', type=Path, default=ROOT/'docs/assets/r1-tablet.png')
    args = parser.parse_args()
    print(json.dumps(reproduce(args.image), indent=2))
