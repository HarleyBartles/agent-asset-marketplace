# House Skills Source Root

Issue: MARK-13/MARK-14

This directory is the canonical source-root marker for House Skills: Harley's
first-party GPT-native custom skill set after the MARK-9 sanity rollup.

MARK-16 imports the first reviewed full skill source records under this root.
Later House Skills import slices should continue adding reviewed, versioned
GPT-native skill sources here before projecting them into one or more Codex
plugin bundles.

## Current Scope

- Establish first-party source custody for the `house-skills` asset family.
- Keep accepted, provisional, retired, folded, and reference-only decisions in
  provenance/source metadata instead of pretending every historical skill is
  active or installable.
- Preserve the distinction between canonical skill source identity and Codex
  plugin projection.

## Non-Goals In This Slice

- No ChatGPT skill ZIP packaging.
- No full House Skills text import.
- No revival of `skill-market`.
- No standalone GitHub operations or GitHub issue-management skills.
- No deck, PPTX, or receipt surfaces.

## Decision Manifest

MARK-14 adds the repo-backed House Skills decision/import manifest at
`sources/house-skills/decisions.json` and a human-readable summary at
`sources/house-skills/decisions.md`. Later import slices should use that
manifest to decide which skills to import as v1, keep as v0.1, fold, retire,
treat as reference-only, or defer.

## Imported Source Records

MARK-16 imports exactly two canonical House Skills source records:

- `linear-v1/SKILL.md` — renamed/reframed successor to old
  `linear-control-plane`; owns Linear connector mechanics and durable Linear
  working-state operations.
- `worker-dispatch-linear-v1/SKILL.md` — renamed/reframed successor to old
  `linear-codex-dispatch`; owns Linear-based Codex worker dispatch, status,
  PR-gate, and PR-verification routing.

These source records preserve the MARK-15 rule that Codex Cloud coding work
uses a responsible human assignee plus a distinct Codex delegate, and that
connector mutation is not proof until the issue is re-fetched and observable
state verifies delegation.

No other House Skill source text is imported in MARK-16.
