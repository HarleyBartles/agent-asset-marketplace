# House Skills Decision Manifest Summary

Issue: MARK-14/MARK-15/MARK-16/MARK-17/MARK-18/MARK-19

`decisions.json` is the repo-backed decision/import manifest for the House
Skills source set. It records MARK-9 sanity-rollup decisions after the MARK-13
plugin skeleton. MARK-15 extends that metadata with the observed Linear/Codex
delegation mechanics. MARK-16 through MARK-19 then import reviewed
canonical `SKILL.md` source records while leaving plugin projection for later.

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
- `issue` names the slices that created and extended the manifest.
- `sourceSet` points to the House Skills source root, intake record, asset
  catalog, and provenance record.
- `issueLineage` records MARK-9, MARK-13, MARK-14, MARK-15, MARK-16, MARK-17, MARK-18, and MARK-19 roles.
- `statusVocabulary` defines the accepted decision statuses.
- `pluginPosture` records the first-party bundle/provenance posture, cheap
  bundle-space assumption, and current source-import boundary.
- `globalDecisions` captures cross-skill decisions that later import slices must
  preserve.
- `skillDecisions` captures row-level decisions for active, provisional,
  folded, retired, reference-only, and deferred skill surfaces.
- `todoNextSlices` lists known follow-up work that should not be pretended done
  by the current bounded source-import slice.

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
- Linear/Codex dispatch requires both the responsible human assignee and the
  distinct Codex delegate; coding work must not be delegated to the Linear
  agent.

## MARK-16 Source Import

MARK-16 imports the first two reviewed House Skills source records under the
canonical source root:

- `gpt-skills/house-skills/linear-v1/SKILL.md` is the renamed/reframed successor
  to old `linear-control-plane`. It owns Linear connector mechanics, Linear
  object operations, and durable Linear working-state surfaces.
- `gpt-skills/house-skills/worker-dispatch-linear-v1/SKILL.md` is the
  renamed/reframed successor to old `linear-codex-dispatch`. It owns
  Linear-based Codex worker dispatch, worker status checks, PR-gate routing, PR
  verification routing, and merge-readiness routing.

Both imported source records preserve the MARK-15 delegation mechanics: a
responsible human assignee plus a distinct Codex delegate, no coding delegation
to the Linear agent, and no success claim until the issue is re-fetched and
observable Linear state verifies delegation. The Codex plugin bundle remains a
metadata-only projection in this slice; no `SKILL.md` files are copied into
`plugins/house-skills/skills/`.

No other House Skill source text is imported in MARK-16.

## MARK-17 Source Import

MARK-17 imports the next three reviewed base/work-mode House Skills source
records under the canonical source root:

- `gpt-skills/house-skills/gpt-base-doctrine-v1/SKILL.md` is the versioned
  GPT-wide base doctrine source. It carries the cross-project boring-first
  mantra: “We make exciting things possible by adopting a boring-first
  posture.”
- `gpt-skills/house-skills/work-mode-router-v1/SKILL.md` is the
  renamed/reframed successor to old `gpt-bootstrap`. It owns first
  classification and routes normal coding work away from legacy chat/YAML
  dispatch habits.
- `gpt-skills/house-skills/worker-readiness-prep-v1/SKILL.md` owns executable
  worker handoff shaping and the internal readiness gate.

`worker-readiness-gate-v1` is not imported as a standalone top-level skill. Its
valuable checks are folded into `worker-readiness-prep-v1`. No TPS, busters,
skill maintenance, Adventures, Rooms, deck/PPTX/receipt, unrelated source
imports, or Codex plugin bundle projections are imported in MARK-17.

## Linear/Codex Delegation Mechanics

MARK-15 records the live MARK-13/MARK-14 delegation lesson as metadata for
later `linear-v1` and `worker-dispatch-linear-v1` implementation. The durable
mechanics are:

- Codex Cloud work needs both a human assignee and a Codex delegate.
- The human assignee remains responsible for the issue. The observed working
  human assignee in this workspace is `Harley Bartles`
  (`0f41920d-8499-4555-993d-066c003cf580`).
- The Codex agent is distinct from the Linear agent. Do not delegate coding work
  to the Linear agent.
- The observed working Codex delegate is `Codex`
  (`a1b0a6a6-48b3-4af6-9a99-744f5ae357d1`).
- A connector mutation is not proof of delegation. After assignment or
  delegation mutation, re-fetch the issue and verify observable state before
  claiming dispatch.
- Success evidence includes `delegate: Codex`, the expected human assignee,
  status moved to Todo or In Progress as appropriate, Codex activity, or a PR
  attachment.
