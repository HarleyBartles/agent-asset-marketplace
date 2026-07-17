# House Skills Provenance

## cleanup-custody

- Source path: `sources/first_party/skills/cleanup-custody/SKILL.md`
- Public identity: `cleanup-custody`
- Provenance/history only: legacy profanity-bearing cleanup-skill naming
- Scope: cleanup-custody only
- Notes: Keep the active public source name neutral. Do not use the legacy profanity-bearing name as the primary public surface name.

## skill-validator

- Source path: `sources/first_party/skills/skill-validator/SKILL.md`
- Public identity: `skill-validator`
- Provenance/history only: MARK-21 skill maintenance House Skills source slice (retired)
- Scope: skill validation
- Notes: Retired legacy skill helper. Skill validation is now covered by the repo skill standards at `docs/skill-standards-policy.md` and the canonical validation entrypoints `tools/check_marketplace.py` (CI gate) and `tools/rebuild_marketplace.py` (rebuild). This record exists only for provenance audit of the retired source path.

## skill-packager

- Source path: `sources/first_party/skills/skill-packager/SKILL.md`
- Public identity: `skill-packager`
- Provenance/history only: MARK-21 skill maintenance House Skills source slice (retired)
- Scope: skill packaging
- Notes: Retired legacy skill helper. Skill packaging is now handled by `tools/package_skill_zips.py` and the deterministic marketplace generation pipeline. This record exists only for provenance audit of the retired source path.

## connector-safety

- Source path: `sources/first_party/skills/connector-safety`
- Public identity: `connector-safety`
- Provenance/history: installed connector-safety package landed via WILL-274; v1.1 zip update
- Ownership: Harley-authored first-party House skill
- Scope: connector and tool safety blocks, discover-before-mutation flow, exact-state guarded writes, blocked-write recovery, narrow retries, invalid-attempt handling, post-create read chains, and safe-action reporting
- Notes: Canonical source now lives in `sources/first_party/skills/connector-safety/`. `agents/openai.yaml` was copied into repo source control and retains the repository policy fields while adopting the clearer interface description and visual hints from the zip. `assets/icon.svg` was not included because the zip did not provide it. The current update sharpens the connector safety doctrine with mandatory discover -> read -> write -> verify guidance while preserving the existing blocked-write and exact-state guard rules.

## adventures-project-doctrine-v1

- Source path: `sources/first_party/skills/adventures-project-doctrine/v1/adventures-project-doctrine-v1/SKILL.md`
- Public identity: `adventures-project-doctrine-v1`
- Provenance/history only: MARK-22 prep payload for Adventures House Skills survivor import
- Scope: Adventures project doctrine
- Notes: Imported as the primary Adventures survivor. Preserves shared doctrine, connector posture, visual canon, and resource discipline while stripping retired image-generation framing, deck/PPTX, receipt, and standalone GitHub operations residue from the active House Skills lane.

## base-doctrine

- Source path: `sources/first_party/skills/base-doctrine`
- Public identity: `base-doctrine`
- Provenance/history only: MARK-30 base and control plane update
- Scope: cross-runtime shared doctrine
- Notes: Imported as the shared doctrine store for cross-runtime House Skills, including the bounded read-loop doctrine and the updated source/reference routing table.

## bootstrap-router

- Source path: `sources/first_party/skills/bootstrap-router`
- Public identity: `bootstrap-router`
- Provenance/history: MARK-161 bootstrap-router seed contract from the attached GPT bootstrap package
- Scope: first-turn bootstrap routing and request classification
- Notes: Imported from the attached GPT bootstrap package and adapted to the House Skills lane so first-turn routing stays local, ordinary-chat keeps an escape hatch, and coding work routes through linear-issue-shaping.

## rooms-image-sidecars

