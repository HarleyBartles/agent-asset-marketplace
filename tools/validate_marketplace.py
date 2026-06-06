#!/usr/bin/env python3
"""Lightweight marketplace validation for the canonical source tree."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def check_json(path: Path) -> None:
    with path.open("r", encoding="utf-8") as fh:
        json.load(fh)
    print(f"OK json: {path.relative_to(ROOT)}")


def check_text(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(path)
    content = path.read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError(f"{path} is empty")
    print(f"OK text: {path.relative_to(ROOT)}")


def main() -> int:
    required = [
        ROOT / "gpt-skills/house-skills/cleanup-custody-v0.1/SKILL.md",
        ROOT / "gpt-skills/house-skills/skill-validator-v1/SKILL.md",
        ROOT / "gpt-skills/house-skills/skill-packager-v1/SKILL.md",
        ROOT / "gpt-skills/house-skills/skill-buster-v0.1/SKILL.md",
        ROOT / "sources/house-skills/decisions.json",
        ROOT / "sources/house-skills/decisions.md",
        ROOT / "sources/house-skills/intake.json",
        ROOT / "provenance/house-skills.md",
    ]

    check_json(ROOT / "sources/house-skills/decisions.json")
    check_json(ROOT / "sources/house-skills/intake.json")
    for path in required:
        if path.suffix.lower() == ".md":
            check_text(path)
        elif path.suffix.lower() == ".json":
            continue
        else:
            check_text(path)

    print("Marketplace validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
