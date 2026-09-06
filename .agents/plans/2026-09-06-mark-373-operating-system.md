# MARK-373 Operating-System Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish a single model-agnostic operating-system contract in the marketplace so later repository adoption work can inherit clear authority, bounded reading, proportionate validation, review, and publication semantics.

**Architecture:** Rebase the Superpowers+ derivation onto current upstream first, then repair the original owners of contradictory behavior rather than layering compensating overrides on stale v6.2 semantics. Put cross-runtime authority and autonomy in `base-doctrine`, repository-facing validation choreography in `repo-worker-base`, and stage-specific behavior in the owning Superpowers+ skills. Validate both deterministic source contracts and observed composed-stack behavior while leaving domain evidence and repository commands to downstream repos.

**Tech Stack:** Markdown skill/reference assets, JSON evaluation fixtures, pytest structural contract tests, upstream Superpowers provenance/diffing, the repository marketplace/index generators, the tracked pre-commit hook, and the repository's existing pressure-evaluation tooling.

**Execution Strategy:** `executing-plans` — the contract edits are coupled through shared authority and generated marketplace surfaces; one executor should make the semantic changes in dependency order and run the full repository gate once at the commit boundary. PR #311 is the plan-only PR. After this plan is approved and merged, implementation starts from current `main` in a fresh implementation worktree/branch and opens a separate Draft implementation PR.

## Global Constraints

- MARK-373 is the shared operating-system layer; it does not implement Bunch, Rooms, Portfolio, or Patch repository adoption.
- The contract is model-agnostic and must remain viable for Luna, Terra, Sol, and Astra.
- Rebase Superpowers+ onto current upstream v6.3 before applying MARK-373 semantic changes. Preserve first-party additions deliberately; do not blindly replace the derivative with upstream.
- The owning skill defines its own applicability and safety conditions; callers may request a capability but may not bypass or strengthen that owner gate.
- The authority order is: explicit human instruction; repository canon/policy for the touched surface; owning-skill applicability and safety contract; caller/runbook routing advice; generic defaults.
- Reversible investigation, diagnosis, repair, focused verification, and already-authorized publication preparation continue without synthetic approval pauses.
- Human input is required only for unresolved requirements/authority or before unauthorized destructive, irreversible, permission-changing, or externally consequential actions.
- Portable skills must not encode this repository's `Z:/` paths or `tools/run.py` commands; consumer repositories supply their own concrete paths, focused checks, canonical commit gate, and hosted-CI details.
- Canonical skill source is under `codex-marketplace/plugins/<plugin>/`; generated bundles, manifests, installed skills, indexes, and mesh files are regenerated outputs.
- Implementation PRs are Draft-first. A PR becomes ready only after the current committed head has local canonical hook evidence and completed local review/repair work.
- Where hosted CI consumes billed capacity, Draft PRs must not trigger the paid validation loop. The local tracked hook materially mirrors hosted CI, and alternate triggers such as unconditional `push` workflows must not bypass the Draft skip policy.
- Separate test-first discipline from test volume. Preserve meaningful RED/GREEN behavior but do not require ceremonial direct tests for implementation details that introduce no independent behavior or contract.
- Do not introduce an Astra-only branch, model conditional, overlay skill, or alternate workflow stack.

---

## Downstream Contract Map

The implementation must make these later adoption boundaries explicit in the plan and implementation PR description:

| Related issue | Later repository responsibility | MARK-373 export |
|---|---|---|
| `BUNCH-152` | DDD, CQRS, event sourcing, persistence, replay, API, and statistical/domain evidence | Authority, applicable-skill routing, focused-slice choreography, hooked commit gate, state-bound proof, and Draft-first publication |
| `ROOMS-55` | Three-domain authority, canon, custody, retired workflow cleanup, and ambiguity ownership | Owning-skill applicability, human-authority boundary, progressive reading, model/delegation separation, and review/readiness distinction |
| `PORT-15` | Visual, accessibility, editorial, public-route, and concrete hooked-gate evidence | Generic validation choreography and publication state; no visual/editorial policy |
| `PATCH-53` | Thin creative-repo adoption, story/canon boundaries, compact validation, and regression proof | The smallest shared baseline; no imported domain hierarchy or creative canon |

## Planned File Map

### Upstream derivation and canonical portable source

