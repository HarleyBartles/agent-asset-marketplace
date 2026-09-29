# Marketplace Migration and Source Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish an unambiguous marketplace source revision and a safe consumer migration guide for selectable standards, ambient capabilities, and the retired index mesh.

**Architecture:** Keep consumer runner mechanics in the pinned marketplace-source checkout and keep the consumer's outer `tools/run.py ci` interface stable. Prepare selected standards and capability-based workflow documents before cutover; remove refresh and mesh projection dependencies in one runner change, prove the new hook works without ambient subscriptions, then remove subscriptions that existed only to provide copied runner assets. Treat the merged marketplace source commit SHA as the immutable release version because this repository has no semantic release or GitHub Release convention.

**Tech Stack:** Markdown guidance, Python migration integration tests, marketplace build and installed-skill generator, Git/GitHub PR publication.

**Spec:** `.agents/specs/2026-09-28-ambient-operating-model-and-selectable-standards-design.md`; roadmap: `.agents/plans/ambient-operating-model/roadmap.md`.

**Execution Strategy:** `executing-plans` - the guide, its integration proof, generated product, and source revision release are sequential and share one migration contract; separate implementer handoffs would add little independent review value.

## Global Constraints

- Do not edit Rooms-Mostly or another consumer repository in this marketplace plan.
- Keep a consumer's outer `tools/run.py ci --apply` and `tools/run.py ci --check` entrypoints stable.
- Do not remove consumer plugin subscriptions until the updated runner and tracked hook pass without ambient skill projections.
- A consumer selects only standards it declares; an empty marketplace-standard selection remains valid.
- Runtime skill availability does not prove repository subscription, local skill ownership, or standard adoption.
- Required workflow capabilities must stop and report before dependent work if no suitable runtime provider exists.
- Hosted validation must use the consumer's pinned deployed checkers and must not depend on Codex or ambient plugin projections.
- Use the exact merged source commit SHA as the published marketplace version; do not invent a semantic-version or tag convention.
- Preserve the normal tracked pre-commit hook and Draft PR policy while implementation and review continue.

## Review Focus

- **Unsafe mixed-runner transition:** refreshing installed skills can remove the mesh script before the old runner stops calling it. Cover with explicit cutover order and the existing integration test that runs pinned resources without `.agents/skills/`.
- **Premature subscription removal:** an old pinned repo-shape checker may still require bootstrap plugins. Keep subscriptions until the consumer advances to the compatibility revision and its hook passes; test the current no-subscription contract.
- **Capability migration loss:** legacy exact names may be ambient, repository-owned, or genuinely unavailable. Document the new capability sections, exact local custody, and required stop/report behavior while retaining the explicit legacy bridge.
- **Hosted false confidence:** local runtime availability is not hosted evidence. Require hosted validation against deployed selected resources and state the boundary in migration and release docs.

______________________________________________________________________

## Task 1: Make consumer migration sequencing safe and capability-aware

**Files:** `skills/repo-shape/references/consumer-runner-migration.md`; `skills/repo-shape/tests/scripts/test_consumer_runner_migration.py`; relevant `skills/repo-shape/tests/scripts/test_operating_model_plugin_contracts.py` cases.

**Consumes:** Plan 2 runner bridge, Plan 3 capability contract, current Rooms runner and pinned source evidence.

- [ ] **Step 1: Confirm the migration test covers zero ambient projections**

Run `py -3 -m pytest skills/repo-shape/tests/scripts/test_consumer_runner_migration.py skills/repo-shape/tests/scripts/test_operating_model_plugin_contracts.py -q`.

Expected: the consumer migration fixture passes with an empty plugin subscription list and without `.agents/skills/`; the standards dispatcher and refresh script resolve from the pinned source.

- [ ] **Step 2: Rewrite the runner cutover order**

Update the guide so consumers first preserve current state, preview and deploy their declared standards, and prepare capability-based runbook/playbook requirements. Then make one runner cutover that points standards checks and refresh to pinned resources and removes all mesh targets/calls before any refresh can delete copied mesh scripts. Keep existing plugin subscriptions during that cutover. Only after the new tracked hook passes should the consumer remove subscriptions and skill copies whose sole purpose was runner implementation, then rerun local and hosted validation without ambient projections.

- [ ] **Step 3: Document rollback and exact release pin use**

State that rollback restores the whole pre-cutover state, including the prior source gitlink, runner, hook, standards declaration, subscriptions, and generated outputs. Tell consumers to pin the published marketplace source SHA and never restore mesh calls against the post-retirement source.

- [ ] **Step 4: Verify migration behavior**

