#!/usr/bin/env python3
"""Build the renderer wheel without leaving build metadata in package source."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="mdformat-safe-link-labels-") as temporary:
        temporary_root = Path(temporary)
        source = temporary_root / "source"
        output = temporary_root / "wheels"
        output.mkdir()
        shutil.copytree(
            PACKAGE_ROOT,
            source,
            ignore=shutil.ignore_patterns("wheels", "__pycache__", "*.pyc", "*.egg-info", "build"),
        )
        subprocess.run(
            [sys.executable, "-m", "pip", "wheel", "--no-deps", "--wheel-dir", str(output), str(source)],
            check=True,
        )
        built_wheels = list(output.glob("*.whl"))
        if len(built_wheels) != 1:
            raise RuntimeError(f"expected one renderer wheel, found {len(built_wheels)}")
        wheel_directory = PACKAGE_ROOT / "wheels"
        wheel_directory.mkdir(exist_ok=True)
        destination = wheel_directory / built_wheels[0].name
        shutil.copy2(built_wheels[0], destination)
        print(f"Built {destination.relative_to(PACKAGE_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