- If GitHub connector binding causes Linear mutation or verification
  instability, prefer a Linear-only connector/tool context before retrying
  Linear assignment/delegation. Do not keep blind-retrying unstable mixed-tool
  calls.

These details are represented in `globalDecisions` under
`global.linear-codex-delegation.mechanics` and on the
`worker-dispatch-linear-v1` skill decision row.

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
- `work-mode-router-v1`
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
- `tps-reporting-v1`
- `tps-ingress-v1`

Rows with `importAction: "todo-later"` or
`importAction: "todo-later-with-modification"` intentionally do not claim that
source content has already been imported. Rows with `importAction` values such
as `imported-source-mark-16`, `imported-source-mark-17`, or
`imported-source-mark-18` point to canonical source records under
`gpt-skills/house-skills/`.

## MARK-18 Source Import

MARK-18 imports exactly two TPS protocol House Skills source records under the
canonical source root:

- `gpt-skills/house-skills/tps-reporting-v1/SKILL.md` is the producer-side TPS
  report protocol. It requires a cover sheet, keeps domain-specific report
  bodies owned by the reporting domain, partitions verified source from claims,
  inferences, assumptions, and out-of-scope material, and treats tests as
  evidence rather than automatic issue-goal conformance.
- `gpt-skills/house-skills/tps-ingress-v1/SKILL.md` is the consumer-side TPS
  ingress protocol. It gates incoming reports on cover sheet presence, reviews
  and falsifies material claims against durable source surfaces, and routes
  accept, repair, falsified, or blocked outcomes.

Generic/base source partitioning is folded into TPS in this slice; no distinct
standalone residue was imported. No busters, cleanup custody, skill maintenance,
Adventures, Rooms, plugin projections, standalone GitHub operations, deck/PPTX,
receipt surfaces, or ChatGPT skill ZIPs are imported by MARK-18.

## Non-Import Confirmation

MARK-18 imports only the TPS/reporting-ingress source slice after the earlier
MARK-16 and MARK-17 source imports. It does not project actual House Skill
source content into `plugins/house-skills/skills/`, package ChatGPT skill ZIPs,
import busters, cleanup custody, skill maintenance, Adventures, Rooms,
standalone GitHub operations, deck/PPTX/receipt surfaces, or revive retired
skills as installable entries.

## TODOs for Later Import Slices

- Import remaining reviewed `SKILL.md` content only in bounded later slices.
- Reconcile linked MARK-9 ledgers into repo-backed source records before using
  this manifest as complete source truth for every chunk.
- Add per-skill provenance/license details when each active v1 or v0.1 skill is
  imported.
- Resolve parked Adventures presentation/package QA fragments before silently
  retiring those checks.
- Watch for future evidence of generic/base source partitioning residue outside
  TPS; MARK-18 found no distinct standalone residue.
- Project imported source records into installable Codex plugin bundles only in
  a later explicit projection slice, if desired.

## MARK-18 TPS Reporting/Ingress Source Import

MARK-18 imports the TPS protocol split as private first-party local source:

- `gpt-skills/house-skills/tps-reporting-v1/SKILL.md` for producer-side reports.
- `gpt-skills/house-skills/tps-ingress-v1/SKILL.md` for consumer-side report ingress.

No busters, cleanup custody, skill maintenance, Adventures, Rooms-specific overlays, plugin projections, standalone GitHub operations, deck/PPTX/receipt surfaces, or ChatGPT skill ZIPs are imported in MARK-18.

## MARK-19 Core Generic Buster Source Import

MARK-19 imports the core generic buster slice as reviewed private first-party local source under the canonical House Skills root:

- `gpt-skills/house-skills/buster-framework-v1/SKILL.md` — GPT-wide mechanics for true pre-action buster gates.
- `gpt-skills/house-skills/ambiguity-buster-v1/SKILL.md` — unresolved ambiguity gate.
- `gpt-skills/house-skills/boring-buster-v1/SKILL.md` — boring-readiness gate for small, explicit, falsifiable work.
- `gpt-skills/house-skills/invariant-buster-v1/SKILL.md` — binding-constraint gate.
- `gpt-skills/house-skills/analogy-buster-v1/SKILL.md` — analogy clarity/distortion gate.
- `gpt-skills/house-skills/canon-buster-v1/SKILL.md` — generic canon/source-truth drift gate extracted from Rooms-derived residue without importing Rooms-specific law.

The import is source-only. The Codex plugin projection remains metadata-only and does not bundle these skill files in this slice. MARK-19 does not import TPS/reporting-ingress, cleanup custody, skill maintenance, Adventures, Rooms-specific overlays, plugin projections, deck/PPTX/receipt surfaces, or ChatGPT skill ZIPs.
