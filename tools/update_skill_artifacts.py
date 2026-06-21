#!/usr/bin/env python3
"""Worker-facing entrypoint for deterministic skill artifact updates.

Current scope: GPT-ready packaging of Codex plugin skills from marketplace
source plus any repo-owned GPT overlay.
"""

from __future__ import annotations

import argparse

from materialize_projection import reconcile_projection
from skill_zip_artifacts import print_registry_receipt, synchronize_skill_zips, validate_skill_zip_registry
from validate_generated_drift import validate_generated_drift


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

    if args.check:
        reconcile_projection(write=False)
        registry = validate_skill_zip_registry()
        validate_generated_drift(base=args.base, full_regeneration=args.full_regeneration)
        print_registry_receipt(registry)
        return 0

    reconcile_projection(write=True)
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
