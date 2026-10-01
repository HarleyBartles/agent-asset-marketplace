#!/usr/bin/env python3
"""Create a git worktree at the canonical sibling location and prepare dependencies.

This script follows the skill-bundled CLI contract:
- `--help` prints usage and classifies each flag.
- `--check` (the default) reports what the script would do and exits 0 when
  the requested worktree already exists, otherwise 1.
- `--apply` creates the worktree, initializes pinned submodules, and installs dependencies.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


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
    """Return the main repository worktree root.

    The first worktree reported by `git worktree list` is the main worktree.
    Using this instead of `--git-common-dir` avoids misplacing worktrees when
    the repository uses `--separate-git-dir` or other non-standard git-dir
    layouts.
    """
    result = subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            return Path(line.split(" ", 1)[1]).resolve()
    raise RuntimeError("Could not determine the main repository root")


def _canonical_worktree_root(main_repo_root: Path, branch: str) -> Path:
    repo_name = main_repo_root.name
    return main_repo_root.parent / "_agent-worktrees" / repo_name / branch


def _sanitize_branch_name(branch: str) -> str:
    """Replace filesystem/URL-unsafe characters with a dash.

    This must match the canonical set in the repo-standards scratch-workspace policy.
    """
    return re.sub(r'[:\\?*"<>|/\\\\]', "-", branch)


def _canonical_scratch_root(main_repo_root: Path, branch: str) -> Path:
    repo_name = main_repo_root.name
    return main_repo_root.parent / "_agent-scratch" / repo_name / _sanitize_branch_name(branch)


def _normalize_branch_name(branch: str) -> str:
    """Strip a leading refs/heads/ prefix so full refs can be used as branch names."""
    prefix = "refs/heads/"
    if branch.startswith(prefix):
        branch = branch[len(prefix) :]
    return branch


def _validate_branch_name(branch: str) -> None:
    """Raise ValueError if branch is not a valid git branch name."""
    result = subprocess.run(
        ["git", "check-ref-format", "--branch", branch],
        capture_output=True,
        text=True,
        env=_stripped_env(),
    )
    if result.returncode != 0:
        raise ValueError(f"invalid branch name: {branch!r}")


def _validate_worktree_root(main_repo_root: Path, branch: str) -> Path:
    """Return the resolved worktree path, refusing paths that escape the canonical root."""
    _validate_branch_name(branch)
    canonical_root = _canonical_worktree_root(main_repo_root, "placeholder").parent
    worktree_root = _canonical_worktree_root(main_repo_root, branch).resolve()
    try:
        worktree_root.relative_to(canonical_root.resolve())
    except ValueError as exc:
        raise ValueError(f"branch {branch!r} would place worktree outside the canonical root {canonical_root}") from exc
    if worktree_root == canonical_root.resolve():
        raise ValueError(f"branch {branch!r} resolves to the canonical worktree root")
    return worktree_root


def _is_under_repo(repo_root: Path, candidate: Path) -> bool:
    """Return True if candidate resolves to a path inside repo_root."""
    try:
        candidate.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return False
    return True


def _find_command_bus(repo_root: Path) -> Optional[Path]:
    """Return the repo's canonical command-bus entry point if one exists.

    Prefer the concrete Python bus so the dispatch can run it directly; fall
    back to platform wrappers only when the Python bus is absent.
    """
    for name in ("run.py", "run", "run.ps1"):
        candidate = repo_root / "tools" / name
        if candidate.is_file():
            return candidate
    return None


def _shell_path(path: Path, shell: str) -> str:
    """Render a native path for the selected POSIX shell on Windows."""
    if os.name != "nt":
        return str(path)
    shell_path = Path(shell)
    if shell_path.name.lower() == "bash.exe" and "system32" in {part.lower() for part in shell_path.parts}:
        drive = path.drive.rstrip(":").lower()
        tail = path.as_posix().split(":", 1)[1].lstrip("/")
        return f"/mnt/{drive}/{tail}"
    return path.as_posix()


def _dispatch_capability(
    repo_root: Path,
    capability: str,
    *extra: str,
) -> Optional[int]:
    """Run a named capability through the repo's command bus, or return None to fall back.

    Returns the command's exit code when the bus owns the capability. Returns
    None when the repo has no command bus or the bus does not advertise the
    capability, signalling the caller to use the bundled implementation. A
    repo-owned command that fails is never silently retried.
    """
    bus = _find_command_bus(repo_root)
    if bus is None:
        return None

    if bus.suffix == ".py":
        cmd = [sys.executable, str(bus), capability, *extra]
    elif bus.suffix == ".ps1":
        ps = shutil.which("pwsh") or shutil.which("powershell")
        if not ps:
            return None
        cmd = [ps, "-ExecutionPolicy", "Bypass", "-File", str(bus), capability, *extra]
    else:
        shell = shutil.which("bash") or shutil.which("sh")
        if not shell:
            return None
        # POSIX shells on Windows treat backslashes in a native path as escape
        # characters. Forward slashes keep the absolute drive path intact for
        # Git Bash and other Windows-hosted sh implementations.
        bus_arg = _shell_path(bus, shell)
        cmd = [shell, bus_arg, capability, *extra]

    result = subprocess.run(
        cmd,
        cwd=repo_root,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )

    is_unknown = result.returncode == 2 and "invalid choice" in (result.stdout + result.stderr).lower()

    # Only surface bus output when the repo actually owns the capability.
    if not is_unknown:
        if result.stdout:
            sys.stdout.write(result.stdout)
        if result.stderr:
            sys.stderr.write(result.stderr)

    if is_unknown:
        return None
    return result.returncode


def _run_command(cmd: list[str], cwd: Path) -> int:
    """Run an external command, using the shell on Windows for .cmd/.bat tools."""
    if sys.platform == "win32":
        command = subprocess.list2cmdline([str(arg) for arg in cmd])
        result = subprocess.run(
            command,
            cwd=cwd,
            env=_stripped_env(),
            shell=True,
            text=True,
        )
    else:
        result = subprocess.run(
            [str(arg) for arg in cmd],
            cwd=cwd,
            env=_stripped_env(),
            text=True,
        )
    return result.returncode


def _is_poetry_project(repo_root: Path) -> bool:
    """Return True when the repo's pyproject.toml is managed by Poetry."""
    pyproject = repo_root / "pyproject.toml"
    if not pyproject.is_file():
        return False
    if (repo_root / "poetry.lock").is_file():
        return True
    try:
        text = pyproject.read_text(encoding="utf-8")
    except OSError:
        return False
    return re.search(r"^\[tool\.poetry\]", text, re.MULTILINE) is not None


