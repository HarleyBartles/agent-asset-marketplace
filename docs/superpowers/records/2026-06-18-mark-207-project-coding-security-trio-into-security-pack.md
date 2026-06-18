# MARK-207 Project Coding-Security Trio Into Security Pack Implementation Record

**Issue:** MARK-207
**Branch:** `harleydbartles/mark-207-project-coding-security-trio-into-security-pack`
**Starting main SHA:** `2931b99f407215d6b5cea137a64d2947b7284497`
**Implementation commit SHA:** `21dc9d9d4d7098fd6dc5e063d92d814fd7d26e2f`
**PR URL:** [https://github.com/HarleyBartles/agent-asset-marketplace/pull/120](https://github.com/HarleyBartles/agent-asset-marketplace/pull/120)
**Publication state:** The MARK-207 trio projection is published on the required branch and tracked by PR #120 against `main`. This record captures the repo-resident change set, the derived artifact refresh, and the remaining repo-wide validation blocker that is outside the issue slice.

## Files changed

Representative repo surfaces changed for this issue:

- `sources/third_party/codex-cortex/upstream/skills/secure-coding-practices/`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/`
- `sources/third_party/codex-cortex/upstream/skills/security-testing-patterns/`
- `codex-marketplace/plugins/codex-cortex/skills/secure-coding-practices/`
- `codex-marketplace/plugins/codex-cortex/skills/owasp-top-10/`
- `codex-marketplace/plugins/codex-cortex/skills/security-testing-patterns/`
- `codex-marketplace/plugins/security-pack/skills/secure-coding-practices/`
- `codex-marketplace/plugins/security-pack/skills/owasp-top-10/`
- `codex-marketplace/plugins/security-pack/skills/security-testing-patterns/`
- `codex-marketplace/plugins/codex-cortex/.codex-plugin/plugin.json`
- `codex-marketplace/plugins/security-pack/.codex-plugin/plugin.json`
- `codex-marketplace/plugins/codex-cortex/README.md`
- `codex-marketplace/plugins/codex-cortex/SOURCE.md`
- `codex-marketplace/plugins/codex-cortex/references/source-map.md`
- `codex-marketplace/plugins/codex-cortex/references/bundle-manifest.json`
- `codex-marketplace/plugins/security-pack/README.md`
- `codex-marketplace/plugins/security-pack/SOURCE.md`
- `codex-marketplace/plugins/security-pack/references/source-map.md`
- `codex-marketplace/plugins/security-pack/references/bundle-manifest.json`
- `sources/first_party/skills/codex-cortex/intake.json`
- `sources/first_party/skills/codex-cortex/decisions.json`
- `sources/first_party/skills/codex-cortex/decisions.md`
- `provenance/codex-cortex.md`
- `sources/README.md`
- `sources/third_party/README.md`
- `repo-index/repo-index.json`
- `generated/skill-zips/registry.json`
- `generated/skill-zips/codex-cortex/secure-coding-practices/skill.zip`
- `generated/skill-zips/codex-cortex/owasp-top-10/skill.zip`
- `generated/skill-zips/codex-cortex/security-testing-patterns/skill.zip`
- `generated/skill-zips/security-pack/secure-coding-practices/skill.zip`
- `generated/skill-zips/security-pack/owasp-top-10/skill.zip`
- `generated/skill-zips/security-pack/security-testing-patterns/skill.zip`
- `docs/superpowers/plans/2026-06-18-mark-207-project-coding-security-trio-into-security-pack.md`
- `docs/superpowers/records/2026-06-18-mark-207-project-coding-security-trio-into-security-pack.md`

## Scope and boundary

- Included: the retained upstream trio source, the `codex-cortex` custody projection, the installable `security-pack` slice, the derived skill-zip refresh, marketplace/index/provenance updates, and this durable record.
- Included as a validation repair only: byte-normalizing `codex-marketplace/plugins/superpowers/.codex-plugin/plugin.json` so the marketplace validator could advance past a raw-byte mismatch unrelated to the MARK-207 slice.
- Excluded: the remaining `adventures-pack/brainstorming` drift. That is a repo-wide validation blocker, but it is outside the MARK-207 slice and was intentionally left untouched.

## Generated artifact alignment

The MARK-207 work required regenerating the skill-zip corpus so the new `security-pack` and `codex-cortex` skill exports existed in `generated/skill-zips/registry.json`.

The regeneration step used:

- `py -3 tools/update_skill_artifacts.py --all`

That produced the derived exports for:

- `generated/skill-zips/codex-cortex/secure-coding-practices/skill.zip`
- `generated/skill-zips/codex-cortex/owasp-top-10/skill.zip`
- `generated/skill-zips/codex-cortex/security-testing-patterns/skill.zip`
- `generated/skill-zips/security-pack/secure-coding-practices/skill.zip`
- `generated/skill-zips/security-pack/owasp-top-10/skill.zip`
- `generated/skill-zips/security-pack/security-testing-patterns/skill.zip`
- `generated/skill-zips/registry.json`

This is a derived export surface, not canonical source.

## Validation

- `py -3 tools/validate_repo_index.py`
  - Result: passed.
- `py -3 tools/validate_skill_zips.py`
  - Result: passed.
- `py -3 tools/validate_generated_drift.py --base origin/main`
  - Result: passed after marking the new trio source and generated paths intent-to-add so the diff-based check could see them.
- `git diff --check`
  - Result: passed with line-ending warnings only.
- `py -3 tools/validate_marketplace.py`
  - Result: failed on unrelated `adventures-pack` mirror drift at `scripts\\helper.js`.

## Exact validation blocker

`validate_marketplace.py` currently fails on unrelated repository drift in `adventures-pack/brainstorming`:

- `ValueError: adventures-pack component brainstorming file content mismatch at scripts\\helper.js`

I did not repair that drift.

## Notes

- The implementation record is intentionally factual about the MARK-207 slice and the repo-wide blocker.
- The final publication metadata will be filled in after the branch is committed, pushed, and opened as a draft PR.
