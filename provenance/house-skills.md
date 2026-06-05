# House Skills Provenance And Trust Posture

Issue: MARK-13/MARK-14/MARK-15/MARK-16/MARK-17

## Source Identity

House Skills is the repo-backed first-party bundle/provenance group for Harley's
custom GPT-native skills after the MARK-9 sanity rollup.

- Canonical source root: `gpt-skills/house-skills/`
- Codex plugin projection: `plugins/house-skills/`
- Asset catalog: `sources/house-skills/assets.json`
- Intake/source posture record: `sources/house-skills/intake.json`
- Decision/import manifest: `sources/house-skills/decisions.json`
- Readable decision summary: `sources/house-skills/decisions.md`

## MARK-13 Decision

MARK-13 creates a validation-compatible marketplace skeleton only. It establishes
the bundle/provenance shape for future imports without copying full House Skill
source text into the repository.

The installable projection is intentionally thin: it proves the marketplace
entry, plugin manifest, placeholder bundle directories, asset catalog, and
provenance records can validate together.

## MARK-14 Decision Manifest

MARK-14 adds a machine-readable and human-readable decision/import manifest for
the MARK-9 sanity-rollup decisions. The manifest distinguishes v1, v0.1, fold,
retire, reference-only, and defer outcomes so later import slices know what to
import, keep provisional, fold into other surfaces, retire, preserve as
reference-only, or park for future work.

MARK-14 remains metadata-only: it does not import full `SKILL.md` content,
package skill ZIPs, or make retired skills installable.

## MARK-15 Linear/Codex Delegation Mechanics

MARK-15 records the observed Linear/Codex delegation mechanics for later
`linear-v1` and `worker-dispatch-linear-v1` import work. This is metadata and
implementation guidance only; no full skill source is imported here.

The preserved mechanics are that Codex Cloud work needs both a responsible human
assignee and a distinct Codex delegate; the human remains accountable; coding
work must not be delegated to the Linear agent; delegation claims must be
verified by re-fetching the issue after mutation; and unstable mixed
GitHub/Linear connector calls should be replaced with a Linear-only
connector/tool context before retrying rather than blind-retried.

Recorded workspace identities:

- Human assignee: Harley Bartles
  (`0f41920d-8499-4555-993d-066c003cf580`)
- Codex delegate: Codex
  (`a1b0a6a6-48b3-4af6-9a99-744f5ae357d1`)

## MARK-16 Linear And Worker Dispatch Source Import

MARK-16 imports the first actual House Skills source-content slice. The imported
canonical sources are:

- `gpt-skills/house-skills/linear-v1/SKILL.md` — successor to the old installed
  `linear-control-plane` skill, updated for the MARK-9/MARK-15 Linear-first and
  Codex-delegation decisions.
- `gpt-skills/house-skills/worker-dispatch-linear-v1/SKILL.md` — successor to
  the old installed `linear-codex-dispatch` skill, updated for the preferred
  Linear-based dispatch taxonomy and MARK-15 delegation verification rule.

The import is source-only. The Codex plugin projection remains metadata-only and
does not bundle these skill files in this slice. No other House Skills are
imported by MARK-16.

## MARK-17 Base Doctrine And Work-Mode Source Import

MARK-17 imports the next bounded House Skills source-content slice. The imported
canonical sources are:

- `gpt-skills/house-skills/gpt-base-doctrine-v1/SKILL.md` — versioned successor
  to the old installed `gpt-base-doctrine`, updated to carry the cross-project
  boring-first operating mantra as first-class GPT-wide doctrine.
- `gpt-skills/house-skills/work-mode-router-v1/SKILL.md` — renamed/reframed
  successor to old `gpt-bootstrap`, updated so work-mode routing replaces old
  bootstrap confusion and normal coding work routes through Linear/Codex rather
  than chat/YAML dispatch habits.
- `gpt-skills/house-skills/worker-readiness-prep-v1/SKILL.md` — source import
  for executable worker handoff preparation, including the folded internal gate
  behavior from the candidate `worker-readiness-gate-v1`.

The import is source-only. The Codex plugin projection remains metadata-only and
does not bundle these skill files in this slice. `worker-readiness-gate-v1` is
not imported as a standalone top-level skill. No TPS, busters, skill
maintenance, Adventures, Rooms, deck/PPTX/receipt, or unrelated House Skills are
imported by MARK-17.

## Trust And License Posture

- House Skills are first-party/private local assets unless later content import
  records a narrower license or third-party dependency.
- This slice does not mirror third-party content.
- This slice does not package ChatGPT skill ZIPs or generated deployment output.
- Future imports must update this record when they add actual skill content,
  scripts, hooks, assets, or non-first-party material. MARK-17 adds only
  first-party Markdown source records and no scripts, hooks, assets, or
  non-first-party material.

## Active, Provisional, Retired, And Reference-Only Posture

House Skills may eventually be grouped into multiple sensible plugin bundles;
bundle space is cheap. Asset identity is intentionally separate from plugin
projection.

Known MARK-9 posture carried into this skeleton:

- `cleanup-custody-v0.1` is the accepted public rename for the provisional
  cleanup custody workflow; the installed profanity-bearing source name remains
  provenance/history only.
- `rooms-image-sidecars-v0.1` belongs in House Skills as a v0.1 candidate.
- `canon-buster-v1` is a House Skill candidate with generic value extracted
  from the Rooms-specific use.
- `worker-readiness-gate` should live inside `worker-readiness-prep`, not as a
  standalone top-level installable skill in this skeleton.
- `worker-dispatch-linear-v1` is the preferred narrow dispatch/control-plane
  taxonomy candidate if later implementation proves it.
- `skill-creator` is reference-only/system-built-in and is not imported.
- `skill-market` is retired because MARK replaces it.
- Standalone GitHub issue-management and GitHub operations skills are retired;
  Linear is the issue/control-plane surface and GitHub remains a normal
  evidence/tool surface.
- Deck, PPTX, and receipt surfaces are outside this House Skills import slice.

## Quality Posture

Current quality status: early private marketplace skeleton.

Validation route:

```sh
python3 tools/validate_marketplace.py
```

Before external distribution or real installation claims, later slices must add
reviewed skill content, update asset/provenance records, and verify the plugin
projection still matches the canonical source under `gpt-skills/house-skills/`.

## Localization Posture

The skeleton metadata is English-source. No translation is needed for MARK-13.
Future imported skill content should revisit localization needs per skill or
bundle.
