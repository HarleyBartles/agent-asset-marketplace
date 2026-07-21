import hashlib
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import validate_authority_assets as validator  # noqa: E402


CITATIONS_TEXT = (
    "# Citations\n\n"
    "## Scholarly citation\n\nExample Authority (2026).\n\n"
    "## Derivation boundary\n\nOperational guidance is a clean-room synthesis.\n\n"
    "## Attribution\n\nAttribution retained under CC-BY-4.0.\n\n"
    "## Human review\n\nReviewed and approved on 2026-07-20.\n"
)


def write_authority_fixture(
    root: Path,
    *,
    lane: str,
    skill_name: str = "skill",
    source_content: str | None = None,
) -> Path:
    skill = root / skill_name
    authority = skill / "assets/authority"
    authority.mkdir(parents=True)
    citations_path = authority / "CITATIONS.md"
    citations_path.write_text(CITATIONS_TEXT, encoding="utf-8", newline="\n")
    citations_hash = validator._compute_file_sha256(citations_path)

    evidence_hash = citations_hash
    if lane == "skills-with-source" and source_content is not None:
        ref_source = authority / "reference-source"
        ref_source.mkdir(parents=True)
        source_file = ref_source / "source.txt"
        source_file.write_text(source_content, encoding="utf-8", newline="\n")
        evidence_hash = validator._compute_file_sha256(source_file)

    authority_yaml = (
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
        f"  content_sha256: {evidence_hash}\n"
        "  license: CC-BY-4.0\n"
        "  license_url: https://creativecommons.org/licenses/by/4.0/\n"
        "decomposition:\n"
        f"  reconciled_against: {evidence_hash}\n"
        "  references:\n"
        "    - path: references/example.md\n"
        "      source_sections: [Example]\n"
        "      content_mode: first_party_synthesis\n"
        "      load_when: [example topic]\n"
    )
    (authority / "authority.yaml").write_text(authority_yaml, encoding="utf-8", newline="\n")
    source_map_yaml = (
        "schema_version: 1\n"
        f"reconciled_against: {evidence_hash}\n"
        "references:\n"
        "  - path: references/example.md\n"
        "    source_sections: [Example]\n"
        "    content_mode: first_party_synthesis\n"
        "    load_when: [example topic]\n"
    )
    (authority / "source-map.yaml").write_text(source_map_yaml, encoding="utf-8", newline="\n")
    reference = skill / "references/example.md"
    reference.parent.mkdir(parents=True)
    reference.write_text("# Example\n", encoding="utf-8", newline="\n")
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
    authority_text = authority_path.read_text(encoding="utf-8")
    authority_text = re.sub(
        r"content_sha256: [0-9a-f]{64}", "content_sha256: not-a-sha", authority_text
    )
    authority_text = (
        authority_text.replace("title: Example Authority", "title: ''")
        .replace("retrieved_at: '2026-07-20'", "retrieved_at: invalid-date")
        .replace("path: references/example.md", "path: ../escape.md")
        .replace("source_sections: [Example]", "source_sections: []")
    )
    authority_path.write_text(authority_text, encoding="utf-8", newline="\n")
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
    source_skill = write_authority_fixture(
        tmp_path / "source", lane="skills-with-source", source_content="approved source"
    )
    citation_skill = write_authority_fixture(tmp_path / "citation", lane="skills-with-citation")
    citation_sha = hashlib.sha256((citation_skill / "assets/authority/CITATIONS.md").read_bytes()).hexdigest()
    _set_sha_for_skill(citation_skill, citation_sha)

    assert validator.validate_authority_skill(source_skill) == []
    assert validator.validate_authority_skill(citation_skill) == []


