#!/usr/bin/env python3
"""Optional check-only sample; copy and register manually, with no shared ABI or installer."""

from __future__ import annotations

import subprocess
import sys


DESCRIPTION = "Run a repository-owned complete candidate-preserving check command."
SUPPORTED_MODES = ("check",)
PREREQUISITES = ("Register this target in the repository's command bus and provide a complete check command.",)
SIDE_EFFECTS = "Runs checks that may create disposable outputs but must preserve maintained files."


def _help() -> int:
    print("Usage: repository_gate.py --help")
    print("       repository_gate.py --check -- COMMAND [ARGUMENT ...]")
    print(f"\n{DESCRIPTION}")
    print("Supported modes: --check")
    print(f"Prerequisites: {' '.join(PREREQUISITES)}")
    print(f"Side effects: {SIDE_EFFECTS}")
    print("Target arguments: -- followed by the repository-owned check command and its arguments.")
    return 0


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments == ["--help"]:
        return _help()
    if not arguments:
        print("error: select the explicit --check mode or --help", file=sys.stderr)
        return 2
    if arguments[0] != "--check":
        if arguments[0] in {"--apply", "--dry-run"}:
            print(f"error: this target does not support {arguments[0]}; supported: --check", file=sys.stderr)
        else:
            print("error: select the explicit --check mode or --help", file=sys.stderr)
        return 2
    if len(arguments) < 3 or arguments[1] != "--":
        print("error: --check requires -- followed by a command and its arguments", file=sys.stderr)
        return 2

    try:
        completed = subprocess.run(arguments[2:], check=False)
    except OSError as error:
        print(f"error: could not start repository check command: {error}", file=sys.stderr)
        return 2
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
