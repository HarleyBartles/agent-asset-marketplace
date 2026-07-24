#!/usr/bin/env python3
"""Create a git worktree at the canonical sibling location and refresh skills."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


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


def _reject_submodule() -> None:
    result = subprocess.run(
        ["git", "rev-parse", "--show-superproject-working-tree"],
        capture_output=True,
        text=True,
        env=_stripped_env(),
    )
    if result.returncode == 0 and result.stdout.strip():
        raise RuntimeError("This script must not run inside a git submodule")


def _main_repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    common = Path(result.stdout.strip())
    if not common.is_absolute():
        common = (_repo_root() / common).resolve()
    else:
        common = common.resolve()
    return common.parent


def _canonical_worktree_root(main_repo_root: Path, branch: str) -> Path:
    repo_name = main_repo_root.name
    return main_repo_root.parent / "_agent-worktrees" / repo_name / branch


def _find_refresh_script(worktree_root: Path) -> Path | None:
    candidates = [
        worktree_root / ".agents" / "skills" / "refreshing-installed-skills" / "scripts" / "refresh_installed_skills.py",
    ]
    for pattern in [
        "codex-marketplace/plugins/*/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py",
        ".agents/plugins/marketplace-source/codex-marketplace/plugins/*/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py",
    ]:
        candidates.extend(sorted(worktree_root.glob(pattern)))
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a git worktree at the canonical sibling location")
    parser.add_argument("branch", help="branch name to create")
    parser.add_argument("--base-ref", default=None, help="base ref for the new branch (default: HEAD)")
    parser.add_argument("--no-skill-refresh", action="store_true", help="skip refreshing installed skills in the new worktree")
    args = parser.parse_args(argv)

    repo_root = _repo_root()
    _reject_submodule()
    main_repo_root = _main_repo_root()

    worktree_root = _canonical_worktree_root(main_repo_root, args.branch)
    if worktree_root.exists():
        print(f"error: worktree path already exists: {worktree_root}", file=sys.stderr)
        return 1

    worktree_root.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["git", "worktree", "add", str(worktree_root), "-b", args.branch]
    if args.base_ref:
        cmd.append(args.base_ref)

    result = subprocess.run(cmd, cwd=repo_root, env=_stripped_env())
    if result.returncode != 0:
        return result.returncode

    if not args.no_skill_refresh:
        refresh_script = _find_refresh_script(worktree_root)
        if refresh_script:
            subprocess.run([sys.executable, str(refresh_script)], cwd=worktree_root, env=_stripped_env())
        else:
            print("warning: refreshing-installed-skills not found; run it manually in the new worktree", file=sys.stderr)

    print(f"Worktree ready at {worktree_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
