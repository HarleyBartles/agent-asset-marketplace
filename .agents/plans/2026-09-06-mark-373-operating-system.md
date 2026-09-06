# MARK-373 Operating-System Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish a single model-agnostic operating-system contract in the marketplace so later repository adoption work can inherit clear authority, bounded reading, proportionate validation, review, and publication semantics.

**Architecture:** Rebase the Superpowers+ derivation onto the pinned upstream v6.3.0 baseline first, then repair the original owners of contradictory behavior rather than layering compensating overrides on stale v6.2 semantics. Put cross-runtime authority and autonomy in `base-doctrine`, repository-facing validation choreography in `repo-worker-base`, and stage-specific behavior in the owning Superpowers+ skills. Validate deterministic source contracts and observed composed-stack behavior while leaving domain evidence and repository commands to downstream repos.

**Tech Stack:** Markdown skill/reference assets, JSON evaluation fixtures, pytest structural contract tests, a small Python pressure-scan tool, upstream Superpowers provenance/diffing, repository marketplace/index generators, the tracked pre-commit hook, and the repository's existing pressure-evaluation tooling.

**Execution Strategy:** `executing-plans` — one executor makes the coupled semantic changes in dependency order. This plan is deliberately written to be executable by GPT-5.6 Luna without requiring Luna to recreate planner-level architectural decisions. PR #311 is the plan-only PR. After this plan is approved and merged, implementation starts from current `main` in a fresh implementation worktree/branch and opens a separate Draft implementation PR.

## Luna Execution Contract

This section is part of the plan contract, not advisory prose.

OpenAI's current model guidance positions GPT-5.6 Luna as the efficient/high-volume member of the 5.6 family and recommends clear goals, constraints, output contracts, completion criteria, and verification for agentic work. This plan therefore moves consequential design choices into the plan and leaves Luna only bounded repository discovery. The plan must remain executable at Luna **medium reasoning**; higher reasoning may be used, but omitted planner decisions must not be recovered by relying on extra model effort.

Official guidance used for this calibration:

- `https://developers.openai.com/api/docs/models/gpt-5.6-luna`
- `https://developers.openai.com/api/docs/guides/reasoning`
- `https://developers.openai.com/tracks/building-agents`

Execution rules for the Luna implementer:

1. **Pinned decisions are not rediscovery tasks.** If this plan gives an exact SHA, file path, class name, schema, model configuration, command, classification enum, or acceptance condition, use it. Do not choose an alternative merely because another reasonable option exists.
2. **Discovery is bounded.** A discovery step names the sources to inspect, the evidence to record, and the allowed outcomes. Inspect enough to decide among those outcomes, then stop reading.
3. **Technical facts are resolved by inspection.** Do not ask the human about a repository fact that can be read from source, git state, generated metadata, tests, or workflows.
4. **Escalate only plan-changing decisions.** Stop for the human only if evidence would require changing a pinned upstream revision, changing MARK-373 scope/authority, weakening a stated invariant, adding a new external mutation, or choosing between materially different product/architecture outcomes not covered here.
5. **Task exit conditions are binding.** Do not advance because a task “looks done.” Run the task's named focused check and satisfy its explicit green condition.
6. **Do not broaden validation opportunistically.** Use the named focused class/command for the task. The normal hooked commit supplies the broad local gate at the commit boundary.
7. **Do not broaden the model matrix.** The baseline evaluation matrix below is fixed. Extra model/profile/reasoning variants are diagnostic only after a baseline failure.
8. **Do not alter tests to make implementation green unless the contract changed.** If a RED assertion exposes a source defect, repair the owning source. Change the assertion only when repository evidence proves the test encoded the wrong requirement.

## Global Constraints

- MARK-373 is the shared operating-system layer; it does not implement Bunch, Rooms, Portfolio, or Patch repository adoption.
- The contract is model-agnostic and must remain viable for Luna, Terra, Sol, and Astra.
- Superpowers+ rebases onto the **fixed** upstream v6.3.0 commit `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`. A newer upstream revision may be recorded but must not be adopted in MARK-373 without a plan change approved by the human.
- Preserve first-party additions deliberately; do not blindly replace the derivative with upstream.
- The owning skill defines its own applicability and safety conditions; callers may request a capability but may not bypass or strengthen that owner gate.
- The authority order is: explicit human instruction; repository canon/policy for the touched surface; owning-skill applicability and safety contract; caller/runbook routing advice; generic defaults.
- Reversible investigation, diagnosis, repair, focused verification, and already-authorized publication preparation continue without synthetic approval pauses.
- Human input is required only for unresolved requirements/authority or before unauthorized destructive, irreversible, permission-changing, or externally consequential actions.
- Portable skills must not encode this repository's `Z:/` paths or `tools/run.py` commands; consumer repositories supply their own concrete paths, focused checks, canonical commit gate, and hosted-CI details.
- Canonical skill source is under `codex-marketplace/plugins/<plugin>/`; generated bundles, manifests, installed skills, indexes, and mesh files are regenerated outputs.
- Implementation PRs are Draft-first. A PR becomes ready only after the current committed head has local canonical hook evidence and completed local review/repair work.
- Where hosted CI consumes billed capacity, Draft PRs must not trigger the paid validation loop. The local tracked hook materially mirrors hosted CI, and alternate triggers must not bypass the Draft skip policy.
- Separate test-first discipline from test volume. Preserve meaningful RED/GREEN behavior but do not require ceremonial direct tests for implementation details that introduce no independent behavior or contract.
- Do not introduce an Astra-only branch, model conditional, overlay skill, or alternate workflow stack.

---

## Downstream Contract Map

The implementation must make these later adoption boundaries explicit in the implementation PR description:

