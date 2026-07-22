#!/usr/bin/env python3
"""Worker-facing entrypoint for deterministic skill artifact updates.

This script orchestrates the core skill artifact pipeline:
generate mega-packs, generate pack manifests, project skills into plugin
trees and flat skill zips, and refresh the first-party skill catalog.

Use `tools/rebuild_marketplace.py` for the canonical full regeneration and
validation gate. The partial update modes in this script are repair-oriented
fallbacks.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from generate_mega_packs import generate_all_mega_packs
from generate_pack_manifests import generate as generate_pack_manifests
from generate_first_party_skill_catalog import generate as generate_first_party_skill_catalog
from project_skills import project_skills


def _selected_pack(args: argparse.Namespace) -> str | None:
    if args.pack:
        return args.pack
    if args.skill:
        return args.skill.split("/", 1)[0]
    return None


def _run_tool(script_name: str, *args: str) -> None:
    """Run a sibling generator script with the current Python interpreter."""
    script_path = Path(__file__).resolve().with_name(script_name)
    subprocess.run([sys.executable, str(script_path), *args], check=True)


def _run_full_regeneration_checks() -> None:
    """Run the repo-wide generated-surface checks for a full refresh."""
    _run_tool("generate_marketplace.py", "--check")
    _run_tool("generate_repo_index.py", "--check")
    generate_pack_manifests(write=False)
    generate_all_mega_packs(write=False)
    project_skills(write=False)
    _run_tool("generate_provenance_maps.py", "--check")
    _run_tool("generate_source_maps.py", "--check")
    generate_first_party_skill_catalog(write=False)


def _run_full_regeneration_writes() -> None:
    """Run every deterministic writer that participates in a full regen."""
    _run_tool("generate_marketplace.py")
    _run_tool("generate_repo_index.py")
    generate_pack_manifests(write=True)
    generate_all_mega_packs(write=True)
    project_skills(write=True)
    _run_tool("generate_provenance_maps.py")
    _run_tool("generate_source_maps.py")
    generate_first_party_skill_catalog(write=True)


def _run_targeted_writes(selected_pack: str) -> None:
    """Deprecated alias that runs the full skill artifact pipeline."""
    _ = selected_pack  # kept for CLI compatibility
    _run_full_regeneration_writes()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update or validate canonical skill artifacts")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--skill", help="deprecated alias that runs the full pipeline; ignored")
    group.add_argument("--pack", help="deprecated alias that runs the full pipeline; ignored")
    group.add_argument("--all", action="store_true", help="regenerate every installable skill")
    parser.add_argument("--check", action="store_true", help="validate current generated artifacts without writing")
    args = parser.parse_args()

    update_selected = any((args.skill, args.pack, args.all))
    if args.check and update_selected:
        parser.error("--check cannot be combined with update flags")
    if not args.check and not update_selected:
        parser.error("choose one of --skill, --pack, --all, or use --check")
    return args


def main() -> int:
    args = _parse_args()
    selected_pack = _selected_pack(args)

    if args.check:
        _run_full_regeneration_checks()
        return 0

    if args.all:
        _run_full_regeneration_writes()
    else:
        assert selected_pack is not None
        _run_targeted_writes(selected_pack)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())