#!/usr/bin/env python3
"""Canonical non-mutating marketplace validation entrypoint.

This is a thin wrapper around `tools/rebuild_marketplace.py --check`.
The wrapper preserves the canonical CI command and help surface while the
full orchestration lives in the rebuild entry point.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REBUILD = ROOT / "tools" / "rebuild_marketplace.py"


def _parse_args() -> argparse.Namespace:
    epilog = (
        "This is the canonical non-mutating CI gate. It checks whether the committed\n"
        "marketplace surfaces are current and valid without writing any files.\n\n"
        "The check is implemented as `py -3 tools/rebuild_marketplace.py --check`.\n\n"
        "For the full rebuild flow see .agents/guides/marketplace-generation-guide.md."
    )
    parser = argparse.ArgumentParser(
        description="Run the non-mutating marketplace check stack",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog,
    )
    return parser.parse_args()


def main() -> int:
    _parse_args()
    return subprocess.run(
        [sys.executable, str(REBUILD), "--check"],
        cwd=ROOT,
        check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
