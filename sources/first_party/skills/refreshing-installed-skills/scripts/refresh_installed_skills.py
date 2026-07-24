#!/usr/bin/env python3
"""Refresh installed skills from the plugin source, then regenerate the index mesh."""

from __future__ import annotations

import argparse
import json
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
            elif sys.platform == "win32" and rel.endswith(".ps1"):
                return ["pwsh", "-File", str(candidate)]
            elif rel.endswith(".sh") and shutil.which("bash"):
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


def _find_skill_core(repo_root: Path, skill_name: str, core_name: str) -> Path | None:
    """Return the path to a skill's core script, searching installed plugins first."""
    fast_path = repo_root / ".agents" / "skills" / skill_name / "scripts" / core_name
    if fast_path.is_file():
        return fast_path

    marketplace = repo_root / ".agents" / "plugins" / "marketplace.json"
    if marketplace.is_file():
        try:
            data = json.loads(marketplace.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        for plugin in data.get("plugins", []):
            if plugin.get("policy", {}).get("installation") != "INSTALLED_BY_DEFAULT":
                continue
            source_path = plugin.get("source", {}).get("path")
            if not source_path:
                continue
            plugin_path = Path(source_path)
            if not plugin_path.is_absolute():
                plugin_path = (repo_root / plugin_path).resolve()
            candidate = plugin_path / "skills" / skill_name / "scripts" / core_name
            if candidate.is_file():
                return candidate

    for pattern in [
        f"codex-marketplace/plugins/*/skills/{skill_name}/scripts/{core_name}",
        f".agents/plugins/marketplace-source/codex-marketplace/plugins/*/skills/{skill_name}/scripts/{core_name}",
    ]:
        for candidate in sorted(repo_root.glob(pattern)):
            if candidate.is_file():
                return candidate
    return None


def find_mesh_script(repo_root: Path) -> Path | None:
    """Return the path to the repo's generating-index-mesh script, if any."""
    return _find_skill_core(repo_root, "generating-index-mesh", "generate_index_mesh.py")


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
        result = subprocess.run(
            override + (["--check"] if args.check else []),
            cwd=repo_root,
            env=_stripped_env(),
        )
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