- Audit and rebase `codex-marketplace/plugins/superpowers-plus/` from the current v6.2-derived baseline onto upstream `obra/superpowers` v6.3.0, preserving first-party additions and recording the new provenance deliberately.
- Modify `codex-marketplace/plugins/repo-worker-pack/skills/base-doctrine/SKILL.md` to route the new operating contract without duplicating it.
- Create `codex-marketplace/plugins/repo-worker-pack/skills/base-doctrine/references/operating-contract.md` for precedence, owning-skill applicability, model-agnostic autonomy, and the boundary between internal resolution and human-owned decisions.
- Modify `codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/SKILL.md` to expose the repository-facing validation contract.
- Create `codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/references/repository-validation-contract.md` for consumer-supplied focused checks, canonical commit gate, hosted-CI parity, state-bound evidence, Draft-first lifecycle, and anti-bypass CI trigger semantics.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/SKILL.md` to classify before broad environment/doctrine loading and to route only the references needed by the selected mode.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/brainstorming/SKILL.md` so design work scales with actual uncertainty/impact and does not impose universal approval gates on every tiny change.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/verification-before-completion/SKILL.md` to bind evidence to tested state instead of conversational message boundaries and to distinguish focused, hooked, and hosted proof.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/finishing-a-development-branch/SKILL.md` so it reuses valid state-bound evidence and honors already-authorized integration/publication intent instead of mandating a fresh full suite and unconditional integration menu.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/publishing-source/SKILL.md` to make an authorized Draft PR the default publication surface without a second Draft/Ready permission question.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/handoff-gates/SKILL.md` to make readiness recipient-relative and require local canonical proof plus completed local review before Draft promotion.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/SKILL.md` to require observable goals, seams, invariants, authority, and acceptance evidence while making implementation-level code recipient-relative.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/SKILL.md` to preserve no-silent-discard and durable rulings while allowing evidence-backed technical adjudication before the churn cap.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/SKILL.md` to state that workflow ownership decides whether to delegate and this skill decides the exact exposed profile/model/reasoning/context route.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/test-driven-development/SKILL.md` and, where needed, its `writing-good-tests.md` guidance so behavior/contract evidence governs test demand rather than a blanket every-function rule.
- Modify `codex-marketplace/plugins/agentic-evaluation/skills/agent-evaluation/SKILL.md` or its operational reference to describe composed instruction-stack evaluations and per-scenario/per-dimension reporting without claiming model-generalized scores.
- Audit `base-doctrine`, `connector-safety`, `writing-skills`, and other broad roots found by the pressure scan for progressive-disclosure opportunities. Change only roots where the audit demonstrates a real trigger/context-cost problem.

### Repository-local contract consumers

- Modify `.agents/runbooks/implementing.md` and `.agents/runbooks/testing.md` so this repository's concrete commands express focused checks during iteration and the hooked canonical gate at commit without ritual full-suite reruns.
- Audit `.agents/runbooks/implementing.md` and related callers for stale unconditional workflow calls, including unconditional `iterative-review`, unconditional `systematic-debugging`, caller-strengthened TDD, automatic Linear mutation, and unbounded cheap-fix-while-here behavior.
- Retain `.agents/runbooks/pr.md` as the repository-local Draft/hook/hosted-CI owner, but update it if needed to guarantee that Draft PRs do not consume paid hosted CI through `pull_request`, `push`, or alternate workflow triggers.
- Create `tests/test_workflow_contracts.py` for deterministic structural checks over the canonical source files and evaluation fixture.
- Create `tests/pressure/workflow-contracts/README.md`, `campaign.json`, `prompts/`, and `results.md` for the composed-stack pressure campaign. Record actual model runs by model, reasoning, environment, and evidence status.
- Add or extend a bounded static pressure scan that reports candidate contradictions without treating matches as automatic failures.

### Generated outputs

- Regenerate `codex-marketplace/` manifests and bundle manifests, `.agents/plugins/marketplace.json`, `.agents/skills/`, repository indexes, and `INDEX.md` mesh only after all canonical source and test edits are complete.

## Task 1: Rebase Superpowers+ onto current upstream before MARK semantic edits

**Files:**

- Inspect and modify: `codex-marketplace/plugins/superpowers-plus/`
- Update provenance metadata/files owned by the derivative as required by the existing marketplace structure.

**Interfaces:**

