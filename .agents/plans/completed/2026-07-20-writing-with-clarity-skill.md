# Writing With Clarity Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a first-party `writing-with-clarity` skill to `repo-worker-pack` for all human-facing prose, with selective short references and a bundled, reference-only copy of the complete 1918 source text.

**Architecture:** Author the skill under `sources/first_party/skills/writing-with-clarity/` with a small routing `SKILL.md`, task-oriented references, and `references/source/elements-of-style-1918.html`. Add one first-party entry to the `repo-worker-pack` projection-lane registry, then use the canonical rebuild pipeline to generate the plugin projection, manifests, maps, indexes, and GPT zip. The adapted references are operational authority; the historical source is a cold fallback for unresolved context only.

**Tech Stack:** Markdown, JSON, Python marketplace generators/validators, pytest, Git.

## Global Constraints

- Edit first-party skill content only under `sources/first_party/skills/` and edit pack membership only in `codex-marketplace/custody-pack-registry.json`.
- Do not hand-edit projected plugin trees, bundle manifests, source maps, provenance maps, indexes, or skill zips.
- The skill applies to all human-facing prose, but must not invent repository facts or override user/project style requirements.
- `references/source/elements-of-style-1918.html` is bundled but must not be read during ordinary use; read only the relevant source section when a short reference cannot resolve context.
- The adapted first-party references outrank the historical source for operational guidance; the source provides context and provenance only.
- Validate with `py -3 tools/rebuild_marketplace.py`, `py -3 tools/check_marketplace.py`, focused tests, and `git diff --check`.

## File Map

- Create `sources/first_party/skills/writing-with-clarity/SKILL.md` as the compact control-plane router.
- Create `sources/first_party/skills/writing-with-clarity/references/routing.md` for artifact/problem-to-reference selection.
- Create `sources/first_party/skills/writing-with-clarity/references/sentence-mechanics.md` for sentence-level grammar and punctuation.
- Create `sources/first_party/skills/writing-with-clarity/references/composition-and-flow.md` for paragraphs, sequencing, and related ideas.
- Create `sources/first_party/skills/writing-with-clarity/references/clarity-and-concision.md` for direct, concrete, economical prose.
- Create `sources/first_party/skills/writing-with-clarity/references/usage-and-word-choice.md` for ambiguity, misused terms, and inflated wording.
- Create `sources/first_party/skills/writing-with-clarity/references/format-and-markup.md` for human-facing Markdown, UI, errors, and structured prose.
- Create `sources/first_party/skills/writing-with-clarity/references/final-edit.md` for the final review pass.
- Create `sources/first_party/skills/writing-with-clarity/references/source/source-map.md` for stable mappings to the original text.
- Create `sources/first_party/skills/writing-with-clarity/references/source/elements-of-style-1918.html` as the complete public-domain historical source, marked reference-only by the source map and router.
- Modify `codex-marketplace/custody-pack-registry.json` to add the first-party `writing-with-clarity` entry to `repo-worker-pack`.
- Create `tests/test_writing_with_clarity_contract.py` for source, routing, cold-source, and registry contracts.
- Regenerate all derived marketplace surfaces with `py -3 tools/rebuild_marketplace.py`.

## Task 1: Add the RED contract

**Files:** Create `tests/test_writing_with_clarity_contract.py`.

- [x] Add tests that fail before authoring because the source skill directory and registry entry do not exist.
- [x] Assert the source skill has `SKILL.md`, all six short references, the source map, and the complete source reference.
- [x] Assert `SKILL.md` names all human-facing prose triggers, routes to `references/routing.md`, and contains an explicit prohibition on routine loading of the full 1918 source.
- [x] Assert the source map and short references preserve the source-section mapping and precedence rule.
- [x] Assert the registry contains one `first_party`/`verbatim` entry with directory-level canonical and local paths.
- [x] Run `py -3 -m pytest tests/test_writing_with_clarity_contract.py -q` and confirm the expected missing-source failure.

## Task 2: Author the skill and bundled source

**Files:** Create the source skill files listed in the File Map.

