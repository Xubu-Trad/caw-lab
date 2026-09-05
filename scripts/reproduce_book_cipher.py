"""Replay the R1 coordinates against the exact public OCR edition (stdlib only).

Download the URL below unchanged and pass its filename as the only argument.
The source book is not redistributed by this repository.
"""
from pathlib import Path
import argparse,hashlib,json,re

URL='https://archive.org/download/TheEpicofGilgamesh_201606/eog_djvu.txt'
SOURCE_SHA='b66cfab2ac8fa274638036caeb9e06518f03798c84661601c95abcfccf50e33f'
EXPECTED='QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV'
ROOT=Path(__file__).resolve().parents[1]

def reproduce(path):
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA:
        raise ValueError('OCR source hash differs; preserve and investigate the variant.')
    lines=[s for s in raw.decode('utf8').splitlines() if s.strip()]
    coords=[tuple(map(int,m)) for m in re.findall(r'(\d+):(\d+)',(ROOT/'layers/R1-010_friderici_poem_coords/EVIDENCE/full_coords.txt').read_text())]
    if len(coords)!=46:raise ValueError('Expected exactly 46 coordinates')
    numbers=dict(zip('zero one two three four five six seven eight nine'.split(),'0123456789'))
    trace=[]
    for line_number,word_number in coords:
        line=lines[line_number-1]
        tokens=[t for t in (re.sub(r'^[^A-Za-z0-9]+|[^A-Za-z0-9]+$','',w) for w in line.split()) if t]
        # Every coordinate is an in-range word here. No letter fallback is needed.
        if not 1<=word_number<=len(tokens):raise ValueError('Word index out of range')
        token=tokens[word_number-1]
        char=numbers.get(token.lower(),token[0])
        trace.append({'line':line_number,'word':word_number,'output':char,'number_word':token.lower() in numbers})
    output=''.join(x['output'] for x in trace)
    if output!=EXPECTED:raise ValueError('Derived identifier differs from the historical receipt')
    return {'attempt_id':'R1-20260905-PUBLIC-BOOK-REPLAY-001','status':'PASS_REPRODUCED','source_url':URL,'source_bytes':len(raw),'source_sha256':SOURCE_SHA,'nonempty_lines':len(lines),'coordinate_count':len(coords),'word_selections':len(trace),'fallback_selections':0,'number_word_selections':sum(x['number_word'] for x in trace),'output':output,'trace':trace,'limits':'Reproduces the known CID from one exact public OCR edition. No target character is used in selection. Historical novelty, live IPFS availability and independent audio extraction are not established.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('corpus',type=Path,help=URL)
    print(json.dumps(reproduce(parser.parse_args().corpus),indent=2))
