#!/usr/bin/env python3
"""Worker-facing entrypoint for deterministic skill artifact updates.

Current scope: GPT-ready packaging of Codex plugin skills from marketplace
source plus any repo-owned GPT overlay.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from generate_mega_packs import generate_all_mega_packs, load_mega_pack_registry
from materialize_projection import reconcile_projection
from skill_zip_artifacts import print_registry_receipt, synchronize_skill_zips, validate_skill_zip_registry
from validate_generated_drift import validate_generated_drift


def _selected_pack(args: argparse.Namespace) -> str | None:
    if args.pack:
        return args.pack
    if args.skill:
        return args.skill.split("/", 1)[0]
    return None


def _pack_requires_mega_pack_regeneration(pack: str | None) -> bool:
    if pack is None:
        return True
    registry = load_mega_pack_registry()
    return any(mapping.get("mega_pack") == pack for mapping in registry)


def _run_tool(script_name: str, *args: str) -> None:
    """Run a sibling generator script with the current Python interpreter."""
    script_path = Path(__file__).resolve().with_name(script_name)
    subprocess.run([sys.executable, str(script_path), *args], check=True)


def _run_full_regeneration_checks() -> None:
    """Run the repo-wide generated-surface checks for a full refresh."""
    _run_tool("generate_marketplace.py", "--check")
    _run_tool("generate_repo_index.py", "--check")
    _run_tool("generate_pack_manifests.py", "--check")
    _run_tool("generate_adventures_pack_manifest.py", "--check")
    generate_all_mega_packs(write=False)
    reconcile_projection(write=False)
    _run_tool("generate_provenance_maps.py", "--check")
    _run_tool("generate_source_maps.py", "--check")


def _run_full_regeneration_writes(selected_pack: str | None) -> None:
    """Run every deterministic writer that participates in a full regen."""
    _run_tool("generate_marketplace.py")
    _run_tool("generate_repo_index.py")
    _run_tool("generate_pack_manifests.py")
    _run_tool("generate_adventures_pack_manifest.py")
    generate_all_mega_packs(write=True)
    reconcile_projection(write=True, plugin_name=selected_pack)
    _run_tool("generate_provenance_maps.py")
    _run_tool("generate_source_maps.py")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update or validate canonical skill.zip artifacts")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--skill", help="update one installable skill as <pack>/<skill>")
    group.add_argument("--pack", help="update every installable skill in a single marketplace pack")
    group.add_argument("--all", action="store_true", help="regenerate every installable skill")
    parser.add_argument(
        "--full-regeneration",
        action="store_true",
        help="alias for --all that also marks a check as an explicit full-regeneration validation",
    )
    parser.add_argument("--check", action="store_true", help="validate current generated artifacts without writing")
    parser.add_argument("--base", default="origin/main", help="git revision used for generated drift validation")
    args = parser.parse_args()

    update_selected = any((args.skill, args.pack, args.all, args.full_regeneration))
    if args.full_regeneration and (args.skill or args.pack):
        parser.error("--full-regeneration can only be used with --check or --all")
    if args.check and any((args.skill, args.pack, args.all)):
        parser.error("--check cannot be combined with update flags")
    if not args.check and not update_selected:
        parser.error("choose one of --skill, --pack, --all, or --full-regeneration, or use --check")
    return args


def main() -> int:
    args = _parse_args()
    selected_pack = _selected_pack(args)

    if args.check:
        _run_full_regeneration_checks()
        registry = validate_skill_zip_registry()
        validate_generated_drift(base=args.base, full_regeneration=args.full_regeneration)
        print_registry_receipt(registry)
        return 0

    if args.all or args.full_regeneration:
        _run_full_regeneration_writes(selected_pack)
    else:
        if _pack_requires_mega_pack_regeneration(selected_pack):
            generate_all_mega_packs(write=True)
        reconcile_projection(write=True, plugin_name=selected_pack)

    if args.skill:
        registry = synchronize_skill_zips(skill=args.skill, write=True)
        validate_generated_drift(base=args.base, full_regeneration=False)
    elif args.pack:
        registry = synchronize_skill_zips(pack=args.pack, write=True)
        validate_generated_drift(base=args.base, full_regeneration=False)
    else:
        registry = synchronize_skill_zips(write=True)
        validate_generated_drift(base=args.base, full_regeneration=True)

    validate_skill_zip_registry()
    print_registry_receipt(registry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
