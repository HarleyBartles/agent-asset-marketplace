#!/usr/bin/env python3
"""Deploy pinned selected standard resources and their generic local runner."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from urllib.parse import urlsplit, urlunsplit
from pathlib import Path
from typing import Any

import migrate_operating_standards
import operating_standards_catalog
import operating_standards_dispatch
import shared_checkout

RUNTIME_RESOURCES = (
    "skills/repo-shape/scripts/repo_standards.py",
    "skills/repo-shape/scripts/operating_standards_dispatch.py",
    "skills/repo-shape/scripts/operating_standards_catalog.py",
    "skills/repo-shape/scripts/surface_contracts.py",
    "skills/repo-shape/scripts/document_contracts.py",
    "skills/repo-shape/scripts/plugin_contracts.py",
    "skills/repo-shape/scripts/skill_link_contract.py",
    "skills/repo-shape/scripts/shared_checkout.py",
    "skills/repo-shape/scripts/_agents_md.py",
    "skills/repo-shape/scripts/completed_artifact_contract.py",
)
RUNTIME_REFERENCES = (
    "skills/repo-shape/references/repository-shape-manifest.json",
    "skills/repo-shape/references/repository-shape-manifest.schema.json",
    "skills/repo-shape/references/operating-standards-catalog.json",
    "skills/repo-shape/references/operating-standards-catalog.schema.json",
)
PROVENANCE = Path(".agents/standards/provenance.json")


def _source_revision(source_root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(source_root), "rev-parse", "--verify", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    revision = result.stdout.strip()
    if not operating_standards_catalog._REVISION.fullmatch(revision):
        raise ValueError("marketplace-source did not resolve to a pinned commit")
    return revision


def _source_repository(source_root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(source_root), "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return "local-pinned-source"
    value = result.stdout.strip()
    parsed = urlsplit(value)
    if parsed.scheme and parsed.hostname:
        return urlunsplit((parsed.scheme, parsed.hostname, parsed.path, "", ""))
    if "@" in value and ":" in value:
        return value.split("@", 1)[-1]
    return "local-pinned-source"


def _load_composition(repo_root: Path, catalog, revision: str, *, prepare_migration: bool) -> dict[str, Any]:
    contract_path = repo_root / ".agents/contracts/operating-standards.json"
    if contract_path.is_file():
        try:
            composition = json.loads(contract_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"operating-standards contract cannot be read: {exc}") from exc
    elif prepare_migration:
        composition = migrate_operating_standards.plan_migration(repo_root, catalog, revision)
    else:
        raise ValueError("operating-standards.json is missing; use --prepare-migration for a legacy consumer")
    operating_standards_catalog.validate_composition(composition, catalog)
    return composition


def _runtime_destination(resource: str) -> str:
    return f".agents/standards/_runtime/{Path(resource).name}"


def _standard_for_entry(entry: dict[str, Any], source_root: Path):
    refs = source_root / "skills/repo-shape/references"
    catalog = operating_standards_catalog.load_catalog(
        refs / "operating-standards-catalog.json",
        refs / "repository-shape-manifest.json",
        source_root,
        validate_resources=False,
    )
    standard = next((row for row in catalog.standards if row.id == entry["id"]), None)
    if standard is None:
        raise ValueError(f"unknown marketplace standard: {entry['id']}")
    return standard


def _resource_specs(
    source_root: Path, composition: dict[str, Any]
) -> tuple[dict[str, dict[str, str]], dict[str, bytes]]:
    specs: dict[str, dict[str, str]] = {}
    contents: dict[str, bytes] = {}

    def add(resource: str, destination: str, standard_id: str) -> None:
        normalized = resource.replace("\\", "/")
        relative = Path(normalized)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"resource path escapes marketplace source: {resource}")
        source = (source_root / relative).resolve()
        try:
            source.relative_to(source_root.resolve())
        except ValueError as exc:
            raise ValueError(f"resource path escapes marketplace source: {resource}") from exc
        if not source.is_file():
            raise ValueError(f"pinned marketplace resource is missing: {resource}")
        committed = subprocess.run(
            ["git", "-C", str(source_root), "show", f"HEAD:{normalized}"],
            check=True,
            capture_output=True,
        ).stdout
        if source.read_bytes() != committed:
            raise ValueError(f"pinned marketplace resource has uncommitted changes: {normalized}")
        record = {
            "source": normalized,
            "sha256": hashlib.sha256(committed).hexdigest(),
            "standard_id": standard_id,
        }
        if destination in specs and (specs[destination] != record or contents[destination] != committed):
            raise ValueError(f"conflicting selected resource destination: {destination}")
        specs[destination] = record
        contents[destination] = committed

    marketplace_entries = [entry for entry in composition["standards"] if entry["origin"] == "marketplace"]
    if marketplace_entries:
        for resource in RUNTIME_RESOURCES:
            add(resource, _runtime_destination(resource), "_runtime")
        for resource in RUNTIME_REFERENCES:
            add(resource, f".agents/standards/references/{Path(resource).name}", "_runtime")

    for entry in marketplace_entries:
        standard = _standard_for_entry(entry, source_root)
        implementation_root = Path(entry["implementation_root"])
        for resource in standard.resources:
            resource_path = operating_standards_dispatch.resource_destination(
                source_root / implementation_root, resource
            )
            add(resource, resource_path.relative_to(source_root).as_posix(), standard.id)
    return specs, contents


def _read_provenance(path: Path) -> dict[str, Any]:
    if path.is_symlink():
        raise ValueError("standards deployment provenance cannot be a symlink")
    if not path.is_file():
        return {"version": 1, "repository": "", "revision": "", "resources": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"standards deployment provenance cannot be read: {exc}") from exc
    if (
        not isinstance(data, dict)
        or set(data) != {"version", "repository", "revision", "resources"}
        or data.get("version") != 1
        or not isinstance(data.get("repository"), str)
        or not isinstance(data.get("revision"), str)
        or not isinstance(data.get("resources"), dict)
    ):
        raise ValueError("standards deployment provenance has an invalid shape")
    for destination, record in data["resources"].items():
        if (
            not isinstance(destination, str)
            or not isinstance(record, dict)
            or set(record) != {"source", "sha256", "standard_id"}
            or not all(isinstance(record[key], str) for key in record)
            or len(record["sha256"]) != 64
            or any(character not in "0123456789abcdef" for character in record["sha256"])
            or Path(destination).is_absolute()
            or ".." in Path(destination).parts
        ):
            raise ValueError("standards deployment provenance contains an invalid resource record")
    return data


def _safe_destination(repo_root: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"deployment destination must remain inside repository: {relative}")
    destination = repo_root / path
    current = repo_root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"deployment path contains a symlink: {relative}")
    try:
        destination.resolve().relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(f"deployment destination escapes repository: {relative}") from exc
    return destination


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def deploy(
    repo_root: Path,
    source_root: Path,
    catalog,
    *,
    apply: bool,
    prepare_migration: bool = False,
) -> list[str]:
    revision = _source_revision(source_root)
    composition = _load_composition(repo_root, catalog, revision, prepare_migration=prepare_migration)
    for entry in composition["standards"]:
        if entry["origin"] != "marketplace":
            continue
        if entry["revision"] != revision:
            raise ValueError(
                f"standard {entry['id']} revision {entry['revision']} does not match pinned source revision {revision}"
            )
        standard = _standard_for_entry(entry, source_root)
        expected_check = [
            "@python",
            ".agents/standards/_runtime/repo_standards.py",
            "--run-standard",
            entry["id"],
            "--check",
        ]
        expected_apply = (
            [
                "@python",
                ".agents/standards/_runtime/repo_standards.py",
                "--run-standard",
                entry["id"],
                "--apply",
                "--yes",
                "@allow-shared-checkout",
            ]
            if standard.apply
            else []
        )
        if entry["check"] != expected_check or entry["apply"] != expected_apply:
            raise ValueError(f"standard {entry['id']} command vectors do not match the pinned generic runtime")

    desired, contents = _resource_specs(source_root, composition)
    provenance_path = repo_root / PROVENANCE
    previous = _read_provenance(provenance_path)
    previous_resources = previous["resources"]
    if not desired and not previous_resources:
        if provenance_path.is_file():
            if apply:
                provenance_path.unlink()
                return []
            return [f"empty standards selection has unnecessary deployment provenance: {PROVENANCE.as_posix()}"]
        return []
    findings: list[str] = []
    for relative, record in desired.items():
        destination = _safe_destination(repo_root, relative)
        if not destination.exists():
            findings.append(f"missing deployed resource: {relative}")
            continue
        actual = hashlib.sha256(destination.read_bytes()).hexdigest()
        if actual == record["sha256"]:
            continue
        prior = previous_resources.get(relative)
        if prior is None or prior["sha256"] != actual:
            raise ValueError(f"ambiguous existing file has no matching deployment ownership: {relative}")
        findings.append(f"drifted deployed resource: {relative}")

    for relative, prior in previous_resources.items():
        if relative in desired:
            continue
        destination = _safe_destination(repo_root, relative)
        if destination.exists():
            actual = hashlib.sha256(destination.read_bytes()).hexdigest()
            if prior["sha256"] != actual:
                raise ValueError(f"stale deployed resource was modified outside its owner: {relative}")
            findings.append(f"stale deployed resource: {relative}")

    expected_provenance = {
        "version": 1,
        "repository": _source_repository(source_root),
        "revision": revision,
        "resources": desired,
    }
    try:
        current_provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        current_provenance = None
    if current_provenance != expected_provenance:
        findings.append(f"deployment provenance drift: {PROVENANCE.as_posix()}")

    if not apply:
        return findings
    for relative, record in desired.items():
        destination = _safe_destination(repo_root, relative)
        _atomic_write(destination, contents[relative])
    for relative in previous_resources.keys() - desired.keys():
        destination = _safe_destination(repo_root, relative)
        if destination.exists():
            destination.unlink()
    if desired:
        _atomic_write(provenance_path, (json.dumps(expected_provenance, indent=2) + "\n").encode("utf-8"))
    else:
        provenance_path.unlink(missing_ok=True)
    return []


def _repo_root() -> Path:
    env = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(name, None)
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], check=True, capture_output=True, text=True, env=env
    )
    return Path(result.stdout.strip())


def _resolve_marketplace_source(repo_root: Path) -> Path:
    """Resolve the upgraded Codex marketplace snapshot without requiring a consumer submodule."""
    submodule = repo_root / ".agents/plugins/marketplace-source"
    if (submodule / ".git").exists():
        return submodule
    declaration = repo_root / ".agents/plugins/marketplace.json"
    marketplace_name = ""
    source_urls: set[str] = set()
    if declaration.is_file():
        try:
            manifest = json.loads(declaration.read_text(encoding="utf-8"))
            marketplace_name = manifest.get("name", "")
            source_urls = {
                url
                for plugin in manifest.get("plugins", [])
                if isinstance(plugin, dict)
                and isinstance(plugin.get("source"), dict)
                and isinstance((url := plugin["source"].get("url")), str)
                and url
            }
        except (OSError, json.JSONDecodeError):
            pass
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    snapshots = codex_home / ".tmp/marketplaces"
    if marketplace_name and snapshots.is_dir():
        for candidate in snapshots.iterdir():
            if not candidate.is_dir():
                continue
            config = candidate / ".agents/plugins/marketplace.json"
            if not config.is_file():
                continue
            try:
                name = json.loads(config.read_text(encoding="utf-8")).get("name")
            except (OSError, json.JSONDecodeError):
                continue
            try:
                remote = _source_repository(candidate)
            except (OSError, subprocess.CalledProcessError):
                remote = ""

            def normalize(value: str) -> str:
                return value.lower().removesuffix(".git").rstrip("/")

            if name == marketplace_name or normalize(remote) in {normalize(url) for url in source_urls}:
                try:
                    _source_revision(candidate)
                    return candidate
                except (OSError, ValueError, subprocess.CalledProcessError):
                    continue
    raise ValueError(
        "Marketplace source unavailable: add the marketplace in Codex and upgrade it, "
        "or initialize .agents/plugins/marketplace-source for development"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Deploy selected pinned operating standards. (mixed)")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="report deployment drift without writing")
    modes.add_argument("--apply", action="store_true", help="deploy selected files")
    parser.add_argument("--prepare-migration", action="store_true", help="select from the legacy exception contract")
    parser.add_argument("--yes", action="store_true", help="confirm deployment writes")
    parser.add_argument("--allow-shared-checkout", action="store_true")
    args = parser.parse_args(argv)
    if args.apply and not args.yes:
        print("ERROR: --apply requires --yes")
        return 1
    try:
        root = _repo_root()
        source = _resolve_marketplace_source(root)
        skill = source / "skills/repo-shape"
        catalog = operating_standards_catalog.load_catalog(
            skill / "references/operating-standards-catalog.json",
            skill / "references/repository-shape-manifest.json",
            source,
        )
        if args.apply and not shared_checkout.approve_mutation(
            root, "deploy-operating-standards", args.allow_shared_checkout
        ):
            return 1
        findings = deploy(root, source, catalog, apply=args.apply, prepare_migration=args.prepare_migration)
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}")
        return 1
    for finding in findings:
        print(f"DRIFT: {finding}")
    if findings:
        return 1
    print("OK operating standards deployment")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
