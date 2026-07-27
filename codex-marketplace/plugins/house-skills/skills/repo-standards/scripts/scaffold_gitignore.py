#!/usr/bin/env python3
"""Ensure the repo's SDD workspace is gitignored via its local .gitignore."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


SDD_GITIGNORE_CONTENT = "*\n!.gitignore\n"
SDD_GITIGNORE_PATH = Path(".agents") / "superpowers" / "sdd" / ".gitignore"

STALE_RULE_PATTERNS = {
    ".agents/superpowers/sdd/**",
    "!.agents/superpowers/sdd/.gitignore",
}

# Full block the old scaffold used to append; removed in apply mode if contiguous.
STALE_RULE_BLOCK = """# Superpowers sdd/ is a local-only session workspace.
# Track only the directory scaffold (.gitignore); ignore all session contents at any depth.
# plans/ and specs/ are fully repo resident and not governed by this block.
.agents/superpowers/sdd/**
!.agents/superpowers/sdd/.gitignore"""


def _stripped_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    return Path(result.stdout.strip())


def _sdd_gitignore_path(repo_root: Path) -> Path:
    return repo_root / SDD_GITIGNORE_PATH


def _has_sdd_rule(content: str) -> bool:
    lines = {line.strip() for line in content.splitlines()}
    return "*" in lines and "!.gitignore" in lines


def _has_stale_root_rule(content: str) -> bool:
    lines = {line.strip() for line in content.splitlines()}
    return bool(STALE_RULE_PATTERNS & lines)


def _remove_stale_root_rule(content: str) -> str:
    # Remove the exact contiguous block the old scaffold used to append.
    if STALE_RULE_BLOCK in content:
        content = content.replace(STALE_RULE_BLOCK, "")
    # Remove any remaining stale pattern lines that may have been added manually.
    lines = content.splitlines()
    cleaned = [line for line in lines if line.strip() not in STALE_RULE_PATTERNS]
    text = "\n".join(cleaned).rstrip()
    if text:
        text += "\n"
    return text


def main(argv: list[str] | None = None) -> int:
    epilog = """\
examples:
  %(prog)s --check               verify the sdd .gitignore rule
  %(prog)s                       create the sdd .gitignore rule if missing
  %(prog)s --force               same as without --force (accepted for uniform CLI)

The SDD workspace is .agents/superpowers/sdd/. It must be ignored by a local
.gitignore file containing:

  *
  !.gitignore

The root .gitignore must not contain the stale rule:

  .agents/superpowers/sdd/**
  !.agents/superpowers/sdd/.gitignore

If the rule is already present, the script makes no changes. Other rules are
preserved.

exit codes:
  0  rule is present or was applied
  1  drift detected or files could not be written"""
    parser = argparse.ArgumentParser(
        description="Ensure the repo's SDD workspace is gitignored via its local .gitignore.",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report drift without writing",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Accepted for a uniform scaffold interface; has no destructive effect",
    )
    args = parser.parse_args(argv)

    repo_root = _repo_root()
    root_gitignore_path = repo_root / ".gitignore"
    sdd_gitignore_path = _sdd_gitignore_path(repo_root)

    drift_messages: list[str] = []

    if not root_gitignore_path.is_file():
        drift_messages.append("DRIFT: .gitignore missing")
    else:
        root_content = root_gitignore_path.read_text(encoding="utf-8")
        if _has_stale_root_rule(root_content):
            drift_messages.append("DRIFT: .gitignore contains stale sdd rule")

    if not sdd_gitignore_path.is_file():
        drift_messages.append(f"DRIFT: {SDD_GITIGNORE_PATH.as_posix()} missing")
    else:
        sdd_content = sdd_gitignore_path.read_text(encoding="utf-8")
        if not _has_sdd_rule(sdd_content):
            drift_messages.append(
                f"DRIFT: {SDD_GITIGNORE_PATH.as_posix()} missing required rule(s)"
            )

    if args.check:
        if drift_messages:
            for msg in drift_messages:
                print(msg)
            return 1
        print("OK .gitignore: sdd rule present")
        return 0

    if drift_messages:
        if not root_gitignore_path.is_file():
            root_gitignore_path.write_text("", encoding="utf-8", newline="\n")
            print(f"wrote {root_gitignore_path.relative_to(repo_root).as_posix()}")
        else:
            root_content = root_gitignore_path.read_text(encoding="utf-8")
            cleaned = _remove_stale_root_rule(root_content)
            if cleaned != root_content:
                with root_gitignore_path.open("w", encoding="utf-8", newline="\n") as f:
                    f.write(cleaned)
                print(f"updated {root_gitignore_path.relative_to(repo_root).as_posix()}")

        sdd_gitignore_path.parent.mkdir(parents=True, exist_ok=True)
        if not sdd_gitignore_path.is_file() or sdd_gitignore_path.read_text(encoding="utf-8") != SDD_GITIGNORE_CONTENT:
            sdd_gitignore_path.write_text(SDD_GITIGNORE_CONTENT, encoding="utf-8", newline="\n")
            print(f"wrote {sdd_gitignore_path.relative_to(repo_root).as_posix()}")
        return 0

    print("OK .gitignore: sdd rule present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
