# House Skills Provenance

## cleanup-custody

- Source path: `codex-marketplace/plugins/house-skills/skills/cleanup-custody/v0.1/cleanup-custody-v0.1/SKILL.md`
- Public identity: `cleanup-custody`
- Provenance/history only: legacy profanity-bearing cleanup-skill naming
- Scope: cleanup-custody only
- Notes: Keep the active public source name neutral. Do not use the legacy profanity-bearing name as the primary public surface name.

## skill-validator

- Source path: `codex-marketplace/plugins/house-skills/skills/skill-validator/v1/skill-validator-v1/SKILL.md`
- Public identity: `skill-validator`
- Provenance/history only: MARK-21 skill maintenance House Skills source slice
- Scope: skill validation
- Notes: Validator requirements are authoritative over creator output. `skill-creator` is reference-only/system-built-in and was not imported. `skill-market` is retired because MARK replaces it and was not revived.

## skill-packager

- Source path: `codex-marketplace/plugins/house-skills/skills/skill-packager/v1/skill-packager-v1/SKILL.md`
- Public identity: `skill-packager`
- Provenance/history only: MARK-21 skill maintenance House Skills source slice
- Scope: skill packaging
- Notes: Validation must happen before packaging. This source import does not add repo-import ZIP packaging, ChatGPT skill ZIP packaging, plugin projections, or skill-market replacement logic.

## connector-safety

- Source path: `codex-marketplace/plugins/house-skills/skills/connector-safety`
- Public identity: `connector-safety`
- Provenance/history: installed connector-safety package landed via WILL-274; v1.1 zip update
- Ownership: Harley-authored first-party House skill
- Scope: connector and tool safety blocks, discover-before-mutation flow, exact-state guarded writes, blocked-write recovery, narrow retries, invalid-attempt handling, post-create read chains, and safe-action reporting
- Notes: Canonical source now lives in the House skills lane. `agents/openai.yaml` was copied into repo source control and retains the repository policy fields while adopting the clearer interface description and visual hints from the zip. `assets/icon.svg` was not included because the zip did not provide it. The current update sharpens the connector safety doctrine with mandatory discover -> read -> write -> verify guidance while preserving the existing blocked-write and exact-state guard rules.

## adventures-project-doctrine-v1

- Source path: `codex-marketplace/plugins/house-skills/skills/adventures-project-doctrine/v1/adventures-project-doctrine-v1/SKILL.md`
- Public identity: `adventures-project-doctrine-v1`
- Provenance/history only: MARK-22 prep payload for Adventures House Skills survivor import
- Scope: Adventures project doctrine
- Notes: Imported as the primary Adventures survivor. Preserves shared doctrine, connector posture, visual canon, and resource discipline while stripping retired image-generation framing, deck/PPTX, receipt, and standalone GitHub operations residue from the active House Skills lane.

## gpt-base-doctrine-v1.1

- Source path: `codex-marketplace/plugins/house-skills/skills/gpt-base-doctrine`
- Public identity: `gpt-base-doctrine-v1.1`
- Provenance/history only: MARK-30 base and control plane update
- Scope: GPT-wide shared doctrine
- Notes: Imported as the shared doctrine store for GPT-wide House Skills, including the bounded read-loop doctrine and the updated source/reference routing table.

## rooms-image-sidecars

- Source path: `codex-marketplace/plugins/house-skills/skills/rooms-image-sidecars/v0.1/rooms-image-sidecars-v0.1/SKILL.md`
- Public identity: `rooms-image-sidecars`
- Provenance/history only: MARK-23 prep payload for Rooms House Skills survivor import
- Scope: Rooms image sidecar preparation
- Notes: Imported as the primary Rooms survivor. Provides GPT-side starter packet guidance for image evidence before Albert/Pit ingestion. No standalone GitHub mechanics, canon busters, or adjacent Rooms residue were imported.

## rooms-canon-buster

