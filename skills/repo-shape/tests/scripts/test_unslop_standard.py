from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[4]
SCRIPT = ROOT / "skills/repo-shape/scripts/unslop_standard.py"
SCHEMA = ROOT / "skills/repo-shape/references/unslop-contract.schema.json"
CATALOG = ROOT / "skills/repo-shape/references/operating-standards-catalog.json"
MANIFEST = ROOT / "skills/repo-shape/references/repository-shape-manifest.json"


def _module():
    spec = importlib.util.spec_from_file_location("unslop_standard_under_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _repo(root: Path) -> None:
    subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Unslop fixture"], cwd=root, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "unslop-fixture@example.invalid"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    doctrine = root / ".agents/doctrine/marketplace-worker-doctrine.md"
    doctrine.parent.mkdir(parents=True, exist_ok=True)
    doctrine.write_text("# Marketplace worker doctrine\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", ".agents/doctrine/marketplace-worker-doctrine.md"],
        cwd=root,
        check=True,
        capture_output=True,
    )


def _contract(root: Path, roots: list[str] | None = None) -> Path:
    path = root / ".agents/contracts/unslop.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"version": 1, "profile_roots": [".agents/unslop"] if roots is None else roots}
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _workflow(
    root: Path,
    path: str = ".agents/runbooks/planning.md",
    *,
    routed: bool = True,
    route_text: str | None = None,
) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    guidance = route_text or (
        "Use $unslop-profiles to find and apply the relevant profile during planning." if routed else "Plan the work."
    )
    target.write_text(f"# Planning\n\n## Unslop profile routing\n\n{guidance}\n", encoding="utf-8")
    subprocess.run(["git", "add", path], cwd=root, check=True, capture_output=True)


def _profile(
    root: Path,
    *,
    name: str = "repository.md",
    profile_id: str = "specific-claims",
    workflow: str = "../runbooks/planning.md",
    reference: str = "../doctrine/marketplace-worker-doctrine.md",
    missing_section: str | None = None,
) -> Path:
    headings = {
        "Task trigger and scope": "Use during implementation planning when describing the intended change.",
        "Recurring failure pattern": "Plans promise validation without naming executable evidence.",
        "Recognition cues": "The plan uses the phrase robust validation without a concrete command or evidence target.",
        "Corrective behavior": "Name the command, expected observation, and the decision it supports.",
        "False-positive and override boundaries": (
            "Keep the phrase when quoting an existing requirement or when it has a precise defined meaning."
        ),
        "Applicable workflow paths": f"- [Planning runbook]({workflow})",
        "Doctrine and skill references": f"- [Marketplace worker doctrine]({reference})",
        "Application example": (
            "In a plan, replace an unsupported 'robust validation' claim with the exact check and expected result."
        ),
    }
    if missing_section:
        del headings[missing_section]
    body = [f"# Unslop Profile: {profile_id}", ""]
    for heading, content in headings.items():
        body.extend([f"## {heading}", "", content, ""])
    path = root / ".agents/unslop" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body), encoding="utf-8")
    return path


def test_default_and_additional_profile_roots_allow_empty_and_absent_directories(tmp_path: Path) -> None:
    _repo(tmp_path)
    _contract(tmp_path, [".agents/unslop", "packages/ui/.agents/unslop", "docs/profiles"])
    (tmp_path / ".agents/unslop").mkdir(parents=True)

    assert _module().validate(tmp_path) == []


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ("not json", "cannot be read"),
        ('{"version":2,"profile_roots":[".agents/unslop"]}', "version"),
        ('{"version":1,"profile_roots":["C:/profiles"]}', "repository-relative"),
        ('{"version":1,"profile_roots":["../profiles"]}', "repository-relative"),
        ('{"version":1,"profile_roots":[".agents/unslop",".agents/unslop"]}', "duplicate"),
        ('{"version":1,"profile_roots":[]}', "profile_roots"),
    ],
)
def test_contract_rejects_malformed_or_unsafe_roots(tmp_path: Path, payload: str, message: str) -> None:
    _repo(tmp_path)
    path = tmp_path / ".agents/contracts/unslop.json"
    path.parent.mkdir(parents=True)
    path.write_text(payload, encoding="utf-8")

    assert any(message in finding.lower() for finding in _module().validate(tmp_path))


