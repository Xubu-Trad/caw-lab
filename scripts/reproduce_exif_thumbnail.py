"""Identify the tablet's EXIF thumbnail and compare two transcribed hex prefixes."""
from pathlib import Path
import hashlib
import json
import zlib

ROOT = Path(__file__).resolve().parents[1]

def reproduce():
    png = (ROOT / 'docs/assets/r1-tablet.png').read_bytes()
    if hashlib.sha256(png).hexdigest() != '889253e7fa85f5e5fd05622b8a105fd61acf83bdfdae3e600bdfedd173b2da41':
        raise ValueError('Unexpected tablet bytes')
    profile = zlib.decompress(png[0x40:])
    lines = profile.decode('ascii').splitlines()
    exif = bytes.fromhex(''.join(lines[3:]))
    if len(exif) != int(lines[2]) or len(exif) != 17282 or exif[:6] != b'Exif\0\0':
        raise ValueError('Unexpected EXIF profile')
    start = exif.find(b'\xff\xd8\xff')
    end = exif.rfind(b'\xff\xd9') + 2
    thumbnail = exif[start:end]
    digest = hashlib.sha256(thumbnail).hexdigest()
    if start != 334 or len(thumbnail) != 16948 or digest != 'd01b9f33ccbfbee1851c3c771df07536238340841a8d31feb913cfcadfac88d1':
        raise ValueError('Unexpected thumbnail bytes')
    matches = []
    for prefix, expected in [('4f4e7a01eb9aaec62c111de45850199c', 25222), ('03135d96d21d45bc8', 12511)]:
        offset = exif.hex().find(prefix)
        if offset != expected:
            raise ValueError('Prefix mismatch')
        matches.append({'prefix': prefix, 'hex_digit_offset': offset, 'byte_aligned': offset % 2 == 0})
    return {'thumbnail_bytes': len(thumbnail), 'thumbnail_sha256': digest, 'prefix_matches': matches,
            'limits': 'Prefix comparison only, not full screenshot OCR. Ordinary EXIF thumbnail; no new cipher layer claimed.'}

if __name__ == '__main__':
    print(json.dumps(reproduce(), indent=2))
