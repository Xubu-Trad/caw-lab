"""Reconstruct the R1 RIFF INFO block using libsndfile 1.0.31 and an in-memory WAV."""
import argparse
import ctypes as C
import ctypes.util
import hashlib
import json
import os
from pathlib import Path
import struct
import wave


class Info(C.Structure):
    _fields_ = [
        ("frames", C.c_longlong), ("samplerate", C.c_int), ("channels", C.c_int),
        ("format", C.c_int), ("sections", C.c_int), ("seekable", C.c_int),
    ]


library = C.CDLL(ctypes.util.find_library("sndfile"))
library.sf_version_string.restype = C.c_char_p
library.sf_open_fd.argtypes = [C.c_int,C.c_int,C.POINTER(Info),C.c_int]
library.sf_open_fd.restype = C.c_void_p
library.sf_set_string.argtypes = [C.c_void_p,C.c_int,C.c_char_p]
library.sf_write_short.argtypes = [C.c_void_p,C.POINTER(C.c_short),C.c_longlong]
library.sf_write_short.restype = C.c_longlong
library.sf_close.argtypes = [C.c_void_p]
assert library.sf_version_string() == b"libsndfile-1.0.31"


def write_info(fields):
    descriptor = os.memfd_create("riddle-software-control")
    try:
        handle = library.sf_open_fd(descriptor, 0x20, C.byref(Info(0,48000,2,0x010002,0,0)), 0)
        if not handle:
            raise RuntimeError("Could not open RAM-backed fixture")
        try:
            if library.sf_write_short(handle, (C.c_short * 4)(0,0,0,0), 4) != 4:
                raise RuntimeError("Silent sample write failed")
            for tag, value in fields:
                if library.sf_set_string(handle, tag, value):
                    raise RuntimeError(f"Setting tag {tag} failed")
        finally:
            if library.sf_close(handle):
                raise RuntimeError("Closing WAV failed")
        raw = os.pread(descriptor, os.fstat(descriptor).st_size, 0)
    finally:
        os.close(descriptor)
    start = raw.index(b"LIST")
    size = struct.unpack_from("<I",raw,start+4)[0]
    return raw[start:start+size+8]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wav", type=Path)
    args = parser.parse_args()
    sha = lambda data: hashlib.sha256(data).hexdigest()
    with wave.open(str(args.wav), "rb") as wav:
        pcm = wav.readframes(wav.getnframes())
    assert sha(pcm) == "9a50dfecbbe8612b6470f804e6a752d2d98ad43c2daae126fd80fc4bf094086d"
    reference = pcm[-500:]
    # Title, Album, Artist, Comments, Year, Genre, Software, Track. Preserve trailing spaces.
    # This ordering follows Audacity 3.1.3 src/export/ExportPCM.cpp:817-877.
    tags = [(1,b"Gilgamesh's Lover"),(7,b"Teh eyes to see. "),(4,b"nobody"),
            (5,b"CAW Is a decentralized social clearing house of trustless interaction "),
            (6,b"2020"),(16,b"hoof dovoi"),(3,b"RYO OS 0.43"),(9,b"7")]
    chunk = write_info(tags)
    assert chunk == reference[:244]
    id3_field = b"Software\0RYO OS 0.43"
    assert id3_field in reference[244:]
    controls = {}
    for software in (b"RYO OS 0.43", b"CONTROL", b""):
        out = write_info([(3,software)])
        offset = out.index(b"ISFT")
        length = struct.unpack_from("<I",out,offset+4)[0]
        controls[software.decode()] = out[offset+8:offset+8+length].rstrip(b"\0").decode()
    print(json.dumps({"library":library.sf_version_string().decode(),"pcm_sha256":sha(pcm),
                      "reference_tail_sha256":sha(reference),"generated_INFO_sha256":sha(chunk),
                      "generated_INFO_size":len(chunk),"full_INFO_equal":True,
                      "id3_user_text_field":"Software = RYO OS 0.43","software_controls":controls,
                      "limit":"Reproduces bytes from supplied labels. Original application and OS remain unidentified."},indent=2))