- Starts from the current first-party derivative based on `obra/superpowers` v6.2.0.
- Uses the previously audited current upstream v6.3.0 baseline (`b36e0829c6d0140e93cfef2ca599b1b07d4a7797`) rather than assuming the old derivative is still the right semantic base.
- Produces a clean v6.3-derived baseline with first-party behavior preserved intentionally and no MARK-specific semantic edits yet.

- [ ] **Step 1: Reconfirm upstream provenance before mutation.**

  Verify the current derivative provenance and the current upstream v6.3 source. If upstream has moved beyond the audited v6.3.0 commit, record the difference and use the latest explicitly approved/current source rather than silently rebasing to an unknown revision.

- [ ] **Step 2: Diff upstream v6.2 -> v6.3 and classify each changed Superpowers skill.**

  Record which upstream changes can be accepted directly, which overlap first-party modifications, and which require a deliberate merge. Pay particular attention to brainstorming scaling, SDD rulings/not-stalls, pre-dispatch conflict scans, same-shaped microtask batching, reviewer evidence reuse, worktree cleanup, compression, testing guidance, and any changed Codex/event-driven behavior.

- [ ] **Step 3: Rebase the derivative without losing first-party owners.**

  Apply upstream v6.3 changes to the canonical Superpowers+ sources. Preserve first-party additions where they remain intentional, resolve conflicts explicitly, and update provenance so the resulting tree no longer claims v6.2 as its active base.

- [ ] **Step 4: Validate the rebased baseline before MARK-specific edits.**

  Run the smallest existing marketplace/skill structural checks that prove the derivative is well-formed and generated surfaces can still be rebuilt. Do not run the full repository gate merely because the upstream rebase task ended; the hooked commit remains the canonical broad gate.

- [ ] **Step 5: Mark Task 1 checklist items complete in this plan.**

## Task 2: Lock the MARK contract with failing structural tests and an evaluation fixture

**Files:**

- Create: `tests/test_workflow_contracts.py`
- Create: `tests/pressure/workflow-contracts/README.md`
- Create: `tests/pressure/workflow-contracts/campaign.json`
- Create: `tests/pressure/workflow-contracts/prompts/`
- Create: `tests/pressure/workflow-contracts/results.md`

**Interfaces:**

- Consumes Task 1's rebased v6.3-derived baseline.
- Produces deterministic assertions that fail on the remaining contradictory wording and a reusable scenario schema for observed RED/GREEN runs.

- [ ] **Step 1: Add structural contract assertions before changing MARK-owned source.**

  Assert that the canonical files expose these semantic anchors: classify-before-bootstrap routing; explicit authority precedence; owning-skill applicability; model-agnostic autonomy; state-bound evidence; focused/hooked/hosted validation distinction; Draft-first publication; recipient-relative planning; early evidence-backed adjudication; separate delegation/model decisions; proportionate TDD/test-volume semantics; non-universal brainstorming approval; branch-finish reuse of unchanged evidence; and Draft-hosted-CI anti-bypass semantics.

- [ ] **Step 2: Add static pressure-scan assertions/reporting.**

  Scan active portable and marketplace-local instruction surfaces for candidate phrases and patterns including `wait for approval`, `ask your human partner`, `full test suite`, `run multiple times`, `every new function`, `at session start`, `at every decision point`, `MUST READ`, unconditional connector writes, unconditional skill invocations, hard-coded personal paths, and repo-specific commands inside portable skills. Treat hits as review candidates with owning-file context, not automatic test failures.

- [ ] **Step 3: Run the focused test file to capture RED evidence.**

  Run `py -3 -m pytest tests/test_workflow_contracts.py -q`. The test must fail only for remaining MARK-373 contract gaps on the rebased baseline; do not hard-code assumptions that upstream v6.3 still contains every v6.2 defect.

- [ ] **Step 4: Write the evaluation fixture.**

  Define scenarios for: trivial docs correction; a specified bug whose first focused test fails; genuine ambiguity; a demonstrably wrong reviewer finding; authorized Draft PR creation; resume after compaction; unauthorized destructive work; parallelizable bounded work with mixed profile selection; a small reversible change where a full matrix is wasteful; a repo-local rule conflicting with a portable skill; a tiny change that must not trigger universal design approval; a branch-finish path with already-valid canonical evidence and already-authorized PR publication; and a no-independent-behavior helper that must not acquire a ceremonial direct test. For each scenario, include expected authority decision, expected next action, applicable evidence scope, and rubric dimensions for unnecessary questions, instruction reads, redundant verification, premature stopping, completion quality, scope/authority violations, delegation quality, and context/time cost.

