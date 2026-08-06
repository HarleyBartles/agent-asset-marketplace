# Implementation Plan: Cortex/ECC Tier 1 first-party skill migration (MARK-353)

## Scope

Convert the 30 currently projected Claude-Cortex and ECC third-party skill remnants into 15 source-backed first-party skills, remove the residual upstream snapshots, retire the `codex-cortex` and `everything-codex-code` mega-packs, and land all changes in a single PR.

## References

- Design spec: `.agents/superpowers/specs/2026-07-21-cortex-ecc-remnant-clearance-design.md`
- Retained upstream inventory: `.agents/superpowers/specs/2026-07-21-cortex-ecc-retained-upstream-inventory.md`
- Custody/projection doctrine: `docs/custody-and-projection-doctrine.md`
- Skill standards: `.agents/doctrine/skill-standards-policy.md`
- OpenAI agent contract: `.agents/docs/contracts/openai-agent-yaml.md`
- Frontmatter contract: `.agents/docs/contracts/skill-frontmatter.md`
- Tooling: `tools/AGENTS.md`

## Worktree

- Branch: `mark-353-cortex-ecc-tier1`
- Worktree: `Z:\_agent-worktrees\agent-asset-marketplace\mark-353-cortex-ecc-tier1`
- Base commit: `81c70cb568c6d821e75768f73a3c781070bb95f1` (`origin/main`; rebased 2026-07-21)

## Global constraints

- Every first-party skill lives under `sources/first_party/skills/<skill-name>/`.
- Skill `SKILL.md` body must be under 500 words; detailed guidance goes in `references/operational-guidance.md`.
- Every marketplace-projected skill needs `agents/openai.yaml` with `version: 1`, `metadata`, `interface`, and explicit `policy.allow_implicit_invocation`.
- Source-backed skills need `assets/authority/authority.yaml`, `assets/authority/source-map.yaml`, and `assets/authority/CITATIONS.md`.
- The editable source of truth for pack assignment is `codex-marketplace/custody-pack-registry.json`.
- All derived surfaces (projections, manifests, source maps, provenance maps, zips, indexes) are regenerated with `py -3 tools/rebuild_marketplace.py`.
- CI gate is `py -3 tools/check_marketplace.py`.
- Each skill (or logically atomic cluster) is one commit. The final integration and mega-pack retirement are separate commits.

## Authority-lane decisions

This plan keeps the authority surface simple for Tier 1:

| skill | lane | vendored source |
|-------|------|-----------------|
| `python` | `skills-with-citation` | none |
| `python-frameworks` | `skills-with-citation` | none |
| `api-design` | `skills-with-mixed-source` | OpenAPI Specification 3.1.0 `.md` |
| `secure-development` | `skills-with-citation` | none |
| `risk-gates` (expanded) | `skills-with-citation` | none |
| `frontend-ux` | `skills-with-citation` | none |
| `playwright-testing` | `skills-with-citation` | none |
| `mermaid-diagramming` | `skills-with-citation` | none |
| `event-driven-systems` | `skills-with-citation` | none |
| `release-engineering` | `skills-with-citation` | none |
| `requirements-elicitation` | `skills-with-citation` | none |
| `estimation` | `skills-with-citation` | none |
| `agentic-harness` | `skills-with-citation` | none |
| `agent-evaluation` | `skills-with-citation` | none |
| `research-ops` | `skills-with-citation` | none |

Deviation from design: the design lists `mermaid-diagramming` as `skills-with-source` and `playwright-testing` as `skills-with-source` or `skills-with-citation`. To avoid unbounded vendored-doc acquisition in Tier 1, this plan treats both as `skills-with-citation`. `api-design` keeps the vendored OpenAPI spec per the design. Sign-off should confirm or override this choice.

## Shared templates

### New first-party skill scaffold

Run the marketplace scaffolder once per skill:

```powershell
.\.agents\skills\mark-skill-authoring\scripts\new-skill.ps1 `
  -Name <skill-name> -Custody marketplace -Lane skills-with-citation
```

For `api-design` use the mixed-source path described in Task 2.

### `SKILL.md` frontmatter template

```yaml
---
name: <skill-name>
description: Use when [specific triggering conditions].
metadata:
  source-id: <skill-name>
  source-path: sources/first_party/skills/<skill-name>/SKILL.md
  provenance-name: <Display Name> first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when [one-line scope].
  use_when:
  - Use when [condition 1].
  - Use when [condition 2].
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
  related_skills:
  - [related-skill-1]
  - [related-skill-2]
license: MIT
---
```

### `agents/openai.yaml` template

```yaml
version: 1
metadata:
  skill_name: <skill-name>
  plugin: <pack-name>
  source_category: first_party
interface:
  display_name: <Display Name>
  short_description: Use when [triggering conditions].
  default_prompt: Use <skill-name> when [triggering conditions].
policy:
  allow_implicit_invocation: true
```

### `assets/authority/authority.yaml` (skills-with-citation)

```yaml
schema_version: 1
custody: marketplace
lane: skills-with-citation
authority:
  title: <Display Name>
  canonical_url: https://[primary-source-url]
  pinned_source_url: https://[primary-source-url]
  latest_check_url: https://[primary-source-url]
  revision: '[version or date]'
  retrieved_at: '2026-07-21'
  content_sha256: <sha256-of-CITATIONS.md>
  license: MIT
  license_url: https://opensource.org/licenses/MIT
decomposition:
  reconciled_against: <sha256-of-CITATIONS.md>
  references:
  - path: references/operational-guidance.md
    source_sections:
    - [section name]
    load_when:
    - Use when <skill-name> operational guidance is needed.
    content_mode: first_party_synthesis
```

### `assets/authority/source-map.yaml` (skills-with-citation)

```yaml
schema_version: 1
reconciled_against: <sha256-of-CITATIONS.md>
references:
  - path: references/operational-guidance.md
    source_sections:
    - [section name]
    load_when:
    - Use when <skill-name> operational guidance is needed.
    content_mode: first_party_synthesis
