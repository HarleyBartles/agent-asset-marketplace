#!/usr/bin/env python3
"""Validate recorded local authority evidence without performing network checks."""

from __future__ import annotations

from datetime import date
from pathlib import Path
import hashlib
import re

import yaml


ROOT = Path(__file__).resolve().parent.parent
LANES = {"skills-with-source", "skills-with-citation", "skills-with-mixed-source"}
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
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
SAFE_LABEL_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
CITATION_SECTIONS = (
    "Scholarly citation",
    "Derivation boundary",
    "Attribution",
    "Human review",
)


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys at every level."""


def _construct_unique_mapping(loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[object, object]:
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise yaml.YAMLError(f"mapping key {key!r} must be a string")
        if key in mapping:
            raise yaml.YAMLError(f"duplicate key {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def discover_authority_assets(root: Path) -> list[Path]:
    roots = [root / ".agents/skills", root / "codex-marketplace" / "plugins"]
    found: set[Path] = set()
    for skills_root in roots:
        if not skills_root.is_dir():
            continue
        for authority in skills_root.glob("*/assets/authority"):
            if authority.is_dir():
                found.add(authority.parent.parent)
        for authority in skills_root.glob("*/skills/*/assets/authority"):
            if authority.is_dir():
                found.add(authority.parent.parent)
    return sorted(found)


def _load_mapping(path: Path, errors: list[str]) -> dict[object, object] | None:
    try:
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader)
    except (OSError, TypeError, UnicodeDecodeError, yaml.YAMLError) as error:
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


def _nonblank_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_safe_label(value: object) -> bool:
    return _nonblank_string(value) and SAFE_LABEL_PATTERN.fullmatch(value) is not None


def _validate_string_list(value: object, *, field: str, errors: list[str]) -> bool:
    if not isinstance(value, list) or not value or not all(_nonblank_string(item) for item in value):
        errors.append(f"{field} must be a nonempty list of nonblank strings")
        return False
    return True


def _validate_reference_path(value: object, *, skill_root: Path, field: str, errors: list[str]) -> None:
    if not _nonblank_string(value):
        errors.append(f"{field} must name an existing file under references/")
        return
    relative_path = Path(value)
    references_root = skill_root / "references"
    candidate = skill_root / relative_path
    if (
        relative_path.is_absolute()
        or not relative_path.parts
        or relative_path.parts[0] != "references"
        or ".." in relative_path.parts
        or not candidate.is_file()
        or not candidate.resolve().is_relative_to(references_root.resolve())
    ):
        errors.append(f"{field} must name an existing file under references/")


def _validate_citations(path: Path, errors: list[str]) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        errors.append(f"CITATIONS.md cannot be read: {error}")
        return
    for section in CITATION_SECTIONS:
        heading = f"## {section}"
        match = re.search(rf"^{re.escape(heading)}\s*$", text, flags=re.MULTILINE)
        label = section.lower()
        if match is None:
            errors.append(f"CITATIONS.md is missing {label} section")
            continue
        following = text[match.end():]
        content = following.split("\n## ", maxsplit=1)[0].strip()
        if not content or re.search(r"\b(?:TODO|TBD)\b|^(?:Record|State)\b", content, flags=re.IGNORECASE | re.MULTILINE):
            errors.append(f"CITATIONS.md {label} section must contain non-placeholder content")


def _compute_file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_single_authority_record(
    record: object, field_prefix: str, errors: list[str]
) -> dict | None:
    if not isinstance(record, dict):
        errors.append(f"{field_prefix} must be a mapping")
        return None
    for field in sorted(REQUIRED_AUTHORITY_FIELDS):
        if field not in record:
            errors.append(f"{field_prefix} is missing {field}")
        elif not _nonblank_string(record[field]):
            errors.append(f"{field_prefix} {field} must be a nonblank string")
        elif field in URL_FIELDS and not _is_nonblank_http_url(record[field]):
            errors.append(f"{field_prefix} {field} must be a nonblank http:// or https:// URL")
    content_sha256 = record.get("content_sha256")
    if _nonblank_string(content_sha256) and not SHA256_PATTERN.fullmatch(content_sha256):
        errors.append(f"{field_prefix} content_sha256 must be a 64-character lowercase SHA-256")
    retrieved_at = record.get("retrieved_at")
    if _nonblank_string(retrieved_at):
        try:
            date.fromisoformat(retrieved_at)
        except ValueError:
            errors.append(f"{field_prefix} retrieved_at must be an ISO-8601 date")
    return record


def _validate_sha_against_evidence(
    skill_root: Path,
    record: dict,
    source_map: dict | None,
    citations_path: Path,
    errors: list[str],
) -> None:
    """Ensure recorded SHA values honestly represent a retained local file."""
    lane = record.get("lane")
    authority = record.get("authority")
    if not isinstance(authority, dict):
        return

    reference_source = skill_root / "assets/authority/reference-source"

    if lane == "skills-with-mixed-source":
        decomposition = record.get("decomposition")
        authority_reconciled = (
            decomposition.get("reconciled_against")
            if isinstance(decomposition, dict)
            else None
        )
        source_map_reconciled = (
            source_map.get("reconciled_against")
            if isinstance(source_map, dict)
            else None
        )
        for label, source_record in authority.items():
            if not isinstance(label, str):
                continue
            if not _is_safe_label(label):
                errors.append(
                    f"authority.yaml authority source label {label!r} must be a safe single directory name"
                )
                continue
            if not isinstance(source_record, dict):
                continue
            content_sha256 = source_record.get("content_sha256")
            if not isinstance(content_sha256, str):
                continue
            label_dir = reference_source / label
            expected_shas: set[str] = set()
            file_paths: list[Path] = []
            if label_dir.is_dir():
                for path in label_dir.rglob("*"):
                    if (
                        path.is_file()
                        and not any(part.startswith(".") for part in path.relative_to(label_dir).parts)
                    ):
                        file_paths.append(path)
                        expected_shas.add(_compute_file_sha256(path))
            evidence_desc = f"reference-source/{label}/*"
            if not expected_shas:
                errors.append(
                    f"authority.yaml authority[{label}] content_sha256 has no local evidence in {evidence_desc}"
                )
                continue
            if content_sha256 not in expected_shas:
                errors.append(
                    f"authority.yaml authority[{label}] content_sha256 does not match SHA-256 of {evidence_desc}"
                )
            for path in file_paths:
                file_hash = _compute_file_sha256(path)
                if file_hash != content_sha256:
                    rel = path.relative_to(label_dir)
                    errors.append(
                        f"reference-source/{label}/{rel} is not recorded in authority.yaml and does not match authority[{label}] content_sha256"
                    )
            auth_rec = authority_reconciled.get(label) if isinstance(authority_reconciled, dict) else None
            if isinstance(auth_rec, str) and auth_rec not in expected_shas:
                errors.append(
                    f"authority.yaml decomposition.reconciled_against[{label}] does not match SHA-256 of {evidence_desc}"
                )
            sm_rec = source_map_reconciled.get(label) if isinstance(source_map_reconciled, dict) else None
            if isinstance(sm_rec, str) and sm_rec not in expected_shas:
                errors.append(
                    f"source-map.yaml reconciled_against[{label}] does not match SHA-256 of {evidence_desc}"
                )
            if isinstance(auth_rec, str) and content_sha256 != auth_rec:
                errors.append(
                    f"authority.yaml authority[{label}] content_sha256 must match decomposition.reconciled_against[{label}]"
                )
        return

    content_sha256 = authority.get("content_sha256")
    if not isinstance(content_sha256, str):
        return

    decomposition = record.get("decomposition")
    authority_reconciled = decomposition.get("reconciled_against") if isinstance(decomposition, dict) else None
    source_map_reconciled = source_map.get("reconciled_against") if isinstance(source_map, dict) else None

    expected_shas: set[str] = set()
    evidence_desc = ""
    if lane == "skills-with-citation":
        if citations_path.is_file():
            expected_shas.add(_compute_file_sha256(citations_path))
            evidence_desc = "assets/authority/CITATIONS.md"
    elif lane == "skills-with-source":
        if reference_source.is_dir():
            for path in reference_source.rglob("*"):
                if (
                    path.is_file()
                    and not any(part.startswith(".") for part in path.relative_to(reference_source).parts)
                ):
                    expected_shas.add(_compute_file_sha256(path))
        evidence_desc = "assets/authority/reference-source/*"

    if not expected_shas:
        errors.append(f"authority.yaml content_sha256 has no local evidence to validate against for lane {lane}")
        return

    if content_sha256 not in expected_shas:
        errors.append(f"authority.yaml content_sha256 does not match SHA-256 of {evidence_desc}")
    if isinstance(authority_reconciled, str) and authority_reconciled not in expected_shas:
        errors.append(f"authority.yaml decomposition.reconciled_against does not match SHA-256 of {evidence_desc}")
    if isinstance(source_map_reconciled, str) and source_map_reconciled not in expected_shas:
        errors.append(f"source-map.yaml reconciled_against does not match SHA-256 of {evidence_desc}")
    if isinstance(authority_reconciled, str) and content_sha256 != authority_reconciled:
        errors.append("authority.yaml content_sha256 must match decomposition.reconciled_against")


def _validate_references(
    references: object, *, record_name: str, lane: object, skill_root: Path, errors: list[str]
) -> list[object] | None:
    if not isinstance(references, list):
        errors.append(f"{record_name} references must be a nonempty list")
        return None
    if not references:
        errors.append(f"{record_name} references must be a nonempty list")
        return references
    for index, reference in enumerate(references, start=1):
        if not isinstance(reference, dict):
            errors.append(f"{record_name} references[{index}] must be a mapping")
            continue
        for field in sorted(REQUIRED_REFERENCE_FIELDS):
            if field not in reference:
                errors.append(f"{record_name} references[{index}] is missing {field}")
        _validate_reference_path(
            reference.get("path"),
            skill_root=skill_root,
            field=f"{record_name} references[{index}] path",
            errors=errors,
        )
        _validate_string_list(
            reference.get("source_sections"),
            field=f"{record_name} references[{index}] source_sections",
            errors=errors,
        )
        _validate_string_list(
            reference.get("load_when"),
            field=f"{record_name} references[{index}] load_when",
            errors=errors,
        )
        content_mode = reference.get("content_mode")
        if not isinstance(content_mode, str) or content_mode not in CONTENT_MODES:
            errors.append(
                f"{record_name} references[{index}] has unsupported content_mode "
                f"{content_mode!r}"
            )
        if lane == "skills-with-citation" and content_mode not in CONTENT_MODES:
            errors.append(
                f"{record_name} references[{index}] has unsupported content_mode "
                f"{content_mode!r} for skills-with-citation"
            )
    return references


def validate_authority_skill(skill_root: Path) -> list[str]:
    authority_root = skill_root / "assets/authority"
    authority_path = authority_root / "authority.yaml"
    source_map_path = authority_root / "source-map.yaml"
    citations_path = authority_root / "CITATIONS.md"
    errors: list[str] = []

    if (
        skill_root.name.startswith("mark-")
        and skill_root.parent.name == "skills"
        and skill_root.parent.parent.name == ".agents"
    ):
        errors.append("local mark-* skills must not contain authority assets")

    for path in (authority_path, source_map_path, citations_path):
        if not path.is_file():
            errors.append(f"missing {path.name}")

    if not authority_path.is_file():
        return errors

    record = _load_mapping(authority_path, errors)
    source_map = _load_mapping(source_map_path, errors) if source_map_path.is_file() else None
    if record is None:
        return errors

    if type(record.get("schema_version")) is not int or record.get("schema_version") != 1:
        errors.append("authority.yaml must declare schema_version: 1")

    lane = record.get("lane")
    if not isinstance(lane, str) or lane not in LANES:
        errors.append(f"authority.yaml lane must be one of {sorted(LANES)}")
    if record.get("custody") != "marketplace":
        errors.append("authority.yaml must declare custody: marketplace")

    authority = record.get("authority")
    authority_records: dict[str, dict] = {}
    if not isinstance(authority, dict):
        errors.append("authority.yaml authority must be a mapping")
    else:
        if lane == "skills-with-mixed-source":
            if not authority:
                errors.append("authority.yaml authority must contain at least one source label")
            for label, source_record in authority.items():
                if not _nonblank_string(label):
                    errors.append("authority.yaml authority source labels must be nonblank strings")
                    continue
                if not _is_safe_label(label):
                    errors.append(
                        f"authority.yaml authority source label {label!r} must be a safe single directory name"
                    )
                    continue
                validated = _validate_single_authority_record(
                    source_record, f"authority.yaml authority[{label}]", errors
                )
                if validated is not None:
                    authority_records[label] = validated
        else:
            validated = _validate_single_authority_record(
                authority, "authority.yaml authority", errors
            )
            if validated is not None:
                authority_records[""] = validated

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
            if lane == "skills-with-mixed-source":
                if not isinstance(authority_reconciled_against, dict) or not authority_reconciled_against:
                    errors.append(
                        "authority.yaml decomposition reconciled_against must be a non-empty mapping for skills-with-mixed-source"
                    )
                else:
                    for label, sha in authority_reconciled_against.items():
                        if not _nonblank_string(label):
                            errors.append(
                                "authority.yaml decomposition reconciled_against labels must be nonblank strings"
                            )
                        elif not _nonblank_string(sha) or not SHA256_PATTERN.fullmatch(sha):
                            errors.append(
                                f"authority.yaml decomposition reconciled_against[{label}] must be a 64-character lowercase SHA-256"
                            )
                    if isinstance(authority, dict):
                        for label in authority:
                            if label not in authority_reconciled_against:
                                errors.append(
                                    f"authority.yaml decomposition.reconciled_against is missing source label {label}"
                                )
                        for label in authority_reconciled_against:
                            if label not in authority:
                                errors.append(
                                    f"authority.yaml decomposition.reconciled_against has unknown source label {label}"
                                )
            else:
                if not _nonblank_string(authority_reconciled_against):
                    errors.append("authority.yaml decomposition reconciled_against must be a nonblank string")
                elif not SHA256_PATTERN.fullmatch(authority_reconciled_against):
                    errors.append("authority.yaml decomposition reconciled_against must be a 64-character lowercase SHA-256")
        authority_references = _validate_references(
            decomposition.get("references"),
            record_name="authority.yaml decomposition",
            lane=lane,
            skill_root=skill_root,
            errors=errors,
        )

    source_map_reconciled_against: object | None = None
    source_map_references: list[object] | None = None
    if source_map is not None:
        if type(source_map.get("schema_version")) is not int or source_map.get("schema_version") != 1:
            errors.append("source-map.yaml must declare schema_version: 1")
        for field in sorted(set(source_map) - SOURCE_MAP_FIELDS):
            errors.append(f"source-map.yaml has unsupported top-level field {field}")
        if "reconciled_against" not in source_map:
            errors.append("source-map.yaml is missing reconciled_against")
        else:
            source_map_reconciled_against = source_map["reconciled_against"]
            if lane == "skills-with-mixed-source":
                if not isinstance(source_map_reconciled_against, dict) or not source_map_reconciled_against:
                    errors.append(
                        "source-map.yaml reconciled_against must be a non-empty mapping for skills-with-mixed-source"
                    )
                else:
                    for label, sha in source_map_reconciled_against.items():
                        if not _nonblank_string(label):
                            errors.append("source-map.yaml reconciled_against labels must be nonblank strings")
                        elif not _nonblank_string(sha) or not SHA256_PATTERN.fullmatch(sha):
                            errors.append(
                                f"source-map.yaml reconciled_against[{label}] must be a 64-character lowercase SHA-256"
                            )
                    if isinstance(authority, dict):
                        for label in authority:
                            if label not in source_map_reconciled_against:
                                errors.append(
                                    f"source-map.yaml reconciled_against is missing source label {label}"
                                )
                        for label in source_map_reconciled_against:
                            if label not in authority:
                                errors.append(
                                    f"source-map.yaml reconciled_against has unknown source label {label}"
                                )
            else:
                if not _nonblank_string(source_map_reconciled_against):
                    errors.append("source-map.yaml reconciled_against must be a nonblank string")
                elif not SHA256_PATTERN.fullmatch(source_map_reconciled_against):
                    errors.append("source-map.yaml reconciled_against must be a 64-character lowercase SHA-256")
        source_map_references = _validate_references(
            source_map.get("references"),
            record_name="source-map.yaml",
            lane=lane,
            skill_root=skill_root,
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
    elif lane == "skills-with-mixed-source":
        if not reference_source.is_dir() or not any(reference_source.iterdir()):
            errors.append("skills-with-mixed-source reference-source must contain at least one labelled source directory")
        else:
            for label in authority_records:
                label_dir = reference_source / label
                if not label_dir.is_dir() or not _contains_non_hidden_file(label_dir):
                    errors.append(
                        f"skills-with-mixed-source reference-source/{label} must contain at least one non-hidden file"
                    )
    if lane == "skills-with-citation" and reference_source.is_dir() and any(reference_source.iterdir()):
        errors.append("skills-with-citation reference-source must not contain vendored source files")
    if citations_path.is_file():
        _validate_citations(citations_path, errors)

    _validate_sha_against_evidence(skill_root, record, source_map, citations_path, errors)

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