| Related issue | Later repository responsibility | MARK-373 export |
|---|---|---|
| `BUNCH-152` | DDD, CQRS, event sourcing, persistence, replay, API, and statistical/domain evidence | Authority, applicable-skill routing, focused-slice choreography, hooked commit gate, state-bound proof, and Draft-first publication |
| `ROOMS-55` | Three-domain authority, canon, custody, retired workflow cleanup, and ambiguity ownership | Owning-skill applicability, human-authority boundary, progressive reading, model/delegation separation, and review/readiness distinction |
| `PORT-15` | Visual, accessibility, editorial, public-route, and concrete hooked-gate evidence | Generic validation choreography and publication state; no visual/editorial policy |
| `PATCH-53` | Thin creative-repo adoption, story/canon boundaries, compact validation, and regression proof | The smallest shared baseline; no imported domain hierarchy or creative canon |

## Fixed Evidence Artifacts

Use these exact durable paths. Do not invent alternate homes for the same evidence.

- `.agents/docs/mark-373-superpowers-v6.3-rebase.md` — v6.2 -> pinned v6.3 upstream classification and merge record.
- `tests/test_workflow_contracts.py` — deterministic structural contract tests, organized into the exact classes named below.
- `tools/workflow_pressure_scan.py` — candidate-only static pressure scanner.
- `tests/pressure/workflow-contracts/pressure-scan.json` — generated raw scanner output.
- `tests/pressure/workflow-contracts/pressure-scan.md` — reviewed/classified scanner findings.
- `tests/pressure/workflow-contracts/red-baseline.md` — initial structural RED inventory after the upstream rebase.
- `tests/pressure/workflow-contracts/ci-parity.md` — concrete local-hook/hosted-CI parity and trigger evidence for this repository.
- `tests/pressure/workflow-contracts/README.md` — campaign instructions and evidence conventions.
- `tests/pressure/workflow-contracts/campaign.json` — scenario definitions and canonical model matrix.
- `tests/pressure/workflow-contracts/prompts/` — scenario prompts.
- `tests/pressure/workflow-contracts/results.md` — observed model results.

## Structural Test Partition

`tests/test_workflow_contracts.py` uses **pytest classes, not custom markers**, so interim RED state is unambiguous. Create these exact classes:

- `TestAuthorityBootstrapPortability` — Task 3 owner.
- `TestValidationTddPublication` — Task 4 owner.
- `TestPlanningDelegationReview` — Task 5 owner.
- `TestRepositoryCallersAndPressure` — Task 6 owner.
- `TestEvaluationCampaign` — Task 2 fixture/schema owner and Task 7 evidence-shape owner.

Task 2 runs the whole file once to capture the initial RED inventory. Tasks 3-6 run only their owned class and require that class to become green; failures in classes owned by later tasks are expected and do not block interim progress. Run the entire file expecting green only after Task 6 has completed its source/repo-local repairs. Task 7 adds observed behavioral evidence; it must not weaken the already-green structural assertions.

## Canonical Evaluation Matrix

The baseline is **one general-purpose standard run per model family**, not every exposed profile/reasoning combination:

| Family | Baseline model | Mode | Reasoning | Baseline profile rule |
|---|---|---|---|---|
| Luna | `gpt-5.6-luna` | standard | medium | one general-purpose Luna route |
| Terra | `gpt-5.6-terra` | standard | medium | one general-purpose Terra route |
| Sol | `gpt-5.6-sol` | standard | medium | one general-purpose Sol route |
| Astra | `gpt-6-astra` | standard | medium | one general-purpose Astra route |

If the live harness exposes named profiles rather than raw model/mode/effort controls, select exactly one general-purpose profile that resolves to each family and record its effective model/reasoning configuration. Do not use reviewer-specialist profiles as the family baseline. If a family is unavailable, record `unavailable` plus the observed reason. Additional reasoning levels or specialist profiles are allowed only as **diagnostic runs after a baseline failure** and do not become extra completion requirements.

## Planned File Map

### Upstream derivation and canonical portable source

- Audit and rebase `codex-marketplace/plugins/superpowers-plus/` from the current v6.2-derived baseline onto pinned upstream `obra/superpowers` v6.3.0 commit `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`.
- Create `.agents/docs/mark-373-superpowers-v6.3-rebase.md` for the upstream classification/merge record.
- Modify `codex-marketplace/plugins/repo-worker-pack/skills/base-doctrine/SKILL.md` and create `references/operating-contract.md` for precedence, owning-skill applicability, autonomy, and human-owned decision boundaries.
- Modify `codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/SKILL.md` and create `references/repository-validation-contract.md` for focused checks, hooked canonical gate, state-bound evidence, hosted-CI parity, Draft lifecycle, and anti-bypass semantics.
- Modify the owning Superpowers+ skills: `using-superpowers-plus`, `brainstorming`, `verification-before-completion`, `test-driven-development`, `finishing-a-development-branch`, `publishing-source`, `handoff-gates`, `writing-plans`, `subagent-driven-development`, and `selecting-a-subagent`.
- Modify `test-driven-development/writing-good-tests.md` only if the root cannot be reconciled cleanly without changing that reference.
- Modify `agentic-evaluation/skills/agent-evaluation/SKILL.md` or the smallest existing operational reference after inspecting that skill's current source map.
- Audit `base-doctrine`, `connector-safety`, `writing-skills`, and other broad roots surfaced by the pressure scan. Change only roots where the scan plus source inspection demonstrates a real trigger/context-cost or portability problem.

### Repository-local contract consumers and evidence

