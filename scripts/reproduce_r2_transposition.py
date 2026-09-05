"""Reproduce the zrUfKaKV hex transposition with exact hashes and inverse checks.

Usage: python r2_decode.py path/to/zrUfKaKV.txt --out-dir decoded
The source file is never modified. No network access or external packages.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

HEX_SHA = '18f043170bc47a7d3aa9ee6989fe964803d240c90d62717b7fb7ad16539acd76'
BYTES_SHA = 'a7f4839ffa14040e5a68d05ba668826ddcbda9bcdf28f5f8e5a59390a898d92c'
ORIGIN_SHA = 'f8aeadf1d0f7933a5ae87ccc22ca4d0ad41ee038da85f785bb7a15feb7f8a12f'
READING_SHA = '2a77d034354b3ee698dd0266f93dfd5627e033cb8f79ec891498b80b7eab0e52'
N = 2884

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def decode(source: bytes) -> tuple[bytes, bytes, dict]:
    # Only ASCII whitespace and hexadecimal letter case may vary in the wrapper.
    text = source.decode('ascii')
    compact = ''.join(c for c in text if c not in ' \t\r\n\v\f').lower()
    if len(compact) != N or any(c not in '0123456789abcdef' for c in compact):
        raise ValueError('Expected exactly 2884 hexadecimal digits.')
    if sha(compact.encode('ascii')) != HEX_SHA:
        raise ValueError('Source hex SHA256 does not match the verified payload.')
    if sha(bytes.fromhex(compact)) != BYTES_SHA:
        raise ValueError('Decoded input SHA256 does not match.')
    indexes = [(641 * j) % N for j in range(N)]
    if len(set(indexes)) != N or (641 * 9) % N != 1:
        raise RuntimeError('Permutation or inverse verification failed.')
    origin_hex = ''.join(compact[i] for i in indexes)
    origin = bytes.fromhex(origin_hex)
    reading = origin[-2:] + origin[:-2]
    # Both descriptions must reproduce every original hex digit, without padding.
    reencoded_origin = ''.join(origin_hex[(9*j) % N] for j in range(N))
    reading_hex = reading.hex()
    reencoded_reading = ''.join(reading_hex[(4+9*j) % N] for j in range(N))
    direct_reading_hex = ''.join(compact[(320+641*j) % N] for j in range(N))
    if reencoded_origin != compact or reencoded_reading != compact:
        raise RuntimeError('Inverse did not reproduce the original hex exactly.')
    if bytes.fromhex(direct_reading_hex) != reading:
        raise RuntimeError('Declared reading rotation does not match direct formula.')
    if sha(origin) != ORIGIN_SHA or sha(reading) != READING_SHA:
        raise RuntimeError('Output SHA256 mismatch.')
    return origin, reading, {
        'source_file_sha256': sha(source),
        'wrapper_whitespace_removed': len(text) - len(compact),
        'hex_digits': N,
        'normalized_hex_sha256': HEX_SHA,
        'decoded_input_sha256': BYTES_SHA,
        'origin_recipe': 'P[j] = C[(641*j) mod 2884]; hex-decode P',
        'reading_rotation': 'Move the final two bytes (th) to the front, with no edits.',
        'reading_recipe': 'R[j] = C[(320+641*j) mod 2884]; hex-decode R',
        'origin_inverse': 'C[j] = P[(9*j) mod 2884]',
        'reading_inverse': 'C[j] = R[(4+9*j) mod 2884]',
        'output_bytes': len(origin),
        'origin_sha256': ORIGIN_SHA,
        'reading_sha256': READING_SHA,
        'bijection_uses_every_hex_digit_once': True,
        'both_inverse_roundtrips_exact': True,
        'no_padding_dropped_bytes_or_spelling_repairs': True,
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    origin, reading, receipt = decode(args.input.read_bytes())
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / 'origin.txt').write_bytes(origin)
    (args.out_dir / 'reading_rotation.txt').write_bytes(reading)
    (args.out_dir / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
