# Unslop-plus split into unslop-engine and unslop-profiles

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Retire the `unslop-plus` skill, split it into `unslop-engine` and `unslop-profiles` first-party skills, and wire both into the `unslop-plus` plugin, `repo-worker-pack`, and `house-skills`.

**Architecture:** Two focused source skills replace the monolithic skill. `unslop-engine` carries the adapted `unslop.py` engine and authority records; `unslop-profiles` is a read-when router with the 13 existing profile files. The `unslop-plus` plugin becomes a projection-lane pack, `repo-worker-pack` carries `unslop-profiles` for default install, and `house-skills` auto-includes both from first-party source.

**Tech Stack:** Markdown skill files, YAML frontmatter, JSON registry, Python helper scripts, Codex plugin manifests, `py -3 tools/rebuild_marketplace.py` / `py -3 tools/check_marketplace.py`.

## Global Constraints

- Do not edit `sources/third_party/unslop/upstream/`.
- Do not change `codex-marketplace/plugin-roots.json`.
- Do not add new profiles or rewrite `unslop.py`.
- Do not edit generated plugin surfaces by hand; edit the registry and source skills, then regenerate.
- All text files must use LF line endings (`newline="\n"` in Python, or ensure no CRLF).
- `generated/skill-zips/unslop-plus.zip` must be deleted after the rebuild.
- `sources/first_party/skills/unslop-plus/` must be deleted after migration.

---

### Task 1: Create `unslop-engine` source skill

**Files:**
- Create: `sources/first_party/skills/unslop-engine/SKILL.md`
- Create: `sources/first_party/skills/unslop-engine/agents/openai.yaml`
- Create: `sources/first_party/skills/unslop-engine/assets/authority/authority.yaml`
- Create: `sources/first_party/skills/unslop-engine/assets/authority/source-map.yaml`
- Create: `sources/first_party/skills/unslop-engine/assets/authority/CITATIONS.md`
- Create: `sources/first_party/skills/unslop-engine/references/upstream-provenance.md`
- Move/copy: `sources/first_party/skills/unslop-plus/scripts/unslop.py` → `sources/first_party/skills/unslop-engine/scripts/unslop.py`
- Move/copy: `sources/first_party/skills/unslop-plus/scripts/validate_unslop_output.py` → `sources/first_party/skills/unslop-engine/scripts/validate_unslop_output.py`
- Move/update: `sources/first_party/skills/unslop-plus/scripts/validate_package.py` → `sources/first_party/skills/unslop-engine/scripts/validate_package.py`
- Move/copy: `sources/first_party/skills/unslop-plus/LICENSE.upstream` → `sources/first_party/skills/unslop-engine/LICENSE.upstream`

**Interfaces:**
- Consumes: upstream `mshumer/unslop` concept, existing `unslop-plus/scripts/unslop.py`.
- Produces: `sources/first_party/skills/unslop-engine/` source root ready for projection.

- [x] **Step 1.1: Create the source directory tree**

Run:
```bash
mkdir -p sources/first_party/skills/unslop-engine/scripts
mkdir -p sources/first_party/skills/unslop-engine/agents
mkdir -p sources/first_party/skills/unslop-engine/assets/authority
mkdir -p sources/first_party/skills/unslop-engine/references
```

- [x] **Step 1.2: Move/copy engine scripts and upstream license**

Run:
```bash
cp sources/first_party/skills/unslop-plus/scripts/unslop.py sources/first_party/skills/unslop-engine/scripts/unslop.py
cp sources/first_party/skills/unslop-plus/scripts/validate_unslop_output.py sources/first_party/skills/unslop-engine/scripts/validate_unslop_output.py
cp sources/first_party/skills/unslop-plus/LICENSE.upstream sources/first_party/skills/unslop-engine/LICENSE.upstream
cp sources/first_party/skills/unslop-plus/references/upstream-provenance.md sources/first_party/skills/unslop-engine/references/upstream-provenance.md
```

- [x] **Step 1.3: Update `references/upstream-provenance.md` path references**

Edit `sources/first_party/skills/unslop-engine/references/upstream-provenance.md` and replace any references to `skills/unslop-plus/` with `skills/unslop-engine/`. Use `grep` to confirm there are no remaining `unslop-plus` strings.

- [x] **Step 1.4: Write `SKILL.md`**

Create `sources/first_party/skills/unslop-engine/SKILL.md` with this content:

