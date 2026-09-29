#!/usr/bin/env python3
"""Preview or apply migration from legacy surface exceptions to selected standards."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

import operating_standards_catalog
import plugin_contracts

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
TARGET = Path(".agents/contracts/operating-standards.json")


def _root() -> Path:
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(key, None)
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    return Path(result.stdout.strip())


def _source_root(root: Path) -> Path:
    pinned = root / ".agents/plugins/marketplace-source"
    if (pinned / "skills/repo-shape").is_dir():
        return pinned
    if (root / "skills/repo-shape").is_dir():
        return root
    raise ValueError("pinned marketplace-source with Agent Operating Model resources is unavailable")


def _load_catalog(root: Path):
    source = _source_root(root)
    skill = source / "skills/repo-shape"
    return operating_standards_catalog.load_catalog(
        skill / "references/operating-standards-catalog.json",
        skill / "references/repository-shape-manifest.json",
        source,
    )


def plan_migration(repo_root: Path, catalog, revision: str) -> dict:
    if not operating_standards_catalog._REVISION.fullmatch(revision):
        raise ValueError("marketplace revision must be a pinned commit")
    manifest_path = SKILL_ROOT / "references/repository-shape-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    surfaces = {item["id"]: item for item in manifest["surfaces"]}
    known = set(surfaces)
    exceptions = plugin_contracts.load_legacy_surface_exceptions(repo_root, known)
    enabled = known - exceptions

    entries = []
    adopted: set[str] = set()
    for standard in catalog.standards:
        if standard.legacy_migration == "explicit":
            continue
        count = sum(surface in enabled for surface in standard.surfaces)
        if count not in (0, len(standard.surfaces)):
            raise ValueError(f"partially enabled legacy standard: {standard.id}")
        if count:
            adopted.add(standard.id)

    # Legacy required_with constraints cannot be represented by an incomplete selection.
    for surface_id, surface in surfaces.items():
        partner = surface.get("required_with")
        if partner and ((surface_id in enabled) != (partner in enabled)):
            raise ValueError(f"broken legacy required_with relationship: {surface_id} requires {partner}")

    for standard in catalog.standards:
        if standard.legacy_migration == "explicit" or standard.id not in adopted:
            continue
        missing = set(standard.requires) - adopted
        if missing:
            raise ValueError(
                f"legacy standard {standard.id} requires disabled standard(s): {', '.join(sorted(missing))}"
            )
        paths = [
            surfaces[item]["path"]
            for item in standard.surfaces
            if surfaces[item].get("ownership") == "consumer-generated"
        ]
        entry = {
            "id": standard.id,
            "origin": "marketplace",
            "revision": revision,
            "implementation_root": f".agents/standards/{standard.id}",
            "check": [
                "@python",
                ".agents/standards/_runtime/repo_standards.py",
                "--run-standard",
                standard.id,
                "--check",
            ],
            "apply": (
                [
                    "@python",
                    ".agents/standards/_runtime/repo_standards.py",
                    "--run-standard",
                    standard.id,
                    "--apply",
                    "--yes",
                    "@allow-shared-checkout",
                ]
                if standard.apply
                else []
            ),
            "generated_paths": paths,
            "requires": list(standard.requires),
        }
        entries.append(entry)
    result = {"version": 1, "standards": entries}
    operating_standards_catalog.validate_composition(result, catalog)
    return result


def _require_deployed_implementations(repo_root: Path, composition: dict) -> None:
    for entry in composition["standards"]:
        root = (repo_root / entry["implementation_root"]).resolve()
        try:
            root.relative_to(repo_root.resolve())
        except ValueError as exc:
            raise ValueError(f"implementation root escapes repository: {entry['implementation_root']}") from exc
        if not root.is_dir():
            raise ValueError(
                f"cannot activate migration before deploying standard {entry['id']}: {entry['implementation_root']}"
            )
        for capability in ("check", "apply"):
            vector = entry[capability]
            if not vector:
                continue
            for argument in vector[1:]:
                if not argument.endswith(".py") or argument.startswith("-"):
                    continue
                command_path = (repo_root / argument).resolve()
                try:
                    command_path.relative_to(repo_root.resolve())
                except ValueError as exc:
                    raise ValueError(f"standard command escapes repository: {argument}") from exc
                if not command_path.is_file():
                    raise ValueError(
                        f"cannot activate migration before deploying standard {entry['id']} runtime: {argument}"
                    )


def migrate_contract(repo_root: Path, catalog, revision: str, *, apply: bool) -> dict:
    result = plan_migration(repo_root, catalog, revision)
    if apply:
        _require_deployed_implementations(repo_root, result)
    target = repo_root / TARGET
    if target.exists():
        existing = json.loads(target.read_text(encoding="utf-8"))
        operating_standards_catalog.validate_composition(existing, catalog)
        raise ValueError(f"target contract already exists and will not be overwritten: {TARGET.as_posix()}")
    if apply:
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(f".{target.name}.tmp")
        try:
            temporary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
            os.replace(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Preview or apply explicit operating standards migration. (mixed)")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="preview without writing (default)")
    modes.add_argument("--apply", action="store_true", help="write the new contract")
    parser.add_argument("--revision", help="pinned marketplace source commit; defaults to the submodule HEAD")
    args = parser.parse_args(argv)
    try:
        root = _root()
        revision = (
            args.revision
            or subprocess.run(
                ["git", "-C", str(root / ".agents/plugins/marketplace-source"), "rev-parse", "--verify", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
        contract = migrate_contract(root, _load_catalog(root), revision, apply=args.apply)
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(contract, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