- Modify `.agents/runbooks/implementing.md` and `.agents/runbooks/testing.md` for focused iteration and one hooked broad commit gate.
- Modify `.agents/runbooks/pr.md` only where necessary to make current Draft/CI facts explicit or preserve parity after source changes.
- Inspect `.github/workflows/marketplace-validation.yml`; it is the current hosted validation workflow and is the source of truth for the current trigger/command evidence described in Task 6.
- Create `tests/test_workflow_contracts.py` with the fixed class partition above.
- Create `tools/workflow_pressure_scan.py` and the fixed pressure/evaluation evidence artifacts above.

### Generated outputs

- Regenerate marketplace manifests, bundle manifests, `.agents/plugins/marketplace.json`, `.agents/skills/`, repository indexes, and `INDEX.md` mesh only after canonical source/test/tool edits are complete.

## Task 1: Rebase Superpowers+ onto the pinned upstream v6.3 baseline

**Files:**

- Inspect and modify: `codex-marketplace/plugins/superpowers-plus/`
- Create: `.agents/docs/mark-373-superpowers-v6.3-rebase.md`
- Update: derivative provenance metadata/files required by the existing marketplace structure.

**Consumes:** current first-party derivative based on `obra/superpowers` v6.2.0.

**Produces:** a clean derivative based on exactly `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`, plus a durable classification record. No MARK-specific semantic repairs belong in this task.

- [ ] **Step 1: Verify the pinned upstream object and current derivative provenance.**

  Confirm the v6.2-derived source provenance currently recorded by the marketplace. Confirm upstream commit `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` is retrievable and corresponds to v6.3.0.

  **Decision:** that SHA is the MARK-373 implementation baseline. If upstream has a newer revision, record its SHA/tag/date in the rebase record under `Newer upstream observed`, but continue with `b36e0829...`. Do **not** adopt the newer revision. If the pinned commit itself cannot be retrieved or does not match v6.3.0, stop with that concrete blocker because the pinned source assumption is false.

- [ ] **Step 2: Write the rebase record before modifying derivative source.**

  Create `.agents/docs/mark-373-superpowers-v6.3-rebase.md` with these sections:

  1. `Pinned baseline` — old v6.2 provenance, pinned v6.3 SHA/tag, retrieval source.
  2. `Newer upstream observed` — newer SHA/tag/date if present, otherwise `none observed`; explicitly state it is out of scope.
  3. `Skill classification` — table columns `skill | upstream v6.3 change | first-party overlap | action | rationale`.
  4. `Merge notes` — conflicts and how each was resolved.
  5. `Validation` — focused commands/results run for the rebased baseline.

- [ ] **Step 3: Classify the v6.2 -> pinned-v6.3 changes.**

  For every upstream-changed Superpowers skill, choose exactly one action in the record: `accept-upstream`, `merge-with-first-party`, `retain-first-party`, or `not-applicable`. Pay particular attention to brainstorming scaling, SDD rulings/not-stalls, pre-dispatch conflict scans, same-shaped microtask batching, reviewer evidence reuse, worktree cleanup, compression, testing guidance, and Codex/event-driven behavior.

  Do not leave an action blank. `retain-first-party` requires a rationale showing why the local owner remains intentional.

- [ ] **Step 4: Rebase the derivative.**

  Apply the pinned v6.3 changes according to the classification table. Preserve intentional first-party additions, resolve conflicts according to the recorded action, and update provenance so the active derivative no longer claims v6.2 as its base.

- [ ] **Step 5: Validate the rebased baseline.**

  Run the smallest existing marketplace/skill structural checks needed to prove the derivative remains well formed and regenerable. Record exact commands/results in the rebase document. Do not run the repository-wide canonical CI gate merely because Task 1 ended.

  **Green exit:** all upstream-changed skills have an explicit classification/action, active provenance names the pinned v6.3 baseline, and the focused structural/regeneration checks pass.

- [ ] **Step 6: Mark Task 1 checklist items complete in this plan.**

## Task 2: Lock the MARK contract with staged RED tests, the scanner contract, and evaluation fixtures

**Files:**

- Create: `tests/test_workflow_contracts.py`
- Create: `tools/workflow_pressure_scan.py`
- Create: `tests/pressure/workflow-contracts/README.md`
- Create: `tests/pressure/workflow-contracts/campaign.json`
- Create: `tests/pressure/workflow-contracts/prompts/`
- Create: `tests/pressure/workflow-contracts/red-baseline.md`
- Create/generated: `tests/pressure/workflow-contracts/pressure-scan.json`
- Create: `tests/pressure/workflow-contracts/pressure-scan.md`
- Create: `tests/pressure/workflow-contracts/results.md`

**Consumes:** Task 1's pinned v6.3-derived baseline.

**Produces:** deterministic contract tests with explicit ownership, a stable candidate-only scanner, a recorded RED inventory, and a fixed composed-scenario/model schema.

- [ ] **Step 1: Create the five structural test classes.**

  Use the exact class names from `Structural Test Partition`. Each test name should state one observable contract. Tests may inspect canonical Markdown/source content and fixture schemas; avoid brittle full-paragraph equality where a narrower semantic anchor proves the requirement.

  Class ownership:

  - `TestAuthorityBootstrapPortability`: classify-before-bootstrap, precedence, owning-skill applicability, autonomy, bounded roots, no portable machine/repo assumptions.
  - `TestValidationTddPublication`: state-bound evidence, focused/hooked/hosted distinction, TDD test-volume rule, branch-finish evidence reuse, Draft-first publication, hosted-CI anti-bypass contract.
  - `TestPlanningDelegationReview`: non-universal brainstorming gate, recipient-relative plans, early evidence-backed review adjudication, delegation-vs-model separation, Sol ordinary strong route/Astra exceptional escalation.
  - `TestRepositoryCallersAndPressure`: marketplace runbooks do not resurrect conditional owners, force Linear writes, require ritual reruns, or mandate unbounded fix-while-here work; pressure scan artifacts conform to schema.
  - `TestEvaluationCampaign`: scenario set, baseline matrix, per-run metadata, per-dimension result shape, and `unavailable` semantics.

