#!/usr/bin/env python3
"""Canonical full marketplace rebuild and validation entrypoint."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _run_tool(script_name: str, *args: str) -> None:
    script_path = Path(__file__).resolve().with_name(script_name)
    subprocess.run([sys.executable, str(script_path), *args], check=True)


def _run_git(*args: str) -> None:
    subprocess.run(["git", *args], cwd=ROOT, check=True)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the full marketplace rebuild and validation stack")
    parser.add_argument("--base", default="origin/main", help="git revision used for generated drift validation")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    _run_tool("update_skill_artifacts.py", "--all", "--base", args.base)
    _run_tool("normalize_first_party_skill_sources.py", "--check")
    _run_tool("generate_repo_index.py")
    _run_tool("validate_marketplace.py")
    _run_tool("generate_repo_index.py", "--check")
    _run_tool("generate_index_mesh.py")
    _run_tool("generate_index_mesh.py", "--check")
    _run_tool("generate_first_party_skill_catalog.py", "--check")
    _run_tool("validate_repo_index.py")
    _run_tool("validate_skill_zips.py")
    _run_git("diff", "--check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
