#!/usr/bin/env python3
"""Sample dry-run-only target that describes a change without writing it."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--content", required=True)
    args = parser.parse_args()
    destination = Path(args.path)
    state = "update" if destination.exists() else "create"
    print(f"would {state} {destination} with the proposed content")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