def test_declared_profile_root_must_be_a_directory_when_present(tmp_path: Path) -> None:
    _repo(tmp_path)
    _contract(tmp_path, ["profiles"])
    (tmp_path / "profiles").write_text("not a directory", encoding="utf-8")

    assert any("not a directory" in finding.lower() for finding in _module().validate(tmp_path))


def test_duplicate_profile_ids_are_rejected_across_declared_roots(tmp_path: Path) -> None:
    _repo(tmp_path)
    _contract(tmp_path, [".agents/unslop", "team/profiles"])
    _workflow(tmp_path)
    _profile(tmp_path)
    second = _profile(tmp_path, name="team.md")
    target = tmp_path / "team/profiles/team.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    second.rename(target)

    assert any("duplicate profile id" in finding.lower() for finding in _module().validate(tmp_path))


def test_nested_profile_roots_do_not_scan_the_same_file_twice(tmp_path: Path) -> None:
    _repo(tmp_path)
    _contract(tmp_path, [".agents/unslop", ".agents/unslop/team"])
    _workflow(tmp_path)
    _profile(tmp_path)
    _profile(
        tmp_path,
        name="team/team.md",
        profile_id="team-pattern",
        workflow="../../runbooks/planning.md",
        reference="../../doctrine/marketplace-worker-doctrine.md",
    )

    assert _module().validate(tmp_path) == []


def test_profile_requires_operational_sections(tmp_path: Path) -> None:
    _repo(tmp_path)
    _contract(tmp_path)
    _workflow(tmp_path)
    _profile(tmp_path, missing_section="Corrective behavior")

    assert any("corrective behavior" in finding.lower() for finding in _module().validate(tmp_path))


def test_profile_title_must_be_its_first_heading(tmp_path: Path) -> None:
    _repo(tmp_path)
    _contract(tmp_path)
    _workflow(tmp_path)
    profile = _profile(tmp_path)
    text = profile.read_text(encoding="utf-8")
    text = text.replace("# Unslop Profile: specific-claims", "# Notes\n\n# Unslop Profile: specific-claims", 1)
    profile.write_text(text, encoding="utf-8")

    assert any("first heading" in finding.lower() for finding in _module().validate(tmp_path))


@pytest.mark.parametrize("broken", ["../doctrine/missing.md", "file:///outside/policy.md", "javascript:alert(1)"])
def test_profile_rejects_broken_local_references(tmp_path: Path, broken: str) -> None:
    _repo(tmp_path)
    _contract(tmp_path)
    _workflow(tmp_path)
    _profile(tmp_path, reference=broken)

    assert any("reference" in finding.lower() or "link" in finding.lower() for finding in _module().validate(tmp_path))


def test_profile_allows_external_http_authority_reference(tmp_path: Path) -> None:
    _repo(tmp_path)
    _contract(tmp_path)
    _workflow(tmp_path)
    _profile(tmp_path, reference="https://example.invalid/authoritative-policy")

    assert _module().validate(tmp_path) == []


