#!/usr/bin/env python3
"""Check or scaffold consumer adoption of the optional Unslop standard."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import unquote, urlsplit


CONTRACT = Path(".agents/contracts/unslop.json")
DEFAULT_ROOTS = [".agents/unslop"]
PROFILE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROFILE_TITLE = re.compile(r"(?m)^#\s+Unslop Profile:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*$")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
REQUIRED_SECTIONS = (
    "Task trigger and scope",
    "Recurring failure pattern",
    "Recognition cues",
    "Corrective behavior",
    "False-positive and override boundaries",
    "Applicable workflow paths",
    "Doctrine and skill references",
    "Application example",
)


def _safe_repo_path(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise ValueError(f"{label} must be a non-empty repository-relative path")
    normalized = value.replace("\\", "/")
    posix = PurePosixPath(normalized)
    windows = PureWindowsPath(normalized)
    if (
        posix.is_absolute()
        or windows.is_absolute()
        or windows.drive
        or normalized.startswith(("/", "!", ":"))
        or ".." in posix.parts
        or normalized in {"", "."}
    ):
        raise ValueError(f"{label} must be repository-relative without '..': {value}")
    return normalized


def _contained(root: Path, path: Path, *, label: str) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _sections(text: str) -> tuple[str, dict[str, str]]:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    live: list[str] = []
    fenced = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            fenced = not fenced
        elif not fenced:
            live.append(line)
    markdown = "\n".join(live)
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", markdown))
    sections = {
        match.group(1).strip(): markdown[
            match.end() : matches[index + 1].start() if index + 1 < len(matches) else None
        ].strip()
        for index, match in enumerate(matches)
    }
    return markdown, sections


def _links(section: str) -> list[str]:
    return [match.group(1).split(maxsplit=1)[0].strip("<>") for match in LINK.finditer(section)]


def _resolve_local_link(repo_root: Path, document: Path, target: str, *, label: str) -> Path | None:
    parts = urlsplit(target)
    if parts.scheme or parts.netloc or not parts.path:
        return None
    candidate = (document.parent / unquote(parts.path)).resolve()
    if not _contained(repo_root, candidate, label=label):
        raise ValueError(f"{label} escapes the repository: {target}")
    if not candidate.is_file():
        raise ValueError(f"{label} does not resolve: {target}")
    return candidate


def _tracked(repo_root: Path, path: Path) -> bool:
    relative = path.relative_to(repo_root.resolve()).as_posix()
    result = subprocess.run(
        ["git", "-C", str(repo_root), "ls-files", "--error-unmatch", "--", relative],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def _profile_findings(repo_root: Path, path: Path, seen_ids: set[str]) -> list[str]:
    findings: list[str] = []
    relative = path.relative_to(repo_root).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"profile cannot be read ({relative}): {exc}"]
    markdown, sections = _sections(text)
    match = PROFILE_TITLE.search(markdown)
    if not match:
        findings.append(f"profile requires '# Unslop Profile: <stable-id>' title ({relative})")
        profile_id = ""
    else:
        profile_id = match.group(1)
        if not PROFILE_ID.fullmatch(profile_id):
            findings.append(f"profile id must be kebab-case ({relative})")
        elif profile_id in seen_ids:
            findings.append(f"duplicate profile id: {profile_id}")
        else:
            seen_ids.add(profile_id)

    for name in REQUIRED_SECTIONS:
        if not sections.get(name, "").strip():
            findings.append(f"profile missing required section '{name}' ({relative})")

    reference_section = sections.get("Doctrine and skill references", "")
    reference_links = _links(reference_section)
    if not reference_links:
        findings.append(f"profile requires at least one doctrine or skill reference link ({relative})")
    for target in reference_links:
        try:
            _resolve_local_link(repo_root, path, target, label=f"profile reference in {relative}")
        except ValueError as exc:
            findings.append(str(exc))

    workflow_section = sections.get("Applicable workflow paths", "")
    workflow_links = _links(workflow_section)
    if not workflow_links:
        findings.append(f"profile requires at least one applicable workflow link ({relative})")
    for target in workflow_links:
        try:
            workflow = _resolve_local_link(repo_root, path, target, label=f"workflow route in {relative}")
        except ValueError as exc:
            findings.append(str(exc))
            continue
        if workflow is None:
            findings.append(f"workflow route must be a local file path ({relative}): {target}")
            continue
        if not _tracked(repo_root, workflow):
            findings.append(f"workflow route is not a tracked repository file ({relative}): {target}")
            continue
        _, workflow_sections = _sections(workflow.read_text(encoding="utf-8"))
        route = workflow_sections.get("Unslop profile routing", "")
        if "$unslop-profiles" not in route:
            findings.append(
                f"workflow lacks $unslop-profiles in its 'Unslop profile routing' section "
                f"({workflow.relative_to(repo_root).as_posix()})"
            )
    return findings


def validate(repo_root: Path) -> list[str]:
    """Return structural, path, and workflow-routing findings for a consumer."""
    repo_root = repo_root.resolve()
    contract_path = repo_root / CONTRACT
    if not contract_path.is_file():
        return [f"missing adoption contract: {CONTRACT.as_posix()}"]
    try:
        data = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"adoption contract cannot be read: {exc}"]
    if not isinstance(data, dict) or set(data) != {"version", "profile_roots"}:
        return ["adoption contract must contain only version and profile_roots"]
    if isinstance(data["version"], bool) or data["version"] != 1:
        return ["adoption contract version must be 1"]
    roots = data["profile_roots"]
    if not isinstance(roots, list) or not roots:
        return ["profile_roots must be a non-empty list"]
    findings: list[str] = []
    normalized_roots: list[str] = []
    for raw in roots:
        try:
            normalized_roots.append(_safe_repo_path(raw, label="profile root"))
        except ValueError as exc:
            findings.append(str(exc))
    if len(normalized_roots) != len(set(normalized_roots)):
        findings.append("profile_roots contains duplicate paths")
    profile_paths: list[tuple[Path, Path]] = []
    for root_value in normalized_roots:
        profile_root = (repo_root / root_value).resolve()
        if not _contained(repo_root, profile_root, label="profile root"):
            findings.append(f"profile root escapes the repository: {root_value}")
            continue
        if profile_root.exists() and not profile_root.is_dir():
            findings.append(f"profile root is not a directory: {root_value}")
            continue
        if not profile_root.exists():
            continue
        try:
            profile_paths.extend((profile_root, path) for path in profile_root.rglob("*.md"))
        except OSError as exc:
            findings.append(f"profile root cannot be read ({root_value}): {exc}")
    seen_ids: set[str] = set()
    for profile_root, profile in sorted(profile_paths, key=lambda item: item[1]):
        escapes_root = not _contained(profile_root, profile, label="profile")
        escapes_repo = not _contained(repo_root, profile, label="profile")
        if escapes_root or escapes_repo:
            findings.append(f"profile escapes the repository: {profile}")
            continue
        findings.extend(_profile_findings(repo_root, profile, seen_ids))
    return findings


def apply(repo_root: Path) -> list[str]:
    """Create only a missing default adoption contract, then validate it."""
    repo_root = repo_root.resolve()
    target = repo_root / CONTRACT
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps({"version": 1, "profile_roots": DEFAULT_ROOTS}, indent=2) + "\n", encoding="utf-8")
    return validate(repo_root)


def _repo_root() -> Path:
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(key, None)
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], check=True, capture_output=True, text=True, env=env
    )
    return Path(result.stdout.strip())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check or scaffold the optional Unslop consumer standard. (mixed)")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="validate without writing (default)")
    modes.add_argument("--apply", action="store_true", help="create a missing default adoption contract")
    args = parser.parse_args(argv)
    try:
        repo_root = _repo_root()
        findings = apply(repo_root) if args.apply else validate(repo_root)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"DRIFT: Unslop standard could not inspect repository: {exc}")
        return 1
    if findings:
        for finding in findings:
            print(f"DRIFT: {finding}")
        return 1
    print("OK Unslop standard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
