#!/usr/bin/env python3
"""Check this repository's pinned AOM adoption records without certifying semantics."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ".agents/contracts/operating-standards.json"
CERTIFICATION_PATH = ".agents/contracts/standards-certification.md"
SOURCE_REPOSITORY = "https://github.com/HarleyBartles/agent-asset-marketplace.git"
SOURCE_COMMIT = "3d59506dbd7a02266dedc9251b396dd60e5cc37d"
HOOK_SOURCE_COMMIT = SOURCE_COMMIT
COMMIT_PATTERN = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
STANDARD_DEFINITIONS = {
    "root-agent-router": "skills/agents-routing/references/standard.md",
    "runbook-composition": "skills/runbook-composition/references/standard.md",
    "playbook-composition": "skills/playbook-composition/references/standard.md",
    "tracked-validation-hook": "skills/tracked-repo-hooks/references/standard.md",
    "review-entrypoint": "skills/review-entrypoint/references/standard.md",
    "contribution-entrypoint": "skills/contribution-entrypoint/references/standard.md",
    "completed-artifact-custody": "skills/completed-artifact-custody/references/standard.md",
    "unslop": "skills/unslop/references/standard.md",
}
UNSLOP_RUNBOOKS = (
    ".agents/runbooks/planning.md",
    ".agents/runbooks/implementing.md",
    ".agents/runbooks/code-review.md",
    ".agents/runbooks/pr.md",
)


def _unknown_fields(value: dict[str, Any], allowed: set[str], label: str) -> list[str]:
    unknown = sorted(set(value) - allowed)
    return [f"{label} contains unknown field(s): {', '.join(unknown)}"] if unknown else []


def _relative_path_findings(value: object, *, allow_fragment: bool = False) -> list[str]:
    if not isinstance(value, str) or not value:
        return ["path must be a non-empty repository-relative POSIX path"]

    path_value = value
    fragment = ""
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


def _resolve_repo_file(repo_root: Path, value: str) -> Path | None:
    file_part = value.partition("#")[0]
    root = repo_root.resolve()
    candidate = (root / Path(*PurePosixPath(file_part).parts)).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def _subscription_findings(record: object) -> list[str]:
    if not isinstance(record, dict):
        return ["subscription record must be a JSON object"]

    findings = _unknown_fields(record, {"version", "standards"}, "record")
    version = record.get("version")
    if not isinstance(version, (int, float)) or isinstance(version, bool) or version != 2:
        findings.append("record version must be numeric 2")

    entries = record.get("standards")
    if not isinstance(entries, list):
        findings.append("standards must be an array")
        return findings

    seen: set[str] = set()
    selected: set[str] = set()
    for index, entry in enumerate(entries):
        label = f"standards[{index}]"
        if not isinstance(entry, dict):
            findings.append(f"{label} must be an object")
            continue
        findings.extend(_unknown_fields(entry, {"id", "source", "certification"}, label))

        standard_id = entry.get("id")
        if not isinstance(standard_id, str) or not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", standard_id):
            findings.append(f"{label}.id must be lowercase kebab-case")
        elif standard_id in seen:
            findings.append(f"{label}.id duplicates {standard_id!r}")
        else:
            seen.add(standard_id)
            selected.add(standard_id)

        if not isinstance(standard_id, str) or standard_id not in STANDARD_DEFINITIONS:
            findings.append(f"unexpected selected standard: {standard_id}")

        source = entry.get("source")
        if not isinstance(source, dict):
            findings.append(f"{label}.source must be an object")
        else:
            findings.extend(_unknown_fields(source, {"repository", "commit", "definition"}, f"{label}.source"))
            if source.get("repository") != SOURCE_REPOSITORY:
                findings.append(f"{label}.source.repository is an unexpected source repository")
            commit = source.get("commit")
            if not isinstance(commit, str) or not COMMIT_PATTERN.fullmatch(commit):
                findings.append(f"{label}.source.commit must be a full lowercase Git object ID")
            elif commit != (HOOK_SOURCE_COMMIT if standard_id == "tracked-validation-hook" else SOURCE_COMMIT):
                findings.append(f"{label}.source.commit does not match the repository's certified pin")
            definition = source.get("definition")
            findings.extend(f"{label}.source.{issue}" for issue in _relative_path_findings(definition))
            if isinstance(standard_id, str) and standard_id in STANDARD_DEFINITIONS:
                if definition != STANDARD_DEFINITIONS[standard_id]:
                    findings.append(f"{label}.source.definition path does not match the selected standard")

        certification = entry.get("certification")
        findings.extend(
            f"{label}.certification.{issue}" for issue in _relative_path_findings(certification, allow_fragment=True)
        )
        if isinstance(standard_id, str) and standard_id in STANDARD_DEFINITIONS:
            expected_certification = f"{CERTIFICATION_PATH}#{standard_id}"
            if certification != expected_certification:
                findings.append(f"{label}.certification must point to {expected_certification}")

    for standard_id in STANDARD_DEFINITIONS:
        if standard_id not in selected:
            findings.append(f"missing selected standard: {standard_id}")
    return findings


def _check_hook_command_contract(repo_root: Path) -> list[str]:
    relative = ".agents/contracts/repo-standards-commands.json"
    path = _resolve_repo_file(repo_root, relative)
    if path is None:
        return [f"tracked-validation-hook: {relative} resolves outside the repository"]
    try:
        declaration = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"tracked-validation-hook: {relative} is missing"]
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"tracked-validation-hook: {relative} is not readable JSON: {exc}"]
    if not isinstance(declaration, dict):
        return [f"tracked-validation-hook: {relative} must be a JSON object"]

    findings = _unknown_fields(declaration, {"check"}, relative)
    commands = declaration.get("check")
    expected = [["@python", "tools/run.py", "ci", "--check"]]
    if not isinstance(commands, list) or not commands:
        findings.append("tracked-validation-hook: command contract check must be a non-empty array")
    elif commands != expected:
        findings.append(
            "tracked-validation-hook: command contract check must be exactly @python tools/run.py ci --check"
        )
    return findings


def check_repository(repo_root: Path) -> list[str]:
    """Return structural and selected mechanical-policy findings only."""
    record_path = repo_root / Path(*PurePosixPath(RECORD_PATH).parts)
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"missing subscription record: {RECORD_PATH}"]
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"{RECORD_PATH} is not readable JSON: {exc}"]

    findings = _subscription_findings(record)
    entries = record.get("standards", []) if isinstance(record, dict) else []
    if not isinstance(entries, list) or not entries:
        return findings

    root_agents = _resolve_repo_file(repo_root, "AGENTS.md")
    if root_agents is None or not root_agents.is_file():
        findings.append("selected standards require root AGENTS.md")
    else:
        text = root_agents.read_text(encoding="utf-8")
        for required_route in (RECORD_PATH, CERTIFICATION_PATH):
            if required_route not in text:
                findings.append(f"root AGENTS.md must route to {required_route}")

    certification = _resolve_repo_file(repo_root, CERTIFICATION_PATH)
    if certification is None or not certification.is_file():
        findings.append(f"certification file is missing: {CERTIFICATION_PATH}")
        certification_text = ""
    else:
        certification_text = certification.read_text(encoding="utf-8")
    for standard_id in STANDARD_DEFINITIONS:
        if not re.search(rf"^##\s+{re.escape(standard_id)}\s*$", certification_text, re.MULTILINE):
            findings.append(f"certification section is missing: {standard_id}")

    required_files = {
        "root-agent-router": ("tools/validate_agents_md.py",),
        "tracked-validation-hook": (
            "githooks/pre-commit",
            ".github/workflows/marketplace-validation.yml",
            "tools/run.py",
        ),
        "review-entrypoint": ("REVIEW.md",),
        "contribution-entrypoint": ("CONTRIBUTING.md",),
        "unslop": (".agents/unslop",),
    }
    for standard_id, paths in required_files.items():
        for relative in paths:
            path = _resolve_repo_file(repo_root, relative)
            expected_directory = relative == ".agents/unslop"
            if path is None:
                findings.append(f"required by {standard_id}: {relative} resolves outside the repository")
            elif expected_directory and not path.is_dir():
                findings.append(f"required by {standard_id}: {relative} directory is missing")
            elif not expected_directory and not path.is_file():
                findings.append(f"required by {standard_id}: {relative} is missing")

    for relative in UNSLOP_RUNBOOKS:
        path = _resolve_repo_file(repo_root, relative)
        if path is None or not path.is_file() or "../unslop/repository.md" not in path.read_text(encoding="utf-8"):
            findings.append(f"Unslop profile route is missing from {relative}")

    findings.extend(_check_hook_command_contract(repo_root))

    workflow = _resolve_repo_file(repo_root, ".github/workflows/marketplace-validation.yml")
    if (
        workflow is not None
        and workflow.is_file()
        and "githooks/pre-commit" not in workflow.read_text(encoding="utf-8")
    ):
        findings.append("tracked-validation-hook: hosted workflow must invoke githooks/pre-commit")
    runner = _resolve_repo_file(repo_root, "tools/run.py")
    if runner is not None and runner.is_file():
        runner_text = runner.read_text(encoding="utf-8")
        if "tools/check_agent_standards.py" not in runner_text:
            findings.append("root-agent-router: tools/run.py must invoke tools/check_agent_standards.py")
        if "tools/validate_agents_md.py" not in runner_text:
            findings.append("root-agent-router: tools/run.py must invoke tools/validate_agents_md.py")

    return list(dict.fromkeys(findings))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check this repository's pinned AOM records and mechanical obligations. (read-only)"
    )
    parser.add_argument("--check", action="store_true", help="check the repository (default)")
    parser.add_argument("--repo-root", type=Path, default=ROOT, help="repository root (default: this checkout)")
    args = parser.parse_args(argv)

    findings = check_repository(args.repo_root)
    for finding in findings:
        print(f"ERROR: {finding}", file=sys.stderr)
    if findings:
        return 1
    print("OK adoption structure and selected mechanical surfaces; semantic certification is not assessed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
