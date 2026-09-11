# MARK-373 Contracts and Routing Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/subagent-driven-development` (recommended) or `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Establish one unambiguous `.agents/contracts/` home for repository contracts and make `/using-superpowers-plus` the sole skill-composition router for repo-backed workflows.

**Architecture:** Move both human-readable and machine-readable repository contracts into `.agents/contracts/`; contract format does not determine custody. Update the canonical `repo-standards` source before regenerating installed copies. Portable stage skills select workflows, while local runbooks retain only repository-specific paths, commands, constraints, and acceptance evidence.

**Tech Stack:** Markdown, JSON, Python, pytest, repository generators.

**Spec:** `.agents/plans/2026-09-06-mark-373-operating-system.md`, extended by the human-approved unified-contract and sole-router decisions captured in this plan.

**Execution Strategy:** `subagent-driven-development` — the contract migration and routing cleanup are separable review units, but canonical-source edits must precede generated installed-skill refreshes.

## Global Constraints

- A contract is a contract regardless of serialization; every repo-level contract lives under `.agents/contracts/`.
- Delete `.agents/contracts/` after migration. Do not preserve a forwarding directory, duplicate copy, or compatibility contract.
- `.agents/doctrine/` contains policy and authority statements, not executable command declarations or format contracts.
- Skill-owned schemas and contracts remain colocated with their canonical skill when they are not repository-level contracts.
- `/using-superpowers-plus` remains the sole session bootstrap and skill-composition router.
- Local runbooks contain only repository-specific facts and constraints; they do not independently compose skills.
- Stage skills continue to own their portable workflow semantics and read the applicable local runbook after bootstrap routing.
- Edit canonical plugin skill sources first. Regenerate `.agents/skills/`; do not hand-edit generated installed copies.
- Preserve Draft PR #311. Do not run paid model evaluation and do not promote the PR Ready.

## Decision table

| Surface | Classification | Destination/action |
|---|---|---|
| `.agents/contracts/openai-agent-yaml.md` | repository-level human-readable contract | move to `.agents/contracts/openai-agent-yaml.md` |
| `.agents/contracts/skill-frontmatter.md` | repository-level human-readable contract | move to `.agents/contracts/skill-frontmatter.md` |
| `.agents/contracts/repo-standards-commands.json` | repository-level machine-readable contract | move to `.agents/contracts/repo-standards-commands.json` |
| `.agents/contracts/INDEX.md` | generated navigation | replace with generated `.agents/contracts/INDEX.md` |
| `.agents/doctrine/contracts.md` | custody/routing policy, not a contract | rename to `.agents/doctrine/contracts.md` and describe the unified boundary |
| skill-local schemas, authority maps, and result contracts | owner-local contracts | keep with their owning canonical skill |
| plugin bundle manifests and marketplace JSON | generated/configuration surfaces | keep with their current consumers |
| completed-plan JSON evidence | historical evidence | keep in completed-plan custody |

---

### Task 1: Move repository contracts into one boundary

**Files:**
- Move: `.agents/contracts/openai-agent-yaml.md` -> `.agents/contracts/openai-agent-yaml.md`
- Move: `.agents/contracts/skill-frontmatter.md` -> `.agents/contracts/skill-frontmatter.md`
- Move: `.agents/contracts/repo-standards-commands.json` -> `.agents/contracts/repo-standards-commands.json`
- Move: `.agents/doctrine/contracts.md` -> `.agents/doctrine/contracts.md`
- Modify: `.devin/rules/contracts.md`
- Modify: `.agents/docs/AGENTS.md`
- Modify: `.agents/doctrine/skill-standards-policy.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/references/codex-marketplace-compatibility.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-skills/references/skill-authoring-checklist.md`
- Modify: any tracked historical Markdown link found by the exact old-path scan
- Test: `tests/test_repo_standards.py`
- Test: `tests/test_workflow_contracts.py`

**Interfaces:**
- Consumes: existing contract contents and repository index/link generators.
- Produces: one `.agents/contracts/` boundary with no live or historical link to `.agents/contracts/` or `.agents/contracts/repo-standards-commands.json`.

