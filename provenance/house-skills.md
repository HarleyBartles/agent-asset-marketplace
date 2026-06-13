# House Skills Provenance

## cleanup-custody

- Source path: `gpt-skills/house-skills/cleanup-custody/v0.1/cleanup-custody-v0.1/SKILL.md`
- Public identity: `cleanup-custody`
- Provenance/history only: legacy profanity-bearing cleanup-skill naming
- Scope: cleanup-custody only
- Notes: Keep the active public source name neutral. Do not use the legacy profanity-bearing name as the primary public surface name.

## skill-validator

- Source path: `gpt-skills/house-skills/skill-validator/v1/skill-validator-v1/SKILL.md`
- Public identity: `skill-validator`
- Provenance/history only: MARK-21 skill maintenance House Skills source slice
- Scope: skill validation
- Notes: Validator requirements are authoritative over creator output. `skill-creator` is reference-only/system-built-in and was not imported. `skill-market` is retired because MARK replaces it and was not revived.

## skill-packager

- Source path: `gpt-skills/house-skills/skill-packager/v1/skill-packager-v1/SKILL.md`
- Public identity: `skill-packager`
- Provenance/history only: MARK-21 skill maintenance House Skills source slice
- Scope: skill packaging
- Notes: Validation must happen before packaging. This source import does not add repo-import ZIP packaging, ChatGPT skill ZIP packaging, plugin projections, or skill-market replacement logic.

## skill-buster

- Source path: `gpt-skills/house-skills/skill-buster/v0.1/skill-buster-v0.1/SKILL.md`
- Public identity: `skill-buster`
- Provenance/history only: MARK-21 skill maintenance House Skills source slice
- Scope: skill maintenance breakdown and closure checks
- Notes: Remains v0.1. One-at-a-time is the reliable boring path. Batch handoff remains unreliable and non-closure-critical.

## connector-safety

- Source path: `gpt-skills/house-skills/connector-safety/SKILL.md`
- Public identity: `connector-safety`
- Provenance/history: installed connector-safety package landed via WILL-274; v1.1 zip update
- Ownership: Harley-authored first-party House skill
- Scope: connector and tool safety blocks, exact-state guarded writes, blocked-write recovery, narrow retries, invalid-attempt handling, and safe-action reporting
- Notes: Canonical source now lives in the House skills lane. `agents/openai.yaml` was copied into repo source control and retains the repository policy fields while adopting the clearer interface description and visual hints from the zip. `assets/icon.svg` was not included because the zip did not provide it.

## adventures-project-doctrine-v1

- Source path: `gpt-skills/house-skills/adventures-project-doctrine/v1/adventures-project-doctrine-v1/SKILL.md`
- Public identity: `adventures-project-doctrine-v1`
- Provenance/history only: MARK-22 prep payload for Adventures House Skills survivor import
- Scope: Adventures project doctrine
- Notes: Imported as the primary Adventures survivor. Preserves shared doctrine, connector posture, visual canon, and resource discipline while stripping retired image-generation framing, deck/PPTX, receipt, and standalone GitHub operations residue from the active House Skills lane.

## gpt-base-doctrine-v1.1

- Source path: `gpt-skills/house-skills/gpt-base-doctrine/SKILL.md`
- Public identity: `gpt-base-doctrine-v1.1`
- Provenance/history only: MARK-30 base and control plane update
- Scope: GPT-wide shared doctrine
- Notes: Imported as the shared doctrine store for GPT-wide House Skills, including the bounded read-loop doctrine and the updated source/reference routing table.

## rooms-image-sidecars

- Source path: `gpt-skills/house-skills/rooms-image-sidecars/v0.1/rooms-image-sidecars-v0.1/SKILL.md`
- Public identity: `rooms-image-sidecars`
- Provenance/history only: MARK-23 prep payload for Rooms House Skills survivor import
- Scope: Rooms image sidecar preparation
- Notes: Imported as the primary Rooms survivor. Provides GPT-side starter packet guidance for image evidence before Albert/Pit ingestion. No standalone GitHub mechanics, canon busters, or adjacent Rooms residue were imported.

## House Skills plugin projection

- Bundle name: `house-skills`
- Bundle version: `1.0.0`
- Marketplace source: `.agents/plugins/marketplace.json`
- Human registry source: `sources/house-skills/decisions.md`
- Structured registry mirror: `sources/house-skills/decisions.json`
- Plugin manifest: `plugins/house-skills/.codex-plugin/plugin.json`
- Bundle skill: `plugins/house-skills/skills/house-skills/SKILL.md`
- Bundle manifest: `plugins/house-skills/skills/house-skills/references/bundle-manifest.json`
- Source map: `plugins/house-skills/skills/house-skills/references/source-map.md`
- Generator: `tools/generate_marketplace.py`
- Validator: `tools/validate_marketplace.py`
- Projection scope: reviewed active House Skills only, grouped into base/control plane, Adventures v1.1, and Rooms, plus the shared `connector-safety` component in the base/control-plane lane
- Notes: This is a Harley-owned first-party Codex marketplace projection kept clean for a future permissive publication decision. It does not replace the source ledger in `sources/house-skills/` and does not make retired, folded, reference-only, or deferred records active installable entries. `connector-safety` is projected here as a shared safety dependency for side-effecting connector/tool work.