```markdown
---
name: unslop-engine
description: Use when you need to empirically detect repetitive AI output patterns in a domain and generate a reusable anti-slop profile.
license: MIT
metadata:
  source-id: unslop-engine
  source-path: sources/first_party/skills/unslop-engine/SKILL.md
  provenance-name: Unslop Engine first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  use_when:
    - Use when generating a domain-specific anti-slop profile from samples or observed defaults.
  do_not_use_when:
    - Do not use when applying an existing anti-slop profile to a task.
  related_skills:
    - unslop-profiles
---

# Unslop Engine

## When to Use

Use this skill when you need to empirically detect repetitive AI output patterns in a domain and generate a reusable anti-slop profile.

Do not use this skill when applying an existing anti-slop profile; use `$unslop-profiles` instead.

## Core Pattern

1. Identify the domain and whether you are analyzing text or visual samples.
2. Collect representative samples (inline, fixture files, or a sample directory).
3. Run the engine:
   ```bash
   py -3 scripts/unslop.py --domain "..." [--type visual --count N]
   ```
4. Review the generated artifacts in `unslop-output/`:
   - `analysis.md` — counted repeated patterns
   - `skill.md` — generated anti-slop profile
5. Return the profile name, the dominant repeated patterns, and how to use the profile.
```

- [x] **Step 1.5: Write `agents/openai.yaml`**

Create `sources/first_party/skills/unslop-engine/agents/openai.yaml`:

```yaml
interface:
  display_name: Unslop Engine
  short_description: Use when generating a reusable anti-slop profile from observed defaults.
  default_prompt: Use $unslop-engine to analyze a domain for repetitive AI defaults and generate a reusable anti-slop profile.
policy:
  allow_implicit_invocation: false
```

- [x] **Step 1.6: Write authority records**

Create `sources/first_party/skills/unslop-engine/assets/authority/authority.yaml`:

```yaml
schema_version: 1
custody: marketplace
lane: skills-with-citation
authority:
  title: "mshumer/unslop"
  canonical_url: https://github.com/mshumer/unslop
  pinned_source_url: https://github.com/mshumer/unslop/blob/edcb62386d129c65e4395f0cfcc9168eb1ba2148/README.md
  latest_check_url: https://github.com/mshumer/unslop
  revision: edcb62386d129c65e4395f0cfcc9168eb1ba2148
  retrieved_at: "2026-07-22"
  content_sha256: 5c5e317d341aa63d73f73ca0b50309ca712acaebf660c6057b4ee376736643bd
  license: MIT
  license_url: https://github.com/mshumer/unslop/blob/main/LICENSE
decomposition:
  reconciled_against: 5c5e317d341aa63d73f73ca0b50309ca712acaebf660c6057b4ee376736643bd
  references:
    - path: SKILL.md
      source_sections:
        - Upstream unslop engine concept
      load_when:
        - Use when generating a domain-specific anti-slop profile.
      content_mode: first_party_synthesis
    - path: references/upstream-provenance.md
      source_sections:
        - Upstream provenance and adaptation rationale
      load_when:
        - Use when verifying authority or provenance.
      content_mode: first_party_synthesis
```

Create `sources/first_party/skills/unslop-engine/assets/authority/source-map.yaml`:

```yaml
schema_version: 1
reconciled_against: 5c5e317d341aa63d73f73ca0b50309ca712acaebf660c6057b4ee376736643bd
references:
  - path: SKILL.md
    source_sections:
      - Upstream unslop engine concept
    load_when:
      - Use when generating a domain-specific anti-slop profile.
    content_mode: first_party_synthesis
  - path: references/upstream-provenance.md
    source_sections:
      - Upstream provenance and adaptation rationale
    load_when:
      - Use when verifying authority or provenance.
    content_mode: first_party_synthesis
```

Create `sources/first_party/skills/unslop-engine/assets/authority/CITATIONS.md`:

```markdown
# Authority record for unslop-engine

## Scholarly citation

- Upstream repository: https://github.com/mshumer/unslop
- Pinned commit: edcb62386d129c65e4395f0cfcc9168eb1ba2148
- License: MIT
- Upstream README SHA-256: 5c5e317d341aa63d73f73ca0b50309ca712acaebf660c6057b4ee376736643bd

## Derivation boundary

- The unslop-engine `SKILL.md` is a first-party operational synthesis of the upstream engine concept (sample collection, pattern detection, profile generation) adapted for Codex/GPT skill use.
- The bundled `scripts/unslop.py` is an Asset Marketplace adaptation that replaces the upstream `claude` CLI dependency with Python standard library text analysis and optional Playwright visual evidence.
- The upstream MIT license and copyright are preserved in `LICENSE.upstream`.

## Human review

- Reviewer: Harley Bartles
- Date: 2026-07-22
- Decision: Approved. Operational `SKILL.md` body contains no inline citations; source-grounded claims are recorded in `assets/authority/`.
```

