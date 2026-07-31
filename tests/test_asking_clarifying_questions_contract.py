from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from tree_canonicalization import canonicalize_tree_bytes  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources/first_party/skills/asking-clarifying-questions'
SKILL = SOURCE / 'SKILL.md'
AGENTS = SOURCE / 'agents' / 'openai.yaml'
REGISTRY = ROOT / 'codex-marketplace' / 'custody-pack-registry.json'
PROJECTION_ROOTS = [
    ROOT / 'codex-marketplace' / 'plugins' / 'repo-worker-pack' / 'skills' / 'asking-clarifying-questions',
    ROOT / '.agents' / 'skills' / 'asking-clarifying-questions',
]


def _canonical_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    if path.name == 'openai.yaml':
        return canonicalize_tree_bytes(path, raw)
    return raw


def _skill_frontmatter() -> dict:
    text = SKILL.read_text(encoding='utf-8')
    parts = text.split('---')
    if len(parts) < 3:
        raise ValueError('SKILL.md must have opening and closing frontmatter delimiters')
    return yaml.safe_load(parts[1]) or {}


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
    frontmatter = _skill_frontmatter()
    assert frontmatter.get('name') == 'asking-clarifying-questions'
    assert frontmatter.get('description')
    assert frontmatter.get('license') == 'MIT'

    metadata = frontmatter.get('metadata') or {}
    assert metadata.get('source-id') == 'asking-clarifying-questions'
    assert metadata.get('source-path') == 'sources/first_party/skills/asking-clarifying-questions/SKILL.md'
    assert metadata.get('source-category') == 'first_party'
    assert metadata.get('status') == 'active'
    assert isinstance(metadata.get('use_when'), list)
    assert isinstance(metadata.get('do_not_use_when'), list)


def test_skill_body_is_under_500_words():
    body = _skill_body()
    words = re.findall(r'\b\w+\b', body)
    assert len(words) < 500, f'body is {len(words)} words'


def test_skill_body_contains_clarifying_question_pattern():
    body = _skill_body().lower()
    assert 'next action' in body
    assert 'ambiguity' in body
    assert 'risk of guessing' in body
    assert 'recommendation' in body
    assert 'question' in body
    assert 'brainstorming' in body
    assert 'risk-gates' in body


def test_agents_openai_yaml_has_required_fields():
    data = yaml.safe_load(AGENTS.read_text(encoding='utf-8'))
    assert data.get('version') == 1
    assert data.get('metadata', {}).get('skill_name') == 'asking-clarifying-questions'
    interface = data.get('interface') or {}
    assert interface.get('display_name') == 'Asking Clarifying Questions'
    assert interface.get('short_description')
    assert interface.get('default_prompt')
    assert data.get('policy', {}).get('allow_implicit_invocation') is True


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
    assert entry.get('lane') == 'Worker'
    assert entry.get('source_path') == 'sources/first_party/skills/asking-clarifying-questions/SKILL.md'
    assert entry.get('source_author') == 'Harley Bartles'
    assert entry.get('source_license') == 'MIT'
    assert entry.get('source_repo') == 'https://github.com/HarleyBartles/agent-asset-marketplace'
    assert entry['copy_expectation'] == 'byte_identical'
    assert 'provenance_note' in entry


def test_pressure_test_report_exists_and_passes():
    pressure_dir = ROOT / 'tests' / 'pressure' / 'asking-clarifying-questions'
    assert pressure_dir.is_dir()
    prompt = pressure_dir / 'prompts' / 'baseline-ambiguous-instruction.md'
    assert prompt.is_file()
    results = pressure_dir / 'results.md'
    assert results.is_file()
    results_text = results.read_text(encoding='utf-8')
    assert 'Verdict:' in results_text
    assert 'PASS' in results_text


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