def _set_sha_for_skill(skill: Path, sha: str) -> None:
    authority_path = skill / "assets/authority/authority.yaml"
    source_map_path = skill / "assets/authority/source-map.yaml"
    authority_path.write_text(
        authority_path.read_text(encoding="utf-8")
        .replace(
            "content_sha256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            f"content_sha256: {sha}",
        )
        .replace("reconciled_against: v1", f"reconciled_against: {sha}"),
        encoding="utf-8",
        newline="\n",
    )
    source_map_path.write_text(
        source_map_path.read_text(encoding="utf-8").replace(
            "reconciled_against: v1", f"reconciled_against: {sha}"
        ),
        encoding="utf-8",
        newline="\n",
    )


def write_mixed_source_fixture(root: Path) -> tuple[Path, dict[str, str]]:
    skill = root / "mixed"
    authority_root = skill / "assets/authority"
    authority_root.mkdir(parents=True)
    ref_source = authority_root / "reference-source"
    ref_source.mkdir(parents=True)

    postgresql_dir = ref_source / "postgresql-docs"
    postgresql_dir.mkdir(parents=True)
    postgresql_file = postgresql_dir / "postgresql-18.4-docs.tar.gz"
    postgresql_file.write_bytes(b"postgresql source")
    postgresql_hash = validator._compute_file_sha256(postgresql_file)

    sqlite_dir = ref_source / "sqlite-docs"
    sqlite_dir.mkdir(parents=True)
    sqlite_file = sqlite_dir / "sqlite-doc-3530300.zip"
    sqlite_file.write_bytes(b"sqlite source")
    sqlite_hash = validator._compute_file_sha256(sqlite_file)

    (authority_root / "CITATIONS.md").write_text(
        "# Citations\n\n"
        "## Scholarly citation\n\nPostgreSQL and SQLite docs.\n\n"
        "## Derivation boundary\n\nMixed source.\n\n"
        "## Attribution\n\nSee licenses.\n\n"
        "## Human review\n\nApproved.\n",
        encoding="utf-8",
        newline="\n",
    )

    pg_ref = skill / "references/postgresql.md"
    pg_ref.parent.mkdir(parents=True)
    pg_ref.write_text("# PostgreSQL\n", encoding="utf-8", newline="\n")
    sqlite_ref = skill / "references/sqlite.md"
    sqlite_ref.parent.mkdir(parents=True, exist_ok=True)
    sqlite_ref.write_text("# SQLite\n", encoding="utf-8", newline="\n")

    authority_yaml = (
        "schema_version: 1\n"
        "custody: marketplace\n"
        "lane: skills-with-mixed-source\n"
        "authority:\n"
        "  postgresql-docs:\n"
        "    title: PostgreSQL Docs\n"
        "    canonical_url: https://postgresql.org/docs\n"
        "    pinned_source_url: https://postgresql.org/docs/download\n"
        "    latest_check_url: https://postgresql.org/docs\n"
        "    revision: '1'\n"
        "    retrieved_at: '2026-07-21'\n"
        f"    content_sha256: {postgresql_hash}\n"
        "    license: PostgreSQL License\n"
        "    license_url: https://postgresql.org/about/licence/\n"
        "  sqlite-docs:\n"
        "    title: SQLite Docs\n"
        "    canonical_url: https://sqlite.org/docs.html\n"
        "    pinned_source_url: https://sqlite.org/download.zip\n"
        "    latest_check_url: https://sqlite.org/docs.html\n"
        "    revision: '1'\n"
        "    retrieved_at: '2026-07-21'\n"
        f"    content_sha256: {sqlite_hash}\n"
        "    license: Public Domain\n"
        "    license_url: https://sqlite.org/copyright.html\n"
        "decomposition:\n"
        "  reconciled_against:\n"
        f"    postgresql-docs: {postgresql_hash}\n"
        f"    sqlite-docs: {sqlite_hash}\n"
        "  references:\n"
        "    - path: references/postgresql.md\n"
        "      source_sections: ['postgresql: Server Administration']\n"
        "      content_mode: licensed_adaptation\n"
        "      load_when: [postgresql]\n"
        "    - path: references/sqlite.md\n"
        "      source_sections: ['sqlite: SQL Language']\n"
        "      content_mode: licensed_adaptation\n"
        "      load_when: [sqlite]\n"
    )
    (authority_root / "authority.yaml").write_text(authority_yaml, encoding="utf-8", newline="\n")

    source_map_yaml = (
        "schema_version: 1\n"
        "reconciled_against:\n"
        f"  postgresql-docs: {postgresql_hash}\n"
        f"  sqlite-docs: {sqlite_hash}\n"
        "references:\n"
        "  - path: references/postgresql.md\n"
        "    source_sections: ['postgresql: Server Administration']\n"
        "    content_mode: licensed_adaptation\n"
        "    load_when: [postgresql]\n"
        "  - path: references/sqlite.md\n"
        "    source_sections: ['sqlite: SQL Language']\n"
        "    content_mode: licensed_adaptation\n"
        "    load_when: [sqlite]\n"
    )
    (authority_root / "source-map.yaml").write_text(source_map_yaml, encoding="utf-8", newline="\n")

    return skill, {
        "postgresql-docs": postgresql_hash,
        "sqlite-docs": sqlite_hash,
    }


