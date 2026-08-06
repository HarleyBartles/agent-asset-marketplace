# [Authoritative First-Party Skill Enrichment] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Every skill task also requires the local `mark-skill-authoring` skill and `superpowers-plus:writing-skills` to author operational prose under the 500-word `SKILL.md` body limit.

**Goal:** Replace the agreed overlapping third-party specialist skills with authoritative, first-party, source-backed or citation-backed skills, landed in a single epic branch and one master PR to `main`.

**Architecture:** Each skill lives as an immutable first-party source root under `sources/first_party/skills/<skill>/` and is projected into the appropriate Codex marketplace pack through `codex-marketplace/custody-pack-registry.json`. Source-backed lanes keep vendored snapshots and decomposition in `assets/authority/`; citation-backed lanes keep scholarly evidence in `assets/authority/CITATIONS.md`. A new `dotnet-pack` plugin root replaces `dotnet-kit`, and the full marketplace rebuild stack validates the projection.

**Tech Stack:** Python 3, YAML, Markdown, Git, `curl`, `tar`; repo tooling `tools/rebuild_marketplace.py` and `tools/check_marketplace.py`; local skills `mark-skill-authoring` and `superpowers-plus:writing-skills`.

## Global Constraints

- One epic branch: `harleydbartles/afpse-epic` from `origin/main`.
- One master PR to `main`; no per-skill PRs.
- `sources/third_party/` is immutable for retained snapshots; the drained `dotnet-claude-kit` upstream snapshot is removed in Task 16.
- Mega-pack duplicates in `codex-cortex`, `everything-codex-code`, `house-skills`, `unslop-plus`, and `game-studio` are retained as provenance collections this pass.
- Only one new plugin root: `dotnet-pack` replacing `dotnet-kit`.
- `MARK-352` produces a decision matrix only; it does not implement additional skills.
- All first-party skills use MIT license and the canonical first-party frontmatter from `.agents/doctrine/skill-standards-policy.md`.
- Operational `SKILL.md` body is under 500 words; no inline citations.
- Source-backed skills store vendored source in `assets/authority/reference-source/` and record `content_sha256`.
- Citation-backed skills keep no vendored source; evidence is in `assets/authority/CITATIONS.md`.
- Each skill branch is branched from the current `harleydbartles/afpse-epic` HEAD and fast-merged back after validation.

## Common Scaffolding and Templates

Use these exact templates for every skill. Replace `<skill>`, `<Skill Title>`, `<pack>`, `<lane>`, `<canonical-url>`, `<pinned-source-url>`, `<revision>`, `<YYYY-MM-DD>`, `<sha256>`, `<license-name>`, `<license-url>`, `<content-mode>`, and `<source-sections>` with the concrete values from the per-skill brief below. `<source-sections>` is a YAML flow list (e.g., `["Strategic Design", "Tactical Design", "Building Blocks"]`). Do not commit files containing literal `<...>` placeholders.

### `SKILL.md` template

```markdown
---
name: <skill>
description: <Use when ... . Do not use when ... .>
metadata:
  source-id: <skill>
  source-path: sources/first_party/skills/<skill>/SKILL.md
  provenance-name: <Skill Title> first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: <Use when ... .>
  use_when:
  - <Use when ...>
  do_not_use_when:
  - <Do not use when another more specific skill owns this task.>
license: MIT
---

# <Skill Title>

## Overview
<Core principle in 1-2 sentences.>

## When to Use
- <Trigger / symptom 1>
- <Trigger / symptom 2>
- <Do not use when ...>

## Core Pattern
<Before/after comparison or step-by-step guidance.>

## Common Mistakes
- <Mistake 1 and fix>
- <Mistake 2 and fix>
```

### `agents/openai.yaml` template

```yaml
version: 1
metadata:
  skill_name: <skill>
  plugin: <pack>
  source_category: first_party
interface:
  display_name: <Skill Title>
  short_description: <Use when ... .>
  default_prompt: <Use when ... .>
policy:
  allow_implicit_invocation: true
```

### `assets/authority/authority.yaml` template

```yaml
schema_version: 1
custody: marketplace
lane: <lane>
authority:
  title: "<Skill Title>"
  canonical_url: <canonical-url>
  pinned_source_url: <pinned-source-url>
  latest_check_url: <canonical-url>
  revision: <revision>
  retrieved_at: <YYYY-MM-DD>
  content_sha256: <sha256>
  license: <license-name>
  license_url: <license-url>
decomposition:
  reconciled_against: <sha256>
  references:
  - path: references/operational-guidance.md
    source_sections: <source-sections>
    load_when:
    - Use when <skill> operational guidance is needed.
    content_mode: <content-mode>
```

### `assets/authority/source-map.yaml` template

```yaml
schema_version: 1
reconciled_against: <sha256>
references:
- path: references/operational-guidance.md
  source_sections: <source-sections>
  load_when:
  - Use when <skill> operational guidance is needed.
  content_mode: <content-mode>
```

### `assets/authority/CITATIONS.md` template

```markdown
# Authority record for <skill>

## Scholarly citation

<Citation list or source reference.>

## Derivation boundary

<What operational guidance is derived from the authority and what remains outside it.>

## Attribution

<License and attribution obligations.>

## Human review

- Reviewer: Harley Bartles
- Date: <YYYY-MM-DD>
- Decision: Approved for first-party operational guidance. Operational SKILL.md text contains no inline citations.
```

### Source download helpers

For a single web-page authority:

```bash
curl.exe -L -o sources/first_party/skills/<skill>/assets/authority/reference-source/<skill>.html <canonical-url>
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/<skill>/assets/authority/reference-source/<skill>.html').read_bytes()).hexdigest())"
```

For a single GitHub repository:

```bash
curl.exe -L -o sources/first_party/skills/<skill>/assets/authority/reference-source/<skill>.tar.gz https://github.com/<owner>/<repo>/archive/refs/heads/<branch>.tar.gz
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/<skill>/assets/authority/reference-source/<skill>.tar.gz').read_bytes()).hexdigest())"
```

For a citation-backed skill, download the primary authority to the scratch folder (not committed), compute the SHA-256, then delete the scratch file:

```bash
New-Item -ItemType Directory -Force -Path ../_agent-scratch/agent-asset-marketplace/afpse-epic
curl.exe -L -o ../_agent-scratch/agent-asset-marketplace/afpse-epic/<skill>.html <canonical-url>
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('../_agent-scratch/agent-asset-marketplace/afpse-epic/<skill>.html').read_bytes()).hexdigest())"
Remove-Item ../_agent-scratch/agent-asset-marketplace/afpse-epic/<skill>.html
```

---

### Task 1: MARK-339 — Establish the authority inventory and migration baseline

**Files:**
- Create: `provenance/afpse-authority-inventory.md`
- Modify: `harleydbartles/afpse-epic` branch (create it if it does not exist)

**Interfaces:**
- Consumes: `origin/main`.
- Produces: `harleydbartles/afpse-epic` branch; baseline doc used by all skill subagents.

- [ ] **Step 1: Create the epic branch from `main`**

```bash
git fetch origin
git checkout origin/main
git checkout -b harleydbartles/afpse-epic
```

Expected: `git branch --show-current` prints `harleydbartles/afpse-epic`.

- [ ] **Step 2: Write the authority inventory baseline**

Create `provenance/afpse-authority-inventory.md` with the table from the design spec:

```markdown
# Authoritative First-Party Skill Enrichment — Authority Inventory

| Issue | Skill | Lane | Primary pack | Replaced third-party entries | Execution branch |
|---|---|---|---|---|---|
| MARK-340 | `ddd` | skills-with-source | `architecture-pack` | `dotnet-claude-kit` `ddd` | `harleydbartles/mark-340-re-custody-ddd-from-the-eric-evans-ddd-reference` |
| MARK-341 | `cqrs` | skills-with-citation | `architecture-pack` | `claude-cortex` `cqrs-event-sourcing` | `harleydbartles/mark-341-split-cqrs-and-event-sourcing-into-clean-room-citation` |
| MARK-341 | `event-sourcing` | skills-with-citation | `architecture-pack` | same as `cqrs` | same as `cqrs` |
| MARK-342 | `clean-architecture` | skills-with-citation | `architecture-pack` | `dotnet-claude-kit` `clean-architecture` | `harleydbartles/mark-342-create-clean-architecture-and-hexagonal-architecture-citation-backed` |
| MARK-342 | `hexagonal-architecture` | skills-with-citation | `architecture-pack` | none | same as `clean-architecture` |
| MARK-343 | `owasp-top-ten` | skills-with-source | `security-pack` | `claude-cortex` `owasp-top-10` | `harleydbartles/mark-343-re-custody-owasp-top-ten-and-establish-an-asvs-verification` |
| MARK-344 | `openapi-specification` | skills-with-source | `api-contracts-pack` | `claude-cortex` `openapi-specification` | `harleydbartles/mark-344-re-custody-the-openapi-specification-specialist-skill` |
| MARK-345 | `wcag` | skills-with-source | `frontend-pack` | `claude-cortex` `accessibility-audit` | `harleydbartles/mark-345-re-custody-the-wcag-accessibility-audit-specialist-skill` |
| MARK-346 | `dotnet` | skills-with-source | `dotnet-pack` | `dotnet-claude-kit` `modern-csharp`, `ef-core`, `testing`, `clean-architecture`, `ddd`, `vertical-slice` | `harleydbartles/mark-346-create-the-first-party-net-ecosystem-skill-and-migrate` |
| MARK-347 | `typescript` | skills-with-source | `language-patterns-pack` | `claude-cortex` `typescript-advanced-patterns` | `harleydbartles/mark-347-create-the-first-party-typescript-ecosystem-skill` |
| MARK-348 | `react` | skills-with-source | `frontend-pack` | `claude-cortex` `react-performance-optimization` | `harleydbartles/mark-348-create-the-first-party-react-ecosystem-skill` |
| MARK-349 | `web-styling` | skills-with-source if licenses permit; otherwise skills-with-citation | `frontend-pack` | none | `harleydbartles/mark-349-create-the-cross-framework-web-styling-skill` |
| MARK-350 | `observability` | skills-with-source | `engineering-pack` | none | `harleydbartles/mark-350-create-the-opentelemetry-observability-skill` |
| MARK-351 | `web-identity` | skills-with-citation | `security-pack` | none | `harleydbartles/mark-351-create-the-cross-stack-web-identity-citation-backed-skill` |
```

- [ ] **Step 3: Commit the baseline**

```bash
git add provenance/afpse-authority-inventory.md
git commit -m "docs: MARK-339 authority inventory and migration baseline"
git push -u origin harleydbartles/afpse-epic
```

Expected: branch published to origin.

### Task 2: MARK-340 — Re-custody `ddd` from Eric Evans' DDD Reference

**Files:**
- Create: `sources/first_party/skills/ddd/SKILL.md`
- Create: `sources/first_party/skills/ddd/agents/openai.yaml`
- Create: `sources/first_party/skills/ddd/references/operational-guidance.md`
- Create: `sources/first_party/skills/ddd/assets/authority/authority.yaml`
- Create: `sources/first_party/skills/ddd/assets/authority/source-map.yaml`
- Create: `sources/first_party/skills/ddd/assets/authority/CITATIONS.md`
- Create: `sources/first_party/skills/ddd/assets/authority/reference-source/ddd.html`

**Interfaces:**
- Consumes: `harleydbartles/afpse-epic`.
- Produces: Skill `ddd` in `architecture-pack`; registry snippet below.

Skill values:
- `<skill>` = `ddd`
- `<Skill Title>` = `DDD`
- `<pack>` = `architecture-pack`
- `<lane>` = `skills-with-source`
- `<canonical-url>` = `https://www.domainlanguage.com/ddd/reference/`
- `<pinned-source-url>` = `https://www.domainlanguage.com/ddd/reference/`
- `<revision>` = `current`
- `<license-name>` = `Copyright Eric Evans / Domain Language; reference extraction`
- `<license-url>` = `https://www.domainlanguage.com/ddd/reference/`
- `<content-mode>` = `licensed_adaptation`
- `<source-sections>` = `["Strategic Design", "Tactical Design", "Building Blocks"]`

Content brief for `references/operational-guidance.md`:
- Define bounded context and ubiquitous language before modeling.
- Strategic patterns: bounded context, context mapping, subdomain types.
- Tactical patterns: aggregates, entities, value objects, domain events, repositories, services, modules.
- When to use DDD (complex domains) and when not to (simple CRUD).

`SKILL.md` description: "Use when modeling a complex business domain, defining bounded contexts, or choosing tactical DDD patterns. Do not use when the domain is simple CRUD or when a more specific skill already owns the abstraction."

