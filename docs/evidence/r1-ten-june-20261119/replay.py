"""Check the June 9 thread, tablet verse, decoded R1 audio tail and affine example offline."""
import argparse
import hashlib
import json
from html.parser import HTMLParser
from math import gcd
from pathlib import Path

CID = "QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV"
COMMENT = b"CAW Is a decentralized social clearing house of trustless interaction "
VERSE_PREFIX = "The archievest speaks truest of the orginal 11"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_hash(data, expected, label):
    require(hashlib.sha256(data).hexdigest() == expected, f"{label} SHA-256 mismatch")


class Thread(HTMLParser):
    """Read Twitter's tweet paragraphs and the link destinations within each one."""

    def __init__(self):
        super().__init__()
        self.posts = []
        self.words = None
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "p" and "tweet-text" in attrs.get("class", "").split():
            self.words = []
            self.links = []
        elif self.words is not None and tag == "a" and "data-expanded-url" in attrs:
            self.links.append(attrs["data-expanded-url"])
        elif self.words is not None and tag == "br":
            self.words.append(" ")

    def handle_data(self, data):
        if self.words is not None:
            self.words.append(data)

    def handle_endtag(self, tag):
        if tag == "p" and self.words is not None:
            self.posts.append((" ".join("".join(self.words).split()), self.links))
            self.words = None


def check_thread(data):
    check_hash(data, "dd951b0886fab4b18053a92d416494422dcc08f174e18b69f6a643c4cb7d3731", "archive HTML")
    thread = Thread()
    thread.feed(data.decode("utf-8"))
    thread.close()
    markers = {
        "6/": ["only the, his lover may hear"],
        "8/ (a)": [VERSE_PREFIX],
        "12/ (b)": [CID],
        "13/": ["IPFS download file (file with no extension)", "Finally found .APE extension"],
        "15/": ["DEEP SOUND 2.0", "password", "enkidu"],
        "16/": ["opened enkidu.txt", "hex with missing letters"],
        "17/": ["Atbash"],
        "18/": ["Atbash", "proposal text"],
        "19/": ["The final version"],
    }
    urls = {"12/ (b)": "https://ipfs.io/ipfs/" + CID, "19/": "https://pastebin.com/yhcajZq0"}
    for prefix, phrases in markers.items():
        matches = [(text, links) for text, links in thread.posts if text.startswith(prefix)]
        require(len(matches) == 1, f"Expected one archived post starting with {prefix}")
        text, links = matches[0]
        require(all(phrase in text for phrase in phrases), f"Archived wording differs in {prefix}")
        if prefix in urls:
            require(urls[prefix] in links, f"Archived destination differs in {prefix}")
    return list(markers)


def check_tablet(data):
    check_hash(data, "889253e7fa85f5e5fd05622b8a105fd61acf83bdfdae3e600bdfedd173b2da41", "tablet")
    # Hex starts after the first three IEND checksum bytes. The fourth is at EOF before two CRLFs.
    marker = b"\x00\x00\x00\x00IEND\xae\x42\x60"
    require(data.count(marker) == 1 and data.endswith(b"\x82\r\n\r\n"), "Unexpected IEND boundary")
    encoded = data.split(marker)[1][:-5]
    verse = bytes.fromhex(encoded.decode("ascii"))
    check_hash(verse, "c1dfa2443b0a167034ae06ea67bcac44f1c3714d54a8c671d971b9613f5de19a", "IEND verse")
    first = verse.decode("ascii").splitlines()[0]
    require(first == VERSE_PREFIX + ", but not the 12th", "First line differs")
    return first


def check_pcm(pcm):
    check_hash(pcm, "9a50dfecbbe8612b6470f804e6a752d2d98ad43c2daae126fd80fc4bf094086d", "raw PCM")
    tail = pcm[-500:]
    check_hash(tail, "bdae1720729520529d098b2ee8d7e504b9e1e69350b2c70f4fb87d38e207c2e4", "PCM tail")
    split = 8 + int.from_bytes(tail[4:8], "little")
    info, id3 = tail[:split], tail[split:]
    require(info[:4] == b"LIST" and info[8:12] == b"INFO" and len(info) == 244, "LIST/INFO chunk differs")
    require(id3[:4] == b"id3 " and 8 + int.from_bytes(id3[4:8], "little") == len(id3) == 256, "id3 chunk differs")
    # These offsets apply only to the hash-verified chunks above. INFO stores a NUL-padded
    # string. ID3v2.3 COMM has two flag bytes, an encoding, three language bytes and a description terminator.
    info_size = int.from_bytes(info[84:88], "little")
    require(info[80:84] == b"ICMT" and info[88:88 + info_size].rstrip(b"\0") == COMMENT, "INFO comment differs")
    frame = id3.index(b"COMM")
    payload_size = int.from_bytes(id3[frame + 4:frame + 8], "big")
    require(id3[frame + 8:frame + 10] == bytes(2), "COMM flags differ")
    payload = id3[frame + 10:frame + 10 + payload_size]
    require(payload == bytes(5) + COMMENT, "ID3 comment differs")
    return {"offset_in_pcm": len(pcm)-len(tail), "info_bytes": len(info), "id3_bytes": len(id3),
            "comment_in_both_fields": COMMENT.decode("ascii")}


def check_affine():
    maps = [(a, b) for a in range(26) if gcd(a, 26) == 1 for b in range(26) if (a, b) != (1, 0)]
    require(len(maps) == 311 and sum(a == 1 for a, b in maps) == 25, "Unexpected affine count")
    phrase = "hoof dovoi"
    result = "".join(chr(97 + (19 * (ord(c) - 97) + 24) % 26) if c != " " else c for c in phrase)
    require(result == "beep deheu", "Affine counterexample differs")
    return {"nonidentity_maps": len(maps), "included_nonidentity_caesar_shifts": 25, "a19_b24": result}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive_html", type=Path, help="Original Wayback id_ response body, saved as HTML")
    parser.add_argument("tablet_png", type=Path, help="Original R1 tablet PNG")
    parser.add_argument("raw_pcm", type=Path, help="FFmpeg s16le sample bytes from canonical.ape, without a WAV header")
    args = parser.parse_args()
    try:
        result = {"thread_posts_checked": check_thread(args.archive_html.read_bytes()),
                  "verse_first_line": check_tablet(args.tablet_png.read_bytes()),
                  "pcm_tail": check_pcm(args.raw_pcm.read_bytes()), "affine": check_affine()}
    except (ValueError, OSError) as error:
        parser.exit(1, f"Check failed: {error}\n")
    print(json.dumps(result, indent=2))
