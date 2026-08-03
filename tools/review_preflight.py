#!/usr/bin/env python3
"""Read-only preflight scanner for the review phase.

This is a non-mutating check that runs the same pattern-based scans Devin auto
review tends to catch: secrets/PII in reference files, SKILL.md frontmatter
schema, stale cross-skill script paths, malformed markdown tables, and repo
convention drift.

Usage:
    py -3 tools/review_preflight.py --check
    py -3 tools/review_preflight.py --check --base-ref origin/main
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent


# Discord snowflake IDs are 17-20 digit unsigned integers.
_SNOWFLAKE = re.compile(r"\d{17,20}")

# Context that makes a 17-20 digit number likely a real server/guild/channel/user ID.
_SNOWFLAKE_CONTEXT = re.compile(
    r"(?:guild|server|channel|user|tenant|discord)[-_ ]?id",
    re.IGNORECASE,
)

# Any already-redacted placeholder like <DISCORD_GUILD_ID>.
_PLACEHOLDER = re.compile(r"<[^>]+>")

# Email, token/key/secret, and private-IP patterns are conservative.
_EMAIL = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
_TOKEN_LIKE = re.compile(
    r"(?:api[_-]?key|token|secret|password|private[_-]?key|credential)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-]{20,})['\"]?",
    re.IGNORECASE,
)
_PRIVATE_IP = re.compile(
    r"(?:\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})\b)"
)

# Stale script path after the move into subagent-workspace.
_STALE_SCRIPT_PATH = re.compile(r"subagent-driven-development/scripts")

# py -m without the repo's py -3 convention.
_PY_M = re.compile(r"\bpy -m ")

# Known buggy new_plugin.py return pattern.
_NEW_PLUGIN_BOGUS_RETURN = re.compile(r"return 0 if result is None or args\.check else 1")

# new_plugin.py default-enabling a pack.
_NEW_PLUGIN_ENABLED_TRUE = re.compile(r'"enabled"\s*:\s*True')


def _changed_files(base_ref: str | None) -> list[Path]:
    if base_ref is None:
        result = subprocess.run(
            ["git", "ls-files", "--"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return [ROOT / p for p in result.stdout.splitlines() if (ROOT / p).is_file()]

    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base_ref}...HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [ROOT / p for p in result.stdout.splitlines() if (ROOT / p).is_file()]


def _warn(findings: list[str], path: Path, line_no: int, message: str) -> None:
    rel = path.relative_to(ROOT)
    findings.append(f"{rel}:{line_no}: {message}")


def _scan_security(path: Path, content: str, findings: list[str]) -> None:
    for line_no, line in enumerate(content.splitlines(), start=1):
        # Strip placeholders so <DISCORD_GUILD_ID> does not trip the numeric scan.
        depl = _PLACEHOLDER.sub("", line)

        # 17-20 digit snowflake-like IDs in reference files, especially when they
        # appear next to guild/server/channel/user language.
        if path.suffix in {".md", ".json", ".yaml", ".yml", ".txt"} or "references" in path.parts:
            for match in _SNOWFLAKE.finditer(depl):
                # Require some nearby context that makes it look like a real identifier
                # *or* require the file is in a references/ directory.
                span = match.span()
                context_window = depl[max(0, span[0] - 80) : min(len(depl), span[1] + 80)]
                in_references = "references" in path.parts
                has_context = _SNOWFLAKE_CONTEXT.search(context_window) is not None
                if in_references or has_context:
                    _warn(
                        findings,
                        path,
                        line_no,
                        f"possible real identifier {match.group()}: replace with a placeholder or env-var reference",
                    )

        if _EMAIL.search(line):
            _warn(findings, path, line_no, "email address in source; use a placeholder or env-var reference")

        for token_match in _TOKEN_LIKE.finditer(line):
            value = token_match.group(1)
            if value and not value.upper().startswith(("YOUR_", "INSERT_", "PLACEHOLDER")):
                _warn(
                    findings,
                    path,
                    line_no,
                    "possible token/secret value in source; use a placeholder or env-var reference",
                )

        if _PRIVATE_IP.search(line):
            _warn(
                findings, path, line_no, "private IP address in source; replace with a placeholder or env-var reference"
            )


def _scan_skill_frontmatter(path: Path, content: str, findings: list[str]) -> None:
    if path.name != "SKILL.md":
        return
    if not content.startswith("---"):
        return
    parts = content.split("---", 2)
    if len(parts) < 3:
        return
    try:
        front = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return

    if not isinstance(front, dict):
        return

    metadata = front.get("metadata") or {}
    if "license" in metadata:
        _warn(findings, path, 1, "`license` is nested under `metadata`; move it to a top-level frontmatter field")

    if "license" not in front:
        _warn(findings, path, 1, "top-level `license` frontmatter field is missing")


_SKIP_STALE_PATHS = {
    "reviewer-known-findings.md",
}


def _scan_stale_paths(path: Path, content: str, findings: list[str]) -> None:
    if path.suffix not in {".md", ".ps1"} or path.name in _SKIP_STALE_PATHS:
        return
    for line_no, line in enumerate(content.splitlines(), start=1):
        if _STALE_SCRIPT_PATH.search(line):
            _warn(
                findings,
                path,
                line_no,
                "stale path `subagent-driven-development/scripts`; use `subagent-workspace/scripts`",
            )


def _scan_markdown_tables(path: Path, content: str, findings: list[str]) -> None:
    if path.suffix != ".md":
        return
    in_code_block = False
    for line_no, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if "|" not in line:
            continue
        # Skip lines that are clearly not table rows (e.g., inline `|`).
        if not (line.startswith("|") or line.startswith("  |")):
            continue
        if not line.rstrip().endswith("|"):
            _warn(findings, path, line_no, "markdown table row does not end with `|`")


def _scan_py3_convention(path: Path, content: str, findings: list[str]) -> None:
    if path.suffix != ".md":
        return
    for line_no, line in enumerate(content.splitlines(), start=1):
        if _PY_M.search(line):
            _warn(findings, path, line_no, "use `py -3 -m` instead of `py -m` per repo convention")


def _scan_new_plugin(path: Path, content: str, findings: list[str]) -> None:
    if path.name != "new_plugin.py":
        return
    for line_no, line in enumerate(content.splitlines(), start=1):
        if _NEW_PLUGIN_BOGUS_RETURN.search(line):
            _warn(findings, path, line_no, "dry-run and validation-error exit codes are indistinguishable")
        if _NEW_PLUGIN_ENABLED_TRUE.search(line):
            _warn(
                findings, path, line_no, "new packs should be registered with `enabled: false` unless explicitly opt-in"
            )


def _scan_file(path: Path, findings: list[str]) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return

    _scan_security(path, content, findings)
    _scan_skill_frontmatter(path, content, findings)
    _scan_stale_paths(path, content, findings)
    _scan_markdown_tables(path, content, findings)
    _scan_py3_convention(path, content, findings)
    _scan_new_plugin(path, content, findings)


def _main() -> int:
    parser = argparse.ArgumentParser(description="Read-only review preflight scanner.")
    parser.add_argument("--check", action="store_true", help="Run the read-only preflight scan.")
    parser.add_argument(
        "--base-ref", default=None, help="Base ref to compare against (default: origin/main, or all tracked files)"
    )
    args = parser.parse_args()

    if not args.check:
        parser.print_help()
        return 0

    base_ref = args.base_ref
    if base_ref is None:
        if (
            subprocess.run(
                ["git", "rev-parse", "--verify", "origin/main"],
                cwd=ROOT,
                capture_output=True,
            ).returncode
            == 0
        ):
            base_ref = "origin/main"

    files = _changed_files(base_ref)
    findings: list[str] = []
    for path in files:
        _scan_file(path, findings)

    if findings:
        for finding in findings:
            print(f"PREFLIGHT WARN {finding}", file=sys.stderr)
        print(f"\nreview-preflight: {len(findings)} issue(s) found", file=sys.stderr)
        return 1

    print(f"OK review-preflight: {len(files)} file(s) scanned, 0 issues")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