## Active imports

### Base and control plane

- `don-logan-boundary-v1` - `gpt-skills/house-skills/don-logan-boundary/v1/don-logan-boundary-v1/SKILL.md`
- `gpt-base-doctrine-v1.1` - `gpt-skills/house-skills/gpt-base-doctrine/SKILL.md`
- `work-mode-router-v1` - `gpt-skills/house-skills/work-mode-router/v1/work-mode-router-v1/SKILL.md`
- `worker-dispatch-linear-v1` - `gpt-skills/house-skills/worker-dispatch-linear/v1/worker-dispatch-linear-v1/SKILL.md`
- `linear-v1.1` - `gpt-skills/house-skills/linear/SKILL.md`
- `tps-reporting-v1` - `gpt-skills/house-skills/tps-reporting/v1/tps-reporting-v1/SKILL.md`
- `tps-ingress-v1` - `gpt-skills/house-skills/tps-ingress/v1/tps-ingress-v1/SKILL.md`
- `session-buster-v0.2` - `gpt-skills/house-skills/session-buster/v0.2/session-buster-v0.2/SKILL.md`
- `session-buster-ingress-v0.2` - `gpt-skills/house-skills/session-buster-ingress/v0.2/session-buster-ingress-v0.2/SKILL.md`
- `crew-v1` - `gpt-skills/house-skills/crew/v1/crew-v1/SKILL.md`
- `crew-buster-v1` - `gpt-skills/house-skills/crew-buster/v1/crew-buster-v1/SKILL.md`

### Adventures v1.1

- `adventures-project-doctrine-v1.1` - `gpt-skills/house-skills/adventures-project-doctrine/v1.1/adventures-project-doctrine-v1.1/SKILL.md`
- `adventures-bootstrap-v1.1` - `gpt-skills/house-skills/adventures-bootstrap/v1.1/adventures-bootstrap-v1.1/SKILL.md`
- `adventures-github-operations-v1.1` - `gpt-skills/house-skills/adventures-github-operations/v1.1/adventures-github-operations-v1.1/SKILL.md`
- `adventures-visual-preproduction-v1.1` - `gpt-skills/house-skills/adventures-visual-preproduction/v1.1/adventures-visual-preproduction-v1.1/SKILL.md`
- `adventures-storyboard-preflight-v1.1` - `gpt-skills/house-skills/adventures-storyboard-preflight/v1.1/adventures-storyboard-preflight-v1.1/SKILL.md`
- `adventures-visual-bible-creator-v1.1` - `gpt-skills/house-skills/adventures-visual-bible-creator/v1.1/adventures-visual-bible-creator-v1.1/SKILL.md`
- `adventures-visual-bible-interpreter-v1.1` - `gpt-skills/house-skills/adventures-visual-bible-interpreter/v1.1/adventures-visual-bible-interpreter-v1.1/SKILL.md`
- `adventures-image-qa-v1.1` - `gpt-skills/house-skills/adventures-image-qa/v1.1/adventures-image-qa-v1.1/SKILL.md`
- `adventures-asset-sheet-compiler-v1.1` - `gpt-skills/house-skills/adventures-asset-sheet-compiler/v1.1/adventures-asset-sheet-compiler-v1.1/SKILL.md`
- `adventures-frame-buster-v1.1` - `gpt-skills/house-skills/adventures-frame-buster/v1.1/adventures-frame-buster-v1.1/SKILL.md`

### Rooms

- `rooms-project-doctrine-v1` - `gpt-skills/house-skills/rooms-project-doctrine/v1/rooms-project-doctrine-v1/SKILL.md`
- `rooms-bootstrap-v1` - `gpt-skills/house-skills/rooms-bootstrap/v1/rooms-bootstrap-v1/SKILL.md`
- `rooms-source-partitioning-v1` - `gpt-skills/house-skills/rooms-source-partitioning/v1/rooms-source-partitioning-v1/SKILL.md`
- `rooms-ambiguity-buster-v1` - `gpt-skills/house-skills/rooms-ambiguity-buster/v1/rooms-ambiguity-buster-v1/SKILL.md`
- `rooms-analogy-buster-v1` - `gpt-skills/house-skills/rooms-analogy-buster/v1/rooms-analogy-buster-v1/SKILL.md`
- `rooms-zoom-outs-buster-v1` - `gpt-skills/house-skills/rooms-zoom-outs-buster/v1/rooms-zoom-outs-buster-v1/SKILL.md`
- `rooms-character-investigation-v1` - `gpt-skills/house-skills/rooms-character-investigation/v1/rooms-character-investigation-v1/SKILL.md`
- `rooms-sheet-creator-v1` - `gpt-skills/house-skills/rooms-sheet-creator/v1/rooms-sheet-creator-v1/SKILL.md`

Retired, folded, reference-only, and deferred MARK-9 decisions remain in Linear ledgers and are not duplicated here.