- Source path: `codex-marketplace/plugins/house-skills/skills/rooms-canon-buster`
- Public identity: `rooms-canon-buster`
- Provenance/history: MARK-97 attached rooms canon buster zip update
- Ownership: Harley-authored first-party House skill
- Scope: Rooms canon pressure checks and lawful canon/item adjustment
- Notes: Canonical source now lives in the House skills lane and is projected into the Rooms portion of the bundle. `agents/openai.yaml` was copied into repo source control and keeps the clear policy/interface fields from the zip. `assets/icon.svg` was included with the zip and is vendored here.

## asset-market

- Source path: `codex-marketplace/plugins/house-skills/skills/asset-market`
- Public identity: `asset-market`
- Provenance/history: MARK-109 saved GPT skill zip source package
- Scope: marketplace source and pack acquisition
- Notes: Imported from the saved zip as the exact-fidelity source staging root for marketplace pulls, including pack-root resolution and per-skill install-unit expansion.

## linear-issue-compactor

- Source path: `codex-marketplace/plugins/house-skills/skills/linear-issue-compactor`
- Public identity: `linear-issue-compactor`
- Provenance/history: MARK-135 Linear issue compactor skill
- Scope: Linear issue compaction and connector-readable issue bodies
- Notes: Repo-backed first-party Linear compaction skill for splitting oversized issue bodies into attached documents plus a compact TOC body while preserving issue fidelity.

## boring-loop

- Source path: `codex-marketplace/plugins/house-skills/skills/boring-loop`
- Public identity: `boring-loop`
- Provenance/history: MARK-152 Boring Loop beta first-party source
- Ownership: Harley-owned first-party House skill
- Scope: loop cadence, readiness and false-green prevention, parent/child DoD coverage, queue grooming, next boring move selection, route-to-specialist guidance
- Notes: Canonical source lives at `sources/first_party/skills/boring-loop/` and is projected into House Skills and repo-worker-base. Direct GPT export is the default unless a later validation proves an overlay is required.

## linear-superpowers

- Source path: `codex-marketplace/plugins/house-skills/skills/linear-superpowers`
- Public identity: `linear-superpowers`
- Provenance/history: MARK-139 Linear Superpowers compositional skill
- Ownership: Harley-owned first-party House skill
- Scope: Linear issue and track shaping with smallest-applicable workflow selection
- Notes: New first-party compositional Linear workflow skill for naming the smallest applicable workflow skill, explaining why it applies, and listing the evidence required to prove it was followed. The canonical source is a directory-level skill spec with `SKILL.md` and `agents/openai.yaml`, and it composes `/using-superpowers`, `/writing-plans`, `/executing-plans`, `/connector-safety`, `/linear-issue-compactor`, and `/unslop-superpowers` without creating a second source of truth or requiring a GPT-only overlay.

## github-operations

- Source path: `codex-marketplace/plugins/house-skills/skills/github-operations`
- Public identity: `github-operations`
- Provenance/history: MARK-142 GitHub operations zip import
- Ownership: Harley-owned first-party House skill
- Scope: GitHub evidence, PR review routing, and publication proof
- Notes: First-party GitHub proof skill for verifying GitHub repository evidence, publication proof, mergeability, and closure claims. The native review write reference keeps same-account connector use on `COMMENT` reviews instead of trying to force `REQUEST_CHANGES`. The Adventures overlay composes this base skill rather than owning the generic doctrine.

## github-superpowers

- Source path: `codex-marketplace/plugins/house-skills/skills/github-superpowers`
- Public identity: `github-superpowers`
- Provenance/history: MARK-143 GitHub Superpowers compositional skill
- Ownership: Harley-owned first-party House skill
- Scope: GitHub-facing workflow selection, proof boundaries, and branch-closeout routing
- Notes: First-party compositional GitHub workflow skill for naming the smallest applicable specialist workflow, preserving `github-operations` as the GitHub proof and review-write boundary skill, and keeping GitHub proof, publication, merge, and final-main verification narrow. The canonical source is a directory-level skill spec with `SKILL.md` and `agents/openai.yaml`, and it composes `@unslop-superpowers` when repo-specific anti-slop controls or evidence requirements matter.