- Source path: `sources/first_party/skills/rooms-image-sidecars/v0.1/rooms-image-sidecars-v0.1/SKILL.md`
- Public identity: `rooms-image-sidecars`
- Provenance/history only: MARK-23 prep payload for Rooms House Skills survivor import
- Scope: Rooms image sidecar preparation
- Notes: Imported as the primary Rooms survivor. Provides GPT-side starter packet guidance for image evidence before Albert/Pit ingestion. No standalone GitHub mechanics, canon busters, or adjacent Rooms residue were imported.

## rooms-canon-buster

- Source path: `sources/first_party/skills/rooms-canon-buster` (retired 2026-07-16)
- Public identity: `rooms-canon-buster`
- Provenance/history only: MARK-97 attached rooms canon buster zip update (retired)
- Ownership: Harley-authored first-party House skill
- Scope: Rooms canon pressure checks and lawful canon/item adjustment
- Notes: Retired as part of the buster framework consolidation. The Rooms canon gate function now lives in `rooms-risk-gates` under `references/rooms-canon-gate.md`. This record exists only for provenance audit of the retired source path.

## asset-market

- Source path: `sources/first_party/skills/asset-market`
- Public identity: `asset-market`
- Provenance/history: MARK-109 saved GPT skill zip source package
- Scope: marketplace source and pack acquisition
- Notes: Imported from the saved zip as the exact-fidelity source staging root for marketplace pulls, including pack-root resolution and per-skill install-unit expansion.

## linear-issue-compactor

- Source path: `sources/first_party/skills/linear-issue-compactor`
- Public identity: `linear-issue-compactor`
- Provenance/history only: MARK-135 Linear issue compactor skill
- Scope: Linear issue compaction and connector-readable issue bodies
- Notes: Historical/provenance-only record for the retired Linear compaction skill. The active compact issue-shape doctrine now lives in `linear-issue-shaping`, and any remaining mention here exists only so the retired source path and decision can be audited.

## boring-loop

- Source path: `sources/first_party/skills/boring-loop` (retired 2026-07-16)
- Public identity: `boring-loop`
- Provenance/history only: MARK-152 Boring Loop beta first-party source (retired)
- Ownership: Harley-owned first-party House skill
- Scope: loop cadence, readiness and false-green prevention, parent/child DoD coverage, queue grooming, next boring move selection, route-to-specialist guidance
- Notes: Retired as part of the buster framework consolidation. The boring-loop function is now covered by `verification-before-completion` and `repo-worker-base` for finish-line enforcement. This record exists only for provenance audit of the retired source path.

## github-operations

- Source path: `sources/first_party/skills/github-operations`
- Public identity: `github-operations`
- Provenance/history: MARK-142 GitHub operations zip import
- Ownership: Harley-owned first-party House skill
- Scope: GitHub evidence, PR review routing, and publication proof
- Notes: First-party GitHub proof skill for verifying GitHub repository evidence, publication proof, mergeability, and closure claims. The native review write reference keeps same-account connector use on `COMMENT` reviews instead of trying to force `REQUEST_CHANGES`. The canonical first-party source now lives in `sources/first_party/skills/github-operations/`; House Skills projects that source rather than owning it.

## linear-superpowers

- Source path: `sources/first_party/skills/linear-superpowers`
- Public identity: `linear-superpowers`
- Provenance/history only: MARK-139 Linear Superpowers compositional skill
- Scope: Linear issue and track shaping with smallest-applicable workflow selection
- Notes: Retired first-party compositional router. The active compact issue-shape doctrine and Linear routing now live in `linear-issue-shaping`, and the workflow-selection behavior is owned by `using-superpowers` and `work-mode-router`. This record exists only for provenance audit of the retired source path.

## github-superpowers

- Source path: `sources/first_party/skills/github-superpowers`
- Public identity: `github-superpowers`
- Provenance/history only: MARK-143 GitHub Superpowers compositional skill
- Scope: GitHub-facing workflow selection, proof boundaries, and branch-closeout routing
- Notes: Retired first-party compositional router. GitHub proof, publication, merge, and final-main verification remain in `github-operations`, and workflow selection is owned by `using-superpowers` and `work-mode-router`. This record exists only for provenance audit of the retired source path.

