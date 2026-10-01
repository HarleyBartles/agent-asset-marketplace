#!/usr/bin/env python3
"""Optional Python command bus starter with repository-editable target metadata."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any


TARGET_DIR = Path(__file__).resolve().parent / "targets"
MODE_OPTIONS = {"--check": "check", "--apply": "apply", "--dry-run": "dry-run"}
VALID_MODES = frozenset(MODE_OPTIONS.values())

TARGETS: dict[str, dict[str, Any]] = {
    "check_status": {
        "command": [sys.executable, str(TARGET_DIR / "check_status.py")],
        "description": "Demonstrate check-mode dispatch and argument forwarding.",
        "supported_modes": ["check"],
        "prerequisites": ["Python available through the current interpreter."],
        "side_effects": "Reads no maintained files and writes no maintained files.",
        "argument_help": "Optional arguments are echoed; --exit-code N sets the sample target status.",
    },
    "apply_change": {
        "command": [sys.executable, str(TARGET_DIR / "apply_change.py")],
        "description": "Demonstrate an explicit repository mutation.",
        "supported_modes": ["apply"],
        "prerequisites": ["Python available through the current interpreter."],
        "side_effects": "Writes the requested sample content to --path.",
        "argument_help": "--path PATH --content TEXT",
    },
    "preview_change": {
        "command": [sys.executable, str(TARGET_DIR / "preview_change.py")],
        "description": "Demonstrate a read-only proposed mutation preview.",
        "supported_modes": ["dry-run"],
        "prerequisites": ["Python available through the current interpreter."],
        "side_effects": "Reads the destination when it exists and writes nothing.",
        "argument_help": "--path PATH --content TEXT",
    },
}


def validate_target(name: str, target: object) -> dict[str, Any]:
    if not isinstance(target, dict):
        raise ValueError(f"target {name!r} metadata must be a mapping")
    command = target.get("command")
    if not isinstance(command, list) or not command or not all(isinstance(part, str) for part in command):
        raise ValueError(f"target {name!r} command must be a non-empty list of strings")
    if not command[0]:
        raise ValueError(f"target {name!r} command executable must not be empty")
    for field in ("description", "side_effects", "argument_help"):
        value = target.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"target {name!r} requires non-empty {field} help")
    prerequisites = target.get("prerequisites")
    if not isinstance(prerequisites, list) or not all(isinstance(item, str) for item in prerequisites):
        raise ValueError(f"target {name!r} prerequisites must be a list of strings")
    modes = target.get("supported_modes")
    if not isinstance(modes, list) or not modes or not all(isinstance(mode, str) for mode in modes):
        raise ValueError(f"target {name!r} requires a non-empty supported_modes list")
    if any(mode not in VALID_MODES for mode in modes):
        raise ValueError(f"target {name!r} lists an unsupported mode")
    if len(modes) != len(set(modes)):
        raise ValueError(f"target {name!r} repeats a supported mode")
    return target


def _print_top_help() -> int:
    try:
        targets = [(name, validate_target(name, target)) for name, target in TARGETS.items()]
    except ValueError as error:
        return _fail(str(error))
    print("Usage: run.py [--help]")
    print("       run.py <target> (--help|--check|--apply|--dry-run) [-- <target-arguments>...]")
    print("\nTargets:")
    for name, target in targets:
        modes = ", ".join(f"--{mode}" for mode in target["supported_modes"])
        print(f"  {name:<18} {target['description']} Supported: {modes}.")
    print("\nA selected target requires exactly one supported mode or --help.")
    return 0


def _print_target_help(name: str, target: dict[str, Any]) -> None:
    modes = ", ".join(f"--{mode}" for mode in target["supported_modes"])
    prerequisites = "; ".join(target["prerequisites"]) or "None declared."
    print(f"Usage: run.py {name} (--help|--check|--apply|--dry-run) [-- <target-arguments>...]")
    print(f"\n{target['description']}")
    print(f"Supported modes: {modes}.")
    print(f"Prerequisites: {prerequisites}")
    print(f"Side effects: {target['side_effects']}")
    print(f"Target arguments: {target['argument_help']}")


def _fail(message: str, *, usage: str | None = None) -> int:
    print(f"error: {message}", file=sys.stderr)
    if usage is not None:
        print(usage, file=sys.stderr)
    return 2


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if not arguments or arguments == ["--help"]:
        return _print_top_help()

    name, *target_arguments = arguments
    if name not in TARGETS:
        return _fail(f"unknown target: {name}")

    try:
        target = validate_target(name, TARGETS[name])
    except ValueError as error:
        return _fail(str(error))

    if target_arguments and target_arguments[0] == "--help":
        if len(target_arguments) != 1:
            return _fail(f"target {name!r} help does not accept target arguments")
        _print_target_help(name, target)
        return 0
    if not target_arguments or target_arguments[0] not in MODE_OPTIONS:
        return _fail(
            f"target {name!r} requires an explicit mode or --help",
            usage=f"Usage: run.py {name} (--help|--check|--apply|--dry-run) [-- <target-arguments>...]",
        )

    mode_option = target_arguments[0]
    mode = MODE_OPTIONS[mode_option]
    remaining = target_arguments[1:]
    if "--" in remaining:
        separator = remaining.index("--")
        bus_tokens = remaining[:separator]
        if any(value in MODE_OPTIONS for value in bus_tokens):
            return _fail("select exactly one mode; target mode-looking arguments must follow --")
        if bus_tokens:
            return _fail("target arguments must follow --")
        forwarded = remaining[separator + 1 :]
    else:
        if any(value in MODE_OPTIONS for value in remaining):
            return _fail("select exactly one mode; target mode-looking arguments must follow --")
        if remaining:
            return _fail("target arguments must follow --")
        forwarded = []
    if mode not in target["supported_modes"]:
        return _fail(f"target {name!r} does not support {mode_option}")

    try:
        completed = subprocess.run(
            [*target["command"], mode_option, *forwarded],
            check=False,
        )
    except OSError as error:
        return _fail(f"could not start target {name!r}: {error}")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
