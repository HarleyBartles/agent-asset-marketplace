# asking-clarifying-questions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `asking-clarifying-questions` first-party marketplace skill, project it into `house-skills` (mega-pack) and `repo-worker-pack`, and validate it with a contract test plus a manual subagent pressure scenario.

**Architecture:** A single canonical source tree under `sources/first_party/skills/asking-clarifying-questions/` holds `SKILL.md`, `agents/openai.yaml`, and `references/.gitkeep`. The `repo-worker-pack` bundle entry and source-ledger in `codex-marketplace/custody-pack-registry.json` are extended; `house-skills` auto-includes all first-party skills. The full marketplace rebuild projects and validates all derived surfaces.

**Tech Stack:** Markdown, YAML, JSON, Python/pytest, `py -3 tools/rebuild_marketplace.py --apply`, `bash scripts/ci-preflight.sh --check`.

## Global Constraints

- First-party skill source lives under `sources/first_party/skills/asking-clarifying-questions/`.
- `SKILL.md` body must be under 500 words; frontmatter must include `name`, `description`, `license`, `metadata` with canonical identity and trigger fields.
- `agents/openai.yaml` must include `version: 1`, `metadata.skill_name`, `interface.display_name`, `interface.short_description`, `interface.default_prompt`, `policy.allow_implicit_invocation`.
- Do not hand-edit derived projection surfaces; regenerate with `py -3 tools/rebuild_marketplace.py --apply`.
- All text files written with LF line endings (`newline="\n"`).
- Run pytest with `tools` on `PYTHONPATH` (`$env:PYTHONPATH='tools'` on Windows PowerShell, `PYTHONPATH=tools` on Unix).
- Commit after each independently testable task.

## Task 1: Write the failing contract test

**Files:**
- Create: `tests/test_asking_clarifying_questions_contract.py`

**Interfaces:**
- Consumes: none
- Produces: `tests/test_asking_clarifying_questions_contract.py`

- [ ] **Step 1: Write the test file**

Create `tests/test_asking_clarifying_questions_contract.py` with the following content:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

```text
$env:PYTHONPATH = 'tools'
py -3 -m pytest tests/test_asking_clarifying_questions_contract.py -v
```

Expected: FAIL. The source skill directory and `agents/openai.yaml` do not exist yet.

- [ ] **Step 3: Commit**

```text
git add tests/test_asking_clarifying_questions_contract.py
git commit -m 'test: add contract test for asking-clarifying-questions skill' -m 'Generated with [Devin](https://devin.ai)' -m 'Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>'
```

## Task 2: Scaffold and author the skill source

**Files:**
- Create: `sources/first_party/skills/asking-clarifying-questions/SKILL.md`
- Create: `sources/first_party/skills/asking-clarifying-questions/agents/openai.yaml`
- Create (via scaffold): `sources/first_party/skills/asking-clarifying-questions/references/.gitkeep`

**Interfaces:**
- Consumes: none
- Produces: canonical first-party skill source

- [ ] **Step 1: Scaffold the source directory**

```text
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name asking-clarifying-questions --custody marketplace --lane first_party
```

- [ ] **Step 2: Read the scaffold SKILL.md and overwrite it**

Read `sources/first_party/skills/asking-clarifying-questions/SKILL.md`, then use `write` to replace it with the following exact content:

