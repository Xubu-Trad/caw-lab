"""
Base91 (aka "base91") encode/decode utilities.

Why this exists:
- Your logs show /tmp/b91.py became corrupted via paste, causing SyntaxError.
- This file lives in-repo, is importable, and is self-tested via doctest.

Run:
  python3 -m doctest -v tools/b91.py
"""

from __future__ import annotations

import logging
from typing import Dict

log = logging.getLogger(__name__)

ALPHABET = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    "!#$%&()*+,./:;<=>?@[]^_`{|}~\""
)
assert len(ALPHABET) == 91, "base91 alphabet must be 91 chars"

_DEC: Dict[str, int] = {c: i for i, c in enumerate(ALPHABET)}

def encode(data: bytes) -> str:
    """
    >>> encode(b"")
    ''
    >>> decode(encode(b"hello"))
    b'hello'
    """
    assert isinstance(data, (bytes, bytearray))
    n = 0
    b = 0
    out = []
    for byte in data:
        b |= byte << n
        n += 8
        if n > 13:
            v = b & 8191
            if v > 88:
                b >>= 13
                n -= 13
            else:
                v = b & 16383
                b >>= 14
                n -= 14
            out.append(ALPHABET[v % 91])
            out.append(ALPHABET[v // 91])
    if n:
        out.append(ALPHABET[b % 91])
        if n > 7 or b > 90:
            out.append(ALPHABET[b // 91])
    return "".join(out)

def decode(s: str) -> bytes:
    """
    Ignores whitespace; errors on any other non-alphabet char.

    >>> decode(encode(b""))
    b''
    >>> decode(encode(b"hello"))
    b'hello'
    >>> import os
    >>> x = os.urandom(64)
    >>> decode(encode(x)) == x
    True
    """
    assert isinstance(s, str)
    v = -1
    b = 0
    n = 0
    out = bytearray()

    for ch in s:
        if ch not in _DEC:
            if ch.isspace():
                continue
            raise ValueError(f"invalid base91 char: {ch!r}")
        c = _DEC[ch]
        if v < 0:
            v = c
            continue

        v += c * 91
        b |= v << n
        n += 13 if (v & 8191) > 88 else 14

        while n >= 8:
            out.append(b & 255)
            b >>= 8
            n -= 8
        v = -1

    if v >= 0:
        b |= v << n
        n += 7
        while n >= 8:
            out.append(b & 255)
            b >>= 8
            n -= 8

    return bytes(out)
