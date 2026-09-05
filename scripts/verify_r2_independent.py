#!/usr/bin/env python3
"""Independently replay R2 by scattering source digits; Python standard library only."""
import argparse
import collections
import csv
import hashlib
import json
import math
from pathlib import Path

SOURCE_SHA = '18f043170bc47a7d3aa9ee6989fe964803d240c90d62717b7fb7ad16539acd76'
READING_SHA = '2a77d034354b3ee698dd0266f93dfd5627e033cb8f79ec891498b80b7eab0e52'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def decode(source):
    # Require the exact source. This audit performs no input normalization.
    if len(source) != 2884 or digest(source) != SOURCE_SHA:
        raise ValueError('Source does not match the pinned 2884-byte hex artifact')
    cipher = source.decode('ascii')
    slots = [None] * len(cipher)
    for i, digit in enumerate(cipher):
        destination = (9 * i + 4) % len(cipher)
        if slots[destination] is not None:
            raise ValueError('Permutation collision')
        slots[destination] = digit
    if None in slots:
        raise ValueError('Unfilled destination')
    reading_hex = ''.join(slots)
    reading = bytes.fromhex(reading_hex)
    encoded = ''.join(reading_hex[(9 * i + 4) % len(cipher)] for i in range(len(cipher)))
    if encoded != cipher or digest(reading) != READING_SHA:
        raise ValueError('Round trip or expected output failed')
    return cipher, reading


def rank_affine_classes(cipher):
    # A robustness check using unrelated, locally bundled Python documentation.
    # No R2 plaintext or CAW manifesto is used to build the score table.
    import pydoc_data.topics
    corpus = '\n'.join(pydoc_data.topics.topics[k] for k in sorted(pydoc_data.topics.topics)).encode().lower()
    singles = collections.Counter(corpus)
    pairs = collections.Counter(zip(corpus, corpus[1:]))
    scores = [[math.log((pairs[a, b] + .05) / (singles[a] + .05 * 256)) for b in range(256)] for a in range(256)]
    digits = [int(c, 16) for c in cipher]
    n = len(digits)
    rows = []
    for stride in range(1, n):
        if math.gcd(stride, n) != 1:
            continue
        for parity in (0, 1):
            ordered = [digits[(stride * j + parity) % n] for j in range(n)]
            raw = bytes((ordered[j] << 4) | ordered[j + 1] for j in range(0, n, 2))
            candidate = raw.lower()
            score = sum(scores[candidate[j]][candidate[(j + 1) % len(candidate)]] for j in range(len(candidate))) / len(candidate)
            rows.append({'stride': stride, 'parity': parity, 'score': score, 'sha256': digest(raw)})
    rows.sort(key=lambda row: row['score'], reverse=True)
    return {
        'training': 'Python pydoc_data.topics, sorted topics joined by LF, UTF-8, lowercase',
        'training_sha256': digest(corpus), 'training_bytes': len(corpus),
        'classes_tested': len(rows), 'top_five': rows[:5],
        'rank_of_641_parity_zero': next(i + 1 for i, row in enumerate(rows) if row['stride'] == 641 and row['parity'] == 0),
        'scope': 'All invertible hex strides and both nibble parities; circular scoring identifies byte rotations. Does not choose a sentence boundary.',
        'limit': 'A heuristic robustness check, not a probability of truth or proof of author intent. Scores depend on the installed Python documentation version.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--rank', action='store_true', help='Check all 2448 affine classes with unrelated documentation scores')
    args = parser.parse_args()
    cipher, reading = decode(args.source.read_bytes())
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / 'reading.txt').write_bytes(reading)
    origin = reading[2:] + reading[:2]
    (args.out_dir / 'origin.txt').write_bytes(origin)
    rows = []
    for i, byte in enumerate(reading):
        hi = (320 + 641 * 2 * i) % len(cipher)
        lo = (320 + 641 * (2 * i + 1)) % len(cipher)
        if int(cipher[hi] + cipher[lo], 16) != byte:
            raise ValueError('Character map failed')
        rows.append({'output_byte': i, 'character_escaped': repr(chr(byte)), 'byte_hex': f'{byte:02x}', 'input_hex_high_position': hi, 'input_hex_low_position': lo})
    with (args.out_dir / 'character_map.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    receipt = {
        'source_sha256': SOURCE_SHA, 'source_hex_characters': len(cipher),
        'rule': 'Assign cipher digit C[i] to reading-hex position (9*i+4) mod 2884',
        'every_destination_filled_once': True, 'exact_inverse': True,
        'reading_bytes': len(reading), 'reading_words_whitespace_split': len(reading.split()),
        'reading_sha256': digest(reading), 'origin_sha256': digest(origin),
        'rotation': 'Reading moves final two bytes th from raw origin to front; semantic boundary choice, no edits',
        'character_map_rows': len(rows),
        'character_map_sha256': digest((args.out_dir / 'character_map.csv').read_bytes()),
        'limit': 'Round-trip equality alone cannot establish meaningful decoding. The complete coherent message and independently scored ranking provide additional evidence.'
    }
    if args.rank:
        receipt['unrelated_corpus_ranking'] = rank_affine_classes(cipher)
    (args.out_dir / 'verification.json').write_bytes((json.dumps(receipt, indent=2) + '\n').encode())
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
