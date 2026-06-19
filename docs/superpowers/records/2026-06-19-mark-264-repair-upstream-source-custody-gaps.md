# MARK-264 Implementation Record

**Goal:** normalize the frontend-pack custody pointers onto the retained `codex-cortex` source root without reshaping the active marketplace surface.

## Scope

- Updated the frontend-pack README, source note, source map, and provenance note to point at the normalized `sources/third_party/codex-cortex/upstream/` custody root.
- Kept the projected skill set, bundle contents, and marketplace boundaries unchanged.
- Recorded the work in the Superpowers plan/record surfaces for issue-traceable handoff.

## Files Changed

- `codex-marketplace/plugins/frontend-pack/README.md`
- `codex-marketplace/plugins/frontend-pack/SOURCE.md`
- `codex-marketplace/plugins/frontend-pack/references/source-map.md`
- `docs/superpowers/plans/2026-06-19-mark-264-repair-upstream-source-custody-gaps.md`
- `docs/superpowers/records/2026-06-19-mark-264-repair-upstream-source-custody-gaps.md`
- `provenance/frontend-pack.md`

## Validation

- `py -3 tools/validate_marketplace.py`
- `py -3 tools/validate_repo_index.py`
- `py -3 tools/validate_skill_zips.py`
- `git diff --check`

## Generated Artifacts

No generated artifact content changed. The repo already retained the frontend skill slice under the normalized `codex-cortex` custody root, so this issue only needed source/provenance pointer normalization and no regeneration step.

## Notes

- `dotnet-kit` was inspected as part of the issue source basis, but its selective retained snapshot remained within the current pack boundary and did not require a change for this repair.

## Publication

- Branch: `harleydbartles/mark-264-repair-upstream-source-custody-gaps`
- Commit: `c1e607681536035a4d25a8f003deff339859c708`
- Draft PR: [#134](https://github.com/HarleyBartles/agent-asset-marketplace/pull/134)
