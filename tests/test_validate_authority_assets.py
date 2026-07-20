from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import validate_authority_assets as validator  # noqa: E402


def write_authority_fixture(root: Path, *, lane: str) -> Path:
    skill = root / "skill"
    authority = skill / "assets/authority"
    authority.mkdir(parents=True)
    (authority / "authority.yaml").write_text(
        "schema_version: 1\n"
        f"lane: {lane}\n"
        "authority:\n"
        "  title: Example Authority\n"
        "  canonical_url: https://example.com/authority\n"
        "  pinned_source_url: https://example.com/authority/v1\n"
        "  latest_check_url: https://example.com/authority\n"
        "  revision: v1\n"
        "  retrieved_at: '2026-07-20'\n"
        "  content_sha256: example-hash\n"
        "  license: CC-BY-4.0\n"
        "  license_url: https://creativecommons.org/licenses/by/4.0/\n"
        "decomposition:\n"
        "  reconciled_against: v1\n"
        "  references:\n"
        "    - path: references/example.md\n"
        "      source_sections: [Example]\n"
        "      content_mode: first_party_synthesis\n"
        "      load_when: [example topic]\n",
        encoding="utf-8",
        newline="\n",
    )
    (authority / "source-map.yaml").write_text(
        "schema_version: 1\n"
        "reconciled_against: v1\n"
        "references:\n"
        "  - path: references/example.md\n"
        "    source_sections: [Example]\n"
        "    content_mode: first_party_synthesis\n"
        "    load_when: [example topic]\n",
        encoding="utf-8",
        newline="\n",
    )
    (authority / "CITATIONS.md").write_text(
        "# Citations\n\n## Human review\n", encoding="utf-8", newline="\n"
    )
    return skill


def test_source_lane_requires_reference_source(tmp_path: Path):
    skill = write_authority_fixture(tmp_path, lane="skills-with-source")
    errors = validator.validate_authority_skill(skill)
    assert any("reference-source" in error for error in errors)


def test_citation_lane_rejects_vendored_source(tmp_path: Path):
    skill = write_authority_fixture(tmp_path, lane="skills-with-citation")
    (skill / "assets/authority/reference-source").mkdir(parents=True)
    (skill / "assets/authority/reference-source/source.pdf").write_bytes(b"source")
    errors = validator.validate_authority_skill(skill)
    assert any("must not contain" in error for error in errors)


def test_empty_authority_mapping_fails_schema_validation(tmp_path: Path):
    skill = write_authority_fixture(tmp_path, lane="skills-with-citation")
    (skill / "assets/authority/authority.yaml").write_text("{}\n", encoding="utf-8", newline="\n")
    errors = validator.validate_authority_skill(skill)
    assert any("schema_version" in error for error in errors)


def test_valid_source_and_citation_lanes_pass(tmp_path: Path):
    source_skill = write_authority_fixture(tmp_path / "source", lane="skills-with-source")
    (source_skill / "assets/authority/reference-source").mkdir(parents=True)
    (source_skill / "assets/authority/reference-source/source.txt").write_text(
        "approved source", encoding="utf-8", newline="\n"
    )
    citation_skill = write_authority_fixture(tmp_path / "citation", lane="skills-with-citation")
    assert validator.validate_authority_skill(source_skill) == []
    assert validator.validate_authority_skill(citation_skill) == []
