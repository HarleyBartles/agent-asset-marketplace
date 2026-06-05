# House Skills Provenance And Trust Posture

Issue: MARK-13/MARK-14/MARK-15

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

## Trust And License Posture

- House Skills are first-party/private local assets unless later content import
  records a narrower license or third-party dependency.
- This slice does not mirror third-party content.
- This slice does not package ChatGPT skill ZIPs or generated deployment output.
- Future imports must update this record when they add actual skill content,
  scripts, hooks, assets, or non-first-party material.

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