- [ ] **Step 1: Branch from the epic**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
git checkout -b harleydbartles/mark-340-re-custody-ddd-from-the-eric-evans-ddd-reference
```

- [ ] **Step 2: Scaffold the skill**

```bash
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name ddd --custody marketplace --lane skills-with-source
```

Expected: `sources/first_party/skills/ddd/` created with `SKILL.md`, `references/.gitkeep`, `assets/authority/authority.yaml`, `assets/authority/source-map.yaml`, `assets/authority/CITATIONS.md`, `assets/authority/reference-source/.gitkeep`.

- [ ] **Step 3: Download the canonical source**

```bash
curl.exe -L -o sources/first_party/skills/ddd/assets/authority/reference-source/ddd.html https://www.domainlanguage.com/ddd/reference/
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/ddd/assets/authority/reference-source/ddd.html').read_bytes()).hexdigest())"
```

Expected: a 64-character SHA-256 hash. Use it as `<sha256>`.

- [ ] **Step 4: Replace `.gitkeep` and write the reference file**

```bash
Remove-Item sources/first_party/skills/ddd/assets/authority/reference-source/.gitkeep
Remove-Item sources/first_party/skills/ddd/references/.gitkeep
```

Create `sources/first_party/skills/ddd/references/operational-guidance.md` using the content brief above. Invoke `superpowers-plus:writing-skills` and `mark-skill-authoring` to produce operational prose under the 500-word `SKILL.md` body limit.

- [ ] **Step 5: Write `SKILL.md` and `agents/openai.yaml`**

Use the Common Templates with the values above. The `description` is: "Use when modeling a complex business domain, defining bounded contexts, or choosing tactical DDD patterns. Do not use when the domain is simple CRUD or when a more specific skill already owns the abstraction."

- [ ] **Step 6: Write `assets/authority/authority.yaml`, `source-map.yaml`, and `CITATIONS.md`**

Use the Common Templates. `CITATIONS.md` content:

```markdown
# Authority record for ddd

## Scholarly citation

- Eric Evans. "Domain-Driven Design Reference." https://www.domainlanguage.com/ddd/reference/ (accessed <YYYY-MM-DD>).
- Operational guidance extracted from the DDD Reference definitions of strategic and tactical design.

## Derivation boundary

- Derived: bounded context, ubiquitous language, domain model, aggregates, entities, value objects, domain events, repositories, factories, services, modules.
- Outside scope: full implementation of Evans' book; upstream code samples; tool-specific modeling software.

## Attribution

- Copyright Eric Evans / Domain Language, Inc.
- Vendored page snapshot used under reference extraction; operational prose is MIT-licensed first-party synthesis.

## Human review

- Reviewer: Harley Bartles
- Date: <YYYY-MM-DD>
- Decision: Approved. Operational SKILL.md text contains no inline citations.
```

- [ ] **Step 7: Validate the skill**

```bash
py -3 tools/validate_authority_assets.py
```

Expected: no errors for `sources/first_party/skills/ddd`.

- [ ] **Step 8: Run first-party normalization**

```bash
py -3 tools/normalize_first_party_skill_sources.py
```

Expected: `OK first-party skill sources: 0 file(s) normalized` if the template is already canonical, or `WROTE ...` lines followed by `OK first-party skill sources: N file(s) normalized`.

- [ ] **Step 9: Commit and push**

```bash
git add sources/first_party/skills/ddd
git commit -m "feat(MARK-340): re-custody ddd from Eric Evans DDD Reference"
git push -u origin harleydbartles/mark-340-re-custody-ddd-from-the-eric-evans-ddd-reference
```

- [ ] **Step 10: Record the registry snippet**

Save for Task 16:

```json
{
  "canonical_name": "ddd",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/ddd",
  "local_path": "skills/ddd",
  "provenance_note": "Projected verbatim from the first-party ddd skill.",
  "copy_expectation": "byte_identical"
}
```

### Task 3: MARK-341 — Split `cqrs` and `event-sourcing` into clean-room citation-backed skills

**Files:**
- Create: `sources/first_party/skills/cqrs/SKILL.md`
- Create: `sources/first_party/skills/cqrs/agents/openai.yaml`
- Create: `sources/first_party/skills/cqrs/references/operational-guidance.md`
- Create: `sources/first_party/skills/cqrs/assets/authority/authority.yaml`
- Create: `sources/first_party/skills/cqrs/assets/authority/source-map.yaml`
- Create: `sources/first_party/skills/cqrs/assets/authority/CITATIONS.md`
- Create: `sources/first_party/skills/event-sourcing/SKILL.md`
- Create: `sources/first_party/skills/event-sourcing/agents/openai.yaml`
- Create: `sources/first_party/skills/event-sourcing/references/operational-guidance.md`
- Create: `sources/first_party/skills/event-sourcing/assets/authority/authority.yaml`
- Create: `sources/first_party/skills/event-sourcing/assets/authority/source-map.yaml`
- Create: `sources/first_party/skills/event-sourcing/assets/authority/CITATIONS.md`

**Interfaces:**
- Consumes: `harleydbartles/afpse-epic`; both skills share one execution branch.
- Produces: `cqrs` and `event-sourcing` in `architecture-pack`.

- [ ] **Step 1: Branch from the epic**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
git checkout -b harleydbartles/mark-341-split-cqrs-and-event-sourcing-into-clean-room-citation
```

- [ ] **Step 2: Scaffold both skills**

```bash
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name cqrs --custody marketplace --lane skills-with-citation
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name event-sourcing --custody marketplace --lane skills-with-citation
```

- [ ] **Step 3: Download primary authority snapshots to scratch**

For `cqrs`:

```bash
New-Item -ItemType Directory -Force -Path ../_agent-scratch/agent-asset-marketplace/afpse-epic
curl.exe -L -o ../_agent-scratch/agent-asset-marketplace/afpse-epic/cqrs.html https://martinfowler.com/bliki/CQRS.html
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('../_agent-scratch/agent-asset-marketplace/afpse-epic/cqrs.html').read_bytes()).hexdigest())"
Remove-Item ../_agent-scratch/agent-asset-marketplace/afpse-epic/cqrs.html
```

For `event-sourcing`:

```bash
curl.exe -L -o ../_agent-scratch/agent-asset-marketplace/afpse-epic/event-sourcing.html https://martinfowler.com/eaaDev/EventSourcing.html
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('../_agent-scratch/agent-asset-marketplace/afpse-epic/event-sourcing.html').read_bytes()).hexdigest())"
Remove-Item ../_agent-scratch/agent-asset-marketplace/afpse-epic/event-sourcing.html
```

Record the two SHA-256 hashes as `<sha256-cqrs>` and `<sha256-event-sourcing>`.

- [ ] **Step 4: Remove `.gitkeep` files and write reference files**

```bash
Remove-Item sources/first_party/skills/cqrs/references/.gitkeep
Remove-Item sources/first_party/skills/event-sourcing/references/.gitkeep
```

Create `sources/first_party/skills/cqrs/references/operational-guidance.md` with:
- Separate commands (writes) from queries (reads).
- Event sourcing as a persistence option, not a requirement.
- Consistency trade-offs and when CQRS is overkill.
- Typical project shapes and team boundaries.

Create `sources/first_party/skills/event-sourcing/references/operational-guidance.md` with:
- Event store as source of truth.
- Events, event streams, projections, snapshots.
- Versioning and schema evolution.
- Concurrency models and idempotency.

Invoke `superpowers-plus:writing-skills` and `mark-skill-authoring` to author the `SKILL.md` bodies under 500 words.

- [ ] **Step 5: Write `SKILL.md` and `agents/openai.yaml` for both skills**

`cqrs` values:
- `<skill>` = `cqrs`
- `<Skill Title>` = `CQRS`
- `<pack>` = `architecture-pack`
- `<lane>` = `skills-with-citation`
- `<canonical-url>` = `https://martinfowler.com/bliki/CQRS.html`
- `<pinned-source-url>` = `https://martinfowler.com/bliki/CQRS.html`
- `<revision>` = `current`
- `<license-name>` = `Multiple; see CITATIONS.md`
- `<license-url>` = `https://martinfowler.com/bliki/CQRS.html`
- `<content-mode>` = `first_party_synthesis`
- `<source-sections>` = `["Martin Fowler CQRS", "Greg Young CQRS/Event Sourcing", "Microsoft CQRS pattern"]`
- `description`: "Use when separating read and write models in a distributed or high-scale system, or when event sourcing is under consideration. Do not use when simple CRUD or single-model consistency is sufficient."

`event-sourcing` values:
- `<skill>` = `event-sourcing`
- `<Skill Title>` = `Event Sourcing`
- `<pack>` = `architecture-pack`
- `<lane>` = `skills-with-citation`
- `<canonical-url>` = `https://martinfowler.com/eaaDev/EventSourcing.html`
- `<pinned-source-url>` = `https://martinfowler.com/eaaDev/EventSourcing.html`
- `<revision>` = `current`
- `<license-name>` = `Multiple; see CITATIONS.md`
- `<license-url>` = `https://martinfowler.com/eaaDev/EventSourcing.html`
- `<content-mode>` = `first_party_synthesis`
- `<source-sections>` = `["Martin Fowler Event Sourcing", "Greg Young CQRS/Event Sourcing", "Microsoft Event Sourcing pattern"]`
- `description`: "Use when the system needs an audit log, temporal queries, or event-driven state reconstruction. Do not use when a simple relational model is enough or when strong immediate consistency is required."

- [ ] **Step 6: Write `assets/authority/authority.yaml`, `source-map.yaml`, and `CITATIONS.md` for both skills**

For `cqrs`, `CITATIONS.md`:

```markdown
# Authority record for cqrs

## Scholarly citation

- Martin Fowler. "CQRS." https://martinfowler.com/bliki/CQRS.html (accessed <YYYY-MM-DD>).
- Greg Young. "CQRS, Task Based UIs, Event Sourcing, aha!" https://codebetter.com/gregyoung/2010/02/16/cqrs-task-based-uis-event-sourcing-aha/ (accessed <YYYY-MM-DD>).
- Microsoft Azure Architecture Center. "CQRS pattern." https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs (accessed <YYYY-MM-DD>).

## Derivation boundary

- Derived: command/query separation, read/write model separation, event sourcing as optional companion, consistency trade-offs.
- Outside scope: implementation frameworks, specific vendor products.

## Attribution

- Clean-room first-party synthesis under MIT; attribution retained in CITATIONS.md only.

## Human review

- Reviewer: Harley Bartles
- Date: <YYYY-MM-DD>
- Decision: Approved. Operational SKILL.md text contains no inline citations.
```

For `event-sourcing`, `CITATIONS.md`:

```markdown
# Authority record for event-sourcing

## Scholarly citation

- Martin Fowler. "Event Sourcing." https://martinfowler.com/eaaDev/EventSourcing.html (accessed <YYYY-MM-DD>).
- Greg Young. "CQRS, Task Based UIs, Event Sourcing, aha!" https://codebetter.com/gregyoung/2010/02/16/cqrs-task-based-uis-event-sourcing-aha/ (accessed <YYYY-MM-DD>).
- Microsoft Azure Architecture Center. "Event Sourcing pattern." https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing (accessed <YYYY-MM-DD>).

## Derivation boundary

- Derived: event store, event streams, projections, snapshots, versioning, concurrency.
- Outside scope: specific event-store products, full CQRS implementation details (use cqrs skill).

## Attribution

- Clean-room first-party synthesis under MIT; attribution retained in CITATIONS.md only.

## Human review

- Reviewer: Harley Bartles
- Date: <YYYY-MM-DD>
- Decision: Approved. Operational SKILL.md text contains no inline citations.
```

- [ ] **Step 7: Validate both skills**

```bash
py -3 tools/validate_authority_assets.py
py -3 tools/normalize_first_party_skill_sources.py
```

Expected: no authority errors; normalization writes any required formatting changes.

- [ ] **Step 8: Commit and push the shared branch**

```bash
git add sources/first_party/skills/cqrs sources/first_party/skills/event-sourcing
git commit -m "feat(MARK-341): split cqrs and event-sourcing citation-backed skills"
git push -u origin harleydbartles/mark-341-split-cqrs-and-event-sourcing-into-clean-room-citation
```

- [ ] **Step 9: Record registry snippets**

`cqrs`:

```json
{
  "canonical_name": "cqrs",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/cqrs",
  "local_path": "skills/cqrs",
  "provenance_note": "Projected verbatim from the first-party cqrs skill.",
  "copy_expectation": "byte_identical"
}
```

`event-sourcing`:

```json
{
  "canonical_name": "event-sourcing",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/event-sourcing",
  "local_path": "skills/event-sourcing",
  "provenance_note": "Projected verbatim from the first-party event-sourcing skill.",
  "copy_expectation": "byte_identical"
}
```

