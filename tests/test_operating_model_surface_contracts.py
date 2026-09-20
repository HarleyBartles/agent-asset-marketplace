from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "codex-marketplace" / "plugins" / "agent-operating-model" / "skills" / "repo-shape"
MODULE_PATH = SKILL_ROOT / "scripts" / "surface_contracts.py"
SCHEMA_PATH = SKILL_ROOT / "references" / "repository-shape-manifest.schema.json"
AUDIT_PATH = SKILL_ROOT / "references" / "consumer-surface-audit.md"
SCAFFOLD_PATH = SKILL_ROOT / "scripts" / "scaffold_operating_model_contract.py"


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


def _run_scaffold(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCAFFOLD_PATH), *args],
        cwd=repo,
        capture_output=True,
        text=True,
    )


def test_operating_model_contract_scaffold_creates_missing_file(tmp_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    result = _run_scaffold(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads((tmp_path / ".agents/contracts/agent-operating-model.json").read_text())
    assert data == {"version": 1, "surface_exceptions": [], "unslop_profile_roots": [".agents/contracts/unslop"]}


def test_operating_model_contract_customized_valid_passes(tmp_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    path = tmp_path / ".agents/contracts/agent-operating-model.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "version": 1,
                "surface_exceptions": [{"id": "marketplace-source-submodule", "reason": "source repository"}],
                "unslop_profile_roots": [".agents/contracts/unslop", "packages/ui/.agents/contracts/unslop"],
            }
        ),
        encoding="utf-8",
    )
    before = path.read_bytes()
    assert _run_scaffold(tmp_path, "--check").returncode == 0
    assert _run_scaffold(tmp_path).returncode == 0
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({"version": 2, "surface_exceptions": [], "unslop_profile_roots": []}, "version"),
        (
            {"version": 1, "surface_exceptions": [{"id": "invented", "reason": "x"}], "unslop_profile_roots": []},
            "unknown surface",
        ),
    ],
)
def test_operating_model_contract_rejects_invalid_content(tmp_path: Path, payload: object, message: str) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    path = tmp_path / ".agents/contracts/agent-operating-model.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
    result = _run_scaffold(tmp_path, "--check")
    assert result.returncode != 0
    assert message in (result.stdout + result.stderr).lower()


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


@pytest.mark.parametrize(
    ("field", "value"), [("path", "../outside"), ("seed", "/absolute"), ("scaffold", "../tool.py")]
)
def test_surface_contract_rejects_escaping_paths(tmp_path: Path, field: str, value: str) -> None:
    surface = _valid_surface(**{field: value})
    with pytest.raises(ValueError, match="repository-relative path"):
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
