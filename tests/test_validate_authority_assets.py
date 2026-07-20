from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import validate_authority_assets as validator  # noqa: E402


def write_authority_fixture(root: Path, *, lane: str, skill_name: str = "skill") -> Path:
    skill = root / skill_name
    authority = skill / "assets/authority"
    authority.mkdir(parents=True)
    (authority / "authority.yaml").write_text(
        "schema_version: 1\n"
        "custody: marketplace\n"
        f"lane: {lane}\n"
        "authority:\n"
        "  title: Example Authority\n"
        "  canonical_url: https://example.com/authority\n"
        "  pinned_source_url: https://example.com/authority/v1\n"
        "  latest_check_url: https://example.com/authority\n"
        "  revision: v1\n"
        "  retrieved_at: '2026-07-20'\n"
        "  content_sha256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"
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
    reference = skill / "references/example.md"
    reference.parent.mkdir(parents=True)
    reference.write_text("# Example\n", encoding="utf-8", newline="\n")
    (authority / "CITATIONS.md").write_text(
        "# Citations\n\n"
        "## Scholarly citation\n\nExample Authority (2026).\n\n"
        "## Derivation boundary\n\nOperational guidance is a clean-room synthesis.\n\n"
        "## Attribution\n\nAttribution retained under CC-BY-4.0.\n\n"
        "## Human review\n\nReviewed and approved on 2026-07-20.\n",
        encoding="utf-8",
        newline="\n",
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


def test_source_map_must_be_valid_yaml_mapping_with_schema(tmp_path: Path):
    skill = write_authority_fixture(tmp_path, lane="skills-with-citation")
    (skill / "assets/authority/source-map.yaml").write_text("- not-a-mapping\n", encoding="utf-8", newline="\n")
    errors = validator.validate_authority_skill(skill)
    assert any("source-map.yaml must contain a YAML mapping" in error for error in errors)


def test_source_map_must_match_authority_decomposition(tmp_path: Path):
    skill = write_authority_fixture(tmp_path, lane="skills-with-citation")
    (skill / "assets/authority/source-map.yaml").write_text(
        "schema_version: 1\n"
        "reconciled_against: v2\n"
        "references: []\n",
        encoding="utf-8",
        newline="\n",
    )
    errors = validator.validate_authority_skill(skill)
    assert any("reconciled_against must match" in error for error in errors)
    assert any("references must match" in error for error in errors)


def test_citation_lane_requires_first_party_synthesis_in_both_records(tmp_path: Path):
    skill = write_authority_fixture(tmp_path, lane="skills-with-citation")
    authority_path = skill / "assets/authority/authority.yaml"
    authority_path.write_text(
        authority_path.read_text(encoding="utf-8").replace("first_party_synthesis", "licensed_adaptation"),
        encoding="utf-8",
        newline="\n",
    )
    source_map_path = skill / "assets/authority/source-map.yaml"
    source_map_path.write_text(
        source_map_path.read_text(encoding="utf-8").replace("first_party_synthesis", "verbatim_source"),
        encoding="utf-8",
        newline="\n",
    )
    errors = validator.validate_authority_skill(skill)
    assert sum("must use first_party_synthesis" in error for error in errors) == 2


def test_discovery_reports_authority_directory_missing_authority_yaml(tmp_path: Path, capsys):
    marketplace_authority = tmp_path / "sources/first_party/skills/example/assets/authority"
    local_authority = tmp_path / ".agents/skills/mark-example/assets/authority"
    for authority_root in (marketplace_authority, local_authority):
        authority_root.mkdir(parents=True)
        (authority_root / "CITATIONS.md").write_text("# Citations\n", encoding="utf-8", newline="\n")

    assert validator.validate_authority_assets(tmp_path) == 1
    output = capsys.readouterr().out
    assert str(marketplace_authority.parent.parent) in output
    assert str(local_authority.parent.parent) in output
    assert output.count("missing authority.yaml") == 2


def test_authority_requires_typed_nonblank_values_safe_references_and_real_citations(tmp_path: Path):
    skill = write_authority_fixture(tmp_path, lane="skills-with-citation")
    authority_path = skill / "assets/authority/authority.yaml"
    authority_path.write_text(
        authority_path.read_text(encoding="utf-8")
        .replace("title: Example Authority", "title: ''")
        .replace("content_sha256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "content_sha256: not-a-sha")
        .replace("retrieved_at: '2026-07-20'", "retrieved_at: invalid-date")
        .replace("path: references/example.md", "path: ../escape.md")
        .replace("source_sections: [Example]", "source_sections: []"),
        encoding="utf-8",
        newline="\n",
    )
    source_map_path = skill / "assets/authority/source-map.yaml"
    source_map_path.write_text(
        source_map_path.read_text(encoding="utf-8")
        .replace("path: references/example.md", "path: ../escape.md")
        .replace("source_sections: [Example]", "source_sections: []"),
        encoding="utf-8",
        newline="\n",
    )
    (skill / "assets/authority/CITATIONS.md").write_text(
        "# Citations\n\n"
        "## Scholarly citation\n\nTODO\n\n"
        "## Derivation boundary\n\nState what operational guidance was derived.\n\n"
        "## Attribution\n\nRecord required attribution here.\n\n"
        "## Human review\n\nRecord the reviewer here.\n",
        encoding="utf-8",
        newline="\n",
    )

    errors = validator.validate_authority_skill(skill)
    assert any("title must be a nonblank string" in error for error in errors)
    assert any("content_sha256 must be a 64-character lowercase SHA-256" in error for error in errors)
    assert any("retrieved_at must be an ISO-8601 date" in error for error in errors)
    assert sum("path must name an existing file under references/" in error for error in errors) == 2
    assert sum("source_sections must be a nonempty list of nonblank strings" in error for error in errors) == 2
    assert any("CITATIONS.md scholarly citation section must contain non-placeholder content" in error for error in errors)
    assert any("CITATIONS.md derivation boundary section must contain non-placeholder content" in error for error in errors)
    assert any("CITATIONS.md attribution section must contain non-placeholder content" in error for error in errors)
    assert any("CITATIONS.md human review section must contain non-placeholder content" in error for error in errors)


def test_authority_rejects_duplicate_yaml_keys_and_non_utf8_content(tmp_path: Path):
    skill = write_authority_fixture(tmp_path, lane="skills-with-citation")
    authority_path = skill / "assets/authority/authority.yaml"
    authority_path.write_text(
        authority_path.read_text(encoding="utf-8") + "lane: skills-with-citation\n",
        encoding="utf-8",
        newline="\n",
    )
    (skill / "assets/authority/source-map.yaml").write_bytes(b"\xff\xfe")

    errors = validator.validate_authority_skill(skill)
    assert any("duplicate key" in error for error in errors)
    assert any("source-map.yaml cannot be read as YAML" in error for error in errors)


def test_authority_returns_errors_for_container_values_without_traceback(tmp_path: Path):
    skill = write_authority_fixture(tmp_path, lane="skills-with-citation")
    authority_path = skill / "assets/authority/authority.yaml"
    authority_path.write_text(
        authority_path.read_text(encoding="utf-8")
        .replace("schema_version: 1", "schema_version: [1]")
        .replace("lane: skills-with-citation", "lane: [skills-with-citation]")
        .replace("content_mode: first_party_synthesis", "content_mode: [first_party_synthesis]"),
        encoding="utf-8",
        newline="\n",
    )
    source_map_path = skill / "assets/authority/source-map.yaml"
    source_map_path.write_text(
        source_map_path.read_text(encoding="utf-8")
        .replace("schema_version: 1", "schema_version: [1]")
        .replace("content_mode: first_party_synthesis", "content_mode: [first_party_synthesis]"),
        encoding="utf-8",
        newline="\n",
    )

    errors = validator.validate_authority_skill(skill)

    assert any("authority.yaml must declare schema_version: 1" in error for error in errors)
    assert any("authority.yaml lane must be one of" in error for error in errors)
    assert any("source-map.yaml must declare schema_version: 1" in error for error in errors)
    assert sum("has unsupported content_mode" in error for error in errors) == 2


def test_authority_rejects_non_string_or_unhashable_mapping_keys(tmp_path: Path):
    skill = write_authority_fixture(tmp_path, lane="skills-with-citation")
    (skill / "assets/authority/authority.yaml").write_text(
        "? [unexpected, key]\n: value\n",
        encoding="utf-8",
        newline="\n",
    )

    errors = validator.validate_authority_skill(skill)

    assert any("cannot be read as YAML" in error for error in errors)


def test_local_mark_skill_authority_assets_are_rejected(tmp_path: Path):
    skill = write_authority_fixture(
        tmp_path / ".agents/skills", lane="skills-with-citation", skill_name="mark-example"
    )

    errors = validator.validate_authority_skill(skill)

    assert any("local mark-* skills must not contain authority assets" in error for error in errors)


def test_authority_records_require_marketplace_custody(tmp_path: Path):
    skill = write_authority_fixture(tmp_path, lane="skills-with-citation")
    authority_path = skill / "assets/authority/authority.yaml"
    authority_path.write_text(
        authority_path.read_text(encoding="utf-8").replace("custody: marketplace", "custody: local"),
        encoding="utf-8",
        newline="\n",
    )

    errors = validator.validate_authority_skill(skill)

    assert any("authority.yaml must declare custody: marketplace" in error for error in errors)


def test_valid_source_and_citation_lanes_pass(tmp_path: Path):
    source_skill = write_authority_fixture(tmp_path / "source", lane="skills-with-source")
    (source_skill / "assets/authority/reference-source").mkdir(parents=True)
    (source_skill / "assets/authority/reference-source/source.txt").write_text(
        "approved source", encoding="utf-8", newline="\n"
    )
    citation_skill = write_authority_fixture(tmp_path / "citation", lane="skills-with-citation")
    assert validator.validate_authority_skill(source_skill) == []
    assert validator.validate_authority_skill(citation_skill) == []