### Task 4: MARK-342 — Create `clean-architecture` and `hexagonal-architecture` citation-backed skills

**Files:**
- Create: `sources/first_party/skills/clean-architecture/SKILL.md`
- Create: `sources/first_party/skills/clean-architecture/agents/openai.yaml`
- Create: `sources/first_party/skills/clean-architecture/references/operational-guidance.md`
- Create: `sources/first_party/skills/clean-architecture/assets/authority/authority.yaml`
- Create: `sources/first_party/skills/clean-architecture/assets/authority/source-map.yaml`
- Create: `sources/first_party/skills/clean-architecture/assets/authority/CITATIONS.md`
- Create: `sources/first_party/skills/hexagonal-architecture/SKILL.md`
- Create: `sources/first_party/skills/hexagonal-architecture/agents/openai.yaml`
- Create: `sources/first_party/skills/hexagonal-architecture/references/operational-guidance.md`
- Create: `sources/first_party/skills/hexagonal-architecture/assets/authority/authority.yaml`
- Create: `sources/first_party/skills/hexagonal-architecture/assets/authority/source-map.yaml`
- Create: `sources/first_party/skills/hexagonal-architecture/assets/authority/CITATIONS.md`

**Interfaces:**
- Consumes: `harleydbartles/afpse-epic`; both skills share one execution branch.
- Produces: `clean-architecture` and `hexagonal-architecture` in `architecture-pack`.

- [ ] **Step 1: Branch from the epic**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
git checkout -b harleydbartles/mark-342-create-clean-architecture-and-hexagonal-architecture-citation-backed
```

- [ ] **Step 2: Scaffold both skills**

```bash
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name clean-architecture --custody marketplace --lane skills-with-citation
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name hexagonal-architecture --custody marketplace --lane skills-with-citation
```

- [ ] **Step 3: Download primary authority snapshots to scratch**

For `clean-architecture`:

```bash
New-Item -ItemType Directory -Force -Path ../_agent-scratch/agent-asset-marketplace/afpse-epic
curl.exe -L -o ../_agent-scratch/agent-asset-marketplace/afpse-epic/clean-architecture.html https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('../_agent-scratch/agent-asset-marketplace/afpse-epic/clean-architecture.html').read_bytes()).hexdigest())"
Remove-Item ../_agent-scratch/agent-asset-marketplace/afpse-epic/clean-architecture.html
```

For `hexagonal-architecture`:

```bash
curl.exe -L -o ../_agent-scratch/agent-asset-marketplace/afpse-epic/hexagonal-architecture.html https://alistair.cockburn.us/hexagonal-architecture/
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('../_agent-scratch/agent-asset-marketplace/afpse-epic/hexagonal-architecture.html').read_bytes()).hexdigest())"
Remove-Item ../_agent-scratch/agent-asset-marketplace/afpse-epic/hexagonal-architecture.html
```

Record the SHA-256 hashes as `<sha256-clean>` and `<sha256-hexagonal>`.

- [ ] **Step 4: Remove `.gitkeep` files and write reference files**

```bash
Remove-Item sources/first_party/skills/clean-architecture/references/.gitkeep
Remove-Item sources/first_party/skills/hexagonal-architecture/references/.gitkeep
```

Create `sources/first_party/skills/clean-architecture/references/operational-guidance.md` with:
- Dependency direction: domain innermost, frameworks outermost.
- Layers: entities, use cases, interface adapters, frameworks.
- Testability and boundary enforcement.

Create `sources/first_party/skills/hexagonal-architecture/references/operational-guidance.md` with:
- Ports and adapters; domain at center.
- Primary and secondary adapters.
- Isolation from frameworks, databases, UI.
- Similarities and differences with clean/onion architecture.

Invoke `superpowers-plus:writing-skills` and `mark-skill-authoring` to author the `SKILL.md` bodies under 500 words.

- [ ] **Step 5: Write `SKILL.md` and `agents/openai.yaml` for both skills**

`clean-architecture` values:
- `<skill>` = `clean-architecture`
- `<Skill Title>` = `Clean Architecture`
- `<pack>` = `architecture-pack`
- `<lane>` = `skills-with-citation`
- `<canonical-url>` = `https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html`
- `<pinned-source-url>` = `https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html`
- `<revision>` = `current`
- `<license-name>` = `Multiple; see CITATIONS.md`
- `<license-url>` = `https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html`
- `<content-mode>` = `first_party_synthesis`
- `<source-sections>` = `["Robert C. Martin Clean Architecture", "Alistair Cockburn Hexagonal Architecture", "Jeffrey Palermo Onion Architecture"]`
- `description`: "Use when designing testable, framework-independent applications with clear dependency rules. Do not use when the team is committed to a framework-centric stack and the cost of ports/adapters is unjustified."

`hexagonal-architecture` values:
- `<skill>` = `hexagonal-architecture`
- `<Skill Title>` = `Hexagonal Architecture`
- `<pack>` = `architecture-pack`
- `<lane>` = `skills-with-citation`
- `<canonical-url>` = `https://alistair.cockburn.us/hexagonal-architecture/`
- `<pinned-source-url>` = `https://alistair.cockburn.us/hexagonal-architecture/`
- `<revision>` = `current`
- `<license-name>` = `Multiple; see CITATIONS.md`
- `<license-url>` = `https://alistair.cockburn.us/hexagonal-architecture/`
- `<content-mode>` = `first_party_synthesis`
- `<source-sections>` = `["Alistair Cockburn Hexagonal Architecture", "Robert C. Martin Clean Architecture", "Jeffrey Palermo Onion Architecture"]`
- `description`: "Use when isolating domain logic from frameworks, UI, and databases through ports and adapters. Do not use when the domain is trivial or the project is a thin framework wrapper."

- [ ] **Step 6: Write `assets/authority/authority.yaml`, `source-map.yaml`, and `CITATIONS.md` for both skills**

For `clean-architecture`, `CITATIONS.md`:

```markdown
# Authority record for clean-architecture

## Scholarly citation

- Robert C. Martin. "The Clean Architecture." https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html (accessed <YYYY-MM-DD>).
- Alistair Cockburn. "Hexagonal Architecture." https://alistair.cockburn.us/hexagonal-architecture/ (accessed <YYYY-MM-DD>).
- Jeffrey Palermo. "The Onion Architecture: Part 1." https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/ (accessed <YYYY-MM-DD>).

## Derivation boundary

- Derived: dependency rule, layers, boundaries, entities/use cases/interface adapters, testability.
- Outside scope: specific frameworks, UI patterns.

## Attribution

- Clean-room first-party synthesis under MIT; attribution retained in CITATIONS.md only.

## Human review

- Reviewer: Harley Bartles
- Date: <YYYY-MM-DD>
- Decision: Approved. Operational SKILL.md text contains no inline citations.
```

For `hexagonal-architecture`, `CITATIONS.md`:

```markdown
# Authority record for hexagonal-architecture

## Scholarly citation

- Alistair Cockburn. "Hexagonal Architecture." https://alistair.cockburn.us/hexagonal-architecture/ (accessed <YYYY-MM-DD>).
- Robert C. Martin. "The Clean Architecture." https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html (accessed <YYYY-MM-DD>).
- Jeffrey Palermo. "The Onion Architecture: Part 1." https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/ (accessed <YYYY-MM-DD>).

## Derivation boundary

- Derived: ports/adapters, domain at center, primary and secondary adapters, isolation from frameworks/databases/UI.
- Outside scope: implementation frameworks.

## Attribution

- Clean-room first-party synthesis under MIT; attribution retained in CITATIONS.md only.

## Human review

- Reviewer: Harley Bartles
- Date: <YYYY-MM-DD>
- Decision: Approved. Operational SKILL.md text contains no inline citations.
```

- [ ] **Step 7: Validate and commit**

```bash
py -3 tools/validate_authority_assets.py
py -3 tools/normalize_first_party_skill_sources.py
git add sources/first_party/skills/clean-architecture sources/first_party/skills/hexagonal-architecture
git commit -m "feat(MARK-342): clean-architecture and hexagonal-architecture citation-backed skills"
git push -u origin harleydbartles/mark-342-create-clean-architecture-and-hexagonal-architecture-citation-backed
```

- [ ] **Step 8: Record registry snippets**

`clean-architecture`:

```json
{
  "canonical_name": "clean-architecture",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/clean-architecture",
  "local_path": "skills/clean-architecture",
  "provenance_note": "Projected verbatim from the first-party clean-architecture skill.",
  "copy_expectation": "byte_identical"
}
```

`hexagonal-architecture`:

```json
{
  "canonical_name": "hexagonal-architecture",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/hexagonal-architecture",
  "local_path": "skills/hexagonal-architecture",
  "provenance_note": "Projected verbatim from the first-party hexagonal-architecture skill.",
  "copy_expectation": "byte_identical"
}
```

### Task 5: MARK-343 — Re-custody OWASP Top Ten and establish an ASVS verification route

**Files:**
- Create: `sources/first_party/skills/owasp-top-ten/SKILL.md`
- Create: `sources/first_party/skills/owasp-top-ten/agents/openai.yaml`
- Create: `sources/first_party/skills/owasp-top-ten/references/operational-guidance.md`
- Create: `sources/first_party/skills/owasp-top-ten/assets/authority/authority.yaml`
- Create: `sources/first_party/skills/owasp-top-ten/assets/authority/source-map.yaml`
- Create: `sources/first_party/skills/owasp-top-ten/assets/authority/CITATIONS.md`
- Create: `sources/first_party/skills/owasp-top-ten/assets/authority/reference-source/owasp-top-ten.html`

**Interfaces:**
- Consumes: `harleydbartles/afpse-epic`; canonical authorities `https://owasp.org/Top10/` and OWASP ASVS.
- Produces: `owasp-top-ten` in `security-pack`.

Skill values:
- `<skill>` = `owasp-top-ten`
- `<Skill Title>` = `OWASP Top Ten`
- `<pack>` = `security-pack`
- `<lane>` = `skills-with-source`
- `<canonical-url>` = `https://owasp.org/Top10/`
- `<pinned-source-url>` = `https://owasp.org/Top10/`
- `<revision>` = `current`
- `<license-name>` = `CC-BY-SA-4.0`
- `<license-url>` = `https://creativecommons.org/licenses/by-sa/4.0/`
- `<content-mode>` = `licensed_adaptation`
- `<source-sections>` = `["Top 10 risks", "ASVS verification route", "Prevention cheat sheets"]`

Content brief for `references/operational-guidance.md`:
- Top 10 risks with concise descriptions and prevention controls.
- ASVS verification route: level 1/2/3 and how to map to the Top 10.
- Common misconfigurations and secure defaults.

`SKILL.md` description: "Use when reviewing web application security risks, mapping controls to OWASP Top 10, or establishing an ASVS verification route. Do not use when the task is pen-testing execution or vendor tool selection."

- [ ] **Step 1: Branch from the epic**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
git checkout -b harleydbartles/mark-343-re-custody-owasp-top-ten-and-establish-an-asvs-verification
```

- [ ] **Step 2: Scaffold the skill**

```bash
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name owasp-top-ten --custody marketplace --lane skills-with-source
```

- [ ] **Step 3: Download the canonical source**

```bash
curl.exe -L -o sources/first_party/skills/owasp-top-ten/assets/authority/reference-source/owasp-top-ten.html https://owasp.org/Top10/
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/owasp-top-ten/assets/authority/reference-source/owasp-top-ten.html').read_bytes()).hexdigest())"
```

Record the SHA-256 as `<sha256>`.

- [ ] **Step 4: Clean up scaffold placeholders and write the reference file**

```bash
Remove-Item sources/first_party/skills/owasp-top-ten/assets/authority/reference-source/.gitkeep
Remove-Item sources/first_party/skills/owasp-top-ten/references/.gitkeep
```

Create `sources/first_party/skills/owasp-top-ten/references/operational-guidance.md` using the content brief.

- [ ] **Step 5: Write `SKILL.md` and `agents/openai.yaml`**

Use the Common Templates with the values above.

- [ ] **Step 6: Write `assets/authority/authority.yaml`, `source-map.yaml`, and `CITATIONS.md`**

`CITATIONS.md`:

```markdown
# Authority record for owasp-top-ten

## Scholarly citation

- OWASP Foundation. "OWASP Top 10." https://owasp.org/Top10/ (accessed <YYYY-MM-DD>).
- OWASP Foundation. "Application Security Verification Standard (ASVS)." https://owasp.org/www-project-application-security-verification-standard/ (accessed <YYYY-MM-DD>).

## Derivation boundary

