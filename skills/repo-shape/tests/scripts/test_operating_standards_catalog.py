from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "skills/repo-shape/scripts"
sys.path.insert(0, str(SCRIPTS))

import operating_standards_catalog  # noqa: E402

CATALOG = ROOT / "skills/repo-shape/references/operating-standards-catalog.json"
MANIFEST = ROOT / "skills/repo-shape/references/repository-shape-manifest.json"


def _load(payload: dict[str, object] | None = None, *, tmp_path: Path | None = None):
    if payload is None:
        return operating_standards_catalog.load_catalog(CATALOG, MANIFEST, ROOT)
    assert tmp_path is not None
    path = tmp_path / "catalog.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return operating_standards_catalog.load_catalog(path, MANIFEST, ROOT)


def test_catalog_assigns_each_shape_surface_once_to_independent_standards() -> None:
    catalog = _load()
    raw_manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected = {surface["id"] for surface in raw_manifest["surfaces"]}
    memberships = [surface_id for standard in catalog.standards for surface_id in standard.surfaces]
    memberships.extend(catalog.migration_surfaces)

    assert set(memberships) == expected
    assert len(memberships) == len(set(memberships))
    assert {standard.id for standard in catalog.standards} >= {
        "root-agent-router",
        "runbook-composition",
        "playbook-composition",
        "markdown-formatting",
    }
    assert "operating-model-contract" in catalog.migration_surfaces
    by_id = {standard.id: set(standard.surfaces) for standard in catalog.standards}
    assert by_id["root-agent-router"].isdisjoint(by_id["playbook-composition"])


def test_catalog_rejects_duplicate_standard_ids(tmp_path: Path) -> None:
    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    payload["standards"].append(payload["standards"][0])

    with pytest.raises(ValueError, match="duplicate standard id"):
        _load(payload, tmp_path=tmp_path)


def test_catalog_rejects_unknown_or_duplicate_surface_ids(tmp_path: Path) -> None:
    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    payload["standards"][0]["surfaces"].append("not-a-real-surface")
    with pytest.raises(ValueError, match="unknown surface"):
        _load(payload, tmp_path=tmp_path)

    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    payload["standards"][1]["surfaces"].append(payload["standards"][0]["surfaces"][0])
    with pytest.raises(ValueError, match="assigned more than once"):
        _load(payload, tmp_path=tmp_path)


def test_catalog_rejects_unknown_dependencies_and_cycles(tmp_path: Path) -> None:
    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    payload["standards"][0]["requires"] = ["missing-standard"]
    with pytest.raises(ValueError, match="unknown dependency"):
        _load(payload, tmp_path=tmp_path)

    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    first, second = payload["standards"][:2]
    first["requires"] = [second["id"]]
    second["requires"] = [first["id"]]
    with pytest.raises(ValueError, match="dependency cycle"):
        _load(payload, tmp_path=tmp_path)


def test_catalog_rejects_resources_outside_or_missing_from_marketplace_source(tmp_path: Path) -> None:
    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    payload["standards"][0]["resources"] = ["../outside.py"]
    with pytest.raises(ValueError, match="repository-relative"):
        _load(payload, tmp_path=tmp_path)

    payload["standards"][0]["resources"] = ["skills/repo-shape/scripts/not-real.py"]
    with pytest.raises(ValueError, match="resource does not exist"):
        _load(payload, tmp_path=tmp_path)