- [ ] **Step 2: Implement the pressure scanner as a dedicated tool.**

  Create `tools/workflow_pressure_scan.py`. `tests/test_workflow_contracts.py` tests this tool's schema/behavior; do not bury scanning logic inside the pytest file.

  Scan these active authored surfaces:

  - `codex-marketplace/plugins/*/skills/**/SKILL.md`
  - portable skill `references/*.md` reachable from those roots
  - root `AGENTS.md`
  - `.agents/runbooks/*.md`
  - `.agents/doctrine/*.md`

  Exclude generated `.agents/skills/`, completed/archived plans/specs, licenses, fixture prompts/results, and vendored upstream snapshots that are not active authored instruction surfaces.

  Candidate rules include: `wait for approval`, `ask your human partner`, `full test suite`, `run multiple times`, `every new function`, `at session start`, `at every decision point`, `MUST READ`, unconditional connector writes, unconditional skill invocations, hard-coded personal paths, and repo-specific commands inside portable skills.

  CLI contract for this plan:

  `py -3 tools/workflow_pressure_scan.py --format json --output tests/pressure/workflow-contracts/pressure-scan.json`

  Raw JSON schema:

  - top level: `schema_version`, `commit`, `generated_at`, `patterns`, `hits`.
  - each hit: `path`, `line`, `rule`, `excerpt`.
  - scanner exits non-zero only for scanner/runtime/schema failure. Finding candidates is not itself failure.

  Create `pressure-scan.md` with columns `path | line | rule | excerpt | owner | classification | action`. Classification is exactly one of `defect`, `intended`, `repo-local`, `deferred`. `deferred` requires a reason and durable tracking reference. An unresolved `defect` blocks final readiness.

- [ ] **Step 3: Create the fixed evaluation campaign.**

  Put the canonical four-family medium-reasoning matrix from this plan into `campaign.json`. Do not enumerate every runtime profile. Add the composed scenarios for: trivial docs correction; specified bug whose first focused test fails; genuine ambiguity; demonstrably wrong reviewer finding; authorized Draft PR creation; resume after compaction; unauthorized destructive work; parallelizable bounded work with mixed model selection; small reversible change where a full matrix is wasteful; repo-local rule conflicting with portable skill; tiny change that must not trigger universal design approval; branch-finish with valid canonical evidence and authorized publication; and no-independent-behavior helper that must not acquire a ceremonial direct test.

  Each scenario records: expected authority decision, expected next action, evidence scope, expected stop/continue behavior, and rubric dimensions for unnecessary questions, instruction reads before useful work, redundant verification, premature stopping, completion quality, scope/authority violations, delegation/model quality, and context/time cost.

- [ ] **Step 4: Capture the full initial RED inventory once.**

  Run:

  `py -3 -m pytest tests/test_workflow_contracts.py -q`

  Record every failing test name and the owning future task in `red-baseline.md`. A test already green because upstream v6.3 fixed the behavior is recorded as `already green from upstream`; do not force it red.

  **Important:** from this point through Task 6, do not repeatedly run the full file merely to observe known later-task failures. Each task runs only its owned pytest class.

- [ ] **Step 5: Generate and classify the initial pressure scan.**

  Run the scanner command above, populate `pressure-scan.md`, and use source inspection to classify every hit. Task 2 does not repair all defects; it establishes the inventory and ownership. Assign each `defect` to Task 3, 4, 5, or 6 in the `action` column.

- [ ] **Step 6: Run the Task 2 fixture/schema class.**

  Run:

  `py -3 -m pytest tests/test_workflow_contracts.py::TestEvaluationCampaign -q`

  **Green exit:** the scanner, evidence files, scenario schema, canonical model matrix, and RED inventory exist and `TestEvaluationCampaign` passes. Other classes may remain red according to `red-baseline.md`.

- [ ] **Step 7: Mark Task 2 checklist items complete in this plan.**

## Task 3: Establish shared authority, applicability, bounded reading, and autonomy ownership

**Files:**

- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/base-doctrine/SKILL.md`
- Create: `codex-marketplace/plugins/repo-worker-pack/skills/base-doctrine/references/operating-contract.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/SKILL.md`
- Modify only when Task 2 classified a defect there: `connector-safety/SKILL.md`, `writing-skills/SKILL.md`, or another broad root named in `pressure-scan.md`.

**Consumes:** Task 2 defects assigned to Task 3.

**Produces:** the cross-runtime authority/autonomy/read contract with no broad-bootstrap or portable-path leakage.

- [ ] **Step 1: Add the operating contract.**

  Define the exact authority precedence from Global Constraints; owning-skill applicability; reversible-work autonomy; technical investigation before human questions; human-owned requirement/authority boundaries; and model-agnostic applicability across Luna/Terra/Sol/Astra.

- [ ] **Step 2: Make `base-doctrine` a bounded router.**

  Keep reference selection, canonical source boundary, bounded-read doctrine, and the route to `operating-contract.md`. Do not make the root load every reference.

- [ ] **Step 3: Refactor `using-superpowers-plus`.**

  Request classification is the first semantic action. After classification, inspect only environment dimensions that can alter the selected route/next action; load only owning references needed by that route; stop reading once the next lawful action is known.

- [ ] **Step 4: Repair only Task-3-owned broad-root/portability defects.**

  Use `pressure-scan.md` as the worklist. For each Task-3 `defect`, either repair the owning source or, if inspection proves the hit intentional, change its classification with rationale. Remove existing hard-coded personal paths or marketplace-only commands from portable skills; do not merely add a rule forbidding future leakage.

- [ ] **Step 5: Run only Task 3's structural class.**

  `py -3 -m pytest tests/test_workflow_contracts.py::TestAuthorityBootstrapPortability -q`

  Regenerate the pressure scan and update classifications only for paths changed in this task.

  **Green exit:** `TestAuthorityBootstrapPortability` passes and no unresolved Task-3 `defect` remains in `pressure-scan.md`.

- [ ] **Step 6: Mark Task 3 checklist items complete in this plan.**

## Task 4: Export validation, TDD, branch-finish, and Draft-first publication semantics

**Files:**

- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/SKILL.md`
- Create: `codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/references/repository-validation-contract.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/verification-before-completion/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/test-driven-development/SKILL.md`
- Modify if required by the root reconciliation: `codex-marketplace/plugins/superpowers-plus/skills/test-driven-development/writing-good-tests.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/finishing-a-development-branch/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/handoff-gates/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/publishing-source/SKILL.md`

