import importlib.util
import sys
from pathlib import Path
import pytest


REPO_ROOT = Path(__file__).resolve().parents[4]

SKILL_ROOT = REPO_ROOT / "skills" / "repo-shape" / "scripts"

REPO_STANDARDS = SKILL_ROOT / "repo_standards.py"

SCAFFOLD_MARKDOWN_FORMATTING = SKILL_ROOT / "scaffold_markdown_formatting.py"

sys.path.insert(0, str(SKILL_ROOT))

_SPEC = importlib.util.spec_from_file_location("repo_standards_under_test", REPO_STANDARDS)

repo_standards = importlib.util.module_from_spec(_SPEC)


_SPEC.loader.exec_module(repo_standards)


_MARKDOWN_SPEC = importlib.util.spec_from_file_location(
    "scaffold_markdown_formatting_under_test", SCAFFOLD_MARKDOWN_FORMATTING
)

scaffold_markdown_formatting = importlib.util.module_from_spec(_MARKDOWN_SPEC)


_MARKDOWN_SPEC.loader.exec_module(scaffold_markdown_formatting)


def test_scaffold_runbooks_stub_is_stage_composition_root(tmp_path: Path) -> None:
    spec = importlib.util.spec_from_file_location("scaffold_runbooks_under_test", SKILL_ROOT / "scaffold_runbooks.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    content = mod._runbook_content("implementing.md")
    for heading in (
        "## When",
        "## Required skills",
        "## Composition",
        "## Doctrine and contracts",
        "## Local commands and paths",
        "## Evidence contract",
        "## Prohibited combinations",
        "## Playbook routing",
    ):
        assert heading in content
    assert "completing-plans.md" not in mod.RUNBOOK_TITLES


def test_scaffold_playbooks_stub_is_topical_composition(tmp_path: Path) -> None:
    spec = importlib.util.spec_from_file_location("scaffold_playbooks_under_test", SKILL_ROOT / "scaffold_playbooks.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    content = mod._playbook_content("testing.md")
    for heading in (
        "## When",
        "## Required skills",
        "## Composition",
        "## Doctrine and contracts",
        "## Local commands and paths",
        "## Evidence contract",
        "## Prohibited combinations",
        "## Runbook routing",
    ):
        assert heading in content
    assert "testing.md" in mod.PLAYBOOK_TITLES


def _composition_document(extra_heading: str, links: str = "") -> str:
    headings = (
        "When",
        "Required skills",
        "Composition",
        "Doctrine and contracts",
        "Local commands and paths",
        "Evidence contract",
        "Prohibited combinations",
    )
    body = "# Example\n\n" + "\n\n".join(f"## {heading}\n\n- defined" for heading in headings)
    return body + f"\n\n## {extra_heading}\n\n{links}\n"


def test_runbook_composition_reports_missing_required_sections(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "testing.md").write_text("# Testing\n\nLocal commands only.\n", encoding="utf-8")
    findings = repo_standards._check_composition_graph(tmp_path)
    assert any("testing.md" in finding and "Required skills" in finding for finding in findings)


def test_composition_graph_accepts_reciprocal_playbook_route(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    playbooks = tmp_path / ".agents" / "playbooks"
    runbooks.mkdir(parents=True)
    playbooks.mkdir(parents=True)
    (runbooks / "implementing.md").write_text(
        _composition_document("Playbook routing", "- [Testing](../playbooks/testing.md) - when tests change."),
        encoding="utf-8",
    )
    (playbooks / "testing.md").write_text(
        _composition_document("Runbook routing", "- [Implementation](../runbooks/implementing.md)"),
        encoding="utf-8",
    )
    assert repo_standards._check_composition_graph(tmp_path) == []


def test_composition_graph_accepts_standalone_playbook(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    playbooks = tmp_path / ".agents" / "playbooks"
    runbooks.mkdir(parents=True)
    playbooks.mkdir(parents=True)
    (runbooks / "implementing.md").write_text(_composition_document("Playbook routing", "None."), encoding="utf-8")
    (playbooks / "testing.md").write_text(_composition_document("Runbook routing", "None."), encoding="utf-8")
    assert repo_standards._check_composition_graph(tmp_path) == []


def test_composition_graph_rejects_nonreciprocal_edge(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    playbooks = tmp_path / ".agents" / "playbooks"
    runbooks.mkdir(parents=True)
    playbooks.mkdir(parents=True)
    (runbooks / "implementing.md").write_text(
        _composition_document("Playbook routing", "- [Testing](../playbooks/testing.md)"), encoding="utf-8"
    )
    (playbooks / "testing.md").write_text(
        _composition_document("Runbook routing", "- [Review](../runbooks/code-review.md)"), encoding="utf-8"
    )
    findings = repo_standards._check_composition_graph(tmp_path)
    assert any("reciprocal" in finding for finding in findings)


def test_composition_graph_accepts_playbook_to_playbook_composition(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    playbooks = tmp_path / ".agents" / "playbooks"
    runbooks.mkdir(parents=True)
    playbooks.mkdir(parents=True)
    routing = "- [Testing](../playbooks/testing.md)\n- [Security](../playbooks/security.md)"
    (runbooks / "implementing.md").write_text(_composition_document("Playbook routing", routing), encoding="utf-8")
    (playbooks / "testing.md").write_text(
        _composition_document("Runbook routing", "- [Implementation](../runbooks/implementing.md)").replace(
            "## Composition\n\n- defined",
            "## Composition\n\n- [Security](security.md)",
        ),
        encoding="utf-8",
    )
    (playbooks / "security.md").write_text(
        _composition_document("Runbook routing", "- [Implementation](../runbooks/implementing.md)"),
        encoding="utf-8",
    )
    assert repo_standards._check_composition_graph(tmp_path) == []


def test_composition_graph_rejects_missing_playbook_composition_target(tmp_path: Path) -> None:
    playbooks = tmp_path / ".agents" / "playbooks"
    playbooks.mkdir(parents=True)
    (playbooks / "testing.md").write_text(
        _composition_document("Runbook routing", "None.").replace(
            "## Composition\n\n- defined",
            "## Composition\n\n- [Security](security.md)",
        ),
        encoding="utf-8",
    )

    findings = repo_standards._check_composition_graph(tmp_path)
    assert any("security.md" in finding and "does not resolve" in finding for finding in findings)


def test_composition_graph_rejects_playbook_composition_cycle(tmp_path: Path) -> None:
    playbooks = tmp_path / ".agents" / "playbooks"
    playbooks.mkdir(parents=True)
    (playbooks / "testing.md").write_text(
        _composition_document("Runbook routing", "None.").replace(
            "## Composition\n\n- defined",
            "## Composition\n\n- [Security](security.md)",
        ),
        encoding="utf-8",
    )
    (playbooks / "security.md").write_text(
        _composition_document("Runbook routing", "None.").replace(
            "## Composition\n\n- defined",
            "## Composition\n\n- [Testing](testing.md)",
        ),
        encoding="utf-8",
    )

    findings = repo_standards._check_composition_graph(tmp_path)
    assert any("composition cycle" in finding and "testing.md" in finding for finding in findings)


def test_composition_graph_ignores_playbook_links_outside_composition(tmp_path: Path) -> None:
    playbooks = tmp_path / ".agents" / "playbooks"
    playbooks.mkdir(parents=True)
    (playbooks / "testing.md").write_text(
        _composition_document("Runbook routing", "None.").replace(
            "## Doctrine and contracts\n\n- defined",
            "## Doctrine and contracts\n\n- [Security](security.md)",
        ),
        encoding="utf-8",
    )
    (playbooks / "security.md").write_text(
        _composition_document("Runbook routing", "None.").replace(
            "## Doctrine and contracts\n\n- defined",
            "## Doctrine and contracts\n\n- [Testing](testing.md)",
        ),
        encoding="utf-8",
    )

    assert repo_standards._check_composition_graph(tmp_path) == []


def test_apply_fails_when_composition_graph_remains_invalid(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "implementing.md").write_text("# Implementation\n", encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text('{"version": 3, "surfaces": []}\n', encoding="utf-8")
    monkeypatch.setattr(repo_standards, "_repo_root", lambda: tmp_path)
    monkeypatch.setattr(repo_standards, "_manifest_path", lambda: manifest)
    monkeypatch.setattr(repo_standards, "_is_submodule", lambda _root: False)
    monkeypatch.setattr(repo_standards.shared_checkout, "approve_mutation", lambda *_args: True)

    assert repo_standards.main(["--apply", "--yes"]) == 1
    captured = capsys.readouterr()
    assert "apply did not converge" in captured.err


def test_runbook_composition_ignores_agents_md_and_absent_dir(tmp_path: Path) -> None:
    assert repo_standards._check_composition_graph(tmp_path) == []
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "AGENTS.md").write_text("# Router\n", encoding="utf-8")
    assert repo_standards._check_composition_graph(tmp_path) == []


def test_runbook_composition_works_without_generated_index(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "implementing.md").write_text(
        "# Implementing\n\n"
        "## When\n\nUse it.\n\n"
        "## Required skills\n\nNone.\n\n"
        "## Composition\n\nCompose it.\n\n"
        "## Doctrine and contracts\n\nRead doctrine.\n\n"
        "## Local commands and paths\n\nRun commands.\n\n"
        "## Evidence contract\n\nRecord evidence.\n\n"
        "## Prohibited combinations\n\nNone.\n\n"
        "## Playbook routing\n\nNone.\n",
        encoding="utf-8",
    )
    assert repo_standards._check_composition_graph(tmp_path) == []


def test_runbook_composition_warns_on_fenced_heading(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "testing.md").write_text("# Testing\n\n```markdown\n## Required skills\n```\n", encoding="utf-8")
    findings = repo_standards._check_composition_graph(tmp_path)
    assert any("testing.md" in finding for finding in findings)


def test_runbook_composition_warns_on_commented_heading(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "testing.md").write_text("# Testing\n\n<!-- ## Required skills -->\n", encoding="utf-8")
    findings = repo_standards._check_composition_graph(tmp_path)
    assert any("testing.md" in finding for finding in findings)


def test_runbook_composition_warns_on_extended_heading(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "testing.md").write_text("# Testing\n\n## Required skills for maintainers\n", encoding="utf-8")
    findings = repo_standards._check_composition_graph(tmp_path)
    assert any("testing.md" in finding for finding in findings)


def test_scaffold_pr_template_carries_composition_sections() -> None:
    spec = importlib.util.spec_from_file_location("scaffold_runbooks_pr_test", SKILL_ROOT / "scaffold_runbooks.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    content = mod._runbook_content("pr.md")
    for heading in (
        "## When",
        "## Required skills",
        "## Composition",
        "## Doctrine and contracts",
        "## Local commands and paths",
        "## Evidence contract",
        "## Prohibited combinations",
    ):
        assert heading in content
