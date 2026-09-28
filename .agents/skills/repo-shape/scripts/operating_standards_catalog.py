#!/usr/bin/env python3
"""Validate the Agent Operating Model standards catalog and its source resources."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import surface_contracts


_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_REQUIRED = {"id", "title", "surfaces", "resources", "check", "apply", "requires"}


@dataclass(frozen=True)
class OperatingStandard:
    id: str
    title: str
    surfaces: tuple[str, ...]
    resources: tuple[str, ...]
    check: bool
    apply: bool
    requires: tuple[str, ...]


@dataclass(frozen=True)
class StandardsCatalog:
    version: int
    standards: tuple[OperatingStandard, ...]


def _string_list(raw: Any, *, field: str, standard_id: str, allow_empty: bool = False) -> tuple[str, ...]:
    if not isinstance(raw, list) or (not raw and not allow_empty):
        raise ValueError(f"standard {standard_id} {field} must be a non-empty list")
    if any(not isinstance(item, str) or not item.strip() for item in raw):
        raise ValueError(f"standard {standard_id} {field} must contain non-empty strings")
    if len(raw) != len(set(raw)):
        raise ValueError(f"standard {standard_id} {field} contains duplicate values")
    return tuple(raw)


def _resource_path(raw: str, *, standard_id: str, source_root: Path) -> Path:
    normalized = raw.replace("\\", "/")
    path = Path(normalized)
    if (
        path.is_absolute()
        or normalized.startswith("/")
        or not path.parts
        or ".." in path.parts
        or normalized in {"", "."}
    ):
        raise ValueError(f"standard {standard_id} resource must be repository-relative without '..': {raw}")
    candidate = (source_root / path).resolve()
    try:
        candidate.relative_to(source_root.resolve())
    except ValueError as exc:
        raise ValueError(f"standard {standard_id} resource escapes marketplace source: {raw}") from exc
    if not candidate.is_file():
        raise ValueError(f"standard {standard_id} resource does not exist: {normalized}")
    return candidate


def _check_cycles(standards: dict[str, OperatingStandard]) -> None:
    done: set[str] = set()
    active: list[str] = []

    def visit(standard_id: str) -> None:
        if standard_id in active:
            cycle = " -> ".join([*active[active.index(standard_id) :], standard_id])
            raise ValueError(f"standard dependency cycle: {cycle}")
        if standard_id in done:
            return
        active.append(standard_id)
        for dependency in standards[standard_id].requires:
            if dependency not in standards:
                raise ValueError(f"standard {standard_id} has unknown dependency: {dependency}")
            visit(dependency)
        active.pop()
        done.add(standard_id)

    for standard_id in standards:
        visit(standard_id)


def load_catalog(catalog_path: Path, manifest_path: Path, source_root: Path) -> StandardsCatalog:
    """Load and validate catalog structure, surface ownership, dependencies, and resources."""

    raw = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    if not isinstance(raw, dict) or set(raw) != {"version", "standards"}:
        raise ValueError("catalog must contain only version and standards")
    if raw["version"] != 1:
        raise ValueError("catalog version must be 1")
    rows = raw["standards"]
    if not isinstance(rows, list) or not rows:
        raise ValueError("catalog standards must be a non-empty list")

    standards: list[OperatingStandard] = []
    ids: set[str] = set()
    assigned: dict[str, str] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != _REQUIRED:
            raise ValueError(f"standard[{index}] must contain exactly: {', '.join(sorted(_REQUIRED))}")
        standard_id = row["id"]
        title = row["title"]
        if not isinstance(standard_id, str) or not _ID.fullmatch(standard_id):
            raise ValueError(f"standard[{index}] id must be kebab-case")
        if standard_id in ids:
            raise ValueError(f"duplicate standard id: {standard_id}")
        ids.add(standard_id)
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"standard {standard_id} title must be non-empty")
        surfaces = _string_list(row["surfaces"], field="surfaces", standard_id=standard_id)
        resources = _string_list(row["resources"], field="resources", standard_id=standard_id)
        requires = _string_list(row["requires"], field="requires", standard_id=standard_id, allow_empty=True)
        for surface_id in surfaces:
            if surface_id in assigned:
                raise ValueError(f"surface {surface_id} assigned more than once")
            assigned[surface_id] = standard_id
        for resource in resources:
            _resource_path(resource, standard_id=standard_id, source_root=source_root)
        for capability in ("check", "apply"):
            if not isinstance(row[capability], bool):
                raise ValueError(f"standard {standard_id} {capability} must be a boolean")
        if not row["check"]:
            raise ValueError(f"standard {standard_id} must support check")
        standards.append(
            OperatingStandard(
                standard_id,
                title,
                surfaces,
                resources,
                row["check"],
                row["apply"],
                requires,
            )
        )

    manifest = surface_contracts.load_manifest(manifest_path)
    expected_surfaces = {surface.id for surface in manifest.surfaces}
    actual_surfaces = set(assigned)
    unknown_surfaces = actual_surfaces - expected_surfaces
    if unknown_surfaces:
        raise ValueError(f"catalog contains unknown surface(s): {', '.join(sorted(unknown_surfaces))}")
    uncovered = expected_surfaces - actual_surfaces
    if uncovered:
        raise ValueError(f"catalog does not assign surface(s): {', '.join(sorted(uncovered))}")
    by_id = {standard.id: standard for standard in standards}
    _check_cycles(by_id)
    return StandardsCatalog(version=1, standards=tuple(standards))
