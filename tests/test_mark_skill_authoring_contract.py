from pathlib import Path
import sys

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".agents" / "skills" / "mark-skill-authoring" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import new_skill  # noqa: E402
import normalize_first_party_skill_sources as normalize  # noqa: E402


def test_local_request_requires_mark_prefix():
    with pytest.raises(ValueError, match="local custody requires the mark- prefix"):
        new_skill.validate_request("ddd", "local", "first_party")


def test_marketplace_request_rejects_mark_prefix():
    with pytest.raises(ValueError, match="marketplace custody cannot use the mark- prefix"):
        new_skill.validate_request("mark-ddd", "marketplace", "skills-with-source")


def test_local_request_requires_first_party_lane():
    with pytest.raises(ValueError, match="local custody requires the first_party lane"):
        new_skill.validate_request("mark-example", "local", "skills-with-source")


def test_render_scaffold_uses_lane_specific_authority_shape():
    source_files = new_skill.render_scaffold("ddd", "marketplace", "skills-with-source")
    citation_files = new_skill.render_scaffold("owasp", "marketplace", "skills-with-citation")
    assert "assets/authority/authority.yaml" in source_files
    assert "assets/authority/CITATIONS.md" in source_files
    assert "assets/authority/reference-source/.gitkeep" in source_files
    assert "assets/authority/reference-source/.gitkeep" not in citation_files


def test_rendered_authority_record_has_required_decomposition_keys():
    files = new_skill.render_scaffold("ddd", "marketplace", "skills-with-source")
    authority = files["assets/authority/authority.yaml"]
    assert "decomposition:" in authority
    assert "  reconciled_against:" in authority
    assert "  references:" in authority


def test_rendered_files_are_lf_terminated():
    files = new_skill.render_scaffold("ddd", "marketplace", "skills-with-source")
    assert all(content.endswith("\n") for content in files.values())


def test_yaml_sensitive_name_remains_a_string_in_rendered_yaml():
    files = new_skill.render_scaffold("true", "marketplace", "first_party")
    frontmatter = yaml.safe_load(files["SKILL.md"].split("---", 2)[1])
    authority = yaml.safe_load(files["assets/authority/authority.yaml"])
    source_map = yaml.safe_load(files["assets/authority/source-map.yaml"])

    assert frontmatter["name"] == "true"
    assert isinstance(frontmatter["name"], str)
    assert authority["authority"]["title"] == "true"
    assert isinstance(authority["authority"]["title"], str)
    assert source_map["authority"]["title"] == "true"
    assert isinstance(source_map["authority"]["title"], str)


def test_scaffold_check_does_not_write(tmp_path: Path):
    assert new_skill.scaffold(tmp_path, "mark-example", "local", "first_party", check=True) == 0
    assert not (tmp_path / ".agents/skills/mark-example").exists()


def test_local_guidance_routes_to_mark_skill_authoring():
    standards = (ROOT / "docs/skill-standards-policy.md").read_text(encoding="utf-8")
    guide = (ROOT / ".agents/guides/skill-authoring-guide.md").read_text(encoding="utf-8")
    assert "mark-skill-authoring" in standards
    assert "mark-skill-authoring" in guide
    assert "authoring-skills" not in standards
    assert "authoring-skills" not in guide


def test_first_party_normalizer_preserves_use_with(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    skill_md = tmp_path / "sample" / "SKILL.md"
    skill_md.parent.mkdir(parents=True)
    monkeypatch.setattr(normalize, "ROOT", tmp_path)
    skill_md.write_text(
        "---\n"
        "name: sample\n"
        "description: Use when testing metadata preservation.\n"
        "metadata:\n"
        "  source-id: sample\n"
        "  source-path: sample/SKILL.md\n"
        "  provenance-name: Sample first-party skill\n"
        "  source-category: first_party\n"
        "  status: active\n"
        "  owner: Harley Bartles\n"
        "  scope: metadata test\n"
        "  use_when:\n"
        "    - Use when testing metadata preservation.\n"
        "  do_not_use_when:\n"
        "    - Do not use when the test is unrelated.\n"
        "  use_with:\n"
        "    - superpowers-plus:writing-skills\n"
        "license: MIT\n"
        "---\n\n# Sample\n",
        encoding="utf-8",
    )
    assert normalize._normalize_skill(skill_md, write=False) is False
