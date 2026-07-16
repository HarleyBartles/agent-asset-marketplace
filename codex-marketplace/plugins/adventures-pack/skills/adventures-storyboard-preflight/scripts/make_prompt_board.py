#!/usr/bin/env python3
"""Create a deterministic Adventures prompt board PNG from a JSON specification."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import json
import textwrap
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps


PAPER = "#f8f4ea"
INK = "#1f2933"
MUTED = "#5b6470"
PANEL = "#ffffff"
BORDER = "#27313d"
ACCENT = "#2f6f73"
AMBER = "#9a6b00"
RED = "#8b1e1e"
GREEN = "#245c35"


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


def _resolve(path_text: str, base: Path) -> Path:
    path = Path(path_text)
    if not path.is_absolute():
        path = base / path
    return path.resolve()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    if not text:
        return []
    words = str(text).replace("\n", " \n ").split()
    lines: list[str] = []
    current = ""
    for word in words:
        if word == "\n":
            if current:
                lines.append(current)
                current = ""
            continue
        trial = word if not current else current + " " + word
        bbox = draw.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill: str,
    max_width: int,
    line_gap: int = 6,
    max_lines: int | None = None,
) -> int:
    x, y = xy
    lines = _wrap(draw, text, font, max_width)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        if lines:
            lines[-1] = lines[-1].rstrip(" .,") + "..."
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y += (bbox[3] - bbox[1]) + line_gap
    return y


def _fit_image(path: Path, box: tuple[int, int, int, int]) -> Image.Image:
    with Image.open(path) as src:
        src = src.convert("RGB")
        max_w = max(1, box[2] - box[0])
        max_h = max(1, box[3] - box[1])
        return ImageOps.contain(src, (max_w, max_h), method=Image.Resampling.LANCZOS)


def _draw_image_slot(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    slot: dict[str, Any],
    box: tuple[int, int, int, int],
    base: Path,
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=18, fill=PANEL, outline=BORDER, width=4)
    title_font = _font(32, True)
    role_font = _font(22, True)
    cap_font = _font(22, False)
    src_font = _font(18, False)

    title = str(slot.get("title", "Reference"))
    role = str(slot.get("role", "reference"))
    caption = str(slot.get("caption", ""))
    path_text = str(slot.get("path", ""))

    draw.text((x1 + 24, y1 + 18), title, font=title_font, fill=INK)
    role_color = ACCENT if "style" in role else AMBER if "layout" in role or "geometry" in role else MUTED
    role_y = y1 + 60
    role_box = (x1 + 24, role_y, x1 + 24 + min(520, 22 * len(role)), role_y + 34)
    draw.rounded_rectangle(role_box, radius=10, fill="#eef4f4", outline=role_color, width=2)
    draw.text((x1 + 36, role_y + 4), role, font=role_font, fill=role_color)

    image_top = y1 + 112
    image_bottom = y2 - 150
    image_box = (x1 + 24, image_top, x2 - 24, image_bottom)
    draw.rectangle(image_box, fill="#f1f3f5", outline="#d3d8dd", width=2)

    if path_text:
        path = _resolve(path_text, base)
        if path.exists():
            fitted = _fit_image(path, image_box)
            ix = image_box[0] + ((image_box[2] - image_box[0]) - fitted.width) // 2
            iy = image_box[1] + ((image_box[3] - image_box[1]) - fitted.height) // 2
            canvas.paste(fitted, (ix, iy))
        else:
            draw.text((image_box[0] + 20, image_box[1] + 20), f"Missing: {path_text}", font=cap_font, fill=RED)
    else:
        draw.text((image_box[0] + 20, image_box[1] + 20), "No image path supplied", font=cap_font, fill=RED)

    y = image_bottom + 18
    y = _draw_wrapped(draw, (x1 + 24, y), caption, cap_font, INK, x2 - x1 - 48, max_lines=3)
    _draw_wrapped(draw, (x1 + 24, y + 4), path_text, src_font, MUTED, x2 - x1 - 48, max_lines=2)


def _draw_list_panel(
    draw: ImageDraw.ImageDraw,
    title: str,
    items: list[str],
    box: tuple[int, int, int, int],
    color: str,
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=16, fill=PANEL, outline=color, width=4)
    title_font = _font(30, True)
    item_font = _font(23, False)
    draw.text((x1 + 22, y1 + 18), title, font=title_font, fill=color)
    y = y1 + 62
    for item in items:
        if y > y2 - 42:
            draw.text((x1 + 26, y), "...", font=item_font, fill=MUTED)
            break
        bullet = "- " + str(item)
        y = _draw_wrapped(draw, (x1 + 26, y), bullet, item_font, INK, x2 - x1 - 52, max_lines=3)
        y += 8



def _format_reference_rows(spec: dict[str, Any]) -> list[str]:
    rows: list[str] = []
    policy = str(spec.get("reference_policy", "minimum_sufficient_references"))
    use_all = bool(spec.get("use_all_available_images", False))
    rows.append(f"policy: {policy}; use_all_available_images: {str(use_all).lower()}")
    selected = list(spec.get("selected_generation_references", []))
    if selected:
        rows.append("attach:")
        for item in selected[:6]:
            path = str(item.get("path", ""))
            role = str(item.get("role", "reference"))
            required = str(bool(item.get("required", False))).lower()
            rows.append(f"- {role}, required={required}: {path}")
    excluded = list(spec.get("excluded_available_images", []))
    if excluded:
        rows.append("do not attach:")
        for item in excluded[:6]:
            path = str(item.get("path", ""))
            reason = str(item.get("reason", "not needed"))
            rows.append(f"- {path}: {reason}")
    return rows


def render(spec: dict[str, Any], output: Path, spec_base: Path) -> None:
    width = int(spec.get("width", 2400))
    height = int(spec.get("height", 1800))
    canvas = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(canvas)

    title_font = _font(54, True)
    sub_font = _font(26, False)
    title = str(spec.get("title", "Adventures Prompt Board"))
    subtitle = str(spec.get("subtitle", "pre-generation reference custody"))
    draw.text((60, 42), title, font=title_font, fill=INK)
    draw.text((64, 108), subtitle, font=sub_font, fill=MUTED)

    image_slots = list(spec.get("image_slots", []))[:4]
    top = 170
    left = 60
    gap = 30
    slot_h = int(spec.get("slot_height", 820))
    slot_w = (width - 2 * left - gap * (len(image_slots) - 1)) // max(1, len(image_slots))
    for idx, slot in enumerate(image_slots):
        x1 = left + idx * (slot_w + gap)
        _draw_image_slot(canvas, draw, slot, (x1, top, x1 + slot_w, top + slot_h), spec_base)

    lower_top = top + slot_h + 34
    lower_gap = 28
    lower_w = (width - 2 * left - lower_gap * 2) // 3
    lower_h = 420
    show_box = (left, lower_top, left + lower_w, lower_top + lower_h)
    no_box = (left + lower_w + lower_gap, lower_top, left + 2 * lower_w + lower_gap, lower_top + lower_h)
    qa_box = (left + 2 * (lower_w + lower_gap), lower_top, width - left, lower_top + lower_h)
    _draw_list_panel(draw, "MUST SHOW", list(spec.get("must_show", [])), show_box, GREEN)
    _draw_list_panel(draw, "MUST NOT SHOW", list(spec.get("must_not_show", [])), no_box, RED)
    _draw_list_panel(draw, "QA GATES", list(spec.get("qa_gates", [])), qa_box, AMBER)

    prompt_top = lower_top + lower_h + 34
    prompt_bottom = height - 90
    reference_rows = _format_reference_rows(spec)
    has_ref_lock = bool(spec.get("selected_generation_references") or spec.get("excluded_available_images"))
    if has_ref_lock:
        ref_w = int((width - 2 * left - 28) * 0.38)
        prompt_box = (left, prompt_top, width - left - ref_w - 28, prompt_bottom)
        ref_box = (width - left - ref_w, prompt_top, width - left, prompt_bottom)
    else:
        prompt_box = (left, prompt_top, width - left, prompt_bottom)
        ref_box = None

    draw.rounded_rectangle(prompt_box, radius=16, fill=PANEL, outline=BORDER, width=4)
    draw.text((prompt_box[0] + 24, prompt_top + 18), "PROMPT CARRY-FORWARD", font=_font(30, True), fill=ACCENT)
    prompt = str(spec.get("prompt_carry_forward", ""))
    _draw_wrapped(
        draw,
        (prompt_box[0] + 24, prompt_top + 62),
        prompt,
        _font(24, False),
        INK,
        prompt_box[2] - prompt_box[0] - 48,
        max_lines=10,
    )

    if ref_box is not None:
        draw.rounded_rectangle(ref_box, radius=16, fill=PANEL, outline=BORDER, width=4)
        draw.text((ref_box[0] + 24, prompt_top + 18), "REFERENCE LOCK", font=_font(30, True), fill=AMBER)
        y = prompt_top + 62
        for row in reference_rows:
            y = _draw_wrapped(draw, (ref_box[0] + 24, y), row, _font(20, False), INK, ref_w - 48, max_lines=2)
            y += 5
            if y > prompt_bottom - 40:
                break

    notes = list(spec.get("source_notes", []))
    if notes:
        note_text = " | ".join(str(n) for n in notes)
        _draw_wrapped(
            draw,
            (left + 24, height - 64),
            note_text,
            _font(18, False),
            MUTED,
            width - 2 * left - 48,
            max_lines=2,
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a deterministic Adventures prompt board PNG from JSON.")
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    spec_path = args.spec.resolve()
    with spec_path.open("r", encoding="utf-8") as handle:
        spec = json.load(handle)
    render(spec, args.output.resolve(), spec_path.parent)


if __name__ == "__main__":
    main()