def _install_dependencies(repo_root: Path) -> int:
    """Install dependencies for common package managers when not repo-owned.

    Runs every recognised installer so mixed-language worktrees get all of their
    dependencies. Returns 0 when there is nothing to do or every installation
    succeeds. A failed installation or a recognised manifest without its required
    installer returns a non-zero exit code so the worktree is not left broken.
    """
    package_lock = repo_root / "package-lock.json"
    package_json = repo_root / "package.json"
    yarn_lock = repo_root / "yarn.lock"
    pnpm_lock = repo_root / "pnpm-lock.yaml"
    requirements = repo_root / "requirements.txt"

    exit_codes = []

    if package_lock.is_file():
        if not shutil.which("npm"):
            print(f"error: package-lock.json present in {repo_root} but npm is not available", file=sys.stderr)
            return 1
        print(f"Installing npm dependencies (ci) in {repo_root}")
        exit_codes.append(_run_command(["npm", "ci"], repo_root))
    elif yarn_lock.is_file():
        if not shutil.which("yarn"):
            print(f"error: yarn.lock present in {repo_root} but yarn is not available", file=sys.stderr)
            return 1
        print(f"Installing yarn dependencies in {repo_root}")
        exit_codes.append(_run_command(["yarn", "install", "--frozen-lockfile"], repo_root))
    elif pnpm_lock.is_file():
        if not shutil.which("pnpm"):
            print(f"error: pnpm-lock.yaml present in {repo_root} but pnpm is not available", file=sys.stderr)
            return 1
        print(f"Installing pnpm dependencies in {repo_root}")
        exit_codes.append(_run_command(["pnpm", "install", "--frozen-lockfile"], repo_root))
    elif package_json.is_file():
        if not shutil.which("npm"):
            print(f"error: package.json present in {repo_root} but npm is not available", file=sys.stderr)
            return 1
        print(f"Installing npm dependencies in {repo_root}")
        exit_codes.append(_run_command(["npm", "install"], repo_root))

    if requirements.is_file():
        pip = shutil.which("pip") or shutil.which("pip3")
        if not pip:
            # pip may be available only as `python -m pip` in some Python
            # distributions. Do not delete the worktree for a missing pip
            # executable; the user can install requirements manually.
            print(
                f"warning: requirements.txt present in {repo_root} but pip is not on PATH; "
                "leaving the worktree for manual Python setup",
                file=sys.stderr,
            )
        else:
            print(f"Installing Python requirements in {repo_root}")
            pip_code = _run_command([pip, "install", "-r", "requirements.txt"], repo_root)
            if pip_code != 0:
                # pip is often blocked on externally-managed Python installs. Do not
                # delete a freshly created worktree for this; the worktree is still
                # useful and the user can install dependencies into a venv later.
                print(
                    f"warning: pip install failed in {repo_root}; leaving the worktree for manual Python setup",
                    file=sys.stderr,
                )

    if _is_poetry_project(repo_root):
        if not shutil.which("poetry"):
            print(f"error: Poetry project detected in {repo_root} but poetry is not available", file=sys.stderr)
            return 1
        print(f"Installing Poetry dependencies in {repo_root}")
        exit_codes.append(_run_command(["poetry", "install", "--no-interaction"], repo_root))

    return next((code for code in exit_codes if code != 0), 0)


