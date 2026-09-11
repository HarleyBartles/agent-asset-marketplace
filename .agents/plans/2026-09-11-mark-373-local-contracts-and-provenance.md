# MARK-373 Local Contracts and Provenance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove obsolete prefix-based local-skill semantics, give repo-resident unslop profiles contract custody, make Superpowers+ provenance truthful, and keep portable skills separate from repo-local runbooks.

**Architecture:** Treat `repo.local_skills` as an exact allowlist throughout installation and provenance, with legacy prefix keys accepted only by the scaffold migration boundary. Move this repository's binding unslop overlay into `.agents/contracts/unslop/`, make repo-standards define that consumer custody, replace false snapshot boilerplate with per-skill provenance grounded in the pinned upstream commit, and audit every runbook so generic method returns to its owning skill.

**Tech Stack:** Markdown, JSON, Python, pytest, repository marketplace/install/index generators.

**Spec:** Human-approved MARK-373 follow-up discussion on 2026-09-11; live comparison with `Z:/rooms-mostly` and `Z:/wild-bunch` confirms exact `repo.local_skills` registration and repo-resident `.agents/unslop/` overlays.

**Execution Strategy:** `manual` — the changes share one custody and vocabulary model and require consistent semantic adjudication across tooling, skills, provenance, and runbooks.

## Global Constraints

- `repo.local_skills` contains exact complete skill identifiers; it is not a prefix list.
- `local_skill_prefixes` is legacy input accepted only for explicit migration by the repo-standards scaffold; active runtime and generated contracts do not expose prefix semantics.
- Repo-resident unslop profiles are binding repository contracts under `.agents/contracts/unslop/`; portable generic profiles remain owned by the shipped `unslop-profiles` skill.
- Consumer repo-standards defines the custody convention but does not ship a consumer's repo-specific profile content.
- Superpowers+ pins upstream v6.3.0 commit `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` without vendoring an upstream snapshot.
- A skill derived from upstream says it is marketplace-maintained and points to the pinned basis; an entirely first-party skill does not claim upstream derivation.
- Skill descriptions use consumer-neutral trigger language. Repo, product, portfolio, architecture, and taste-specific conditions belong in local overlays or the relevant skill body.
- Runbooks describe how to work in this repository: local paths, commands, custody, exceptions, and evidence requirements. Generic method, sequencing, self-review, and handoff behaviour belong to portable skills.
- Edit canonical plugin sources first and regenerate installed copies and indexes.
- Keep PR #311 Draft. Do not run Quorum or paid model evaluation.

### Task 1: Make local-skill registration exact

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/refreshing-installed-skills/SKILL.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/scaffold_marketplace_json.py`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-shape-standard.md`
- Modify: `tools/marketplace_utils.py`
- Test: `tests/test_refresh_installed_skills.py`
- Test: `tests/test_repo_standards.py`

- [ ] **Step 1: Add RED exact-registration tests.** Prove that `repo.local_skills: [alpha]` preserves `alpha` but not `alpha-extra`, that undeclared local directories are rejected, and that legacy `local_skill_prefixes` is migrated only by the scaffold.
- [ ] **Step 2: Verify RED.** Run the focused installer and scaffold tests and confirm prefix matching is the cause.
- [ ] **Step 3: Implement exact identity semantics.** Rename internal variables and helpers, compare directory names by exact membership, pass exact names to extension hooks, and emit exact names in provenance and generated manifests.
- [ ] **Step 4: Retire active prefix language.** Update portable skill/reference prose, examples, function names, diagnostics, and current tests while retaining narrowly labelled legacy migration coverage.
- [ ] **Step 5: Run focused tests.** Require exact registration, orphan cleanup, provenance, scaffold migration, and marketplace generation to pass.

### Task 2: Put repo-resident unslop profiles under contract custody

**Files:**
- Move: `.agents/docs/unslop/profile.md` -> `.agents/contracts/unslop/repository.md`
- Move/regenerate: `.agents/docs/unslop/INDEX.md` -> `.agents/contracts/unslop/INDEX.md`
- Modify: `.agents/doctrine/contracts.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-shape-standard.md`
- Modify: `tools/generate_repo_index.py`
- Modify: affected indexes and tests

- [ ] **Step 1: Add RED custody assertions.** Require the marketplace profile at `.agents/contracts/unslop/repository.md`, reject active `.agents/docs/unslop/` and root `.agents/unslop/` custody, and require repo-standards to define scoped and repo-wide consumer locations.
- [ ] **Step 2: Verify RED.** Confirm the current docs location and generated index entry fail.
- [ ] **Step 3: Move and classify the marketplace profile.** Preserve binding repository-specific constraints, remove any generic profile material already owned by the portable skill, and update references.
- [ ] **Step 4: Define the consumer convention.** Use `.agents/contracts/unslop/` for repo-wide profiles and `<scope>/.agents/contracts/unslop/` for justified subsystem overlays; require explicit indexing and local ownership.
- [ ] **Step 5: Regenerate indexes and verify custody.** Ensure no obsolete live unslop folder remains and no consumer-specific profile is added to the portable pack.

