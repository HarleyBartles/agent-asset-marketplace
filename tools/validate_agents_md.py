#!/usr/bin/env python3
"""Validate that only the allow-listed AGENTS.md files remain in the repo.

This is the CI gate referenced by the .devin/rules migration. After the
migration, scoped law lives in .devin/rules/*.md; AGENTS.md is reserved for
genuinely always-on law.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_AGENTS_MD = {
    "AGENTS.md",
    ".agents/AGENTS.md",
    ".agents/docs/AGENTS.md",
    ".agents/doctrine/AGENTS.md",
    ".agents/guides/AGENTS.md",
    ".agents/plugins/AGENTS.md",
    "sources/third_party/superpowers/obra-superpowers/v6.2.0/AGENTS.md",
}

MAX_ROOT_LINES = 55


def main() -> int:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    agents_files = [
        p for p in result.stdout.split("\0") if p and p.endswith("AGENTS.md")
    ]

    disallowed = [p for p in agents_files if p not in ALLOWED_AGENTS_MD]
    if disallowed:
        print("Disallowed AGENTS.md files found:", file=sys.stderr)
        for p in disallowed:
            print(f"  - {p}", file=sys.stderr)
        print(
            "Scoped law must be in .devin/rules/*.md; see .agents/docs/mesh-policy.md.",
            file=sys.stderr,
        )
        return 1

    for p in agents_files:
        text = (ROOT / p).read_text(encoding="utf-8")
        if any(ord(c) > 127 for c in text):
            print(f"Non-ASCII characters in {p}", file=sys.stderr)
            return 1
        if "<" in text and ">" in text:
            print(f"Placeholder-like '<...>' content in {p}", file=sys.stderr)
            return 1
        if p == "AGENTS.md" and text.count("\n") + 1 > MAX_ROOT_LINES:
            print(f"Root AGENTS.md exceeds {MAX_ROOT_LINES} lines", file=sys.stderr)
            return 1

    print(f"OK validate_agents_md: {len(agents_files)} allowed AGENTS.md file(s) present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
