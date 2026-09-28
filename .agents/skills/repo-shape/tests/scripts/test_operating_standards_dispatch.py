from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "skills/repo-shape/scripts"
sys.path.insert(0, str(SCRIPTS))

import operating_standards_catalog  # noqa: E402
import operating_standards_dispatch  # noqa: E402

CATALOG = operating_standards_catalog.load_catalog(
    ROOT / "skills/repo-shape/references/operating-standards-catalog.json",
    ROOT / "skills/repo-shape/references/repository-shape-manifest.json",
    ROOT,
)
REVISION = "c" * 40


def _entry(root: Path, standard_id: str, *, origin: str = "repository", requires=None) -> dict:
    implementation = root / ".agents/standards" / standard_id
    implementation.mkdir(parents=True, exist_ok=True)
    script = implementation / "mark.py"
    script.write_text(
        f"from pathlib import Path\nPath({str(root / (standard_id + '.marker'))!r}).write_text('ran')\n",
        encoding="utf-8",
    )
    entry = {
        "id": standard_id,
        "origin": origin,
        "implementation_root": implementation.relative_to(root).as_posix(),
        "check": ["@python", f".agents/standards/{standard_id}/mark.py"],
        "apply": ["@python", f".agents/standards/{standard_id}/mark.py"],
        "generated_paths": [],
        "requires": requires or [],
    }
    if origin == "marketplace":
        entry["revision"] = REVISION
    return entry


def test_dispatch_runs_only_two_selected_standards_and_omits_the_third(tmp_path: Path) -> None:
    entries = [_entry(tmp_path, name) for name in ("alpha", "beta", "gamma")]
    declaration = {"version": 1, "standards": entries[:2]}
    (tmp_path / ".agents/contracts").mkdir(parents=True)
    path = tmp_path / ".agents/contracts/operating-standards.json"
    path.write_text(json.dumps(declaration), encoding="utf-8")

    result = operating_standards_dispatch.dispatch(tmp_path, CATALOG, path, mode="check")

    assert result == ["alpha", "beta"]
    assert (tmp_path / "alpha.marker").exists()
    assert (tmp_path / "beta.marker").exists()
    assert not (tmp_path / "gamma.marker").exists()


def test_empty_selection_runs_no_marketplace_checks(tmp_path: Path) -> None:
    path = tmp_path / ".agents/contracts/operating-standards.json"
    path.parent.mkdir(parents=True)
    path.write_text('{"version":1,"standards":[]}\n', encoding="utf-8")

    assert operating_standards_dispatch.dispatch(tmp_path, CATALOG, path, mode="check") == []


def test_repository_owned_standard_runs_without_plugin_subscription(tmp_path: Path) -> None:
    entry = _entry(tmp_path, "repo-lint")
    contract = tmp_path / ".agents/contracts/operating-standards.json"
    contract.parent.mkdir(parents=True)
    contract.write_text(json.dumps({"version": 1, "standards": [entry]}), encoding="utf-8")
    # An explicitly empty plugin subscription has no bearing on the declared checker.
    plugins = tmp_path / ".agents/plugins/marketplace.json"
    plugins.parent.mkdir(parents=True)
    plugins.write_text('{"plugins":[]}\n', encoding="utf-8")

    assert operating_standards_dispatch.dispatch(tmp_path, CATALOG, contract, mode="check") == ["repo-lint"]
    assert (tmp_path / "repo-lint.marker").exists()


def test_invalid_dependency_fails_before_any_selected_command_runs(tmp_path: Path) -> None:
    second = _entry(tmp_path, "markdown-formatting", origin="marketplace")
    second["requires"] = ["root-agent-router"]
    # Catalog says markdown-formatting has no dependency, but the explicit graph still
    # requires that root-agent-router be selected with it.
    contract = tmp_path / ".agents/contracts/operating-standards.json"
    contract.parent.mkdir(parents=True)
    contract.write_text(json.dumps({"version": 1, "standards": [second]}), encoding="utf-8")

    with pytest.raises(ValueError, match="unknown required standard"):
        operating_standards_dispatch.dispatch(tmp_path, CATALOG, contract, mode="check")

    assert not (tmp_path / "markdown-formatting.marker").exists()


def test_apply_runs_only_selected_apply_vectors(tmp_path: Path) -> None:
    selected = _entry(tmp_path, "repo-deploy")
    _entry(tmp_path, "repo-skip")
    contract = tmp_path / ".agents/contracts/operating-standards.json"
    contract.parent.mkdir(parents=True)
    contract.write_text(json.dumps({"version": 1, "standards": [selected]}), encoding="utf-8")

    assert operating_standards_dispatch.dispatch(tmp_path, CATALOG, contract, mode="apply") == ["repo-deploy"]
    assert (tmp_path / "repo-deploy.marker").exists()
    assert not (tmp_path / "repo-skip.marker").exists()


def test_single_standard_dispatch_includes_declared_dependencies_first(tmp_path: Path) -> None:
    dependency = _entry(tmp_path, "root-agent-router", origin="marketplace")
    target = _entry(tmp_path, "markdown-formatting", origin="marketplace", requires=["root-agent-router"])
    # Give the dependency checker a visible execution order.
    dependency_script = tmp_path / dependency["implementation_root"] / "mark.py"
    target_script = tmp_path / target["implementation_root"] / "mark.py"
    dependency_script.write_text(f"open({str(tmp_path / 'order.marker')!r}, 'a').write('dep\\n')\n", encoding="utf-8")
    target_script.write_text(
        f"from pathlib import Path; p=Path({str(tmp_path / 'order.marker')!r}); "
        "p.write_text((p.read_text() if p.exists() else '')+'target\\n')\n",
        encoding="utf-8",
    )
    contract = tmp_path / ".agents/contracts/operating-standards.json"
    contract.parent.mkdir(parents=True)
    contract.write_text(json.dumps({"version": 1, "standards": [dependency, target]}), encoding="utf-8")

    completed = operating_standards_dispatch.dispatch(
        tmp_path, CATALOG, contract, mode="check", standard_id="markdown-formatting"
    )

    assert completed == ["root-agent-router", "markdown-formatting"]
    assert (tmp_path / "order.marker").read_text(encoding="utf-8").splitlines() == ["dep", "target"]


def test_unavailable_later_command_fails_preflight_before_first_marker(tmp_path: Path) -> None:
    first = _entry(tmp_path, "repo-first")
    second = _entry(tmp_path, "repo-second")
    second["check"] = ["codex_missing_executable_for_test"]
    contract = tmp_path / ".agents/contracts/operating-standards.json"
    contract.parent.mkdir(parents=True)
    contract.write_text(json.dumps({"version": 1, "standards": [first, second]}), encoding="utf-8")

    with pytest.raises(ValueError, match="command executable is unavailable"):
        operating_standards_dispatch.dispatch(tmp_path, CATALOG, contract, mode="check")

    assert not (tmp_path / "repo-first.marker").exists()
