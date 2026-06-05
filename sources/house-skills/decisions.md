# House Skills Decision Manifest Summary

Issue: MARK-14

`decisions.json` is the repo-backed decision/import manifest for the House
Skills source set. It records MARK-9 sanity-rollup decisions after the MARK-13
plugin skeleton without importing full `SKILL.md` content.

## Manifest Path

- Machine-readable manifest: `sources/house-skills/decisions.json`
- Human-readable summary: `sources/house-skills/decisions.md`
- Source root marker: `gpt-skills/house-skills/`
- Plugin projection placeholder: `plugins/house-skills/`

This location keeps source/intake decisions separate from the Codex plugin
projection. Later slices can import reviewed source into `gpt-skills/house-skills/`
and project one or more sensible bundles afterward.

## Schema Fields

The JSON manifest uses these top-level fields:

- `manifestVersion` and `manifestId` identify the manifest format and record.
- `issue` names the slice that created the manifest.
- `sourceSet` points to the House Skills source root, intake record, asset
  catalog, and provenance record.
- `issueLineage` records MARK-9, MARK-13, and MARK-14 roles.
- `statusVocabulary` defines the accepted decision statuses.
- `pluginPosture` records the first-party bundle/provenance posture, cheap
  bundle-space assumption, and no-full-import boundary.
- `globalDecisions` captures cross-skill decisions that later import slices must
  preserve.
- `skillDecisions` captures row-level decisions for active, provisional,
  folded, retired, reference-only, and deferred skill surfaces.
- `todoNextSlices` lists known follow-up work that should not be pretended done
  by this slice.

## Status Vocabulary

- `v1`: stable versioned House Skill candidate for later source import.
- `v0.1`: useful and bundleable, but provisional and not v1-ready.
- `fold`: do not import as standalone; move surviving value to the named home.
- `retire`: do not import or revive as active installable skill content.
- `reference-only`: preserve as evidence/system/context reference only.
- `defer`: out of the current House Skills import; preserve parked questions or
  future owner without claiming active import readiness.

## Global Decisions Captured

- `skill-creator` is reference-only/system-built-in and not imported.
- `skill-market` retires because MARK replaces it.
- Standalone GitHub issue-management and GitHub operations skills retire; GitHub
  remains ordinary evidence/tool surface only.
- `worker-readiness-gate` behavior folds inside `worker-readiness-prep` instead
  of standing alone as a top-level House Skill in this manifest.
- Generic/base source partitioning probably belongs in TPS unless implementation
  proves residue.
- Deck/PPTX/receipt surfaces are out of this House Skills import.
- `cleanup-custody-v0.1` is the accepted public rename for the installed
  profanity-bearing cleanup skill; the original name is provenance/history only.
- PRs are the normal worker work packet for repo/code work.

## First Skill Decision Rows

The first rows needed by later import slices are present in `skillDecisions`,
including:

- `skill-validator-v1`
- `skill-packager-v1`
- `skill-buster-v0.1`
- `canon-buster-v1`
- `cleanup-custody-v0.1`
- `rooms-image-sidecars-v0.1`
- `skill-creator`
- `skill-market`
- `github-issue-management`
- `github-operations`
- `worker-readiness-prep-v1`
- `worker-readiness-gate-v1`
- `worker-dispatch-linear-v1`
- `generic-base-source-partitioning`
- `deck-pptx-receipt-surfaces`
- `adventures-presentation-qa`
- `adventures-project-doctrine-v1`
- `gpt-base-doctrine-v1`
- `pig-stack`
- `adventures-github-overlay`
- `rooms-github-proof-residue`

Rows with `importAction: "todo-later"` or
`importAction: "todo-later-with-modification"` intentionally do not claim that
source content has already been imported.

## Non-Import Confirmation

MARK-14 adds decision/provenance metadata only. It does not project actual House
Skill source content into `plugins/house-skills/skills/`, package ChatGPT skill
ZIPs, or revive retired skills as installable entries.

## TODOs for Later Import Slices

- Import reviewed `SKILL.md` content only in bounded later slices.
- Reconcile linked MARK-9 ledgers into repo-backed source records before using
  this manifest as complete source truth for every chunk.
- Add per-skill provenance/license details when each active v1 or v0.1 skill is
  imported.
- Resolve parked Adventures presentation/package QA fragments before silently
  retiring those checks.
- Prove whether generic/base source partitioning has residue outside TPS during
  implementation.