## unslop-superpowers

- Source path: `codex-marketplace/plugins/house-skills/skills/unslop-superpowers`
- Public identity: `unslop-superpowers`
- Provenance/history: MARK-144 Unslop Superpowers compositional guard skill
- Ownership: Harley-owned first-party House skill
- Scope: repo-specific anti-slop controls, profile-aware workflow shaping, and the narrow direct-to-main escape hatch for profile-only updates
- Notes: First-party compositional anti-slop guard skill for turning repo unslop profile findings into non-goals, evidence requirements, and review controls. The canonical source is a directory-level skill spec with `SKILL.md` and `agents/openai.yaml`, and it composes `@using-superpowers`, `@connector-safety`, and `@unslop` without replacing the underlying profile-generation engine.

## skill-handoff

- Source path: `codex-marketplace/plugins/house-skills/skills/skill-handoff`
- Public identity: `skill-handoff`
- Provenance/history: MARK-109 saved GPT skill zip source package
- Scope: skill package handoff cadence
- Notes: Imported from the saved zip as the exact handoff surface for visible `skill.zip` presentation and landed confirmation.

## skill-installer

- Source path: `codex-marketplace/plugins/house-skills/skills/skill-installer`
- Public identity: `skill-installer`
- Provenance/history: MARK-109 saved GPT skill zip source package
- Scope: skill installation handoff orchestration
- Notes: Imported from the saved zip as the source-to-handoff coordinator for GPT skill installation flows.

## rooms-bootstrap

- Source path: `codex-marketplace/plugins/house-skills/skills/rooms-bootstrap`
- Public identity: `rooms-bootstrap`
- Provenance/history: MARK-97 rooms bootstrap zip update
- Scope: Rooms first-read router
- Notes: Imported as the compact Rooms router that cleans the route map and hands off to project doctrine or a more specific Rooms capability. Preserves the stronger repo/posture routing while adopting the zip's clearer packaging metadata. `agents/openai.yaml` keeps the repo-local brand color and implicit invocation fields; `assets/icon.svg` stays the active icon.
## wild-bunch-project-doctrine-v1

- Source path: `codex-marketplace/plugins/house-skills/skills/wild-bunch-project-doctrine`
- Public identity: `wild-bunch-project-doctrine`
- Provenance/history: MARK-85 Wild Bunch first-party source hydration from attached zip
- Ownership: Harley-authored first-party House skill
- Scope: Wild Bunch project posture and repo sensitivity
- Notes: Hydrated from the authoritative attached zip and projected unchanged into the House Skills lane.

## wild-bunch-domain-modeling-v1

- Source path: `codex-marketplace/plugins/house-skills/skills/wild-bunch-domain-modeling`
- Public identity: `wild-bunch-domain-modeling`
- Provenance/history: MARK-85 Wild Bunch first-party source hydration from attached zip
- Ownership: Harley-authored first-party House skill
- Scope: Wild Bunch gameplay state, GameSession boundaries, clue and journal flows, travel, horses, and hidden culprit truth
- Notes: Hydrated from the authoritative attached zip and projected unchanged into the House Skills lane.

## wild-bunch-dotnet-architecture-v1

- Source path: `codex-marketplace/plugins/house-skills/skills/wild-bunch-dotnet-architecture`
- Public identity: `wild-bunch-dotnet-architecture`
- Provenance/history: MARK-85 Wild Bunch first-party source hydration from attached zip
- Ownership: Harley-authored first-party House skill
- Scope: Wild Bunch C#/.NET architecture guardrails for domain ownership, mutation routes, persistence, and framework leakage
- Notes: Hydrated from the authoritative attached zip and projected unchanged into the House Skills lane.

## wild-bunch-browser-game-v1

- Source path: `codex-marketplace/plugins/house-skills/skills/wild-bunch-browser-game`
- Public identity: `wild-bunch-browser-game`
- Provenance/history: MARK-85 Wild Bunch first-party source hydration from attached zip
- Ownership: Harley-authored first-party House skill
- Scope: Wild Bunch browser delivery, HUD design, Phaser/TypeScript/Vite, DOM overlays, playtest evidence, and browser QA
- Notes: Hydrated from the authoritative attached zip and projected unchanged into the House Skills lane.

