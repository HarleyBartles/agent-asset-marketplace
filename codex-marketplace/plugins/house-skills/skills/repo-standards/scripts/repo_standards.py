#!/usr/bin/env python3
"""Check or apply the repo-standards shape."""

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
        capture_output=True, text=True, check=True, env=_stripped_env(),
    )
    return Path(result.stdout.strip())


def _is_shared_checkout(repo_root: Path) -> bool:
    git_dir = subprocess.run(
        ["git", "rev-parse", "--absolute-git-dir"],
        cwd=repo_root, capture_output=True, text=True, check=True, env=_stripped_env(),
    ).stdout.strip()
    git_common = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=repo_root, capture_output=True, text=True, check=True, env=_stripped_env(),
    ).stdout.strip()
    # A linked worktree (shared checkout) has its git-dir under .git/worktrees/<name>
    # while the common dir is the main .git directory.
    return Path(git_dir).resolve() != Path(git_common).resolve()


def _is_submodule(repo_root: Path) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--show-superproject-working-tree"],
        cwd=repo_root, capture_output=True, text=True, env=_stripped_env(),
    )
    return result.returncode == 0 and result.stdout.strip()


def _manifest_path() -> Path:
    return Path(__file__).resolve().parent.parent / "references" / "repository-shape-manifest.json"


def _template_path(surface: dict[str, object]) -> Path | None:
    source = surface.get("source")
    if not source:
        return None
    return Path(__file__).resolve().parent.parent / "templates" / str(source)


def _scaffold_script_path(surface: dict[str, object]) -> Path | None:
    scaffold = surface.get("scaffold")
    if not scaffold:
        return None
    return Path(__file__).resolve().parent / str(scaffold)


def _git_hooks_dir(repo_root: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--git-path", "hooks"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    return Path(result.stdout.strip())


def _check_surface_content(repo_root: Path, rel: str, template: Path | None) -> list[str]:
    findings: list[str] = []
    full = repo_root / rel
    if not full.is_file():
        findings.append(f"missing: {rel}")
        return findings
    if template is not None and template.is_file():
        expected = template.read_bytes()
        actual = full.read_bytes()
        if expected != actual:
            findings.append(f"drift: {rel}")
    return findings


def _check_marketplace_json(repo_root: Path, rel: str) -> list[str]:
    findings: list[str] = []
    full = repo_root / rel
    if not full.is_file():
        findings.append(f"missing: {rel}")
        return findings
    try:
        data = json.loads(full.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        findings.append(f"invalid JSON {rel}: {exc}")
        return findings
    if not isinstance(data, dict) or not isinstance(data.get("repo"), dict):
        findings.append(f"drift: {rel} missing top-level 'repo' object")
        return findings
    prefixes = data["repo"].get("local_skill_prefixes")
    if not isinstance(prefixes, list) or not prefixes:
        findings.append(f"drift: {rel} repo.local_skill_prefixes is missing or empty")
    return findings


def _check_surface(repo_root: Path, surface: dict[str, object]) -> list[str]:
    findings: list[str] = []
    rel = str(surface["path"])
    kind = str(surface.get("kind", "file"))
    template = _template_path(surface)
    if kind == "submodule":
        gitmodules = repo_root / ".gitmodules"
        if not gitmodules.is_file():
            findings.append(f"missing .gitmodules for submodule: {rel}")
            return findings
        if rel not in gitmodules.read_text(encoding="utf-8"):
            findings.append(f"missing submodule entry: {rel}")
            return findings
        if not (repo_root / rel / ".git").exists() and not (repo_root / ".git" / "modules" / rel.replace("/", "-")).exists():
            findings.append(f"submodule not initialized: {rel}")
        return findings
    if kind == "hook":
        hook_path = _git_hooks_dir(repo_root) / Path(rel).name
        if not hook_path.is_file():
            findings.append(f"missing hook: {rel}")
            return findings
        if template is not None and template.is_file():
            expected = template.read_bytes()
            actual = hook_path.read_bytes()
            if expected != actual:
                findings.append(f"drift: {rel}")
        return findings
    if rel == ".agents/plugins/marketplace.json":
        return _check_marketplace_json(repo_root, rel)
    if rel == ".gitignore":
        gitignore = repo_root / ".gitignore"
        if not gitignore.is_file():
            findings.append("missing: .gitignore")
            return findings
        text = gitignore.read_text(encoding="utf-8")
        if ".agents/superpowers/sdd/**" not in text or "!.agents/superpowers/sdd/.gitignore" not in text:
            findings.append("drift: .gitignore missing sdd rule")
        return findings
    if not (repo_root / rel).exists():
        findings.append(f"missing: {rel}")
        return findings
    if template is not None:
        findings.extend(_check_surface_content(repo_root, rel, template))
    return findings


def _apply_surface(repo_root: Path, surface: dict[str, object]) -> bool:
    rel = str(surface["path"])
    kind = str(surface.get("kind", "file"))
    template = _template_path(surface)
    scaffold = _scaffold_script_path(surface)
    if kind in ("file", "hook") and template is not None:
        if kind == "hook":
            full = _git_hooks_dir(repo_root) / Path(rel).name
        else:
            full = repo_root / rel
        full.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(template, full)
        if kind == "hook":
            full.chmod(0o755)
        print(f"wrote {rel}")
        return True
    if scaffold is not None and scaffold.is_file():
        result = subprocess.run(
            [sys.executable, str(scaffold)],
            cwd=repo_root,
            capture_output=True,
            text=True,
            env=_stripped_env(),
        )
        if result.returncode != 0:
            print(f"error applying {rel}: {result.stderr or result.stdout}", file=sys.stderr)
            return False
        print(result.stdout.strip())
        return True
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check or apply repo-standards")
    parser.add_argument("--check", action="store_true", help="report drift only")
    parser.add_argument("--apply", action="store_true", help="apply missing surfaces")
    parser.add_argument("--yes", action="store_true", help="skip interactive approval")
    parser.add_argument("--allow-shared-checkout", action="store_true", help="allow writes in the shared checkout")
    args = parser.parse_args(argv)

    repo_root = _repo_root()
    if _is_submodule(repo_root):
        print("error: repo-standards must not run inside a submodule", file=sys.stderr)
        return 1

    manifest = json.loads(_manifest_path().read_text(encoding="utf-8"))
    surfaces = manifest.get("surfaces", [])

    findings: list[str] = []
    for surface in surfaces:
        findings.extend(_check_surface(repo_root, surface))

    if args.check or not args.apply:
        if findings:
            for f in findings:
                print(f"DRIFT: {f}")
            return 1
        print("OK repo-standards: all surfaces present")
        return 0

    if args.allow_shared_checkout:
        print("warning: --allow-shared-checkout is an override and requires human approval before applying changes", file=sys.stderr)
    if not args.allow_shared_checkout and _is_shared_checkout(repo_root):
        print("error: shared checkout; use --allow-shared-checkout to override", file=sys.stderr)
        return 1

    if not args.yes:
        print(f"Will apply {len(findings)} missing surfaces: {findings}")
        print("Add --yes to apply.")
        return 1

    for surface in surfaces:
        if _check_surface(repo_root, surface):
            _apply_surface(repo_root, surface)
    print("OK repo-standards: applied missing surfaces")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
