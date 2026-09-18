import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ROOT / "codex-marketplace" / "plugins"
EXPECTED_SKILLS = {
    "command-bus",
    "python",
    "repo-agent-assets",
    "repo-composition",
    "repo-shape",
    "repo-standards",
    "repository-validation",
    "tracked-repo-hooks",
}


def _bundle_entries(plugin: str) -> set[str]:
    manifest = json.loads((PLUGINS / plugin / "references" / "bundle-manifest.json").read_text(encoding="utf-8"))
    return {entry["canonical_name"] for entry in manifest["entries"]}


def test_agent_operating_model_owns_expected_skills_once() -> None:
    assert _bundle_entries("agent-operating-model") == EXPECTED_SKILLS
    assert "repo-standards" not in _bundle_entries("repo-worker-pack")
    assert "python" not in _bundle_entries("language-patterns-pack")


def test_repo_standards_router_names_every_focused_owner() -> None:
    text = (PLUGINS / "agent-operating-model" / "skills" / "repo-standards" / "SKILL.md").read_text(encoding="utf-8")
    for skill in EXPECTED_SKILLS - {"repo-standards"}:
        assert f"`{skill}`" in text


def test_repo_standards_compatibility_entrypoint_delegates_to_repo_shape() -> None:
    wrapper = PLUGINS / "agent-operating-model" / "skills" / "repo-standards" / "scripts" / "repo_standards.py"
    text = wrapper.read_text(encoding="utf-8")
    assert '"repo-shape" / "scripts" / "repo_standards.py"' in text
