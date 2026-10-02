# V2 Subscription and Repository-Owned Compliance Plan

**Status:** completed-awaiting-retirement

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate this Marketplace checkout to explicit v2 standard subscriptions and a truthful, repository-owned compliance chain without weakening its normal gate.

**Architecture:** Replace the v1 deployment manifest as the repository's adoption record with a minimal set of immutable definition pins and certification references. Implement the Marketplace's own mechanical checks under `tools/`, preserve semantic assessment in readable certification, and route the same checker through the existing Windows hook and Linux CI gate. The old byte-provenance runtime can remain on disk temporarily for Plan 9 cleanup, but no longer owns or blocks the active compliance chain.

**Tech Stack:** Python 3, JSON, Markdown, existing `tools/run.py` command registry and tracked hook/hosted CI.

**Spec:** [Approved AOM design](../../specs/2026-09-30-aom-standard-adoption-and-shipping.md), sections 1, 2, 3, 6, 7, and 8.

**Roadmap:** [Marketplace migration roadmap](2026-10-01-plan-7-marketplace-migration-roadmap.md), Plan 8. Baseline: Plan 7 planning commit following `3d59506db`.

**Execution Strategy:** `executing-plans` - contract, checker, and gate wiring form one authority transition with ordered dependencies and must be reviewed together; separate implementer handoffs would risk an intermediate state where neither contract is authoritative.

## Global Constraints

- The selected standards are `root-agent-router`, `runbook-composition`, `playbook-composition`, `tracked-validation-hook`, `review-entrypoint`, `contribution-entrypoint`, `completed-artifact-custody`, and `unslop`.
- Do not add `repo-plugin-subscriptions`, `command-bus`, or `agent-doctrine-contracts` subscriptions. Preserve `marketplace-registry` as a repository-owned concern.
- `.agents/contracts/operating-standards.json` records only version, standard ID, immutable source repository/commit/definition, and repository certification reference. It does not carry implementation commands or generated paths.
- Pin each definition to `3d59506dbd7a02266dedc9251b396dd60e5cc37d`; all eight definition paths were verified present at that existing commit before this plan was written.
- Keep a root `AGENTS.md` and make it route agents to subscriptions and readable certification. Preserve unrelated root guidance.
- Certification states observed implementation, evidence, and drift controls. Structural validation must not claim semantic compliance.
- Keep the existing Windows hook and Linux hosted workflow as the canonical equivalent repository gate. Do not bypass them or silently omit existing product checks.
- Preserve existing local skills, marketplace catalog, generated plugin output, and unrelated standards documents unless this plan names an owner change.
- Do not use a copied AOM scaffolder to deploy or overwrite this repository's implementation.

## Review Focus

- A catalog entry is not a subscription: the plan excludes `repo-plugin-subscriptions` because this checkout publishes `.agents/plugins/marketplace.json` but README states it declares no skill subscriptions.
- A v2 record can be structurally valid while the implementation is incomplete. Tests must preserve an explicit not-certified or gap state instead of inferring certification from subscription presence.
- A plugin refresh must not change the immutable standard pins or raise an automatic stale-version alarm.
- The checker must run from a clean clone without network access and must not execute source-pinned definitions or modify files.
- The normal hook's staged-tree behavior and existing Linux workflow remain intact when the repo-standards target changes.

## Mechanical and semantic boundary

| Selected pledge                     | Mechanical repository check                                                              | Semantic self-certification / review                                                               |
| ----------------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Root AGENTS router                  | Existing allow-list, root line budget, and CI invocation                                 | Useful progressive routes, scoped quality, and no duplicated doctrine                              |
| Runbook composition                 | Existing Markdown-link validator checks references                                       | Each maintained runbook is a useful work-stage lifecycle guide and is routed at the right point    |
| Playbook composition                | Existing Markdown-link validator checks references                                       | Concern/stage distinction, useful guidance, discoverability, and capability availability claims    |
| Tracked hook and CI                 | Hook/command contract, hosted workflow, and command runner route are present and aligned | Candidate-tree correctness, Linux/Windows equivalence, prerequisite coverage, and no-skip behavior |
| Review and contribution entrypoints | Root `REVIEW.md` and `CONTRIBUTING.md` exist and their local links resolve               | Each entrypoint is sufficient and useful for its audience                                          |
| Completed artifact custody          | No checker may infer completion from markers or checkbox counts                          | Next-slice semantic discovery, preservation of active plans, and promotion of durable knowledge    |
| Unslop                              | `.agents/unslop/` exists and relevant runbooks link to the profile                       | Distinct recurrence evidence, effective guards, and maintained feedback loop                       |

Mechanical results support the certification; they do not certify the semantic column.

______________________________________________________________________

### Task 1: Specify and implement the repository-owned read-only checker

**Files:**

- Create: `tests/repository/test_agent_standards.py`
- Create: `tools/check_agent_standards.py`
- Read: `.agents/contracts/operating-standards.json`
- Read: `.agents/standards/_runtime/repo_standards.py`
- Read: `tools/run.py`
- Read: `.agents/contracts/repo-standards-commands.json`
- Read: `.github/workflows/marketplace-validation.yml`
- Read: `.agents/specs/2026-09-30-aom-standard-adoption-and-shipping.md`

**Consumes:** The v2 structure and self-certification boundaries in the approved specification, plus the currently active hook and hosted gate.

**Produces:** Behavior tests and a deterministic, offline, repository-owned checker with clear mechanical diagnostics and no deployment or semantic-certification side effects.

