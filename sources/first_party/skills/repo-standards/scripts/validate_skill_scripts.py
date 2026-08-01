#!/usr/bin/env python3
"""Validate that first-party skill-bundled Python scripts follow the CLI contract.

Contract (evolving): every Python script under sources/first_party/skills/*/scripts/
should:
- respond to --help with exit 0 and a usage line
- declare a classification (read-only / mixed / mutating) in its help text
- respond to --check with an exit code that is not a parser error (i.e. not 2)

The validator currently enforces --help and --check presence. Missing
classification is reported as a warning but not a hard failure, because the
existing scaffolders do not yet declare it. They will be hardened over time.

Scripts that are not yet compliant are tracked in DEFERRED until they are
migrated. They are reported but do not fail validation.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(result.stdout.strip())


ROOT = _repo_root()
SCRIPTS_GLOB = "sources/first_party/skills/*/scripts/*.py"

# Scripts known to not yet support the contract, or that are the validator itself.
# They are reported but do not fail validation. Remove entries as they are migrated.
DEFERRED: set[str] = {
    "_agents_md.py",
    "unslop.py",
    "validate_package.py",
    "validate_unslop_output.py",
    "validate_skill_scripts.py",
}


class Report:
    def __init__(self) -> None:
        self.ok: list[str] = []
        self.warn: list[str] = []
        self.deferred: list[str] = []
        self.fail: list[str] = []

    def record(self, status: str, path: Path, detail: str) -> None:
        rel = path.relative_to(ROOT).as_posix()
        line = f"{status:8} {rel}: {detail}"
        print(line)
        if status == "OK":
            self.ok.append(rel)
        elif status == "WARN":
            self.warn.append(rel)
        elif status == "DEFERRED":
            self.deferred.append(rel)
        else:
            self.fail.append(rel)


def _run_help(path: Path) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(path), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.returncode, result.stdout + result.stderr


def _run_check(path: Path) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(path), "--check"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.returncode, result.stdout + result.stderr


def _classifies(help_text: str) -> bool:
    lowered = help_text.lower()
    return any(word in lowered for word in ["read-only", "mutating", "mixed"])


def _validate_one(path: Path, report: Report) -> None:
    rel_name = path.name
    if rel_name in DEFERRED:
        report.record("DEFERRED", path, "known non-compliant script")
        return

    help_rc, help_text = _run_help(path)
    if help_rc != 0:
        report.record("FAIL", path, f"--help exited {help_rc}")
        return
    if "usage" not in help_text.lower():
        report.record("FAIL", path, "--help output does not contain 'usage:'")
        return
    if not _classifies(help_text):
        report.record("WARN", path, "--help does not declare read-only/mutating/mixed classification")

    check_rc, _ = _run_check(path)
    if check_rc == 2:
        report.record("FAIL", path, "--check exits 2 (unrecognized argument); contract requires --check support")
        return

    if _classifies(help_text):
        report.record("OK", path, f"--help and --check respond ({check_rc})")
    else:
        report.record("OK", path, f"--help and --check respond ({check_rc}); add classification to help text")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate first-party skill-bundled Python scripts follow the --help/--check contract. (read-only)"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        default=True,
        help="run validation and report drift (default, read-only)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="alias for --check; this validator is read-only (read-only)",
    )
    parser.add_argument(
        "--deferred",
        action="store_true",
        help="list the deferred (known non-compliant) scripts and exit",
    )
    args = parser.parse_args(argv)

    if args.deferred:
        for name in sorted(DEFERRED):
            print(name)
        return 0

    report = Report()
    scripts = sorted(ROOT.glob(SCRIPTS_GLOB))
    if not scripts:
        print("no first-party skill scripts found", file=sys.stderr)
        return 1

    for path in scripts:
        _validate_one(path, report)

    print()
    print(f"OK: {len(report.ok)}  WARN: {len(report.warn)}  Deferred: {len(report.deferred)}  FAIL: {len(report.fail)}")
    if report.fail:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
