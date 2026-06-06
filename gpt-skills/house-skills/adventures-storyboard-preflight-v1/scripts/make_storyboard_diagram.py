#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
"""Create a simple storyboard diagram PNG from a JSON specification."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


def _xy(points: list[list[float]]) -> list[tuple[int, int]]:
    return [(int(x), int(y)) for x, y in points]


def _arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], fill: str, width: int) -> None:
    draw.line([start, end], fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = max(12, width * 3)
    left = (end[0] - size * math.cos(angle - 0.5), end[1] - size * math.sin(angle - 0.5))
    right = (end[0] - size * math.cos(angle + 0.5), end[1] - size * math.sin(angle + 0.5))
    draw.polygon([end, (int(left[0]), int(left[1])), (int(right[0]), int(right[1]))], fill=fill)


def render(spec: dict[str, Any], output: Path) -> None:
    width = int(spec.get("width", 1600))
    height = int(spec.get("height", 1200))
    background = spec.get("background", "#ffffff")
    image = Image.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(image)

    for item in spec.get("items", []):
        kind = item.get("type")
        fill = item.get("fill")
        outline = item.get("outline")
        stroke = int(item.get("stroke", 3))
        if kind == "rect":
            draw.rectangle(item["box"], fill=fill, outline=outline, width=stroke)
        elif kind == "ellipse":
            draw.ellipse(item["box"], fill=fill, outline=outline, width=stroke)
        elif kind == "polygon":
            draw.polygon(_xy(item["points"]), fill=fill, outline=outline)
        elif kind == "line":
            draw.line(_xy(item["points"]), fill=fill or outline or "#000000", width=stroke)
        elif kind == "dashed_line":
            points = _xy(item["points"])
            dash = int(item.get("dash", 40))
            gap = int(item.get("gap", 24))
            if len(points) != 2:
                continue
            (x1, y1), (x2, y2) = points
            length = math.hypot(x2 - x1, y2 - y1)
            if length == 0:
                continue
            pos = 0.0
            while pos < length:
                end = min(pos + dash, length)
                a = pos / length
                b = end / length
                p1 = (int(x1 + (x2 - x1) * a), int(y1 + (y2 - y1) * a))
                p2 = (int(x1 + (x2 - x1) * b), int(y1 + (y2 - y1) * b))
                draw.line([p1, p2], fill=fill or "#000000", width=stroke)
                pos += dash + gap
        elif kind == "arrow":
            pts = _xy(item["points"])
            if len(pts) >= 2:
                _arrow(draw, pts[0], pts[-1], fill or "#000000", stroke)
        elif kind == "text":
            text = str(item.get("text", ""))
            size = int(item.get("size", 22))
            location = tuple(item.get("at", [0, 0]))
            item_font = _font(size, bool(item.get("bold")))
            draw.text(location, text, fill=fill or "#000000", font=item_font)
        else:
            raise ValueError(f"Unsupported item type: {kind}")

    image.save(output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a storyboard diagram PNG from JSON.")
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with args.spec.open("r", encoding="utf-8") as handle:
        spec = json.load(handle)
    render(spec, args.output)


if __name__ == "__main__":
    main()