## wild-bunch-worker-verification-v1

- Source path: `codex-marketplace/plugins/house-skills/skills/wild-bunch-worker-verification`
- Public identity: `wild-bunch-worker-verification`
- Provenance/history: MARK-85 Wild Bunch first-party source hydration from attached zip
- Ownership: Harley-authored first-party House skill
- Scope: Wild Bunch worker returns, PRs, commits, validation notes, and completion verification
- Notes: Hydrated from the authoritative attached zip and projected unchanged into the House Skills lane.

## House Skills plugin projection

- Bundle name: `house-skills`
- Bundle version: `1.0.0`
- Marketplace source: `.agents/plugins/marketplace.json`
- Human registry source: `sources/first_party/skills/house-skills/decisions.md`
- Structured registry mirror: `sources/first_party/skills/house-skills/decisions.json`
- Plugin manifest: `codex-marketplace/plugins/house-skills/.codex-plugin/plugin.json`
- Bundle skill: `codex-marketplace/plugins/house-skills/skills/house-skills`
- Bundle manifest: `codex-marketplace/plugins/house-skills/skills/house-skills/references/bundle-manifest.json`
- Source map: `codex-marketplace/plugins/house-skills/skills/house-skills/references/source-map.md`
- Generator: `tools/generate_marketplace.py`
- Validator: `tools/validate_marketplace.py`
- Projection scope: reviewed active House Skills only, grouped into base/control plane, Adventures v1.1, Rooms, and Wild Bunch, plus the shared `connector-safety` component in the base/control-plane lane, the new `github-operations` and `github-superpowers` GitHub skills, the `codex-repo-receipts` repo receipt skill, the `rooms-canon-buster` Rooms canon-pressure overlay, the refreshed `rooms-bootstrap` v1.1 root, and the hydrated Wild Bunch first-party roots.
- Notes: This is a Harley-owned first-party Codex marketplace projection kept clean for a future permissive publication decision. It does not replace the source ledger in `sources/first_party/skills/house-skills/` and does not make retired, folded, reference-only, or deferred records active installable entries. `connector-safety` is projected here as a shared safety dependency for side-effecting connector/tool work, `github-operations` is projected here as the generic GitHub proof base skill, `github-superpowers` is projected here as the GitHub-facing compositional workflow skill, `codex-repo-receipts` is projected here as the durable repo-receipt skill, `rooms-canon-buster` is projected here as a Rooms canon-pressure overlay, and `rooms-bootstrap` is projected here as the refreshed first-turn Rooms router.

## Active imports

### Base and control plane

- `don-logan-boundary-v1` - `codex-marketplace/plugins/house-skills/skills/don-logan-boundary/v1/don-logan-boundary-v1/SKILL.md`
- `gpt-base-doctrine-v1.1` - `codex-marketplace/plugins/house-skills/skills/gpt-base-doctrine`
- `work-mode-router-v1` - `codex-marketplace/plugins/house-skills/skills/work-mode-router/v1/work-mode-router-v1/SKILL.md`
- `worker-dispatch-linear-v2` - `codex-marketplace/plugins/house-skills/skills/worker-dispatch-linear`
- `linear-v1.1` - `codex-marketplace/plugins/house-skills/skills/linear`
- `tps-reporting-v1` - `codex-marketplace/plugins/house-skills/skills/tps-reporting/v1/tps-reporting-v1/SKILL.md`
- `tps-ingress-v1` - `codex-marketplace/plugins/house-skills/skills/tps-ingress/v1/tps-ingress-v1/SKILL.md`
- `session-buster-v0.2` - `codex-marketplace/plugins/house-skills/skills/session-buster/v0.2/session-buster-v0.2/SKILL.md`
- `session-buster-ingress-v0.2` - `codex-marketplace/plugins/house-skills/skills/session-buster-ingress/v0.2/session-buster-ingress-v0.2/SKILL.md`
- `crew-v1` - `codex-marketplace/plugins/house-skills/skills/crew/v1/crew-v1/SKILL.md`
- `crew-buster-v1` - `codex-marketplace/plugins/house-skills/skills/crew-buster/v1/crew-buster-v1/SKILL.md`

