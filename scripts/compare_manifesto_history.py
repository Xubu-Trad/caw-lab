"""Compare a local clone of the public manifesto history with exact decoded Enkidu."""
from pathlib import Path
import argparse, hashlib, json, subprocess

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('repository',type=Path)
    ap.add_argument('enkidu',type=Path)
    ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args()
    pseudo=args.enkidu.read_bytes()
    sha=lambda b:hashlib.sha256(b).hexdigest()
    if sha(pseudo)!='4f4edfdece802b300aeab48932b115d83eb04575753bfd128a3cc47c5cc25b19':
        raise ValueError('Wrong Enkidu source')
    raw=bytes.fromhex(pseudo.translate(bytes.maketrans(b'UVWXYZ',b'fedcba')).decode())
    normalized=raw.replace(b'\t',b' ')
    if sha(normalized)!='836c98641fd1222156d49c68d210d9860319b323f890b5af82860ac14aba366c':
        raise ValueError('Wrong decoded text')
    repo=args.repository.resolve()
    git=['git','-c','safe.directory='+str(repo),'-C',str(repo)]
    commits=['a5c85ac9b2f4a960964e3898637c2fe9f5cb6e87','37399aeb55974d4b09d404014865b5ef8918e9de','95da76a8ab376e871e4b579e0927b8ccc58aad4b','bdca31c8e4ae732378b345c9da585c9fec2804ec']
    rows=[]
    for commit in commits:
        data=subprocess.check_output(git+['show',commit+':README.md'])
        title,_,body=data.partition(b'\n')
        rows.append({'commit':commit,'author_date':subprocess.check_output(git+['show','-s','--format=%aI',commit],text=True).strip(),'title':title.decode(),'file_bytes':len(data),'file_sha256':sha(data),'body_bytes':len(body),'body_sha256':sha(body),'exact_normalized_manifesto_match':body==normalized})
    if [x['exact_normalized_manifesto_match'] for x in rows]!=[False,True,True,True]:
        raise ValueError('Unexpected historical comparison result')
    receipt={'repository':'https://github.com/cawdevelopment/manifesto','normalization':'Decode Enkidu U-Z to f-a; replace 60 tabs with one space each. Remove the first Markdown title line of each upstream README. No other edits.','decoded_original_sha256':sha(raw),'normalized_sha256':sha(normalized),'rows':rows,'conclusion':'The entire 10596-byte normalized audio-derived manifesto is the body of all three substantial August25,2022 commits. The later two commits only change the Markdown heading.','limit':'Exact text correspondence corroborates the recovered document. It is not proof that the repository account is the riddle author or an assertion that no additional cipher could exist.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_bytes((json.dumps(receipt,indent=2)+'\n').encode())
    print(json.dumps(receipt,indent=2))

if __name__=='__main__': main()