**Consumes:** Task 3 operating contract plus Task-4 defects from `pressure-scan.md`.

**Produces:** portable validation/publication choreography, state-bound proof, proportionate TDD, and branch-finish behavior.

- [ ] **Step 1: Add `repository-validation-contract.md`.**

  Define consumer inputs for: change-class -> focused-check mapping; canonical tracked pre-commit gate; hosted-CI workflow; Draft-skip/anti-bypass condition; state/evidence identifiers. Define the lifecycle exactly as:

  `focused falsifying checks while editing -> normal hooked commits while Draft -> local review/repair -> Ready only on current local proof -> hosted CI confirmation`

  Repositories own their commands/domain evidence. Marketplace owns choreography/evidence semantics.

- [ ] **Step 2: Update `repo-worker-base`.**

  Route to the validation contract without embedding this repository's concrete commands/paths.

- [ ] **Step 3: Make verification state-bound.**

  Replace conversational “run in this message” freshness with evidence keyed to tested tree/head/staged state, command/scope, relevant environment, and result. Reuse unchanged proof. Repeat/broaden only for new changes, failure, unresolved concern, nondeterminism, environment drift, or a different proof claim.

- [ ] **Step 4: Reconcile TDD with behavior/contract evidence.**

  Preserve RED/GREEN for changed behavior and bug fixes. Remove blanket “every new function/method has a direct test” semantics. Tests protect observable behavior/contracts; trivial forwarders/constants/helpers may be covered transitively when direct tests would mirror implementation. Do not introduce a new human approval gate for trivial glue/config/generated work.

- [ ] **Step 5: Reconcile branch finish.**

  Reuse current canonical state-bound proof instead of mandating a fresh full suite. If the integration/publication route is already authorized, continue on that route rather than presenting a generic menu. Preserve explicit confirmation for destructive discard and a real question when destination/authority is genuinely unknown.

- [ ] **Step 6: Update handoff and publication owners.**

  `handoff-gates`: readiness is recipient/stage-relative; Draft promotion requires current local canonical proof and completed local review/repair; numeric score is diagnostic, not work-generation pressure.

  `publishing-source`: an already-authorized implementation PR opens Draft by default; Ready is a later evidence-backed transition, not a second creation choice.

- [ ] **Step 7: Encode portable hosted-CI economics.**

  Where hosted CI is billed, a tracked local hook materially mirrors it, Draft PRs skip hosted CI, alternate triggers cannot make ordinary Draft iteration consume the same paid validation, and a hosted failure reasonably catchable locally is parity drift to repair.

- [ ] **Step 8: Repair Task-4 pressure defects and run only Task 4's class.**

  `py -3 -m pytest tests/test_workflow_contracts.py::TestValidationTddPublication -q`

  Regenerate/update pressure findings for changed paths.

  **Green exit:** `TestValidationTddPublication` passes and no unresolved Task-4 `defect` remains.

- [ ] **Step 9: Mark Task 4 checklist items complete in this plan.**

## Task 5: Remove universal design approval and make planning, delegation, and review recipient-relative

**Files:**

- Modify: `codex-marketplace/plugins/superpowers-plus/skills/brainstorming/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/SKILL.md`
- Modify: `codex-marketplace/plugins/agentic-evaluation/skills/agent-evaluation/SKILL.md` or its smallest existing operational reference after source inspection.

**Consumes:** Tasks 3-4 contracts plus Task-5 defects from `pressure-scan.md`.

**Produces:** stage guidance that scales with uncertainty and recipient capability without model-specific workflow forks.

- [ ] **Step 1: Reconcile `brainstorming`.**

  Preserve collaborative design for ambiguous/consequential creative work. Remove universal “every project needs design approval” and repeated approvals for bounded work whose intent is already settled. Human-owned product/canon choices remain human decisions.

- [ ] **Step 2: Make `writing-plans` explicitly recipient-relative.**

  Preserve strong plans on goal, scope/exclusions, source seams, invariants, interfaces, acceptance evidence, authority, exact known commands/paths, and task decomposition. Exact implementation code is included when contractual or when the selected recipient needs it; it is not mandatory transcription for every capable executor.

  Add the planner rule demonstrated by this plan: for lower-capability execution recipients such as Luna, pre-resolve consequential choices; name exact evidence artifacts and commands; turn unavoidable discovery into finite decision tables; and define a green exit per task. Do not use a stronger executor merely to compensate for an under-specified plan.

- [ ] **Step 3: Refactor SDD adjudication.**

  Preserve finding ledger, no-silent-discard, reviewer-fix loop, and churn cap. Permit evidence-backed technical ruling before a fix when source/tests/contracts falsify the finding. Requirements/authority disputes still route to the human.