```

### `assets/authority/CITATIONS.md` template

```markdown
# Authority record for <skill-name>

## Scholarly citation

- [Source 1]. https://[url] (accessed 2026-07-21). [License].
- [Source 2]. https://[url] (accessed 2026-07-21). [License].

## Derivation boundary

- Derived: [what the skill covers].
- Outside scope: [what it does not cover].

## Attribution

- Clean-room first-party synthesis under MIT; attribution retained in CITATIONS.md only.

## Human review

- Reviewer: Harley Bartles
- Date: 2026-07-21
- Decision: Approved. Operational SKILL.md text contains no inline citations.

## Authority record integrity

- The `content_sha256` value in `authority.yaml` and the `reconciled_against`
  values in `authority.yaml` and `source-map.yaml` are the SHA-256 of this
  `CITATIONS.md` file.
```

Compute the SHA-256 of `CITATIONS.md` after writing it:

```powershell
py -3 -c "import hashlib, pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/<skill-name>/assets/authority/CITATIONS.md').read_bytes()).hexdigest())"
```

Then paste the value into `authority.yaml` and `source-map.yaml`.

### `references/operational-guidance.md` template

```markdown
# <Display Name> operational guidance

## When to apply

[Symptoms and triggers.]

## Core pattern

1. [Step one].
2. [Step two].
3. [Step three].

## Common mistakes

- [Mistake 1] → [fix].
- [Mistake 2] → [fix].

## Related references

