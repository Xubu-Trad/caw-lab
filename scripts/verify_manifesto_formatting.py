#!/usr/bin/env python3
"""Check original manifesto bytes and the missing historical moonning claim."""
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('source', type=Path, help='Exact audio-extracted enkidu.full_pseudohex.txt')
    ap.add_argument('--out-dir', required=True, type=Path)
    args = ap.parse_args()
    pseudo = args.source.read_bytes()
    sha = lambda b: hashlib.sha256(b).hexdigest()
    if sha(pseudo) != '4f4edfdece802b300aeab48932b115d83eb04575753bfd128a3cc47c5cc25b19':
        raise ValueError('Wrong Enkidu input')
    if re.fullmatch(rb'[0-9U-Z]+', pseudo) is None:
        raise ValueError('Unexpected source alphabet')
    raw = bytes.fromhex(pseudo.translate(bytes.maketrans(b'UVWXYZ', b'fedcba')).decode('ascii'))
    if sha(raw) != '03fa37cfe06c7d06d590020e9fcf8c67b4131671c10d48a6f1ef0283df8cfb22':
        raise ValueError('Wrong original text')
    normalized = raw.replace(b'\t', b' ')
    if sha(normalized) != '836c98641fd1222156d49c68d210d9860319b323f890b5af82860ac14aba366c':
        raise ValueError('Wrong normalized text')
    depths = []
    internal = []
    for i, line in enumerate(raw.splitlines(), 1):
        leading = line[:len(line) - len(line.lstrip(b' \t'))]
        if b'\t' in leading:
            depths.append({'line': i, 'tabs': leading.count(b'\t')})
        if b'\t' in line[len(leading):]:
            internal.append(i)
    def positions(word):
        return [{'byte': m.start(), 'line': raw[:m.start()].count(b'\n') + 1} for m in re.finditer(rb'\b' + word + rb'\b', raw)]
    receipt = {
        'source_sha256': sha(pseudo), 'source_bytes': len(pseudo),
        'alphabetic_source_symbols': sum(65 <= c <= 90 for c in pseudo),
        'alphabetic_source_alphabet': ''.join(sorted(set(chr(c) for c in pseudo if 65 <= c <= 90))),
        'mixed_case_or_alternative_A_F_letters': False,
        'raw_manifesto_sha256': sha(raw), 'raw_bytes': len(raw),
        'normalized_sha256': sha(normalized), 'normalization': 'Each TAB replaced by one SPACE; no other changes',
        'tabs': raw.count(b'\t'), 'tab_indented_lines': depths,
        'indentation_depth_counts': dict(collections.Counter(row['tabs'] for row in depths)),
        'tabs_after_first_nonwhitespace_character': internal,
        'historical_claim': 'The archived YALE AND ME recipe requests an N from moonning -> mooning',
        'moonning_positions': positions(b'moonning'), 'mooning_positions': positions(b'mooning'),
        'conclusion': 'That exact historical N extraction has no source in the authenticated text. Other typo-based hypotheses are not excluded.'
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / 'manifesto.original_tabs.txt').write_bytes(raw)
    (args.out_dir / 'manifesto_formatting.json').write_bytes((json.dumps(receipt, indent=2) + '\n').encode())
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
