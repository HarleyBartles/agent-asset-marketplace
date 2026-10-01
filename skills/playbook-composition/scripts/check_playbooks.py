#!/usr/bin/env python3
"""Check selected playbook file/link integrity; this cannot certify concern quality."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
DISCLAIMER = (
    "Review is still required for semantic usefulness and concern classification, effective routing, "
    "non-Markdown routes, and cross-stage fit. This check does not certify compliance."
)


def _local_target(markdown: Path, raw: str, root: Path) -> Path | None:
    target = raw.strip().split(maxsplit=1)[0].strip("<>")
    parts = urlsplit(target)
    if parts.scheme or target.startswith(("#", "//")) or not parts.path:
        return None
    resolved = (markdown.parent / unquote(parts.path)).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f"link escapes repository: {target}")
    return resolved


def _repo_file(root: Path, value: str) -> Path:
    resolved = (root / value).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f"path escapes repository: {value}")
    return resolved


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root", type=Path, default=Path("."), help="repository root (default: current directory)"
    )
    parser.add_argument(
        "--document",
        action="append",
        default=[],
        metavar="PATH",
        help="selected playbook path, relative to the repository; repeatable",
    )
    parser.add_argument(
        "--route-source",
        action="append",
        default=[],
        metavar="PATH",
        help="Markdown route source, relative to the repository; repeatable",
    )
    parser.add_argument("--check", action="store_true", required=True, help="perform read-only integrity checks")
    args = parser.parse_args(argv)

    root = args.repo_root.resolve()
    if not root.is_dir():
        parser.error(f"repository root is not a directory: {root}")
    if not args.document:
        print("ERROR: select at least one --document")
        print(DISCLAIMER)
        return 1

    errors: list[str] = []
    try:
        documents = [_repo_file(root, item) for item in args.document]
        routes = [_repo_file(root, item) for item in args.route_source]
        for label, paths in (("playbook", documents), ("route source", routes)):
            for path in paths:
                if not path.is_file():
                    errors.append(f"{label} is missing: {path.relative_to(root)}")
                elif not path.read_text(encoding="utf-8").strip():
                    errors.append(f"{label} is empty: {path.relative_to(root)}")

        routed: set[Path] = set()
        for path in [*documents, *routes]:
            if not path.is_file():
                continue
            content = path.read_text(encoding="utf-8")
            for raw in LINK.findall(content):
                try:
                    target = _local_target(path, raw, root)
                except ValueError as exc:
                    errors.append(f"{path.relative_to(root)}: {exc}")
                    continue
                if target is None:
                    continue
                if not target.is_file():
                    errors.append(f"{path.relative_to(root)}: broken local link: {raw.strip()}")
                elif path in routes and target in documents:
                    routed.add(target)

        if routes:
            for document in documents:
                if document.is_file() and document not in routed:
                    errors.append(f"no supplied route source links to selected playbook: {document.relative_to(root)}")
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(str(exc))

    for error in errors:
        print(f"ERROR: {error}")
    print(DISCLAIMER)
    if errors:
        return 1
    print(f"OK: checked {len(args.document)} selected playbook(s), {len(args.route_source)} route source(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
