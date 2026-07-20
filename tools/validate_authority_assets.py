#!/usr/bin/env python3
"""Validate recorded local authority evidence without performing network checks."""

from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
LANES = {"skills-with-source", "skills-with-citation"}
CONTENT_MODES = {"first_party_synthesis", "licensed_adaptation", "verbatim_source"}
REQUIRED_AUTHORITY_FIELDS = {
    "title",
    "canonical_url",
    "pinned_source_url",
    "latest_check_url",
    "revision",
    "retrieved_at",
    "content_sha256",
    "license",
    "license_url",
}
URL_FIELDS = {"canonical_url", "pinned_source_url", "latest_check_url", "license_url"}
REQUIRED_REFERENCE_FIELDS = {"path", "source_sections", "content_mode", "load_when"}
SOURCE_MAP_FIELDS = {"schema_version", "reconciled_against", "references"}


def discover_authority_assets(root: Path) -> list[Path]:
    roots = [root / "sources/first_party/skills", root / ".agents/skills"]
    return sorted(
        authority.parent.parent.parent
        for skills_root in roots if skills_root.is_dir()
        for authority in skills_root.glob("*/assets/authority/authority.yaml")
    )


def _load_mapping(path: Path, errors: list[str]) -> dict[object, object] | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        errors.append(f"{path.name} cannot be read as YAML: {error}")
        return None
    if not isinstance(data, dict):
        errors.append(f"{path.name} must contain a YAML mapping")
        return None
    return data


def _is_nonblank_http_url(value: object) -> bool:
    return isinstance(value, str) and value.strip().startswith(("http://", "https://"))


def _contains_non_hidden_file(directory: Path) -> bool:
    return any(
        path.is_file() and not any(part.startswith(".") for part in path.relative_to(directory).parts)
        for path in directory.rglob("*")
    )


def _validate_references(
    references: object, *, record_name: str, lane: object, errors: list[str]
) -> list[object] | None:
    if not isinstance(references, list):
        errors.append(f"{record_name} references must be a list")
        return None
    for index, reference in enumerate(references, start=1):
        if not isinstance(reference, dict):
            errors.append(f"{record_name} references[{index}] must be a mapping")
            continue
        for field in sorted(REQUIRED_REFERENCE_FIELDS):
            if field not in reference:
                errors.append(f"{record_name} references[{index}] is missing {field}")
        if "content_mode" in reference and reference["content_mode"] not in CONTENT_MODES:
            errors.append(
                f"{record_name} references[{index}] has unsupported content_mode "
                f"{reference['content_mode']!r}"
            )
        if lane == "skills-with-citation" and reference.get("content_mode") != "first_party_synthesis":
            errors.append(
                f"{record_name} references[{index}] must use first_party_synthesis "
                "for skills-with-citation"
            )
    return references


def validate_authority_skill(skill_root: Path) -> list[str]:
    authority_root = skill_root / "assets/authority"
    authority_path = authority_root / "authority.yaml"
    source_map_path = authority_root / "source-map.yaml"
    citations_path = authority_root / "CITATIONS.md"
    errors: list[str] = []

    for path in (authority_path, source_map_path, citations_path):
        if not path.is_file():
            errors.append(f"missing {path.name}")

    if not authority_path.is_file():
        return errors

    record = _load_mapping(authority_path, errors)
    if record is None:
        return errors

    source_map = _load_mapping(source_map_path, errors) if source_map_path.is_file() else None

    if record.get("schema_version") != 1:
        errors.append("authority.yaml must declare schema_version: 1")

    lane = record.get("lane")
    if lane not in LANES:
        errors.append(f"authority.yaml lane must be one of {sorted(LANES)}")

    authority = record.get("authority")
    if not isinstance(authority, dict):
        errors.append("authority.yaml authority must be a mapping")
    else:
        for field in sorted(REQUIRED_AUTHORITY_FIELDS):
            if field not in authority:
                errors.append(f"authority.yaml authority is missing {field}")
            elif field in URL_FIELDS and not _is_nonblank_http_url(authority[field]):
                errors.append(f"authority.yaml authority {field} must be a nonblank http:// or https:// URL")

    decomposition = record.get("decomposition")
    authority_reconciled_against: object | None = None
    authority_references: list[object] | None = None
    if not isinstance(decomposition, dict):
        errors.append("authority.yaml decomposition must be a mapping")
    else:
        if "reconciled_against" not in decomposition:
            errors.append("authority.yaml decomposition is missing reconciled_against")
        else:
            authority_reconciled_against = decomposition["reconciled_against"]
        authority_references = _validate_references(
            decomposition.get("references"),
            record_name="authority.yaml decomposition",
            lane=lane,
            errors=errors,
        )

    source_map_reconciled_against: object | None = None
    source_map_references: list[object] | None = None
    if source_map is not None:
        if source_map.get("schema_version") != 1:
            errors.append("source-map.yaml must declare schema_version: 1")
        for field in sorted(set(source_map) - SOURCE_MAP_FIELDS):
            errors.append(f"source-map.yaml has unsupported top-level field {field}")
        if "reconciled_against" not in source_map:
            errors.append("source-map.yaml is missing reconciled_against")
        else:
            source_map_reconciled_against = source_map["reconciled_against"]
        source_map_references = _validate_references(
            source_map.get("references"),
            record_name="source-map.yaml",
            lane=lane,
            errors=errors,
        )

    if authority_reconciled_against is not None and source_map_reconciled_against is not None:
        if authority_reconciled_against != source_map_reconciled_against:
            errors.append("source-map.yaml reconciled_against must match authority.yaml decomposition.reconciled_against")
    if authority_references is not None and source_map_references is not None:
        if authority_references != source_map_references:
            errors.append("source-map.yaml references must match authority.yaml decomposition.references")

    reference_source = authority_root / "reference-source"
    if lane == "skills-with-source":
        if not reference_source.is_dir() or not _contains_non_hidden_file(reference_source):
            errors.append("skills-with-source reference-source must contain at least one non-hidden file")
    if lane == "skills-with-citation" and reference_source.is_dir() and any(reference_source.iterdir()):
        errors.append("skills-with-citation reference-source must not contain vendored source files")

    return errors


def validate_authority_assets(root: Path) -> int:
    has_errors = False
    for skill_root in discover_authority_assets(root):
        errors = validate_authority_skill(skill_root)
        if errors:
            has_errors = True
            print(f"{skill_root}: {'; '.join(errors)}")
    return int(has_errors)


if __name__ == "__main__":
    raise SystemExit(validate_authority_assets(ROOT))
