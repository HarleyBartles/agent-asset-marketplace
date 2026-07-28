from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tree_canonicalization import canonicalize_tree_bytes


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources/first_party/skills/asking-clarifying-questions'
SKILL = SOURCE / 'SKILL.md'
AGENTS = SOURCE / 'agents' / 'openai.yaml'
REGISTRY = ROOT / 'codex-marketplace' / 'custody-pack-registry.json'
PROJECTION_ROOTS = [
    ROOT / 'codex-marketplace' / 'plugins' / 'house-skills' / 'skills' / 'asking-clarifying-questions',
    ROOT / 'codex-marketplace' / 'plugins' / 'repo-worker-pack' / 'skills' / 'asking-clarifying-questions',
    ROOT / '.agents' / 'skills' / 'asking-clarifying-questions',
]


def _canonical_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    if path.name == 'openai.yaml':
        return canonicalize_tree_bytes(path, raw)
    return raw


def _skill_body() -> str:
    text = SKILL.read_text(encoding='utf-8')
    parts = text.split('---')
    if len(parts) < 3:
        raise ValueError('SKILL.md must have opening and closing frontmatter delimiters')
    return '---'.join(parts[2:])


def test_source_skill_has_required_files():
    assert SKILL.is_file()
    assert AGENTS.is_file()
    assert (SOURCE / 'references' / '.gitkeep').is_file()


def test_skill_frontmatter_has_required_fields():
    text = SKILL.read_text(encoding='utf-8')
    assert 'name: asking-clarifying-questions' in text
    assert 'description:' in text
    assert 'metadata:' in text
    assert 'source-id: asking-clarifying-questions' in text
    assert 'source-path: sources/first_party/skills/asking-clarifying-questions/SKILL.md' in text
    assert 'source-category: first_party' in text
    assert 'status: active' in text
    assert 'use_when:' in text
    assert 'do_not_use_when:' in text
    assert 'license: MIT' in text


def test_skill_body_is_under_500_words():
    body = _skill_body()
    words = re.findall(r'\b\w+\b', body)
    assert len(words) < 500, f'body is {len(words)} words'


def test_agents_openai_yaml_has_required_fields():
    text = AGENTS.read_text(encoding='utf-8')
    assert 'version: 1' in text
    assert 'skill_name: asking-clarifying-questions' in text
    assert 'display_name: Asking Clarifying Questions' in text
    assert 'short_description:' in text
    assert 'default_prompt:' in text
    assert 'allow_implicit_invocation: true' in text


def test_repo_worker_pack_registry_contains_entry():
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    pack = next(p for p in registry['packs'] if p.get('bundle_name') == 'repo-worker-pack')
    entries = [e for e in pack['entries'] if e.get('canonical_name') == 'asking-clarifying-questions']
    assert len(entries) == 1
    entry = entries[0]
    assert entry['source_category'] == 'first_party'
    assert entry['content_mode'] == 'verbatim'
    assert entry['source_family'] == 'first_party'
    assert entry['canonical_source_path'] == 'sources/first_party/skills/asking-clarifying-questions'
    assert entry['local_path'] == 'skills/asking-clarifying-questions'
    assert entry['copy_expectation'] == 'byte_identical'
    assert 'provenance_note' in entry


def test_projected_and_installed_skill_trees_match_source():
    source_files = sorted(
        path.relative_to(SOURCE).as_posix() for path in SOURCE.rglob('*') if path.is_file()
    )
    for projection in PROJECTION_ROOTS:
        projection_files = sorted(
            path.relative_to(projection).as_posix() for path in projection.rglob('*') if path.is_file()
        )
        assert projection_files == source_files, projection
        for relative_path in source_files:
            source_path = SOURCE / relative_path
            projection_path = projection / relative_path
            source_bytes = _canonical_bytes(source_path)
            projection_bytes = _canonical_bytes(projection_path)
            assert hashlib.sha256(projection_bytes).digest() == hashlib.sha256(source_bytes).digest(), relative_path
