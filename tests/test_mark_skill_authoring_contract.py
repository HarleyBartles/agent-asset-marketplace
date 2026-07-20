from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".agents" / "skills" / "mark-skill-authoring" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import new_skill  # noqa: E402


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


def test_scaffold_check_does_not_write(tmp_path: Path):
    assert new_skill.scaffold(tmp_path, "mark-example", "local", "first_party", check=True) == 0
    assert not (tmp_path / ".agents/skills/mark-example").exists()
