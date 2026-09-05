"""Verify canonical R1 audio and extract its Enkidu file without running DeepSound.

Requires Python cryptography and a PCM16 WAV decoded losslessly by FFmpeg.
Example: ffmpeg -v error -i canonical.ape -c:a pcm_s16le canonical.wav
Then: python reproduce_ape_to_enkidu.py canonical.ape canonical.wav
No recovered content is executed. Optional --output writes a new file only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import wave
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

APE_SHA = '57674107710cdac58fe68b30cb3c05e3334ece55bc0d71deba84ccd2a8fb3575'
PCM_SHA = '9a50dfecbbe8612b6470f804e6a752d2d98ad43c2daae126fd80fc4bf094086d'
ENKIDU_SHA = '4f4edfdece802b300aeab48932b115d83eb04575753bfd128a3cc47c5cc25b19'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def unpack_normal(pcm):
    # Openwall's documented DeepSound normal-quality LSB ordering.
    assert len(pcm) % 4 == 0
    return bytes(((pcm[i] & 15) << 4) | (pcm[i+2] & 15)
                 for i in range(0, len(pcm), 4))

def extract(ape_path, wav_path):
    ape = ape_path.read_bytes()
    assert len(ape) == 8968236 and sha(ape) == APE_SHA, 'Wrong APE bytes'
    with wave.open(str(wav_path), 'rb') as wav:
        assert (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getnframes()) == (2, 2, 48000, 6491116)
        pcm = wav.readframes(wav.getnframes())
    assert sha(pcm) == PCM_SHA, 'Decoded samples differ'
    head = unpack_normal(pcm[:104])
    assert head[:6] == b'DSCF\x04\x01', 'Missing normal-quality encrypted DeepSound header'
    key = b'enkidu'.ljust(32, b'\x00')
    assert hashlib.sha1(key).digest() == head[6:26], 'Password verifier mismatch'

    # Decrypt only the 32-byte file header first. No target payload is consulted.
    first_ct = unpack_normal(pcm[104:104+32*4])
    decryptor = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
    file_header = decryptor.update(first_ct) + decryptor.finalize()
    assert file_header[:4] == b'DSSF'
    name = file_header[4:24].rstrip(b'\0').decode('ascii')
    length = int.from_bytes(file_header[24:28], 'big')
    assert 0 < length <= 1000000, 'Unexpected file length'
    assert file_header[28:32] == bytes(4)
    plaintext_length = 32 + length + 8
    ciphertext_length = (plaintext_length + 15) // 16 * 16
    ct = unpack_normal(pcm[104:104+ciphertext_length*4])
    decryptor = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
    plain = decryptor.update(ct) + decryptor.finalize()
    assert plain[:32] == file_header
    payload = plain[32:32+length]
    assert plain[32+length:32+length+8] == b'\0\0\0\0DSSF', 'Footer mismatch'
    assert name == 'enkidu.txt' and sha(payload) == ENKIDU_SHA, 'Extracted output differs from pinned evidence'
    return payload, {
        'status': 'PASS', 'ape_bytes': len(ape), 'ape_sha256': sha(ape),
        'pcm_bytes': len(pcm), 'pcm_sha256': sha(pcm),
        'pcm_sample_format': '48000 Hz, stereo, signed 16-bit little-endian',
        'samples_per_channel': 6491116, 'lsb_container_pcm_offset': 0,
        'header_hex': head.hex(), 'mode': 4, 'encrypted': 1,
        'password': 'enkidu', 'key': 'ASCII zero-padded to 32 bytes',
        'cipher': 'AES-256-ECB', 'ciphertext_container_offset': 26,
        'ciphertext_bytes_consumed': ciphertext_length,
        'filename': name, 'declared_payload_bytes': length,
        'payload_sha256': sha(payload), 'footer_hex': '0000000044535346',
        'limitation': 'Reproduces the known Enkidu file; does not establish a new riddle layer or exhaust other possible audio steganography.'
    }

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('ape', type=Path)
    p.add_argument('wav', type=Path)
    p.add_argument('--output', type=Path)
    p.add_argument('--receipt', type=Path)
    a = p.parse_args()
    payload, receipt = extract(a.ape, a.wav)
    if a.output:
        with a.output.open('xb') as f:
            f.write(payload)
    text = json.dumps(receipt, indent=2) + '\n'
    if a.receipt:
        a.receipt.write_text(text, encoding='utf-8')
    print(text)
