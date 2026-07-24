#!/usr/bin/env python3
"""Refresh installed skills from the plugin source, then regenerate the index mesh."""

from __future__ import annotations

import argparse
import os
import shutil
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


def _init_marketplace_source(repo_root: Path) -> None:
    submodule = repo_root / ".agents" / "plugins" / "marketplace-source"
    if not (repo_root / ".gitmodules").is_file():
        return
    if not submodule.exists():
        return
    subprocess.run(
        ["git", "submodule", "update", "--init", "--recursive", str(submodule.relative_to(repo_root))],
        cwd=repo_root,
        env=_stripped_env(),
        check=True,
    )


def _find_override(repo_root: Path) -> list[str] | None:
    for rel in [
        "scripts/refresh-installed-skills.py",
        "scripts/refresh-installed-skills.ps1",
        "scripts/refresh-installed-skills.sh",
        "tools/refresh-installed-skills.py",
        "tools/refresh-installed-skills.ps1",
        "tools/refresh-installed-skills.sh",
    ]:
        candidate = repo_root / rel
        if candidate.is_file():
            if rel.endswith(".py"):
                return [sys.executable, str(candidate)]
            if sys.platform == "win32" and rel.endswith(".ps1"):
                return ["pwsh", "-File", str(candidate)]
            if shutil.which("bash"):
                return ["bash", str(candidate)]
            raise RuntimeError(f"Found {candidate} but no interpreter available")
    return None


def find_install_command(repo_root: Path) -> list[str] | None:
    """Return the command list for the repo's install_agent_skills.py, if any."""
    if (repo_root / "codex-marketplace" / "plugins").is_dir() and (repo_root / "tools" / "install_agent_skills.py").is_file():
        return [sys.executable, str(repo_root / "tools" / "install_agent_skills.py")]
    _init_marketplace_source(repo_root)
    if (repo_root / "scripts" / "install_agent_skills.py").is_file():
        return [sys.executable, str(repo_root / "scripts" / "install_agent_skills.py")]
    return None


def find_mesh_script(repo_root: Path) -> Path | None:
    """Return the path to the repo's generating-index-mesh script, if any."""
    candidates = [
        repo_root / ".agents" / "skills" / "generating-index-mesh" / "scripts" / "generate_index_mesh.py",
    ]
    for pattern in [
        "codex-marketplace/plugins/*/skills/generating-index-mesh/scripts/generate_index_mesh.py",
        ".agents/plugins/marketplace-source/codex-marketplace/plugins/*/skills/generating-index-mesh/scripts/generate_index_mesh.py",
    ]:
        candidates.extend(sorted(repo_root.glob(pattern)))
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def _git_has_changes(repo_root: Path) -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        env=_stripped_env(),
    )
    return bool(result.stdout.strip())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Refresh installed skills and regenerate the index mesh")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    args = parser.parse_args(argv)

    repo_root = _repo_root()
    _reject_submodule()

    override = _find_override(repo_root)
    if override:
        result = subprocess.run(override, cwd=repo_root, env=_stripped_env())
        return result.returncode

    install_cmd = find_install_command(repo_root)
    if install_cmd is None:
        print("error: no install_agent_skills.py command found", file=sys.stderr)
        return 1

    install_run = install_cmd + (["--check"] if args.check else [])
    result = subprocess.run(install_run, cwd=repo_root, env=_stripped_env())
    if result.returncode != 0:
        return result.returncode

    mesh_script = find_mesh_script(repo_root)
    if mesh_script is None:
        print("error: generating-index-mesh skill not found", file=sys.stderr)
        return 1
    mesh_cmd = [sys.executable, str(mesh_script)] + (["--check"] if args.check else [])
    result = subprocess.run(mesh_cmd, cwd=repo_root, env=_stripped_env())
    if result.returncode != 0:
        return result.returncode

    if not args.check and _git_has_changes(repo_root):
        subprocess.run(["git", "add", "-A"], cwd=repo_root, env=_stripped_env(), check=True)
        subprocess.run(
            ["git", "commit", "-m", "chore: refresh installed skills and regenerate index mesh"],
            cwd=repo_root,
            env=_stripped_env(),
            check=True,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
