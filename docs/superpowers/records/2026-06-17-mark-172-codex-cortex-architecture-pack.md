# MARK-172 Codex Cortex / Architecture Pack Implementation Record

**Issue:** MARK-172
**Branch:** `codex/mark-172-codex-cortex-architecture-pack`
**Starting main SHA:** `116120743d0060e58c88758a740ec58a63202ed2`
**Implementation commit SHA:** `e6049ce729c7971e5e600f47df5dc1d349abb8fd`
**PR URL:** [https://github.com/HarleyBartles/agent-asset-marketplace/pull/108](https://github.com/HarleyBartles/agent-asset-marketplace/pull/108)
**Publication state:** Published on branch `codex/mark-172-codex-cortex-architecture-pack` and tracked by PR #108 against `main`. This record documents the two-surface MARK-172 delivery: the `codex-cortex` custody plugin as the canonical imported home for `cqrs-event-sourcing`, and the `architecture-pack` projection plugin that installs the same seed for architecture guidance.

## Files changed

- `docs/superpowers/plans/2026-06-17-mark-172-codex-cortex-architecture-pack.md`
- `docs/superpowers/records/2026-06-17-mark-172-codex-cortex-architecture-pack.md`
- `codex-marketplace/plugin-roots.json`
- `codex-marketplace/manifest.json`
- `.agents/plugins/marketplace.json`
- `codex-marketplace/README.md`
- `codex-marketplace/plugins/README.md`
- `codex-marketplace/plugins/AGENTS.md`
- `README.md`
- `sources/README.md`
- `sources/third_party/README.md`
- `provenance/codex-cortex.md`
- `sources/first_party/skills/codex-cortex/intake.json`
- `sources/first_party/skills/codex-cortex/decisions.json`
- `sources/first_party/skills/codex-cortex/decisions.md`
- `sources/third_party/codex-cortex/upstream/README.md`
- `sources/third_party/codex-cortex/upstream/LICENSE`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/SKILL.md`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/cqrs-patterns.md`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/event-sourcing.md`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/event-store-tech.md`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/consistency-patterns.md`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/best-practices.md`
- `codex-marketplace/plugins/codex-cortex/.codex-plugin/plugin.json`
- `codex-marketplace/plugins/codex-cortex/README.md`
- `codex-marketplace/plugins/codex-cortex/SOURCE.md`
- `codex-marketplace/plugins/codex-cortex/LICENSE`
- `codex-marketplace/plugins/codex-cortex/assets/icon.svg`
- `codex-marketplace/plugins/codex-cortex/references/bundle-manifest.json`
- `codex-marketplace/plugins/codex-cortex/references/source-map.md`
- `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/SKILL.md`
- `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/references/cqrs-patterns.md`
- `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/references/event-sourcing.md`
- `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/references/event-store-tech.md`
- `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/references/consistency-patterns.md`
- `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/references/best-practices.md`
- `codex-marketplace/plugins/architecture-pack/.codex-plugin/plugin.json`
- `codex-marketplace/plugins/architecture-pack/README.md`
- `codex-marketplace/plugins/architecture-pack/SOURCE.md`
- `codex-marketplace/plugins/architecture-pack/LICENSE`
- `codex-marketplace/plugins/architecture-pack/assets/icon.svg`
- `codex-marketplace/plugins/architecture-pack/references/bundle-manifest.json`
- `codex-marketplace/plugins/architecture-pack/references/source-map.md`
- `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/SKILL.md`
- `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/references/cqrs-patterns.md`
- `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/references/event-sourcing.md`
- `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/references/event-store-tech.md`
- `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/references/consistency-patterns.md`
- `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/references/best-practices.md`
- `generated/skill-zips/codex-cortex/cqrs-event-sourcing/skill.zip`
- `generated/skill-zips/architecture-pack/cqrs-event-sourcing/skill.zip`
- `generated/skill-zips/registry.json`
- `repo-index/repo-index.json`
- `tools/generate_repo_index.py`
- `tools/skill_zip_artifacts.py`
- `tools/skill_gpt_exports.py`
- `tools/validate_generated_drift.py`
- `tools/validate_marketplace.py`
- `tools/README.md`
- `tools/package_skill_zips.py`
- `codex-marketplace/plugins/house-skills/skills/skill-packager/scripts/safe_skill_tree.py`
- `codex-marketplace/plugins/house-skills/skills/skill-packager/scripts/package_skill.py`
- `codex-marketplace/plugins/house-skills/skills/skill-packager/scripts/package_and_verify_skill.py`

## Scope and boundary

- Included: `codex-cortex` custody plugin, `architecture-pack` projection plugin, deterministic generated zips, and marketplace/repo-index registration.
- Excluded from this child: later Claude-Cortex candidates and broader architecture taxonomy.
- The custody surface is the canonical home for the imported seed; the projection surface is installable separately.

## Authorship, license, and provenance

- The upstream technical guidance remains attributed to `NickCrew/Claude-Cortex` and is retained in `sources/third_party/codex-cortex/upstream/` under the upstream MIT license.
- The `codex-cortex` plugin is the retained custody home for the imported seed skill and records the intake/decision ledger in `sources/first_party/skills/codex-cortex/`.
- The `architecture-pack` plugin is a downstream installable projection from the `codex-cortex` custody plugin.
- `provenance/codex-cortex.md` carries the upstream intake and custody record.
- `codex-marketplace/plugins/codex-cortex/references/source-map.md` and `codex-marketplace/plugins/architecture-pack/references/source-map.md` separate custody from projection.

## Generated-artifact alignment

The canonical regeneration lane was used to rebuild the generated skill-zips after the packaging writer was normalized for LF/CRLF stability and deterministic metadata.

Changed zip paths from the canonical regeneration:

- `generated/skill-zips/codex-cortex/cqrs-event-sourcing/skill.zip`
- `generated/skill-zips/architecture-pack/cqrs-event-sourcing/skill.zip`

## Validation

- `py -3 tools/generate_marketplace.py`
  - Result: passed; wrote `.agents/plugins/marketplace.json` and `codex-marketplace/manifest.json`.
- `py -3 tools/generate_repo_index.py`
  - Result: passed after adding `codex-cortex` support.
- `py -3 tools/update_skill_artifacts.py --all`
  - Result: passed; regenerated the canonical zip corpus and registry, including `codex-cortex` and `architecture-pack`.
- `py -3 tools/validate_marketplace.py`
  - Result: passed.
- `py -3 tools/validate_repo_index.py`
  - Result: passed.
- `py -3 tools/validate_skill_zips.py`
  - Result: passed.
- `py -3 tools/validate_generated_drift.py --base origin/main`
  - Result: passed.
- `git diff --check`
  - Result: passed, with standard line-ending warnings only.

## Skipped checks

- None. The final state was fully validated before publication.

## Deviations

- The repo-index generator needed a codex-cortex synthesis entry before it could regenerate cleanly.
- The implementation is intentionally split across custody and projection plugins so the installable architecture surface stays separate from the upstream-derived custody home.