- Derived: the ten risk categories, CWE mappings, prevention cheat sheets, verification controls.
- Outside scope: OWASP tools, commercial services, brand marks.

## Attribution

- OWASP Top 10 and ASVS content used under CC-BY-SA-4.0 (verify upstream license before final commit).

## Human review

- Reviewer: Harley Bartles
- Date: <YYYY-MM-DD>
- Decision: Approved. Operational SKILL.md text contains no inline citations.
```

- [ ] **Step 7: Validate, normalize, commit, push**

```bash
py -3 tools/validate_authority_assets.py
py -3 tools/normalize_first_party_skill_sources.py
git add sources/first_party/skills/owasp-top-ten
git commit -m "feat(MARK-343): re-custody owasp-top-ten and ASVS route"
git push -u origin harleydbartles/mark-343-re-custody-owasp-top-ten-and-establish-an-asvs-verification
```

- [ ] **Step 8: Record the registry snippet**

```json
{
  "canonical_name": "owasp-top-ten",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/owasp-top-ten",
  "local_path": "skills/owasp-top-ten",
  "provenance_note": "Projected verbatim from the first-party owasp-top-ten skill.",
  "copy_expectation": "byte_identical"
}
```

### Task 6: MARK-344 — Re-custody `openapi-specification`

**Files:**
- Create: `sources/first_party/skills/openapi-specification/SKILL.md`
- Create: `sources/first_party/skills/openapi-specification/agents/openai.yaml`
- Create: `sources/first_party/skills/openapi-specification/references/operational-guidance.md`
- Create: `sources/first_party/skills/openapi-specification/assets/authority/authority.yaml`
- Create: `sources/first_party/skills/openapi-specification/assets/authority/source-map.yaml`
- Create: `sources/first_party/skills/openapi-specification/assets/authority/CITATIONS.md`
- Create: `sources/first_party/skills/openapi-specification/assets/authority/reference-source/openapi-specification.html`

**Interfaces:**
- Consumes: `harleydbartles/afpse-epic`; canonical authority `https://spec.openapis.org/oas/`.
- Produces: `openapi-specification` in `api-contracts-pack`.

Skill values:
- `<skill>` = `openapi-specification`
- `<Skill Title>` = `OpenAPI Specification`
- `<pack>` = `api-contracts-pack`
- `<lane>` = `skills-with-source`
- `<canonical-url>` = `https://spec.openapis.org/oas/`
- `<pinned-source-url>` = `https://spec.openapis.org/oas/`
- `<revision>` = `current`
- `<license-name>` = `Apache-2.0`
- `<license-url>` = `https://www.apache.org/licenses/LICENSE-2.0`
- `<content-mode>` = `licensed_adaptation`
- `<source-sections>` = `["OpenAPI Object", "Paths", "Components"]`

Content brief for `references/operational-guidance.md`:
- OpenAPI document structure (info, servers, paths, components, security).
- Versioning and compatibility.
- Schema patterns and reusable components.

`SKILL.md` description: "Use when designing, reviewing, or versioning an OpenAPI contract. Do not use when the work is implementation framework-specific or code-generation only."

- [ ] **Step 1: Branch from the epic**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
git checkout -b harleydbartles/mark-344-re-custody-the-openapi-specification-specialist-skill
```

- [ ] **Step 2: Scaffold the skill**

```bash
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name openapi-specification --custody marketplace --lane skills-with-source
```

- [ ] **Step 3: Download the canonical source**

```bash
curl.exe -L -o sources/first_party/skills/openapi-specification/assets/authority/reference-source/openapi-specification.html https://spec.openapis.org/oas/
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/openapi-specification/assets/authority/reference-source/openapi-specification.html').read_bytes()).hexdigest())"
```

Record the SHA-256 as `<sha256>`.

- [ ] **Step 4: Clean up, write reference file, write templates**

```bash
Remove-Item sources/first_party/skills/openapi-specification/assets/authority/reference-source/.gitkeep
Remove-Item sources/first_party/skills/openapi-specification/references/.gitkeep
```

Create `sources/first_party/skills/openapi-specification/references/operational-guidance.md` using the content brief. Write `SKILL.md` and `agents/openai.yaml` using the Common Templates.

- [ ] **Step 5: Write `assets/authority/authority.yaml`, `source-map.yaml`, and `CITATIONS.md`**

`CITATIONS.md`:

```markdown
# Authority record for openapi-specification

## Scholarly citation

- OpenAPI Initiative. "OpenAPI Specification." https://spec.openapis.org/oas/ (accessed <YYYY-MM-DD>).

## Derivation boundary

- Derived: OpenAPI object structure, paths, operations, parameters, schemas, security schemes, version semantics.
- Outside scope: implementation frameworks, code generation, non-spec extensions.

## Attribution

- OpenAPI Specification licensed under Apache-2.0.

## Human review

- Reviewer: Harley Bartles
- Date: <YYYY-MM-DD>
- Decision: Approved. Operational SKILL.md text contains no inline citations.
```

- [ ] **Step 6: Validate, normalize, commit, push**

```bash
py -3 tools/validate_authority_assets.py
py -3 tools/normalize_first_party_skill_sources.py
git add sources/first_party/skills/openapi-specification
git commit -m "feat(MARK-344): re-custody openapi-specification"
git push -u origin harleydbartles/mark-344-re-custody-the-openapi-specification-specialist-skill
```

- [ ] **Step 7: Record the registry snippet**

```json
{
  "canonical_name": "openapi-specification",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/openapi-specification",
  "local_path": "skills/openapi-specification",
  "provenance_note": "Projected verbatim from the first-party openapi-specification skill.",
  "copy_expectation": "byte_identical"
}
```

### Task 7: MARK-345 — Re-custody `wcag` accessibility-audit specialist skill

**Files:**
- Create: `sources/first_party/skills/wcag/SKILL.md`
- Create: `sources/first_party/skills/wcag/agents/openai.yaml`
- Create: `sources/first_party/skills/wcag/references/operational-guidance.md`
- Create: `sources/first_party/skills/wcag/assets/authority/authority.yaml`
- Create: `sources/first_party/skills/wcag/assets/authority/source-map.yaml`
- Create: `sources/first_party/skills/wcag/assets/authority/CITATIONS.md`
- Create: `sources/first_party/skills/wcag/assets/authority/reference-source/wcag.html`

**Interfaces:**
- Consumes: `harleydbartles/afpse-epic`; canonical authority `https://www.w3.org/TR/WCAG22/` and W3C document license.
- Produces: `wcag` in `frontend-pack`.

Skill values:
- `<skill>` = `wcag`
- `<Skill Title>` = `WCAG`
- `<pack>` = `frontend-pack`
- `<lane>` = `skills-with-source`
- `<canonical-url>` = `https://www.w3.org/TR/WCAG22/`
- `<pinned-source-url>` = `https://www.w3.org/TR/WCAG22/`
- `<revision>` = `current`
- `<license-name>` = `W3C Document License`
- `<license-url>` = `https://www.w3.org/Consortium/Legal/2015/doc-license`
- `<content-mode>` = `licensed_adaptation`
- `<source-sections>` = `["Perceivable", "Operable", "Understandable", "Robust"]`

Content brief for `references/operational-guidance.md`:
- POUR principles: Perceivable, Operable, Understandable, Robust.
- Conformance levels A/AA/AAA.
- Common success criteria and testing approach.
- Accessibility audit workflow.

`SKILL.md` description: "Use when auditing web content accessibility against WCAG 2.2 or mapping success criteria to a verification plan. Do not use when the work is general UX design or automated tooling setup only."

- [ ] **Step 1: Branch from the epic**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
git checkout -b harleydbartles/mark-345-re-custody-the-wcag-accessibility-audit-specialist-skill
```

- [ ] **Step 2: Scaffold the skill**

```bash
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name wcag --custody marketplace --lane skills-with-source
```

- [ ] **Step 3: Download the canonical source**

```bash
curl.exe -L -o sources/first_party/skills/wcag/assets/authority/reference-source/wcag.html https://www.w3.org/TR/WCAG22/
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/wcag/assets/authority/reference-source/wcag.html').read_bytes()).hexdigest())"
```

Record the SHA-256 as `<sha256>`.

- [ ] **Step 4: Clean up, write reference, write templates**

```bash
Remove-Item sources/first_party/skills/wcag/assets/authority/reference-source/.gitkeep
Remove-Item sources/first_party/skills/wcag/references/.gitkeep
```

Create `sources/first_party/skills/wcag/references/operational-guidance.md` using the content brief. Write `SKILL.md` and `agents/openai.yaml` using the Common Templates.

- [ ] **Step 5: Write `assets/authority/authority.yaml`, `source-map.yaml`, and `CITATIONS.md`**

`CITATIONS.md`:

```markdown
# Authority record for wcag

## Scholarly citation

- W3C. "Web Content Accessibility Guidelines (WCAG) 2.2." https://www.w3.org/TR/WCAG22/ (accessed <YYYY-MM-DD>).
- W3C document license: https://www.w3.org/Consortium/Legal/2015/doc-license

## Derivation boundary

- Derived: POUR principles, success criteria, conformance levels, sufficient/advisory techniques.
- Outside scope: W3C logos, process documents, non-WCAG WAI materials.

## Attribution

- W3C WCAG documents used under the W3C Document License.

## Human review

- Reviewer: Harley Bartles
- Date: <YYYY-MM-DD>
- Decision: Approved. Operational SKILL.md text contains no inline citations.
```

- [ ] **Step 6: Validate, normalize, commit, push**

```bash
py -3 tools/validate_authority_assets.py
py -3 tools/normalize_first_party_skill_sources.py
git add sources/first_party/skills/wcag
git commit -m "feat(MARK-345): re-custody wcag accessibility-audit skill"
git push -u origin harleydbartles/mark-345-re-custody-the-wcag-accessibility-audit-specialist-skill
```

- [ ] **Step 7: Record the registry snippet**

```json
{
  "canonical_name": "wcag",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/wcag",
  "local_path": "skills/wcag",
  "provenance_note": "Projected verbatim from the first-party wcag skill.",
  "copy_expectation": "byte_identical"
}
```

### Task 8: MARK-347 — Create `typescript` ecosystem skill

**Files:**
- Create: `sources/first_party/skills/typescript/SKILL.md`
- Create: `sources/first_party/skills/typescript/agents/openai.yaml`
- Create: `sources/first_party/skills/typescript/references/operational-guidance.md`
- Create: `sources/first_party/skills/typescript/assets/authority/authority.yaml`
- Create: `sources/first_party/skills/typescript/assets/authority/source-map.yaml`
- Create: `sources/first_party/skills/typescript/assets/authority/CITATIONS.md`
- Create: `sources/first_party/skills/typescript/assets/authority/reference-source/typescript.tar.gz`

**Interfaces:**
- Consumes: `harleydbartles/afpse-epic`; canonical authority `https://github.com/microsoft/TypeScript-Website` (default branch `v2`, CC-BY-4.0).
- Produces: `typescript` in `language-patterns-pack`.

Skill values:
- `<skill>` = `typescript`
- `<Skill Title>` = `TypeScript`
- `<pack>` = `language-patterns-pack`
- `<lane>` = `skills-with-source`
- `<canonical-url>` = `https://github.com/microsoft/TypeScript-Website`
- `<pinned-source-url>` = `https://github.com/microsoft/TypeScript-Website/archive/refs/heads/v2.tar.gz`
- `<revision>` = `v2`
- `<license-name>` = `CC-BY-4.0`
- `<license-url>` = `https://github.com/microsoft/TypeScript-Website/blob/v2/LICENSE`
- `<content-mode>` = `licensed_adaptation`
- `<source-sections>` = `["Type system", "Interfaces and types", "Generics", "Module resolution"]`

Content brief for `references/operational-guidance.md`:
- Type system: primitives, arrays, tuples, unions, intersections, literal types.
- Interfaces, type aliases, generics, mapped types, conditional types.
- Type inference, narrowing, type guards.
- Declaration files, module resolution, TSConfig options.
- When to use strict settings and how to avoid `any`.

`SKILL.md` description: "Use when writing or reviewing TypeScript type design, generics, module resolution, or compiler configuration. Do not use when the work is JavaScript runtime debugging or framework-specific UI composition."