- [x] **Step 1.7: Write updated `scripts/validate_package.py`**

Create `sources/first_party/skills/unslop-engine/scripts/validate_package.py`:

```python
#!/usr/bin/env python3
"""Validate the unslop-engine source skill files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED = [
    "SKILL.md",
    "agents/openai.yaml",
    "scripts/unslop.py",
    "scripts/validate_unslop_output.py",
    "scripts/validate_package.py",
    "references/upstream-provenance.md",
    "assets/authority/authority.yaml",
    "assets/authority/CITATIONS.md",
    "assets/authority/source-map.yaml",
]


def forbidden_fragments() -> list[str]:
    return [
        "git " + "clone https://github.com/mshumer/unslop",
        "claude" + " -p",
        "requires " + "Claude Code",
    ]


def validate(skill_root: Path) -> list[str]:
    issues: list[str] = []
    for rel in REQUIRED:
        if not (skill_root / rel).exists():
            issues.append(f"missing {rel}")

    checked_files = [
        file
        for file in skill_root.rglob("*")
        if file.is_file()
        and file.suffix.lower() in {".md", ".json", ".yaml", ".py", ".txt"}
    ]
    for file in checked_files:
        content = file.read_text(encoding="utf-8", errors="ignore").lower()
        for forbidden in forbidden_fragments():
            if forbidden.lower() in content:
                issues.append(f"forbidden runtime instruction in {file.relative_to(skill_root)}")

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_root", type=Path, nargs="?", default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    issues = validate(args.skill_root)
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}", file=sys.stderr)
        return 1
    print(f"OK: {args.skill_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [x] **Step 1.8: Verify the source skill shape**

Run:
```bash
py -3 sources/first_party/skills/unslop-engine/scripts/validate_package.py
```
Expected: `OK: sources/first_party/skills/unslop-engine`

- [x] **Step 1.9: Commit**

```bash
git add sources/first_party/skills/unslop-engine
git commit -m "feat(unslop): create unslop-engine first-party source skill

