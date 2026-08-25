from __future__ import annotations

import json
import os
import re
from datetime import date
from pathlib import Path
from typing import Any


ENGINE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[6]
DEFAULT_ROOT = ENGINE_ROOT.parent / "writing-style" / "references" / "profiles"
PROFILE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


class ProfileError(ValueError):
    pass


def profiles_root(requested: Path | None) -> Path:
    root = (requested or DEFAULT_ROOT).resolve()
    if root.name == "profiles" and root.parent.name == "references":
        return root
    candidate = root / "references" / "profiles"
    if candidate.is_dir():
        return candidate.resolve()
    raise ProfileError(f"lawful references/profiles root not found: {root}")


def discover(requested: Path | None) -> list[dict[str, str]]:
    root = profiles_root(requested)
    found: list[dict[str, str]] = []
    for directory, names, files in os.walk(root, followlinks=False):
        current = Path(directory)
        for name in list(names) + list(files):
            entry = current / name
            if entry.is_symlink():
                target = entry.resolve()
                try:
                    target.relative_to(root)
                except ValueError as exc:
                    raise ProfileError(f"symlink escape rejected: {entry} -> {target}") from exc
        if "patterns.json" not in files:
            continue
        path = (current / "patterns.json").resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise ProfileError(f"profile path escapes references/profiles: {path}") from exc
        document = load_json(path)
        if not {"profile_id", "profile_kind", "version", "patterns"} <= set(document):
            continue
        found.append(
            {
                "id": str(document["profile_id"]),
                "version": str(document["version"]),
                "kind": str(document["profile_kind"]),
                "path": str(path),
            }
        )
    return sorted(found, key=lambda item: item["path"].replace("\\", "/").casefold())


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ProfileError(f"{path}: invalid UTF-8 JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ProfileError(f"{path}: expected a JSON object")
    return value


def _walk(value: Any, path: str = "$"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield f"{path}.{key}", key, child
            yield from _walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}[{index}]")


def unsafe_fields(value: Any) -> list[str]:
    errors: list[str] = []
    forbidden = (
        "detector", "ai_likelihood", "ai_probability", "authorship_verdict",
        "authorship_score", "forbidden_words", "banned_words", "never_use_tokens",
    )
    for path, key, child in _walk(value):
        normalized = re.sub(r"(?<!^)(?=[A-Z])", "_", key).replace("-", "_").lower()
        if any(term in normalized for term in forbidden):
            errors.append(f"{path}: prohibited detector, authorship, or universal-token semantics")
        if isinstance(child, str):
            lower = child.lower()
            if re.search(r"\b(always|never|every)\b.*\b(remove|delete|ban|forbid|omit|use)\b", lower):
                errors.append(f"{path}: prohibited universal token restriction")
    return errors


def validate_document(path: Path, source_ids: set[str]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        document = load_json(path)
    except ProfileError as exc:
        return [str(exc)], warnings
    required = {"schema_version", "profile_id", "profile_kind", "version", "reviewed_at", "review_after", "patterns"}
    missing = sorted(required - set(document))
    if missing:
        errors.append(f"{path}: missing required fields {missing}")
        return errors, warnings
    if document["schema_version"] != 1:
        errors.append(f"{path}.schema_version: expected 1")
    if not isinstance(document["profile_id"], str) or not PROFILE_ID.fullmatch(document["profile_id"]):
        errors.append(f"{path}.profile_id: expected stable lowercase-hyphenated ID")
    if document["profile_kind"] not in {"fatigue", "voice"}:
        errors.append(f"{path}.profile_kind: unsupported kind {document['profile_kind']!r}")
    if not isinstance(document["version"], str) or not SEMVER.fullmatch(document["version"]):
        errors.append(f"{path}.version: expected semantic version")
    try:
        reviewed = date.fromisoformat(document["reviewed_at"])
        review_after = date.fromisoformat(document["review_after"])
        if reviewed >= review_after:
            errors.append(f"{path}.review_after: must follow reviewed_at")
        if review_after < date.today():
            warnings.append(f"{path}.review_after: expired; recommendations downgrade to candidate")
    except (TypeError, ValueError):
        errors.append(f"{path}: reviewed_at and review_after must be ISO dates")
    patterns = document.get("patterns")
    if not isinstance(patterns, list):
        errors.append(f"{path}.patterns: expected array")
        return errors, warnings
    ids: set[str] = set()
    golden_ids: set[str] = set()
    golden_path = path.with_name("goldens.json")
    if golden_path.is_file():
        try:
            golden = load_json(golden_path)
            golden_ids = {case.get("id") for case in golden.get("cases", []) if isinstance(case, dict)}
        except ProfileError as exc:
            errors.append(str(exc))
    for index, pattern in enumerate(patterns):
        prefix = f"{path}.patterns[{index}]"
        if not isinstance(pattern, dict):
            errors.append(f"{prefix}: expected object")
            continue
        pattern_id = pattern.get("id")
        if not isinstance(pattern_id, str) or not PROFILE_ID.fullmatch(pattern_id):
            errors.append(f"{prefix}.id: expected stable lowercase-hyphenated ID")
        elif pattern_id in ids:
            errors.append(f"{prefix}.id: duplicate {pattern_id}")
        else:
            ids.add(pattern_id)
        if pattern.get("evidence_class") not in {
            "well_supported_reader_fatigue", "plausible_emerging",
            "author_specific_preference", "weak_or_folk_heuristic",
        }:
            errors.append(f"{prefix}.evidence_class: unsupported value")
        unknown_sources = sorted(set(pattern.get("source_ids", [])) - source_ids)
        if unknown_sources:
            errors.append(f"{prefix}.source_ids: unknown IDs {unknown_sources}")
        unknown_goldens = sorted(set(pattern.get("golden_case_ids", [])) - golden_ids)
        if unknown_goldens:
            errors.append(f"{prefix}.golden_case_ids: unknown IDs {unknown_goldens}")
    errors.extend(f"{path}{item[1:]}" for item in unsafe_fields(document))
    if golden_path.is_file():
        golden = load_json(golden_path)
        for index, case in enumerate(golden.get("cases", [])):
            for finding in case.get("expected_findings", []):
                unknown = sorted(set(finding.get("pattern_ids", [])) - ids)
                if unknown:
                    errors.append(f"{golden_path}.cases[{index}].expected_findings: unknown IDs {unknown}")
    return errors, warnings


def source_ids() -> set[str]:
    register = load_json(REPO_ROOT / "research" / "ai-prose-fatigue" / "source-register.json")
    return {item["id"] for item in register.get("sources", [])}