- [ ] **Step 1: Branch from the epic**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
git checkout -b harleydbartles/mark-347-create-the-first-party-typescript-ecosystem-skill
```

- [ ] **Step 2: Scaffold the skill**

```bash
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name typescript --custody marketplace --lane skills-with-source
```

- [ ] **Step 3: Download the canonical source**

```bash
curl.exe -L -o sources/first_party/skills/typescript/assets/authority/reference-source/typescript.tar.gz https://github.com/microsoft/TypeScript-Website/archive/refs/heads/v2.tar.gz
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/typescript/assets/authority/reference-source/typescript.tar.gz').read_bytes()).hexdigest())"
```

Record the SHA-256 as `<sha256>`.

- [ ] **Step 4: Clean up, write reference, write templates**

```bash
Remove-Item sources/first_party/skills/typescript/assets/authority/reference-source/.gitkeep
Remove-Item sources/first_party/skills/typescript/references/.gitkeep
```

Create `sources/first_party/skills/typescript/references/operational-guidance.md` using the content brief. Write `SKILL.md` and `agents/openai.yaml` using the Common Templates.

- [ ] **Step 5: Write `assets/authority/authority.yaml`, `source-map.yaml`, and `CITATIONS.md`**

`CITATIONS.md`:

```markdown
# Authority record for typescript

## Scholarly citation

- Microsoft. "TypeScript Documentation." https://github.com/microsoft/TypeScript-Website (accessed <YYYY-MM-DD>).
- TypeScript-Website repository content licensed under CC-BY-4.0.

## Derivation boundary

- Derived: type system, interfaces, generics, type inference, declaration files, module resolution, TSConfig options.
- Outside scope: TypeScript compiler internals, non-docs examples.

## Attribution

- TypeScript documentation used under CC-BY-4.0.

## Human review