- [x] **Step 1: Add RED custody assertions.** Assert that all three repository contracts exist under `.agents/contracts/`, both former contract homes are absent, `.agents/doctrine/contracts.md` scopes the unified boundary, and tracked non-plan live surfaces contain no old path.
- [x] **Step 2: Verify RED.** Run the new focused tests and confirm they fail only because the old paths still exist.
- [x] **Step 3: Move the authored files with Git-aware moves.** Preserve their contents except for headings or scope text needed to describe the unified contract boundary.
- [x] **Step 4: Update canonical live references.** Repoint the Devin rule, docs router, skill standards, compatibility reference, and writing-skills checklist to `.agents/contracts/`.
- [x] **Step 5: Heal historical links.** Run `py -3 tools/heal_archive_links.py --apply`; inspect every resulting historical-plan/spec edit and retain only deterministic path rewrites.
- [x] **Step 6: Regenerate navigation.** Run `py -3 tools/run.py mesh --apply`; verify `.agents/contracts/INDEX.md` exists and `.agents/contracts/` is absent.
- [x] **Step 7: Prove the migration.** Run the focused custody tests, `py -3 tools/check_archive_links.py --check`, and `rg -n "\.agents/contracts|\.agents/doctrine/repo-standards-commands\.json" . --glob "!evals/**" --glob "!.git/**"`; expected result is no stale reference outside intentionally quoted migration history in this plan.
- [x] **Step 8: Mark Task 1 complete and commit normally.** Stage only the contract migration and deterministic link/index updates; let the tracked hook provide the broad gate.

### Task 2: Teach portable repo standards the unified contract path and sole-router architecture

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/SKILL.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-runbook-standard.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-shape-standard.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-shape-manifest.json`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/repo_standards.py`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/pre-commit`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/contributing-template.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/REVIEW.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/repo-runbook-policy.md`
- Test: `tests/test_repo_standards.py`
- Test: `tests/test_workflow_contracts.py`

**Interfaces:**
- Consumes: Task 1's `.agents/contracts/repo-standards-commands.json` path and the existing `/using-superpowers-plus` bootstrap contract.
- Produces: portable scaffolds and validators that install the unified contract path and delegate skill composition to the sole router.

- [x] **Step 1: Add RED portable tests.** Assert the shape manifest, validator constant, hook template, and reference docs use `.agents/contracts/repo-standards-commands.json`. Assert portable contributor/review/runbook templates enter through `/using-superpowers-plus` and do not independently prescribe a multi-skill invocation stack.
- [x] **Step 2: Verify RED.** Run the owned repo-standards tests and confirm failures identify old contract paths and duplicated routing.
- [x] **Step 3: Change the command-contract seam.** Update the manifest dependency, validator lookup, hook template, and explanatory references to the unified path without weakening exact hook-template validation.
- [x] **Step 4: Correct portable workflow ownership.** Replace `repo-standards -> repo-worker-base -> local runbook -> selected Superpowers lane` and direct stage-skill invocation tables with `using-superpowers-plus -> routed owners -> local runbook`. Keep `repo-standards` responsible only for shape/runbook alignment after routing.
- [x] **Step 5: Thin portable templates.** Templates may name `/using-superpowers-plus` as the entrypoint and describe repository-specific evidence obligations, but must not recreate bootstrap composition.
- [x] **Step 6: Run focused canonical-source tests.** Run the repo-standards and workflow routing tests before regeneration.
- [x] **Step 7: Regenerate installed skills.** Run `py -3 tools/run.py installed-skills --apply`, then verify canonical and generated copies match and contain no old command-contract path.
- [x] **Step 8: Mark Task 2 complete and commit normally.** Stage canonical source, generated installed copies, provenance, and owned tests; let the hook provide the broad gate.

### Task 3: Thin repository entrypoints and runbooks to local deltas

**Files:**
- Modify: `CONTRIBUTING.md`
- Modify: `REVIEW.md`
- Modify: `.agents/doctrine/repo-runbook-policy.md`
- Modify: `.agents/runbooks/implementing.md`
- Modify: `.agents/runbooks/planning.md`
- Modify: `.agents/runbooks/testing.md`
- Modify: `.agents/runbooks/pr.md`
- Modify: `.agents/runbooks/security.md`
- Modify: `.agents/runbooks/code-review.md`
- Modify: `.agents/runbooks/code-style.md`
- Modify: `.agents/runbooks/repo-doctrine.md`
- Modify: `.agents/runbooks/skill-authoring.md`
- Test: `tests/test_workflow_contracts.py`

