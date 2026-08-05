#!/usr/bin/env python3
"""Install the selecting-a-subagent shipped profiles into the local .agents/agents dir.

The profile `.md` assets in the skill's `assets/` directory are the canonical,
shipped copies. This script copies them to the consumer repository's runtime
`.agents/agents/` directory. Profiles that already exist in the target are
overwritten only if the shipped copy differs. Any other (locally managed) files
in the target are left untouched and are never removed.
"""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path


def _skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _default_source() -> Path:
    return _skill_root() / "assets"


def _default_target() -> Path:
    return _skill_root().parents[2] / "agents"


def _profile_paths(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(p for p in directory.iterdir() if p.is_file() and p.suffix == ".md")


def _needs_sync(source: Path, target: Path) -> bool:
    if not target.exists():
        return True
    return source.read_bytes() != target.read_bytes()


def _format_diff(source: Path, target: Path) -> str:
    source_lines = source.read_text(encoding="utf-8").splitlines()
    target_lines = target.read_text(encoding="utf-8").splitlines() if target.exists() else []
    return "\n".join(
        difflib.unified_diff(
            target_lines,
            source_lines,
            fromfile=str(target),
            tofile=str(source),
            lineterm="",
        )
    )


def _install(source_dir: Path, target_dir: Path, apply: bool, show_diff: bool) -> int:
    if not source_dir.is_dir():
        print(f"error: source directory does not exist: {source_dir}", file=sys.stderr)
        return 1

    if apply:
        target_dir.mkdir(parents=True, exist_ok=True)

    source_profiles = _profile_paths(source_dir)
    if not source_profiles:
        print("No shipped .md profile assets found in source directory.")
        return 0

    changes: list[Path] = []
    for source in source_profiles:
        target = target_dir / source.name
        if _needs_sync(source, target):
            changes.append(source)
            if apply:
                target.write_bytes(source.read_bytes())

    if not changes:
        print("OK: all shipped profiles are already installed.")
        return 0

    if not apply:
        print(f"{len(changes)} profile(s) would be added or updated:")
        for p in changes:
            print(f"  {p.name}")
            if show_diff:
                print(_format_diff(p, target_dir / p.name))
        print(
            "\nRun with --apply to write the changes to the target directory.",
            file=sys.stderr,
        )
        return 1

    for p in changes:
        status = "added" if not (target_dir / p.name).exists() else "updated"
        print(f"{status}: {target_dir / p.name}")
    return 0


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Install the selecting-a-subagent shipped .md profile assets into "
            "the consumer repository's .agents/agents directory."
        ),
        epilog=(
            "(mixed: default is a read-only preview; --apply writes to --target.)"
        ),
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=_default_source(),
        help="directory containing the shipped .md profile assets",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=_default_target(),
        help="consumer .agents/agents directory to install the profiles into",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write the shipped profiles into the target directory",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="show a unified diff for each profile that would change",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the script and exit without installing",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.check:
        return 0
    return _install(args.source, args.target, args.apply, args.diff)


if __name__ == "__main__":
    sys.exit(main())