- Reviewer: Harley Bartles
- Date: <YYYY-MM-DD>
- Decision: Approved. Operational SKILL.md text contains no inline citations.
```

- [ ] **Step 6: Validate, normalize, commit, push**

```bash
py -3 tools/validate_authority_assets.py
py -3 tools/normalize_first_party_skill_sources.py
git add sources/first_party/skills/typescript
git commit -m "feat(MARK-347): create typescript ecosystem skill"
git push -u origin harleydbartles/mark-347-create-the-first-party-typescript-ecosystem-skill
```

- [ ] **Step 7: Record the registry snippet**

```json
{
  "canonical_name": "typescript",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/typescript",
  "local_path": "skills/typescript",
  "provenance_note": "Projected verbatim from the first-party typescript skill.",
  "copy_expectation": "byte_identical"
}
```

### Task 9: MARK-349 — Create `web-styling` skill

**Files:**
- Create: `sources/first_party/skills/web-styling/SKILL.md`
- Create: `sources/first_party/skills/web-styling/agents/openai.yaml`
- Create: `sources/first_party/skills/web-styling/references/operational-guidance.md`
- Create: `sources/first_party/skills/web-styling/assets/authority/authority.yaml`
- Create: `sources/first_party/skills/web-styling/assets/authority/source-map.yaml`
- Create: `sources/first_party/skills/web-styling/assets/authority/CITATIONS.md`
- Create (conditional): `sources/first_party/skills/web-styling/assets/authority/reference-source/*.tar.gz` or `*.html`

**Interfaces:**
- Consumes: `harleydbartles/afpse-epic`; canonical authorities CSS Modules, Sass/Less, and styled-components upstream docs/sources.
- Produces: `web-styling` in `frontend-pack`.

This skill is `skills-with-source` only if **all** upstream licenses permit vendoring. Before vendoring, verify each repository's `LICENSE` file. If any upstream is non-redistributable, switch lane to `skills-with-citation` and omit the `reference-source/` snapshots.

Candidate sources (verify license and branch before running):

```bash
curl.exe -L -o sources/first_party/skills/web-styling/assets/authority/reference-source/css-modules.tar.gz https://github.com/css-modules/css-modules/archive/refs/heads/master.tar.gz
curl.exe -L -o sources/first_party/skills/web-styling/assets/authority/reference-source/sass-site.tar.gz https://github.com/sass/sass-site/archive/refs/heads/main.tar.gz
curl.exe -L -o sources/first_party/skills/web-styling/assets/authority/reference-source/less-docs.tar.gz https://github.com/less/less-docs/archive/refs/heads/master.tar.gz
curl.exe -L -o sources/first_party/skills/web-styling/assets/authority/reference-source/styled-components-website.tar.gz https://github.com/styled-components/styled-components-website/archive/refs/heads/main.tar.gz
```

For each downloaded archive, compute SHA-256:

```bash
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/web-styling/assets/authority/reference-source/css-modules.tar.gz').read_bytes()).hexdigest())"
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/web-styling/assets/authority/reference-source/sass-site.tar.gz').read_bytes()).hexdigest())"
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/web-styling/assets/authority/reference-source/less-docs.tar.gz').read_bytes()).hexdigest())"
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/web-styling/assets/authority/reference-source/styled-components-website.tar.gz').read_bytes()).hexdigest())"
```

If the license check fails for any candidate, switch to `skills-with-citation` and use the citation-backed download pattern (scratch `.html`) for the primary authority instead.

Skill values (source lane):
- `<skill>` = `web-styling`
- `<Skill Title>` = `Web Styling`
- `<pack>` = `frontend-pack`
- `<lane>` = `skills-with-source` (or `skills-with-citation` after license check)
- `<canonical-url>` = `https://github.com/css-modules/css-modules`
- `<pinned-source-url>` = `https://github.com/css-modules/css-modules/archive/refs/heads/master.tar.gz`
- `<revision>` = `master`
- `<license-name>` = `Multiple; see CITATIONS.md` (or specific license)
- `<license-url>` = `<repository-LICENSE-URL>`
- `<content-mode>` = `licensed_adaptation` (or `first_party_synthesis` for citation lane)
- `<source-sections>` = `["CSS Modules", "Sass", "Less", "styled-components"]`

Content brief for `references/operational-guidance.md`:
- CSS Modules: local scope, composition, class naming.
- Sass: variables, nesting, mixins, partials, import rules.
- Less: variables, mixins, guards, import.
- styled-components: tagged templates, theming, props-based styles.
- When to use CSS-in-JS vs preprocessed CSS.

`SKILL.md` description: "Use when choosing or refactoring CSS approaches across CSS Modules, Sass, Less, and styled-components. Do not use when the work is design system governance or framework-specific component libraries."

- [ ] **Step 1: Branch from the epic**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
git checkout -b harleydbartles/mark-349-create-the-cross-framework-web-styling-skill
```

- [ ] **Step 2: Scaffold with the chosen lane**

```bash
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name web-styling --custody marketplace --lane skills-with-source
```

If the lane switches to citation, use `--lane skills-with-citation` and update the generated `authority.yaml` and `source-map.yaml` `content_mode` to `first_party_synthesis`.

- [ ] **Step 3: Acquire authority and write references**

Run the candidate downloads and license checks above. Create `sources/first_party/skills/web-styling/references/operational-guidance.md` using the content brief. Remove `.gitkeep` files:

```bash
Remove-Item sources/first_party/skills/web-styling/references/.gitkeep
# Only if using skills-with-source (created by new_skill.py for that lane):
Remove-Item sources/first_party/skills/web-styling/assets/authority/reference-source/.gitkeep -ErrorAction SilentlyContinue
```

- [ ] **Step 4: Write `SKILL.md` and `agents/openai.yaml`**

Use the Common Templates with the values above.

- [ ] **Step 5: Write `assets/authority/authority.yaml`, `source-map.yaml`, and `CITATIONS.md`**

`CITATIONS.md` (source lane):

```markdown
# Authority record for web-styling

## Scholarly citation

- CSS Modules documentation. https://github.com/css-modules/css-modules (accessed <YYYY-MM-DD>).
- Sass documentation. https://github.com/sass/sass-site (accessed <YYYY-MM-DD>).
- Less documentation. https://github.com/less/less-docs (accessed <YYYY-MM-DD>).
- styled-components documentation. https://github.com/styled-components/styled-components-website (accessed <YYYY-MM-DD>).

## Derivation boundary

- Derived: CSS Modules local scope/composition, Sass/Less features, styled-components patterns, cross-framework trade-offs.
- Outside scope: design tokens owned by a design-system skill, framework-specific component libraries.

## Attribution

- Each upstream source used under its respective license; recorded per snapshot.

## Human review

- Reviewer: Harley Bartles
- Date: <YYYY-MM-DD>
- Decision: Approved. Operational SKILL.md text contains no inline citations.
```

If citation lane, replace vendored source claims with the clean-room source citations and set `content_mode: first_party_synthesis`.

- [ ] **Step 6: Validate, normalize, commit, push**

```bash
py -3 tools/validate_authority_assets.py
py -3 tools/normalize_first_party_skill_sources.py
git add sources/first_party/skills/web-styling
git commit -m "feat(MARK-349): create cross-framework web-styling skill"
git push -u origin harleydbartles/mark-349-create-the-cross-framework-web-styling-skill
```

- [ ] **Step 7: Record the registry snippet**

```json
{
  "canonical_name": "web-styling",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/web-styling",
  "local_path": "skills/web-styling",
  "provenance_note": "Projected verbatim from the first-party web-styling skill.",
  "copy_expectation": "byte_identical"
}
```

### Task 10: MARK-348 — Create `react` ecosystem skill

**Files:**
- Create: `sources/first_party/skills/react/SKILL.md`
- Create: `sources/first_party/skills/react/agents/openai.yaml`
- Create: `sources/first_party/skills/react/references/operational-guidance.md`
- Create: `sources/first_party/skills/react/assets/authority/authority.yaml`
- Create: `sources/first_party/skills/react/assets/authority/source-map.yaml`
- Create: `sources/first_party/skills/react/assets/authority/CITATIONS.md`
- Create: `sources/first_party/skills/react/assets/authority/reference-source/react.tar.gz`

**Interfaces:**
- Consumes: `harleydbartles/afpse-epic`; `typescript` and `web-styling` branches landed; canonical authority `https://github.com/reactjs/react.dev` (CC-BY-4.0, default branch `main`).
- Produces: `react` in `frontend-pack`.

Do not start this task until `typescript` (Task 8) and `web-styling` (Task 9) are merged into `harleydbartles/afpse-epic`.

Skill values:
- `<skill>` = `react`
- `<Skill Title>` = `React`
- `<pack>` = `frontend-pack`
- `<lane>` = `skills-with-source`
- `<canonical-url>` = `https://github.com/reactjs/react.dev`
- `<pinned-source-url>` = `https://github.com/reactjs/react.dev/archive/refs/heads/main.tar.gz`
- `<revision>` = `main`
- `<license-name>` = `CC-BY-4.0`
- `<license-url>` = `https://github.com/reactjs/react.dev/blob/main/LICENSE`
- `<content-mode>` = `licensed_adaptation`
- `<source-sections>` = `["Thinking in React", "State and lifecycle", "Hooks", "Performance"]`

Content brief for `references/operational-guidance.md`:
- Functional components and JSX.
- Hooks rules, useState, useEffect, useContext, custom hooks.
- State lifting, composition, conditional rendering.
- Performance: memo, useMemo, useCallback, React.memo.
- When to use Next.js or server components (defer to framework-specific skill).

`SKILL.md` description: "Use when building or reviewing React component architecture, hooks usage, and performance patterns. Do not use when the work is framework-agnostic styling, routing, or state management owned by another skill."

- [ ] **Step 1: Branch from the epic after dependencies merge**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
git checkout -b harleydbartles/mark-348-create-the-first-party-react-ecosystem-skill
```

- [ ] **Step 2: Scaffold the skill**

```bash
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name react --custody marketplace --lane skills-with-source
```

- [ ] **Step 3: Download the canonical source**

```bash
curl.exe -L -o sources/first_party/skills/react/assets/authority/reference-source/react.tar.gz https://github.com/reactjs/react.dev/archive/refs/heads/main.tar.gz
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/react/assets/authority/reference-source/react.tar.gz').read_bytes()).hexdigest())"
```

Record the SHA-256 as `<sha256>`.

- [ ] **Step 4: Clean up, write reference, write templates**

```bash
Remove-Item sources/first_party/skills/react/assets/authority/reference-source/.gitkeep
Remove-Item sources/first_party/skills/react/references/.gitkeep
```

Create `sources/first_party/skills/react/references/operational-guidance.md` using the content brief. Write `SKILL.md` and `agents/openai.yaml` using the Common Templates.

- [ ] **Step 5: Write `assets/authority/authority.yaml`, `source-map.yaml`, and `CITATIONS.md`**

`CITATIONS.md`:

```markdown
# Authority record for react

## Scholarly citation

- React. "React Documentation." https://github.com/reactjs/react.dev (accessed <YYYY-MM-DD>).
- react.dev content licensed under CC-BY-4.0.

## Derivation boundary

- Derived: components, hooks, state, effects, JSX, patterns, performance guidance.
- Outside scope: React source code internals, Next.js specifics, experimental APIs.

## Attribution

- React documentation used under CC-BY-4.0.

## Human review

- Reviewer: Harley Bartles
- Date: <YYYY-MM-DD>
- Decision: Approved. Operational SKILL.md text contains no inline citations.
```

- [ ] **Step 6: Validate, normalize, commit, push**

```bash
py -3 tools/validate_authority_assets.py
py -3 tools/normalize_first_party_skill_sources.py
git add sources/first_party/skills/react
git commit -m "feat(MARK-348): create react ecosystem skill"
git push -u origin harleydbartles/mark-348-create-the-first-party-react-ecosystem-skill
```

- [ ] **Step 7: Record the registry snippet**

```json
{
  "canonical_name": "react",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/react",
  "local_path": "skills/react",
  "provenance_note": "Projected verbatim from the first-party react skill.",
  "copy_expectation": "byte_identical"
}
```

### Task 11: MARK-350 — Create `observability` skill

**Files:**
- Create: `sources/first_party/skills/observability/SKILL.md`
- Create: `sources/first_party/skills/observability/agents/openai.yaml`
- Create: `sources/first_party/skills/observability/references/operational-guidance.md`
- Create: `sources/first_party/skills/observability/assets/authority/authority.yaml`
- Create: `sources/first_party/skills/observability/assets/authority/source-map.yaml`
- Create: `sources/first_party/skills/observability/assets/authority/CITATIONS.md`
- Create: `sources/first_party/skills/observability/assets/authority/reference-source/observability.tar.gz`

**Interfaces:**
- Consumes: `harleydbartles/afpse-epic`; canonical authority `https://github.com/open-telemetry/opentelemetry-specification` (Apache-2.0).
- Produces: `observability` in `engineering-pack`.

Skill values:
- `<skill>` = `observability`
- `<Skill Title>` = `Observability`
- `<pack>` = `engineering-pack`
- `<lane>` = `skills-with-source`
- `<canonical-url>` = `https://github.com/open-telemetry/opentelemetry-specification`
- `<pinned-source-url>` = `https://github.com/open-telemetry/opentelemetry-specification/archive/refs/heads/main.tar.gz`
- `<revision>` = `main`
- `<license-name>` = `Apache-2.0`
- `<license-url>` = `https://github.com/open-telemetry/opentelemetry-specification/blob/main/LICENSE`
- `<content-mode>` = `licensed_adaptation`
- `<source-sections>` = `["Data model", "Traces", "Metrics", "Logs"]`

Content brief for `references/operational-guidance.md`:
- Telemetry signals: traces, metrics, logs.
- OpenTelemetry data model and semantic conventions.
- Context propagation, span attributes, exporters.
- When to add instrumentation and how to avoid high cardinality.

`SKILL.md` description: "Use when designing OpenTelemetry instrumentation, trace/metric/log semantics, or telemetry pipelines. Do not use when the work is log aggregation infrastructure or APM vendor configuration."

- [ ] **Step 1: Branch from the epic**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
git checkout -b harleydbartles/mark-350-create-the-opentelemetry-observability-skill
```

- [ ] **Step 2: Scaffold the skill**

```bash
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name observability --custody marketplace --lane skills-with-source
```

- [ ] **Step 3: Download the canonical source**

```bash
curl.exe -L -o sources/first_party/skills/observability/assets/authority/reference-source/observability.tar.gz https://github.com/open-telemetry/opentelemetry-specification/archive/refs/heads/main.tar.gz
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/observability/assets/authority/reference-source/observability.tar.gz').read_bytes()).hexdigest())"
```

Record the SHA-256 as `<sha256>`.

- [ ] **Step 4: Clean up, write reference, write templates**

```bash
Remove-Item sources/first_party/skills/observability/assets/authority/reference-source/.gitkeep
Remove-Item sources/first_party/skills/observability/references/.gitkeep
```

Create `sources/first_party/skills/observability/references/operational-guidance.md` using the content brief. Write `SKILL.md` and `agents/openai.yaml` using the Common Templates.

- [ ] **Step 5: Write `assets/authority/authority.yaml`, `source-map.yaml`, and `CITATIONS.md`**

`CITATIONS.md`:

```markdown
# Authority record for observability

## Scholarly citation

- OpenTelemetry. "OpenTelemetry Specification." https://github.com/open-telemetry/opentelemetry-specification (accessed <YYYY-MM-DD>).
- OpenTelemetry Specification licensed under Apache-2.0.

## Derivation boundary

- Derived: traces, metrics, logs, resource semantics, context propagation, OTLP, semantic conventions.
- Outside scope: language SDK APIs, collector configuration, vendor backends.

## Attribution

- OpenTelemetry Specification used under Apache-2.0.

## Human review

- Reviewer: Harley Bartles
- Date: <YYYY-MM-DD>
- Decision: Approved. Operational SKILL.md text contains no inline citations.
```

- [ ] **Step 6: Validate, normalize, commit, push**

```bash
py -3 tools/validate_authority_assets.py
py -3 tools/normalize_first_party_skill_sources.py
git add sources/first_party/skills/observability
git commit -m "feat(MARK-350): create observability skill"
git push -u origin harleydbartles/mark-350-create-the-opentelemetry-observability-skill
```

- [ ] **Step 7: Record the registry snippet**

```json
{
  "canonical_name": "observability",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/observability",
  "local_path": "skills/observability",
  "provenance_note": "Projected verbatim from the first-party observability skill.",
  "copy_expectation": "byte_identical"
}
```

### Task 12: MARK-351 — Create `web-identity` citation-backed skill

**Files:**
- Create: `sources/first_party/skills/web-identity/SKILL.md`
- Create: `sources/first_party/skills/web-identity/agents/openai.yaml`
- Create: `sources/first_party/skills/web-identity/references/operational-guidance.md`
- Create: `sources/first_party/skills/web-identity/assets/authority/authority.yaml`
- Create: `sources/first_party/skills/web-identity/assets/authority/source-map.yaml`
- Create: `sources/first_party/skills/web-identity/assets/authority/CITATIONS.md`

**Interfaces:**
- Consumes: `harleydbartles/afpse-epic`; canonical authorities OAuth 2.0 / OIDC specifications and platform identity docs.
- Produces: `web-identity` in `security-pack`.

Skill values:
- `<skill>` = `web-identity`
- `<Skill Title>` = `Web Identity`
- `<pack>` = `security-pack`
- `<lane>` = `skills-with-citation`
- `<canonical-url>` = `https://datatracker.ietf.org/doc/html/rfc6749`
- `<pinned-source-url>` = `https://datatracker.ietf.org/doc/html/rfc6749`
- `<revision>` = `RFC 6749`
- `<license-name>` = `Multiple; see CITATIONS.md`
- `<license-url>` = `https://datatracker.ietf.org/doc/html/rfc6749`
- `<content-mode>` = `first_party_synthesis`
- `<source-sections>` = `["RFC 6749 OAuth 2.0", "OpenID Connect Core 1.0", "Platform identity docs"]`

Content brief for `references/operational-guidance.md`:
- OAuth 2.0 flows: authorization code, client credentials, device code.
- OIDC ID tokens and claims.
- Access token vs refresh token vs ID token.
- Client types, consent, identity providers, JWT validation.
- When to use which flow and when to involve human partner.

`SKILL.md` description: "Use when selecting OAuth 2.0 / OIDC flows, validating tokens, or integrating identity providers. Do not use when the work is bespoke session management or platform-specific IAM policy."

- [ ] **Step 1: Branch from the epic**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
git checkout -b harleydbartles/mark-351-create-the-cross-stack-web-identity-citation-backed-skill
```

- [ ] **Step 2: Scaffold the skill**

```bash
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name web-identity --custody marketplace --lane skills-with-citation
```

- [ ] **Step 3: Download primary authority snapshot to scratch**

```bash
New-Item -ItemType Directory -Force -Path ../_agent-scratch/agent-asset-marketplace/afpse-epic
curl.exe -L -o ../_agent-scratch/agent-asset-marketplace/afpse-epic/web-identity.html https://datatracker.ietf.org/doc/html/rfc6749
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('../_agent-scratch/agent-asset-marketplace/afpse-epic/web-identity.html').read_bytes()).hexdigest())"
Remove-Item ../_agent-scratch/agent-asset-marketplace/afpse-epic/web-identity.html
```

Record the SHA-256 as `<sha256>`.

- [ ] **Step 4: Remove `.gitkeep` files and write reference file**

```bash
Remove-Item sources/first_party/skills/web-identity/references/.gitkeep
```

Create `sources/first_party/skills/web-identity/references/operational-guidance.md` using the content brief. Invoke `superpowers-plus:writing-skills` and `mark-skill-authoring` to author the `SKILL.md` body under 500 words.

- [ ] **Step 5: Write `SKILL.md` and `agents/openai.yaml`**

Use the Common Templates with the values above.

- [ ] **Step 6: Write `assets/authority/authority.yaml`, `source-map.yaml`, and `CITATIONS.md`**

`CITATIONS.md`:

```markdown
# Authority record for web-identity

## Scholarly citation

- IETF RFC 6749. "The OAuth 2.0 Authorization Framework." https://datatracker.ietf.org/doc/html/rfc6749 (accessed <YYYY-MM-DD>).
- OpenID Foundation. "OpenID Connect Core 1.0." https://openid.net/specs/openid-connect-core-1_0.html (accessed <YYYY-MM-DD>).
- Platform identity documentation (Microsoft identity platform, Auth0, Okta) as citable operational context.

## Derivation boundary

- Derived: OAuth 2.0 flows, OIDC ID tokens, access/refresh tokens, identity providers, client types, consent, JWT claims.
- Outside scope: specific platform SDKs, vendor-specific configuration UI.

## Attribution

- Clean-room first-party synthesis under MIT; RFC and specification citations retained in CITATIONS.md only.

## Human review

- Reviewer: Harley Bartles
- Date: <YYYY-MM-DD>
- Decision: Approved. Operational SKILL.md text contains no inline citations.
```

- [ ] **Step 7: Validate, normalize, commit, push**

```bash
py -3 tools/validate_authority_assets.py
py -3 tools/normalize_first_party_skill_sources.py
git add sources/first_party/skills/web-identity
git commit -m "feat(MARK-351): create web-identity citation-backed skill"
git push -u origin harleydbartles/mark-351-create-the-cross-stack-web-identity-citation-backed-skill
```

- [ ] **Step 8: Record the registry snippet**

```json
{
  "canonical_name": "web-identity",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/web-identity",
  "local_path": "skills/web-identity",
  "provenance_note": "Projected verbatim from the first-party web-identity skill.",
  "copy_expectation": "byte_identical"
}
```

### Task 13: MARK-346 — Create `dotnet` ecosystem skill

**Files:**
- Create: `sources/first_party/skills/dotnet/SKILL.md`
- Create: `sources/first_party/skills/dotnet/agents/openai.yaml`
- Create: `sources/first_party/skills/dotnet/references/operational-guidance.md`
- Create: `sources/first_party/skills/dotnet/assets/authority/authority.yaml`
- Create: `sources/first_party/skills/dotnet/assets/authority/source-map.yaml`
- Create: `sources/first_party/skills/dotnet/assets/authority/CITATIONS.md`
- Create: `sources/first_party/skills/dotnet/assets/authority/reference-source/dotnet.tar.gz`

**Interfaces:**
- Consumes: `harleydbartles/afpse-epic` after foundation wave and `web-identity` are merged; canonical authorities `https://github.com/dotnet/docs` and `https://github.com/dotnet/AspNetCore.Docs` (both CC-BY-4.0).
- Produces: `dotnet` in `dotnet-pack`.

Do not start this task until the foundation wave (Tasks 2-7) and `web-identity` (Task 12) are merged into the epic.

Skill values:
- `<skill>` = `dotnet`
- `<Skill Title>` = `Dotnet`
- `<pack>` = `dotnet-pack`
- `<lane>` = `skills-with-source`
- `<canonical-url>` = `https://github.com/dotnet/docs`
- `<pinned-source-url>` = `https://github.com/dotnet/docs` (the SHA-256 below is for the combined local `dotnet.tar.gz`)
- `<revision>` = `main`
- `<license-name>` = `CC-BY-4.0`
- `<license-url>` = `https://github.com/dotnet/docs/blob/main/LICENSE`
- `<content-mode>` = `licensed_adaptation`
- `<source-sections>` = `["C# language", ".NET runtime", "ASP.NET Core"]`

Content brief for `references/operational-guidance.md`:
- C# language fundamentals (records, pattern matching, nullability, generics, async/await).
- .NET runtime: configuration, dependency injection, logging.
- ASP.NET Core: minimal APIs, middleware, routing, validation.
- Data access and testing (high-level; defer to language-specific skills for deep SQL/EF).

`SKILL.md` description: "Use when building or reviewing .NET ecosystem applications, C# language patterns, ASP.NET Core APIs, and common library choices. Do not use when the work is SQL/EF deep tuning, cloud deployment, or a language other than C#/.NET."

- [ ] **Step 1: Branch from the epic after dependencies merge**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
git checkout -b harleydbartles/mark-346-create-the-first-party-net-ecosystem-skill-and-migrate
```

- [ ] **Step 2: Scaffold the skill**

```bash
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name dotnet --custody marketplace --lane skills-with-source
```

- [ ] **Step 3: Download the canonical sources and build a combined archive**

```bash
New-Item -ItemType Directory -Force -Path sources/first_party/skills/dotnet/assets/authority/reference-source
New-Item -ItemType Directory -Force -Path ../_agent-scratch/agent-asset-marketplace/afpse-epic/dotnet-source
curl.exe -L -o sources/first_party/skills/dotnet/assets/authority/reference-source/dotnet-docs.tar.gz https://github.com/dotnet/docs/archive/refs/heads/main.tar.gz
curl.exe -L -o sources/first_party/skills/dotnet/assets/authority/reference-source/aspnetcore-docs.tar.gz https://github.com/dotnet/AspNetCore.Docs/archive/refs/heads/main.tar.gz
tar -xzf sources/first_party/skills/dotnet/assets/authority/reference-source/dotnet-docs.tar.gz -C ../_agent-scratch/agent-asset-marketplace/afpse-epic/dotnet-source
tar -xzf sources/first_party/skills/dotnet/assets/authority/reference-source/aspnetcore-docs.tar.gz -C ../_agent-scratch/agent-asset-marketplace/afpse-epic/dotnet-source
tar -czf sources/first_party/skills/dotnet/assets/authority/reference-source/dotnet.tar.gz -C ../_agent-scratch/agent-asset-marketplace/afpse-epic/dotnet-source .
Remove-Item sources/first_party/skills/dotnet/assets/authority/reference-source/dotnet-docs.tar.gz
Remove-Item sources/first_party/skills/dotnet/assets/authority/reference-source/aspnetcore-docs.tar.gz
Remove-Item -Recurse -Force ../_agent-scratch/agent-asset-marketplace/afpse-epic/dotnet-source
py -3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('sources/first_party/skills/dotnet/assets/authority/reference-source/dotnet.tar.gz').read_bytes()).hexdigest())"
```

Record the SHA-256 of `dotnet.tar.gz` as `<sha256>`.

- [ ] **Step 4: Clean up, write reference, write templates**

```bash
Remove-Item sources/first_party/skills/dotnet/assets/authority/reference-source/.gitkeep
Remove-Item sources/first_party/skills/dotnet/references/.gitkeep
```

Create `sources/first_party/skills/dotnet/references/operational-guidance.md` using the content brief. Write `SKILL.md` and `agents/openai.yaml` using the Common Templates.

- [ ] **Step 5: Write `assets/authority/authority.yaml`, `source-map.yaml`, and `CITATIONS.md`**

`CITATIONS.md`:

```markdown
# Authority record for dotnet

## Scholarly citation

- Microsoft. ".NET documentation." https://github.com/dotnet/docs (accessed <YYYY-MM-DD>).
- Microsoft. "ASP.NET Core documentation." https://github.com/dotnet/AspNetCore.Docs (accessed <YYYY-MM-DD>).
- Both repositories' documentation content licensed under CC-BY-4.0.

## Derivation boundary

- Derived: C# language, .NET runtime, ASP.NET Core web apps, minimal APIs, EF Core, testing.
- Outside scope: .NET runtime source code, Visual Studio tooling, Azure services.

## Attribution

- .NET and ASP.NET Core documentation used under CC-BY-4.0.

## Human review

- Reviewer: Harley Bartles
- Date: <YYYY-MM-DD>
- Decision: Approved. Operational SKILL.md text contains no inline citations.
```

- [ ] **Step 6: Validate, normalize, commit, push**

```bash
py -3 tools/validate_authority_assets.py
py -3 tools/normalize_first_party_skill_sources.py
git add sources/first_party/skills/dotnet
git commit -m "feat(MARK-346): create dotnet ecosystem skill"
git push -u origin harleydbartles/mark-346-create-the-first-party-net-ecosystem-skill-and-migrate
```

- [ ] **Step 7: Record the registry snippet**

```json
{
  "canonical_name": "dotnet",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/dotnet",
  "local_path": "skills/dotnet",
  "provenance_note": "Projected verbatim from the first-party dotnet ecosystem skill.",
  "copy_expectation": "byte_identical"
}
```

### Task 14: MARK-352 — Qualify next authoritative-source specialist candidates

**Files:**
- Create: `provenance/afpse-candidate-qualification.md`

**Interfaces:**
- Consumes: all source-backed skill branches landed; authority and licensing patterns observed during execution.
- Produces: decision matrix only; no new skills.

- [ ] **Step 1: Branch from the epic after source lanes are stable**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
git checkout -b harleydbartles/mark-352-qualify-the-next-authoritative-source-specialist-candidates
```

- [ ] **Step 2: Create the candidate qualification matrix**

Create `provenance/afpse-candidate-qualification.md` with a decision matrix covering candidate specialisms such as `graphql`, `kubernetes`, `rust`, `go`, `python-language`, `mobile-platforms`, and `api-gateways`. For each candidate include:

- Proposed skill name.
- Canonical authority URL(s) or repository.
- License and vendoring feasibility.
- Primary pack home.
- Overlapping third-party entries to retire.
- Confidence rating and open questions.

Use the observed licensing outcomes from Tasks 2-13 to calibrate feasibility.

- [ ] **Step 3: Commit and push**

```bash
git add provenance/afpse-candidate-qualification.md
git commit -m "docs(MARK-352): qualify next authoritative-source specialist candidates"
git push -u origin harleydbartles/mark-352-qualify-the-next-authoritative-source-specialist-candidates
```

### Task 15: `dotnet-pack` plugin-root bootstrapping from `dotnet-kit`

**Files:**
- Create: `codex-marketplace/plugins/dotnet-pack/.codex-plugin/plugin.json`
- Create: `codex-marketplace/plugins/dotnet-pack/README.md`
- Create: `codex-marketplace/plugins/dotnet-pack/SOURCE.md`
- Create: `codex-marketplace/plugins/dotnet-pack/PROJECTION.md`
- Create: `codex-marketplace/plugins/dotnet-pack/LICENSE`
- Create: `codex-marketplace/plugins/dotnet-pack/assets/icon.svg`
- Create: `provenance/dotnet-pack.md`

**Interfaces:**
- Consumes: `dotnet` skill branch merged; retiring `dotnet-kit` plugin root.
- Produces: new `dotnet-pack` plugin root containing only the first-party `dotnet` skill; ready for registry integration.

- [ ] **Step 1: Check out the epic and create the new plugin root**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
New-Item -ItemType Directory -Force -Path codex-marketplace/plugins/dotnet-pack/.codex-plugin
New-Item -ItemType Directory -Force -Path codex-marketplace/plugins/dotnet-pack/assets
New-Item -ItemType Directory -Force -Path codex-marketplace/plugins/dotnet-pack/references
```

- [ ] **Step 2: Copy and edit the plugin manifest**

Copy `codex-marketplace/plugins/dotnet-kit/.codex-plugin/plugin.json` to `codex-marketplace/plugins/dotnet-pack/.codex-plugin/plugin.json`, then edit to:

```json
{
  "name": "dotnet-pack",
  "version": "1.0.0",
  "description": "First-party .NET ecosystem pack projected from the dotnet skill.",
  "author": {
    "name": "Harley Bartles"
  },
  "homepage": "https://github.com/HarleyBartles/agent-asset-marketplace",
  "repository": "https://github.com/HarleyBartles/agent-asset-marketplace",
  "license": "MIT",
  "keywords": [
    "dotnet",
    "csharp",
    "aspnetcore",
    "codex"
  ],
  "skills": "./skills/",
  "interface": {
    "displayName": "Dotnet Pack",
    "shortDescription": ".NET ecosystem Codex pack",
    "longDescription": "A repo-local Codex plugin bundle projecting the first-party .NET ecosystem skill.",
    "developerName": "Harley Bartles",
    "category": "Productivity",
    "capabilities": [
      "Interactive",
      "Write"
    ],
    "defaultPrompt": [
      "Inspect the dotnet-pack source map and bundle manifest.",
      "Use the pack to install the dotnet skill.",
      "Confirm provider-specific assumptions are stripped from the projection."
    ],
    "brandColor": "#0F4C81",
    "composerIcon": "./assets/icon.svg",
    "logo": "./assets/icon.svg"
  }
}
```

- [ ] **Step 3: Copy static assets**

```bash
Copy-Item codex-marketplace/plugins/dotnet-kit/LICENSE codex-marketplace/plugins/dotnet-pack/LICENSE
Copy-Item codex-marketplace/plugins/dotnet-kit/assets/icon.svg codex-marketplace/plugins/dotnet-pack/assets/icon.svg
```

- [ ] **Step 4: Write `README.md` with generated-content markers**

Create `codex-marketplace/plugins/dotnet-pack/README.md`:

```markdown
# Dotnet Pack

This plugin bundle projects the first-party .NET ecosystem skill into an installable Codex marketplace pack.

## Bundle contents
<!-- BEGIN GENERATED: bundle-contents -->
<!-- END GENERATED: bundle-contents -->

### Documentation
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary
- `dotnet` carries the first-party .NET ecosystem guidance.
- Provider-specific assumptions from the upstream snapshot are stripped or rewritten in the installable pack.

## Install shape

The installable skill zips are generated under `generated/skill-zips/dotnet-pack/<skill-name>/skill.zip`.
```

- [ ] **Step 5: Write `SOURCE.md` with generated-content markers**

Create `codex-marketplace/plugins/dotnet-pack/SOURCE.md`:

```markdown
# Source

This plugin projects the first-party `dotnet` skill into a Codex marketplace pack.

<!-- BEGIN GENERATED: pack-inventory -->
<!-- END GENERATED: pack-inventory -->

## Boundary
- `dotnet` is first-party source custody under `sources/first_party/skills/dotnet/`.
```

- [ ] **Step 6: Write `PROJECTION.md` with generated-content markers**

Create `codex-marketplace/plugins/dotnet-pack/PROJECTION.md`:

```markdown
# Projection

This root is the Codex-facing marketplace projection of the .NET ecosystem pack.

## Layer Model

This repository uses two distinct layers for the dotnet-pack bundle:

- Source custody keeps the first-party `dotnet` skill verbatim.
- Projection layer holds the source-controlled marketplace copy with first-party selection decisions.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected skill is materialized from `sources/first_party/skills/dotnet/` per the registry.
- Frontmatter contract: [.agents/docs/contracts/skill-frontmatter.md](../../../.agents/docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [.agents/docs/contracts/openai-agent-yaml.md](../../../.agents/docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the first-party source custody root.
- Do apply projection-layer adaptations in the marketplace copy where they can be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `dotnet-pack` is the .NET ecosystem plugin projection.
<!-- BEGIN GENERATED: projection-contract -->
<!-- END GENERATED: projection-contract -->
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/icon.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/bundle-manifest.json`
- `references/source-map.md`
```

- [ ] **Step 7: Write `provenance/dotnet-pack.md`**

Create `provenance/dotnet-pack.md`:

```markdown
# Dotnet Pack Provenance

This plugin projects the first-party `dotnet` ecosystem skill into a Codex marketplace pack.

## Upstream basis

- `dotnet` first-party skill: `sources/first_party/skills/dotnet/`

## Pack shape

- Codex plugin root: `codex-marketplace/plugins/dotnet-pack/`
- Skill root: `codex-marketplace/plugins/dotnet-pack/skills/`
- Generated install units: `generated/skill-zips/dotnet-pack/<skill-name>/skill.zip`

## Rights and Attribution

- `dotnet` content is MIT-licensed first-party.
```

- [ ] **Step 8: Validate the new plugin root shape**

```bash
py -3 tools/validate_authority_assets.py
py -3 tools/normalize_first_party_skill_sources.py --check
```

Expected: no errors.

- [ ] **Step 9: Commit and push**

```bash
git add codex-marketplace/plugins/dotnet-pack provenance/dotnet-pack.md
git commit -m "feat: bootstrap dotnet-pack plugin root from dotnet-kit"
git push origin harleydbartles/afpse-epic
```

### Task 16: Registry integration in `codex-marketplace/custody-pack-registry.json`

**Files:**
- Modify: `codex-marketplace/custody-pack-registry.json`
- Modify: `codex-marketplace/plugin-roots.json` (generated by `tools/generate_plugin_root_inventory.py`)

**Interfaces:**
- Consumes: all registry snippets from Tasks 2-14; `dotnet-pack` plugin root from Task 15.
- Produces: updated registry ready for full marketplace rebuild.

- [ ] **Step 1: Check out the epic and create a registry branch**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
git checkout -b harleydbartles/mark-afpse-registry-integration
```

- [ ] **Step 2: Remove retired third-party entries**

In `codex-marketplace/custody-pack-registry.json`, remove the following `entries` objects by `canonical_name`:

- `architecture-pack`: remove `cqrs-event-sourcing`
- `api-contracts-pack`: remove `openapi-specification`
- `security-pack`: remove `owasp-top-10`
- `frontend-pack`: remove `accessibility-audit` and `react-performance-optimization`
- `language-patterns-pack`: remove `typescript-advanced-patterns`

- [ ] **Step 3: Add first-party entries to existing packs**

Add these objects to the `entries` arrays of the named packs:

`architecture-pack` entries to add:

```json
[
{
  "canonical_name": "ddd",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/ddd",
  "local_path": "skills/ddd",
  "provenance_note": "Projected verbatim from the first-party ddd skill.",
  "copy_expectation": "byte_identical"
},
{
  "canonical_name": "cqrs",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/cqrs",
  "local_path": "skills/cqrs",
  "provenance_note": "Projected verbatim from the first-party cqrs skill.",
  "copy_expectation": "byte_identical"
},
{
  "canonical_name": "event-sourcing",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/event-sourcing",
  "local_path": "skills/event-sourcing",
  "provenance_note": "Projected verbatim from the first-party event-sourcing skill.",
  "copy_expectation": "byte_identical"
},
{
  "canonical_name": "clean-architecture",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/clean-architecture",
  "local_path": "skills/clean-architecture",
  "provenance_note": "Projected verbatim from the first-party clean-architecture skill.",
  "copy_expectation": "byte_identical"
},
{
  "canonical_name": "hexagonal-architecture",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/hexagonal-architecture",
  "local_path": "skills/hexagonal-architecture",
  "provenance_note": "Projected verbatim from the first-party hexagonal-architecture skill.",
  "copy_expectation": "byte_identical"
}
]
```

`api-contracts-pack` entry to add:

```json
{
  "canonical_name": "openapi-specification",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/openapi-specification",
  "local_path": "skills/openapi-specification",
  "provenance_note": "Projected verbatim from the first-party openapi-specification skill.",
  "copy_expectation": "byte_identical"
}
```

`security-pack` entries to add:

```json
[
{
  "canonical_name": "owasp-top-ten",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/owasp-top-ten",
  "local_path": "skills/owasp-top-ten",
  "provenance_note": "Projected verbatim from the first-party owasp-top-ten skill.",
  "copy_expectation": "byte_identical"
},
{
  "canonical_name": "web-identity",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/web-identity",
  "local_path": "skills/web-identity",
  "provenance_note": "Projected verbatim from the first-party web-identity skill.",
  "copy_expectation": "byte_identical"
}
]
```

`frontend-pack` entries to add:

```json
[
{
  "canonical_name": "wcag",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/wcag",
  "local_path": "skills/wcag",
  "provenance_note": "Projected verbatim from the first-party wcag skill.",
  "copy_expectation": "byte_identical"
},
{
  "canonical_name": "react",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/react",
  "local_path": "skills/react",
  "provenance_note": "Projected verbatim from the first-party react skill.",
  "copy_expectation": "byte_identical"
},
{
  "canonical_name": "web-styling",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/web-styling",
  "local_path": "skills/web-styling",
  "provenance_note": "Projected verbatim from the first-party web-styling skill.",
  "copy_expectation": "byte_identical"
}
]
```

`language-patterns-pack` entry to add:

```json
{
  "canonical_name": "typescript",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/typescript",
  "local_path": "skills/typescript",
  "provenance_note": "Projected verbatim from the first-party typescript skill.",
  "copy_expectation": "byte_identical"
}
```

`engineering-pack` entry to add:

```json
{
  "canonical_name": "observability",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/observability",
  "local_path": "skills/observability",
  "provenance_note": "Projected verbatim from the first-party observability skill.",
  "copy_expectation": "byte_identical"
}
```

- [ ] **Step 4: Replace the `dotnet-claude-kit` mega-pack node with the `dotnet-pack` projection-lane node**

Remove the `dotnet-claude-kit` mega-pack node and insert the following node in its place in `codex-marketplace/custody-pack-registry.json`:

```json
{
  "bundle_name": "dotnet-pack",
  "plugin_root": "codex-marketplace/plugins/dotnet-pack",
  "bundle_version": "1.0.0",
  "bundle_type": "projection-lane",
  "category": "Productivity",
  "is_mega_pack": false,
  "notes": [
    ".NET ecosystem pack projects the first-party dotnet skill."
  ],
  "source_ledger": [
    "sources/first_party/skills/dotnet/SKILL.md"
  ],
  "provenance_refs": [
    "provenance/dotnet-pack.md"
  ],
  "generated_doc_surfaces": [
    "README.md",
    "SOURCE.md",
    "PROJECTION.md"
  ],
  "entries": [
    {
      "canonical_name": "dotnet",
      "source_category": "first_party",
      "content_mode": "verbatim",
      "source_family": "first_party",
      "canonical_source_path": "sources/first_party/skills/dotnet",
      "local_path": "skills/dotnet",
      "provenance_note": "Projected verbatim from the first-party dotnet ecosystem skill.",
      "copy_expectation": "byte_identical"
    }
  ]
}
```

- [ ] **Step 5: Delete the drained third-party source and adapter trees**

```powershell
Remove-Item -Recurse -Force sources/third_party/dotnet-claude-kit/upstream
Remove-Item -Recurse -Force adapters/codex/dotnet-kit
```

Expected: `sources/third_party/dotnet-claude-kit/upstream/` and `adapters/codex/dotnet-kit/` no longer exist.

- [ ] **Step 6: Regenerate the plugin-root inventory**

```bash
py -3 tools/generate_plugin_root_inventory.py
```

Expected: `Wrote codex-marketplace/plugin-roots.json`.

- [ ] **Step 7: Validate registry and plugin root inventory**

```bash
py -3 tools/generate_plugin_root_inventory.py --check
py -3 tools/validate_authority_assets.py
py -3 tools/normalize_first_party_skill_sources.py --check
```

Expected: plugin-root inventory is current and authority assets are valid. `generate_pack_manifests` checks are intentionally deferred to Task 17 (`rebuild_marketplace.py` and `check_marketplace.py`) because the new `dotnet-pack` bundle manifest is generated as part of the full marketplace rebuild.

- [ ] **Step 8: Commit the registry changes**

```bash
git add -u
git add codex-marketplace/custody-pack-registry.json codex-marketplace/plugin-roots.json
git commit -m "feat: integrate first-party skill assignments and dotnet-pack registry node"
git push origin harleydbartles/mark-afpse-registry-integration
```

### Task 17: Merge branches, full marketplace rebuild, CI gate, and PR

**Files:**
- Modify: `harleydbartles/afpse-epic` (merge all issue branches)
- Modify: generated surfaces under `codex-marketplace/`, `.agents/plugins/`, `generated/skill-zips/`, `repo-index/`, etc.

**Interfaces:**
- Consumes: all validated issue branches and registry integration branch.
- Produces: one master PR to `main` with full head SHA.

- [ ] **Step 1: Fast-merge all issue branches into the epic**

```bash
git checkout harleydbartles/afpse-epic
git pull origin harleydbartles/afpse-epic
$branches = @(
  "harleydbartles/mark-340-re-custody-ddd-from-the-eric-evans-ddd-reference",
  "harleydbartles/mark-341-split-cqrs-and-event-sourcing-into-clean-room-citation",
  "harleydbartles/mark-342-create-clean-architecture-and-hexagonal-architecture-citation-backed",
  "harleydbartles/mark-343-re-custody-owasp-top-ten-and-establish-an-asvs-verification",
  "harleydbartles/mark-344-re-custody-the-openapi-specification-specialist-skill",
  "harleydbartles/mark-345-re-custody-the-wcag-accessibility-audit-specialist-skill",
  "harleydbartles/mark-346-create-the-first-party-net-ecosystem-skill-and-migrate",
  "harleydbartles/mark-347-create-the-first-party-typescript-ecosystem-skill",
  "harleydbartles/mark-348-create-the-first-party-react-ecosystem-skill",
  "harleydbartles/mark-349-create-the-cross-framework-web-styling-skill",
  "harleydbartles/mark-350-create-the-opentelemetry-observability-skill",
  "harleydbartles/mark-351-create-the-cross-stack-web-identity-citation-backed-skill",
  "harleydbartles/mark-352-qualify-the-next-authoritative-source-specialist-candidates",
  "harleydbartles/mark-afpse-registry-integration"
)
foreach ($branch in $branches) {
  git merge --no-ff $branch -m "merge $branch into afpse-epic"
}
```

- [ ] **Step 2: Run the canonical full marketplace rebuild**

```bash
py -3 tools/rebuild_marketplace.py --base origin/main
```

Expected: exits 0. Review the generated surfaces for `dotnet-pack`, updated pack entries, and new first-party skill projections.

- [ ] **Step 3: Commit generated surfaces**

```bash
git add -A
git commit -m "chore: regenerate marketplace projections for afpse-epic"
```

- [ ] **Step 4: Run the CI gate**

```bash
py -3 tools/check_marketplace.py --base origin/main
```

Expected: exits 0.

- [ ] **Step 5: Push the epic branch and open the master PR**

```bash
git push origin harleydbartles/afpse-epic
git rev-parse HEAD
```

Expected: head SHA printed. Use it plus the branch name `harleydbartles/afpse-epic` to open a PR into `main` with the title:

`feat: authoritative first-party skill enrichment (AFPSE)`

Use `pr_body.txt` at the repo root or summarize:

- Re-custodies `ddd`, `owasp-top-ten`, `openapi-specification`, `wcag`.
- Creates first-party `cqrs`, `event-sourcing`, `clean-architecture`, `hexagonal-architecture`, `typescript`, `react`, `web-styling`, `observability`, `web-identity`, `dotnet`.
- Replaces `dotnet-kit` with `dotnet-pack`.
- Updates `codex-marketplace/custody-pack-registry.json` and regenerates all marketplace surfaces.
- Closes MARK-339 through MARK-352.

- [ ] **Step 6: Publication proof**

Return must include:
- open PR URL;
- branch name `harleydbartles/afpse-epic`;
- full head SHA from `git rev-parse HEAD`.

## Plan Self-Review and Execution Confidence

**SDD Confidence Rating:** 8/10.

**Why not 10/10:**
- Exact upstream snapshot identity (default branch names, vendoring feasibility, and precise license URLs for CSS Modules/Sass/styled-components) must be discovered during execution. The plan provides candidate URLs and explicit license-verification gates.
- The `dotnet` combined source archive command depends on `tar` and scratch-folder behavior; the SHA-256 is computed after the fact, so the exact archive contents are not pre-determined.
- Operational `SKILL.md` prose is intentionally authored by `superpowers-plus:writing-skills` and `mark-skill-authoring` under the 500-word limit, so the final wording is not fully specified in the plan.

**Verifications performed against current source:**
- `new_skill.py` exists at `.agents/skills/mark-skill-authoring/scripts/new_skill.py` and accepts `--name`, `--custody marketplace`, and `--lane` values used in the plan.
- `tools/validate_authority_assets.py`, `tools/normalize_first_party_skill_sources.py`, `tools/rebuild_marketplace.py`, `tools/check_marketplace.py`, `tools/generate_plugin_root_inventory.py`, and `tools/generate_pack_manifests.py` all exist and support the flags used in the plan.
- `codex-marketplace/custody-pack-registry.json` contains the existing pack nodes and `entries` arrays referenced in Task 16.
- `codex-marketplace/plugins/dotnet-kit/` contains the files used for `dotnet-pack` bootstrapping (LICENSE, icon, and plugin.json); `adapters/codex/dotnet-kit/` and the `dotnet-claude-kit` upstream snapshot are removed in Task 16.
- The current branch is `harleydbartles/afpse-epic` and `origin/main` resolves.

**Known gaps / discovery required during execution:**
1. `web-styling` upstream license check: if any candidate source is not redistributable, switch to `skills-with-citation` and update `CITATIONS.md` and `content_mode`.
2. `typescript` archive URL: verify the default branch is still `v2`; if `master` or `main` is now primary, update the `curl` URL.
3. `dotnet` upstream license: confirm `dotnet/docs` and `AspNetCore.Docs` are still CC-BY-4.0 and that combined vendoring is acceptable.
4. `ddd` source page is a single web page; if it is not curl-able or requires JavaScript, fall back to a citation-backed approach.
