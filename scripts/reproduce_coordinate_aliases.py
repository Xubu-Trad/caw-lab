"""Verify single-channel strings as projections of known coordinates. Requires Pillow."""
from pathlib import Path
from PIL import Image
import json,hashlib,re
root=Path(__file__).resolve().parents[1]
png=root/'docs/assets/r1-tablet.png'
raw=png.read_bytes(); assert hashlib.sha256(raw).hexdigest()=='889253e7fa85f5e5fd05622b8a105fd61acf83bdfdae3e600bdfedd173b2da41'
a=Image.open(png);rgb_image=a.convert('RGB');pixels=list(zip(*(iter(rgb_image.tobytes()),)*3))
bits=[c&1 for p in pixels for c in p]
def pack(bits):return bytes(sum(b<<(7-k) for k,b in enumerate(bits[i:i+8])) for i in range(0,len(bits)-7,8))
rgb=pack(bits); coords=rgb.split(b'\0',1)[0]
assert len(coords.splitlines())==46
r=pack([p[0]&1 for p in pixels]);g=pack([p[1]&1 for p in pixels]);b=pack([p[2]&1 for p in pixels])
known_coords=b'\n'.join(f'{a}:{b}'.encode('ascii') for a,b in re.findall(r'(\d+):(\d+)',(root/'layers/R1-010_friderici_poem_coords/EVIDENCE/full_coords.txt').read_text(encoding='utf8')))
assert coords==known_coords
knownbits=[int(k) for byte in known_coords+b'\0' for k in f'{byte:08b}']
result={'png_sha256':hashlib.sha256(raw).hexdigest(),'rgb_coordinates_bytes':len(coords),'rgb_coordinates_sha256':hashlib.sha256(coords).hexdigest(),'known_bit_count_including_NUL':len(knownbits),'channels':[]}
for i,(name,lane) in enumerate(zip('rgb',(r,g,b))):
 predicted=pack(knownbits[i::3]); assert lane[:len(predicted)]==predicted
 text_runs=[{'offset':m.start(),'length':len(m[0]),'text':m[0].decode('ascii')} for m in re.finditer(rb'[\x20-\x7e]{6,}',lane[:130])]
 result['channels'].append({'channel':name,'predicted_bytes':len(predicted),'prediction_sha256':hashlib.sha256(predicted).hexdigest(),'predicted_hex':predicted.hex(),'predicted_text':predicted.decode('ascii','replace'),'matches_original_lane_prefix':True,'printable_runs':text_runs})
red_first_row_reverse=r[:80][::-1]
assert hashlib.sha256(red_first_row_reverse).hexdigest()=='f81be2b74ab9d158b98ee750ca1db954564e882c783f7e4660477a0e0ade046c'
result['red_first_row_reversed_bytes']={'method':'Reverse the 80 red-channel bytes of the first 640-pixel row. This corresponds to horizontal reversed pixel traversal and opposite bit packing.','text':red_first_row_reverse.decode('ascii'),'sha256':hashlib.sha256(red_first_row_reverse).hexdigest(),'fully_predictable_from_known_coordinates':True}
print(json.dumps(result,indent=2))
