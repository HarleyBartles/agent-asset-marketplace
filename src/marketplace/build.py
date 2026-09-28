"""Deterministically assemble self-contained Codex marketplace plugins."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from marketplace.definitions import DefinitionError, load_marketplace


class BuildError(RuntimeError):
    """The expected package tree differs from the committed build output."""


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def _copy_source(
    source: Path, destination: Path, source_root: Path, *, excluded_directories: frozenset[str] = frozenset()
) -> None:
    resolved_root = source_root.resolve()
    paths = [source] if source.is_file() else sorted(source.rglob("*"))
    for path in paths:
        relative = Path() if source.is_file() else path.relative_to(source)
        if any(part in excluded_directories for part in relative.parts):
            continue
        resolved = path.resolve()
        try:
            resolved.relative_to(resolved_root)
        except ValueError as exc:
            raise DefinitionError(f"source symlink escapes {source_root.name} root: {path}") from exc
        target = destination if source.is_file() else destination / relative
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)


def _expected_plugins(root: Path, staging: Path) -> None:
    marketplace = load_marketplace(root)
    definitions = root / "plugin-definitions"
    skills_root = root / "skills"
    shared_root = root / "shared"
    for name, plugin in marketplace.plugins.items():
        package = staging / name
        files = definitions / name / "files"
        if files.exists():
            _copy_source(files, package, definitions / name)
        _write_json(package / ".codex-plugin/plugin.json", plugin.manifest)
        if plugin.bundle is not None:
            entries = []
            for skill in plugin.skills:
                entries.append(
                    {
                        "canonical_name": skill.name,
                        **skill.provenance,
                        "canonical_source_path": f"skills/{skill.source_id}",
                        "local_path": f"skills/{skill.name}",
                        "source_path": f"skills/{skill.source_id}/SKILL.md",
                    }
                )
            _write_json(package / "references/bundle-manifest.json", {**plugin.bundle, "entries": entries})
        for skill in plugin.skills:
            skill_target = package / "skills" / skill.name
            _copy_source(
                skill.source,
                skill_target,
                skills_root,
                excluded_directories=frozenset({"__pycache__", ".pytest_cache", "runs", "evaluator-only"}),
            )
            provenance = [f"Canonical source: `{skill.source_id}`", ""]
            for key, label in (
                ("source_license", "License"),
                ("source_author", "Attribution"),
                ("source_repo", "Source repository"),
                ("provenance_note", "Provenance"),
            ):
                if value := skill.provenance.get(key):
                    provenance.append(f"- {label}: {value}")
            provenance_path = skill_target / "PROVENANCE.md"
            if provenance_path.exists():
                raise DefinitionError(f"plugin {name} skill {skill.name}: PROVENANCE.md collides with authored source")
            provenance_path.write_text("\n".join(provenance) + "\n", encoding="utf-8", newline="\n")
            for resource in skill.resources:
                target = skill_target / resource.destination
                if target.exists():
                    raise DefinitionError(
                        f"plugin {name} skill {skill.name}: destination collision at {resource.destination}"
                    )
                _copy_source(resource.source, target, shared_root)


def _package_files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for package in sorted(root.iterdir())
        if package.is_dir()
        for path in sorted(package.rglob("*"))
        if path.is_file() and path.name != "INDEX.md"
    }


def build_marketplace(root: Path, *, apply: bool) -> bool:
    """Build plugin packages; check mode compares output without changing it."""
    root = root.resolve()
    output = root / "codex-marketplace/plugins"
    with tempfile.TemporaryDirectory(prefix="marketplace-build-") as temporary:
        staging = Path(temporary) / "plugins"
        staging.mkdir()
        _expected_plugins(root, staging)
        expected = _package_files(staging)
        actual = _package_files(output) if output.exists() else {}
        if not apply:
            if expected != actual:
                missing = sorted(expected.keys() - actual.keys())
                unexpected = sorted(actual.keys() - expected.keys())
                changed = sorted(key for key in expected.keys() & actual.keys() if expected[key] != actual[key])
                raise BuildError(
                    f"marketplace plugin output is stale; missing={missing}, unexpected={unexpected}, changed={changed}"
                )
            return True
        replacement = output.parent / ".plugins-build"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.mkdir(parents=True, exist_ok=True)
        if replacement.exists():
            shutil.rmtree(replacement)
        shutil.copytree(staging, replacement)
        if output.exists():
            for child in output.iterdir():
                if child.is_dir():
                    shutil.rmtree(child)
        for child in replacement.iterdir():
            child.replace(output / child.name)
        replacement.rmdir()
        return True
