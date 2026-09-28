from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "skills/repo-shape/scripts"
sys.path.insert(0, str(SCRIPTS))

import migrate_operating_standards  # noqa: E402
import operating_standards_catalog  # noqa: E402

CATALOG_PATH = ROOT / "skills/repo-shape/references/operating-standards-catalog.json"
MANIFEST_PATH = ROOT / "skills/repo-shape/references/repository-shape-manifest.json"
CATALOG = operating_standards_catalog.load_catalog(CATALOG_PATH, MANIFEST_PATH, ROOT)
REVISION = "b" * 40


def _legacy_repo(root: Path, selected: set[str]) -> tuple[Path, bytes, bytes]:
    contract_path = root / ".agents/contracts/agent-operating-model.json"
    contract_path.parent.mkdir(parents=True)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    known = {surface["id"] for surface in manifest["surfaces"]}
    standard_surfaces = {surface_id for standard in CATALOG.standards for surface_id in standard.surfaces}
    assert standard_surfaces <= known
    selected_surfaces = {
        surface_id for standard in CATALOG.standards if standard.id in selected for surface_id in standard.surfaces
    }
    exceptions = [{"id": surface_id, "reason": "legacy fixture"} for surface_id in sorted(known - selected_surfaces)]
    contract = {
        "version": 1,
        "surface_exceptions": exceptions,
        "unslop_profile_roots": [".agents/contracts/unslop"],
    }
    contract_path.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")
    plugin_path = root / ".agents/plugins/marketplace.json"
    plugin_path.parent.mkdir(parents=True)
    plugin_path.write_text('{"plugins":[]}\n', encoding="utf-8")
    hook_path = root / "githooks/pre-commit"
    hook_path.parent.mkdir(parents=True)
    hook_path.write_text("hook stays byte-identical\n", encoding="utf-8")
    return contract_path, contract_path.read_bytes(), hook_path.read_bytes()


def test_migration_preview_preserves_enabled_standards_and_does_not_write(tmp_path: Path) -> None:
    selected = {"root-agent-router", "markdown-formatting"}
    legacy_path, legacy_before, hook_before = _legacy_repo(tmp_path, selected)
    target = tmp_path / ".agents/contracts/operating-standards.json"

    result = migrate_operating_standards.plan_migration(tmp_path, CATALOG, REVISION)

    assert {entry["id"] for entry in result["standards"]} == selected
    assert all(entry["revision"] == REVISION for entry in result["standards"])
    assert "operating-model-contract" not in {entry["id"] for entry in result["standards"]}
    assert not target.exists()
    assert legacy_path.read_bytes() == legacy_before
    assert (tmp_path / "githooks/pre-commit").read_bytes() == hook_before


def test_migration_refuses_partial_legacy_standard_adoption(tmp_path: Path) -> None:
    _legacy_repo(tmp_path, {"root-agent-router", "runbook-composition"})
    legacy_path = tmp_path / ".agents/contracts/agent-operating-model.json"
    data = json.loads(legacy_path.read_text(encoding="utf-8"))
    data["surface_exceptions"].append({"id": "runbook-set", "reason": "legacy partial exception"})
    legacy_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="partially enabled legacy standard"):
        migrate_operating_standards.plan_migration(tmp_path, CATALOG, REVISION)

    assert not (tmp_path / ".agents/contracts/operating-standards.json").exists()


def test_migration_refuses_when_no_authoritative_legacy_contract_exists(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="no authoritative legacy surface contract"):
        migrate_operating_standards.plan_migration(tmp_path, CATALOG, REVISION)


def test_migration_apply_writes_only_the_new_contract(tmp_path: Path) -> None:
    selected = {"root-agent-router"}
    legacy_path, legacy_before, hook_before = _legacy_repo(tmp_path, selected)

    migrate_operating_standards.migrate_contract(tmp_path, CATALOG, REVISION, apply=False)
    target = tmp_path / ".agents/contracts/operating-standards.json"
    assert not target.exists()

    migrate_operating_standards.migrate_contract(tmp_path, CATALOG, REVISION, apply=True)
    assert json.loads(target.read_text(encoding="utf-8"))["standards"][0]["id"] == "root-agent-router"
    assert legacy_path.read_bytes() == legacy_before
    assert (tmp_path / "githooks/pre-commit").read_bytes() == hook_before