- [ ] **Step 4: Tighten subagent/model selection ownership.**

  Stage/workflow decides whether to delegate. `selecting-a-subagent` chooses least-escalated adequate profile/model/reasoning/context from runtime inventory. Keep Sol as ordinary strong reviewer/orchestrator; Astra is explicit exceptional escalation for genuinely difficult/high-consequence reasoning or human choice. Do not redefine `strongest`/`reviewer-strong` as Astra.

- [ ] **Step 5: Extend evaluation guidance.**

  Composed instruction stacks are the evaluation unit. Require held-out scenarios where practical and per-scenario/per-dimension evidence. Keep model-specific observations separate from cross-model conclusions; rubric evidence is not model self-rating.

- [ ] **Step 6: Repair Task-5 pressure defects and run only Task 5's class.**

  `py -3 -m pytest tests/test_workflow_contracts.py::TestPlanningDelegationReview -q`

  **Green exit:** `TestPlanningDelegationReview` passes and no unresolved Task-5 `defect` remains.

- [ ] **Step 7: Mark Task 5 checklist items complete in this plan.**

## Task 6: Align marketplace callers and prove concrete local/hosted CI parity

**Files:**

- Modify: `.agents/runbooks/implementing.md`
- Modify: `.agents/runbooks/testing.md`
- Modify only if current facts/changes require it: `.agents/runbooks/pr.md`
- Inspect: `.github/workflows/marketplace-validation.yml`
- Inspect: active tracked pre-commit hook and the shared `ci` task implementation/registry used by `tools/run.py`
- Update: `tests/pressure/workflow-contracts/ci-parity.md`
- Update: `tests/pressure/workflow-contracts/pressure-scan.md`

**Consumes:** Tasks 3-5 portable contracts plus Task-6 pressure defects.

**Produces:** repo-local callers that do not strengthen owners, plus concrete proof that local canonical validation and paid hosted validation cover the same CI contract and Draft iteration cannot trigger the paid loop accidentally.

### Fixed current CI facts to verify, not redesign

At plan time, `.github/workflows/marketplace-validation.yml` has these facts:

- `pull_request` events: `opened`, `synchronize`, `reopened`, `ready_for_review`.
- job guard: `${{ github.event_name != 'pull_request' || github.event.pull_request.draft == false }}`.
- `push` is restricted to `main`.
- `workflow_dispatch` exists as an explicit manual trigger.
- hosted validation command is `tools/run ci --check`.

At plan time, `.agents/runbooks/pr.md` states the normal pre-commit hook materializes the staged snapshot, runs `ci --apply`, stages only owned generated surfaces, then runs `ci --check --diagnostics`.

If those facts are still true at implementation time, Luna records them and proceeds; do not invent a new CI design. If source has changed, compare the new state to the acceptance criteria below and repair only a real contract regression.

- [ ] **Step 1: Remove ritual freshness/repetition from repo-local callers.**

  Keep focused checks during editing and the hooked broad gate at normal commit. Remove “run validation multiple times” unless nondeterminism/flakiness is the claim being tested.

- [ ] **Step 2: Remove caller-strengthened conditional workflows.**

  `iterative-review` is not mandatory where its owner excludes the current frontier orchestrator. `systematic-debugging` is not mandatory for every ordinary failing test when bounded diagnosis suffices. Repo runbooks do not strengthen TDD beyond its owner or hard-code model/review routes owned elsewhere.

- [ ] **Step 3: Return Linear mutation authority to the Linear owner.**

  Keep scope honesty, but remove blanket “implementation agent must mutate Linear when scope changes.” Mutation follows `linear-issue-shaping`/connector authority. When unauthorized, report the discrepancy rather than writing anyway.

- [ ] **Step 4: Bound fix-while-here.**

  Opportunistic fixes are allowed only when low-risk, mechanically bounded, inside the already-touched surface, and not a new product/architecture/migration decision or validation campaign. Otherwise track separately.

- [ ] **Step 5: Prove CI command parity using the shared `ci` task, not string similarity.**

  In `ci-parity.md`, record:

  - hosted workflow path and hosted command;
  - active tracked hook path and hook command sequence;
  - source location of the `ci` task registry/pipeline used by both commands;
  - the set/order of checks dispatched by hosted `ci --check`;
  - the set/order of checks dispatched by local `ci --check --diagnostics` after `ci --apply`;
  - any difference and whether it is only execution mode/reporting (`apply`, diagnostics vs fail-fast) or an actual omitted check.

  **Materially mirrors =** after local mechanical `ci --apply`, local `ci --check --diagnostics` and hosted `ci --check` invoke the same canonical CI check registry for the same repository state. Diagnostics/fail-fast presentation may differ; the local path must not omit a hosted validation target. If a hosted target is absent locally, parity is red and must be repaired before readiness.

- [ ] **Step 6: Prove Draft anti-bypass from triggers.**

  In `ci-parity.md`, record a trigger table with `event | branch/state | job runs? | rationale`.

  **Green criteria for this repository:**

  - Draft `pull_request` events reach the workflow but the validation job is skipped by the draft guard.
  - Ready/non-Draft PR events can run the validation job.
  - feature/task branch `push` does not trigger this hosted workflow because `push` is `main` only.
  - `workflow_dispatch` is an explicit manual action and therefore is not an automatic Draft-iteration bypass; do not remove it merely to satisfy this policy.
  - no other workflow or reusable-call path runs the paid equivalent CI command automatically on feature/task branch pushes or Draft PR synchronization.

  If another workflow does run an equivalent paid validation automatically during Draft iteration, repair or gate that trigger.

- [ ] **Step 7: Run repo-local focused checks and Task 6's structural class.**

  Run:

  - `py -3 -m pytest tests/test_validate_agent_mesh.py tests/test_review_preflight.py tests/test_review_preflight_extensions.py -q`
  - `py -3 tools/run.py mesh --check`
  - `py -3 -m pytest tests/test_workflow_contracts.py::TestRepositoryCallersAndPressure -q`

  Add a focused workflow test only if the trigger/parity audit exposes an untested invariant that can regress mechanically.