## unslop-superpowers

- Source path: `sources/first_party/skills/unslop-superpowers`
- Public identity: `unslop-superpowers`
- Provenance/history only: MARK-144 Unslop Superpowers compositional guard skill
- Scope: repo-specific anti-slop controls, profile-aware workflow shaping, and the narrow direct-to-main escape hatch for profile-only updates
- Notes: Retired first-party compositional guard. Repo-specific anti-slop profile work is now routed to `unslop-plus` or `unslop`, and workflow selection is owned by `using-superpowers` and `work-mode-router`. This record exists only for provenance audit of the retired source path.

## context-safety

- Source path: `sources/first_party/skills/context-safety`
- Public identity: `context-safety`
- Provenance/history: MARK-310 context safety first-party skill
- Ownership: Harley-owned first-party House skill
- Scope: large text write safety, bounded composition, and atomic replacement
- Notes: First-party safety skill for large generated or edited text files. The canonical source is a directory-level skill spec with `SKILL.md` and `agents/openai.yaml`, and it teaches bounded composition, safe staging, and atomic replacement for large writes.

## risk-gates

- Source path: `sources/first_party/skills/risk-gates`
- Public identity: `risk-gates`
- Provenance/history: 2026-07-16 buster framework consolidation
- Ownership: Harley-owned first-party House skill
- Scope: consolidated pre-action risk gate router with generic and Rooms-specific gate references
- Notes: Imported as the consolidated risk-gates skill that retires and replaces the six MARK-19 core generic buster source records (buster-framework, ambiguity-buster, boring-buster, invariant-buster, analogy-buster, canon-buster) plus the Rooms gate overlays (rooms-ambiguity-buster, rooms-analogy-buster, rooms-canon-buster, rooms-zoom-outs-buster), crew/crew-buster, boring-loop, and session-buster/session-buster-ingress. Generic gate references live under `references/gates/`; Rooms-specific gate profiles live in `rooms-risk-gates/references/`.

## skill-handoff

- Source path: `sources/first_party/skills/skill-handoff`
- Public identity: `skill-handoff`
- Provenance/history only: MARK-109 saved GPT skill zip source package (retired)
- Scope: skill package handoff cadence
- Notes: Retired legacy skill helper. Skill handoff is now covered by `writing-plans` plus the repo skill spec where appropriate. This record exists only for provenance audit of the retired source path.

## skill-installer

- Source path: `sources/first_party/skills/skill-installer`
- Public identity: `skill-installer`
- Provenance/history only: MARK-109 saved GPT skill zip source package (retired)
- Scope: skill installation handoff orchestration
- Notes: Retired legacy skill helper. Skill installation is now handled by `tools/install_agent_skills.py` and the deterministic marketplace pipeline. This record exists only for provenance audit of the retired source path.

## rooms-bootstrap

- Source path: `sources/first_party/skills/rooms-bootstrap` (retired 2026-07-16)
- Public identity: `rooms-bootstrap`
- Provenance/history: MARK-97 rooms bootstrap zip update
- Scope: Rooms first-read router
- Notes: Retired as part of MARK-334. The Rooms first-read router function was merged into `rooms-project-doctrine`. This record exists only for provenance audit of the retired source path.
## wild-bunch-project-doctrine-v1

- Source path: `sources/first_party/skills/wild-bunch-project-doctrine`
- Public identity: `wild-bunch-project-doctrine`
- Provenance/history: MARK-85 Wild Bunch first-party source hydration from attached zip
- Ownership: Harley-authored first-party House skill
- Scope: Wild Bunch project posture and repo sensitivity
- Notes: Hydrated from the authoritative attached zip and projected unchanged into the House Skills lane.

## wild-bunch-domain-modeling-v1