def _init_submodules(worktree_root: Path) -> int:
    """Initialize and update submodules in the new worktree.

    A linked worktree does not automatically populate submodule checkouts.
    Initialize the consumer-pinned revisions without fetching or advancing them.
    """
    gitmodules = worktree_root / ".gitmodules"
    if not gitmodules.is_file():
        return 0

    result = subprocess.run(
        ["git", "submodule", "update", "--init", "--recursive"],
        cwd=worktree_root,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"error: failed to initialize submodules in {worktree_root}: {result.stderr.strip()}", file=sys.stderr)
        return result.returncode
    return 0


def _configure_worktree(
    worktree_root: Path,
) -> int:
    """Initialize generic submodules and repository dependencies in the new worktree."""
    exit_code = _init_submodules(worktree_root)
    if exit_code != 0:
        return exit_code

    exit_code = _dispatch_capability(worktree_root, "install-deps", "--apply")
    if exit_code is None:
        exit_code = _install_dependencies(worktree_root)
    if exit_code != 0:
        print(f"error: installing dependencies failed in {worktree_root}", file=sys.stderr)
        return exit_code

    print(f"Worktree ready at {worktree_root}")
    return 0


def _default_base_ref(main_repo_root: Path) -> tuple[str, bool]:
    """Return the base ref to use and whether it was resolved from origin."""
    fetch = subprocess.run(
        ["git", "fetch", "origin"],
        cwd=main_repo_root,
        env=_stripped_env(),
        capture_output=True,
    )
    if fetch.returncode == 0:
        return "origin/main", True
    return "HEAD", False


