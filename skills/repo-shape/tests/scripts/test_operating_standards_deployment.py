from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "skills/repo-shape/scripts"
sys.path.insert(0, str(SCRIPTS))

import deploy_operating_standards  # noqa: E402
import migrate_operating_standards  # noqa: E402
import operating_standards_catalog  # noqa: E402

CATALOG_PATH = ROOT / "skills/repo-shape/references/operating-standards-catalog.json"
MANIFEST_PATH = ROOT / "skills/repo-shape/references/repository-shape-manifest.json"
CATALOG = operating_standards_catalog.load_catalog(CATALOG_PATH, MANIFEST_PATH, ROOT)
STANDARD_ID = "root-gitignore-hygiene"


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def _source_fixture(root: Path, standard_id: str = STANDARD_ID) -> tuple[Path, str]:
    source = root / ".agents/plugins/marketplace-source"
    resources = set(deploy_operating_standards.RUNTIME_RESOURCES)
    resources.update(deploy_operating_standards.RUNTIME_REFERENCES)
    standard = next(item for item in CATALOG.standards if item.id == standard_id)
    resources.update(standard.resources)
    for resource in resources:
        source_file = ROOT / resource
        target = source / resource
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target)
    _git(source, "init")
    _git(source, "config", "user.name", "Deployment Fixture")
    _git(source, "config", "user.email", "deployment-fixture@example.invalid")
    _git(source, "add", ".")
    _git(source, "commit", "-m", "source fixture")
    return source, _git(source, "rev-parse", "HEAD")


def _entry(revision: str, standard_id: str = STANDARD_ID) -> dict[str, object]:
    standard = next(item for item in CATALOG.standards if item.id == standard_id)
    return {
        "id": standard_id,
        "origin": "marketplace",
        "revision": revision,
        "implementation_root": f".agents/standards/{standard_id}",
        "check": [
            "@python",
            ".agents/standards/_runtime/repo_standards.py",
            "--run-standard",
            standard_id,
            "--check",
        ],
        "apply": [
            "@python",
            ".agents/standards/_runtime/repo_standards.py",
            "--run-standard",
            standard_id,
            "--apply",
            "--yes",
            "@allow-shared-checkout",
        ],
        "generated_paths": [],
        "requires": list(standard.requires),
    }


def _consumer(root: Path, revision: str) -> Path:
    contract = root / ".agents/contracts/operating-standards.json"
    contract.parent.mkdir(parents=True, exist_ok=True)
    contract.write_text(json.dumps({"version": 1, "standards": [_entry(revision)]}), encoding="utf-8")
    return contract


def test_deployment_check_is_read_only_and_apply_copies_only_selected_resources(tmp_path: Path) -> None:
    source, revision = _source_fixture(tmp_path)
    contract = _consumer(tmp_path, revision)
    empty_skills = tmp_path / ".agents/skills"
    empty_skills.mkdir(parents=True)

    findings = deploy_operating_standards.deploy(tmp_path, source, CATALOG, apply=False)

    assert findings
    assert not (tmp_path / ".agents/standards").exists()
    assert deploy_operating_standards.deploy(tmp_path, source, CATALOG, apply=True) == []
    deployed = tmp_path / f".agents/standards/{STANDARD_ID}/scripts/scaffold_gitignore.py"
    assert deployed.read_bytes() == (source / "skills/repo-shape/scripts/scaffold_gitignore.py").read_bytes()
    assert not (tmp_path / ".agents/standards/runbook-composition").exists()
    assert empty_skills.is_dir()
    assert contract.is_file()

    provenance = json.loads((tmp_path / ".agents/standards/provenance.json").read_text(encoding="utf-8"))
    entry = provenance["resources"][f".agents/standards/{STANDARD_ID}/scripts/scaffold_gitignore.py"]
    assert entry["sha256"] == hashlib.sha256(deployed.read_bytes()).hexdigest()
    assert entry["source"] == "skills/repo-shape/scripts/scaffold_gitignore.py"
    assert provenance["revision"] == revision


def test_deployment_refuses_revision_mismatch_and_unowned_overwrite(tmp_path: Path) -> None:
    source, revision = _source_fixture(tmp_path)
    _consumer(tmp_path, "f" * 40)
    with pytest.raises(ValueError, match="does not match pinned source revision"):
        deploy_operating_standards.deploy(tmp_path, source, CATALOG, apply=True)

    _consumer(tmp_path, revision)
    conflict = tmp_path / f".agents/standards/{STANDARD_ID}/scripts/scaffold_gitignore.py"
    conflict.parent.mkdir(parents=True)
    conflict.write_text("consumer-owned collision\n", encoding="utf-8")
    with pytest.raises(ValueError, match="ambiguous existing file"):
        deploy_operating_standards.deploy(tmp_path, source, CATALOG, apply=True)


def test_deployment_check_refuses_escaped_implementation_root(tmp_path: Path) -> None:
    source, revision = _source_fixture(tmp_path)
    contract = _consumer(tmp_path, revision)
    data = json.loads(contract.read_text(encoding="utf-8"))
    data["standards"][0]["implementation_root"] = "../outside"
    contract.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="repository-relative"):
        deploy_operating_standards.deploy(tmp_path, source, CATALOG, apply=False)


