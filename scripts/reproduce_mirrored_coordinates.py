"""Compare a preserved reversed 38-pair copy with the known tablet coordinates."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
COPY = '91:731 6:078 4:968 21:199 7:6701 7:5411 3:691 21:973 31:025 2:862 21:973 3:655 3:964 1:042 11:012 9:063 41:875 1:726 6:596 6:736 21:915 22:604 7:693 2:842 32:05 2:32 31:011 3:55 1:017 61:707 21:121 41:19 2:19 7:99 11:722 02:441 4:55 12:371'

def reproduce():
    original = re.findall(r'\d+:\d+', (ROOT / 'layers/R1-010_friderici_poem_coords/EVIDENCE/full_coords.txt').read_text())
    copied = COPY.split()
    restored = [token[::-1] for token in copied[::-1]]
    if len(original) != 46 or len(copied) != 38 or restored != original[:38]:
        raise ValueError('The preserved copy does not match the known prefix')
    return len(restored)

if __name__ == '__main__':
    print(f'PASS: {reproduce()} reversed pairs equal the first 38 of 46 known coordinates')