- Source path: `sources/first_party/skills/wild-bunch-domain-modeling`
- Public identity: `wild-bunch-domain-modeling`
- Provenance/history: MARK-85 Wild Bunch first-party source hydration from attached zip
- Ownership: Harley-authored first-party House skill
- Scope: Wild Bunch gameplay state, GameSession boundaries, clue and journal flows, travel, horses, and hidden culprit truth
- Notes: Hydrated from the authoritative attached zip and projected unchanged into the House Skills lane.

## wild-bunch-dotnet-architecture-v1

- Source path: `sources/first_party/skills/wild-bunch-dotnet-architecture`
- Public identity: `wild-bunch-dotnet-architecture`
- Provenance/history: MARK-85 Wild Bunch first-party source hydration from attached zip
- Ownership: Harley-authored first-party House skill
- Scope: Wild Bunch C#/.NET architecture guardrails for domain ownership, mutation routes, persistence, and framework leakage
- Notes: Hydrated from the authoritative attached zip and projected unchanged into the House Skills lane.

## wild-bunch-browser-game-v1

- Source path: `sources/first_party/skills/wild-bunch-browser-game`
- Public identity: `wild-bunch-browser-game`
- Provenance/history: MARK-85 Wild Bunch first-party source hydration from attached zip
- Ownership: Harley-authored first-party House skill
- Scope: Wild Bunch browser delivery, HUD design, Phaser/TypeScript/Vite, DOM overlays, playtest evidence, and browser QA
- Notes: Hydrated from the authoritative attached zip and projected unchanged into the House Skills lane.

## wild-bunch-worker-verification-v1

- Source path: `sources/first_party/skills/wild-bunch-worker-verification`
- Public identity: `wild-bunch-worker-verification`
- Provenance/history: MARK-85 Wild Bunch first-party source hydration from attached zip
- Ownership: Harley-authored first-party House skill
- Scope: Wild Bunch worker returns, PRs, commits, validation notes, and completion verification
- Notes: Hydrated from the authoritative attached zip and projected unchanged into the House Skills lane.

## tps-reporting

- Source path: `sources/first_party/skills/tps-reporting` (retired 2026-07-16)
- Public identity: `tps-reporting`
- Provenance/history only: MARK-30 base and control plane (retired)
- Ownership: Harley-authored first-party House skill
- Scope: producer-side report hygiene — partition reports, worker returns, Linear/Codex status notes, verification summaries, and continuity notes so claims do not become truth
- Notes: Retired as part of the tps skill retirement. The report hygiene function now lives in `base-doctrine` under `references/report-hygiene.md`. This record exists only for provenance audit of the retired source path.

## tps-ingress

- Source path: `sources/first_party/skills/tps-ingress` (retired 2026-07-16)
- Public identity: `tps-ingress`
- Provenance/history only: MARK-30 base and control plane (retired)
- Ownership: Harley-authored first-party House skill
- Scope: consumer-side feedback verification — evaluate review, verifier, worker, issue, PR, automated-check, or external feedback before it becomes action, scope, evidence, or closure posture
- Notes: Retired as part of the tps skill retirement. The feedback verification function now lives in `risk-gates` under `references/gates/feedback-gate.md`. This record exists only for provenance audit of the retired source path.

## House Skills plugin projection

