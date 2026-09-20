from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts"
sys.path.insert(0, str(SCRIPTS))
from skill_link_contract import check_skill_links  # noqa: E402


def _write_playbook(root: Path, required: str) -> Path:
    path = root / ".agents/playbooks/testing.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        f"# Testing\n\n## Required skills\n\n{required}\n\n## Composition\n\nUse the workflow.\n", encoding="utf-8"
    )
    return path


def test_installed_skill_reference_resolves_from_visible_namespace(tmp_path: Path) -> None:
    skill = tmp_path / ".agents/skills/test-driven-development"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: test-driven-development\n---\n", encoding="utf-8")
    assert check_skill_links(tmp_path) == []


def test_dead_skill_link_names_document_and_skill(tmp_path: Path) -> None:
    path = _write_playbook(tmp_path, "- `missing-skill` — required.")
    finding = check_skill_links(tmp_path)[0]
    assert finding.surface == path.relative_to(tmp_path).as_posix()
    assert "missing-skill" in finding.message