Move adapted unslop.py, validators, and provenance from unslop-plus.
Add SKILL.md, agents/openai.yaml, and skills-with-citation authority records.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
```

---

### Task 2: Create `unslop-profiles` source skill

**Files:**
- Create: `sources/first_party/skills/unslop-profiles/SKILL.md`
- Create: `sources/first_party/skills/unslop-profiles/agents/openai.yaml`
- Copy: `sources/first_party/skills/unslop-plus/profiles/*.md` → `sources/first_party/skills/unslop-profiles/profiles/*.md`

**Interfaces:**
- Consumes: the 13 existing profile files from `unslop-plus/profiles/`.
- Produces: `sources/first_party/skills/unslop-profiles/` source root ready for projection.

- [x] **Step 2.1: Create the source directory tree and copy profiles**

Run:
```bash
mkdir -p sources/first_party/skills/unslop-profiles/agents
mkdir -p sources/first_party/skills/unslop-profiles/profiles
cp sources/first_party/skills/unslop-plus/profiles/*.md sources/first_party/skills/unslop-profiles/profiles/
```

Verify:
```bash
ls sources/first_party/skills/unslop-profiles/profiles/
```
Expected: `api-design.md`, `architecture.md`, `cleanup-custody.md`, `code-review.md`, `debugging.md`, `frontend-react.md`, `frontend-ui.md`, `implementation-plans.md`, `security-review.md`, `technical-writing.md`, `testing.md`, `worker-returns.md`, `writing.md`

- [x] **Step 2.2: Write `SKILL.md`**

Create `sources/first_party/skills/unslop-profiles/SKILL.md`:

```markdown
---
name: unslop-profiles
description: Use when applying anti-slop guidance to writing, documentation, implementation plans, code review, worker returns, debugging, React work, UI design, API design, architecture, testing, security review, or repository cleanup.
license: MIT
metadata:
  source-id: unslop-profiles
  source-path: sources/first_party/skills/unslop-profiles/SKILL.md
  provenance-name: Unslop Profiles first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  use_when:
    - Use when writing general prose.
    - Use when writing or reviewing technical documentation.
    - Use when drafting implementation plans.
    - Use when reviewing code changes.
    - Use when writing worker return reports.
    - Use when debugging software.
    - Use when building React frontends.
    - Use when designing generic UI.
    - Use when designing APIs.
    - Use when reasoning about architecture.
    - Use when writing or reviewing tests.
    - Use when performing security reviews.
    - Use when classifying repository cleanup or custody.
  do_not_use_when:
    - Do not use when generating a new domain-specific profile.
  related_skills:
    - unslop-engine
---

# Unslop Profiles

Do not apply a profile from memory. Pick the profile matching the current task and read the file before applying its avoid/prefer rules.

| Task | Profile file |
|---|---|
| Writing general prose | `profiles/writing.md` |
| Technical documentation | `profiles/technical-writing.md` |
| Implementation plans | `profiles/implementation-plans.md` |
| Code review | `profiles/code-review.md` |
| Worker returns | `profiles/worker-returns.md` |
| Debugging | `profiles/debugging.md` |
| React frontend | `profiles/frontend-react.md` |
| Generic UI | `profiles/frontend-ui.md` |
| API design | `profiles/api-design.md` |
| Architecture | `profiles/architecture.md` |
| Testing | `profiles/testing.md` |
| Security review | `profiles/security-review.md` |
| Repository cleanup | `profiles/cleanup-custody.md` |
```

- [x] **Step 2.3: Write `agents/openai.yaml`**

Create `sources/first_party/skills/unslop-profiles/agents/openai.yaml`:

```yaml
interface:
  display_name: Unslop Profiles
  short_description: Use when applying the right anti-slop profile to a software development workflow.
  default_prompt: Use $unslop-profiles to apply the right anti-slop profile for the current task.
policy:
  allow_implicit_invocation: true
```

- [x] **Step 2.4: Verify profile count and naming**

Run:
```bash
python -c "from pathlib import Path; p=Path('sources/first_party/skills/unslop-profiles/profiles'); assert len(list(p.glob('*.md'))) == 13; print('OK: 13 profiles')"
```
Expected: `OK: 13 profiles`

- [x] **Step 2.5: Commit**

```bash
git add sources/first_party/skills/unslop-profiles
git commit -m "feat(unslop): create unslop-profiles first-party router skill

Move the thirteen portable profiles from unslop-plus and add a read-when router SKILL.md.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
```


---

### Task 3: Reconfigure the `unslop-plus` projection-lane pack in `custody-pack-registry.json`

**Files:**
- Modify: `codex-marketplace/custody-pack-registry.json`

**Interfaces:**
- Consumes: `sources/first_party/skills/unslop-engine/` and `sources/first_party/skills/unslop-profiles/`.
- Produces: registry node that drives `codex-marketplace/plugins/unslop-plus/` projection.

- [x] **Step 3.1: Remove the `unslop` mega-pack mapping**

Edit `codex-marketplace/custody-pack-registry.json` and remove this top-level mapping object:

Old:
```json
    {
      "source_family": "unslop",
      "custody_root": "sources/third_party/unslop/upstream",
      "mega_pack": "unslop-plus",
      "mega_pack_root": "codex-marketplace/plugins/unslop-plus",
      "category": "Productivity",
      "is_mega_pack": true
    },
```

New: nothing.

- [x] **Step 3.2: Add the `unslop-plus` projection-lane pack node**

Immediately after the `house-skills` mega-pack mapping (or in the `packs` array near `repo-worker-pack`), add:

```json
    {
      "bundle_name": "unslop-plus",
      "plugin_root": "codex-marketplace/plugins/unslop-plus",
      "bundle_version": "1.0.0",
      "bundle_type": "projection-lane",
      "category": "Productivity",
      "is_mega_pack": false,
      "notes": [
        "Unslop+ is a first-party projection-lane bundle containing the unslop engine skill and the anti-slop profile router skill.",
        "The bundle replaces the previous unslop mega-pack and keeps the engine separate from the profile router."
      ],
      "source_ledger": [
        "sources/first_party/skills/unslop-engine",
        "sources/first_party/skills/unslop-profiles"
      ],
      "provenance_refs": [
        "provenance/unslop.md",
        "codex-marketplace/plugins/unslop-plus/references/source-map.md"
      ],
      "generated_doc_surfaces": [
        "README.md",
        "SOURCE.md"
      ],
      "entries": [
        {
          "canonical_name": "unslop-engine",
          "source_category": "first_party",
          "content_mode": "verbatim",
          "source_family": "first_party",
          "canonical_source_path": "sources/first_party/skills/unslop-engine",
          "local_path": "skills/unslop-engine",
          "provenance_note": "Projected verbatim from the first-party unslop-engine skill.",
          "copy_expectation": "byte_identical"
        },
        {
          "canonical_name": "unslop-profiles",
          "source_category": "first_party",
          "content_mode": "verbatim",
          "source_family": "first_party",
          "canonical_source_path": "sources/first_party/skills/unslop-profiles",
          "local_path": "skills/unslop-profiles",
          "provenance_note": "Projected verbatim from the first-party unslop-profiles skill.",
          "copy_expectation": "byte_identical"
        }
      ]
    },
```

- [x] **Step 3.3: Replace `unslop-plus` with `unslop-profiles` in `repo-worker-pack` entries**

In `codex-marketplace/custody-pack-registry.json`, inside the `repo-worker-pack` `entries` array, replace the `unslop-plus` entry with `unslop-profiles`.

Old:
```json
        {
          "canonical_name": "unslop-plus",
          "source_category": "first_party",
          "content_mode": "verbatim",
          "source_family": "first_party",
          "canonical_source_path": "sources/first_party/skills/unslop-plus",
          "local_path": "skills/unslop-plus",
          "provenance_note": "Projected verbatim from the first-party unslop-plus skill.",
          "copy_expectation": "byte_identical"
        },
```

New:
```json
        {
          "canonical_name": "unslop-profiles",
          "source_category": "first_party",
          "content_mode": "verbatim",
          "source_family": "first_party",
          "canonical_source_path": "sources/first_party/skills/unslop-profiles",
          "local_path": "skills/unslop-profiles",
          "provenance_note": "Projected verbatim from the first-party unslop-profiles skill.",
          "copy_expectation": "byte_identical"
        },
```

- [x] **Step 3.4: Update `repo-worker-pack` source ledger**

In the `repo-worker-pack` node, replace `sources/first_party/skills/unslop-plus` with `sources/first_party/skills/unslop-profiles` in the `source_ledger` array.

- [x] **Step 3.5: Validate JSON syntax**

Run:
```bash
python -m json.tool codex-marketplace/custody-pack-registry.json > /dev/null
```
Expected: no output, exit 0.

- [x] **Step 3.6: Commit**

```bash
git add codex-marketplace/custody-pack-registry.json
git commit -m "refactor(registry): convert unslop-plus to projection-lane pack and add unslop-profiles to repo-worker-pack

Replace the unslop mega-pack mapping with a projection-lane unslop-plus node containing unslop-engine and unslop-profiles.
Move unslop-profiles into repo-worker-pack for default install.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
```

---

### Task 4: Update `unslop-plus` plugin metadata and generated-doc markers

**Files:**
- Modify: `codex-marketplace/plugins/unslop-plus/.codex-plugin/plugin.json`
- Modify: `codex-marketplace/plugins/unslop-plus/README.md`
- Modify: `codex-marketplace/plugins/unslop-plus/SOURCE.md`

**Interfaces:**
- Consumes: new `unslop-engine` and `unslop-profiles` skill names.
- Produces: plugin root with generated-doc marker pairs and updated plugin manifest.

- [x] **Step 4.1: Rewrite `plugin.json`**

Replace `codex-marketplace/plugins/unslop-plus/.codex-plugin/plugin.json` entirely with:

```json
{
  "name": "unslop-plus",
  "version": "1.0.0",
  "description": "Anti-slop engine and profile router for software development workflows.",
  "author": {
    "name": "Asset Marketplace",
    "url": "https://github.com/HarleyBartles/agent-asset-marketplace"
  },
  "homepage": "https://github.com/HarleyBartles/agent-asset-marketplace",
  "repository": "https://github.com/HarleyBartles/agent-asset-marketplace",
  "license": "MIT",
  "keywords": [
    "skill",
    "unslop-engine",
    "unslop-profiles",
    "profile",
    "validation",
    "code-review",
    "debugging",
    "testing",
    "architecture"
  ],
  "skills": "./skills/",
  "interface": {
    "displayName": "Unslop+",
    "shortDescription": "Anti-slop engine and profile router for software development workflows.",
    "longDescription": "Asset Marketplace-owned unslop-plus package. Use $unslop-engine to generate a domain-specific anti-slop profile, or $unslop-profiles to apply the right existing profile for writing, technical-writing, implementation-plans, code-review, worker-returns, debugging, frontend-react, frontend-ui, api-design, architecture, testing, security-review, or cleanup-custody workflows.",
    "developerName": "Asset Marketplace",
    "category": "Productivity",
    "capabilities": [],
    "websiteURL": "https://github.com/HarleyBartles/agent-asset-marketplace",
    "defaultPrompt": [
      "Use $unslop-profiles to apply the right anti-slop profile for the current workflow, or $unslop-engine to generate a new domain-specific profile."
    ],
    "composerIcon": "./assets/icon.svg",
    "logo": "./assets/icon.svg",
    "screenshots": []
  }
}
```

- [x] **Step 4.2: Rewrite `README.md`**

Replace `codex-marketplace/plugins/unslop-plus/README.md` entirely with:

```markdown
# Unslop+

Anti-slop engine and profile router for software development workflows.

## What's Included
<!-- BEGIN GENERATED: bundle-contents -->
<!-- END GENERATED: bundle-contents -->

## Usage

Use `$unslop-engine` to generate a new domain-specific anti-slop profile from samples, or `$unslop-profiles` to apply the right existing profile for your current task.

## Provenance

- Engine: Adapted from `mshumer/unslop` (MIT license, Copyright (c) 2026 Matt Shumer). The upstream script is a Claude Code CLI tool; the projected `unslop-engine` skill is adapted for Codex/GPT skill use with Python standard library text analysis. See `SOURCE.md` for the adaptation rationale.
- Profiles: First-party portable profiles by Asset Marketplace (MIT license).
- Upstream source custody: `sources/third_party/unslop/upstream/` (retained verbatim).
- First-party profile custody: `sources/first_party/skills/unslop-profiles/profiles/`.
- Upstream MIT notice: `skills/unslop-engine/LICENSE.upstream`.
```

- [x] **Step 4.3: Rewrite `SOURCE.md`**

Replace `codex-marketplace/plugins/unslop-plus/SOURCE.md` entirely with:

```markdown
# Source

This plugin projects a first-party `unslop-engine` skill and a first-party `unslop-profiles` skill.

## Upstream Basis

- Repo: `mshumer/unslop`
- URL: <https://github.com/mshumer/unslop.git>
- Pinned commit: `edcb62386d129c65e4395f0cfcc9168eb1ba2148`
- License: `MIT` (Copyright (c) 2026 Matt Shumer)
- Source custody: `sources/third_party/unslop/upstream/`
- Projection: engine script adapted into `skills/unslop-engine/scripts/unslop.py`

### Why the upstream engine is adapted, not shipped verbatim

The upstream `unslop.py` is a Claude Code CLI tool. It cannot ship verbatim as a Codex/GPT skill package because:

1. **Claude Code CLI dependency**: The upstream script requires the `claude` CLI binary and spawns `claude -p` as a subprocess for sample generation. This runtime assumption is inappropriate for a Codex/GPT skill package.
2. **Interactive TerminalUI**: The upstream script includes an interactive terminal UI with spinners, progress bars, TTY detection, ANSI color codes, and live-updating display. These are not appropriate for a non-interactive skill package.
3. **Process signal handling**: The upstream uses `signal`, `os`, and `time` modules for subprocess management and timeout handling tied to the Claude Code CLI process model.
4. **Claude Code permission denial handling**: The upstream includes Claude Code-specific permission denial detection and error messages.

The projected `unslop-engine` skill adapts the upstream idea (sample collection, pattern detection, profile generation) to use Python standard library text analysis, local sample files, and optional Playwright for visual evidence. The upstream MIT license and copyright are preserved in `skills/unslop-engine/LICENSE.upstream`.

## First-Party Source Custody
<!-- BEGIN GENERATED: pack-inventory -->
<!-- END GENERATED: pack-inventory -->

## Marketplace Composition

- The `unslop-plus` plugin root projects `unslop-engine` and `unslop-profiles` first-party skills.
- The `unslop-engine` skill is an adaptation of the upstream `mshumer/unslop` idea; the `unslop-profiles` skill is a first-party read-when router.
- Each profile is portable across repos with no Asset Marketplace-specific nouns.
- Provenance distinguishes third-party engine adaptation from first-party profile authorship.
- Upstream MIT license preserved at `skills/unslop-engine/LICENSE.upstream`.
- Plugin-level MIT license at `LICENSE` covers first-party profile and adaptation work.
```

- [x] **Step 4.4: Commit**

```bash
git add codex-marketplace/plugins/unslop-plus/.codex-plugin/plugin.json codex-marketplace/plugins/unslop-plus/README.md codex-marketplace/plugins/unslop-plus/SOURCE.md
git commit -m "docs(unslop-plus): update plugin manifest, README, and SOURCE for split

Reference $unslop-engine and $unslop-profiles. Add generated doc markers for bundle contents and pack inventory.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
```


---

### Task 5: Update doctrine and provenance docs

**Files:**
- Modify: `docs/custody-and-projection-doctrine.md`
- Modify: `provenance/unslop.md`

**Interfaces:**
- Consumes: new `unslop-plus` projection-lane pack shape and new `unslop-engine`/`unslop-profiles` source paths.
- Produces: accurate doctrine and provenance records.

- [x] **Step 5.1: Update `docs/custody-and-projection-doctrine.md`**

Edit `docs/custody-and-projection-doctrine.md`. Change:

Old:
```markdown
Six maintained mega-packs carry the remaining broad custody-root bundles. The
editable pack registry in `codex-marketplace/custody-pack-registry.json`
declares both projection-lane pack nodes and mega-pack nodes; mega-pack nodes
set `is_mega_pack: true`, while the registry as a whole decides which plugin
roots are actively projected:
```

New:
```markdown
Five maintained mega-packs carry the remaining broad custody-root bundles. The
editable pack registry in `codex-marketplace/custody-pack-registry.json`
declares both projection-lane pack nodes and mega-pack nodes; mega-pack nodes
set `is_mega_pack: true`, while the registry as a whole decides which plugin
roots are actively projected:
```

Then remove the `unslop-plus` mega-pack bullet:

Old:
```markdown
- **`unslop-plus`** — unslop source family mega-pack.
```

New: nothing.

- [x] **Step 5.2: Update `provenance/unslop.md`**

Edit `provenance/unslop.md` and make these replacements:

Old:
```markdown
MARK-99 adds an Asset Marketplace-owned `unslop` GPT/Codex package at `codex-marketplace/plugins/unslop/`.
```
New:
```markdown
MARK-99 adds an Asset Marketplace-owned `unslop-plus` GPT/Codex package at `codex-marketplace/plugins/unslop-plus/`.
```

Old:
```markdown
- **Marketplace package**: `codex-marketplace/plugins/unslop/`
```
New:
```markdown
- **Marketplace package**: `codex-marketplace/plugins/unslop-plus/`
```

Old:
```markdown
- **GPT skill install path**: `codex-marketplace/plugins/unslop/skills/unslop/`
- **Codex plugin install path**: `codex-marketplace/plugins/unslop/.codex-plugin/plugin.json`
```
New:
```markdown
- **GPT skill install paths**: `codex-marketplace/plugins/unslop-plus/skills/unslop-engine/` and `codex-marketplace/plugins/unslop-plus/skills/unslop-profiles/`
- **Codex plugin install path**: `codex-marketplace/plugins/unslop-plus/.codex-plugin/plugin.json`
```

Old:
```markdown
- **Plugin name**: `unslop`
- **Display name**: `Unslop`
```
New:
```markdown
- **Plugin name**: `unslop-plus`
- **Display name**: `Unslop+`
```

Old:
```markdown
- **Content mode**: Mixed `adapted` (main skill) and `verbatim` (profiles)
```
New:
```markdown
- **Content mode**: `verbatim` (first-party `unslop-engine` and `unslop-profiles` skills); upstream engine concept is adapted into `unslop-engine`
```

- [x] **Step 5.3: Commit**

```bash
git add docs/custody-and-projection-doctrine.md provenance/unslop.md
git commit -m "docs(unslop): update doctrine and provenance for unslop-plus split

Remove unslop-plus from mega-pack list and update provenance paths to unslop-plus plugin and unslop-engine/unslop-profiles skills.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
```

---

### Task 6: Retire `unslop-plus` source skill and stale artifacts

**Files:**
- Delete: `sources/first_party/skills/unslop-plus/` (after migration)
- Delete: `generated/skill-zips/unslop-plus.zip` (after rebuild)

**Interfaces:**
- Consumes: completed Tasks 1–5.
- Produces: clean source tree with no stale `unslop-plus` skill or zip artifacts.

- [x] **Step 6.1: Verify all assets are migrated**

Run:
```bash
Test-Path "sources/first_party/skills/unslop-engine/scripts/unslop.py"
Test-Path "sources/first_party/skills/unslop-engine/scripts/validate_unslop_output.py"
Test-Path "sources/first_party/skills/unslop-engine/scripts/validate_package.py"
Test-Path "sources/first_party/skills/unslop-engine/references/upstream-provenance.md"
Test-Path "sources/first_party/skills/unslop-engine/LICENSE.upstream"
Test-Path "sources/first_party/skills/unslop-profiles/profiles/writing.md"
```
Expected: all return `True`.

- [x] **Step 6.2: Delete the retired source directory**

Run:
```bash
Remove-Item -Recurse -Force sources/first_party/skills/unslop-plus
```

- [x] **Step 6.3: Delete the stale skill zip**

Run:
```bash
Remove-Item -Force generated/skill-zips/unslop-plus.zip
```

- [x] **Step 6.4: Commit**

```bash
git add -A
git commit -m "chore(unslop): retire unslop-plus source skill and stale zip

Delete sources/first_party/skills/unslop-plus/ and generated/skill-zips/unslop-plus.zip after migrating assets to unslop-engine and unslop-profiles.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
```

---

### Task 7: Regenerate marketplace and validate

**Files:**
- Regenerate: `codex-marketplace/plugins/unslop-plus/references/bundle-manifest.json`
- Regenerate: `codex-marketplace/plugins/unslop-plus/skills/`
- Regenerate: `codex-marketplace/plugins/repo-worker-pack/`
- Regenerate: `codex-marketplace/plugins/house-skills/`
- Regenerate: `.agents/plugins/marketplace.json`, `codex-marketplace/manifest.json`
- Regenerate: `generated/skill-zips/unslop-engine.zip`, `generated/skill-zips/unslop-profiles.zip`
- Regenerate: `repo-index/repo-index.json`

**Interfaces:**
- Consumes: all source, registry, and plugin manual edits from Tasks 1–6.
- Produces: a consistent, validated marketplace projection.

- [x] **Step 7.1: Rebuild the marketplace**

Run:
```bash
py -3 tools/rebuild_marketplace.py
```
Expected: completes without errors.

- [x] **Step 7.2: Run the CI check**

Run:
```bash
py -3 tools/check_marketplace.py
```
Expected: `Marketplace validation passed.`

- [x] **Step 7.3: Run targeted validators**

Run:
```bash
py -3 tools/validate_marketplace.py --skip-freshness-checks
py -3 tools/install_agent_skills.py --check
```
Expected: both pass.

- [x] **Step 7.4: Manual projection checks**

Run:
```bash
Test-Path "codex-marketplace/plugins/unslop-plus/skills/unslop-engine/SKILL.md"
Test-Path "codex-marketplace/plugins/unslop-plus/skills/unslop-profiles/SKILL.md"
Test-Path "codex-marketplace/plugins/repo-worker-pack/skills/unslop-profiles/SKILL.md"
Test-Path "codex-marketplace/plugins/house-skills/skills/unslop-engine/SKILL.md"
Test-Path "codex-marketplace/plugins/house-skills/skills/unslop-profiles/SKILL.md"
Test-Path "generated/skill-zips/unslop-engine.zip"
Test-Path "generated/skill-zips/unslop-profiles.zip"
```
Expected: all return `True`.

Run:
```bash
Test-Path "generated/skill-zips/unslop-plus.zip"
```
Expected: `False`.

- [x] **Step 7.5: Check `unslop-profiles/SKILL.md` instructs file reads**

Run:
```bash
Select-String -Path "codex-marketplace/plugins/unslop-plus/skills/unslop-profiles/SKILL.md" -Pattern "profiles/\w+\.md" | Select-Object -First 5
```
Expected: lines matching `profiles/<name>.md` are present in the body.

- [x] **Step 7.6: Commit regenerated surfaces**

```bash
git add -A
git commit -m "regenerate(unslop): project unslop-engine and unslop-profiles into marketplace

Run rebuild_marketplace.py and check_marketplace.py. Update unslop-plus plugin, repo-worker-pack, house-skills, marketplace manifests, skill zips, and repo index.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
```

---

## Plan review

- **Spec coverage:** Every section of the design spec has a corresponding task.
- **Placeholder scan:** No `TBD`, `TODO`, or vague steps remain.
- **Interim state:** Between Task 6 and Task 7 the marketplace will fail validation because `unslop-plus` source is gone but projections are stale. This is expected and fixed by Task 7.
- **Task independence:** Tasks 1 and 2 are fully independent. Tasks 3–6 are sequential. Task 7 depends on all preceding tasks.
- **Execution confidence:** **9/10**. All file targets, exact contents, registry edits, and validation commands are specified. The only runtime uncertainty is the exact text of `validate_package.py` forbidden-fragment checks, which are already defined.