- [ ] **Step 5: Mark Task 2 checklist items complete in this plan.**

## Task 3: Establish shared authority, applicability, bounded reading, and autonomy ownership

**Files:**

- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/base-doctrine/SKILL.md`
- Create: `codex-marketplace/plugins/repo-worker-pack/skills/base-doctrine/references/operating-contract.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/SKILL.md`
- Audit/modify as evidence requires: `codex-marketplace/plugins/repo-worker-pack/skills/connector-safety/SKILL.md`, `codex-marketplace/plugins/superpowers-plus/skills/writing-skills/SKILL.md`, and other broad roots surfaced by Task 2.

**Interfaces:**

- Consumes Task 2's failing structural assertions and pressure-scan candidates.
- Produces the cross-runtime contract that every later stage and consumer repository can reference without broad bootstrap cost.

- [ ] **Step 1: Add the operating-contract reference.**

  State the authority precedence exactly as defined in Global Constraints. Define the owning-skill rule: callers route capability requests, while the skill that owns a capability decides applicability and safety. Define the autonomy rule in operational terms: continue through reversible investigation, diagnosis, repair, focused checks, and authorized publication preparation; ask only for unresolved human-owned requirements/authority or high-risk unauthorized actions. State that this contract applies across Luna, Terra, Sol, and Astra.

- [ ] **Step 2: Reduce `base-doctrine/SKILL.md` to a bounded router.**

  Keep only the reference-selection map, canonical source boundary, and route to `operating-contract.md`; preserve durable-doctrine and bounded-read routing without making the root skill load every reference.

- [ ] **Step 3: Refactor `using-superpowers-plus/SKILL.md`.**

  Make request classification the first semantic action. After classification, inspect only environment dimensions that can change the selected route, load only the owning doctrine/skill references required by that route, and stop when the next lawful action is known.

- [ ] **Step 4: Audit broad roots for progressive disclosure and portability.**

  Review `connector-safety`, `writing-skills`, `base-doctrine`, and any other high-pressure roots reported by Task 2. Move detailed recipes/examples into references only where the root is actually over-broad. Remove existing portable hard-coded personal paths or marketplace-only commands rather than merely forbidding new ones.

- [ ] **Step 5: Run the focused structural test and pressure scan.**

  Run `py -3 -m pytest tests/test_workflow_contracts.py -q`. Authority/bootstrap/portability assertions must pass while later task assertions remain the only expected failures. Review pressure-scan hits and classify any remaining hit as intended, repo-local, deferred with reason, or defect to repair.

- [ ] **Step 6: Mark Task 3 checklist items complete in this plan.**

## Task 4: Export the repository validation, TDD, and Draft-first publication contract

**Files:**

- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/SKILL.md`
- Create: `codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/references/repository-validation-contract.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/verification-before-completion/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/test-driven-development/SKILL.md`
- Modify if needed: `codex-marketplace/plugins/superpowers-plus/skills/test-driven-development/writing-good-tests.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/finishing-a-development-branch/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/handoff-gates/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/publishing-source/SKILL.md`

**Interfaces:**

- Consumes Task 3's operating contract.
- Produces the portable choreography later repositories adopt with their own commands and domain-specific evidence.

- [ ] **Step 1: Add the repository-validation reference.**

  Define consumer inputs for: change-class-to-focused-check mapping; canonical tracked pre-commit gate command/executable; hosted-CI workflow; Draft-skip/anti-bypass condition; and state/evidence identifiers. Define the sequence as focused falsifying slice while editing, normal hooked commit over the intended staged tree, reuse while the tested state is unchanged, local review/repair while Draft, promotion to Ready only on current local proof, and hosted CI confirmation after promotion. State that consumer repos own domain-specific evidence and commands.

- [ ] **Step 2: Update `repo-worker-base`.**

  Add a bounded pointer to the new reference and state that repo-worker supplies choreography while each repository supplies concrete validation, paths, and CI implementation details.

- [ ] **Step 3: Update `verification-before-completion`.**

  Replace conversational “run in this message” freshness with state-bound evidence: record tested tree/head/staged state, command/scope, relevant environment, and result. Permit reuse of unchanged proof and require a named reason before broadening or repeating: new changes, failure, unresolved concern, nondeterminism, environment drift, or a different claim.

