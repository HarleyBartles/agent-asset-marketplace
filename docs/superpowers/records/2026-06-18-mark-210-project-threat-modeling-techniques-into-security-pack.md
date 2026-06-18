# MARK-210 Threat Modeling Techniques Security Pack Implementation Record

**Issue:** MARK-210
**Branch:** `harleydbartles/mark-210-project-threat-modeling-techniques-into-security-pack`
**Starting main SHA:** `e27cbb584b01a48107d374a72296c64449f21e91`
**Implementation commit SHA:** `eb1cc8c8fdc4bb3660cbee0781ea326ac0645d9e`
**PR URL:** [https://github.com/HarleyBartles/agent-asset-marketplace/pull/118](https://github.com/HarleyBartles/agent-asset-marketplace/pull/118)
**Publication state:** This record captures the MARK-210 projection of `threat-modeling-techniques` into `security-pack`, the retained `codex-cortex` custody slice, the generated artifact refresh, and the validation blocker that remains outside the issue slice. The issue is published on branch `harleydbartles/mark-210-project-threat-modeling-techniques-into-security-pack` and tracked by PR #118 against `main`.

## Files changed

Representative repo surfaces changed for this issue:

- `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/`
- `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/`
- `codex-marketplace/plugins/security-pack/`
- `generated/skill-zips/codex-cortex/threat-modeling-techniques/skill.zip`
- `generated/skill-zips/security-pack/threat-modeling-techniques/skill.zip`
- `docs/superpowers/plans/2026-06-18-mark-210-project-threat-modeling-techniques-into-security-pack.md`
- `docs/superpowers/records/2026-06-18-mark-210-project-threat-modeling-techniques-into-security-pack.md`

## Scope and boundary

- Included: the retained upstream `threat-modeling-techniques` source, the `codex-cortex` custody projection, the installable `security-pack` slice, the generated skill zips, marketplace/index/provenance updates, and this durable record.
- Included as a local validation attempt only: the `superpowers` `.codex-plugin/plugin.json` byte-alignment was performed during validation, but it produced no net PR diff and was not part of the published change set.
- Excluded: any repair to `adventures-pack/brainstorming` drift. That is a repo-wide validation blocker, but it is outside the MARK-210 slice and was intentionally left untouched.

## Validation-related repair

`py -3 tools/validate_marketplace.py` initially exposed drift in `codex-marketplace/plugins/superpowers/.codex-plugin/plugin.json`.

I byte-aligned that file by copying the retained source projection over the marketplace projection so validation could proceed, but that attempt did not leave a net diff in the PR. It was outside the MARK-210 security-pack slice and is mentioned here only as a validation step that had to be cleared before the real review blocker could be observed.

## Generated artifact alignment

The MARK-210 work required a regeneration pass for the skill-zip corpus so the new `security-pack` and `codex-cortex` threat-modeling exports existed in `generated/skill-zips/registry.json`.

The targeted generator invocation did not have the needed registry entry yet, so the publish path used:

- `py -3 tools/update_skill_artifacts.py --all`

That regenerated the full corpus and produced the new derived artifacts for:

- `generated/skill-zips/codex-cortex/threat-modeling-techniques/skill.zip`
- `generated/skill-zips/security-pack/threat-modeling-techniques/skill.zip`
- `generated/skill-zips/registry.json`

This is a derived export surface, not canonical source.

## Validation

- `py -3 tools/validate_repo_index.py`
  - Result: passed.
- `py -3 tools/validate_marketplace.py`
  - Result: first failed on `codex-marketplace/plugins/superpowers/.codex-plugin/plugin.json` drift, then failed again after the byte-alignment on unrelated `adventures-pack/brainstorming` drift at `scripts/helper.js`.
- `git diff --check`
  - Result: passed with line-ending warnings only.

## Exact validation blocker

`validate_marketplace.py` currently fails on unrelated repository drift in `adventures-pack/brainstorming`:

- `ValueError: adventures-pack component brainstorming file content mismatch at scripts\helper.js`

I did not repair that drift.

## Notes

- The implementation record intentionally separates the MARK-210 slice from the repo-wide validation blocker.
- The final publication surface for this work remains the branch/PR once the commit is pushed and opened.