**Interfaces:**
- Consumes: Task 2's portable sole-router architecture.
- Produces: local guidance that adds marketplace facts without selecting or sequencing bootstrap/owner skills.

- [x] **Step 1: Add RED local-routing tests.** Enumerate the live entrypoints/runbooks above. Permit one `/using-superpowers-plus` entrypoint instruction; reject headings or prose that independently instruct readers to invoke multiple workflow skills. Do not reject skill names used as ownership links or factual references.
- [x] **Step 2: Verify RED.** Run the routing test and record which files currently duplicate composition.
- [x] **Step 3: Thin contributor and review entrypoints.** Keep stage descriptions and repository review concerns, but route skill selection once through `/using-superpowers-plus`.
- [x] **Step 4: Thin stage runbooks.** Remove `Skills to Invoke`/`Routing to skills` composition sections and generic TDD, planning, review, debugging, security-profile, or publication workflows already owned by skills. Keep repository paths, commands, generated-source rules, Draft-CI behavior, and marketplace-specific acceptance checks.
- [x] **Step 5: Preserve specialised local deltas.** Keep skill-authoring paths/scaffold commands, marketplace regeneration behavior, repository test locations, local security surfaces, and local PR/CI commands. Skill names may identify the portable owner but must not create a second invocation sequence.
- [x] **Step 6: Verify semantic completeness.** Compare each thinned runbook with its pre-edit version and prove every removed generic rule is owned by `/using-superpowers-plus` or the routed stage skill; restore any repository-specific fact that has no owner.
- [x] **Step 7: Run focused routing tests and a literal scan.** Search live entrypoints/runbooks for imperative `invoke /...` or multi-skill routing lists; adjudicate every remaining hit.
- [x] **Step 8: Regenerate navigation if file headings or links changed.** Run `py -3 tools/run.py mesh --apply` only when required by the edited surfaces.
- [x] **Step 9: Mark Task 3 complete and commit normally.** Stage the local overlays and tests; let the hook provide the broad gate.

### Task 4: Remove unverifiable pressure-campaign residue

**Files:**
- Keep: `tests/pressure/workflow-contracts/prompts/**`
- Keep: `tests/pressure/workflow-contracts/campaign.json`
- Keep and thin: `tests/pressure/workflow-contracts/README.md`
- Keep: `tests/pressure/workflow-contracts/ci-parity.md`
- Keep: `tests/pressure/workflow-contracts/workflow-inventory.md`
- Keep and rename: `tests/pressure/workflow-contracts/pressure-scan-dispositions.json` -> `tests/pressure/workflow-contracts/pressure-scan-decisions.json`
- Delete: `tests/pressure/workflow-contracts/pressure-scan.json`
- Delete: `tests/pressure/workflow-contracts/pressure-scan.md`
- Delete: `tests/pressure/workflow-contracts/campaign-meta.json`
- Delete: `tests/pressure/workflow-contracts/scores/**`
- Delete: `tests/pressure/workflow-contracts/results.md`
- Delete: `tests/pressure/workflow-contracts/red-baseline.md`
- Delete locally: ignored `tests/pressure/workflow-contracts/runs/**`
- Modify: `tests/test_workflow_contracts.py`
- Modify: `.agents/plans/2026-09-06-mark-373-operating-system.md`
- Modify: `.agents/plans/2026-09-06-mark-373-operating-system.checkpoint.md`

**Interfaces:**
- Consumes: reusable campaign inputs and the current scanner.
- Produces: a pressure-test surface containing future-use assets and current checked controls, with no unverifiable historical-result paperwork.