```yaml
---
name: asking-clarifying-questions
description: Use when an ambiguity remains after safe internal resolution and a single answer from your human partner would unblock the next action, without needing a full design session or a pre-action risk gate.
metadata:
  source-id: asking-clarifying-questions
  source-path: sources/first_party/skills/asking-clarifying-questions/SKILL.md
  provenance-name: Asking Clarifying Questions first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: mid-flight ambiguity resolution through a single clarifying question
  use_when:
  - Use when an ambiguity is internally unresolved and a single human decision would unblock the immediate next step.
  - Use when the agent is mid-plan, mid-execution, or inside another skill and a missing fact, term, scope, boundary, or output shape prevents safe progress.
  - Use when the answer is a concrete decision, not a design.
  do_not_use_when:
  - Do not use when the ambiguity needs a full spec or design; use brainstorming.
  - Do not use when the next action could violate scope, authority, source truth, canon, safety, or involve irreversible mutation; use risk-gates.
  - Do not use when the answer is already forced by durable source, policy, or a safe default; resolve internally.
  use_instead:
  - brainstorming
  - risk-gates
  related_skills:
  - brainstorming
  - risk-gates
  - writing-plans
  - executing-plans
  - handoff-gates
license: MIT
---

# Asking Clarifying Questions

Ask one narrow question that your human partner can answer when a single unresolved ambiguity blocks the immediate next step.

## Core pattern

1. State the immediate next action that depends on the answer.
2. State the ambiguity concisely (one missing fact, term, scope, boundary, or output shape).
3. State the risk of guessing.
4. Give a concrete recommendation and the available options.
5. Ask one question.
6. Record the answer and continue.

## When to use

- Internal resolution is exhausted (rules, source truth, non-goals, safe defaults).
- A single missing decision separates the agent from the next action.
- The cost of guessing is wasted motion or reversible rework, not a canon or authority mistake.

## When not to use

- The ambiguity needs a full design or spec: use `brainstorming`.
- The ambiguity affects scope, authority, source truth, canon, safety, or irreversible mutation: use `risk-gates` and accept a block if needed.
- The answer is already forced or harmless: resolve internally and do not ask.

## Common mistakes

- Asking a vague question instead of a single decision.
- Asking when the answer is already in durable source or policy.
- Treating a clarifying question as a substitute for a missing design or risk gate.
- Asking multiple questions in one turn.

## Relation to other skills

- `brainstorming` asks many questions to shape a design.
- `risk-gates` decides whether to proceed, repair, or block when hidden risk is present.
- `asking-clarifying-questions` handles the 'interactive'/'amber' outcome where a single human answer is the lawful next step.
```

- [ ] **Step 3: Create agents/openai.yaml**

Create `sources/first_party/skills/asking-clarifying-questions/agents/openai.yaml` with the following content:

```yaml
version: 1
metadata:
  skill_name: asking-clarifying-questions
  source_category: first_party

interface:
  display_name: Asking Clarifying Questions
  short_description: Use when an ambiguity remains after safe internal resolution and a single answer from your human partner would unblock the next action, without needing a full design session or a pre-action risk gate.
  default_prompt: Use /asking-clarifying-questions when an ambiguity is internally unresolved and a single human decision would unblock the immediate next step. State the next action, the ambiguity, the risk of guessing, a recommendation with options, and ask one concrete question. Do not use when the ambiguity needs a full design or spec (use brainstorming), when it could violate scope/authority/source/canon/safety/irreversible mutation (use risk-gates), or when the answer is already forced by durable source or policy.
policy:
  products:
  - chatgpt
  - codex
  - api
  - atlas
  allow_implicit_invocation: true
```

- [ ] **Step 4: Run the source-level tests**

```text
$env:PYTHONPATH = 'tools'
py -3 -m pytest tests/test_asking_clarifying_questions_contract.py -k 'source or frontmatter or body or agents' -v
```

Expected: PASS. The registry and projection tests still fail at this point; that is expected and fixed in Task 3.

- [ ] **Step 5: Commit**

```text
git add sources/first_party/skills/asking-clarifying-questions/
git commit -m 'feat: add asking-clarifying-questions first-party skill source' -m 'Generated with [Devin](https://devin.ai)' -m 'Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>'
```

## Task 3: Wire repo-worker-pack and regenerate marketplace

**Files:**
- Modify: `codex-marketplace/custody-pack-registry.json`

**Interfaces:**
- Consumes: canonical source from Task 2
- Produces: `repo-worker-pack` projection, `house-skills` projection, installed skill in `.agents/skills/asking-clarifying-questions`

- [ ] **Step 1: Create a temporary registry update script**

Create `update_registry.py` in the repo root with the following content:

```python
import json
from pathlib import Path

p = Path('codex-marketplace/custody-pack-registry.json')
registry = json.loads(p.read_text(encoding='utf-8'))
pack = next(pack for pack in registry['packs'] if pack.get('bundle_name') == 'repo-worker-pack')

skill_source = 'sources/first_party/skills/asking-clarifying-questions'
if skill_source not in pack['source_ledger']:
    pack['source_ledger'].append(skill_source)

new_entry = {
    'canonical_name': 'asking-clarifying-questions',
    'source_category': 'first_party',
    'content_mode': 'verbatim',
    'source_family': 'first_party',
    'canonical_source_path': 'sources/first_party/skills/asking-clarifying-questions',
    'local_path': 'skills/asking-clarifying-questions',
    'provenance_note': 'Projected verbatim from the first-party asking-clarifying-questions skill. Any-time clarifying-question skill for single ambiguities.',
    'copy_expectation': 'byte_identical',
}
if not any(e.get('canonical_name') == 'asking-clarifying-questions' for e in pack['entries']):
    pack['entries'].append(new_entry)

p.write_text(json.dumps(registry, indent=2) + chr(10), encoding='utf-8', newline='\n')
```

