from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from tree_canonicalization import canonicalize_tree_bytes  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources/first_party/skills/writing-with-clarity"
SKILL = SOURCE / "SKILL.md"
REGISTRY = ROOT / "codex-marketplace/custody-pack-registry.json"

SHORT_REFERENCES = {
    "references/routing.md",
    "references/sentence-mechanics.md",
    "references/composition-and-flow.md",
    "references/clarity-and-concision.md",
    "references/usage-and-word-choice.md",
    "references/format-and-markup.md",
    "references/final-edit.md",
    "assets/authority/source-map.yaml",
}

REFERENCE_SOURCE_DIR = (
    SOURCE / "assets/authority/reference-source/elements-of-style-1918"
)
FULL_SOURCE = REFERENCE_SOURCE_DIR / "elements-of-style-1918.txt"
PROJECTION_ROOTS = [
    ROOT / "codex-marketplace/plugins/repo-worker-pack/skills/writing-with-clarity",
    ROOT / ".agents/skills/writing-with-clarity",
]
PACK_DOCS = [
    ROOT / "codex-marketplace/plugins/repo-worker-pack/README.md",
    ROOT / "codex-marketplace/plugins/repo-worker-pack/SOURCE.md",
    ROOT / "codex-marketplace/plugins/repo-worker-pack/PROJECTION.md",
]
REPO_WORKER_PACK_MANIFEST = (
    ROOT / "codex-marketplace/plugins/repo-worker-pack/references/bundle-manifest.json"
)


def _canonical_bytes(path: Path) -> bytes:
    """Compare agent YAML canonically to allow injected projection identity."""
    raw = path.read_bytes()
    if path.name == "openai.yaml":
        return canonicalize_tree_bytes(path, raw)
    return raw


def test_source_skill_contains_expected_reference_tree():
    assert SKILL.is_file()
    for relative_path in SHORT_REFERENCES:
        assert (SOURCE / relative_path).is_file(), relative_path
    assert REFERENCE_SOURCE_DIR.is_dir()
    assert FULL_SOURCE.is_file()


def test_skill_routes_all_human_facing_prose_without_defaulting_to_full_source():
    text = SKILL.read_text(encoding="utf-8")
    assert "all prose intended for human readers" in text
    assert "references/routing.md" in text
    assert "one primary reference" in text
    assert "at most one secondary reference" in text
    assert "Do not read the whole source tree during ordinary use" in text
    assert "assets/authority/source-map.yaml" in text
    assert "when a shorter reference leaves an unresolved question" in text
    assert "This is a separate" in text
    assert "secondary topical reference" in text
    assert "Do not use when another more specific skill owns this task." in text


def test_short_references_preserve_source_mapping_and_precedence():
    source_map = (SOURCE / "assets/authority/source-map.yaml").read_text(encoding="utf-8")
    assert "elementary-rules-of-usage.md: II. Elementary Rules Of Usage" in source_map
    assert (
        "elementary-principles-of-composition.md: III. Elementary Principles Of Composition"
        in source_map
    )
    assert (
        "words-and-expressions-commonly-misused.md: V. Words And Expressions Commonly Misused"
        in source_map
    )
    assert "a-few-matters-of-form.md: IV. A Few Matters Of Form" in source_map
    assert "spelling.md: VI. Spelling" in source_map

    authority_evidence = (
        (SOURCE / "assets/authority/CITATIONS.md").read_text(encoding="utf-8")
        + "\n"
        + (SOURCE / "assets/authority/authority.yaml").read_text(encoding="utf-8")
    )
    assert "https://www.gutenberg.org/ebooks/37134" in authority_evidence
    assert "https://gutenberg.org/files/37134/37134.txt" in authority_evidence
    assert "dd6ce8de3be796f400f600ebf681b9a298f623c2c4139f9d5049a7c58c65d277" in authority_evidence.lower()

    for relative_path in SHORT_REFERENCES - {"references/routing.md", "assets/authority/source-map.yaml"}:
        text = (SOURCE / relative_path).read_text(encoding="utf-8")
        assert "Source basis" in text, relative_path
        assert "historical source" in text, relative_path


def test_router_has_explicit_artifact_precedence_and_retry_boundary():
    routing = (SOURCE / "references/routing.md").read_text(encoding="utf-8")
    format_reference = (SOURCE / "references/format-and-markup.md").read_text(encoding="utf-8")
    assert "artifact route takes precedence" in routing
    assert "| `final-edit.md` |" not in routing
    assert "final-edit pass is separate" in routing
    assert "retry only when the product behavior confirms" in format_reference


def test_historical_source_is_marked_reference_only():
    source_markers = (
        (SOURCE / "assets/authority/source-map.yaml").read_text(encoding="utf-8")
        + "\n"
        + (SOURCE / "assets/authority/CITATIONS.md").read_text(encoding="utf-8")
        + "\n"
        + SKILL.read_text(encoding="utf-8")
    )
    assert "historical" in source_markers
    assert "not default operational guidance" in source_markers or "not current style authority" in source_markers
    assert FULL_SOURCE.is_file()
    text = FULL_SOURCE.read_text(encoding="utf-8")
    assert "The Elements of Style" in text
    assert "Project Gutenberg" in text


def test_projected_and_installed_skill_trees_match_source():
    source_files = sorted(path.relative_to(SOURCE).as_posix() for path in SOURCE.rglob("*") if path.is_file())
    for projection in PROJECTION_ROOTS:
        projection_files = sorted(
            path.relative_to(projection).as_posix() for path in projection.rglob("*") if path.is_file()
        )
        assert projection_files == source_files, projection
        for relative_path in source_files:
            source_path = SOURCE / relative_path
            projection_path = projection / relative_path
            source_bytes = _canonical_bytes(source_path)
            projection_bytes = _canonical_bytes(projection_path)
            assert hashlib.sha256(projection_bytes).digest() == hashlib.sha256(source_bytes).digest(), relative_path


def test_repo_worker_pack_inventory_docs_are_manifest_backed():
    manifest = json.loads(REPO_WORKER_PACK_MANIFEST.read_text(encoding="utf-8"))
    manifest_entry_count = len(manifest["entries"])
    for path in PACK_DOCS:
        text = path.read_text(encoding="utf-8")
        assert "writing-with-clarity" in text, path
        assert "BEGIN GENERATED:" in text, path
    assert f"Manifest entry count: {manifest_entry_count}." in PACK_DOCS[0].read_text(encoding="utf-8")
    assert f"Active manifest entries ({manifest_entry_count}):" in PACK_DOCS[2].read_text(encoding="utf-8")


def test_repo_worker_pack_registry_contains_first_party_entry():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    pack = next(pack for pack in registry["packs"] if pack.get("bundle_name") == "repo-worker-pack")
    entries = [entry for entry in pack["entries"] if entry.get("canonical_name") == "writing-with-clarity"]
    assert len(entries) == 1
    entry = entries[0]
    assert entry["source_category"] == "first_party"
    assert entry["content_mode"] == "verbatim"
    assert entry["source_family"] == "first_party"
    assert entry["canonical_source_path"] == "sources/first_party/skills/writing-with-clarity"
    assert entry["local_path"] == "skills/writing-with-clarity"
