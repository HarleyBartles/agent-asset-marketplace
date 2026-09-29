#!/usr/bin/env python3
"""Scaffold or validate the consumer operating-standards composition."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path

import operating_standards_catalog


_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_ROOT = _SCRIPT_DIR.parent
_CATALOG_PATH = _SKILL_ROOT / "references" / "operating-standards-catalog.json"
_MANIFEST_PATH = _SKILL_ROOT / "references" / "repository-shape-manifest.json"
_TEMPLATE_PATH = _SKILL_ROOT / "templates" / "operating-standards.json"
_CONTRACT_RELATIVE = Path(".agents/contracts/operating-standards.json")


def _repo_root() -> Path:
    env = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(name, None)
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    return Path(result.stdout.strip())


def _source_root(repo_root: Path) -> Path:
    submodule = repo_root / ".agents/plugins/marketplace-source"
    if (submodule / "skills/repo-shape").is_dir():
        return submodule
    if (repo_root / "skills/repo-shape").is_dir():
        return repo_root
    raise FileNotFoundError("pinned marketplace-source with Agent Operating Model resources is unavailable")


def _load_catalog(repo_root: Path):
    source_root = _source_root(repo_root)
    catalog_path = (
        _CATALOG_PATH
        if _CATALOG_PATH.is_file()
        else source_root / "skills/repo-shape/references/operating-standards-catalog.json"
    )
    manifest_path = (
        _MANIFEST_PATH
        if _MANIFEST_PATH.is_file()
        else source_root / "skills/repo-shape/references/repository-shape-manifest.json"
    )
    return operating_standards_catalog.load_catalog(catalog_path, manifest_path, source_root)


def _read_contract(path: Path, catalog) -> list[str]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        operating_standards_catalog.validate_composition(raw, catalog)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"operating-standards contract is invalid: {exc}"]
    return []


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def scaffold_contract(repo_root: Path, catalog, *, apply: bool) -> list[str]:
    """Create the explicit empty composition only on apply; never overwrite existing content."""

    target = repo_root / _CONTRACT_RELATIVE
    if not target.is_file():
        if not apply:
            return [f"missing: {_CONTRACT_RELATIVE.as_posix()}"]
        raw = json.loads(_TEMPLATE_PATH.read_text(encoding="utf-8"))
        operating_standards_catalog.validate_composition(raw, catalog)
        _atomic_write(target, (json.dumps(raw, indent=2) + "\n").encode("utf-8"))
        return []
    return _read_contract(target, catalog)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scaffold or validate operating standards. (mixed)")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="validate without writing")
    modes.add_argument("--apply", action="store_true", help="create a missing explicit empty composition")
    args = parser.parse_args(argv)
    root = _repo_root()
    try:
        catalog = _load_catalog(root)
        findings = scaffold_contract(root, catalog, apply=args.apply)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        findings = [str(exc)]
    if findings:
        for finding in findings:
            print(f"DRIFT: {finding}")
        return 1
    print("OK operating-standards composition")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
