#!/usr/bin/env python3
"""Sync subagent profiles from the current worktree to the main checkout.

The Devin Desktop runtime resolves subagent profiles against the main checkout's
``.agents/agents/`` directory, even when the agent is working in a linked
worktree. This script copies the worktree's ``reviewer-*.md`` (and any other
``.agents/agents/*.md``) profiles to the main checkout so the runtime can
``run_subagent`` with new or changed profiles while a feature branch is still in
progress.

The main checkout files are intentionally left uncommitted. They are staging
copies for the local runtime and will be overwritten/replaced when the feature
branch is merged and the main checkout is updated normally.
"""

from __future__ import annotations

import argparse
import difflib
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT / ".agents" / "agents"


def _git(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def _find_main_worktree() -> Path:
    """Return the filesystem path of the main (non-linked) git worktree."""
    output = _git("worktree", "list", "--porcelain")
    entries: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for raw in output.splitlines():
        if raw.startswith("worktree "):
            if current:
                entries.append(current)
            current = {"worktree": raw.split(" ", 1)[1]}
        elif raw.startswith("HEAD "):
            current["head"] = raw.split(" ", 1)[1]
        elif raw.startswith("branch "):
            current["branch"] = raw.split(" ", 1)[1]
        elif raw.startswith("bare"):
            current["bare"] = "true"
        elif raw == "":
            continue
    if current:
        entries.append(current)

    for entry in entries:
        if entry.get("bare"):
            continue
        branch = entry.get("branch", "")
        if branch == "refs/heads/main":
            return Path(entry["worktree"]).resolve()

    # Fallback: the worktree whose git directory is the common git directory.
    git_dir = Path(_git("rev-parse", "--absolute-git-dir").strip()).resolve()
    common_dir = Path(_git("rev-parse", "--git-common-dir").strip())
    if not common_dir.is_absolute():
        common_dir = (git_dir / common_dir).resolve()
    for entry in entries:
        if entry.get("bare"):
            continue
        candidate = Path(entry["worktree"]).resolve()
        candidate_git_dir = subprocess.run(
            ["git", "rev-parse", "--absolute-git-dir"],
            cwd=candidate,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if Path(candidate_git_dir).resolve() == common_dir:
            return candidate

    raise RuntimeError("Could not find the main git worktree")


def _profile_paths(agents_dir: Path) -> list[Path]:
    if not agents_dir.is_dir():
        return []
    return sorted(p for p in agents_dir.iterdir() if p.is_file() and p.suffix == ".md")


def _main_worktree_preview(main: Path) -> str:
    """Return a short, human-readable preview of the main worktree for prompts."""
    try:
        status = _git("status", "--short", cwd=main)
        dirty = " (dirty)" if status.strip() else ""
    except subprocess.CalledProcessError:
        dirty = ""
    return f"{main}{dirty}"


def _approve(apply: bool, yes: bool, main: Path, allow_shared: bool) -> bool:
    if not apply:
        return True
    if not allow_shared:
        print(
            "error: applying without --allow-shared-checkout is not allowed; "
            "pass --allow-shared-checkout to write to the main checkout.",
            file=sys.stderr,
        )
        return False
    if yes:
        return True
    try:
        response = input(
            f"This will overwrite subagent profiles in the main checkout "
            f"{_main_worktree_preview(main)}. Continue? (y/N) "
        )
    except (EOFError, KeyboardInterrupt):
        return False
    return response.strip().lower() == "y"


def _needs_sync(source: Path, target: Path) -> bool:
    if not target.exists():
        return True
    if source.read_bytes() == target.read_bytes():
        return False
    return True


def _format_diff(source: Path, target: Path) -> str:
    source_lines = source.read_text(encoding="utf-8").splitlines()
    target_lines = target.read_text(encoding="utf-8").splitlines() if target.exists() else []
    return "\n".join(
        difflib.unified_diff(
            target_lines,
            source_lines,
            fromfile=str(target),
            tofile=str(source),
            lineterm="",
        )
    )


def _sync_profiles(apply: bool, allow_shared: bool, yes: bool) -> int:
    main = _find_main_worktree()
    source_dir = AGENTS_DIR
    target_dir = main / ".agents" / "agents"

    if not source_dir.is_dir():
        print(f"error: source directory does not exist: {source_dir}", file=sys.stderr)
        return 1

    if not _approve(apply, yes, main, allow_shared):
        print("Aborted.", file=sys.stderr)
        return 1

    if apply:
        target_dir.mkdir(parents=True, exist_ok=True)

    source_profiles = _profile_paths(source_dir)
    target_profiles = _profile_paths(target_dir)
    target_by_name = {p.name: p for p in target_profiles}
    source_by_name = {p.name: p for p in source_profiles}

    changed: list[Path] = []
    added: list[Path] = []
    removed: list[Path] = []
    untouched: list[Path] = []

    for source in source_profiles:
        target = target_dir / source.name
        if _needs_sync(source, target):
            if apply:
                target.write_bytes(source.read_bytes())
                if target.name in target_by_name:
                    changed.append(target)
                else:
                    added.append(target)
            else:
                if not target.exists():
                    added.append(source)
                else:
                    changed.append(source)
        else:
            untouched.append(source)

    stale = [p for p in target_profiles if p.name not in source_by_name]
    for target in stale:
        if apply:
            target.unlink()
            removed.append(target)
        else:
            removed.append(target)

    if not apply:
        if not changed and not added and not removed:
            print("OK runtime agents: main checkout is in sync with worktree.")
            return 0
        print("error: main checkout is missing or out of sync with the following profiles:", file=sys.stderr)
        for p in added:
            print(f"  missing: {p.name}", file=sys.stderr)
        for p in removed:
            print(f"  stale: {p.name}", file=sys.stderr)
        for p in changed:
            print(f"  out of sync: {p.name}", file=sys.stderr)
            print(_format_diff(p, target_dir / p.name), file=sys.stderr)
        print(
            f"Run `py -3 {Path(__file__).relative_to(ROOT)} --apply --allow-shared-checkout` to sync, "
            "or `py -3 tools/run.py runtime-agents --apply --allow-shared-checkout`. "
            "Then restart the IDE so the runtime picks up the new profiles.",
            file=sys.stderr,
        )
        return 1

    if not changed and not added and not removed:
        print("OK runtime agents: nothing to sync.")
        return 0

    for target in added:
        print(f"Added {target.relative_to(main)}")
    for target in changed:
        print(f"Updated {target.relative_to(main)}")
    for target in removed:
        print(f"Removed {target.relative_to(main)}")
    print("\nNOTE: an IDE restart is required before the runtime will pick up new or changed subagent profiles.")
    return 0


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Sync subagent profiles from the current worktree to the main checkout "
            "for the runtime. (mixed: --check is read-only, --apply is mutating.)"
        ),
        epilog="Use --apply to copy files; --check (the default) only reports drift.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="copy the current worktree's .agents/agents/*.md profiles to the main checkout",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="report drift without modifying the main checkout (default)",
    )
    parser.add_argument(
        "--allow-shared-checkout",
        action="store_true",
        help="allow applying changes to the main (shared) checkout",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="skip the interactive confirmation when applying changes",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = _parse_args(argv)
        if args.apply and args.check:
            print("error: --apply and --check are mutually exclusive", file=sys.stderr)
            return 1
        apply = args.apply
        if not apply and not args.check:
            args.check = True
        allow_shared = getattr(args, "allow_shared_checkout", False)
        return _sync_profiles(apply, allow_shared, args.yes)
    except FileNotFoundError as exc:
        print(f"error: required command or path not found: {exc}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        print(f"error: git command failed: {exc}", file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