- [x] Record the selected IDs and exact definition pins as fixture inputs; reject an unselected catalog entry and do not infer adoption from installed capabilities.
- [x] Cover malformed and duplicate subscription IDs, non-full Git IDs, unsafe paths, missing certification references, and missing root router. The remote definition path is structurally validated but need not exist in a consumer checkout.
- [x] Cover certification that accurately identifies an implementation gap without declaring success; do not equate structural validity with compliance.
- [x] Identify which selected-standard obligations are mechanically checkable here and which require agent/human semantic review; preserve existing checks only when they enforce a retained invariant.
- [x] Run focused cases to demonstrate expected failures before implementation.
- [x] Validate the v2 subscription schema, exact selected set, pin formats, known source repository, safe relative definition/certification paths, local certification presence, root `AGENTS.md`, and route targets. Do not require source definition files to be copied into the adopting checkout.
- [x] Validate only repository-chosen mechanical policy: retain meaningful AGENTS.md size alarms and structure checks, hook/CI command coverage, and required entrypoint locations. Book references use the existing Markdown-link checker; book category and usefulness stay semantic.
- [x] Keep semantic book usefulness, router quality, unslop effectiveness, hook parity quality, and all other judgment-based claims in certification/review instead of pretending source text or checker success proves them.
- [x] Ensure check mode performs no network access, writes, scaffold deployment, format changes, or execution of commands from the subscription record.
- [x] Ensure diagnostics distinguish malformed authority records, missing implementation evidence, mechanical policy failures, and semantic claims the checker cannot decide.
- [x] Run the focused behavior suite and the targeted static checks for the new code.

### Task 2: Atomically migrate v2 adoption and the active compliance chain

**Files:**

- Modify: `.agents/contracts/operating-standards.json`
- Create: `.agents/contracts/standards-certification.md`
- Modify: `AGENTS.md`
- Modify: `tools/run.py`
- Modify only if required by evidence: existing `.agents/doctrine/`, `.agents/contracts/`, `.agents/runbooks/`, `.agents/playbooks/`, `REVIEW.md`, and `CONTRIBUTING.md`
- Test: `tests/repository/test_agent_standards.py`; complete candidate hook on the atomic commit

**Consumes:** The checker interface from Task 1 and exact source definitions at the verified pin.

**Produces:** A minimal v2 subscription record, discoverable accurate certification, and an active hook/CI chain that uses the repository-owned checker. Commit these authority changes atomically because the current legacy gate reads v1-only fields from the subscription file.

- [x] Replace v1 command vectors and deployment roots with exactly the eight selected standards and their full immutable source, commit, definition, and certification identities.
- [x] Create certification entries that map each pledge to actual implementation, evidence, and drift controls; report any gap or unverified claim plainly, and do not mark the set fully certified while any adopted invariant is unmet.
- [x] Update root `AGENTS.md` with a concise conditional route to the subscription and certification while preserving its existing pointer-only shape.
- [x] Do not adopt doctrine/contracts standard merely because certification uses `.agents/contracts/`; do not add empty books or sections to resemble AOM starters.
- [x] Correct any concrete compliance gap discovered in the selected repository-owned surfaces only when the current plan's scoped implementation can safely close it; otherwise record the exact gap for Plan 9/11 and retain honest uncertified status.
- [x] Link planning, implementation, review, and PR runbooks directly to `.agents/unslop/repository.md`; keep ambient `$unslop-profiles` assistance optional for fresh clones.
- [x] Record concrete near-miss evidence in the repo-owned Unslop profile with a clear candidate status; do not label one session as cross-agent recurrence.
- [x] Run the focused checker and semantic read-through against each pinned definition and certification entry.
- [x] Replace the `_check_standard_deployment()` byte-equality prerequisite with the repository-owned checker; retain checks for generated Marketplace/plugin artifacts through their actual generator owners.
- [x] Remove the active gate's dependency on v1-only fields and generic scaffold dispatch. Do not yet delete now-unreferenced deployment files; Plan 9 owns retirement.
- [x] Preserve staged-candidate validation, apply/check behavior, diagnostics, command ordering, and the Windows/Linux shared target set.
- [x] Confirm the hook and hosted workflow invoke the same logical CI gate and that no user command is silently dropped.
- [x] Run `py -3 tools/check_agent_standards.py --check`, `py -3 tools/run.py repo-standards --check`, and the focused checker suite.
- [x] Run the complete normal Windows pre-commit gate by committing this atomic change; do not duplicate the full gate immediately before or after that hooked commit. Task 2 execution evidence records the full hook passing on atomic commit `534ee8400`.

### Task 3: Review and close the migration slice

**Files:**

- Modify: this plan, marking completed tasks
- Modify: `roadmap.md`, recording Plan 8's final commit and findings
- Review: complete change from the Plan 7 baseline

**Consumes:** Tasks 1-2, their focused evidence, and the completed Windows hook result.

**Produces:** A reviewable, committed v2 subscription transition with no claim of Linux execution until Plan 11 has current-hosted evidence.

- [x] Inspect the complete diff for retained selected standards, unselected standards, local plugin catalog ownership, and accidental deployment/scaffolder activity.
- [x] Verify generated files are changed only through their canonical generators; do not modify `dist/` by hand.
- [x] Obtain a fresh whole-slice review and resolve all material findings.
- [x] Update roadmap state, commit, and return a handoff summary that distinguishes Windows evidence from still-pending Linux evidence.
