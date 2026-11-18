#!/usr/bin/env python3
"""Replay the R1 upper strip from the source photograph. Requires Python 3 and Pillow."""

import argparse
import hashlib
import io
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SIZE = (640, 776)
CROP = (80, 2, 560, 32)  # Pillow bounds exclude the last column and row.
PHOTO_SHA = "cb832039260309924a5dcbf039c4b5143607cdfa3f5d657c328372484a90137c"
TABLET_SHA = "889253e7fa85f5e5fd05622b8a105fd61acf83bdfdae3e600bdfedd173b2da41"
SCREEN_SHA = "78bc3d00bc473bb6c63c43e21da91f6d8179510b9ade596fca4e18dc958152a3"
COORD_SHA = "cd8b7360f4363064f6c0719d1658e859b546dc5d95a10aa026a68b268ed53998"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_hash(data, expected, label):
    require(hashlib.sha256(data).hexdigest() == expected, label + " SHA-256 mismatch")


def read_image(path, expected, mode, label):
    data = path.read_bytes()
    check_hash(data, expected, label)
    with Image.open(io.BytesIO(data)) as image:
        require(image.size == SIZE, label + " dimensions differ")
        return image.convert(mode)


def replay_rows(photo, tablet_path, coordinate_path):
    tablet = read_image(tablet_path, TABLET_SHA, "RGBA", "tablet")
    pairs = re.findall(rb"[0-9]+:[0-9]+", coordinate_path.read_bytes())
    coordinate_bytes = b"\n".join(pairs)
    check_hash(coordinate_bytes, COORD_SHA, "normalized coordinates")
    bits = [byte >> shift & 1 for byte in coordinate_bytes for shift in range(7, -1, -1)]

    area = (0, 0, SIZE[0], 92)
    target = tablet.crop(area)
    require(target.getchannel("A").getextrema() == (255, 255), "non-opaque upper pixel")
    expected = bytearray(value & 254 for value in photo.crop(area).tobytes())
    for index, bit in enumerate(bits):
        expected[index] |= bit
    actual = target.convert("RGB").tobytes()
    differences = sum(a != b for a, b in zip(expected, actual))
    require(differences == 0, f"{differences} RGB channel values differ in rows 0–91")
    last_pixel = (len(bits) - 1) // 3
    return {
        "rows_0_through_91": len(actual) // (SIZE[0] * 3),
        "pixels_compared": len(actual) // 3,
        "rgb_channel_values_compared": len(actual),
        "differing_rgb_channel_values": differences,
        "alpha": 255,
        "coordinate_bytes": len(coordinate_bytes),
        "coordinate_bits": len(bits),
        "last_coordinate_bit_xy": [last_pixel % SIZE[0], last_pixel // SIZE[0]],
        "remaining_nonzero_low_bits": sum(value & 1 for value in actual[len(bits):]),
    }


def photo_mask(photo):
    raw = photo.tobytes()
    require(raw[::3] == raw[1::3] == raw[2::3], "photograph is not grayscale")
    return bytes(gray <= 1 for gray in photo.getchannel("R").crop(CROP).tobytes())


def measure_screenshot(photo, screenshot):
    dark_source = photo.getchannel("R").load()
    screen = screenshot.load()
    thresholds = (64, 100, 128, 180)
    report = {}
    center_mask = bytearray()
    for label, bounds in (("center", CROP), ("across_width", (0, 2, 640, 64))):
        counts = {level: dict(both_dark=0, screenshot_only=0, photo_only=0, both_light=0)
                  for level in thresholds}
        x0, y0, x1, y1 = bounds
        for y in range(y0, y1):
            for x in range(x0, x1):
                rgb = screen[x, y]
                if max(rgb) - min(rgb) >= 12:
                    require(label != "center", "colored pixel in center study area")
                    continue
                intensity = sum(rgb)
                if label == "center":
                    center_mask.append(intensity < 3 * 64)
                for level in thresholds:
                    # Multiplication compares the arithmetic mean without rounding.
                    pair = (dark_source[x, y] <= 1, intensity < 3 * level)
                    key = {(True, True): "both_dark", (False, True): "screenshot_only",
                           (True, False): "photo_only", (False, False): "both_light"}[pair]
                    counts[level][key] += 1
        report[label] = counts
    return bytes(center_mask), report


def mask_path(mask):
    """One rectangle per contiguous run in a scan line, in native image coordinates."""
    x0, y0, x1, y1 = CROP
    width = x1 - x0
    require(len(mask) == width * (y1 - y0), "unexpected mask dimensions")
    segments = []
    for row in range(y1 - y0):
        cells = mask[row * width:(row + 1) * width]
        for run in re.finditer(b"\x01+", cells):
            length = run.end() - run.start()
            segments.append(f"M{x0 + run.start()} {y0 + row}h{length}v1h-{length}z")
    return " ".join(segments)


def figure_text(photo_path, screenshot_path):
    parts = ['''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1032" height="333" viewBox="0 0 1032 333" role="img" aria-labelledby="title desc">
  <title id="title">Dark pixels in the R1 upper strip</title>
  <desc id="desc">Side-by-side masks of the same area of the unmarked photograph and the hunter's screenshot. All 878 dark pixel positions coincide. The lower panels enlarge the central 96 columns five times.</desc>
  <rect width="1032" height="333" fill="#fff"/>
  <g font-family="system-ui, sans-serif" fill="#1d252c">
    <text x="24" y="35" font-size="29" font-weight="700">Dark pixels in the R1 upper strip</text>
    <text x="24" y="61" font-size="17">Columns 80–559, rows 2–31. Both masks select the same 878 of 14,400 positions.</text>
    <text x="24" y="193" font-size="17" font-weight="600">Detail at 5×</text>
    <text x="133" y="193" font-size="17">Columns 272–367, rows 2–25</text>''']
    panels = (
        (24, "photo-mask", "Unmarked photograph", "Gray level 0 or 1", photo_path),
        (528, "screenshot-mask", "Hunter’s screenshot", "Mean RGB brightness below 64", screenshot_path),
    )
    for x, name, title, rule, path in panels:
        parts.append(f'''    <g transform="translate({x} 0)">
      <text y="96" font-size="21" font-weight="650">{title}</text>
      <text y="117" font-size="16" fill="#42525e">{rule}</text>
      <rect x="-0.5" y="127.5" width="481" height="31" fill="white" stroke="#a4b1b9"/>
      <svg x="0" y="128" width="480" height="30" viewBox="80 2 480 30" overflow="hidden">
        <path id="{name}" fill="#172026" shape-rendering="crispEdges" d="{path}"/>
      </svg>
      <path d="M192 161v4h96v-4" stroke="#516875" fill="none"/>
      <rect x="-0.5" y="200.5" width="481" height="121" fill="white" stroke="#a4b1b9"/>
      <svg x="0" y="201" width="480" height="120" viewBox="272 2 96 24" overflow="hidden">
        <use xlink:href="#{name}"/>
      </svg>
    </g>''')
    return "\n".join(parts) + "\n  </g>\n</svg>\n"


def verify_figure(file, photo_path):
    content = file.read_text(encoding="utf-8")
    root = ET.fromstring(content)
    paths = []
    for name in ("photo-mask", "screenshot-mask"):
        elements = root.findall(".//{http://www.w3.org/2000/svg}path[@id='" + name + "']")
        require(len(elements) == 1, f"missing or duplicate SVG path for {name}")
        paths.append(elements[0].get("d"))
        require(paths[-1] == photo_path, f"published {name} differs from the photograph")
    require(content == figure_text(*paths), "figure framing or labels differ")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("photograph", type=Path, help="pinned GITenberg frontispiece JPEG")
    parser.add_argument("--tablet", type=Path, default=ROOT / "docs/assets/r1-tablet.png")
    parser.add_argument("--coordinates", type=Path, default=ROOT /
                        "layers/R1-010_friderici_poem_coords/EVIDENCE/full_coords.txt")
    parser.add_argument("--screenshot", type=Path, help="optional pinned hunter screenshot PNG")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--figure", type=Path, default=HERE / "comparison.svg",
                       help="published figure to verify")
    group.add_argument("--write-figure", type=Path, help="create a new SVG from both original images")
    args = parser.parse_args()
    if args.write_figure and not args.screenshot:
        parser.error("--write-figure requires the pinned --screenshot")

    photo = read_image(args.photograph, PHOTO_SHA, "RGB", "photograph")
    result = {"canonical_replay": replay_rows(photo, args.tablet, args.coordinates)}
    measured = photo_mask(photo)
    require(sum(measured) == 878, "source mask count differs")
    source_path = mask_path(measured)
    figure = args.figure
    if args.screenshot:
        screenshot = read_image(args.screenshot, SCREEN_SHA, "RGB", "screenshot")
        observed, counts = measure_screenshot(photo, screenshot)
        require(observed == measured, "independently thresholded masks differ")
        result["screenshot_threshold_counts"] = counts
        if args.write_figure:
            figure = args.write_figure
            with figure.open("x", encoding="utf-8", newline="\n") as out:
                out.write(figure_text(source_path, mask_path(observed)))
    verify_figure(figure, source_path)
    result["public_figure"] = {"positions_per_panel": len(measured), "dark_in_each": sum(measured),
                               "photo_only": 0, "screenshot_panel_only": 0}
    result["original_screenshot_remeasured"] = args.screenshot is not None
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, ET.ParseError) as error:
        raise SystemExit(str(error))