- [ ] **Step 4: Reconcile TDD ownership with behavior/contract evidence.**

  Preserve RED/GREEN as the normal way to establish changed behavior and bug fixes, but remove blanket wording that every function/method requires a direct test or that trivial glue/config/generated work must always stop for human permission. Align the root with `writing-good-tests.md`: every test should name the behavior or contract it protects; trivial forwarders/constants/helpers may be covered transitively when direct tests would only mirror implementation.

- [ ] **Step 5: Reconcile branch-finish ownership.**

  Remove unconditional full-suite reruns when current canonical state-bound proof already exists. If the user's/task's integration destination is already authorized, do not force a generic merge/PR/keep menu; continue to the authorized route. Preserve explicit confirmation for destructive discard and genuinely unknown integration destination.

- [ ] **Step 6: Update `handoff-gates`.**

  Make readiness relative to recipient and stage. Require current local canonical proof and completed local review/repair before Draft promotion. Keep numeric scoring diagnostic rather than a reason to invent work or rerun unchanged validation.

- [ ] **Step 7: Update `publishing-source`.**

  Preserve validation-before-publication and make an authorized implementation PR Draft-first by default. Ready is a later evidence-backed transition, not an alternative creation mode that requires a second permission question.

- [ ] **Step 8: Encode hosted-CI economics and anti-bypass semantics.**

  The portable contract must say that where hosted CI is billed, the tracked hook materially mirrors it and hosted CI skips Draft PRs. Consumer adoption must audit alternate triggers (`push`, reusable workflow calls, scheduled/manual paths where relevant) so normal Draft iteration cannot silently burn the same paid CI. A hosted failure that the local mirror reasonably could have caught is parity drift to repair.

- [ ] **Step 9: Run the focused structural test.**

  Run `py -3 -m pytest tests/test_workflow_contracts.py -q` and confirm validation/TDD/publication/branch-finish assertions are green.

- [ ] **Step 10: Mark Task 4 checklist items complete in this plan.**

## Task 5: Remove universal design approval and make planning, delegation, and review composition recipient-relative

**Files:**

- Modify: `codex-marketplace/plugins/superpowers-plus/skills/brainstorming/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/SKILL.md`
- Modify: `codex-marketplace/plugins/agentic-evaluation/skills/agent-evaluation/SKILL.md` or its operational reference, selecting the smaller source seam after inspection

**Interfaces:**

- Consumes Tasks 3 and 4's shared authority and evidence semantics.
- Produces stage guidance that scales with task uncertainty and recipient capability without model-specific forks.

- [ ] **Step 1: Reconcile `brainstorming` with the autonomy contract.**

  Preserve genuine collaborative design for ambiguous or consequential creative work, but remove universal “every project needs design approval” and repeated approval gates for bounded work whose intent is already clear. Scale the design artifact and approval need to uncertainty/consequence; user-owned product/canon choices remain human decisions.

- [ ] **Step 2: Refactor `writing-plans`.**

  Keep plans strong on observable goal, scope/exclusions, source seams, invariants, interfaces, acceptance evidence, authority boundaries, and genuine task decomposition. Make exact implementation code optional and recipient-relative rather than mandatory transcription.

- [ ] **Step 3: Refactor SDD adjudication.**

  Preserve the finding ledger, no-silent-discard rule, reviewer-fix loop, and churn cap. Permit an evidence-backed technical ruling before dispatching a fix when source, tests, or contracts falsify the finding. Route unresolved requirement/authority disputes to the human.

- [ ] **Step 4: Tighten subagent selection.**

  State separately that the stage/workflow decides whether delegation is warranted and `selecting-a-subagent` chooses the least-escalated adequate exposed profile, model, reasoning, and context route. Preserve runtime inventory as authoritative. Keep Sol as the ordinary strong reviewer/orchestrator unless evidence says otherwise; do not redefine `strongest` or `reviewer-strong` to mean Astra. Astra is an explicit exceptional escalation for genuinely difficult/high-consequence reasoning or explicit human choice.

- [ ] **Step 5: Extend agent evaluation guidance.**

  Add composed instruction stacks as the evaluation unit, require held-out scenarios where practical, and require per-scenario/per-dimension reporting. Keep model-specific observations separate from cross-model conclusions and distinguish rubric evidence from model self-rating.

