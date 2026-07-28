#!/usr/bin/env python3
"""Run ruff and only report findings on added or modified lines.

The project's ruff configuration enforces a strict ruleset across the whole
repository, but the tree still carries pre-existing lint debt in some files.
This wrapper lets CI and the local preflight gate the *diff* so that new
changes are clean without demanding a one-shot cleanup of the whole tree.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

_HUNK_RE = re.compile(r"^@@ -(?:\d+)(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def _run(cmd: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=check,
    )


def _resolve_base_ref(args: argparse.Namespace) -> str | None:
    """Return the single git ref to diff against, or None if no useful base exists."""
    if args.changed_from:
        if _run(["git", "rev-parse", "--verify", args.changed_from]).returncode == 0:
            return args.changed_from
        print(f"warning: {args.changed_from} not found, no diff available to lint", file=sys.stderr)
        return None
    if _run(["git", "rev-parse", "--verify", "origin/main"]).returncode == 0:
        return "origin/main"
    print("warning: origin/main not found, no diff available to lint", file=sys.stderr)
    return None


def _changed_python_files(base_ref: str | None) -> list[Path]:
    """Return the list of .py files changed since the base ref."""
    if base_ref is None:
        return []
    diff = _run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base_ref}...HEAD"]
    )
    return [
        Path(p)
        for p in diff.stdout.splitlines()
        if p.endswith(".py") and Path(p).is_file()
    ]


def _added_line_numbers(base_ref: str, path: Path) -> set[int]:
    """Return the set of new-file line numbers added or modified in `path`."""
    diff = _run(
        ["git", "diff", "--unified=0", f"{base_ref}...HEAD", "--", str(path)]
    )
    added: set[int] = set()
    new_line = 0
    for line in diff.stdout.splitlines():
        if line.startswith("@@"):
            match = _HUNK_RE.match(line)
            if match:
                new_line = int(match.group(1))
            continue
        if line.startswith("---") or line.startswith("+++"):
            continue
        if line.startswith(r"\ No newline"):
            continue
        if line.startswith("+"):
            added.add(new_line)
            new_line += 1
        elif line.startswith(" "):
            new_line += 1
        # lines starting with '-' do not advance the new-file line counter
    return added


def _format_diagnostic(path: Path, diagnostic: dict[str, object]) -> str:
    location = diagnostic["location"]
    return (
        f"{path}:{location['row']}:{location['column']}: "
        f"{diagnostic['code']} {diagnostic['message']}"
    )


def _lint_file(base_ref: str, path: Path) -> list[str]:
    """Return ruff findings in `path` that fall on changed lines only."""
    added_lines = _added_line_numbers(base_ref, path)
    if not added_lines:
        return []
    result = _run(
        [sys.executable, "-m", "ruff", "check", "--output-format=json", str(path)]
    )
    if result.returncode not in (0, 1):
        print(result.stderr, file=sys.stderr)
        return [f"error: ruff failed on {path} (exit {result.returncode})"]
    if not result.stdout.strip():
        return []
    try:
        diagnostics = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return [f"error: invalid ruff output for {path}: {exc}"]
    if not isinstance(diagnostics, list):
        return [f"error: unexpected ruff output for {path}: {diagnostics!r}"]
    findings: list[str] = []
    for d in diagnostics:
        location = d["location"]
        end = d["end_location"]
        start_row = location["row"]
        end_row = end["row"]
        if any(start_row <= row <= end_row for row in added_lines):
            findings.append(_format_diagnostic(path, d))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run ruff on the diff and report only added/modified-line findings."
    )
    parser.add_argument(
        "--changed-from",
        default="",
        help="Base git ref to compare against (default: origin/main).",
    )
    args = parser.parse_args(argv)

    base_ref = _resolve_base_ref(args)
    files = _changed_python_files(base_ref)
    if not files:
        print("No changed Python files to lint.")
        return 0

    all_findings: list[str] = []
    for path in files:
        if base_ref is None:
            continue
        all_findings.extend(_lint_file(base_ref, path))

    if all_findings:
        for finding in all_findings:
            print(finding)
        print(f"Found {len(all_findings)} new lint finding(s).", file=sys.stderr)
        return 1

    print("No new lint findings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
