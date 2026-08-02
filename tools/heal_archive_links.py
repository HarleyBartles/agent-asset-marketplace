#!/usr/bin/env python3
"""Heal internal markdown links after plans/specs are archived to completed/.

When a plan or spec is moved into .agents/plans/completed/ or
.agents/specs/completed/, the links inside it only need to be re-resolved
against the new source location. The target files are the same except that
.agents/plans/... and .agents/specs/... paths now live under completed/.

CLI contract:
- --help prints usage and classifies each flag.
- --check (default) reports stale links and what would be fixed.
- --apply rewrites the files in place.
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


_LINK_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)|\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")
_URL_RE = re.compile(r"^(?:[a-z]+://|mailto:|tel:|#)")

_PLANS_COMPLETED = Path(".agents/plans/completed")
_SPECS_COMPLETED = Path(".agents/specs/completed")
_PLANS_ACTIVE = Path(".agents/plans")
_SPECS_ACTIVE = Path(".agents/specs")


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


REPO_ROOT = _repo_root()


def _completed_dirs() -> list[Path]:
    return [d for d in (REPO_ROOT / _PLANS_COMPLETED, REPO_ROOT / _SPECS_COMPLETED) if d.is_dir()]


def _markdown_files() -> list[Path]:
    files: list[Path] = []
    for d in _completed_dirs():
        files.extend(p for p in d.rglob("*.md") if p.name != "INDEX.md")
    return sorted(set(files))


def _old_src_dir(src: Path) -> Path:
    """Return the directory the archived file used to live in before completion."""
    src_dir = src.parent
    for completed, active in (
        (REPO_ROOT / _PLANS_COMPLETED, REPO_ROOT / _PLANS_ACTIVE),
        (REPO_ROOT / _SPECS_COMPLETED, REPO_ROOT / _SPECS_ACTIVE),
    ):
        try:
            rel = src_dir.relative_to(completed)
            return active / rel
        except ValueError:
            continue
    return src_dir


def _map_completed(target: Path) -> Path:
    """If a target is an active plan/spec, return its completed counterpart if it exists."""
    for active, completed in (
        (REPO_ROOT / _PLANS_ACTIVE, REPO_ROOT / _PLANS_COMPLETED),
        (REPO_ROOT / _SPECS_ACTIVE, REPO_ROOT / _SPECS_COMPLETED),
    ):
        try:
            rel = target.relative_to(active)
            completed_target = completed / rel
            if completed_target.exists():
                return completed_target
        except ValueError:
            continue
    return target


def _best_replacement(src: Path, url: str, target: Path) -> str:
    """Return the relative URL from src's directory to target."""
    try:
        rel = target.relative_to(src.parent)
    except ValueError:
        rel = Path(os.path.relpath(target, src.parent))
    url_out = rel.as_posix()
    if "#" in url:
        url_out += "#" + url.split("#", 1)[1]
    return url_out


def _resolve_target(src_dir: Path, url: str) -> Path | None:
    if not url or _URL_RE.match(url):
        return None
    path = url.split("#", 1)[0]
    if path.startswith("/"):
        return (REPO_ROOT / path.lstrip("/")).resolve()
    return (src_dir / path).resolve()


def _code_block_lines(text: str) -> set[int]:
    """Return 0-based line numbers that fall inside fenced code blocks."""
    in_block = False
    lines = text.splitlines()
    inside: set[int] = set()
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_block = not in_block
            continue
        if in_block:
            inside.add(i)
    return inside


def _heal_file(src: Path, fix: bool) -> tuple[list[str], list[str]]:
    text = src.read_text(encoding="utf-8", errors="replace")
    old_src_dir = _old_src_dir(src)
    repairs: list[str] = []
    unresolved: list[str] = []
    new_text = text
    offset = 0
    code_lines = _code_block_lines(text)

    for m in _LINK_RE.finditer(text):
        # Skip links inside fenced code blocks.
        line_no = text[: m.start()].count("\n")
        if line_no in code_lines:
            continue

        # m.group(0) is the full link; group 2 is the URL for image links and
        # group 5 is the URL for regular links.
        url = m.group(2) if m.group(1) is not None else m.group(5)

        # If the link already resolves from its archived location, leave it alone.
        # This avoids false "unresolved" reports for links like "../../../AGENTS.md"
        # that were originally broken but are correct once the file is archived.
        current_target = _resolve_target(src.parent, url)
        if current_target is not None and current_target.exists():
            continue

        # Resolve the link as it would have resolved from the original active file
        target = _resolve_target(old_src_dir, url)
        if target is None:
            continue

        # If the target is an active plan/spec, prefer its completed counterpart.
        # This is the mechanical "insert completed/" rule: the old file was
        # simply archived, so the link only needs that one directory inserted.
        new_target = _map_completed(target)

        if not new_target.exists():
            # Target does not exist in either active or completed trees.
            # In apply mode, remove the link but keep regular link text.
            repairs.append(f"{src.as_posix()}: {url} (missing) -> unlink")
            start = m.start() + offset
            end = m.end() + offset
            if m.group(1) is not None:
                # Image link with no target: drop it entirely.
                replacement = ""
            else:
                # Regular link with no target: keep the visible text.
                replacement = m.group(4)
            new_text = new_text[:start] + replacement + new_text[end:]
            offset += len(replacement) - len(m.group(0))
            continue

        # Compute the correct relative path from the new archived file
        new_url = _best_replacement(src, url, new_target)
        if new_url == url:
            continue

        repairs.append(f"{src.as_posix()}: {url} -> {new_url}")
        start = m.start() + offset
        end = m.end() + offset

        # Replace only the URL part of the link, preserving !, alt text and any title.
        url_local_start = m.start(2) if m.group(1) is not None else m.start(5)
        url_local_end = m.end(2) if m.group(1) is not None else m.end(5)
        full = m.group(0)
        replacement = full[: url_local_start - m.start()] + new_url + full[url_local_end - m.start() :]

        new_text = new_text[:start] + replacement + new_text[end:]
        offset += len(replacement) - len(m.group(0))

    if fix and new_text != text:
        with src.open("w", encoding="utf-8", newline="\n") as f:
            f.write(new_text)

    return repairs, unresolved


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Heal markdown links in archived plans and specs. (mixed: supports --check and --apply)",
        epilog="Default mode is --check. Use --apply to rewrite files.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        default=True,
        help="report stale links and what would be fixed (default, read-only)",
    )
    mode.add_argument(
        "--apply",
        action="store_true",
        help="rewrite links in place (mutating)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    fix = args.apply

    files = _markdown_files()
    all_repairs: list[str] = []
    all_unresolved: list[str] = []

    for src in files:
        repairs, unresolved = _heal_file(src, fix)
        all_repairs.extend(repairs)
        all_unresolved.extend(unresolved)

    for r in all_repairs:
        print(r)
    for u in all_unresolved:
        print(f"unresolved: {u}")

    if all_unresolved:
        return 1
    if all_repairs:
        if fix:
            print(f"\nHealed {len(all_repairs)} link(s).")
        else:
            print(f"\nFound {len(all_repairs)} link(s) that would be healed; use --apply to fix.")
            return 1
    else:
        print("\nNo stale archive links found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