- Bundle name: `house-skills`
- Bundle version: `1.0.0`
- Marketplace source: `.agents/plugins/marketplace.json`
- Plugin manifest: `codex-marketplace/plugins/house-skills/.codex-plugin/plugin.json`
- Bundle skill: `codex-marketplace/plugins/house-skills/skills/house-skills`
- Bundle manifest: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Source map: `codex-marketplace/plugins/house-skills/references/source-map.md`
- Generator: `tools/generate_marketplace.py`
- Validator: `tools/validate_marketplace.py`
- Projection scope: reviewed active House Skills only, grouped into base/control plane, Adventures v1.1, Rooms, and Wild Bunch, plus the shared `connector-safety` component in the base/control-plane lane, the `github-operations` GitHub proof skill, the `risk-gates` consolidated pre-action risk gate router, the `rooms-risk-gates` Rooms-specific gate overlay, and the hydrated Wild Bunch first-party roots.
- Notes: This is a Harley-owned first-party Codex marketplace projection kept clean for a future permissive publication decision. It does not replace the source ledger in `sources/first_party/skills/house-skills/` and does not make retired, folded, reference-only, or deferred records active installable entries. `connector-safety` is projected here as a shared safety dependency for side-effecting connector/tool work, `github-operations` is projected here as the generic GitHub proof base skill, `risk-gates` is projected here as the consolidated pre-action risk gate router, and `rooms-risk-gates` is projected here as the Rooms-specific gate overlay.

## Active imports

### Base and control plane

- `don-logan-boundary-v1` - `sources/first_party/skills/don-logan-boundary/v1/don-logan-boundary-v1/SKILL.md`
- `base-doctrine` - `sources/first_party/skills/base-doctrine`
- `work-mode-router-v1` - `sources/first_party/skills/work-mode-router/v1/work-mode-router-v1/SKILL.md`
- `linear-issue-shaping-v1` - `sources/first_party/skills/linear-issue-shaping`
- `using-linear-v1` - `sources/first_party/skills/using-linear`
- `risk-gates` - `sources/first_party/skills/risk-gates/SKILL.md`

### Adventures v1.1

- `adventures-project-doctrine-v1.1` - `sources/first_party/skills/adventures-project-doctrine/v1.1/adventures-project-doctrine-v1.1/SKILL.md`
- `adventures-bootstrap-v1.1` - `sources/first_party/skills/adventures-bootstrap/v1.1/adventures-bootstrap-v1.1/SKILL.md`
- `adventures-github-operations-v1.1` - `sources/first_party/skills/adventures-github-operations/v1.1/adventures-github-operations-v1.1/SKILL.md`
- `adventures-visual-preproduction-v1.1` - `sources/first_party/skills/adventures-visual-preproduction/v1.1/adventures-visual-preproduction-v1.1/SKILL.md`
- `adventures-storyboard-preflight-v1.1` - `sources/first_party/skills/adventures-storyboard-preflight/v1.1/adventures-storyboard-preflight-v1.1/SKILL.md`
- `adventures-visual-bible-creator-v1.1` - `sources/first_party/skills/adventures-visual-bible-creator/v1.1/adventures-visual-bible-creator-v1.1/SKILL.md`
- `adventures-visual-bible-interpreter-v1.1` - `sources/first_party/skills/adventures-visual-bible-interpreter/v1.1/adventures-visual-bible-interpreter-v1.1/SKILL.md`
- `adventures-image-qa-v1.1` - `sources/first_party/skills/adventures-image-qa/v1.1/adventures-image-qa-v1.1/SKILL.md`
- `adventures-asset-sheet-compiler-v1.1` - `sources/first_party/skills/adventures-asset-sheet-compiler/v1.1/adventures-asset-sheet-compiler-v1.1/SKILL.md`
- `adventures-frame-buster-v1.1` - `sources/first_party/skills/adventures-frame-buster/v1.1/adventures-frame-buster-v1.1/SKILL.md`

### Rooms

- `rooms-project-doctrine-v1` - `sources/first_party/skills/rooms-project-doctrine/v1/rooms-project-doctrine-v1/SKILL.md`
- `rooms-risk-gates` - `sources/first_party/skills/rooms-risk-gates/SKILL.md`
- `rooms-character-investigation-v1` - `sources/first_party/skills/rooms-character-investigation/v1/rooms-character-investigation-v1/SKILL.md`
- `rooms-sheet-creator-v1` - `sources/first_party/skills/rooms-sheet-creator/v1/rooms-sheet-creator-v1/SKILL.md`

Retired, folded, reference-only, and deferred MARK-9 decisions remain in Linear ledgers and are not duplicated here.
