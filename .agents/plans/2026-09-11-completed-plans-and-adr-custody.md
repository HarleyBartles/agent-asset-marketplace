# Completed Plans and ADR Custody Implementation Plan

**Goal:** Remove completed plans from the tracked repository, preserve a verified off-repo convenience archive, and establish ADRs as the durable home for architecture decisions.

**Architecture:** In-flight plans remain committed under `.agents/plans/`. A portable repo-standards archive command copies completed plans to the repository's protected off-repo cold-store lane with a hash manifest, verifies the copy, then permits removal from Git. Durable decisions extracted from historical plans are represented as numbered ADRs under `.agents/docs/adr/`; the tracked tree does not preserve a mutable completed-plan archive.

**Tech Stack:** Python, Markdown, JSON, pytest, existing marketplace and mesh generators.

**Execution Strategy:** `manual` — custody, migration, and ADR adjudication share one repository-wide invariant.

## Global Constraints

- Keep Draft PR #311 Draft; do not run Quorum or paid-model evaluation.
- Archive only `.agents/plans/completed/` in this slice. Completed specs remain until a separate custody decision determines whether each is an ADR candidate or non-durable scratch.
- Use `Z:/_agent-scratch/agent-asset-marketplace/archive/completed-plans/` as the exact cold-store destination for this migration.
- Archive copies are convenience retrieval material. Git history remains the immutable receipt.
- The archive command must fail before deletion when source hashes, copied files, or its manifest do not agree.
- Durable decisions must be expressed as ADRs or current doctrine/runbooks before their source plans leave the tracked tree.

### Task 1: Define portable completed-plan cold-store custody

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/scratch-workspace-policy.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/completed-plans.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/completed-plans-rule.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-shape-manifest.json`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-shape-standard.md`
- Test: `tests/test_repo_standards.py`

- [x] Add failing structural tests that reject tracked completed-plan directories as the repository completion home and require an explicit off-repo archive convention.
- [x] Replace the portable completed-plan template/rule with the off-repo lifecycle; retain no consumer-specific paths.
- [x] Extend scratch policy and validation vocabulary with a protected `archive/completed-plans/` lane separate from disposable branch scratch.
- [x] Run focused repo-standards tests.

### Task 2: Implement verified archive and cleanup mechanics

**Files:**
- Create: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/archive_completed_plans.py`
- Modify: relevant repo-standards script validation/manifest surfaces
- Modify: `tools/check_archive_links.py`
- Modify: `tools/heal_archive_links.py`
- Test: `tests/test_repo_standards.py`
- Test: targeted archive-link tests

- [x] Add failing tests for copy-only `--check`, deterministic manifest generation, hash verification, and refusal to delete a mismatched source/archive pair.
- [x] Implement the generic archive command with `--check` and explicit `--apply`; do not delete repository files itself.
- [x] Retire tracked-completed-directory assumptions from link healing/checking and mesh shape validation.
- [x] Run focused archive and standards tests.

### Task 3: Establish ADR log and extract durable decisions

**Files:**
- Create: `adr/README.md`
- Create: `adr/0001-plugin-first-marketplace-source.md`
- Create: `adr/0002-derived-agent-mesh.md`
- Create: `adr/0003-off-repo-completed-plan-custody.md`
- Modify: `.agents/doctrine/completed-plans.md`
- Modify: `.agents/doctrine/plans.md`
- Modify: `.agents/runbooks/completing-plans.md`
- Modify: `AGENTS.md`

- [x] Add focused tests that require a root `adr/` log, numbered records, and current plan doctrine that does not claim completed plans stay tracked.
- [x] Write only decisions that still constrain current operation: plugin-first source custody, derived agent-mesh navigation, and off-repo completed-plan custody. Cite historical plan names as non-authoritative origin context and current doctrine/source as present authority.
- [x] Replace the tracked `completed/` lifecycle with archive-then-remove mechanics and a requirement to promote enduring decisions before plan removal.
- [x] Run doctrine/runbook and ADR structural tests.

### Task 4: Archive this repository's completed plans

**Files:**
- Remove from Git after verified copy: `.agents/plans/completed/**`
- Modify/regenerate: `.agents/plans/INDEX.md`, `.agents/plans/INDEX.json`, mesh and repo-index outputs

- [x] Inventory the exact tracked completed-plan file set and generate the archive manifest at the approved cold-store path.
- [x] Verify every archive file hash against its tracked source before removal.
- [x] Remove the complete tracked `.agents/plans/completed/` tree with Git-aware deletion; do not remove `.agents/specs/completed/`.
- [x] Regenerate indexes and prove no active tracked references still require the completed-plan directory.

### Task 5: Verify, publish, and record evidence

**Files:**
- Modify: this plan
- Modify: `.agents/plans/2026-09-06-mark-373-operating-system.checkpoint.md`
- Modify: PR #311 body

- [x] Run focused archive, repo-standards, workflow-contract, and generated-surface suites.
- [x] Run the normal hooked commit gate; push the existing branch.
- [x] Update the checkpoint and Draft PR with exact archive count/path, ADR inventory, validation evidence, and any evidence boundary.
- [x] Confirm clean local/remote equality, base `main`, and Draft status.

## Acceptance Evidence

- No tracked `.agents/plans/completed/` directory remains.
- The off-repo archive has a deterministic manifest and byte-hash parity with every removed plan.
- New consumer repos receive a safe archive-then-remove lifecycle rather than a tracked completed-plan archive.
- `adr/` contains a discoverable numbered ADR log with only currently durable decisions.
- Current doctrine, templates, runbooks, validators, and generated indexes do not contradict the new custody model.