- [Cited source 1](https://[url])
- [Cited source 2](https://[url])
```

### Skill body template

```markdown
# <Display Name>

## Overview

[Core principle in 1-2 sentences.]

## When to Use

- [Trigger 1].
- [Trigger 2].

Do not use when another more specific skill owns the task.

## Core Pattern

[Before/after or step-by-step guidance under 500 words total.]

## Common Mistakes

- [Mistake] → [fix].
```

## Sample completed skill: `python`

This sample is the reference shape the other 14 skills should mirror.

### `sources/first_party/skills/python/SKILL.md`

```markdown
---
name: python
description: Use when writing, reviewing, or debugging Python code and the task
  calls for idiomatic language patterns, concurrency, testing, or type-safety guidance.
metadata:
  source-id: python
  source-path: sources/first_party/skills/python/SKILL.md
  provenance-name: Python first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when writing, reviewing, or debugging Python code and the task
    calls for idiomatic language patterns, concurrency, testing, or type-safety guidance.
  use_when:
  - Use when writing or reviewing Python code.
  - Use when choosing between async and sync patterns.
  - Use when diagnosing test, type, or performance issues in Python.
  do_not_use_when:
  - Do not use when another language-specific or framework-specific skill owns the task.
  related_skills:
  - python-frameworks
  - typescript
  - database-engines
license: MIT
---

# Python

Use this skill for idiomatic Python guidance across language patterns, concurrency, testing, and type safety.

## When to Use

- Writing or reviewing Python code.
- Choosing between async/await, threading, or synchronous execution.
- Writing tests, handling type annotations, or profiling a hot path.

## Core Pattern

1. Prefer explicit over implicit: write readable code, avoid surprise imports, and document public APIs.
2. Use `asyncio` for I/O-bound concurrency; use `concurrent.futures` or multiprocessing for CPU-bound work.
3. Structure tests with `pytest`, fixtures for shared state, and parametrization for data-driven cases.
4. Add type hints where they clarify contracts; run `mypy` or a type checker in CI.
5. Profile before optimizing; `cProfile` and `line_profiler` identify real bottlenecks.

## Common Mistakes

- Mixing `async` and sync I/O in the same loop. → Await async libraries or run blocking calls in executors.
- Overusing mocks and testing implementation instead of behavior. → Mock boundaries, not internals.
- Ignoring type checker errors. → Treat `mypy` failures like test failures.

Load `references/operational-guidance.md` for deeper coverage of asyncio, pytest, and typing patterns.
```

### `sources/first_party/skills/python/agents/openai.yaml`

```yaml
version: 1
metadata:
  skill_name: python
  plugin: language-patterns-pack
  source_category: first_party
interface:
  display_name: Python
  short_description: Use when writing, reviewing, or debugging Python code.
  default_prompt: Use python when writing, reviewing, or debugging Python code.
policy:
  allow_implicit_invocation: true
```

### `sources/first_party/skills/python/assets/authority/authority.yaml`

```yaml
schema_version: 1
custody: marketplace
lane: skills-with-citation
authority:
  title: Python
  canonical_url: https://docs.python.org/3/
  pinned_source_url: https://docs.python.org/3/
  latest_check_url: https://docs.python.org/3/
  revision: '3.13'
  retrieved_at: '2026-07-21'
  content_sha256: <sha256-of-CITATIONS.md>
  license: PSF License Agreement
  license_url: https://docs.python.org/3/license.html
decomposition:
  reconciled_against: <sha256-of-CITATIONS.md>
  references:
  - path: references/operational-guidance.md
    source_sections:
    - Python language patterns
    - Asyncio and concurrency
    - Testing with pytest
    - Type safety
    load_when:
    - Use when python operational guidance is needed.
    content_mode: first_party_synthesis
```

### `sources/first_party/skills/python/assets/authority/source-map.yaml`

```yaml
schema_version: 1
reconciled_against: <sha256-of-CITATIONS.md>
references:
  - path: references/operational-guidance.md
    source_sections:
    - Python language patterns
    - Asyncio and concurrency
    - Testing with pytest
    - Type safety
    load_when:
    - Use when python operational guidance is needed.
    content_mode: first_party_synthesis
```

### `sources/first_party/skills/python/assets/authority/CITATIONS.md`

```markdown
# Authority record for python

## Scholarly citation

- Python Software Foundation. "Python 3.13 Documentation." https://docs.python.org/3/ (accessed 2026-07-21). PSF License Agreement.
- pytest contributors. "pytest documentation." https://docs.pytest.org/en/stable/contents.html (accessed 2026-07-21). MIT.
- mypy contributors. "mypy documentation." https://mypy.readthedocs.io/en/stable/ (accessed 2026-07-21). MIT.

## Derivation boundary

- Derived: idiomatic Python patterns, asyncio concurrency, pytest testing, type annotations, profiling.
- Outside scope: specific web framework guidance (see python-frameworks), non-Python languages.

## Attribution

- Clean-room first-party synthesis under MIT; upstream documentation cited only in CITATIONS.md.

## Human review

- Reviewer: Harley Bartles
- Date: 2026-07-21
- Decision: Approved. Operational SKILL.md text contains no inline citations.

## Authority record integrity

- The `content_sha256` value in `authority.yaml` and the `reconciled_against`
  values in `authority.yaml` and `source-map.yaml` are the SHA-256 of this
  `CITATIONS.md` file.
```

### `sources/first_party/skills/python/references/operational-guidance.md`

```markdown
# Python operational guidance

## When to apply

Use when the Python skill loaded and the question is deeper than a single sentence:
- choosing concurrency primitives,
- structuring pytest suites,
- applying type annotations,
- profiling and optimization.

## Asyncio and concurrency

- Use `async`/`await` for I/O-bound work (network, files, databases).
- Use `asyncio.gather` for independent coroutines; use `asyncio.TaskGroup` for structured cancellation when available.
- Run blocking CPU work in `loop.run_in_executor` or `ProcessPoolExecutor`.

## Testing with pytest

- Keep tests small and named after the behavior they assert.
- Use fixtures for setup/teardown; prefer `pytest.fixture(scope="function")` unless sharing expensive state.
- Parametrize data-driven cases.

## Type safety

- Annotate public functions; use `Optional`, `Union`, and generics where they remove ambiguity.
- Run `mypy --strict` in CI; suppress only with `# type: ignore[code]` and a comment.

## Profiling

- Profile before rewriting. Use `cProfile` for call counts, `line_profiler` for per-line cost.
- Optimize data structures and algorithms before micro-optimizations.

## Related references

- Python docs: https://docs.python.org/3/
- pytest docs: https://docs.pytest.org/en/stable/
- mypy docs: https://mypy.readthedocs.io/en/stable/
```

## Per-skill content briefs

| skill | replaces | pack home(s) | authority lane | canonical references | body focus |
|-------|----------|--------------|----------------|----------------------|------------|
| `python` | `async-python-patterns`, `python-performance-optimization`, `python-testing-patterns` | `language-patterns-pack` | citation | Python docs, pytest, mypy, asyncio docs | Idiomatic Python, concurrency, testing, types, profiling |
| `python-frameworks` | `django-patterns`, `django-celery`, `django-tdd`, `fastapi-patterns` (retained non-projected; used as citation prompts) | `language-patterns-pack` | citation | Django docs, FastAPI docs, Celery docs | Django, FastAPI, Celery patterns; when to choose each |
| `api-design` | `api-design-patterns`, `openapi-specification` | `api-contracts-pack` | mixed-source (OpenAPI spec vendored) | OpenAPI 3.1 spec, IETF HTTP/REST RFCs, OWASP API Security | Contract-first API design, versioning, pagination, errors, OpenAPI |
| `secure-development` | `secure-coding-practices`, `security-testing-patterns`, `threat-modeling-techniques`, `security-review` | `security-pack` | citation | OWASP Developer Guide, OWASP Testing Guide, CWE, CAPEC, NIST SP 800-53 | Secure coding, testing, threat modeling, review checklists |
| `risk-gates` (expanded) | `safety-guard` | `repo-worker-pack`, `security-pack`, `house-skills` | citation | Risk-gate literature, destructive-operation guard patterns | Add a `safety-gate` for destructive mutations; keep existing gate routing |
| `frontend-ux` | `interaction-design`, `ux-review` | `frontend-pack` | citation | WCAG, W3C HTML/CSS specs, MDN, Material Design, Apple HIG | Component/layout patterns, accessibility, interaction design, UX review |
| `playwright-testing` | `webapp-testing` | `frontend-pack` | citation | Playwright docs, W3C WebDriver | E2E web testing with Playwright: selectors, fixtures, retries, reporting |
| `mermaid-diagramming` | `mermaid-diagramming` (Claude-Cortex) | `planning-pack` | citation | Mermaid docs | Diagram types, syntax, when to use which diagram |
| `event-driven-systems` | `event-driven-architecture` | `architecture-pack` | citation | Kafka docs, RabbitMQ docs, public EDA patterns | Events vs messages, brokers, choreography/orchestration, sagas, idempotency |
| `release-engineering` | `release-analysis`, `release-prep`, `deployment-patterns` | `planning-pack`, `engineering-pack` | citation | Docker docs, Kubernetes docs, GitHub Actions docs, SRE resources | CI/CD, containers, releases, rollback, deployment patterns |
| `requirements-elicitation` | `requirements-discovery` | `planning-pack` | citation | Public requirements-engineering references | Elicit, validate, and document requirements; user stories, acceptance criteria |
| `estimation` | `development-estimation` | `planning-pack` | citation | COCOMO, Agile estimation literature | Estimate effort, risk buffers, confidence levels |
| `agentic-harness` | `agentic-os`, `autonomous-agent-harness`, `continuous-agent-loop`, `agent-harness-construction`, `dynamic-workflow-mode`, `dmux-workflows`, `ai-first-engineering` | `agentic-workflows` | citation | dmux repo, OpenAI/Anthropic docs, public agent-OS/harness papers | Agent loops, harness construction, tool/action spaces, multi-agent orchestration |
| `agent-evaluation` | `agent-eval`, `agent-self-evaluation`, `agent-architecture-audit` | `agentic-evaluation` | citation | SWE-bench, public agent-eval methodologies | Evaluate agent outputs, benchmark design, self-evaluation rubrics |
| `research-ops` | `research-ops` (ECC) | `research-pack` | citation | Evidence-based research methods, public search/evaluation references | Search, evaluate sources, synthesize evidence, cite honestly |

## Task 0 — Delete non-projected upstream source (MARK-369 phase 1)

### What to delete

All directories under:

- `sources/third_party/claude-cortex/upstream/skills/`
- `sources/third_party/ecc/upstream/skills/`

**Except** these 30 projected directories:

Claude-Cortex (16):

```
api-design-patterns
async-python-patterns
development-estimation
event-driven-architecture
interaction-design
mermaid-diagramming
python-performance-optimization
python-testing-patterns
release-analysis
release-prep
requirements-discovery
secure-coding-practices
security-testing-patterns
threat-modeling-techniques
ux-review
webapp-testing
```

ECC (14):

```
agent-architecture-audit
agent-eval
agent-harness-construction
agent-self-evaluation
agentic-os
ai-first-engineering
autonomous-agent-harness
continuous-agent-loop
deployment-patterns
dmux-workflows
dynamic-workflow-mode
research-ops
safety-guard
security-review
```

### Exact command

Use this PowerShell snippet after verifying the exception lists. It is destructive: confirm with the user before running.

```powershell
$claudeRoot = "Z:\_agent-worktrees\agent-asset-marketplace\mark-353-cortex-ecc-tier1\sources\third_party\claude-cortex\upstream\skills"
$eccRoot = "Z:\_agent-worktrees\agent-asset-marketplace\mark-353-cortex-ecc-tier1\sources\third_party\ecc\upstream\skills"

$keepClaude = @(
  "api-design-patterns","async-python-patterns","development-estimation",
  "event-driven-architecture","interaction-design","mermaid-diagramming",
  "python-performance-optimization","python-testing-patterns","release-analysis",
  "release-prep","requirements-discovery","secure-coding-practices",
  "security-testing-patterns","threat-modeling-techniques","ux-review","webapp-testing"
)
$keepEcc = @(
  "agent-architecture-audit","agent-eval","agent-harness-construction",
  "agent-self-evaluation","agentic-os","ai-first-engineering",
  "autonomous-agent-harness","continuous-agent-loop","deployment-patterns",
  "dmux-workflows","dynamic-workflow-mode","research-ops",
  "safety-guard","security-review"
)

Get-ChildItem -Directory $claudeRoot |
  Where-Object { $_.Name -notin $keepClaude } |
  Remove-Item -Recurse -Force

Get-ChildItem -Directory $eccRoot |
  Where-Object { $_.Name -notin $keepEcc } |
  Remove-Item -Recurse -Force
```

### Validation

```powershell
py -3 -m json.tool codex-marketplace\custody-pack-registry.json > $null
```

### Commit

```
MARK-369: delete non-projected Claude-Cortex and ECC upstream snapshots.

Removes all retained third-party skill directories that are not currently
projected in any marketplace pack, keeping the 30 Tier 1 conversion sources.

Generated with Devin
```

## Task 1 — `python` + `python-frameworks`

### Files to create

- `sources/first_party/skills/python/SKILL.md`
- `sources/first_party/skills/python/agents/openai.yaml`
- `sources/first_party/skills/python/assets/authority/authority.yaml`
- `sources/first_party/skills/python/assets/authority/source-map.yaml`
- `sources/first_party/skills/python/assets/authority/CITATIONS.md`
- `sources/first_party/skills/python/references/operational-guidance.md`
- `sources/first_party/skills/python-frameworks/SKILL.md`
- `sources/first_party/skills/python-frameworks/agents/openai.yaml`
- `sources/first_party/skills/python-frameworks/assets/authority/authority.yaml`
- `sources/first_party/skills/python-frameworks/assets/authority/source-map.yaml`
- `sources/first_party/skills/python-frameworks/assets/authority/CITATIONS.md`
- `sources/first_party/skills/python-frameworks/references/operational-guidance.md`

### `custody-pack-registry.json` changes

In the `language-patterns-pack` pack node:

1. Remove these entries:
   - `async-python-patterns`
   - `python-performance-optimization`
   - `python-testing-patterns`
2. Add these entries:

```json
{
  "canonical_name": "python",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/python",
  "local_path": "skills/python",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party python skill."
},
{
  "canonical_name": "python-frameworks",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/python-frameworks",
  "local_path": "skills/python-frameworks",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party python-frameworks skill."
}
```

Keep the `typescript` entry unchanged.

3. Update `notes` to:

```json
"notes": [
  "Language-patterns bundle projected from first-party source custody.",
  "Covers Python language, Python frameworks, and TypeScript."
]
```

### Stale adapters to delete later

Do not delete yet; wait until the projected snapshots are removed in Task 8:

- `adapters/codex/language-patterns-pack/async-python-patterns`
- `adapters/codex/language-patterns-pack/python-performance-optimization`
- `adapters/codex/language-patterns-pack/python-testing-patterns`

### Validation after commit

```powershell
py -3 tools/normalize_first_party_skill_sources.py --check
py -3 tools/rebuild_marketplace.py
```

### Commit

```
MARK-354: add first-party python and python-frameworks skills.

Replaces the Claude-Cortex async-python-patterns, python-performance-optimization,
and python-testing-patterns projections in language-patterns-pack.

Generated with Devin
```

## Task 2 — `api-design`

### Files to create

- `sources/first_party/skills/api-design/SKILL.md`
- `sources/first_party/skills/api-design/agents/openai.yaml`
- `sources/first_party/skills/api-design/assets/authority/authority.yaml`
- `sources/first_party/skills/api-design/assets/authority/source-map.yaml`
- `sources/first_party/skills/api-design/assets/authority/CITATIONS.md`
- `sources/first_party/skills/api-design/assets/authority/reference-source/openapi-specification/OpenAPI-Specification-3.1.0.md`
- `sources/first_party/skills/api-design/references/operational-guidance.md`

### Vendored OpenAPI spec

1. Download the OpenAPI 3.1.0 specification markdown:

```powershell
$outDir = "Z:\_agent-worktrees\agent-asset-marketplace\mark-353-cortex-ecc-tier1\sources\first_party\skills\api-design\assets\authority\reference-source\openapi-specification"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/versions/3.1.0.md" -OutFile "$outDir\OpenAPI-Specification-3.1.0.md"
```

2. Compute SHA-256 of the vendored file:

```powershell
py -3 -c "import hashlib, pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/api-design/assets/authority/reference-source/openapi-specification/OpenAPI-Specification-3.1.0.md').read_bytes()).hexdigest())"
```

3. Set that SHA in both `authority.yaml` (`authority.openapi-specification.content_sha256` and `decomposition.reconciled_against.openapi-specification`) and `source-map.yaml` (`reconciled_against.openapi-specification`).

### `api-design` `assets/authority/authority.yaml`

```yaml
schema_version: 1
custody: marketplace
lane: skills-with-mixed-source
authority:
  openapi-specification:
    title: OpenAPI Specification 3.1.0
    canonical_url: https://spec.openapis.org/oas/v3.1.0
    pinned_source_url: https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/versions/3.1.0.md
    latest_check_url: https://github.com/OAI/OpenAPI-Specification
    revision: '3.1.0'
    retrieved_at: '2026-07-21'
    content_sha256: <sha256-of-vendored-file>
    license: Apache-2.0
    license_url: https://www.apache.org/licenses/LICENSE-2.0
decomposition:
  reconciled_against:
    openapi-specification: <sha256-of-vendored-file>
  references:
  - path: references/operational-guidance.md
    source_sections:
    - API design and OpenAPI
    load_when:
    - Use when api-design operational guidance is needed.
    content_mode: first_party_synthesis
```

### `api-design` `assets/authority/source-map.yaml`

```yaml
schema_version: 1
reconciled_against:
  openapi-specification: <sha256-of-vendored-file>
references:
  - path: references/operational-guidance.md
    source_sections:
    - API design and OpenAPI
    load_when:
    - Use when api-design operational guidance is needed.
    content_mode: first_party_synthesis
```

### `custody-pack-registry.json` changes

In the `api-contracts-pack` pack node:

1. Remove:
   - `api-design-patterns`
   - `openapi-specification`
2. Add:

```json
{
  "canonical_name": "api-design",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/api-design",
  "local_path": "skills/api-design",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party api-design skill."
}
```

3. Delete first-party source `sources/first_party/skills/openapi-specification` (it is merged into `api-design`).
4. Update `notes` to:

```json
"notes": [
  "Contract-design bundle projected from first-party source custody.",
  "The api-design skill replaces the former api-design-patterns and openapi-specification entries."
]
```

### Stale adapters to delete later

- `adapters/codex/api-contracts-pack/api-design-patterns`

### Validation after commit

```powershell
py -3 tools/validate_authority_assets.py
py -3 tools/rebuild_marketplace.py
```

### Commit

```
MARK-355: add first-party api-design skill and retire openapi-specification.

Replaces api-design-patterns and openapi-specification in api-contracts-pack.
Vendors the OpenAPI 3.1.0 spec under assets/authority/reference-source/.

Generated with Devin
```

## Task 3 — `secure-development` + `risk-gates` expansion

### Files to create

- `sources/first_party/skills/secure-development/SKILL.md`
- `sources/first_party/skills/secure-development/agents/openai.yaml`
- `sources/first_party/skills/secure-development/assets/authority/authority.yaml`
- `sources/first_party/skills/secure-development/assets/authority/source-map.yaml`
- `sources/first_party/skills/secure-development/assets/authority/CITATIONS.md`
- `sources/first_party/skills/secure-development/references/operational-guidance.md`

### `risk-gates` edits

1. Add to `sources/first_party/skills/risk-gates/SKILL.md` frontmatter `metadata.use_when`:

```yaml
- Use when about to run a destructive operation (delete, drop, rewrite history, bulk mutation) that could cause data loss or exceed authority.
```

2. Add a `safety-gate` row to the routing table in `sources/first_party/skills/risk-gates/SKILL.md`:

```markdown
| safety-gate | About to run a destructive operation, delete/truncate/drop, rewrite history, or bulk-mutate a durable surface where the cost of a mistake is high. | The operation is ordinary, reversible, or already protected by an explicit user confirmation in the destination workflow. | `references/gates/safety-gate.md` |
```

3. Create `sources/first_party/skills/risk-gates/references/gates/safety-gate.md`:

```markdown
# Safety gate

Use before a destructive or irreversible action.

## Trigger

- Delete, truncate, drop, rewrite history, bulk update, or permission change.
- Any operation where recovery is costly or impossible.

## Green requirements

- The target is explicitly identified.
- The scope is confirmed by source or user authority.
- A backup, dry-run, or rollback path exists when feasible.
- The action is not broader than requested.

## Amber/red signals

- Missing authority for the target or scope.
- No recovery path and no explicit user confirmation.
- The operation would affect data outside the current task scope.

## Mode

- Use `internal_mode` for clearly scoped, recoverable actions.
- Use `interactive_mode` for destructive actions without a clear recovery path.
- Use `blocked_mode` when authority or target evidence is missing.
```

4. If `sources/first_party/skills/risk-gates/agents/openai.yaml` is missing `version` or `metadata`, rewrite it to the standard first-party shape:

```yaml
version: 1
metadata:
  skill_name: risk-gates
  plugin: repo-worker-pack
  source_category: first_party
interface:
  display_name: Risk Gates
  short_description: Use when a pre-action risk gate is needed before a mutation, dispatch, canon claim, analogy, resolution, or destructive operation.
  default_prompt: Use risk-gates before an action that could mutate a durable surface, dispatch work, make a canon claim, rely on an analogy, treat a claim as resolved, act on feedback, or run a destructive operation.
policy:
  allow_implicit_invocation: true
```

5. Add authority assets to `risk-gates`:
   - `sources/first_party/skills/risk-gates/assets/authority/authority.yaml`
   - `sources/first_party/skills/risk-gates/assets/authority/source-map.yaml`
   - `sources/first_party/skills/risk-gates/assets/authority/CITATIONS.md`
   - `sources/first_party/skills/risk-gates/references/operational-guidance.md`

Use the standard `skills-with-citation` template but point the `references` entry at `references/operational-guidance.md`. Canonical references: safety-engineering literature, destructive-operation guard patterns.

### `custody-pack-registry.json` changes

In the `security-pack` pack node:

1. Remove:
   - `secure-coding-practices`
   - `security-testing-patterns`
   - `threat-modeling-techniques`
   - `safety-guard`
   - `security-review`
2. Add:

```json
{
  "canonical_name": "secure-development",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/secure-development",
  "local_path": "skills/secure-development",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party secure-development skill."
},
{
  "canonical_name": "risk-gates",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/risk-gates",
  "local_path": "skills/risk-gates",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party risk-gates skill, expanded with a safety gate for destructive operations."
}
```

3. Clear `source_ledger` (it listed upstream paths that are now retired):

```json
"source_ledger": []
```

4. Update `notes` to:

```json
"notes": [
  "Security pack projected from first-party source custody.",
  "secure-development replaces the former Claude-Cortex and ECC security skills.",
  "risk-gates is projected verbatim with an expanded safety gate for destructive operations."
]
```

### Stale adapters to delete later

- `adapters/codex/security-pack/safety-guard`
- `adapters/codex/security-pack/secure-coding-practices`
- `adapters/codex/security-pack/security-review`
- `adapters/codex/security-pack/security-testing-patterns`
- `adapters/codex/security-pack/threat-modeling-techniques`

### Validation after commit

```powershell
py -3 tools/validate_authority_assets.py
py -3 tools/rebuild_marketplace.py
```

### Commit

```
MARK-356: add secure-development and expand risk-gates safety gate.

Replaces the Claude-Cortex and ECC security skills in security-pack with the
first-party secure-development skill. Expands risk-gates with a safety gate
for destructive operations.

Generated with Devin
```

## Task 4 — `frontend-ux` + `playwright-testing`

### Files to create

- `sources/first_party/skills/frontend-ux/SKILL.md`
- `sources/first_party/skills/frontend-ux/agents/openai.yaml`
- `sources/first_party/skills/frontend-ux/assets/authority/authority.yaml`
- `sources/first_party/skills/frontend-ux/assets/authority/source-map.yaml`
- `sources/first_party/skills/frontend-ux/assets/authority/CITATIONS.md`
- `sources/first_party/skills/frontend-ux/references/operational-guidance.md`
- `sources/first_party/skills/playwright-testing/SKILL.md`
- `sources/first_party/skills/playwright-testing/agents/openai.yaml`
- `sources/first_party/skills/playwright-testing/assets/authority/authority.yaml`
- `sources/first_party/skills/playwright-testing/assets/authority/source-map.yaml`
- `sources/first_party/skills/playwright-testing/assets/authority/CITATIONS.md`
- `sources/first_party/skills/playwright-testing/references/operational-guidance.md`

### `custody-pack-registry.json` changes

In the `frontend-pack` pack node:

1. Remove:
   - `interaction-design`
   - `ux-review`
   - `webapp-testing`
2. Add:

```json
{
  "canonical_name": "frontend-ux",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/frontend-ux",
  "local_path": "skills/frontend-ux",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party frontend-ux skill."
},
{
  "canonical_name": "playwright-testing",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/playwright-testing",
  "local_path": "skills/playwright-testing",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party playwright-testing skill."
}
```

3. Update `notes` to:

```json
"notes": [
  "Frontend bundle projected from retained feature-sliced custody and first-party skills.",
  "frontend-ux replaces interaction-design and ux-review; playwright-testing replaces webapp-testing."
]
```

### Stale adapters

None (the retired skills were verbatim and had no `adapters/codex/frontend-pack` overlays).

### Validation after commit

```powershell
py -3 tools/validate_authority_assets.py
py -3 tools/rebuild_marketplace.py
```

### Commit

```
MARK-357: add frontend-ux and playwright-testing first-party skills.

Replaces interaction-design, ux-review, and webapp-testing in frontend-pack.

Generated with Devin
```

## Task 5 — `mermaid-diagramming` + `event-driven-systems`

### Files to create

- `sources/first_party/skills/mermaid-diagramming/SKILL.md`
- `sources/first_party/skills/mermaid-diagramming/agents/openai.yaml`
- `sources/first_party/skills/mermaid-diagramming/assets/authority/authority.yaml`
- `sources/first_party/skills/mermaid-diagramming/assets/authority/source-map.yaml`
- `sources/first_party/skills/mermaid-diagramming/assets/authority/CITATIONS.md`
- `sources/first_party/skills/mermaid-diagramming/references/operational-guidance.md`
- `sources/first_party/skills/event-driven-systems/SKILL.md`
- `sources/first_party/skills/event-driven-systems/agents/openai.yaml`
- `sources/first_party/skills/event-driven-systems/assets/authority/authority.yaml`
- `sources/first_party/skills/event-driven-systems/assets/authority/source-map.yaml`
- `sources/first_party/skills/event-driven-systems/assets/authority/CITATIONS.md`
- `sources/first_party/skills/event-driven-systems/references/operational-guidance.md`

### `custody-pack-registry.json` changes

In the `planning-pack` pack node:

1. Remove:
   - `mermaid-diagramming` (the third-party Claude-Cortex entry)
2. Add:

```json
{
  "canonical_name": "mermaid-diagramming",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/mermaid-diagramming",
  "local_path": "skills/mermaid-diagramming",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party mermaid-diagramming skill."
}
```

In the `architecture-pack` pack node:

1. Remove:
   - `event-driven-architecture`
2. Add:

```json
{
  "canonical_name": "event-driven-systems",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/event-driven-systems",
  "local_path": "skills/event-driven-systems",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party event-driven-systems skill."
}
```

3. Update `notes` for both packs to reflect the new first-party sources.

### Stale adapters

None for `mermaid-diagramming` or `event-driven-architecture` (they were verbatim).

### Validation after commit

```powershell
py -3 tools/validate_authority_assets.py
py -3 tools/rebuild_marketplace.py
```

### Commit

```
MARK-358: add first-party mermaid-diagramming and event-driven-systems skills.

Replaces the Claude-Cortex mermaid-diagramming and event-driven-architecture
projections in planning-pack and architecture-pack.

Generated with Devin
```

## Task 6 — `release-engineering` + `requirements-elicitation` + `estimation`

### Files to create

For each skill `release-engineering`, `requirements-elicitation`, `estimation`:

- `sources/first_party/skills/<skill>/SKILL.md`
- `sources/first_party/skills/<skill>/agents/openai.yaml`
- `sources/first_party/skills/<skill>/assets/authority/authority.yaml`
- `sources/first_party/skills/<skill>/assets/authority/source-map.yaml`
- `sources/first_party/skills/<skill>/assets/authority/CITATIONS.md`
- `sources/first_party/skills/<skill>/references/operational-guidance.md`

### `custody-pack-registry.json` changes

In the `planning-pack` pack node:

1. Remove:
   - `development-estimation`
   - `release-analysis`
   - `release-prep`
   - `requirements-discovery`
2. Add:

```json
{
  "canonical_name": "release-engineering",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/release-engineering",
  "local_path": "skills/release-engineering",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party release-engineering skill."
},
{
  "canonical_name": "requirements-elicitation",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/requirements-elicitation",
  "local_path": "skills/requirements-elicitation",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party requirements-elicitation skill."
},
{
  "canonical_name": "estimation",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/estimation",
  "local_path": "skills/estimation",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party estimation skill."
}
```

In the `engineering-pack` pack node:

1. Remove:
   - `deployment-patterns`
2. Add:

```json
{
  "canonical_name": "release-engineering",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/release-engineering",
  "local_path": "skills/release-engineering",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party release-engineering skill into the engineering pack."
}
```

3. Update `notes` for both packs.

### Stale adapters

None for the retired skills (they were verbatim).

### Validation after commit

```powershell
py -3 tools/validate_authority_assets.py
py -3 tools/rebuild_marketplace.py
```

### Commit

```
MARK-359: add release-engineering, requirements-elicitation, and estimation.

Replaces development-estimation, release-analysis, release-prep,
requirements-discovery, and deployment-patterns in planning-pack and
engineering-pack.

Generated with Devin
```

## Task 7 — `agentic-harness` + `agent-evaluation` + `research-ops`

### Files to create

For each skill `agentic-harness`, `agent-evaluation`, `research-ops`:

- `sources/first_party/skills/<skill>/SKILL.md`
- `sources/first_party/skills/<skill>/agents/openai.yaml`
- `sources/first_party/skills/<skill>/assets/authority/authority.yaml`
- `sources/first_party/skills/<skill>/assets/authority/source-map.yaml`
- `sources/first_party/skills/<skill>/assets/authority/CITATIONS.md`
- `sources/first_party/skills/<skill>/references/operational-guidance.md`

### `custody-pack-registry.json` changes

In the `agentic-workflows` pack node:

1. Remove:
   - `agent-harness-construction`
   - `autonomous-agent-harness`
   - `continuous-agent-loop`
   - `dynamic-workflow-mode`
   - `dmux-workflows`
   - `agentic-os`
2. Add:

```json
{
  "canonical_name": "agentic-harness",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/agentic-harness",
  "local_path": "skills/agentic-harness",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party agentic-harness skill."
}
```

In the `agentic-evaluation` pack node:

1. Remove:
   - `agent-self-evaluation`
   - `agent-eval`
   - `agent-architecture-audit`
2. Add:

```json
{
  "canonical_name": "agent-evaluation",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/agent-evaluation",
  "local_path": "skills/agent-evaluation",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party agent-evaluation skill."
}
```

In the `research-pack` pack node:

1. Remove:
   - `research-ops` (the ECC entry)
2. Add:

```json
{
  "canonical_name": "research-ops",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/research-ops",
  "local_path": "skills/research-ops",
  "import_status": "imported",
  "copy_expectation": "byte_identical",
  "provenance_note": "Projected verbatim from the first-party research-ops skill."
}
```

In the `engineering-pack` pack node:

1. Remove:
   - `ai-first-engineering`

`observability` remains.

2. Update `notes` for all affected packs.

### Stale adapters to delete later

- `adapters/codex/agentic-evaluation/agent-self-evaluation`

### Validation after commit

```powershell
py -3 tools/validate_authority_assets.py
py -3 tools/rebuild_marketplace.py
```

### Commit

```
MARK-360: add agentic-harness, agent-evaluation, and research-ops.

Consolidates the ECC agent workflow, evaluation, and research skills into
first-party source custody. Removes ai-first-engineering from engineering-pack.

Generated with Devin
```

## Task 8 — Retire mega-packs and delete projected snapshots

### `custody-pack-registry.json` changes

Remove the two mega-pack nodes at the end of the `packs` array:

1. `codex-cortex` (the node with `"source_family": "claude-cortex"`, `"mega_pack": "codex-cortex"`)
2. `everything-codex-code` (the node with `"source_family": "ecc"`, `"mega_pack": "everything-codex-code"`)

### Delete projected upstream snapshots

After the marketplace rebuild in Task 7 passes, delete these 30 directories:

Claude-Cortex:

```
sources/third_party/claude-cortex/upstream/skills/api-design-patterns
sources/third_party/claude-cortex/upstream/skills/async-python-patterns
sources/third_party/claude-cortex/upstream/skills/development-estimation
sources/third_party/claude-cortex/upstream/skills/event-driven-architecture
sources/third_party/claude-cortex/upstream/skills/interaction-design
sources/third_party/claude-cortex/upstream/skills/mermaid-diagramming
sources/third_party/claude-cortex/upstream/skills/python-performance-optimization
sources/third_party/claude-cortex/upstream/skills/python-testing-patterns
sources/third_party/claude-cortex/upstream/skills/release-analysis
sources/third_party/claude-cortex/upstream/skills/release-prep
sources/third_party/claude-cortex/upstream/skills/requirements-discovery
sources/third_party/claude-cortex/upstream/skills/secure-coding-practices
sources/third_party/claude-cortex/upstream/skills/security-testing-patterns
sources/third_party/claude-cortex/upstream/skills/threat-modeling-techniques
sources/third_party/claude-cortex/upstream/skills/ux-review
sources/third_party/claude-cortex/upstream/skills/webapp-testing
```

ECC:

```
sources/third_party/ecc/upstream/skills/agent-architecture-audit
sources/third_party/ecc/upstream/skills/agent-eval
sources/third_party/ecc/upstream/skills/agent-harness-construction
sources/third_party/ecc/upstream/skills/agent-self-evaluation
sources/third_party/ecc/upstream/skills/agentic-os
sources/third_party/ecc/upstream/skills/ai-first-engineering
sources/third_party/ecc/upstream/skills/autonomous-agent-harness
sources/third_party/ecc/upstream/skills/continuous-agent-loop
sources/third_party/ecc/upstream/skills/deployment-patterns
sources/third_party/ecc/upstream/skills/dmux-workflows
sources/third_party/ecc/upstream/skills/dynamic-workflow-mode
sources/third_party/ecc/upstream/skills/research-ops
sources/third_party/ecc/upstream/skills/safety-guard
sources/third_party/ecc/upstream/skills/security-review
```

If the parent `skills` directories are empty after deletion, remove:

- `sources/third_party/claude-cortex/upstream/skills`
- `sources/third_party/ecc/upstream/skills`

If `upstream` becomes empty, remove the upstream roots as well.

### Delete stale adapter trees

```
adapters/codex/api-contracts-pack/api-design-patterns
adapters/codex/language-patterns-pack/async-python-patterns
adapters/codex/language-patterns-pack/python-performance-optimization
adapters/codex/language-patterns-pack/python-testing-patterns
adapters/codex/security-pack/safety-guard
adapters/codex/security-pack/secure-coding-practices
adapters/codex/security-pack/security-review
adapters/codex/security-pack/security-testing-patterns
adapters/codex/security-pack/threat-modeling-techniques
adapters/codex/agentic-evaluation/agent-self-evaluation
```

If a parent directory (`api-contracts-pack`, `language-patterns-pack`, `security-pack`, `agentic-evaluation`) becomes empty except `INDEX.md`, remove the parent as well.

### Rebuild and validate

```powershell
py -3 tools/rebuild_marketplace.py
py -3 tools/check_marketplace.py
```

`rebuild_marketplace.py` will:

1. Regenerate `plugin-roots.json` without `codex-cortex` and `everything-codex-code`.
2. Prune `codex-marketplace/plugins/codex-cortex` and `codex-marketplace/plugins/everything-codex-code`.
3. Regenerate all bundle manifests, source maps, provenance maps, zips, and indexes.

### Commit

```
MARK-361: retire codex-cortex and everything-codex-code mega-packs.

Removes the mega-pack nodes from custody-pack-registry.json, prunes their
projected plugin roots, deletes the 30 projected upstream snapshots, and
deletes stale adapters.

Generated with Devin
```

## Final validation and PR

### Validation command sequence

```powershell
py -3 tools/rebuild_marketplace.py
py -3 tools/check_marketplace.py
```

Both must pass with no diffs. `check_marketplace.py` is the CI gate.

### PR checklist

- [ ] Branch `mark-353-cortex-ecc-tier1` is pushed.
- [ ] All 15 Tier 1 skills are in `sources/first_party/skills/`.
- [ ] `custody-pack-registry.json` has no `claude-cortex` or `ecc` entries in topical packs.
- [ ] `codex-cortex` and `everything-codex-code` are removed from `plugin-roots.json` and `custody-pack-registry.json`.
- [ ] The 30 projected upstream snapshots are deleted.
- [ ] Stale `adapters/codex/` overlays are deleted.
- [ ] `py -3 tools/rebuild_marketplace.py` passes.
- [ ] `py -3 tools/check_marketplace.py` passes.

### PR title

`MARK-353: convert Cortex/ECC Tier 1 remnants to first-party skills and retire mega-packs`

### PR body

```markdown
## Summary

- Converts 30 projected Claude-Cortex/ECC third-party skill remnants into 15 first-party skills.
- Deletes all non-projected and then projected upstream snapshots.
- Retires the `codex-cortex` and `everything-codex-code` mega-packs.
- Removes stale `adapters/codex/` overlays.
- Regenerates all marketplace surfaces from `custody-pack-registry.json`.

## Test plan

- [ ] `py -3 tools/rebuild_marketplace.py`
- [ ] `py -3 tools/check_marketplace.py`

Generated with Devin
```

## Interim-state notes

- Task 0 leaves 30 upstream snapshots in place; they are removed in Task 8.
- Tasks 1-7 temporarily leave stale adapter directories and projected upstream snapshots; these are cleaned in Task 8.
- `py -3 tools/check_marketplace.py` is expected to fail between Tasks 1-7 if run before Task 8, because the mega-packs still reference the retired `claude-cortex`/`ecc` entries. Use `py -3 tools/rebuild_marketplace.py` after each cluster and accept that `check_marketplace.py` is the final gate.

## SDD confidence rating

**7/10**

Strengths:

- Mechanical pack/registry changes are fully specified.
- File paths, command sequences, commit messages, and PR text are exact.
- The sample `python` skill provides a concrete pattern to mirror.

Gaps that require in-flight decisions during implementation:

1. The exact prose for the 14 non-sample skills and their `references/operational-guidance.md` files is not pre-written; the content briefs and templates define the boundary.
2. `api-design` requires downloading and recording the OpenAPI 3.1.0 spec SHA at implementation time.
3. The design proposed `mermaid-diagramming` (and optionally `playwright-testing`) as source-backed; this plan treats both as citation-based to avoid unbounded vendored-doc acquisition. Sign-off should confirm or override.
4. `risk-gates` expansion is small but requires editing an existing first-party skill without overwriting its existing gate reference docs.