def test_profile_resolves_angle_bracketed_local_reference_with_spaces_and_parentheses(tmp_path: Path) -> None:
    _repo(tmp_path)
    _contract(tmp_path)
    _workflow(tmp_path)
    doctrine = tmp_path / ".agents/doctrine/team policy (draft).md"
    doctrine.write_text("# Team policy\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", ".agents/doctrine/team policy (draft).md"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    _profile(tmp_path, reference="<../doctrine/team policy (draft).md>")

    assert _module().validate(tmp_path) == []


@pytest.mark.parametrize(
    ("filename", "reference"),
    [
        ("policy(draft).md", "../doctrine/policy(draft).md"),
        ("policy(draft).md", r"../doctrine/policy\(draft\).md"),
    ],
)
def test_profile_resolves_bare_local_references_with_parentheses(tmp_path: Path, filename: str, reference: str) -> None:
    _repo(tmp_path)
    _contract(tmp_path)
    _workflow(tmp_path)
    doctrine = tmp_path / ".agents/doctrine" / filename
    doctrine.write_text("# Team policy\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", f".agents/doctrine/{filename}"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    _profile(tmp_path, reference=reference)

    assert _module().validate(tmp_path) == []


def test_profile_rejects_missing_workflow_and_workflow_without_profile_route(tmp_path: Path) -> None:
    _repo(tmp_path)
    _contract(tmp_path)
    _workflow(tmp_path, routed=False)
    _profile(tmp_path)

    findings = _module().validate(tmp_path)
    assert any("unslop-profiles" in finding.lower() for finding in findings)

    _profile(tmp_path, workflow="../runbooks/missing.md")
    findings = _module().validate(tmp_path)
    assert any("workflow" in finding.lower() for finding in findings)


@pytest.mark.parametrize(
    "route_text",
    [
        "Do not use $unslop-profiles for this stage.",
        "Do not ever use $unslop-profiles for this stage.",
        "Never, under any circumstances, use $unslop-profiles here.",
        "When planning, cannot use $unslop-profiles.",
        "When doing anything, use $unslop-profiles.",
        "When planning any task, use $unslop-profiles.",
        "Use $unslop-profiles for every task.",
    ],
)
def test_profile_route_requires_an_affirmative_scoped_action(tmp_path: Path, route_text: str) -> None:
    _repo(tmp_path)
    _contract(tmp_path)
    _workflow(tmp_path, route_text=route_text)
    _profile(tmp_path)

    findings = _module().validate(tmp_path)
    assert any("route" in finding.lower() or "unslop-profiles" in finding.lower() for finding in findings)


def test_valid_profile_can_repeat_its_cue_in_an_intentional_example_without_plugin_installation(tmp_path: Path) -> None:
    _repo(tmp_path)
    _contract(tmp_path)
    _workflow(tmp_path)
    profile = _profile(tmp_path)
    content = profile.read_text(encoding="utf-8")
    assert "robust validation" in content.split("## Recognition cues", 1)[1].split("## ", 1)[0]
    assert "robust validation" in content.split("## Application example", 1)[1]

    assert not (tmp_path / ".agents/plugins/marketplace.json").exists()
    assert _module().validate(tmp_path) == []


def test_apply_creates_only_the_missing_default_adoption_contract(tmp_path: Path) -> None:
    _repo(tmp_path)
    module = _module()

    assert module.apply(tmp_path) == []
    contract = tmp_path / ".agents/contracts/unslop.json"
    assert json.loads(contract.read_text(encoding="utf-8")) == {"version": 1, "profile_roots": [".agents/unslop"]}
    assert not (tmp_path / ".agents/unslop").exists()
    before = contract.read_bytes()
    assert module.apply(tmp_path) == []
    assert contract.read_bytes() == before


def test_standard_resources_and_explicit_migration_policy_are_catalogued() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    standard = next(item for item in catalog["standards"] if item["id"] == "unslop")
    assert standard["legacy_migration"] == "explicit"
    assert set(standard["resources"]) >= {
        "skills/repo-shape/references/unslop-standard.md",
        "skills/repo-shape/references/unslop-contract.schema.json",
        "skills/repo-shape/scripts/unslop_standard.py",
    }
    assert standard["requires"] == []
    assert "unslop-plus" not in json.dumps(standard)
    surface_manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert any(surface["id"] == "unslop-contract" for surface in surface_manifest["surfaces"])
    assert SCHEMA.is_file()
