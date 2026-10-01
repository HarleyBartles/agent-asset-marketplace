#!/usr/bin/env python3
"""Editable starter for placement, JSON syntax, and static agent-document link checks."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


DOCUMENT_SUFFIXES = {".md", ".markdown", ".json", ".yaml", ".yml", ".toml"}
INLINE_LINK = re.compile(
    r"!?\[[^\]]*\]\(\s*(<[^>\n]*>|(?:\\.|[^()\s]|\([^()\n]*\))+)(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*\)"
)
REFERENCE_DEFINITION = re.compile(r"^[ \t]{0,3}\[([^\]\n]+)\]:[ \t]*(<[^>\n]*>|(?:\\.|[^\s])+)", re.MULTILINE)
REFERENCE_USE = re.compile(r"!?\[([^\]\n]+)\](?:\[([^\]\n]*)\])?")
FENCE_OPEN = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")
FENCE_CLOSE = re.compile(r"^[ \t]{0,3}(`+|~+)[ \t]*$")
INLINE_CODE_SPAN = re.compile(r"(?<!`)(`+)(?!`)[\s\S]*?(?<!`)\1(?!`)")
DEFAULT_EXCLUDES = (".git/**",)


def _excluded(path: Path, root: Path, patterns: list[str]) -> bool:
    relative = path.relative_to(root).as_posix()
    return ".git" in path.relative_to(root).parts or any(
        fnmatch.fnmatchcase(relative, pattern) for pattern in (*DEFAULT_EXCLUDES, *patterns)
    )


def _markdown_files(root: Path, patterns: list[str], route_roots: list[Path]) -> set[Path]:
    files = {path.resolve() for path in root.rglob("*.md") if not _excluded(path, root, patterns)}
    files.update(path.resolve() for path in root.rglob("*.markdown") if not _excluded(path, root, patterns))
    for route_root in route_roots:
        candidates = [route_root] if route_root.is_file() else route_root.rglob("*")
        files.update(
            path.resolve() for path in candidates if path.is_file() and path.suffix.lower() in {".md", ".markdown"}
        )
    return files


def _resolve_link(source: Path, raw: str, root: Path) -> Path | None:
    link = raw.strip()
    if link.startswith("<") and ">" in link:
        target = link[1 : link.index(">")]
    else:
        target = link.split(maxsplit=1)[0]
    parts = urlsplit(target)
    if parts.scheme or target.startswith("//") or not parts.path:
        return None
    resolved = (source.parent / unquote(parts.path)).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f"link escapes repository: {target}")
    return resolved


def _markdown_link_targets(content: str) -> list[tuple[str | None, str | None]]:
    lines: list[str] = []
    active_fence: tuple[str, int] | None = None
    for line in content.splitlines():
        if active_fence is not None:
            closing = FENCE_CLOSE.match(line)
            if closing and closing.group(1)[0] == active_fence[0] and len(closing.group(1)) >= active_fence[1]:
                active_fence = None
            continue
        opening = FENCE_OPEN.match(line)
        if opening:
            active_fence = (opening.group(1)[0], len(opening.group(1)))
            continue
        if line.startswith("\t") or line.startswith("    "):
            continue
        lines.append(line)
    content = "\n".join(lines)
    content = INLINE_CODE_SPAN.sub(_mask_code_span, content)
    targets = [(match.group(1), None) for match in INLINE_LINK.finditer(content)]
    definitions: dict[str, str] = {}
    for match in REFERENCE_DEFINITION.finditer(content):
        label = " ".join(match.group(1).split()).casefold()
        definitions[label] = match.group(2)
    for line in content.splitlines():
        if REFERENCE_DEFINITION.match(line):
            continue
        without_inline_links = INLINE_LINK.sub("", line)
        for match in REFERENCE_USE.finditer(without_inline_links):
            label = match.group(2) if match.group(2) else match.group(1)
            normalized = " ".join(label.split()).casefold()
            if match.group(2) is None and normalized not in definitions:
                continue
            targets.append((definitions.get(normalized), label))
    return targets


def _mask_code_span(match: re.Match[str]) -> str:
    return "".join("\n" if char == "\n" else " " for char in match.group())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check agent document stores, JSON syntax, and visible Markdown links. "
            "Semantic routing still needs review. (read-only)"
        )
    )
    parser.add_argument(
        "--repo-root", type=Path, default=Path("."), help="repository root (default: current directory)"
    )
    parser.add_argument("--check", action="store_true", help="run read-only checks (default)")
    parser.add_argument(
        "--route-root",
        action="append",
        default=[],
        metavar="PATH",
        help="add a repository-relative Markdown route source file or tree, even if excluded; repeatable",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="GLOB",
        help="exclude a repository-relative document or route-source pattern; repeatable",
    )
    args = parser.parse_args(argv)

    root = args.repo_root.resolve()
    if not root.is_dir():
        parser.error(f"repository root is not a directory: {root}")

    errors: list[str] = []
    stores = [root / ".agents/doctrine", root / ".agents/contracts"]
    for store in stores:
        if not store.is_dir():
            errors.append(f"required agent-document store is missing: {store.relative_to(root).as_posix()}")

    route_roots: list[Path] = []
    for value in args.route_root:
        route_root = (root / value).resolve()
        if not route_root.is_relative_to(root):
            errors.append(f"route root escapes repository: {value}")
        elif not route_root.exists():
            errors.append(f"route root does not exist: {value}")
        elif not route_root.is_file() and not route_root.is_dir():
            errors.append(f"route root is not a file or directory: {value}")
        else:
            route_roots.append(route_root)

    documents = sorted(
        path.resolve()
        for store in stores
        if store.is_dir()
        for path in store.rglob("*")
        if path.is_file() and path.suffix.lower() in DOCUMENT_SUFFIXES and not _excluded(path, root, args.exclude)
    )
    for path in documents:
        if path.suffix.lower() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                errors.append(f"{path.relative_to(root).as_posix()}: invalid JSON syntax: {exc}")

    route_sources = _markdown_files(root, args.exclude, route_roots)
    checked_route_sources = {path for path in documents if path.suffix.lower() in {".md", ".markdown"}}
    for route_root in route_roots:
        candidates = [route_root] if route_root.is_file() else route_root.rglob("*")
        checked_route_sources.update(
            path.resolve() for path in candidates if path.is_file() and path.suffix.lower() in {".md", ".markdown"}
        )
    inbound: set[Path] = set()
    for source in route_sources:
        try:
            content = source.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            if source in checked_route_sources:
                errors.append(f"{source.relative_to(root).as_posix()}: cannot read route source: {exc}")
            continue
        for raw, label in _markdown_link_targets(content):
            if raw is None:
                if source in checked_route_sources:
                    errors.append(f"{source.relative_to(root).as_posix()}: undefined Markdown reference: [{label}]")
                continue
            try:
                target = _resolve_link(source, raw, root)
            except ValueError as exc:
                if source in checked_route_sources:
                    errors.append(f"{source.relative_to(root).as_posix()}: {exc}")
                continue
            if target is None:
                continue
            if not target.is_file():
                if source in checked_route_sources:
                    errors.append(f"{source.relative_to(root).as_posix()}: broken local link: {raw.strip()}")
            elif source != target and target in documents:
                inbound.add(target)

    for path in documents:
        if path not in inbound:
            print(f"CANDIDATE without an inbound Markdown link: {path.relative_to(root).as_posix()}")

    for error in errors:
        print(f"ERROR: {error}")
    print(
        f"Checked {len(documents)} agent document(s). JSON syntax is checked; "
        "schema validation is not performed. Product schema semantics are out of scope."
    )
    print(
        "Static Markdown links only: harness scope, skills, plugin metadata, tool registries, "
        "and other runtime routes may be invisible."
    )
    print(
        "Candidate reachability is advisory and needs repository review; this check does not "
        "certify semantic reachability or compliance."
    )
    if errors:
        return 1
    print("OK: no mechanical errors found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
