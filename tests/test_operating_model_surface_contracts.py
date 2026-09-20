from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "codex-marketplace" / "plugins" / "agent-operating-model" / "skills" / "repo-shape"
MODULE_PATH = SKILL_ROOT / "scripts" / "surface_contracts.py"
SCHEMA_PATH = SKILL_ROOT / "references" / "repository-shape-manifest.schema.json"
AUDIT_PATH = SKILL_ROOT / "references" / "consumer-surface-audit.md"


def _module():
    assert MODULE_PATH.is_file(), "surface_contracts.py must own manifest validation"
    spec = importlib.util.spec_from_file_location("surface_contracts_under_test", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _valid_surface(**overrides: object) -> dict[str, object]:
    surface: dict[str, object] = {
        "id": "example",
        "path": ".agents/example.md",
        "presence": "required",
        "ownership": "consumer-authored",
        "validator": "file-exists",
        "apply": "create",
        "force_reset": "unavailable",
        "seed": None,
        "scaffold": None,
        "required_with": None,
    }
    surface.update(overrides)
    return surface


def _write_manifest(tmp_path: Path, surfaces: list[dict[str, object]]) -> Path:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps({"version": 3, "surfaces": surfaces}), encoding="utf-8")
    return path


def test_surface_contract_assets_exist() -> None:
    assert MODULE_PATH.is_file()
    assert SCHEMA_PATH.is_file()
    assert AUDIT_PATH.is_file()


@pytest.mark.parametrize("missing", ["presence", "ownership", "validator", "apply", "force_reset"])
def test_surface_contract_rejects_implicit_behavior(tmp_path: Path, missing: str) -> None:
    surface = _valid_surface()
    del surface[missing]
    with pytest.raises(ValueError, match=missing):
        _module().load_manifest(_write_manifest(tmp_path, [surface]))


def test_surface_contract_rejects_unknown_fields(tmp_path: Path) -> None:
    surface = _valid_surface(typo="silent-default")
    with pytest.raises(ValueError, match="unknown.*typo"):
        _module().load_manifest(_write_manifest(tmp_path, [surface]))


def test_seed_never_implies_identity_validation(tmp_path: Path) -> None:
    surface = _valid_surface(seed="templates/example.md", validator="identity")
    with pytest.raises(ValueError, match="consumer-authored.*identity"):
        _module().load_manifest(_write_manifest(tmp_path, [surface]))


def test_consumer_surface_rejects_unconditional_overwrite(tmp_path: Path) -> None:
    surface = _valid_surface(apply="overwrite")
    with pytest.raises(ValueError, match="consumer-authored.*overwrite"):
        _module().load_manifest(_write_manifest(tmp_path, [surface]))


def test_surface_contract_rejects_unregistered_validator(tmp_path: Path) -> None:
    surface = _valid_surface(validator="not-registered")
    with pytest.raises(ValueError, match="unregistered validator.*not-registered"):
        _module().load_manifest(_write_manifest(tmp_path, [surface]))


def test_forbidden_surface_requires_remediation(tmp_path: Path) -> None:
    surface = _valid_surface(presence="forbidden", apply="create")
    with pytest.raises(ValueError, match="forbidden.*manual-remediation"):
        _module().load_manifest(_write_manifest(tmp_path, [surface]))


def test_repository_manifest_is_version_three_and_explicit() -> None:
    manifest = _module().load_manifest(SKILL_ROOT / "references" / "repository-shape-manifest.json")
    assert manifest.version == 3
    assert manifest.surfaces
    assert all(surface.presence and surface.ownership and surface.validator for surface in manifest.surfaces)