- [ ] **Step 6: Run the focused structural test.**

  Run `py -3 -m pytest tests/test_workflow_contracts.py -q`; all source-contract assertions must pass.

- [ ] **Step 7: Mark Task 5 checklist items complete in this plan.**

## Task 6: Align this repository's concrete callers, worker/testing overlays, and CI triggers

**Files:**

- Modify: `.agents/runbooks/implementing.md`
- Modify: `.agents/runbooks/testing.md`
- Modify: `.agents/runbooks/pr.md` as required by concrete trigger/parity findings
- Inspect: active repo runbooks/doctrine and `.github/workflows/` for caller-strengthened skills, stale review routes, automatic connector writes, and Draft-CI bypasses

**Interfaces:**

- Consumes the portable contracts from Tasks 3–5.
- Produces the marketplace repository's concrete command/hook/PR overlay without exporting those commands into portable skills.

- [ ] **Step 1: Define focused checks by touched surface.**

  Keep the repository's canonical `py -3 -m pytest` and `py -3 tools/run.py` commands, but state that focused checks are selected while editing and the full canonical gate is exercised by the normal tracked hook at commit. Preserve direct evidence for marketplace, mesh, script, and security changes where those surfaces are touched.

- [ ] **Step 2: Remove ritual freshness and blanket validation repetition.**

  Remove “run validation multiple times” and equivalent rules unless nondeterminism/flakiness is the actual claim under investigation. Repeat or broaden only after a new change, failure, unresolved concern, nondeterminism, environment drift, or a different proof claim.

- [ ] **Step 3: Remove stale caller-strengthened workflow requirements.**

  Audit and repair unconditional calls to conditional owners. In particular: do not require `iterative-review` when its owning skill excludes the current frontier orchestrator; do not require full `systematic-debugging` for every ordinary failing test when a bounded diagnosis suffices; do not strengthen TDD beyond the owner contract; and do not hard-code review/model routes that now belong to shared selection/applicability owners.

- [ ] **Step 4: Return connector mutation authority to connector/domain owners.**

  Remove the blanket rule that implementation agents must mutate Linear whenever scope shifts. The repo may require scope honesty, but actual Linear mutation follows `linear-issue-shaping`/connector authority. If mutation is not authorized, surface the discrepancy in the PR/report rather than writing anyway.

- [ ] **Step 5: Bound fix-while-here work.**

  Replace the unconditional “cheap under ten minutes => fix it” rule with a scope ceiling: opportunistic fixes are acceptable only when low-risk, mechanically bounded, inside the already-touched surface, and not a new product/architecture/migration decision or validation campaign. Otherwise track separately.

- [ ] **Step 6: Verify Draft-first hosted-CI anti-bypass behavior in this repo.**

  Inspect `.agents/runbooks/pr.md` and `.github/workflows/`. Confirm implementation PRs open Draft, hosted CI skips Draft PRs, and `push` or alternate triggers do not cause the paid equivalent workflow to run throughout Draft iteration. Where exact local/hosted parity is technically impossible, document the explicit delta and why.

- [ ] **Step 7: Run local runbook, trigger, and link checks.**

  Run `py -3 -m pytest tests/test_validate_agent_mesh.py tests/test_review_preflight.py tests/test_review_preflight_extensions.py -q` and `py -3 tools/run.py mesh --check` after the overlay edits. Add focused workflow tests if the CI trigger audit exposes an untested Draft-skip invariant.

- [ ] **Step 8: Mark Task 6 checklist items complete in this plan.**

## Task 7: Run observed composed-stack pressure evaluations

**Files:**

- Update: `tests/pressure/workflow-contracts/results.md`
- Update fixture metadata only if observed execution reveals a schema gap; do not move goalposts to make a failing run appear green.

**Interfaces:**

- Consumes the completed shared contracts and repository-local callers from Tasks 3–6.
- Produces observed evidence for the models actually exposed by the implementation environment.

- [ ] **Step 1: Execute every pressure scenario on each available target model/profile.**

  Run the composed scenarios against Luna, Terra, Sol, and Astra where the live harness exposes them. Label each run with exact model/profile, reasoning level, harness/environment, timestamp/commit, and evidence source. If a model is genuinely unavailable, mark it `unavailable` with the observed reason; do not substitute inferred behavior or another model.

