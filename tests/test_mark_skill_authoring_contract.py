from pathlib import Path
import sys
from unittest.mock import patch

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
    first_party_files = new_skill.render_scaffold("ddd", "marketplace", "first_party")
    source_files = new_skill.render_scaffold("ddd", "marketplace", "skills-with-source")
    citation_files = new_skill.render_scaffold("owasp", "marketplace", "skills-with-citation")
    assert set(first_party_files) == {"SKILL.md", "references/.gitkeep"}
    assert "assets/authority/authority.yaml" in source_files
    assert "assets/authority/CITATIONS.md" in source_files
    assert "assets/authority/reference-source/.gitkeep" in source_files
    assert "assets/authority/reference-source/.gitkeep" not in citation_files


def test_rendered_authority_record_has_required_decomposition_keys():
    files = new_skill.render_scaffold("ddd", "marketplace", "skills-with-source")
    authority = files["assets/authority/authority.yaml"]
    assert "custody: marketplace" in authority
    assert "decomposition:" in authority
    assert "  reconciled_against:" in authority
    assert "  references:" in authority


def test_rendered_source_map_uses_decomposition_projection_schema():
    files = new_skill.render_scaffold("ddd", "marketplace", "skills-with-source")
    source_map = yaml.safe_load(files["assets/authority/source-map.yaml"])
    assert source_map == {
        "schema_version": 1,
        "reconciled_against": "TODO",
        "references": [],
    }


def test_rendered_files_are_lf_terminated():
    files = new_skill.render_scaffold("ddd", "marketplace", "skills-with-source")
    assert all(content.endswith("\n") for content in files.values())


def test_marketplace_first_party_scaffold_is_normalization_stable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    skill_root = tmp_path / "sources/first_party/skills/example"
    skill_root.mkdir(parents=True)
    files = new_skill.render_scaffold("example", "marketplace", "first_party")
    for relative_path, content in files.items():
        output = skill_root / relative_path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8", newline="\n")

    monkeypatch.setattr(normalize, "ROOT", tmp_path)
    assert normalize._normalize_skill(skill_root / "SKILL.md", write=False) is False


def test_scaffold_rolls_back_created_destination_when_a_later_write_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    destination = tmp_path / "sources/first_party/skills/example"
    files = new_skill.render_scaffold("example", "marketplace", "skills-with-citation")
    real_open = Path.open

    def fail_on_source_map(self: Path, *args, **kwargs):
        if self.name == "source-map.yaml":
            raise OSError("injected write failure")
        return real_open(self, *args, **kwargs)

    monkeypatch.setattr(new_skill, "_guard_write_checkout", lambda root, allow: root)
    monkeypatch.setattr(new_skill, "render_scaffold", lambda *args: files)
    monkeypatch.setattr(Path, "open", fail_on_source_map)

    with pytest.raises(OSError, match="injected write failure"):
        new_skill.scaffold(tmp_path, "example", "marketplace", "skills-with-citation", check=False)

    assert not destination.exists()
    assert not destination.parent.exists()


def test_yaml_sensitive_name_remains_a_string_in_rendered_yaml():
    files = new_skill.render_scaffold("true", "marketplace", "skills-with-source")
    frontmatter = yaml.safe_load(files["SKILL.md"].split("---", 2)[1])
    authority = yaml.safe_load(files["assets/authority/authority.yaml"])
    source_map = yaml.safe_load(files["assets/authority/source-map.yaml"])

    assert frontmatter["name"] == "true"
    assert isinstance(frontmatter["name"], str)
    assert authority["authority"]["title"] == "true"
    assert isinstance(authority["authority"]["title"], str)
    assert source_map["reconciled_against"] == "TODO"


def test_scaffold_check_does_not_write(tmp_path: Path):
    assert new_skill.scaffold(tmp_path, "mark-example", "local", "first_party", check=True) == 0
    assert not (tmp_path / ".agents/skills/mark-example").exists()


def test_cli_check_resolves_git_top_level_from_nested_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    repo_root = tmp_path / "repo"
    nested = repo_root / "nested" / "directory"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)

    with (
        patch.object(new_skill, "_git", return_value=str(repo_root)),
        patch.object(sys, "argv", [
            "new_skill.py", "--name", "mark-example", "--custody", "local", "--lane", "first_party", "--check"
        ]),
        patch("builtins.print") as printed,
    ):
        assert new_skill.main() == 0

    printed.assert_any_call(repo_root / ".agents/skills/mark-example/SKILL.md")


def test_bash_wrapper_prefers_python3_and_falls_back_to_py_launcher():
    wrapper = (SCRIPTS / "new-skill.sh").read_text(encoding="utf-8")
    assert "command -v python3" in wrapper
    assert 'exec python3 "$script_dir/new_skill.py" "$@"' in wrapper
    assert 'exec py -3 "$script_dir/new_skill.py" "$@"' in wrapper


def test_local_guidance_routes_to_mark_skill_authoring():
    standards = (ROOT / "docs/skill-standards-policy.md").read_text(encoding="utf-8")
    guide = (ROOT / ".agents/guides/skill-authoring-guide.md").read_text(encoding="utf-8")
    assert "mark-skill-authoring" in standards
    assert "mark-skill-authoring" in guide
    assert "authoring-skills" not in standards
    assert "authoring-skills" not in guide


def test_authoring_skill_scaffolds_only_new_skills_and_inspects_existing_ones():
    skill = (ROOT / ".agents/skills/mark-skill-authoring/SKILL.md").read_text(encoding="utf-8")

    assert "For creating a new skill, run" in skill
    assert "reviewing or refreshing an existing skill, inspect its existing custody and lane" in skill


def test_authoring_docs_describe_installed_writing_skills_projection_and_handoff_floor():
    standards = (ROOT / "docs/skill-standards-policy.md").read_text(encoding="utf-8")
    design_guide = (ROOT / ".agents/guides/design-guide.md").read_text(encoding="utf-8")
    source_guidance = (ROOT / ".agents/skills/mark-skill-authoring/references/source-grounded-authoring.md").read_text(encoding="utf-8")
    custody_guidance = (ROOT / ".agents/skills/mark-skill-authoring/references/local-and-marketplace-custody.md").read_text(encoding="utf-8")

    assert "superpowers-plus:writing-skills" in standards
    assert "superpowers:writing-skills" in standards
    assert "upstream origin" in standards
    assert "below `9/10`" in design_guide
    for phrase in (
        "first_party",
        "skills-with-source",
        "skills-with-citation",
        "source_sections",
        "load_when",
        "legal redistribution approval",
        "reference-source",
        "clean-room synthesis",
        "CITATIONS.md",
        "manual freshness review",
        "No inline citations",
    ):
        assert phrase in source_guidance or phrase in custody_guidance


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
