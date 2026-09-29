from pathlib import Path
import sys
import json

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "skills/repo-shape/scripts"
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


def test_legacy_ambient_skill_name_does_not_claim_runtime_availability(tmp_path: Path) -> None:
    _write_playbook(tmp_path, "- `missing-skill` - required.")
    assert check_skill_links(tmp_path) == []


def test_declared_repo_local_skill_must_exist(tmp_path: Path) -> None:
    marketplace = tmp_path / ".agents/plugins/marketplace.json"
    marketplace.parent.mkdir(parents=True)
    marketplace.write_text(json.dumps({"repo": {"local_skills": ["missing-local"]}}), encoding="utf-8")
    findings = check_skill_links(tmp_path)
    assert any(item.code == "missing-repo-local-skill" for item in findings)


def test_declared_repo_local_skill_frontmatter_must_match(tmp_path: Path) -> None:
    marketplace = tmp_path / ".agents/plugins/marketplace.json"
    marketplace.parent.mkdir(parents=True)
    marketplace.write_text(json.dumps({"repo": {"local_skills": ["local-skill"]}}), encoding="utf-8")
    skill = tmp_path / ".agents/skills/local-skill"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: wrong-name\n---\n", encoding="utf-8")
    findings = check_skill_links(tmp_path)
    assert any(item.code == "repo-local-skill-name-mismatch" for item in findings)


def test_ambient_skill_is_not_valid_repository_owned_skill(tmp_path: Path) -> None:
    path = _write_playbook(tmp_path, "None.")
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "## Composition",
        "## Required repository-owned skills\n\n- `repo-worker-base`\n\n## Composition",
    )
    path.write_text(text, encoding="utf-8")
    ambient = tmp_path / ".agents/skills/repo-worker-base"
    ambient.mkdir(parents=True)
    (ambient / "SKILL.md").write_text("---\nname: repo-worker-base\n---\n", encoding="utf-8")

    findings = check_skill_links(tmp_path)

    assert any(item.code == "non-local-repository-skill" for item in findings)


def test_repository_owned_skill_resolves_through_local_skill_custody(tmp_path: Path) -> None:
    path = _write_playbook(tmp_path, "None.")
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "## Composition",
        "## Required repository-owned skills\n\n- `rooms-domain-review`\n\n## Composition",
    )
    path.write_text(text, encoding="utf-8")
    skill = tmp_path / ".agents/skills/rooms-domain-review"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: rooms-domain-review\n---\n", encoding="utf-8")
    marketplace = tmp_path / ".agents/plugins/marketplace.json"
    marketplace.parent.mkdir(parents=True, exist_ok=True)
    marketplace.write_text(json.dumps({"repo": {"local_skills": ["rooms-domain-review"]}}), encoding="utf-8")

    assert check_skill_links(tmp_path) == []


def test_capability_contract_does_not_need_provider_name(tmp_path: Path) -> None:
    path = tmp_path / ".agents/playbooks/testing.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "# Testing\n\n## Required capabilities\n\n- Drive focused verification.\n\n"
        "## Optional capabilities\n\nNone.\n\n## Required repository-owned skills\n\nNone.\n\n"
        "## Optional repository-owned skills\n\nNone.\n\n## Composition\n\nUse an available suitable skill.\n",
        encoding="utf-8",
    )
    assert check_skill_links(tmp_path) == []
