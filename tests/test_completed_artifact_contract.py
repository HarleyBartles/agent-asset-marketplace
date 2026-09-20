from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts"
sys.path.insert(0, str(SCRIPTS))
from completed_artifact_contract import check_completed_artifact_doctrine  # noqa: E402


def test_current_doctrine_passes() -> None:
    path = ROOT / "codex-marketplace/plugins/agent-operating-model/skills/repo-shape/templates/completed-artifacts.md"
    assert check_completed_artifact_doctrine(path) == []


def test_rejected_candidate_does_not_complete_brief(tmp_path: Path) -> None:
    path = tmp_path / "completed-artifacts.md"
    path.write_text(
        "## Scope\naccepted work\n## Doctrine\n"
        "A rejected candidate completes its brief. successor completed-awaiting-retirement git history\n"
        "## Ownership\nowner\n",
        encoding="utf-8",
    )
    assert any(item.code == "invalid-completion-trigger" for item in check_completed_artifact_doctrine(path))
