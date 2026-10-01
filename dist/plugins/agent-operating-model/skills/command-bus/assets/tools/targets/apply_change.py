#!/usr/bin/env python3
"""Sample apply-only target that writes explicitly requested content."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--content", required=True)
    args = parser.parse_args()
    destination = Path(args.path)
    with destination.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(f"{args.content}\n")
    print(f"wrote {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