def _check_worktree(
    main_repo_root: Path,
    branch: str,
    base_ref: Optional[str],
) -> tuple[int, str, str]:
    """Return (exit_code, human_summary, base_ref_to_use).

    - 0 if the worktree already exists and no changes are needed.
    - 1 if the worktree would be created (or the base ref is missing).
    """
    try:
        worktree_root = _validate_worktree_root(main_repo_root, branch)
    except ValueError as exc:
        return 1, f"error: {exc}", ""

    resolved = worktree_root.resolve()
    result = subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        cwd=main_repo_root,
        env=_stripped_env(),
        capture_output=True,
        text=True,
        check=False,
    )
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            existing = Path(line.split(" ", 1)[1]).resolve()
            if existing == resolved:
                return 0, f"OK worktree already exists at {resolved}", ""

    if resolved.is_dir() or resolved.is_file():
        return 1, f"Would fail: path already exists on disk but is not a registered worktree ({resolved})", ""

    effective_base = base_ref
    if effective_base is None:
        effective_base, _ = _default_base_ref(main_repo_root)

    if effective_base == "origin/main":
        verify = subprocess.run(
            ["git", "rev-parse", "--verify", "origin/main"],
            cwd=main_repo_root,
            env=_stripped_env(),
            capture_output=True,
            text=True,
        )
        if verify.returncode != 0:
            return 1, "Would fail: origin/main is not available (fetch from origin failed or ref is missing)", ""

    return 1, f"Would create worktree {resolved} from {effective_base} (branch {branch})", effective_base


def _apply_worktree(
    main_repo_root: Path,
    branch: str,
    base_ref: str,
) -> int:
    worktree_root = _validate_worktree_root(main_repo_root, branch)

    if worktree_root.is_file():
        print(f"error: worktree path is an existing file: {worktree_root}", file=sys.stderr)
        return 1
    if worktree_root.is_dir():
        print(f"error: worktree directory already exists: {worktree_root}", file=sys.stderr)
        return 1

    worktree_root.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["git", "worktree", "add", "--no-track", "-b", branch, str(worktree_root), base_ref]

    # Run from the main worktree so that the default base is origin/main, not the
    # HEAD of any linked worktree the user may be invoking this script from.
    result = subprocess.run(cmd, cwd=main_repo_root, env=_stripped_env())
    if result.returncode != 0:
        return result.returncode

    exit_code = _configure_worktree(worktree_root)
    if exit_code != 0:
        return exit_code

    scratch_root = _canonical_scratch_root(main_repo_root, branch)
    scratch_root.mkdir(parents=True, exist_ok=True)
    print(f"Scratch ready at {scratch_root}")

    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a git worktree at the canonical sibling location. (mixed: supports --check and --apply)",
        epilog="Default mode is --check. Use --apply to create the worktree.",
    )
    parser.add_argument("branch", nargs="?", default=None, help="branch name to create (read-only during --check)")
    parser.add_argument(
        "--base-ref",
        default=None,
        help=(
            "base ref for the new branch (default: origin/main, or HEAD if origin/main is unavailable; "
            "read-only during --check)"
        ),
    )
    parser.add_argument(
        "--no-skill-refresh",
        action="store_true",
        help="deprecated compatibility flag; repo plugins load from native worktree config",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        default=True,
        help="report what the script would do and exit 0 if no changes are needed (default, read-only)",
    )
    mode.add_argument(
        "--apply",
        action="store_true",
        help="create the worktree, initialize submodules, and install dependencies (mutating)",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    _reject_submodule()
    main_repo_root = _main_repo_root()
    branch = _normalize_branch_name(args.branch)

    if args.apply:
        if args.branch is None:
            print("error: branch is required for --apply", file=sys.stderr)
            return 2
        base_ref = args.base_ref
        if base_ref is None:
            base_ref, _ = _default_base_ref(main_repo_root)
        return _apply_worktree(
            main_repo_root,
            branch,
            base_ref,
        )

    # Default / --check mode
    if args.branch is None:
        print("OK pass a branch to check a specific worktree")
        return 0
    exit_code, summary, _ = _check_worktree(main_repo_root, branch, args.base_ref)
    print(summary)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