Run the Task 1 command again. Confirm the fixture proves the runner can use the selected deployed standard and pinned refresh resource with an empty plugin marketplace and no skill projection.

**Task exit:** Migration instructions no longer run a refresh that can remove scripts still required by the old runner; plugin removal follows a proven runner cutover; capability migration and rollback are explicit.

## Task 2: Explain source revision as the release version

**Files:** `docs/distribution.md`; `skills/repo-shape/references/consumer-runner-migration.md`; `.agents/plans/ambient-operating-model/roadmap.md`.

**Consumes:** Task 1 and live repository release evidence: the repository has no semantic release tags or GitHub Releases, while consumer contracts pin marketplace resources by immutable source revision.

- [ ] **Step 1: Add the immutable source revision convention**

Document that consumers use the merged marketplace source commit SHA as the released version for their `marketplace-source` gitlink and deployed standard revisions. Distinguish this revision from plugin metadata's `version` field and from installed skill provenance; do not change plugin versions or create a new tag scheme in this plan.

- [ ] **Step 2: Prepare the migration release note**

Add a concise release note under `docs/` summarizing the five ambient product roles, selectable standard adoption, capability-based runbook requirements, the required missing-capability stop, hosted validation boundary, mesh removal, and ordered runner migration. Link the consumer migration guide and leave exact source SHA reporting to the publication handoff after merge.

**Task exit:** A consumer can identify what changed, which exact source revision to pin, and how to migrate without treating plugin metadata versions as repository-standard revisions.

## Task 3: Validate and publish the source release

**Files:** generated `dist/` and `.agents/skills/` if Task 1 changes packaged sources; the Task 1/2 source files; this plan and the roadmap.

**Consumes:** Tasks 1 and 2.

- [ ] **Step 1: Regenerate and verify owned outputs**

Run `py -3 tools/run.py marketplace --apply` and `py -3 tools/run.py installed-skills --apply`, then run both corresponding `--check` commands. Do not hand-edit generated products.

- [ ] **Step 2: Run focused and complete validation**

Run the consumer-runner migration and plugin-contract suites, then review the source and generated diff. Commit normally so the tracked hook runs the complete canonical apply/check gate. Do not run the full CI check immediately before or after a successful hooked commit.

- [ ] **Step 3: Request a fresh code review and resolve findings**

Review the final branch against the migration order, no-subscription contract, source revision semantics, and hosted validation boundary. Fix confirmed findings and repeat review after corrections.

- [ ] **Step 4: Publish and record the released source version**

Push the branch, verify the exact PR head and checks, move the PR from Draft to Ready only after self-review and hook evidence are current, and merge the authorized PR. Record the merged commit SHA in the roadmap and final migration handoff as the immutable released source version. Hosted marketplace validation may remain skipped for Draft commits; verify the post-Ready checks before merge.

- [ ] **Step 5: Mark the plan complete**

Set this plan to `completed-awaiting-retirement`, update the roadmap with the merged source SHA, PR URL, local hook evidence, hosted checks, and migration guide, and commit those records through the tracked hook.

**Task exit:** The marketplace changes are merged, the release is named by its immutable source SHA, and consumers have a tested migration sequence that preserves their runner and hosted validation boundary.

## Review Focus

- The consumer runner never refreshes away a mesh helper before mesh calls are removed.
- `repo-standards` accepts the new pinned compatibility source without Superpowers+, Repo Worker Pack, Agent Operating Model, or `.agents/skills/` subscriptions.
- The migration retains only individually selected standards and genuinely repository-owned exact skills.
- The release SHA is the merged marketplace source revision used by consumer gitlinks and standard provenance.
- No consumer checkout is edited or claimed as migrated by this marketplace release.

## Handoff

- **Selected lane:** Native `executing-plans` in the existing roadmap worktree/PR. The guide and its integration proof are tightly coupled, and source release/publication depends on their final reviewed tree.
- **Base and publication:** Continue on `codex/ambient-operating-model-design` and Draft PR #338. The user authorized shipping this roadmap; consumer-specific edits remain with their respective agents.
- **Repository guidance:** Follow `AGENTS.md`, `.agents/runbooks/implementing.md`, `.agents/runbooks/pr.md`, `.agents/playbooks/testing.md`, and the portable repo-shape/repo-composition contracts.
- **Consumer evidence:** Rooms was inspected read-only on `main`; its current runner still calls projection refresh and retired mesh scripts, its source gitlink predates the compatibility no-op, and its plugin manifest subscribes to ambient packs. Do not remove those subscriptions until its runner and hook are cut over.