### Task 3: Correct Superpowers+ provenance

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/SOURCE.md`
- Modify: affected `codex-marketplace/plugins/superpowers-plus/skills/*/SKILL.md`
- Test: `tests/test_workflow_contracts.py`

- [ ] **Step 1: Add RED provenance tests.** Reject claims that an upstream snapshot is retained locally; require the pinned commit and distinguish upstream-derived skill names from entirely first-party additions.
- [ ] **Step 2: Verify RED.** Confirm current boilerplate falsely identifies each maintained skill directory as an upstream snapshot.
- [ ] **Step 3: Rewrite plugin provenance.** Call `SOURCE.md` a provenance record, state that upstream source is not vendored, and point comparisons to the repository URL and immutable commit.
- [ ] **Step 4: Rewrite per-skill provenance.** Use “marketplace-maintained derivative” only for skills corresponding to upstream v6.3.0 skills; label marketplace-only additions as first-party without an upstream-derivation claim. Treat `using-superpowers-plus` as the maintained successor to upstream `using-superpowers`.
- [ ] **Step 5: Run focused provenance and marketplace tests.** Require no false snapshot claim in canonical or generated skill prose.

### Task 4: Restore the skill/runbook boundary repo-wide

**Files:**
- Review/modify: `.agents/runbooks/*.md`
- Modify: owning canonical skills only if a generic invariant exists solely in a runbook
- Test: `tests/test_workflow_contracts.py`
- Test: `tests/test_repo_standards.py`

- [ ] **Step 1: Inventory every runbook by sentence ownership.** Classify each substantive instruction as repository path, command, custody, exception, local evidence, or generic workflow method.
- [ ] **Step 2: Add RED boundary tests.** Require runbooks to identify their local scope and reject duplicated generic stage checklists, generic reviewer personas, generic self-review loops, and generic skill sequencing.
- [ ] **Step 3: Thin all violating runbooks.** Keep marketplace-specific facts in runbooks; route generic design, planning, implementation, testing, review, and publication behaviour to their owning skills without copying it.
- [ ] **Step 4: Repair portable owners where needed.** Move a generic invariant into the canonical skill only when the runbook is its sole current owner; otherwise delete the duplicate.
- [ ] **Step 5: Review the complete runbook set.** Confirm `design.md`, `code-review.md`, `implementing.md`, `pr.md`, `testing.md`, and every other runbook satisfy the same boundary.

### Task 5: Make skill discovery consumer-neutral

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/asking-clarifying-questions/SKILL.md`
- Modify: other canonical vendored `SKILL.md` and `agents/openai.yaml` files found by the inventory
- Test: `tests/test_workflow_contracts.py`

- [ ] **Step 1: Add RED portability tests.** Require asking-clarifying-questions to describe unresolved ambiguity generally and reject product-, portfolio-, repository-, architecture-, or taste-specific trigger assumptions in portable descriptions.
- [ ] **Step 2: Verify RED.** Confirm the current taste-word and source-inspection description fails.
- [ ] **Step 3: Repair asking-clarifying-questions.** Define it as the anytime escalation for one unresolved ambiguity that one human answer can settle after safe internal resolution.
- [ ] **Step 4: Audit all canonical descriptions and wrappers.** Keep domain terms only where the skill itself owns that domain; move consumer-specific constraints to local contracts or body guidance.
- [ ] **Step 5: Run the structural and semantic inventory.** Require zero known malformed, misleading, or consumer-specific discovery fields.

### Task 6: Regenerate, review, and publish

**Files:**
- Modify: this plan
- Modify: `.agents/plans/2026-09-06-mark-373-operating-system.checkpoint.md`
- Modify: PR #311 body
- Regenerate: `.agents/skills/`, marketplace manifests, and index mesh

- [ ] **Step 1: Regenerate owned outputs.** Run `py -3 tools/run.py installed-skills --apply` and `py -3 tools/run.py mesh --apply`.
- [ ] **Step 2: Run focused suites and inventories.** Cover installer, repo-standards, workflow contracts, marketplace generation, provenance, custody, and runbook boundaries.
- [ ] **Step 3: Review adversarially.** Check exact registration, legacy migration isolation, source/generated parity, consumer portability, provenance accuracy, contract custody, and absence of Quorum artifacts.
- [ ] **Step 4: Update plan and checkpoint truthfully.** Record deterministic evidence and the semantic-review boundary without creating a duplicate receipt.
- [ ] **Step 5: Commit normally and push.** Let the tracked pre-commit apply/check hook provide the broad gate; push the existing branch.
- [ ] **Step 6: Update and verify Draft PR #311.** Keep it Draft; confirm clean tree, local/remote head equality, base `main`, and honest PR text.

## Acceptance evidence

- Local skill preservation is exact-name based; prefix matching cannot preserve an undeclared sibling.
- Current generated schemas and provenance use `local_skills`; prefix terminology survives only in labelled legacy migration input tests/code.
- Repo-resident unslop contracts live under `.agents/contracts/unslop/`, and repo-standards defines the same consumer pattern.
- No tracked Superpowers+ prose claims an upstream snapshot is retained when it is not.
- Upstream-derived and entirely first-party skills have distinct, truthful provenance.
- Runbooks contain repository-specific operating facts and delegate generic workflow method to skills.
- Portable skill descriptions and wrappers are grammatically clear, semantically accurate, and consumer-neutral.
- Generated installed skills match canonical sources; focused tests and the normal hooked gate pass.
- PR #311 remains Draft and contains no Quorum vendor or paid-evaluation output.

## Plan-readiness self-review

- The plan covers every approved discussion point and the expanded all-runbook audit.
- Exact registration is specified as observable behavior, with legacy migration isolated at one boundary.
- Repo-level contract custody is separated from portable skill-owned profile custody.
- Provenance language distinguishes maintenance from original authorship and does not imply vendored source.
- Semantic review is not falsely reduced to regex; deterministic regressions still receive tests.

**Plan-readiness rating:** 9.3/10.