- [ ] **Step 2: Record per-scenario/per-dimension results.**

  Capture unnecessary human questions, instruction reads before useful work, redundant verification, premature stopping, completion quality, scope/authority violations, delegation/model quality, and context/time cost. Keep model-specific findings separate; do not average them into a single score that hides weaker-model regressions.

- [ ] **Step 3: Repair contract failures exposed by observed runs.**

  If a failure is caused by instruction composition, repair the owning source and rerun the smallest affected scenario/model set. Do not rerun the whole matrix without a named reason.

- [ ] **Step 4: Establish the evaluation completion claim honestly.**

  MARK-373's behavioral lane is complete only when every model exposed in the implementation environment has observed evidence. Unavailable models may remain explicitly unavailable; a fixture alone is not behavioral proof.

- [ ] **Step 5: Mark Task 7 checklist items complete in this plan.**

## Task 8: Regenerate, validate, review, commit, and publish the implementation Draft PR

**Files:**

- Generated by tooling: marketplace manifests, bundle manifests, installed skills, repository indexes, and `INDEX.md` mesh.
- Modify: `.agents/plans/2026-09-06-mark-373-operating-system.md` to check off delivered implementation steps.

**Interfaces:**

- Starts only after PR #311 (this plan PR) is approved and merged.
- Implementation begins from current `main` in a fresh implementation worktree/branch; do not continue implementing on the plan-only PR branch.
- Consumes all completed canonical source, evaluation, and local-overlay work from Tasks 1–7.
- Produces a separate committed, regenerated, GitHub-visible Draft implementation PR into `main` with honest scope and head evidence.

- [ ] **Step 1: Start from approved current `main`.**

  Create a fresh implementation worktree/branch after PR #311 lands. Confirm the merged plan is present and the branch starts from current `main` rather than reusing `codex/mark-373-operating-system` as the implementation branch.

- [ ] **Step 2: Run the marketplace rebuild.**

  Run `py -3 tools/run.py marketplace --apply`. Inspect the diff to confirm generated surfaces reflect canonical source changes and no unrelated plugin content changed.

- [ ] **Step 3: Run focused and structural validation.**

  Run `py -3 -m pytest tests/test_workflow_contracts.py tests/test_validate_agent_mesh.py tests/test_review_preflight.py tests/test_review_preflight_extensions.py -q`. Run `py -3 tools/run.py review-preflight --check` and `py -3 tools/run.py mesh --check` for uncommitted proof. Record failures with their actual state and repair before proceeding.

- [ ] **Step 4: Perform self-review against the related-issue map and owner matrix.**

  Confirm the diff exports only generic workflow semantics; Bunch-specific architecture, Rooms-specific canon/custody, Portfolio-specific visual/public/editorial evidence, and Patch-specific creative-repo details remain downstream. Confirm no private corpus, credential, external secret, Astra-only conditional, generated-surface hand edit, stale v6.2 provenance, caller-strengthened owner gate, or portable repo/machine assumption remains in the changed surfaces.

- [ ] **Step 5: Stage the intended tree and commit normally.**

  Run `git add -A` and commit without `--no-verify`. The tracked hook must materialize the staged snapshot, run the repository canonical apply/check pipeline, stage owned generated outputs, and provide the broad local proof for that exact state. Do not run an equivalent full gate immediately before or after a successful hooked commit.

- [ ] **Step 6: Verify the committed state without duplicating the broad gate.**

  Run `git status --short --branch`, `git diff --check HEAD^`, `py -3 tools/run.py review-preflight --check`, and `py -3 tools/run.py mesh --check`. Capture the committed head SHA and confirm the worktree is clean. If the hook was absent or failed to provide canonical evidence, run the canonical CI command as the named diagnostic and repair the cause.

- [ ] **Step 7: Push and open a separate Draft implementation PR.**

  Push the implementation branch and create a Draft PR targeting `main`. The PR body must link MARK-373 and PR #311, link the four related adoption issues, identify portable contract surfaces changed, list validation/evaluation evidence, state that downstream repository adoption remains out of scope, and include the published branch and full head SHA.

- [ ] **Step 8: Verify GitHub Draft/CI state.**

  Read the created PR and confirm URL, base `main`, branch name, Draft status, head SHA, changed-file scope, and that hosted CI has not been triggered through an alternate path merely because the Draft PR/branch was pushed.