- [ ] **Step 8: Run the complete structural contract file once.**

  `py -3 -m pytest tests/test_workflow_contracts.py -q`

  **Green exit:** the whole structural file is green; `ci-parity.md` has a green parity/anti-bypass verdict; no unresolved `defect` remains in `pressure-scan.md`. If this full run exposes a failure owned by an earlier task, repair that owner and rerun only the failing class first, then rerun the full file once.

- [ ] **Step 9: Mark Task 6 checklist items complete in this plan.**

## Task 7: Run the fixed observed composed-stack evaluation matrix

**Files:**

- Update: `tests/pressure/workflow-contracts/results.md`
- Update `campaign.json` only if an observed harness fact requires recording a resolved profile name/effective config; do not change scenarios/rubrics to make a failure pass.

**Consumes:** structurally green contracts from Tasks 3-6 and the fixed matrix from this plan.

**Produces:** observed evidence for one canonical run per available model family.

- [ ] **Step 1: Resolve one baseline runtime route per family.**

  For Luna, Terra, Sol, and Astra, resolve one general-purpose route to the fixed model/mode/reasoning row. Record exact profile name if the harness requires one and the effective model/reasoning it exposes.

  If the harness cannot expose the exact medium setting for a family, use its one canonical general-purpose route, record the effective setting, and do not search all alternative profiles. If the family itself is unavailable, record `unavailable` with the observed reason.

- [ ] **Step 2: Run every scenario once on each available family baseline.**

  Record for each run: family, exact model/profile, mode/reasoning, harness/environment, commit SHA, timestamp, evidence source, and rubric dimensions. Do not run every exposed reasoning/profile combination.

- [ ] **Step 3: Diagnose only baseline failures.**

  If a baseline scenario fails, first decide whether the failure is instruction composition, harness capability, or model behavior. Repair instruction composition at its owning source. Rerun the smallest affected scenario/family set. A different reasoning level/profile may be run to diagnose the failure, but label it `diagnostic` and do not add it to baseline completion requirements.

- [ ] **Step 4: Keep model conclusions separate.**

  Do not average Luna/Terra/Sol/Astra into one score that hides regressions. Report per scenario/per family: unnecessary questions, instruction reads, redundant verification, premature stopping, completion quality, scope/authority violations, delegation/model quality, context/time cost.

- [ ] **Step 5: Verify evaluation evidence shape.**

  `py -3 -m pytest tests/test_workflow_contracts.py::TestEvaluationCampaign -q`

  **Green exit:** every available family has one observed baseline result per scenario; unavailable families are explicitly recorded; any remaining failing baseline is either repaired or reported as a concrete observed model limitation rather than silently generalized away.

- [ ] **Step 6: Mark Task 7 checklist items complete in this plan.**

## Task 8: Regenerate, review, hook-validate, and publish the separate Draft implementation PR

**Files:**

- Generated by tooling: marketplace manifests, bundle manifests, installed skills, repository indexes, and `INDEX.md` mesh.
- Modify: `.agents/plans/2026-09-06-mark-373-operating-system.md` to check off delivered implementation steps.

**Consumes:** completed Tasks 1-7.

**Produces:** a separate committed, regenerated, GitHub-visible Draft implementation PR into `main` with honest scope and evidence.

- [ ] **Step 1: Confirm implementation branch provenance.**

  This task runs only after PR #311 is approved and merged. Confirm the implementation worktree/branch started from then-current `main`, contains the merged plan, and is not `codex/mark-373-operating-system`.

- [ ] **Step 2: Regenerate marketplace-owned surfaces.**

  `py -3 tools/run.py marketplace --apply`

  Inspect the diff: generated surfaces must reflect canonical authored source; no unrelated plugin content or hand-edited generated output is allowed.

- [ ] **Step 3: Run final focused pre-commit checks, not a duplicate canonical gate.**

  Run:

  - `py -3 -m pytest tests/test_workflow_contracts.py tests/test_validate_agent_mesh.py tests/test_review_preflight.py tests/test_review_preflight_extensions.py -q`
  - `py -3 tools/run.py review-preflight --check`
  - `py -3 tools/run.py mesh --check`

  These are focused/uncommitted proof. Do not immediately run a separate equivalent `ci --check` when a normal hooked commit follows.

- [ ] **Step 4: Self-review the whole change against MARK-373 ownership.**

  Confirm: generic workflow semantics only; downstream Bunch/Rooms/Portfolio/Patch details remain downstream; no private corpus/credential; no Astra-only branch; no hand-edited generated surface; no stale v6.2 active provenance; no caller-strengthened owner gate; no portable repo/machine assumption; no unresolved scanner `defect`; evaluation and CI-parity evidence are honest.

- [ ] **Step 5: Stage and commit normally.**

  `git add -A`, then commit without `--no-verify`. The tracked hook materializes the staged snapshot, applies mechanical CI surfaces, stages its owned generated outputs, and runs the canonical diagnostic check over that staged state. This hooked commit is the broad local proof.

- [ ] **Step 6: Verify committed state without rerunning equivalent broad CI.**

  Run `git status --short --branch`, `git diff --check HEAD^`, `py -3 tools/run.py review-preflight --check`, and `py -3 tools/run.py mesh --check`. Record the committed head SHA and clean-worktree result. If the hook was absent or failed to provide canonical proof, run the repository's canonical CI command as the named fallback/diagnostic and repair the cause.

- [ ] **Step 7: Push and open a separate Draft implementation PR.**

  PR body must link MARK-373, PR #311, BUNCH-152, ROOMS-55, PORT-15, and PATCH-53; name portable contract surfaces changed; summarize the pinned upstream rebase record, structural/evaluation/CI-parity evidence; state downstream adoption is out of scope; include branch and full head SHA.

