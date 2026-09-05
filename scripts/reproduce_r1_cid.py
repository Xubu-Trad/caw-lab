#!/usr/bin/env python3
"""Recompute the R1 APE's historical UnixFS CID using only Python's stdlib.

Usage: python3 scripts/reproduce_r1_cid.py canonical.ape --out-dir replay-cid

Fixed settings: 262144-byte chunks, DAG-PB File leaves, balanced layout,
present empty legacy link names, no directory wrapper, mode or mtime.
This bounded implementation supports a single root with at most 174 leaves.

Schemas and encoding:
https://specs.ipfs.tech/unixfs/
https://ipld.io/specs/codecs/dag-pb/spec/
"""

import argparse
import hashlib
import json
from pathlib import Path


APE_BYTES = 8968236
APE_SHA256 = "57674107710cdac58fe68b30cb3c05e3334ece55bc0d71deba84ccd2a8fb3575"
EXPECTED_CID = "QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV"
EMPTY_FILE_CID = "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH"
CONTROL_CID = "QmacgnYpjkPGGkkq9EyCM8oZ4JPcA664ehXpy3q2xZDxC8"
CHUNK_BYTES = 262144


def varint(number):
    encoded = bytearray()
    while number >= 128:
        encoded.append((number & 127) | 128)
        number >>= 7
    encoded.append(number)
    return bytes(encoded)


def blob(field, value):
    return varint(field * 8 + 2) + varint(len(value)) + value


def uint(field, value):
    return varint(field * 8) + varint(value)


def multihash(value):
    return b"\x12\x20" + hashlib.sha256(value).digest()


def base58(value):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    number = int.from_bytes(value, "big")
    result = ""
    while number:
        number, remainder = divmod(number, 58)
        result = alphabet[remainder] + result
    return "1" * (len(value) - len(value.lstrip(b"\0"))) + result


def cid(block):
    return base58(multihash(block))


def file_leaf(data):
    # UnixFS Data: Type=File (2), optional Data, filesize.
    unixfs = uint(1, 2) + (blob(2, data) if data else b"") + uint(3, len(data))
    return blob(1, unixfs)


def make_dag(data):
    chunks = [data[i:i + CHUNK_BYTES] for i in range(0, len(data), CHUNK_BYTES)] or [b""]
    if len(chunks) > 174:
        raise ValueError("This bounded replay supports at most 174 chunks")
    leaves = [file_leaf(chunk) for chunk in chunks]
    if len(leaves) == 1:
        return leaves[0], leaves, chunks
    links = []
    for leaf in leaves:
        # PBLink: Hash, explicitly present empty Name, cumulative Tsize.
        # The empty Name matches this historical import; omitting it changes CID.
        link = blob(1, multihash(leaf)) + blob(2, b"") + uint(3, len(leaf))
        links.append(blob(2, link))
    unixfs = uint(1, 2) + uint(3, len(data))
    unixfs += b"".join(uint(4, len(chunk)) for chunk in chunks)
    # DAG-PB encodes Links before Data and preserves order for equal link names.
    root = b"".join(links) + blob(1, unixfs)
    return root, leaves, chunks


def reproduce(path):
    if path.stat().st_size != APE_BYTES:
        raise ValueError("Input length does not match the canonical R1 APE")
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != APE_BYTES or digest != APE_SHA256:
        raise ValueError("Input hash does not match the canonical R1 APE")

    empty = cid(file_leaf(b""))
    if empty != EMPTY_FILE_CID:
        raise ValueError("Official empty DAG-PB file test vector failed")

    root, leaves, chunks = make_dag(data)
    actual_cid = cid(root)
    if actual_cid != EXPECTED_CID:
        raise ValueError("Computed CID does not match the book cipher")

    receipt = {
        "ape_bytes": len(data),
        "ape_sha256": digest,
        "cid": actual_cid,
        "matches_book_cipher_cid": actual_cid == EXPECTED_CID,
        "chunk_bytes": CHUNK_BYTES,
        "raw_leaves": False,
        "layout": "balanced",
        "wrap_with_directory": False,
        "link_name_encoding": "present empty legacy string",
        "leaf_nodes": len(leaves),
        "root_bytes": len(root),
        "root_sha256": hashlib.sha256(root).hexdigest(),
        "cumulative_dag_bytes": len(root) + sum(map(len, leaves)),
        "empty_file_test_vector": empty,
        "leaves": [
            {
                "index": index,
                "file_offset": index * CHUNK_BYTES,
                "file_bytes": len(chunk),
                "block_bytes": len(leaf),
                "cid": cid(leaf),
            }
            for index, (chunk, leaf) in enumerate(zip(chunks, leaves))
        ],
        "limits": (
            "Proves content-address identity for the fixed historical importer settings. "
            "Does not establish live network availability or historical custody."
        ),
    }

    # A fixed negative control, without writing or changing the input file.
    mutated = data[:-1] + bytes([data[-1] ^ 1])
    mutated_root, _, _ = make_dag(mutated)
    mutated_cid = cid(mutated_root)
    if mutated_cid == actual_cid or mutated_cid != CONTROL_CID:
        raise ValueError("One-bit negative control failed")
    control = {
        "control": "Flip low bit of last file byte only",
        "mutated_input_bytes": len(mutated),
        "mutated_root_cid": mutated_cid,
        "equals_canonical_cid": mutated_cid == actual_cid,
    }
    return receipt, control


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ape", type=Path, help="Exact canonical R1 APE file")
    parser.add_argument("--out-dir", type=Path, help="Write the two JSON receipts here")
    args = parser.parse_args()
    receipt, control = reproduce(args.ape)
    if args.out_dir is not None:
        args.out_dir.mkdir(parents=True, exist_ok=True)
        for name, value in (("cid_receipt.json", receipt), ("cid_negative_control.json", control)):
            (args.out_dir / name).write_bytes((json.dumps(value, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"cid_receipt": receipt, "negative_control": control}, indent=2))


if __name__ == "__main__":
    main()
