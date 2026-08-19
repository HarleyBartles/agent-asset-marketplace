#!/usr/bin/env python3
"""Synchronize canonical shared references into the superpowers-plus vendored skills."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIR = ROOT / "codex-marketplace" / "plugins" / "superpowers-plus" / "references"
SKILL_DIR = ROOT / "codex-marketplace" / "plugins" / "superpowers-plus" / "skills"

SHARES = {
    "plan-scope-sizing.md": [
        "writing-plans",
        "working-with-epics",
    ],
    "execution-lane-override.md": [
        "executing-plans",
        "subagent-driven-development",
        "dispatching-parallel-agents",
    ],
}


def _canonical_text(filename: str) -> str:
    canonical = CANONICAL_DIR / filename
    if not canonical.exists():
        raise FileNotFoundError(f"Canonical reference missing: {canonical.relative_to(ROOT)}")
    return canonical.read_text(encoding="utf-8")


def _check() -> None:
    failures = 0
    for filename, skills in SHARES.items():
        canonical_text = _canonical_text(filename)
        for skill in skills:
            target = SKILL_DIR / skill / "references" / filename
            if not target.exists():
                print(f"MISSING {target.relative_to(ROOT)}")
                failures += 1
                continue
            target_text = target.read_text(encoding="utf-8")
            if target_text != canonical_text:
                print(f"STALE {target.relative_to(ROOT)}")
                failures += 1
            else:
                print(f"OK {target.relative_to(ROOT)}")
    if failures:
        raise SystemExit(f"{failures} skill reference(s) are missing or stale; run --apply")
    print("All shared skill references are current.")


def _apply() -> None:
    for filename, skills in SHARES.items():
        canonical_text = _canonical_text(filename)
        for skill in skills:
            target = SKILL_DIR / skill / "references" / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(canonical_text, encoding="utf-8", newline="\n")
            print(f"Wrote {target.relative_to(ROOT)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Synchronize canonical shared references into the superpowers-plus vendored skills. (mixed)"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="validate without writing (default)")
    group.add_argument("--apply", action="store_true", help="write the reference copies")
    args = parser.parse_args(argv)
    if args.apply:
        _apply()
    else:
        _check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