- [ ] **Step 2: Run the script and remove it**

```text
py -3 update_registry.py
Remove-Item update_registry.py
```

Expected: `codex-marketplace/custody-pack-registry.json` now contains the new `repo-worker-pack` entry and source ledger item.

- [ ] **Step 3: Run the full marketplace rebuild**

```text
py -3 tools/rebuild_marketplace.py --apply
```

Expected: all phases complete and print `OK` for inventory, heal, project, index, catalog, and validate.

- [ ] **Step 4: Run the full contract test**

```text
$env:PYTHONPATH = 'tools'
py -3 -m pytest tests/test_asking_clarifying_questions_contract.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```text
git add codex-marketplace/custody-pack-registry.json
git add codex-marketplace/plugins/house-skills/ codex-marketplace/plugins/repo-worker-pack/
git add generated/skill-zips/asking-clarifying-questions.zip
git add .agents/skills/asking-clarifying-questions .agents/plugins/marketplace.json
git add codex-marketplace/manifest.json repo-index/ provenance/first-party-skills.md
git status --short
git commit -m 'feat: project asking-clarifying-questions into house-skills and repo-worker-pack' -m 'Generated with [Devin](https://devin.ai)' -m 'Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>'
```

## Task 4: Validate behavior and green CI

**Files:**
- Create: `.agents/superpowers/sdd/2026-07-28-asking-clarifying-questions/pressure-test-report.md`

**Interfaces:**
- Consumes: installed `asking-clarifying-questions` skill and related `brainstorming`/`risk-gates` skills
- Produces: behavior validation report and green preflight

- [ ] **Step 1: Run a manual subagent pressure scenario**

Use `run_subagent` with the `subagent_explore` profile and the following prompt. Save the response in `.agents/superpowers/sdd/2026-07-28-asking-clarifying-questions/pressure-test-report.md`.

```text
You are an agent operating in the current repo worktree. Read the skill at sources/first_party/skills/asking-clarifying-questions/SKILL.md and the related skills at sources/first_party/skills/brainstorming/SKILL.md and sources/first_party/skills/risk-gates/SKILL.md.

Scenario: The user instruction is 'rename the temp file'. The workspace has two files: temp.txt and temp.log. The new name is not given. This is reversible; no scope, authority, canon, safety, or irreversible mutation is at stake. There is a single missing fact (which file) and a single missing output shape (the new name).

Use the asking-clarifying-questions skill. Respond with the compact queue: next action, ambiguity, risk of guessing, recommendation/options, and exactly one concrete question. Do not use brainstorming or risk-gates, and do not proceed to rename.
```

Expected response checklist (record PASS/FAIL in the report):
- Response states the immediate next action (renaming a file).
- Response states the ambiguity (which file and/or new name).
- Response states the risk of guessing (wrong file renamed, wasted round-trip).
- Response gives a concrete recommendation with options.
- Response contains exactly one question.
- Response does not call brainstorming or risk-gates and does not perform the rename.

- [ ] **Step 2: Run full CI preflight**

```text
bash scripts/ci-preflight.sh --check
```

Expected: All preflight checks pass. If the pressure test produced a FAIL, fix the skill body and re-run this step.

- [ ] **Step 3: Fix and push only if preflight or the pressure test fails**

If `bash scripts/ci-preflight.sh --check` or the pressure test produced a FAIL, fix the skill body or source, re-run the failing checks, then stage the changed files shown by `git status --short` and commit:

```text
git commit -m 'fix: address asking-clarifying-questions validation findings' -m 'Generated with [Devin](https://devin.ai)' -m 'Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>'
git push
```

If all checks pass, no additional commit is required.

## Execution Handoff

Plan-readiness score: 9/10

After this plan is approved, choose one of the following execution approaches:

1. **Subagent-Driven (recommended):** Dispatch a fresh `subagent_general` per task, review between tasks, fast iteration. Required sub-skill: `superpowers:subagent-driven-development`.
2. **Inline Execution:** Execute tasks in this session using `superpowers:executing-plans`, batch execution with checkpoints.

Which approach would you like to use?
