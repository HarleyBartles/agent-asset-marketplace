#!/usr/bin/env python3
"""Worker-facing entrypoint for deterministic skill artifact updates.

This script orchestrates the core skill artifact pipeline:
generate pack manifests, project skills into plugin trees, and refresh the
first-party skill catalog.

Use `tools/run marketplace --apply` for the canonical full regeneration and
validation gate. This script is an implementation detail invoked by the
`project` target.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from generate_pack_manifests import generate as generate_pack_manifests
from generate_first_party_skill_catalog import generate as generate_first_party_skill_catalog
from project_skills import project_skills


def _run_tool(script_name: str, *args: str) -> None:
    script_path = Path(__file__).resolve().with_name(script_name)
    subprocess.run([sys.executable, str(script_path), *args], check=True)


def _run_full_regeneration_checks() -> None:
    """Run the repo-wide generated-surface checks for a full refresh."""
    _run_tool("generate_marketplace.py", "--check")
    _run_tool("generate_repo_index.py", "--check")
    generate_pack_manifests(write=False)
    project_skills(write=False)
    _run_tool("generate_provenance_maps.py", "--check")
    _run_tool("generate_source_maps.py", "--check")
    generate_first_party_skill_catalog(write=False)


def _run_full_regeneration_writes() -> None:
    """Run every deterministic writer that participates in a full regen."""
    _run_tool("generate_marketplace.py")
    _run_tool("generate_repo_index.py")
    generate_pack_manifests(write=True)
    project_skills(write=True)
    _run_tool("generate_provenance_maps.py")
    _run_tool("generate_source_maps.py")
    generate_first_party_skill_catalog(write=True)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update or validate canonical skill artifacts")
    parser.add_argument("--all", action="store_true", help="regenerate every installable skill")
    parser.add_argument("--check", action="store_true", help="validate current generated artifacts without writing")
    args = parser.parse_args()
    if args.check and args.all:
        parser.error("--check cannot be combined with --all")
    if not args.check and not args.all:
        parser.error("choose --all or --check")
    return args


def main() -> int:
    args = _parse_args()
    if args.check:
        _run_full_regeneration_checks()
    else:
        _run_full_regeneration_writes()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
