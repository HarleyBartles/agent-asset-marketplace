"""Load and validate source-first marketplace definitions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any


class DefinitionError(ValueError):
    """A marketplace definition is invalid or points outside its source roots."""


AGENT_PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
OPENAI_EXTENSION = "com.openai"
LEGACY_MANIFEST_FIELDS = frozenset({"skills", "mcpServers", "interface"})


@dataclass(frozen=True)
class Resource:
    name: str
    source: Path


@dataclass(frozen=True)
class SkillResource:
    name: str
    source: Path
    destination: Path


@dataclass(frozen=True)
class Skill:
    name: str
    source_id: str
    source: Path
    resources: tuple[SkillResource, ...]
    provenance: dict[str, Any]


@dataclass(frozen=True)
class Plugin:
    name: str
    manifest: dict[str, Any]
    bundle: dict[str, Any] | None
    skills: tuple[Skill, ...]


@dataclass(frozen=True)
class Marketplace:
    plugins: dict[str, Plugin]


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DefinitionError(f"{path}: cannot read JSON: {exc}") from exc


def _safe_source(root: Path, relative: str, label: str) -> Path:
    candidate = Path(relative)
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise DefinitionError(f"{label} escapes {root.name} root: {relative}") from exc
    if not resolved.exists():
        raise DefinitionError(f"{label} does not exist: {relative}")
    return resolved


def _destination(relative: str, plugin_name: str, skill_name: str) -> Path:
    destination = PurePosixPath(relative)
    if destination.is_absolute() or not destination.parts or any(part in {".", ".."} for part in destination.parts):
        raise DefinitionError(
            f"plugin {plugin_name} skill {skill_name}: invalid skill-relative destination {relative!r}"
        )
    return Path(*destination.parts)


def load_marketplace(root: Path) -> Marketplace:
    """Load all product definitions and reject unsafe or unresolved composition."""
    root = root.resolve()
    skills_root = (root / "skills").resolve()
    shared_root = (root / "shared").resolve()
    plugin_root = root / "src/plugin-definitions"
    if not skills_root.is_dir() or not shared_root.is_dir() or not plugin_root.is_dir():
        raise DefinitionError("repository must contain skills/, shared/, and src/plugin-definitions/ roots")

    skills = {path.name: path.resolve() for path in skills_root.iterdir() if path.is_dir()}
    resources_data = _read_json(root / "resources.json")
    if not isinstance(resources_data, dict):
        raise DefinitionError("resources.json must map resource names to shared-root paths")
    resources = {
        name: Resource(name, _safe_source(shared_root, path, f"resource {name}"))
        for name, path in resources_data.items()
        if isinstance(name, str) and isinstance(path, str)
    }
    if len(resources) != len(resources_data):
        raise DefinitionError("resources.json entries require string names and paths")

    plugins: dict[str, Plugin] = {}
    for directory in sorted(path for path in plugin_root.iterdir() if path.is_dir()):
        manifest = _read_json(directory / "plugin.json")
        if not isinstance(manifest, dict) or not isinstance(manifest.get("name"), str) or not manifest["name"].strip():
            raise DefinitionError(f"{directory / 'plugin.json'}: name must be a non-empty string")
        if manifest.get("$schema") != AGENT_PLUGIN_SCHEMA:
            raise DefinitionError(f"{directory / 'plugin.json'}: Agent Plugins schema is required")
        if LEGACY_MANIFEST_FIELDS.intersection(manifest):
            raise DefinitionError(
                f"{directory / 'plugin.json'}: OpenAI-specific fields belong under extensions.{OPENAI_EXTENSION}"
            )
        extensions = manifest.get("extensions", {})
        if not isinstance(extensions, dict) or any(not isinstance(value, dict) for value in extensions.values()):
            raise DefinitionError(f"{directory / 'plugin.json'}: extensions must map namespaces to objects")
        name = manifest["name"]
        if name in plugins:
            raise DefinitionError(f"duplicate plugin name: {name}")
        contents = _read_json(directory / "contents.json")
        if not isinstance(contents, dict) or not isinstance(contents.get("skills"), list):
            raise DefinitionError(f"{directory / 'contents.json'}: skills must be a list")
        bundle_path = directory / "bundle.json"
        bundle = _read_json(bundle_path) if bundle_path.is_file() else None
        if bundle is not None and (not isinstance(bundle, dict) or "entries" in bundle):
            raise DefinitionError(f"{bundle_path}: bundle metadata must be an object without entries")
        if contents.get("enabled") is False:
            continue
        included: list[Skill] = []
        destinations: set[Path] = set()
        for item in contents["skills"]:
            if not isinstance(item, dict) or not isinstance(item.get("name"), str):
                raise DefinitionError(f"plugin {name}: each skill requires a name")
            skill_name = item["name"]
            source_id = item.get("source", skill_name)
            if source_id not in skills:
                raise DefinitionError(f"plugin {name}: unknown skill {skill_name!r}; it must be a declared skill")
            if skill_name in {skill.name for skill in included}:
                raise DefinitionError(f"plugin {name}: duplicate skill {skill_name!r}")
            skill_source = _safe_source(skills_root, source_id, f"skill {source_id}")
            destinations.add(Path("SKILL.md"))
            skill_resources: list[SkillResource] = []
            for reference in item.get("resources", []):
                if not isinstance(reference, dict) or not isinstance(reference.get("source"), str):
                    raise DefinitionError(f"plugin {name} skill {skill_name}: resource requires a source name")
                source_name = reference["source"]
                if source_name not in resources:
                    raise DefinitionError(f"plugin {name} skill {skill_name}: unknown resource {source_name!r}")
                target = _destination(reference.get("destination", ""), name, skill_name)
                if target in destinations:
                    raise DefinitionError(f"plugin {name} skill {skill_name}: destination collision at {target}")
                destinations.add(target)
                skill_resources.append(SkillResource(source_name, resources[source_name].source, target))
            provenance = item.get("provenance", {})
            if not isinstance(provenance, dict):
                raise DefinitionError(f"plugin {name} skill {skill_name}: provenance must be an object")
            included.append(Skill(skill_name, source_id, skill_source, tuple(skill_resources), provenance))
        plugins[name] = Plugin(name, manifest, bundle, tuple(included))
    return Marketplace(plugins)