- [ ] **Step 9: Promote to Ready only after local completion.**

  Keep the PR Draft through implementation, local review, repair, and additional hooked commits. Only mark Ready when the current head has fresh canonical local hook evidence, observed pressure evidence is complete for available models, local review/repair is complete, and no known parity defect remains. Hosted CI then acts as paid confirmation.

- [ ] **Step 10: Treat catchable hosted failures as parity defects.**

  If hosted CI fails after Ready on a condition the local hook could reasonably have caught, repair the hook/hosted parity rather than accepting remote CI as the normal debugging loop.

- [ ] **Step 11: Mark all delivered plan steps complete.**

  Update every completed checkbox in this plan, leave any genuinely undelivered item unchecked with an explicit reason, commit the plan state through the same normal hook path, push the updated head, and re-read the PR before reporting.

## Acceptance Evidence

- Superpowers+ is rebased onto current upstream v6.3 before first-party MARK changes are applied, with provenance and preserved first-party behavior explicit.
- The focused structural test demonstrates the shared operating contract and evaluation fixture.
- Active portable and repo-local instruction surfaces have been pressure-scanned; candidate contradictions are classified rather than silently ignored.
- Universal design approval, unconditional branch-finish menus/full-suite reruns, message-bound verification, and blanket every-function testing no longer contradict the shared contract.
- The marketplace's own callers no longer resurrect conditional `iterative-review`, over-scale debugging, force connector mutations, or absorb unrelated cheap fixes merely because they are cheap.
- The repository validation contract is `focused checks while editing -> hooked commits while Draft -> local review/repair -> Ready -> hosted CI confirmation`.
- Hosted CI skips Draft PRs, alternate triggers do not bypass the policy, and the tracked local hook materially mirrors the paid gate.
- Observed composed-stack results exist for every Luna/Terra/Sol/Astra model/profile available in the implementation environment; unavailable targets are named as unavailable rather than inferred.
- Generated outputs are sourced from canonical plugin files and rebuilt after source edits.
- The normal hooked commit provides the single broad local proof over the exact staged/committed state; equivalent unchanged-state reruns are not required.
- A separate Draft implementation PR is visible on GitHub against `main` with a verified head SHA; PR #311 remains the plan-only PR.
- The implementation PR description and plan explicitly preserve the four downstream issue boundaries.

## Explicit Deferrals

- `BUNCH-152`, `ROOMS-55`, `PORT-15`, and `PATCH-53` adoption changes are not implemented in this PR.
- A model genuinely unavailable to the implementation harness may remain unrun, but its absence must be recorded explicitly; unavailable is not equivalent to passed.
- This plan does not move Bunch domain architecture, Rooms canon/custody, Portfolio visual/public evidence, or Patch creative canon into the shared marketplace layer.
- `iterative-review` itself is not redesigned unless the audit finds its owning applicability contract is internally wrong; stale callers that invoke it unconditionally are in scope and must be removed.
- Progressive-disclosure work outside roots demonstrated by the pressure scan is not a blanket cleanup campaign.

## Plan-readiness self-review

- Spec coverage: all ten MARK-373 findings, the cross-repo contract, Draft-first policy, upstream v6.3 rebase, static pressure scan, observed mixed-model evaluation, preservation list, non-goals, and four related adoption boundaries map to Tasks 1–8.
- Source custody: canonical plugin sources are the only authored skill edit points; generated surfaces are rebuilt after source edits.
- Ordering: upstream rebase precedes MARK RED tests; tests/fixture precede MARK source edits; portable owners precede repo callers; source and local overlays precede regeneration; observed behavioral evaluation occurs before final readiness; regeneration precedes the hooked commit; publication follows verified committed state.
- Validation: commands are repository-specific and named; portable contract references do not export those commands to consumers.
- Authority: human-owned decisions, repository-owned policy, owning-skill applicability, connector mutation authority, and downstream domain ownership remain distinct.
- Publication lifecycle: PR #311 is plan-only; implementation starts from merged `main` on a fresh branch and opens a separate Draft PR.
- No plan step relies on an unresolved user choice.

**Plan-readiness rating:** 9/10. The remaining uncertainty is implementation-discovery uncertainty only: exact upstream conflict resolution, which broad roots the pressure scan proves need editing, and which model profiles are live in the execution harness. Each is assigned to a bounded inspection step with an explicit stop condition and evidence requirement.
