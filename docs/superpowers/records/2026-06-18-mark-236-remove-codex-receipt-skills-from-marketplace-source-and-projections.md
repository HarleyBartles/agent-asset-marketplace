# MARK-236 Remove Codex Receipt Skills From Marketplace Source and Projections

Issue: MARK-236
Branch: `harleydbartles/mark-236-remove-codex-receipt-skills-from-marketplace-source-and`
PR: https://github.com/HarleyBartles/agent-asset-marketplace/pull/126

## Outcome

Removed `codex-repo-receipts` and `codex-receipts-superpowers` from marketplace source, projected install surfaces, generated skill zips, and validator allowlists. Also backfilled the plan ledger by marking completed historical tasks as done and deleting the prior implementation record corpus.

## Changed surfaces

- Removed the two skill roots from `sources/first_party/`.
- Removed the two skill roots from `codex-marketplace/plugins/house-skills/` and the `codex-repo-receipts` projection from `codex-marketplace/plugins/repo-worker-base/`.
- Updated `codex-marketplace/plugins/house-skills/README.md`, `codex-marketplace/plugins/house-skills/skills/house-skills/SKILL.md`, and `codex-marketplace/plugins/house-skills/skills/house-skills/references/{bundle-manifest.json,source-map.md}`.
- Updated `codex-marketplace/plugins/repo-worker-base/{README.md,SOURCE.md,references/source-map.md}`.
- Updated `provenance/{house-skills.md,repo-worker-base.md,superpowers.md}`.
- Updated `generated/skill-zips/registry.json` and removed the generated zip entries for the deleted skills.
- Updated `tools/validate_marketplace.py` and `tests/test_validate_marketplace.py`.
- Backfilled `docs/superpowers/plans/*.md` so completed tasks now use `[x]`, including this issue plan.

## Generated artifacts

- Regenerated the skill artifact corpus with `py -3 tools/update_skill_artifacts.py --all`.
- The deleted skill zips were removed from `generated/skill-zips/`.
- The remaining generated `house-skills` zip was refreshed as part of the full corpus regeneration.

## Validation

- `py -3 tools/update_skill_artifacts.py --all`
- `py -3 tools/validate_marketplace.py`
- `py -3 tools/validate_generated_drift.py --base origin/main`
- `git diff --check`

Result:
- Marketplace validation passed.
- Generated drift validation passed.
- `git diff --check` returned clean, with only Git line-ending warnings in the working copy.

## Notes

- The repository no longer contains the old implementation-record files under `docs/superpowers/records/`.
- Historical plan files were updated to reflect completed work; unfinished future work, if any, remains visible in the active plan file.
