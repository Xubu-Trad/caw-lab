"""Verify the downloaded May 9 PNG, May 12 paste page and November 7 raw paste."""
import argparse
import gzip
import hashlib
import html
import sys
from html.parser import HTMLParser
from pathlib import Path


class PasteText(HTMLParser):
    # A textarea treats markup inside it as text. Expand character references once.
    CDATA_CONTENT_ELEMENTS = (*HTMLParser.CDATA_CONTENT_ELEMENTS, "textarea")

    def __init__(self):
        super().__init__()
        self.parts = None
        self.pastes = []

    def handle_starttag(self, tag, attrs):
        if tag == "textarea" and "js-paste-raw" in (dict(attrs).get("class") or "").split():
            self.parts = []

    def handle_data(self, data):
        if self.parts is not None:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == "textarea" and self.parts is not None:
            self.pastes.append(html.unescape("".join(self.parts)).encode("utf-8"))
            self.parts = None


def read_response(path):
    content = path.read_bytes()
    return gzip.decompress(content) if content.startswith(b"\x1f\x8b") else content


def check(label, data, length, expected_hash):
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != length or digest != expected_hash:
        raise ValueError(f"{label}: got {len(data)} bytes, SHA-256 {digest}")
    return f"{label}: {length} bytes, SHA-256 {digest}"


def verify(image, page, raw):
    results = [check("May 9 tablet", image, 536397,
                     "889253e7fa85f5e5fd05622b8a105fd61acf83bdfdae3e600bdfedd173b2da41")]
    parser = PasteText()
    parser.feed(page.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n"))
    parser.close()
    if len(parser.pastes) != 1 or parser.parts is not None:
        raise ValueError("Expected exactly one complete js-paste-raw textarea")
    text = parser.pastes[0]
    if (text.count(b"\n"), text.count(b"\r"), text.count(b"\t"), text.endswith(b"\n")) != (154, 0, 0, False):
        raise ValueError("Unexpected May textarea whitespace")
    results.append(check("May 12 textarea", text, 10595,
                         "1addb740a13ae52274aff829cc3b627e95eee190c3cb2540c3c30bc6be2b2338"))
    results.append(check("May text with terminal LF", text + b"\n", 10596,
                         "836c98641fd1222156d49c68d210d9860319b323f890b5af82860ac14aba366c"))
    if raw != text.replace(b"\n", b"\r\n"):
        raise ValueError("November raw paste differs from the May text with CRLF line endings")
    results.append(check("November 7 raw paste", raw, 10749,
                         "5e03b441cc8dc10874f9ac956bf9c7c0574fc94e0387b3ef186661505044738b"))
    return results


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("tablet_png", type=Path)
    cli.add_argument("may_page_html", type=Path)
    cli.add_argument("november_raw", type=Path)
    args = cli.parse_args()
    try:
        lines = verify(*(read_response(p) for p in (args.tablet_png, args.may_page_html, args.november_raw)))
    except (OSError, EOFError, ValueError) as error:
        sys.exit(f"FAIL: {error}")
    print("\n".join(lines))