def test_noop_redeployment_preserves_composition_and_deployed_provenance(tmp_path: Path) -> None:
    source, revision = _source_fixture(tmp_path)
    contract = _consumer(tmp_path, revision)
    deploy_operating_standards.deploy(tmp_path, source, CATALOG, apply=True)
    provenance = tmp_path / ".agents/standards/provenance.json"
    deployed_file = tmp_path / f".agents/standards/{STANDARD_ID}/scripts/scaffold_gitignore.py"
    before = (contract.read_bytes(), provenance.read_bytes(), deployed_file.read_bytes())

    assert deploy_operating_standards.deploy(tmp_path, source, CATALOG, apply=True) == []
    assert (contract.read_bytes(), provenance.read_bytes(), deployed_file.read_bytes()) == before


def test_deployed_runner_checks_selected_standard_without_ambient_projection(tmp_path: Path) -> None:
    source, revision = _source_fixture(tmp_path)
    _consumer(tmp_path, revision)
    deploy_operating_standards.deploy(tmp_path, source, CATALOG, apply=True)
    (tmp_path / ".gitignore").write_text("", encoding="utf-8")
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    runtime = tmp_path / ".agents/standards/_runtime/repo_standards.py"

    result = subprocess.run([sys.executable, str(runtime), "--check"], cwd=tmp_path, capture_output=True, text=True)

    assert result.returncode == 0, result.stdout + result.stderr
    assert not (tmp_path / ".agents/skills").exists()
    assert not (tmp_path / ".agents/plugins/marketplace.json").exists()


def test_legacy_prepare_deploys_before_migration_activation(tmp_path: Path) -> None:
    source, revision = _source_fixture(tmp_path)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    selected_surfaces = {
        surface_id for standard in CATALOG.standards if standard.id == STANDARD_ID for surface_id in standard.surfaces
    }
    exceptions = [
        {"id": surface["id"], "reason": "migration fixture"}
        for surface in manifest["surfaces"]
        if surface["id"] not in selected_surfaces
    ]
    legacy = tmp_path / ".agents/contracts/agent-operating-model.json"
    legacy.parent.mkdir(parents=True, exist_ok=True)
    legacy.write_text(json.dumps({"version": 1, "surface_exceptions": exceptions}), encoding="utf-8")
    hook = tmp_path / "githooks/pre-commit"
    hook.parent.mkdir(parents=True)
    hook.write_text("legacy hook\n", encoding="utf-8")
    legacy_before, hook_before = legacy.read_bytes(), hook.read_bytes()

    assert deploy_operating_standards.deploy(tmp_path, source, CATALOG, apply=True, prepare_migration=True) == []
    assert not (tmp_path / ".agents/contracts/operating-standards.json").exists()
    assert legacy.read_bytes() == legacy_before
    assert hook.read_bytes() == hook_before

    migrate_operating_standards.migrate_contract(tmp_path, CATALOG, revision, apply=True)
    assert deploy_operating_standards.deploy(tmp_path, source, CATALOG, apply=False) == []


def test_empty_marketplace_selection_deploys_no_runtime_or_provenance(tmp_path: Path) -> None:
    source, _ = _source_fixture(tmp_path)
    contract = tmp_path / ".agents/contracts/operating-standards.json"
    contract.parent.mkdir(parents=True)
    contract.write_text('{"version":1,"standards":[]}\n', encoding="utf-8")

    assert deploy_operating_standards.deploy(tmp_path, source, CATALOG, apply=True) == []
    assert not (tmp_path / ".agents/standards/_runtime").exists()
    assert not (tmp_path / ".agents/standards/provenance.json").exists()


def test_deployment_refuses_modified_worktree_resource_at_pinned_revision(tmp_path: Path) -> None:
    source, revision = _source_fixture(tmp_path)
    _consumer(tmp_path, revision)
    changed = source / "skills/repo-shape/scripts/scaffold_gitignore.py"
    changed.write_text(changed.read_text(encoding="utf-8") + "# local mutation\n", encoding="utf-8")

    with pytest.raises(ValueError, match="uncommitted changes"):
        deploy_operating_standards.deploy(tmp_path, source, CATALOG, apply=True)

    assert not (tmp_path / ".agents/standards").exists()


def test_runbook_standard_dispatch_validates_its_selected_composition_graph(tmp_path: Path) -> None:
    standard_id = "runbook-composition"
    source, revision = _source_fixture(tmp_path, standard_id)
    _git(tmp_path, "init", "-b", "codex/runbook-standard")
    _consumer(tmp_path, revision)
    contract = tmp_path / ".agents/contracts/operating-standards.json"
    contract.write_text(json.dumps({"version": 1, "standards": [_entry(revision, standard_id)]}), encoding="utf-8")
    deploy_operating_standards.deploy(tmp_path, source, CATALOG, apply=True)

    runtime = tmp_path / ".agents/standards/_runtime/repo_standards.py"
    apply_result = subprocess.run(
        [
            sys.executable,
            str(runtime),
            "--run-standard",
            standard_id,
            "--apply",
            "--yes",
            "--allow-shared-checkout",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert apply_result.returncode == 0, apply_result.stdout + apply_result.stderr
    runbooks = tmp_path / ".agents/runbooks"
    implementing = runbooks / "implementing.md"
    section = "## Playbook routing\n\nNone."
    implementing.write_text(
        implementing.read_text(encoding="utf-8").replace(
            section, "## Playbook routing\n\n- [Missing](../playbooks/missing.md)"
        ),
        encoding="utf-8",
    )
    (tmp_path / ".agents/plugins/marketplace.json").unlink(missing_ok=True)

    result = subprocess.run(
        [sys.executable, str(runtime), "--run-standard", standard_id, "--check"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "playbook target does not resolve" in result.stdout + result.stderr