- [x] Write frontmatter with `name: writing-with-clarity` and a trigger-only description beginning with `Use when`.
- [x] Keep `SKILL.md` compact: human-facing prose scope, source-truth boundary, classify artifact and writing problem, load one primary and at most one secondary short reference, then use `final-edit.md` when revising.
- [x] Make `routing.md` map README/docs/report/explanation/UI/error/commit/PR prose and editing tasks to the smallest relevant references.
- [x] Write the five topical references with actionable rules, modern examples, exceptions, and source-basis pointers; frame active voice, positive form, and concision as heuristics rather than unconditional laws.
- [x] Write `final-edit.md` as a bounded checklist that preserves meaning, audience, accuracy, and project conventions.
- [x] Add `source-map.md` mappings for Rules 1-7, Rules 8-9 and 14-18, Rules 10-13, Chapter V, and Chapters IV/VI.
- [x] Vendor the complete 1918 text in the HTML source reference with the warning held in `source-map.md` and `SKILL.md`; preserve the source heading structure so agents can inspect a targeted section.
- [x] Run the focused contract test and `git diff --check`.

## Task 3: Register and regenerate the repo-worker-pack projection

**Files:** Modify `codex-marketplace/custody-pack-registry.json`; regenerate tool-owned surfaces.

- [x] Add the registry entry with `canonical_name: writing-with-clarity`, `source_category: first_party`, `content_mode: verbatim`, `source_family: first_party`, `canonical_source_path: sources/first_party/skills/writing-with-clarity`, `local_path: skills/writing-with-clarity`, and a provenance note naming the first-party source.
- [x] Run `py -3 tools/rebuild_marketplace.py`.
- [x] Confirm generated `repo-worker-pack` and `house-skills` projections contain the source skill and bundled historical reference; do not hand-edit either projection.
- [x] Run `py -3 tools/check_marketplace.py` after commit, plus `py -3 tools/generate_marketplace.py --check`, `py -3 tools/generate_repo_index.py --check`, `py -3 tools/generate_pack_manifests.py --check`, `py -3 tools/materialize_projection.py --check`, `py -3 tools/generate_index_mesh.py --check`, and `py -3 tools/validate_generated_drift.py --base origin/main`. The first clean-tree run exposed six stale indexes; the canonical index generator refreshed them, after which the validator passed.
- [x] Run `py -3 -m pytest tests/test_writing_with_clarity_contract.py tests/test_validate_marketplace.py tests/test_generator_check_modes.py -q` and `git diff --check`.

## Task 4: Verify pressure behavior and publish

**Files:** Update the plan checkboxes and any source wording needed by verification; no new runtime code.

- [x] Run a guided fresh-context pressure check against representative README, UI/error, and editing prompts using the new skill as the guidance surface.
- [x] Confirm the guided agents select short references first and do not load the full source by default; three completed guided checks were counted, while one later timed-out check was not counted.
- [x] Review the generated diff for scope, licensing/provenance, source/projection separation, and accidental full-source duplication outside the intended skill package.
- [x] Commit the source, registry, tests, plan, and generated surfaces with `feat: add writing with clarity skill`.
- [x] Push the feature branch and open PR #203 into `main`, then verify the published branch head matches the local commit.

## Interim States

- After Task 1, the focused contract is intentionally RED because the source skill and registry entry do not yet exist.
- After Task 2, the source is complete but marketplace projections are intentionally stale until Task 3.
- Completion is not GREEN until the generated surfaces and the published PR head are verified.

## Plan Self-Review

- Source custody, pack membership, generated projections, validation, and publication are covered.
- The historical source is explicitly bounded and cannot silently become the default reference.
- No implementation code or generator changes are required.

**SDD confidence: 8.5/10.** The source path, projection-lane registry shape, rebuild command, and validation stack were verified against the live checkout. Remaining uncertainty is limited to the generated file set, which the canonical rebuild and check commands own.

## Review follow-up: source, routing, and generated documentation

- [x] Remove `final-edit.md` from topical primary/secondary routing and state that it is a separate bounded pass.
- [x] Record the upstream repository, immutable revision, retrieval URL, normalized hash, and public-domain basis for the vendored 1918 source.
- [x] Extend the contract tests to cover projection/installed byte identity and generated pack-document exposure.
- [x] Make manifest-declared README, SOURCE, and PROJECTION inventory blocks generator-owned while retaining authored explanatory prose.
- [x] Repair the repo-worker-pack registry ledger, provenance note, and generator guidance for the stale inventory surfaces.
- [x] Regenerate and validate all affected projections, indexes, maps, manifests, and packages.
- [ ] Obtain a fresh-eyes review of the repaired head, then merge and update the main checkout only after exact-head CI is green.
