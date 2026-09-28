from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts"
sys.path.insert(0, str(SCRIPTS))

import plugin_contracts  # noqa: E402


HARD_PLUGINS = ["agent-operating-model", "superpowers-plus", "repo-worker-pack"]


def _write_marketplace(root: Path, installed: list[str]) -> None:
    path = root / ".agents/plugins/marketplace.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "plugins": [{"name": name, "policy": {"installation": "INSTALLED_BY_DEFAULT"}} for name in installed],
                "repo": {"local_skills": []},
            }
        ),
        encoding="utf-8",
    )


def _default_contract() -> plugin_contracts.ConsumerContract:
    return plugin_contracts.ConsumerContract(surface_exceptions=(), unslop_profile_roots=(".agents/contracts/unslop",))


def test_missing_hard_prerequisite_fails(tmp_path: Path) -> None:
    _write_marketplace(tmp_path, ["agent-operating-model", "repo-worker-pack", "writing-pack"])
    findings = plugin_contracts.check_plugin_contract(tmp_path, _default_contract())
    assert any(item.code == "missing-prerequisite-plugin" and item.surface == "superpowers-plus" for item in findings)


def test_missing_writing_pack_warns_without_failure(tmp_path: Path) -> None:
    _write_marketplace(tmp_path, HARD_PLUGINS)
    findings = plugin_contracts.check_plugin_contract(tmp_path, _default_contract())
    assert [(item.severity, item.code) for item in findings] == [("warning", "missing-writing-pack")]


def test_unslop_profiles_require_unslop_plus(tmp_path: Path) -> None:
    _write_marketplace(tmp_path, HARD_PLUGINS + ["writing-pack"])
    profile = tmp_path / ".agents/contracts/unslop/repository.md"
    profile.parent.mkdir(parents=True)
    profile.write_text("# Repository profile\n", encoding="utf-8")
    findings = plugin_contracts.check_plugin_contract(tmp_path, _default_contract())
    assert any(item.code == "missing-unslop-plus" and item.severity == "failure" for item in findings)


def test_arbitrary_additional_plugins_are_allowed(tmp_path: Path) -> None:
    _write_marketplace(tmp_path, HARD_PLUGINS + ["writing-pack", "anything-else"])
    assert plugin_contracts.check_plugin_contract(tmp_path, _default_contract()) == []


def test_plugin_contract_does_not_inventory_individual_skills(tmp_path: Path) -> None:
    _write_marketplace(tmp_path, HARD_PLUGINS + ["writing-pack"])
    assert plugin_contracts.check_plugin_contract(tmp_path, _default_contract()) == []


def test_coordinator_writing_warning_is_non_blocking(tmp_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    _write_marketplace(tmp_path, HARD_PLUGINS)
    manifest = json.loads((SCRIPTS.parent / "references/repository-shape-manifest.json").read_text(encoding="utf-8"))
    enabled = {"marketplace-json", "operating-model-contract"}
    contract = tmp_path / ".agents/contracts/agent-operating-model.json"
    contract.parent.mkdir(parents=True)
    contract.write_text(
        json.dumps(
            {
                "version": 1,
                "surface_exceptions": [
                    {"id": surface["id"], "reason": "isolated warning fixture"}
                    for surface in manifest["surfaces"]
                    if surface["id"] not in enabled
                ],
                "unslop_profile_roots": [".agents/contracts/unslop"],
            }
        ),
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "repo_standards.py"), "--check"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined
    assert "WARN: [missing-writing-pack]" in combined
    assert "DRIFT:" not in combined
