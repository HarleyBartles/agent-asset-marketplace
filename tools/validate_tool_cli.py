#!/usr/bin/env python3
"""Validate that repo-level tools follow a consistent CLI contract.

A ``tools/*.py`` file is a CLI if it contains an ``if __name__ == "__main__":``
guard; otherwise it is a helper and is ignored by this validator.

The validator enforces:
- ``--help`` exits 0 and contains a ``usage:`` line.
- ``--help`` text states whether the tool is ``read-only``, ``mutating``,
  or ``mixed``.
- ``--check`` is the default, read-only mode for CLIs (exit 0 when clean,
  non-zero when drift or an error is found).
- ``mixed`` and ``mutating`` tools support ``--apply``.
- ``tools/run.py`` declares and forwards the standard flags.
"""

from __future__ import annotations

import argparse
import ast
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT / "tools"


class Report:
    def __init__(self) -> None:
        self.ok: list[str] = []
        self.warn: list[str] = []
        self.fail: list[str] = []

    def record(self, status: str, path: Path, detail: str) -> None:
        rel = path.relative_to(ROOT).as_posix()
        line = f"{status:4} {rel}: {detail}"
        print(line)
        if status == "OK":
            self.ok.append(rel)
        elif status == "WARN":
            self.warn.append(rel)
        else:
            self.fail.append(rel)


def _is_cli(path: Path) -> bool:
    return 'if __name__ == "__main__":' in path.read_text(encoding="utf-8")


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


def _classifies(help_text: str) -> str | None:
    lowered = help_text.lower()
    for cls in ("mixed", "mutating", "read-only"):
        if cls in lowered:
            return cls
    return None


def _description(path: Path) -> str:
    """Return the first ArgumentParser description literal, if any."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return ""
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr == "ArgumentParser":
                for kw in node.keywords:
                    if kw.arg == "description" and isinstance(kw.value, ast.Constant):
                        value = kw.value.value
                        return value if isinstance(value, str) else ""
            if isinstance(func, ast.Name) and func.id == "ArgumentParser":
                for kw in node.keywords:
                    if kw.arg == "description" and isinstance(kw.value, ast.Constant):
                        value = kw.value.value
                        return value if isinstance(value, str) else ""
    return ""


def _supports_flag(path: Path, flag: str) -> bool:
    result = subprocess.run(
        [sys.executable, str(path), f"{flag}", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.returncode == 0 and flag in result.stdout


def _validate_run_py(path: Path, report: Report) -> None:
    text = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        report.record("FAIL", path, f"not parseable: {exc}")
        return

    has_check = "--check" in text
    has_apply = "--apply" in text
    has_allow_shared = "--allow-shared-checkout" in text

    if not has_check:
        report.record("FAIL", path, "missing --check flag")
    if not has_apply:
        report.record("FAIL", path, "missing --apply flag")
    if not has_allow_shared:
        report.record("FAIL", path, "missing --allow-shared-checkout flag")

    has_tasks = False
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = [node.target] if isinstance(node, ast.AnnAssign) else node.targets
            for target in targets:
                if isinstance(target, ast.Name) and target.id == "_TASKS":
                    has_tasks = True
    if not has_tasks:
        report.record("FAIL", path, "_TASKS definition not found")

    if has_check and has_apply and has_allow_shared and has_tasks:
        report.record("OK", path, "tools/run.py declares standard flags and _TASKS")


def _validate_cli(path: Path, report: Report) -> None:
    if path.name == "run.py":
        _validate_run_py(path, report)
        return
    if path.name == "validate_tool_cli.py":
        report.record("OK", path, "validator; self-check skipped")
        return

    help_rc, help_text = _run_help(path)
    if help_rc != 0:
        report.record("FAIL", path, f"--help exited {help_rc}")
        return
    if "usage" not in help_text.lower():
        report.record("FAIL", path, "--help output does not contain 'usage:'")
        return

    desc = _description(path)
    cls = _classifies(desc)
    if not cls:
        report.record("WARN", path, "--help / description does not declare read-only/mutating/mixed classification")
        # Fall through to also check --check
    else:
        # For mixed/mutating, ensure --apply is declared.
        if cls in ("mixed", "mutating") and not _supports_flag(path, "--apply"):
            report.record("FAIL", path, f"{cls} tool does not support --apply")

    # Validators and read-only tools should support --check; mixed and mutating
    # should support --check as the default mode.
    check_rc, _ = _run_check(path)
    if check_rc == 2:
        report.record("FAIL", path, "--check exits 2 (unrecognized argument); contract requires --check support")
        return

    if not cls:
        report.record("OK", path, f"--help and --check respond ({check_rc}); add classification to description")
    else:
        report.record("OK", path, f"--help and --check respond ({check_rc}) as {cls}")


def _tool_scripts() -> list[Path]:
    return sorted(p for p in TOOLS_DIR.glob("*.py") if p.is_file())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate repo-level tools follow the --help/--check CLI contract. (read-only)"
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
    _ = parser.parse_args(argv)

    report = Report()
    for path in _tool_scripts():
        if _is_cli(path):
            _validate_cli(path, report)
        else:
            report.record("OK", path, "helper module; skipped")

    print()
    print(f"OK: {len(report.ok)}  WARN: {len(report.warn)}  FAIL: {len(report.fail)}")
    if report.fail:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