- [x] **Step 1: Add RED custody tests.** Require prompts, campaign configuration, parity analysis, workflow inventory, and scanner decisions; reject committed run metadata, scores, results prose, RED receipts, and reproducible raw scanner output.
- [x] **Step 2: Verify RED.** Run the focused workflow-contract tests and confirm the old result artifacts cause the expected failure.
- [x] **Step 3: Remove committed residue.** Delete the classified `delete_now` files and rename the human disposition registry to `pressure-scan-decisions.json`.
- [x] **Step 4: Make scanner validation dynamic.** Run the scanner in tests and validate its current candidates against the retained human decision registry instead of loading committed raw output.
- [x] **Step 5: Thin campaign documentation.** Keep only future execution instructions, reusable inputs, custody rules, and current parity/inventory pointers. Remove historical Quorum, model-run, score, hash, and unavailable-evidence narratives.
- [x] **Step 6: Remove stale plan/checkpoint claims.** Delete references that treat removed scores, metadata, summaries, or external tooling as durable evidence. Preserve only the decision that paid evaluation is retired and no behavioral baseline is claimed.
- [x] **Step 7: Delete ignored local runs.** Resolve the exact ignored path under this worktree, verify it is inside `tests/pressure/workflow-contracts/runs/`, and remove it without touching external repositories or other worktrees.
- [x] **Step 8: Regenerate indexes and prove custody.** Run `py -3 tools/run.py mesh --apply`, focused workflow-contract tests, `git status --ignored --short tests/pressure/workflow-contracts`, and a literal scan for removed artifact names.
- [x] **Step 9: Mark Task 4 complete and commit normally.** Stage the cleanup, tests, plan, checkpoint, and generated indexes; let the hook provide the broad gate.

### Task 5: Close the sub-slice and publish review evidence

**Files:**
- Modify: `.agents/plans/2026-09-11-mark-373-contracts-and-routing.md`
- Modify: `.agents/plans/2026-09-06-mark-373-operating-system.checkpoint.md`
- Modify: PR #311 body

**Interfaces:**
- Consumes: Tasks 1-4 committed outputs and hook evidence.
- Produces: an honest Draft PR and durable resume state for human review.

- [x] **Step 1: Run final falsification scans.** Confirm one `.agents/contracts/` tree, no former contract directory under `.agents/docs/`, no command contract under doctrine, no stale old-path links, and no local runbook-owned multi-skill composition.
- [x] **Step 2: Review the complete diff.** Check contract custody, generated-source direction, consumer portability, local-rule preservation, and absence of compatibility duplicates.
- [x] **Step 3: Update plan and checkpoint truthfully.** Record only current state, decisive validation, and evidence boundaries; do not recreate a chronological Git/test receipt.
- [x] **Step 4: Commit normally.** Let the tracked pre-commit apply/check gate validate the exact staged state; do not duplicate the broad gate before or after a successful commit.
- [x] **Step 5: Push the existing branch and update Draft PR #311.** Summarize the unified contract boundary and sole-router cleanup. Keep the PR Draft.
- [x] **Step 6: Verify publication.** Confirm local/remote head equality, clean worktree, PR base `main`, and Draft state.

## Acceptance evidence

- `.agents/contracts/` is the only repository-level contract directory and contains both Markdown and JSON contracts.
- The former contract directory under `.agents/docs/` and the former command declaration under `.agents/doctrine/` are absent.
- Contract consumers, canonical repo-standards source, generated installed skills, hooks, tests, indexes, and historical links resolve the new paths.
- `/using-superpowers-plus` is the sole bootstrap/composition router in portable standards and local runbooks.
- Local runbooks preserve repository-specific commands, paths, exceptions, and acceptance evidence without duplicating portable workflow semantics.
- Focused tests prove path migration and routing ownership; normal hooked commits provide broad validation for each committed state.
- PR #311 remains Draft and contains no paid evaluation rerun.

## Plan-readiness self-review

- Dependency order is explicit: contract destination first, portable source second, local overlays third, evidence cleanup fourth, publication last.
- Canonical source and generated copies are separated.
- Historical-link migration and index regeneration are explicit; no compatibility folder is allowed.
- Routing tests distinguish imperative composition from factual owner references to avoid false positives.
- Repository-specific facts receive an explicit preservation check before generic guidance is removed.
- No consequential choice is deferred to the executor.

**Plan-readiness rating:** 9.3/10.
