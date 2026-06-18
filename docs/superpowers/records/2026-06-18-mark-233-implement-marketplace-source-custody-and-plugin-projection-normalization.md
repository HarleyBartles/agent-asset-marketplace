# MARK-233 Marketplace Source Custody and Plugin Projection Normalization Implementation Record

**Issue:** MARK-233
**Branch:** `harleydbartles/mark-233-implement-marketplace-source-custody-and-plugin-projection-normalization`
**Starting main SHA:** `1da78655b12cc0d1e70e91b184893021295ea763`
**Implementation commit SHA:** pending
**PR URL:** pending
**Publication state:** This record captures the MARK-233 custody move that relocates the shared first-party marketplace core skills into `sources/first_party/core/`, the matching projection/path normalization across the marketplace surfaces, and the Superpowers source/projection byte-alignment needed to keep the bundle validators clean. The branch is not yet published in GitHub at the time of this record draft.

## Files changed

Representative repo surfaces changed for this issue:

- `sources/first_party/core/connector-safety/`
- `sources/first_party/core/github-operations/`
- `sources/first_party/core/codex-repo-receipts/`
- `sources/first_party/core/boring-loop/`
- `sources/first_party/core/linear-superpowers/`
- `sources/first_party/core/cleanup-custody/`
- `sources/first_party/core/skill-packager/`
- `sources/first_party/core/skill-validator/`
- `sources/first_party/core/skill-installer/`
- `sources/first_party/core/bootstrap-router/`
- `sources/first_party/core/README.md`
- `sources/README.md`
- `sources/first_party/README.md`
- `codex-marketplace/plugins/house-skills/SOURCE.md`
- `codex-marketplace/plugins/house-skills/skills/house-skills/references/bundle-manifest.json`
- `codex-marketplace/plugins/house-skills/skills/house-skills/references/source-map.md`
- `codex-marketplace/plugins/repo-worker-base/SOURCE.md`
- `codex-marketplace/plugins/repo-worker-base/references/source-map.md`
- `codex-marketplace/plugins/superpowers/SOURCE.md`
- `codex-marketplace/plugins/superpowers/PROJECTION.md`
- `codex-marketplace/plugins/superpowers/references/bundle-manifest.json`
- `codex-marketplace/plugins/superpowers/references/provenance-map.json`
- `codex-marketplace/plugins/superpowers/skills/linear-superpowers/SKILL.md`
- `provenance/house-skills.md`
- `provenance/repo-worker-base.md`
- `provenance/superpowers.md`
- `repo-index/repo-index.json`
- `tools/validate_marketplace.py`
- `generated/skill-zips/registry.json`
- `generated/skill-zips/house-skills/connector-safety/skill.zip`
- `generated/skill-zips/house-skills/github-operations/skill.zip`
- `generated/skill-zips/house-skills/boring-loop/skill.zip`
- `generated/skill-zips/house-skills/cleanup-custody/skill.zip`
- `generated/skill-zips/house-skills/linear-superpowers/skill.zip`
- `generated/skill-zips/house-skills/skill-packager/skill.zip`
- `generated/skill-zips/house-skills/skill-validator/skill.zip`
- `generated/skill-zips/repo-worker-base/connector-safety/skill.zip`
- `generated/skill-zips/repo-worker-base/github-operations/skill.zip`
- `generated/skill-zips/repo-worker-base/boring-loop/skill.zip`
- `generated/skill-zips/superpowers/linear-superpowers/skill.zip`
- `docs/superpowers/plans/2026-06-18-mark-233-implement-marketplace-source-custody-and-plugin-projection-normalization.md`
- `docs/superpowers/records/2026-06-18-mark-233-implement-marketplace-source-custody-and-plugin-projection-normalization.md`

## Scope and boundary

- Included: moving the shared first-party core skills into `sources/first_party/core/`, updating the marketplace source/projection references that point at those roots, refreshing the generated skill-zips corpus, and normalizing the Superpowers retained snapshot so byte-sensitive bundle validation passes.
- Included as validation repair: aligning `sources/third_party/superpowers/obra-superpowers/v5.1.0/.codex-plugin/plugin.json` and the mirrored Superpowers skill files to the active projection bytes so `validate_marketplace.py` could complete.
- Excluded: any repo-wide cleanup beyond the exact custody and projection paths needed for MARK-233.

## Generated artifact alignment

This issue required regenerating the skill-zip corpus after the source custody move and projection normalization.

The regeneration step used:

- `py -3 tools/update_skill_artifacts.py --all`

That refreshed the derived export surface, including `generated/skill-zips/registry.json` and the affected `skill.zip` outputs for the moved core skills.

This is a derived export surface, not canonical source.

## Validation

- `py -3 tools/validate_marketplace.py`
  - Result: passed.
- `py -3 tools/validate_repo_index.py`
  - Result: passed.
- `py -3 tools/validate_generated_drift.py --base origin/main`
  - Result: passed.
- `git diff --check`
  - Result: passed with line-ending warnings only.

## Notes

- The implementation record intentionally separates the MARK-233 slice from any unrelated repo drift.
- The final publication metadata will be filled in after the branch is committed, pushed, and opened as a draft PR.
