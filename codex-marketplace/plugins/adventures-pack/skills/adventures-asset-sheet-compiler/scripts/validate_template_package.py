#!/usr/bin/env python3
"""Validate an Adventures asset-sheet template package zip.

The package must contain:
- template_asset_sheet_<name>_vN.png
- template_asset_sheet_<name>_vN.json
README.md is optional but recommended.

The JSON sidecar must match package filenames and PNG canvas dimensions.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, Iterable

from PIL import Image

REQUIRED_COMPILE_RULES = (
    "read_sidecar_before_compile",
    "use_matching_project_source_png",
    "use_matching_project_source_spec",
    "do_not_infer_slots_from_recent_session_memory",
    "do_not_infer_geometry_from_filename",
)

TEMPLATE_RE = re.compile(r"^template_asset_sheet_[a-z0-9_]+_v[0-9]+$")


def fail(message: str) -> None:
    raise SystemExit(message)


def zip_names(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as z:
        return [n for n in z.namelist() if not n.endswith("/")]


def read_zip_text(z: zipfile.ZipFile, name: str) -> str:
    return z.read(name).decode("utf-8")


def check_box(box: Any, canvas_w: int, canvas_h: int, label: str) -> None:
    if not isinstance(box, list) or len(box) != 4 or not all(isinstance(v, int) for v in box):
        fail(f"{label} must be a list of four integers")
    x0, y0, x1, y1 = box
    if x1 <= x0 or y1 <= y0:
        fail(f"{label} has invalid ordering: {box}")
    if x0 < 0 or y0 < 0 or x1 > canvas_w or y1 > canvas_h:
        fail(f"{label} outside canvas {canvas_w}x{canvas_h}: {box}")


def require_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        fail(f"missing or invalid string field: {key}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an Adventures template package zip")
    parser.add_argument("package", type=Path)
    args = parser.parse_args()

    package = args.package
    if not package.exists() or package.suffix.lower() != ".zip":
        fail(f"not a zip package: {package}")

    names = zip_names(package)
    base_names = [Path(n).name for n in names]
    pngs = [n for n in names if Path(n).suffix.lower() == ".png"]
    jsons = [n for n in names if Path(n).suffix.lower() == ".json"]
    readmes = [n for n in names if Path(n).name == "README.md"]

    if len(pngs) != 1:
        fail(f"expected exactly one PNG, found {len(pngs)}")
    if len(jsons) != 1:
        fail(f"expected exactly one JSON sidecar, found {len(jsons)}")
    if len(readmes) > 1:
        fail("expected at most one README.md")

    with zipfile.ZipFile(package) as z:
        data = json.loads(read_zip_text(z, jsons[0]))
        png_bytes = z.read(pngs[0])
        with Image.open(io.BytesIO(png_bytes)) as im:
            png_w, png_h = im.size

    template_id = require_string(data, "template_id")
    if not TEMPLATE_RE.match(template_id):
        fail(f"template_id does not match expected pattern: {template_id}")

    expected_zip = f"{template_id}.zip"
    expected_png = f"{template_id}.png"
    expected_json = f"{template_id}.json"

    if package.name != expected_zip:
        fail(f"package filename mismatch: expected {expected_zip}, got {package.name}")
    if Path(pngs[0]).name != expected_png:
        fail(f"PNG filename mismatch: expected {expected_png}, got {Path(pngs[0]).name}")
    if Path(jsons[0]).name != expected_json:
        fail(f"JSON filename mismatch: expected {expected_json}, got {Path(jsons[0]).name}")

    fields = {
        "png_filename": expected_png,
        "project_source_package_filename": expected_zip,
        "project_source_png_filename": expected_png,
        "project_source_spec_filename": expected_json,
    }
    for key, expected in fields.items():
        actual = require_string(data, key)
        if actual != expected:
            fail(f"{key} mismatch: expected {expected}, got {actual}")

    canvas = data.get("canvas")
    if not isinstance(canvas, dict):
        fail("canvas must be an object")
    width = canvas.get("width")
    height = canvas.get("height")
    if width != png_w or height != png_h:
        fail(f"canvas mismatch: sidecar {width}x{height}, PNG {png_w}x{png_h}")

    for key in ("version", "status", "layout_type", "supported_layout"):
        require_string(data, key)

    slots = data.get("slots")
    if not isinstance(slots, list) or not slots:
        fail("slots must be a non-empty list")

    seen: set[str] = set()
    for idx, slot in enumerate(slots):
        if not isinstance(slot, dict):
            fail(f"slot {idx} must be an object")
        slot_id = require_string(slot, "slot_id")
        if slot_id in seen:
            fail(f"duplicate slot_id: {slot_id}")
        seen.add(slot_id)
        check_box(slot.get("box"), png_w, png_h, f"slot {slot_id} box")
        if "image_box" in slot:
            check_box(slot.get("image_box"), png_w, png_h, f"slot {slot_id} image_box")
            bx0, by0, bx1, by1 = slot["box"]
            ix0, iy0, ix1, iy1 = slot["image_box"]
            if ix0 < bx0 or iy0 < by0 or ix1 > bx1 or iy1 > by1:
                fail(f"slot {slot_id} image_box is not inside box")
        require_string(slot, "default_fit")
        require_string(slot, "role")

    compile_rules = data.get("compile_rules")
    if not isinstance(compile_rules, dict):
        fail("compile_rules must be an object")
    for key in REQUIRED_COMPILE_RULES:
        if compile_rules.get(key) is not True:
            fail(f"compile_rules.{key} must be true")

    text_regions = data.get("text_regions", [])
    if not isinstance(text_regions, list):
        fail("text_regions must be a list")
    for idx, region in enumerate(text_regions):
        if not isinstance(region, dict):
            fail(f"text region {idx} must be an object")
        check_box(region.get("box"), png_w, png_h, f"text region {idx} box")

    print(json.dumps({"status": "pass", "package": str(package), "template_id": template_id}, indent=2))


if __name__ == "__main__":
    main()
