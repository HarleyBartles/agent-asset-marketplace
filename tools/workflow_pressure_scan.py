#!/usr/bin/env python3
"""Candidate-only pressure scan for composed workflow instructions (read-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


PATTERNS = (
    ("approval-wait", re.compile(r"wait for (?:your )?(?:human|user).*approval", re.I)),
    ("full-test-suite", re.compile(r"full (?:test|suite)|entire test suite", re.I)),
    ("repeated-validation", re.compile(r"run (?:it|the tests|the suite) (?:again|multiple times)", re.I)),
    ("every-function", re.compile(r"every (?:new )?function|each function", re.I)),
    ("universal-startup-read", re.compile(r"at (?:the )?start of every (?:conversation|session)", re.I)),
    ("must-read", re.compile(r"MUST READ|must read", re.I)),
    ("unconditional-connector", re.compile(r"invoke .*connector|always .*connector", re.I)),
    (
        "personal-path",
        re.compile(r"(?<!\w)[A-Za-z]:[\\/]+[A-Za-z0-9_.-]|/Users/|/home/", re.I),
    ),
    ("portable-repo-command", re.compile(r"tools/run\.py|tools/run ", re.I)),
    ("unconditional-skill", re.compile(r"invoke .* unconditionally|always invoke", re.I)),
)


def _is_scannable_file(path: Path) -> bool:
    if path.suffix.lower() in {".md", ".py", ".json", ".yml", ".yaml"}:
        return True
    try:
        return path.read_bytes()[:2] == b"#!"
    except OSError:
        return False


def scan_paths(paths: list[Path], root: Path) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    for path in paths:
        if not path.is_file() or not _is_scannable_file(path):
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            for name, pattern in PATTERNS:
                if pattern.search(line):
                    hits.append(
                        {
                            "path": path.relative_to(root).as_posix(),
                            "line": number,
                            "pattern": name,
                            "context": line.strip(),
                        }
                    )
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Candidate-only pressure scan for composed workflow instructions. (read-only)"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="run the read-only scanner without writing an output file",
    )
    parser.add_argument("paths", nargs="*", type=Path, help="files or directories to scan")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    paths = args.paths or [args.root]
    files: list[Path] = []
    for path in paths:
        resolved = path if path.is_absolute() else args.root / path
        files.extend(resolved.rglob("*") if resolved.is_dir() else [resolved])
    result = scan_paths(files, args.root)
    encoded = json.dumps(result, indent=2) + "\n"
    if args.check:
        print(f"OK workflow pressure scan: {len(result)} candidate hit(s)")
    elif args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
