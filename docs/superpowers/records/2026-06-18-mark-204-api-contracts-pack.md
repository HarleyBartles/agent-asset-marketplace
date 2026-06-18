# MARK-204 API Contracts Pack Implementation Record

**Issue:** MARK-204
**Branch:** `codex/mark-204-api-contracts-pack`
**Starting main SHA:** `e1c06e33f691247b184a59e7c2fcf595798a998b`
**Implementation commit SHA:** `51083b27af272297c469ae6b990c890f9ed1a305`
**PR URL:** [https://github.com/HarleyBartles/agent-asset-marketplace/pull/114](https://github.com/HarleyBartles/agent-asset-marketplace/pull/114)
**Publication state:** Published on branch `codex/mark-204-api-contracts-pack` and tracked by PR #114 against `main`. This record captures the MARK-204 API Contracts Pack projection and the follow-up review repair that corrected the copied-forward icon label and the MARK reference in the bundle manifest.

## Files changed

- `codex-marketplace/plugins/api-contracts-pack/assets/icon.svg`
- `codex-marketplace/plugins/api-contracts-pack/references/bundle-manifest.json`
- `docs/superpowers/records/2026-06-18-mark-204-api-contracts-pack.md`

## Scope and boundary

- Included: the installable `api-contracts-pack` projection for `api-design-patterns`, the retained `codex-cortex` custody slice, generated skill zip outputs, registry/index surfaces, and this durable record.
- Excluded from this child: `openapi-specification`, which remains with MARK-205.
- The repair pass was limited to copied-forward residue and record clarity. It did not expand the pack scope.

## Repair details

- Updated `codex-marketplace/plugins/api-contracts-pack/assets/icon.svg` so the `aria-label` names `API Contracts Pack` instead of `Architecture Pack`.
- Updated `codex-marketplace/plugins/api-contracts-pack/references/bundle-manifest.json` so the boundary note says `openapi-specification remains out of scope for MARK-204`.

## Generated-artifact alignment

The original implementation regenerated both installable zip surfaces because the same imported `api-design-patterns` slice is exported in two plugin roots: the retained `codex-cortex` custody plugin and the installable `api-contracts-pack` projection.

Regeneration commands used during the implementation:

- `py -3 tools/update_skill_artifacts.py --skill api-contracts-pack/api-design-patterns`
- `py -3 tools/update_skill_artifacts.py --skill codex-cortex/api-design-patterns`

Changed zip paths from that regeneration:

- `generated/skill-zips/api-contracts-pack/api-design-patterns/skill.zip`
- `generated/skill-zips/codex-cortex/api-design-patterns/skill.zip`
- `generated/skill-zips/registry.json`

## Validation

- `py -3 tools/validate_marketplace.py`
  - Result: passed.
- `py -3 tools/validate_repo_index.py`
  - Result: passed.
- `git diff --check`
  - Result: passed.

## Skipped checks

- None for this repair pass.

## Notes

- The PR head remains the published delivery surface for the issue.
- The implementation record is intentionally factual about the two generated zip outputs and the reason both changed: each plugin root carries its own installable artifact for the same imported slice.
