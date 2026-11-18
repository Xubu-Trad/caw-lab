"""Read both genre fields from the pinned R1 PCM samples. Python 3 stdlib."""
import argparse
import hashlib
import json
from pathlib import Path
import string
import wave


def replay(wav):
    with wave.open(str(wav), "rb") as audio:
        if audio.getparams()[:4] != (2, 2, 48000, 6491116):
            raise ValueError("Expected the canonical 48 kHz stereo WAV")
        pcm = audio.readframes(audio.getnframes())
    pcm_hash = hashlib.sha256(pcm).hexdigest()
    if pcm_hash != "9a50dfecbbe8612b6470f804e6a752d2d98ad43c2daae126fd80fc4bf094086d":
        raise ValueError("Decoded samples differ from the canonical R1 recording")
    tail = pcm[-500:]
    tail_hash = hashlib.sha256(tail).hexdigest()
    if tail_hash != "bdae1720729520529d098b2ee8d7e504b9e1e69350b2c70f4fb87d38e207c2e4":
        raise ValueError("Terminal metadata hash mismatch")

    # Verified offsets within these exact RIFF INFO and ID3v2.3 chunks.
    if tail[:4] != b"LIST" or tail[8:12] != b"INFO" or tail[244:248] != b"id3 ":
        raise ValueError("Expected the two terminal RIFF chunks")
    if tail[174:178] != b"IGNR" or tail[478:482] != b"TCON" or tail[486:489] != bytes(3):
        raise ValueError("Expected the two genre field headers")
    info_size = int.from_bytes(tail[178:182], "little")
    id3_size = int.from_bytes(tail[482:486], "big")
    info = tail[182:182 + info_size].rstrip(b"\0").decode("ascii")
    id3 = tail[489:488 + id3_size].decode("latin1")
    if info != id3 or info != "hoof dovoi":
        raise ValueError("Genre fields differ from the recorded result")

    alphabet = string.ascii_lowercase
    return {
        "pcm_sha256": pcm_hash,
        "tail_sha256": tail_hash,
        "tail_start_pcm_byte": len(pcm) - len(tail),
        "genre_INFO": info,
        "genre_ID3": id3,
        "whole_string_backwards": info[::-1],
        "words_in_reverse_order": " ".join(reversed(info.split())),
        "each_word_backwards": " ".join(word[::-1] for word in info.split()),
        "full_alphabet_mirror": info.translate(str.maketrans(alphabet, alphabet[::-1])),
        "enkidu_substitution_on_uppercase": info.upper().translate(str.maketrans("UVWXYZ", "fedcba")),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wav", type=Path)
    print(json.dumps(replay(parser.parse_args().wav), indent=2))