def test_mixed_source_lane_passes_with_multiple_vendored_sources(tmp_path: Path):
    skill, _ = write_mixed_source_fixture(tmp_path)
    assert validator.validate_authority_skill(skill) == []


def test_mixed_source_authority_records_require_fields(tmp_path: Path):
    skill, _ = write_mixed_source_fixture(tmp_path)
    authority_path = skill / "assets/authority/authority.yaml"
    text = authority_path.read_text(encoding="utf-8")
    text = text.replace("    title: PostgreSQL Docs", "    title: ''", 1)
    authority_path.write_text(text, encoding="utf-8", newline="\n")
    errors = validator.validate_authority_skill(skill)
    assert any(
        "authority.yaml authority[postgresql-docs] title must be a nonblank string" in error
        for error in errors
    )


def test_mixed_source_reconciled_against_must_be_mapping(tmp_path: Path):
    skill, hashes = write_mixed_source_fixture(tmp_path)
    authority_path = skill / "assets/authority/authority.yaml"
    text = authority_path.read_text(encoding="utf-8")
    text = text.replace(
        f"  reconciled_against:\n"
        f"    postgresql-docs: {hashes['postgresql-docs']}\n"
        f"    sqlite-docs: {hashes['sqlite-docs']}",
        f"  reconciled_against: {hashes['postgresql-docs']}",
    )
    authority_path.write_text(text, encoding="utf-8", newline="\n")

    source_map_path = skill / "assets/authority/source-map.yaml"
    text = source_map_path.read_text(encoding="utf-8")
    text = text.replace(
        f"reconciled_against:\n"
        f"  postgresql-docs: {hashes['postgresql-docs']}\n"
        f"  sqlite-docs: {hashes['sqlite-docs']}",
        f"reconciled_against: {hashes['postgresql-docs']}",
    )
    source_map_path.write_text(text, encoding="utf-8", newline="\n")

    errors = validator.validate_authority_skill(skill)
    assert any("reconciled_against must be a non-empty mapping" in error for error in errors)


def test_mixed_source_per_label_sha_must_match_vendored_file(tmp_path: Path):
    skill, hashes = write_mixed_source_fixture(tmp_path)
    bad_hash = "a" * 64
    authority_path = skill / "assets/authority/authority.yaml"
    text = authority_path.read_text(encoding="utf-8")
    text = text.replace(
        f"    content_sha256: {hashes['postgresql-docs']}",
        f"    content_sha256: {bad_hash}",
        1,
    )
    authority_path.write_text(text, encoding="utf-8", newline="\n")
    errors = validator.validate_authority_skill(skill)
    assert any("reference-source/postgresql-docs" in error for error in errors)


def test_mixed_source_missing_label_directory_fails(tmp_path: Path):
    skill, _ = write_mixed_source_fixture(tmp_path)
    import shutil
    shutil.rmtree(skill / "assets/authority/reference-source/postgresql-docs")
    errors = validator.validate_authority_skill(skill)
    assert any("reference-source/postgresql-docs" in error for error in errors)