### Adventures v1.1

- `adventures-project-doctrine-v1.1` - `codex-marketplace/plugins/house-skills/skills/adventures-project-doctrine/v1.1/adventures-project-doctrine-v1.1/SKILL.md`
- `adventures-bootstrap-v1.1` - `codex-marketplace/plugins/house-skills/skills/adventures-bootstrap/v1.1/adventures-bootstrap-v1.1/SKILL.md`
- `adventures-github-operations-v1.1` - `codex-marketplace/plugins/house-skills/skills/adventures-github-operations/v1.1/adventures-github-operations-v1.1/SKILL.md`
- `adventures-visual-preproduction-v1.1` - `codex-marketplace/plugins/house-skills/skills/adventures-visual-preproduction/v1.1/adventures-visual-preproduction-v1.1/SKILL.md`
- `adventures-storyboard-preflight-v1.1` - `codex-marketplace/plugins/house-skills/skills/adventures-storyboard-preflight/v1.1/adventures-storyboard-preflight-v1.1/SKILL.md`
- `adventures-visual-bible-creator-v1.1` - `codex-marketplace/plugins/house-skills/skills/adventures-visual-bible-creator/v1.1/adventures-visual-bible-creator-v1.1/SKILL.md`
- `adventures-visual-bible-interpreter-v1.1` - `codex-marketplace/plugins/house-skills/skills/adventures-visual-bible-interpreter/v1.1/adventures-visual-bible-interpreter-v1.1/SKILL.md`
- `adventures-image-qa-v1.1` - `codex-marketplace/plugins/house-skills/skills/adventures-image-qa/v1.1/adventures-image-qa-v1.1/SKILL.md`
- `adventures-asset-sheet-compiler-v1.1` - `codex-marketplace/plugins/house-skills/skills/adventures-asset-sheet-compiler/v1.1/adventures-asset-sheet-compiler-v1.1/SKILL.md`
- `adventures-frame-buster-v1.1` - `codex-marketplace/plugins/house-skills/skills/adventures-frame-buster/v1.1/adventures-frame-buster-v1.1/SKILL.md`

### Rooms

- `rooms-project-doctrine-v1` - `codex-marketplace/plugins/house-skills/skills/rooms-project-doctrine/v1/rooms-project-doctrine-v1/SKILL.md`
- `rooms-bootstrap-v1.1` - `codex-marketplace/plugins/house-skills/skills/rooms-bootstrap`
- `rooms-source-partitioning-v1` - `codex-marketplace/plugins/house-skills/skills/rooms-source-partitioning/v1/rooms-source-partitioning-v1/SKILL.md`
- `rooms-ambiguity-buster-v1` - `codex-marketplace/plugins/house-skills/skills/rooms-ambiguity-buster/v1/rooms-ambiguity-buster-v1/SKILL.md`
- `rooms-analogy-buster-v1` - `codex-marketplace/plugins/house-skills/skills/rooms-analogy-buster/v1/rooms-analogy-buster-v1/SKILL.md`
- `rooms-zoom-outs-buster-v1` - `codex-marketplace/plugins/house-skills/skills/rooms-zoom-outs-buster/v1/rooms-zoom-outs-buster-v1/SKILL.md`
- `rooms-character-investigation-v1` - `codex-marketplace/plugins/house-skills/skills/rooms-character-investigation/v1/rooms-character-investigation-v1/SKILL.md`
- `rooms-sheet-creator-v1` - `codex-marketplace/plugins/house-skills/skills/rooms-sheet-creator/v1/rooms-sheet-creator-v1/SKILL.md`

Retired, folded, reference-only, and deferred MARK-9 decisions remain in Linear ledgers and are not duplicated here.
