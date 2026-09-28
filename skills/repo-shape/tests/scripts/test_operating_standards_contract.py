from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "skills/repo-shape/scripts"
sys.path.insert(0, str(SCRIPTS))

import operating_standards_catalog  # noqa: E402
import scaffold_operating_standards  # noqa: E402

CATALOG_PATH = ROOT / "skills/repo-shape/references/operating-standards-catalog.json"
MANIFEST_PATH = ROOT / "skills/repo-shape/references/repository-shape-manifest.json"
CATALOG = operating_standards_catalog.load_catalog(CATALOG_PATH, MANIFEST_PATH, ROOT)
REVISION = "a" * 40


def _entry(
    standard_id: str,
    *,
    origin: str = "marketplace",
    requires: list[str] | None = None,
) -> dict[str, object]:
    entry: dict[str, object] = {
        "id": standard_id,
        "origin": origin,
        "implementation_root": f".agents/standards/{standard_id}",
        "check": ["@python", f".agents/standards/{standard_id}/check.py", "--check"],
        "apply": ["@python", f".agents/standards/{standard_id}/check.py", "--apply"],
        "generated_paths": [],
        "requires": requires or [],
    }
    if origin == "marketplace":
        entry["revision"] = REVISION
    return entry


def _contract(*entries: dict[str, object]) -> dict[str, object]:
    return {"version": 1, "standards": list(entries)}


def test_empty_and_repository_owned_compositions_are_explicit_and_valid(tmp_path: Path) -> None:
    operating_standards_catalog.validate_composition(_contract(), CATALOG)
    operating_standards_catalog.validate_composition(_contract(_entry("repo-lint", origin="repository")), CATALOG)


def test_mixed_composition_can_select_two_catalog_standards_and_omit_another() -> None:
    selected = _contract(
        _entry("root-agent-router"),
        _entry("markdown-formatting"),
    )

    operating_standards_catalog.validate_composition(selected, CATALOG)
    assert {entry["id"] for entry in selected["standards"]} == {"root-agent-router", "markdown-formatting"}


def test_catalog_dependencies_must_be_explicit_in_the_composition() -> None:
    standards = list(CATALOG.standards)
    index = next(i for i, item in enumerate(standards) if item.id == "markdown-formatting")
    standards[index] = replace(standards[index], requires=("root-agent-router",))
    dependent_catalog = replace(CATALOG, standards=tuple(standards))

    with pytest.raises(ValueError, match="missing required standard"):
        operating_standards_catalog.validate_composition(_contract(_entry("markdown-formatting")), dependent_catalog)

    operating_standards_catalog.validate_composition(
        _contract(_entry("root-agent-router"), _entry("markdown-formatting", requires=["root-agent-router"])),
        dependent_catalog,
    )


def test_composition_rejects_unknown_and_duplicate_standard_ids() -> None:
    with pytest.raises(ValueError, match="unknown standard"):
        operating_standards_catalog.validate_composition(_contract(_entry("missing-standard")), CATALOG)

    with pytest.raises(ValueError, match="duplicate standard id"):
        operating_standards_catalog.validate_composition(
            _contract(_entry("root-agent-router"), _entry("root-agent-router")), CATALOG
        )


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda entry: entry.update(check=[]), "check command"),
        (lambda entry: entry.update(apply="python run.py"), "apply command"),
        (lambda entry: entry.update(implementation_root="../outside"), "repository-relative"),
        (lambda entry: entry.update(generated_paths=["../outside/**"]), "repository-relative"),
        (lambda entry: entry.update(requires=["unknown-standard"]), "unknown required standard"),
        (lambda entry: entry.update(revision="main"), "revision must be a pinned commit"),
    ],
)
def test_composition_rejects_invalid_commands_paths_dependencies_and_revisions(mutation, message: str) -> None:
    entry = _entry("root-agent-router")
    mutation(entry)
    with pytest.raises(ValueError, match=message):
        operating_standards_catalog.validate_composition(_contract(entry), CATALOG)


def test_repository_owned_entry_cannot_claim_marketplace_revision() -> None:
    entry = _entry("repo-lint", origin="repository")
    entry["revision"] = REVISION
    with pytest.raises(ValueError, match="repository-owned standard cannot set revision"):
        operating_standards_catalog.validate_composition(_contract(entry), CATALOG)


def test_scaffold_requires_explicit_apply_and_creates_an_empty_contract(tmp_path: Path) -> None:
    target = tmp_path / ".agents/contracts/operating-standards.json"
    findings = scaffold_operating_standards.scaffold_contract(tmp_path, CATALOG, apply=False)
    assert findings
    assert not target.exists()

    assert scaffold_operating_standards.scaffold_contract(tmp_path, CATALOG, apply=True) == []
    assert json.loads(target.read_text(encoding="utf-8")) == {"version": 1, "standards": []}


def test_scaffold_does_not_overwrite_an_invalid_consumer_contract(tmp_path: Path) -> None:
    target = tmp_path / ".agents/contracts/operating-standards.json"
    target.parent.mkdir(parents=True)
    target.write_text('{"version": 9, "standards": []}\n', encoding="utf-8")
    before = target.read_bytes()

    assert scaffold_operating_standards.scaffold_contract(tmp_path, CATALOG, apply=True)
    assert target.read_bytes() == before
