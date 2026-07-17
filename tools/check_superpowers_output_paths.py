#!/usr/bin/env python3
"""Check for stale .superpowers/ output paths after a superpowers upstream bump.

The upstream obra-superpowers framework defaults to ``.superpowers/`` for its
SDD workspace and brainstorm session files. This repo standardizes on
``.agents/superpowers/`` as the single canonical output directory. Overlay
edits are responsible for repointing upstream references; this tool catches
any that were missed.

Run this manually after bumping the superpowers upstream version to verify
the new upstream source didn't re-introduce non-canonical directory references.

Usage:
    py -3 tools/check_superpowers_output_paths.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _git_lines(*args: str) -> list[str]:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True)
    return result.stdout.splitlines()


def main() -> int:
    # Check 1: no tracked .superpowers/ directory at repo root
    stale_dir = ROOT / ".superpowers"
    if stale_dir.exists():
        tracked = _git_lines("ls-files", ".superpowers/")
        if tracked:
            print(f"FAIL: stale .superpowers/ directory is tracked in git ({len(tracked)} file(s)).")
            print(f"  Remove it with `git rm -r --cached .superpowers/` and use .agents/superpowers/ as the canonical output path.")
            return 1

    # Check 2: no .superpowers/ path references in projected skill files
    projection_root = ROOT / "codex-marketplace" / "plugins" / "superpowers-plus" / "skills"
    if not projection_root.exists():
        print("OK: superpowers-plus projection does not exist yet, nothing to check.")
        return 0

    stale_refs: list[str] = []
    for file_path in sorted(projection_root.rglob("*")):
        if not file_path.is_file():
            continue
        rel = file_path.relative_to(ROOT)
        try:
            text = file_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            if ".superpowers/" in line:
                stale_refs.append(f"{rel}:{line_no}: {line.strip()}")

    if stale_refs:
        print(f"FAIL: stale .superpowers/ output path found in {len(stale_refs)} projected line(s) (must be .agents/superpowers/):")
        for ref in stale_refs[:20]:
            print(f"  {ref}")
        if len(stale_refs) > 20:
            print(f"  ... and {len(stale_refs) - 20} more")
        return 1

    print(f"OK: 0 stale .superpowers/ refs in projection, 0 tracked files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
