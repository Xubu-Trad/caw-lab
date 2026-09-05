"""Reproduce the preserved Enkidu pseudohex-to-English step; Python 3 stdlib."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "layers/R1-040_deepsound_enkidu/EVIDENCE/enkidu.full_pseudohex.txt"
TARGET = ROOT / "layers/R1-050_manifesto_final_payload/EVIDENCE/manifesto.en.txt"


def reproduce(source, target):
    expected_input = "4f4edfdece802b300aeab48932b115d83eb04575753bfd128a3cc47c5cc25b19"
    expected_output = "836c98641fd1222156d49c68d210d9860319b323f890b5af82860ac14aba366c"
    if hashlib.sha256(source).hexdigest() != expected_input:
        raise ValueError("Input hash mismatch; do not normalize or substitute the source")
    decoded = bytes.fromhex(source.decode("ascii").translate(str.maketrans("UVWXYZ", "fedcba")))
    if hashlib.sha256(decoded).hexdigest() != "03fa37cfe06c7d06d590020e9fcf8c67b4131671c10d48a6f1ef0283df8cfb22":
        raise ValueError("Intermediate hash mismatch")
    if decoded.count(b"\t") != 60:
        raise ValueError("Unexpected tab count")
    normalized = decoded.replace(b"\t", b" ")
    if len(normalized) != 10596 or hashlib.sha256(normalized).hexdigest() != expected_output:
        raise ValueError("Output receipt mismatch")
    if normalized != target:
        raise ValueError("Output differs from the committed English reference")
    return normalized


if __name__ == "__main__":
    output = reproduce(SOURCE.read_bytes(), TARGET.read_bytes())
    print("PASS: exact English reference; 10596 bytes; 60 tabs replaced with single spaces")
    print(hashlib.sha256(output).hexdigest())
