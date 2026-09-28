#!/usr/bin/env python3
"""Build or check the complete Codex marketplace plugin package tree."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main(argv: list[str] | None = None) -> int:
    from marketplace.build import build_marketplace

    parser = argparse.ArgumentParser(description="Build source definitions into complete Codex plugins. (mixed)")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true", help="replace generated plugin packages")
    mode.add_argument("--check", action="store_true", help="check generated packages without writing")
    args = parser.parse_args(argv)
    build_marketplace(ROOT, apply=args.apply)
    print("OK marketplace plugin packages are current" if args.check else "Built marketplace plugin packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
