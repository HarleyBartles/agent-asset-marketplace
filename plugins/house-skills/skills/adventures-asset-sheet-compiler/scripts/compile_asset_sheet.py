#!/usr/bin/env python3
"""Deterministically compile Adventures of Patch asset sheets with Pillow.

Usage:
    python scripts/compile_asset_sheet.py manifest.json

The manifest declares a lane, output directory, metadata, and source images.
The script never generates or edits character art. It only crops/contains,
pastes images into known template slots, renders text, copies source files, and
creates a zip package.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

RGBA = Tuple[int, int, int, int]
Box = Tuple[int, int, int, int]

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "assets" / "templates"

GREEN = (21, 82, 49)
GOLD = (205, 133, 27)
BG = (250, 251, 248)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)
LIGHT_GREY = (210, 213, 210)
PLACEHOLDER_GREY = (155, 155, 155)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ),
        (
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
        ),
    ]
    for candidate in candidates:
        p = Path(candidate)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


@dataclass(frozen=True)
class LaneSpec:
    template: str
    slots: Dict[str, Box]
    metadata_boxes: Dict[str, Box]
    guidance_box: Optional[Box] = None
    caption_boxes: Optional[Dict[str, Box]] = None


def inner(box: Box, pad: int = 18) -> Box:
    x0, y0, x1, y1 = box
    return (x0 + pad, y0 + pad, x1 - pad, y1 - pad)


def load_lane_from_spec(template_name: str, spec_name: str) -> LaneSpec:
    spec = json.loads((TEMPLATE_DIR / spec_name).read_text())
    slots: Dict[str, Box] = {}
    for hero in spec.get("heroes", []):
        slots[hero["id"]] = tuple(hero["box"])
    for alt in spec.get("alts", []):
        slots[alt["id"]] = tuple(alt["box"])
    return LaneSpec(
        template=template_name,
        slots=slots,
        metadata_boxes=COMMON_META_BOXES,
    )


COMMON_META_BOXES: Dict[str, Box] = {
    "title": (52, 160, 365, 184),
    "type": (430, 160, 700, 184),
    "status": (715, 160, 960, 184),
    "version": (980, 160, 1135, 184),
    "source_qa": (1160, 160, 1485, 184),
}

# Canonical v4 coordinates are derived from the approved single-character asset sheet template.
CHARACTER_V4_SLOTS: Dict[str, Box] = {
    "hero": (86, 286, 710, 570),
    "alt_1": (68, 690, 260, 888),
    "alt_2": (305, 690, 497, 888),
    "alt_3": (542, 690, 734, 888),
    "alt_4": (779, 690, 971, 888),
    "alt_5": (1016, 690, 1208, 888),
    "alt_6": (1253, 690, 1445, 888),
}
CHARACTER_V4_CAPTIONS: Dict[str, Box] = {
    "alt_1": (68, 898, 260, 930),
    "alt_2": (305, 898, 497, 930),
    "alt_3": (542, 898, 734, 930),
    "alt_4": (779, 898, 971, 930),
    "alt_5": (1016, 898, 1208, 930),
    "alt_6": (1253, 898, 1445, 930),
}
LANES: Dict[str, LaneSpec] = {
    "character-v4": LaneSpec(
        template="template_final_asset_sheet_blank_v4.png",
        slots=CHARACTER_V4_SLOTS,
        metadata_boxes=COMMON_META_BOXES,
        guidance_box=(790, 274, 1450, 560),
        caption_boxes=CHARACTER_V4_CAPTIONS,
    ),
    "three-hero-six-alt-v4": load_lane_from_spec(
        "template_asset_sheet_3hero_6alt_v4.png", "template_asset_sheet_3hero_6alt_v4_spec.json"
    ),
    "four-column-four-hero-eight-alt-v2": load_lane_from_spec(
        "template_asset_sheet_4column_4hero_8alt_v2.png", "template_asset_sheet_4column_4hero_8alt_v2_spec.json"
    ),
}


def read_image(path: Path) -> Image.Image:
    with Image.open(path) as im:
        return im.convert("RGBA")


def trim_near_white(im: Image.Image, tolerance: int = 248) -> Image.Image:
    """Trim transparent or near-white margins. This changes placement only, not source files."""
    rgba = im.convert("RGBA")
    alpha = rgba.getchannel("A")
    alpha_bbox = alpha.getbbox()
    if alpha_bbox and alpha_bbox != (0, 0, rgba.width, rgba.height):
        rgba = rgba.crop(alpha_bbox)

    bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
    diff = ImageChops.difference(rgba, bg).convert("L")
    mask = diff.point(lambda p: 255 if p > (255 - tolerance) else 0)
    bbox = mask.getbbox()
    if bbox:
        return rgba.crop(bbox)
    return rgba


def fit_contain(im: Image.Image, box: Box, trim: bool = True, bg_color: Tuple[int, int, int] = WHITE) -> Image.Image:
    if trim:
        im = trim_near_white(im)
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    canvas = Image.new("RGBA", (w, h), bg_color + (255,))
    im = im.convert("RGBA")
    scale = min(w / im.width, h / im.height)
    nw = max(1, int(im.width * scale))
    nh = max(1, int(im.height * scale))
    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    px = (w - nw) // 2
    py = (h - nh) // 2
    canvas.alpha_composite(resized, (px, py))
    return canvas


def draw_text_fit(
    draw: ImageDraw.ImageDraw,
    box: Box,
    text: str,
    max_size: int,
    min_size: int,
    bold: bool,
    fill=GREY,
    anchor="la",
) -> None:
    x0, y0, x1, y1 = box
    text = str(text)
    for size in range(max_size, min_size - 1, -1):
        f = load_font(size, bold)
        bbox = draw.multiline_textbbox((0, 0), text, font=f, spacing=4)
        if bbox[2] - bbox[0] <= x1 - x0 and bbox[3] - bbox[1] <= y1 - y0:
            draw.multiline_text((x0, y0), text, font=f, fill=fill, spacing=4, anchor=anchor)
            return
    f = load_font(min_size, bold)
    draw.multiline_text((x0, y0), text, font=f, fill=fill, spacing=4, anchor=anchor)


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int) -> List[str]:
    lines: List[str] = []
    for raw in str(text).splitlines() or [""]:
        words = raw.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = current + " " + word
            if draw.textlength(candidate, font=font) <= width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_bullets(draw: ImageDraw.ImageDraw, box: Box, bullets: Iterable[str]) -> None:
    x0, y0, x1, y1 = box
    f = load_font(18, False)
    bullet_f = load_font(18, True)
    y = y0
    line_h = 24
    bullet_gap = 14
    text_x = x0 + 28
    for bullet in bullets:
        lines = wrap_lines(draw, str(bullet), f, x1 - text_x)
        if y + len(lines) * line_h > y1:
            break
        draw.text((x0, y), "-", font=bullet_f, fill=(40, 40, 40))
        for line in lines:
            draw.text((text_x, y), line, font=f, fill=(50, 50, 50))
            y += line_h
        y += bullet_gap


def render_metadata(draw: ImageDraw.ImageDraw, lane: LaneSpec, metadata: Dict[str, str]) -> None:
    for key, box in lane.metadata_boxes.items():
        value = metadata.get(key, "")
        if value:
            # Clear value area only, preserving label above.
            x0, y0, x1, y1 = box
            draw.rectangle((x0, y0 - 2, x1, y1 + 3), fill=BG)
            draw_text_fit(draw, box, value, 18, 10, False, fill=GREY)


def render_caption(draw: ImageDraw.ImageDraw, box: Box, text: str) -> None:
    x0, y0, x1, y1 = box
    draw.rectangle((x0, y0, x1, y1), fill=WHITE)
    f = load_font(18, True)
    tw = draw.textlength(text, font=f)
    draw.text((x0 + (x1 - x0 - tw) / 2, y0 + 4), text, font=f, fill=(110, 110, 110))


def normalize_images(manifest: Dict[str, Any]) -> List[Dict[str, Any]]:
    images = manifest.get("images")
    if isinstance(images, dict):
        return [{"slot": k, "path": v} for k, v in images.items()]
    if isinstance(images, list):
        return images
    raise SystemExit("manifest must include images as a list or object")


def safe_copy_name(path: Path, slot: str, requested: Optional[str]) -> str:
    if requested:
        return Path(requested).name
    suffix = path.suffix.lower() or ".png"
    return f"source_{slot}{suffix}"


def compile_sheet(manifest_path: Path) -> Tuple[Path, Path]:
    manifest = json.loads(manifest_path.read_text())
    lane_name = manifest.get("lane")
    if lane_name not in LANES:
        raise SystemExit(f"unknown lane {lane_name!r}. available: {', '.join(LANES)}")
    lane = LANES[lane_name]
    template_path = TEMPLATE_DIR / lane.template
    if not template_path.exists():
        raise SystemExit(f"missing bundled template: {template_path}")

    output_dir = Path(manifest.get("output_dir", manifest_path.parent / "asset_sheet_package")).resolve()
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    source_dir = output_dir / "sources"
    source_dir.mkdir(exist_ok=True)

    sheet = read_image(template_path)
    draw = ImageDraw.Draw(sheet)

    metadata = manifest.get("metadata", {})
    render_metadata(draw, lane, metadata)

    if lane.guidance_box:
        bullets = manifest.get("guidance", [])
        if bullets:
            x0, y0, x1, y1 = lane.guidance_box
            draw.rectangle((x0 - 10, y0 - 10, x1 + 4, y1 + 10), fill=WHITE)
            draw_bullets(draw, lane.guidance_box, bullets)

    copied_sources: List[Dict[str, str]] = []
    trim = bool(manifest.get("trim", True))
    slot_pad = int(manifest.get("slot_pad", 18))

    for item in normalize_images(manifest):
        slot = item["slot"]
        if slot not in lane.slots:
            raise SystemExit(f"slot {slot!r} is not valid for lane {lane_name!r}")
        src = Path(item["path"]).expanduser().resolve()
        if not src.exists():
            raise SystemExit(f"source image not found for slot {slot}: {src}")
        copy_name = safe_copy_name(src, slot, item.get("copy_name"))
        copied = source_dir / copy_name
        shutil.copy2(src, copied)
        copied_sources.append({"slot": slot, "source": str(src), "copied": str(copied)})

        box = tuple(item.get("box", lane.slots[slot]))
        paste_box = tuple(item.get("image_box", inner(box, slot_pad)))
        # Cover the target image area first so placeholder text does not show through.
        draw.rectangle(paste_box, fill=WHITE)
        fitted = fit_contain(read_image(src), paste_box, trim=bool(item.get("trim", trim)))
        sheet.alpha_composite(fitted, (paste_box[0], paste_box[1]))

        if lane.caption_boxes and item.get("caption"):
            render_caption(draw, lane.caption_boxes[slot], str(item["caption"]))

    out_name = manifest.get("output_png", f"asset_sheet__{lane_name}.png")
    out_png = output_dir / Path(out_name).name
    sheet.convert("RGB").save(out_png)

    compile_spec = {
        "lane": lane_name,
        "template": lane.template,
        "manifest": manifest,
        "copied_sources": copied_sources,
        "output_png": str(out_png),
    }
    spec_path = output_dir / "asset_sheet_compile_spec.json"
    spec_path.write_text(json.dumps(compile_spec, indent=2), encoding="utf-8")
    manifest_copy = output_dir / "asset_sheet_manifest.json"
    manifest_copy.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    zip_name = manifest.get("output_zip", output_dir.name + ".zip")
    zip_path = output_dir.parent / Path(zip_name).name
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in output_dir.rglob("*"):
            if p.is_file():
                z.write(p, p.relative_to(output_dir.parent))

    return out_png, zip_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile an Adventures of Patch asset sheet deterministically.")
    parser.add_argument("manifest", type=Path, help="Path to manifest JSON")
    args = parser.parse_args()
    out_png, out_zip = compile_sheet(args.manifest)
    print(json.dumps({"output_png": str(out_png), "output_zip": str(out_zip)}, indent=2))


if __name__ == "__main__":
    main()
