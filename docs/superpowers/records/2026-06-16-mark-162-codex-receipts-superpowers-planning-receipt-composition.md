# MARK-162 Codex Receipts Superpowers Implementation Record

**Issue:** MARK-162
**Branch:** `codex/mark-162-add-codex-receipts-superpowers-planning-receipt-composition`
**Starting main SHA:** `6b71b02d5cdae2873f7c2c141295c90ca0bf5699`
**Implementation SHA:** `10847ae4b89c224d5e09f5dd8413723c9ac59f43`
**Final head SHA:** `c28cfa88d6085325a11c7e5df788e5cbf0e92b6e`
**PR URL:** [https://github.com/HarleyBartles/agent-asset-marketplace/pull/101](https://github.com/HarleyBartles/agent-asset-marketplace/pull/101)
**Publication state:** Published on branch `codex/mark-162-add-codex-receipts-superpowers-planning-receipt-composition` and tracked by PR #101 against `main`. The record commit is the current branch head. Final PR head at publication/review is verified from GitHub PR state; later PR tip movement is publication evidence, not a reason to rewrite this record.

## Changed files

- `codex-marketplace/plugins/house-skills/README.md`
- `codex-marketplace/plugins/house-skills/skills/codex-receipts-superpowers/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/codex-receipts-superpowers/agents/openai.yaml`
- `codex-marketplace/plugins/house-skills/skills/house-skills/references/bundle-manifest.json`
- `codex-marketplace/plugins/house-skills/skills/house-skills/references/source-map.md`
- `codex-marketplace/plugins/superpowers/PROJECTION.md`
- `codex-marketplace/plugins/superpowers/SOURCE.md`
- `codex-marketplace/plugins/superpowers/references/bundle-manifest.json`
- `codex-marketplace/plugins/superpowers/references/codex-marketplace-compatibility.md`
- `codex-marketplace/plugins/superpowers/references/provenance-map.json`
- `codex-marketplace/plugins/superpowers/skills/codex-receipts-superpowers/SKILL.md`
- `codex-marketplace/plugins/superpowers/skills/codex-receipts-superpowers/agents/openai.yaml`
- `docs/superpowers/plans/2026-06-16-mark-162-codex-receipts-superpowers-planning-receipt-composition.md`
- `generated/skill-zips/adventures-pack/base-doctrine/skill.zip`
- `generated/skill-zips/house-skills/base-doctrine/skill.zip`
- `generated/skill-zips/house-skills/bootstrap-router/skill.zip`
- `generated/skill-zips/house-skills/codex-receipts-superpowers/skill.zip`
- `generated/skill-zips/house-skills/house-skills/skill.zip`
- `generated/skill-zips/house-skills/rooms-analogy-buster/skill.zip`
- `generated/skill-zips/house-skills/rooms-character-investigation/skill.zip`
- `generated/skill-zips/house-skills/rooms-project-doctrine/skill.zip`
- `generated/skill-zips/house-skills/work-mode-router/skill.zip`
- `generated/skill-zips/registry.json`
- `generated/skill-zips/superpowers/codex-receipts-superpowers/skill.zip`
- `gpt-overlays/manifest.json`
- `provenance/house-skills.md`
- `provenance/superpowers.md`
- `sources/first_party/skills/house-skills/decisions.json`
- `sources/first_party/skills/house-skills/decisions.md`
- `sources/first_party/skills/house-skills/intake.json`
- `tools/validate_marketplace.py`

## What changed

- Added the canonical House Skills wrapper `codex-receipts-superpowers`.
- Projected the wrapper into the `superpowers` bundle without forking third-party skill source.
- Updated the House Skills inventory, source map, and provenance notes.
- Updated `superpowers` source/projection docs and compatibility/provenance metadata.
- Extended the GPT export manifest so the new skill is classified as a direct export in both `house-skills` and `superpowers`.
- Regenerated the skill zip corpus and registry.
- Extended marketplace validation to permit the new first-party projection.

## Validation

- `py -3 tools/update_skill_artifacts.py --all`
- `py -3 tools/validate_marketplace.py`
- `py -3 tools/validate_repo_index.py`
- `git diff --check`

## Latest checks

- `py -3 tools/validate_marketplace.py`
- `py -3 tools/validate_repo_index.py`
- `git diff --check`

## Notes

- The export generator initially failed because `gpt-overlays/manifest.json` did not classify `superpowers/codex-receipts-superpowers`; adding the direct export classification resolved it.
- The marketplace validator then failed because `tools/validate_marketplace.py` still limited first-party `superpowers` projections to the older wrapper set; adding `codex-receipts-superpowers` to the allowlist resolved it.
- The generator also refreshed several unrelated existing `skill.zip` artifacts and `generated/skill-zips/registry.json`.
- No additional GPT overlay file was needed beyond the manifest classification updates.
- This record captures the implementation SHA separately from the record/receipt SHA so later PR head movement does not require endless record rewrites.
