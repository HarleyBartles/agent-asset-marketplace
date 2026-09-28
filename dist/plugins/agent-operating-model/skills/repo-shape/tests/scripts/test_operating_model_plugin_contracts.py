from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "skills/repo-shape/scripts"
sys.path.insert(0, str(SCRIPTS))

import plugin_contracts  # noqa: E402


def _write_marketplace(root: Path, installed: list[str]) -> None:
    path = root / ".agents/plugins/marketplace.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"plugins": [{"name": name} for name in installed]}), encoding="utf-8")


def _legacy_contract(root: Path) -> None:
    manifest = json.loads((SCRIPTS.parent / "references/repository-shape-manifest.json").read_text(encoding="utf-8"))
    enabled = {"marketplace-json", "operating-model-contract"}
    path = root / ".agents/contracts/agent-operating-model.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "version": 1,
                "surface_exceptions": [
                    {"id": surface["id"], "reason": "isolated legacy fixture"}
                    for surface in manifest["surfaces"]
                    if surface["id"] not in enabled
                ],
                "unslop_profile_roots": [".agents/contracts/unslop"],
            }
        ),
        encoding="utf-8",
    )


def _run_standards(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "repo_standards.py"), "--check"],
        cwd=root,
        capture_output=True,
        text=True,
    )


def test_plugin_contract_is_noop_for_missing_ambient_plugins(tmp_path: Path) -> None:
    _write_marketplace(tmp_path, [])
    config = plugin_contracts.ConsumerContract((), (".agents/contracts/unslop",))
    assert plugin_contracts.check_plugin_contract(tmp_path, config) == []


def test_unslop_profile_presence_does_not_require_plugin_subscription(tmp_path: Path) -> None:
    profile = tmp_path / ".agents/contracts/unslop/repository.md"
    profile.parent.mkdir(parents=True)
    profile.write_text("# Repository profile\n", encoding="utf-8")
    _write_marketplace(tmp_path, [])
    config = plugin_contracts.ConsumerContract((), (".agents/contracts/unslop",))
    assert plugin_contracts.check_plugin_contract(tmp_path, config) == []


def test_legacy_coordinator_passes_without_any_plugin_subscriptions(tmp_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    _write_marketplace(tmp_path, [])
    _legacy_contract(tmp_path)
    result = _run_standards(tmp_path)
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined
    assert "WARN:" not in combined
    assert "DRIFT:" not in combined


def test_composition_coordinator_passes_with_empty_plugin_subscriptions(tmp_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    _write_marketplace(tmp_path, [])
    path = tmp_path / ".agents/contracts/operating-standards.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"version":1,"standards":[]}\n', encoding="utf-8")
    result = _run_standards(tmp_path)
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined
    assert "0 declared standard(s)" in combined
    assert "DRIFT:" not in combined


def test_standard_runner_executes_catalog_surfaces_without_redispatch(tmp_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    _write_marketplace(tmp_path, [])
    implementation = tmp_path / ".agents/standards/root-gitignore-hygiene"
    implementation.mkdir(parents=True)
    resource = implementation / "scripts/scaffold_gitignore.py"
    resource.parent.mkdir(parents=True)
    resource.write_bytes((SCRIPTS / "scaffold_gitignore.py").read_bytes())
    contract = tmp_path / ".agents/contracts/operating-standards.json"
    contract.parent.mkdir(parents=True, exist_ok=True)
    contract.write_text(
        json.dumps(
            {
                "version": 1,
                "standards": [
                    {
                        "id": "root-gitignore-hygiene",
                        "origin": "marketplace",
                        "revision": "d" * 40,
                        "implementation_root": ".agents/standards/root-gitignore-hygiene",
                        "check": [
                            "@python",
                            ".agents/standards/_runtime/repo_standards.py",
                            "--run-standard",
                            "root-gitignore-hygiene",
                            "--check",
                        ],
                        "apply": [
                            "@python",
                            ".agents/standards/_runtime/repo_standards.py",
                            "--run-standard",
                            "root-gitignore-hygiene",
                            "--apply",
                            "--yes",
                        ],
                        "generated_paths": [],
                        "requires": [],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / ".gitignore").write_text("", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "repo_standards.py"), "--run-standard", "root-gitignore-hygiene", "--check"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined
    assert "DRIFT:" not in combined


def test_composition_runner_executes_repo_owned_standard_without_plugins(tmp_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    _write_marketplace(tmp_path, [])
    implementation = tmp_path / ".agents/standards/repo-lint"
    implementation.mkdir(parents=True)
    marker = tmp_path / "repo-lint.marker"
    checker = implementation / "check.py"
    checker.write_text(f"from pathlib import Path; Path({str(marker)!r}).write_text('checked')\n", encoding="utf-8")
    contract = tmp_path / ".agents/contracts/operating-standards.json"
    contract.parent.mkdir(parents=True, exist_ok=True)
    contract.write_text(
        json.dumps(
            {
                "version": 1,
                "standards": [
                    {
                        "id": "repo-lint",
                        "origin": "repository",
                        "implementation_root": ".agents/standards/repo-lint",
                        "check": ["@python", ".agents/standards/repo-lint/check.py"],
                        "apply": ["@python", ".agents/standards/repo-lint/check.py"],
                        "generated_paths": [],
                        "requires": [],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    result = _run_standards(tmp_path)
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined
    assert marker.read_text(encoding="utf-8") == "checked"
    assert "1 declared standard(s)" in combined