- [ ] **Step 8: Verify Draft publication and no hosted-CI burn.**

  Read the PR from GitHub. Confirm base `main`, Draft status, head SHA, scope, and that ordinary Draft creation/synchronization did not execute the paid validation job. A skipped Draft workflow/job is acceptable evidence; an automatically running equivalent validation job is a parity/trigger defect.

- [ ] **Step 9: Keep Draft through local review/repair.**

  Continue normal hooked commits while Draft. Promote to Ready only when the current head has canonical hook proof, local review/repair is complete, the fixed evaluation baseline is complete for available families, structural tests are green, scanner defects are closed, and CI parity is green.

- [ ] **Step 10: Treat catchable hosted failure as parity drift.**

  After Ready, hosted CI is paid confirmation. If it finds a failure the local canonical hook reasonably should have caught, repair hook/hosted parity before treating the work as complete.

- [ ] **Step 11: Finish plan state honestly.**

  Mark delivered checkboxes `[x]`, leave any genuinely undelivered item unchecked with a concrete reason, commit the plan update normally, push, and re-read the implementation PR before reporting completion.

## Acceptance Evidence

- Superpowers+ active provenance is rebased onto exactly upstream v6.3.0 commit `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`; any newer upstream observed is recorded but not adopted.
- `.agents/docs/mark-373-superpowers-v6.3-rebase.md` contains a complete per-skill classification/merge record.
- `tests/test_workflow_contracts.py` uses the fixed class partition; interim tasks make only their owned class green and the full file is green after Task 6.
- `tools/workflow_pressure_scan.py` is the scanner implementation; raw JSON and reviewed Markdown use the fixed schema/classifications and no unresolved `defect` remains at readiness.
- Universal design approval, unconditional branch-finish menus/full-suite reruns, message-bound verification, and blanket every-function testing no longer contradict the shared contract.
- Marketplace callers no longer resurrect conditional `iterative-review`, over-scale debugging, force Linear mutation, or absorb unrelated cheap fixes merely because they are cheap.
- Repository validation lifecycle is `focused checks while editing -> hooked commits while Draft -> local review/repair -> Ready -> hosted CI confirmation`.
- `ci-parity.md` proves local/hosted parity through the shared canonical `ci` check registry, not by superficial command-string equality.
- Draft PR validation job is skipped; feature-branch pushes do not trigger `marketplace-validation`; explicit `workflow_dispatch` is not misclassified as an automatic Draft bypass; no other automatic workflow runs the paid equivalent gate during Draft iteration.
- Evaluation baseline is exactly one canonical run per available Luna/Terra/Sol/Astra family at standard/medium where exposed; diagnostic variants do not expand completion scope.
- Observed composed-stack results exist for every available family/scenario; unavailable targets are explicit rather than inferred.
- Generated outputs derive from canonical plugin files and are rebuilt after source edits.
- A normal hooked commit supplies the single broad local proof over the exact staged/committed state; equivalent unchanged-state reruns are not required.
- A separate Draft implementation PR is visible against `main` with verified head SHA; PR #311 remains plan-only.
- The implementation PR preserves all four downstream adoption boundaries.

## Explicit Deferrals

- `BUNCH-152`, `ROOMS-55`, `PORT-15`, and `PATCH-53` adoption changes are not implemented by MARK-373.
- Upstream Superpowers revisions newer than pinned `b36e0829...` are not adopted by this plan.
- Every reasoning/profile permutation is not an evaluation requirement; only the fixed family baseline is required.
- A genuinely unavailable model family may remain unrun, but absence must be recorded explicitly; unavailable is not passed.
- `iterative-review` itself is not redesigned unless its owning applicability contract is internally wrong; stale unconditional callers are in scope.
- Progressive-disclosure work outside roots demonstrated defective by the pressure scan is not a blanket cleanup campaign.
- This plan does not move Bunch domain architecture, Rooms canon/custody, Portfolio visual/public evidence, or Patch creative canon into the shared marketplace layer.

## Plan-Readiness Self-Review

- **Recipient:** worker-ready for GPT-5.6 Luna at medium reasoning; planner-level choices are pinned rather than delegated to execution.
- **Spec coverage:** all ten MARK-373 findings, upstream v6.3 rebase, static pressure scan, observed mixed-model evaluation, Draft/CI economics, preservation/non-goals, and four downstream adoption boundaries map to Tasks 1-8.
- **Five Luna ambiguities closed:** fixed upstream SHA and record path; fixed one-run-per-family evaluation matrix; named pytest class staging; dedicated scanner/tool/schema; concrete marketplace CI parity/trigger criteria.
- **Source custody:** canonical plugin sources are authored; generated surfaces are rebuilt after source edits.
- **Ordering:** pinned upstream rebase -> RED inventory -> shared authority -> validation/publication -> planning/review -> repo callers/CI parity -> observed evaluations -> final regeneration/hooked publication.
- **Validation:** each semantic task owns one focused structural class and a green exit; full structural rerun happens once after source/caller repair, not at every intermediate stage.
- **Authority:** human-owned decisions, repository policy, owning-skill applicability, connector mutation authority, and downstream domain ownership remain distinct.
- **Publication:** PR #311 is plan-only; implementation starts from merged current `main` and opens a separate Draft PR.
- **No unresolved user choice:** implementation discovery is bounded to factual inspection with enumerated outcomes.

**Plan-readiness rating:** 9.5/10 for a Luna executor. Remaining uncertainty is factual repository state at execution time (for example, whether a source file moved or a runtime family is unavailable), and each such uncertainty now has a named evidence source, allowed outcome, and stop condition rather than an open design choice.
