#!/usr/bin/env python3
"""Read-only structural validation for pinned AOM standard subscriptions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


RECORD_PATH = PurePosixPath(".agents/contracts/operating-standards.json")
_ID = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
_COMMIT = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
_RECORD_FIELDS = {"version", "standards"}
_SUBSCRIPTION_FIELDS = {"id", "source", "certification"}
_SOURCE_FIELDS = {"repository", "commit", "definition"}


def validate_commit(value: object) -> list[str]:
    """Validate a full immutable Git object identifier."""
    if not isinstance(value, str) or not _COMMIT.fullmatch(value):
        return ["commit must be a full lowercase 40- or 64-character hexadecimal Git object ID"]
    return []


def validate_relative_path(value: object, *, allow_fragment: bool = False) -> list[str]:
    """Validate a normalized, portable repository-relative POSIX file path."""
    if not isinstance(value, str) or not value:
        return ["path must be a non-empty repository-relative POSIX path"]

    path_value = value
    if "#" in path_value:
        if not allow_fragment:
            return ["path must not contain a fragment"]
        path_value, separator, fragment = path_value.partition("#")
        if not separator or not fragment or "#" in fragment:
            return ["certification fragment must be non-empty and contain no additional '#' characters"]

    posix = PurePosixPath(path_value)
    windows = PureWindowsPath(path_value)
    if (
        not path_value
        or path_value.startswith("/")
        or "\\" in path_value
        or ":" in path_value
        or windows.anchor
        or windows.drive
        or posix.as_posix() != path_value
        or any(part in {".", ".."} for part in posix.parts)
        or path_value.endswith("/")
    ):
        return ["path must be normalized, repository-relative POSIX form without traversal, anchors, or colons"]
    return []


def _unknown_fields(value: dict[str, Any], allowed: set[str], label: str) -> list[str]:
    unknown = sorted(set(value) - allowed)
    if not unknown:
        return []
    return [f"{label} contains unknown field(s): {', '.join(unknown)}"]


def validate_record(raw: object) -> list[str]:
    """Return structural diagnostics; an empty list is structural validity only."""
    if not isinstance(raw, dict):
        return ["subscription record must be a JSON object"]

    issues = _unknown_fields(raw, _RECORD_FIELDS, "record")
    version = raw.get("version")
    if not isinstance(version, (int, float)) or isinstance(version, bool) or version != 2:
        issues.append("record version must be numeric 2")
    standards = raw.get("standards")
    if not isinstance(standards, list):
        issues.append("standards must be an array")
        return issues

    seen: set[str] = set()
    for index, standard in enumerate(standards):
        label = f"standards[{index}]"
        if not isinstance(standard, dict):
            issues.append(f"{label} must be an object")
            continue
        issues.extend(_unknown_fields(standard, _SUBSCRIPTION_FIELDS, label))

        standard_id = standard.get("id")
        if not isinstance(standard_id, str) or not _ID.fullmatch(standard_id):
            issues.append(f"{label}.id must be lowercase kebab-case")
        elif standard_id in seen:
            issues.append(f"{label}.id duplicates {standard_id!r}")
        else:
            seen.add(standard_id)

        source = standard.get("source")
        if not isinstance(source, dict):
            issues.append(f"{label}.source must be an object")
        else:
            issues.extend(_unknown_fields(source, _SOURCE_FIELDS, f"{label}.source"))
            repository = source.get("repository")
            if not isinstance(repository, str) or not repository.strip():
                issues.append(f"{label}.source.repository must be a non-empty string")
            issues.extend(f"{label}.source.{issue}" for issue in validate_commit(source.get("commit")))
            issues.extend(f"{label}.source.{issue}" for issue in validate_relative_path(source.get("definition")))

        issues.extend(
            f"{label}.certification.{issue}"
            for issue in validate_relative_path(standard.get("certification"), allow_fragment=True)
        )
    return issues


def _resolve_repo_file(repo_root: Path, portable_path: str) -> Path | None:
    """Resolve a validated relative file without following it outside the repo."""
    file_part = portable_path.partition("#")[0]
    root = repo_root.resolve()
    candidate = (root / Path(*PurePosixPath(file_part).parts)).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def check_repository(repo_root: Path) -> list[str]:
    """Read the v2 record and referenced files; never execute, scaffold, or fetch."""
    path = repo_root / Path(*RECORD_PATH.parts)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"missing subscription record: {RECORD_PATH.as_posix()}"]
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"{RECORD_PATH.as_posix()} is not readable JSON: {exc}"]

    version = raw.get("version") if isinstance(raw, dict) else None
    if isinstance(version, (int, float)) and not isinstance(version, bool) and version == 1:
        return [f"{RECORD_PATH.as_posix()} uses legacy version 1; migration is an explicit repository task"]

    issues = validate_record(raw)
    if issues:
        return issues

    standards = raw["standards"]
    if not standards:
        return []

    if not (repo_root / "AGENTS.md").is_file():
        issues.append("selected standards require root AGENTS.md to route subscription and certification")

    for index, standard in enumerate(standards):
        reference = standard["certification"]
        cert_path = _resolve_repo_file(repo_root, reference)
        if cert_path is None:
            issues.append(f"standards[{index}].certification resolves outside the repository")
        elif not cert_path.is_file():
            issues.append(f"standards[{index}].certification file is missing: {reference.partition('#')[0]}")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check pinned standard subscription structure without certifying semantics. (read-only)"
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="repository root (default: current directory)",
    )
    parser.add_argument("--check", action="store_true", help="read-only structural check (default)")
    args = parser.parse_args(argv)

    findings = check_repository(args.repo_root)
    for finding in findings:
        print(f"ERROR: {finding}", file=sys.stderr)
    if findings:
        return 1
    print("OK subscription structure; semantic certification is not assessed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
