#!/usr/bin/env python3
"""Validate tracked Markdown links and active doctrine routing (read-only)."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
ACTIVE_STATUS_PATTERN = re.compile(r"^\s*status:\s*active\s*$", re.MULTILINE | re.IGNORECASE)
EXCLUDED_DIRS = {".git", ".superpowers", "third_party", "marketplace-source"}


def _repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(result.stdout.strip())


def _tracked_markdown(repo_root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=repo_root,
        capture_output=True,
        check=True,
    )
    files: list[Path] = []
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        relative = Path(raw_path.decode("utf-8", errors="surrogateescape"))
        if relative.suffix.lower() not in {".md", ".markdown"}:
            continue
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        path = repo_root / relative
        if path.is_file():
            files.append(path)
    return files


def _is_under(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def _link_paths(source: Path, target: str, repo_root: Path) -> tuple[list[Path], bool]:
    parsed = urlsplit(unquote(target.strip()))
    if parsed.scheme or parsed.netloc:
        return [], False
    raw_path = parsed.path
    if not raw_path:
        return [], False

    root_relative = raw_path.startswith("/")
    clean_path = raw_path.lstrip("/") if root_relative else raw_path
    bases = (repo_root,) if root_relative else (source.parent, repo_root)
    candidates: list[Path] = []
    escaped = False
    seen: set[Path] = set()
    for base in bases:
        try:
            resolved = (base / clean_path).resolve()
        except (OSError, ValueError):
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        if _is_under(resolved, repo_root):
            candidates.append(resolved)
        else:
            escaped = True
    return candidates, escaped


def _link_findings(repo_root: Path, files: list[Path]) -> list[str]:
    findings: list[str] = []
    for source in files:
        relative = source.relative_to(repo_root)
        if source.name not in {"AGENTS.md", "SKILL.md"} and "docs" not in relative.parts[:-1]:
            continue
        try:
            content = source.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        relative_name = relative.as_posix()
        for _label, target in LINK_PATTERN.findall(content):
            candidates, escaped = _link_paths(source, target, repo_root)
            if not candidates:
                if escaped:
                    findings.append(f"repo-escaping link: {relative_name} -> {target}")
                continue
            if target.rstrip().endswith("/"):
                exists = any(candidate.is_dir() for candidate in candidates)
            else:
                exists = any(candidate.exists() for candidate in candidates)
            if not exists:
                findings.append(f"broken link: {relative_name} -> {target}")
    return findings


def _is_active_doctrine(path: Path) -> bool:
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    match = FRONTMATTER_PATTERN.match(content)
    return bool(match and ACTIVE_STATUS_PATTERN.search(match.group(1)))


def _targets_from(source: Path, repo_root: Path) -> set[Path]:
    try:
        content = source.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return set()
    targets: set[Path] = set()
    for _label, raw_target in LINK_PATTERN.findall(content):
        candidates, _escaped = _link_paths(source, raw_target, repo_root)
        for candidate in candidates:
            if candidate.exists():
                targets.add(candidate)
                break
    return targets


def _doctrine_route_findings(repo_root: Path, files: list[Path]) -> list[str]:
    route_targets: dict[Path, set[Path]] = {}
    for route_file in files:
        if route_file.name not in {"AGENTS.md", "INDEX.md"}:
            continue
        route_targets[route_file] = _targets_from(route_file, repo_root)

    findings: list[str] = []
    for doctrine in (path for path in files if _is_active_doctrine(path)):
        relative = doctrine.relative_to(repo_root).as_posix()
        routed = False
        for ancestor in doctrine.parents:
            if not _is_under(ancestor, repo_root):
                break
            for route_file, targets in route_targets.items():
                if route_file.parent != ancestor:
                    continue
                if doctrine in targets or doctrine.parent in targets:
                    routed = True
                    break
            if routed:
                break
        if not routed:
            findings.append(f"active doctrine not routed: {relative}")
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate tracked Markdown links and active doctrine routes (read-only)."
    )
    parser.add_argument("--check", action="store_true", help="run read-only validation (default)")
    parser.parse_args(argv)

    try:
        repo_root = _repo_root()
        files = _tracked_markdown(repo_root)
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"ERROR: could not inspect tracked Markdown: {error}", file=sys.stderr)
        return 1

    findings = _link_findings(repo_root, files)
    findings.extend(_doctrine_route_findings(repo_root, files))
    if findings:
        for finding in findings:
            print(f"DRIFT: {finding}", file=sys.stderr)
        return 1

    print("OK markdown links and doctrine routes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
