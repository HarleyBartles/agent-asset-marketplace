# MARK-373 Operating-System Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish one model-agnostic operating-system contract in the marketplace so later repository adoption work inherits clear authority, bounded reading, proportionate validation, evidence reuse, review, and Draft-first publication semantics.

**Architecture:** Rebase Superpowers+ onto one pinned upstream v6.3.0 source snapshot, then repair contradictory behavior at the owning skill rather than stacking compensating overrides. Put cross-runtime authority/autonomy in `base-doctrine`, repository validation choreography in `repo-worker-base`, and stage-specific behavior in the owning Superpowers+ skills. Validate deterministic source contracts and observed composed-stack behavior while keeping consumer-repository commands and domain evidence downstream.

**Tech Stack:** Markdown skill/reference assets, pytest structural contract tests, JSON pressure fixtures, Python campaign/scanner tools, upstream Git provenance, Codex CLI trial execution, marketplace/index generators, the tracked pre-commit hook, and GitHub Actions.

**Execution Strategy:** `executing-plans`. One GPT-5.6 Luna executor performs the coupled work in dependency order. This plan is intentionally decision-complete for Luna: consequential choices are pinned here; repository discovery is bounded and has explicit evidence destinations and exit conditions. PR #311 remains plan-only until human approval. After approval, implementation continues on the same branch/worktree and PR #311 remains Draft through implementation and local validation unless the PR has already been merged or closed.

## Luna Execution Contract

1. **Pinned decisions are not rediscovery tasks.** Exact SHAs, paths, test classes, schemas, commands, model IDs, and acceptance conditions in this plan are binding.
2. **Bounded discovery only.** A discovery step names sources, evidence destination, and allowed outcomes. Stop reading when one allowed outcome is established.
3. **Resolve repository facts by inspection.** Do not ask the human about source, git, workflow, hook, generated metadata, test, or tool facts that can be observed.
4. **Escalate only plan-changing decisions.** Ask only if evidence requires changing a pinned upstream revision, MARK-373 scope/authority, a stated invariant, an unauthorized external/destructive action, or a materially different product/architecture decision.
5. **Task exits are binding.** Satisfy the task's named checks and green exit before advancing.
6. **Do not broaden validation opportunistically.** Use named focused checks. Normal hooked commits provide the broad local gate at defined commit boundaries.
7. **Do not broaden the evaluation matrix.** Extra profiles/reasoning levels are diagnostic only after a baseline failure.
8. **Do not edit tests merely to obtain green.** Repair owning source when a test expresses the pinned contract; change a test only when evidence proves the assertion wrong.
9. **Compaction does not reset work.** Resume from the durable checkpoint below; do not replay completed discovery or equivalent unchanged-state validation merely because context was compacted.

## Global Constraints

- MARK-373 owns shared agent workflow semantics; it does not implement BUNCH-152, ROOMS-55, PORT-15, or PATCH-53 consumer adoption.
- The contract remains viable for Luna, Terra, Sol, and Astra without model-specific workflow forks.
- Superpowers+ rebases onto exactly upstream v6.3.0 commit `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`; the audited v6.2 comparison point is `3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9`.
- Newer upstream revisions may be recorded but are not adopted without a human-approved plan change.
- Preserve first-party additions deliberately; do not blindly replace the derivative.
- Owning skills define applicability/safety. Callers may route to a capability but may not bypass or strengthen its owner gate.
- Authority order: explicit human instruction; repository canon/policy for touched surface; owning-skill applicability/safety; caller/runbook routing; generic defaults.
- Continue reversible investigation, diagnosis, repair, focused verification, and already-authorized publication preparation without synthetic approval pauses.
- Human input is required only for unresolved human-owned requirements/authority or before unauthorized destructive, irreversible, permission-changing, or externally consequential actions.
- Portable skills must not encode this repository's machine paths or `tools/run.py` commands. Consumers supply their own paths, checks, commit gate, and hosted-CI implementation.
- Canonical authored skill source lives under `codex-marketplace/plugins/<plugin>/`; installed skills, manifests, indexes, and mesh are generated outputs.
- PR #311 stays Draft during implementation/local repair. Ready is a later evidence-backed transition.
- Where hosted CI is billed, Draft iteration must not trigger the paid validation loop. The tracked local hook materially mirrors hosted CI and alternate automatic triggers must not bypass Draft policy.
- Preserve meaningful RED/GREEN behavior without ceremonial direct tests for code with no independent behavior/contract.
- Do not create an Astra-only overlay, alternate stack, or model conditional.

## Downstream Contract Map

| Issue | Repository-owned meaning | MARK-373 export |
|---|---|---|
| `BUNCH-152` | DDD, CQRS, event sourcing, replay, persistence, API/domain evidence | authority, routing, focused/hooked/state-bound evidence, Draft-first publication |
| `ROOMS-55` | three-domain authority, canon/custody, retired workflow cleanup | owner applicability, human boundary, progressive reading, review/readiness split |
| `PORT-15` | visual/accessibility/editorial/public-route evidence | generic validation choreography and publication state |
| `PATCH-53` | thin creative-repo adoption and story/canon evidence | smallest shared workflow baseline |

## Fixed Durable Artifacts

- `.agents/docs/mark-373-superpowers-v6.3-rebase.md` — upstream classification/merge record.
- `.agents/plans/2026-09-06-mark-373-operating-system.checkpoint.md` — Luna checkpoint/resume baton.
- `tests/test_workflow_contracts.py` — structural contract tests.
- `tools/workflow_pressure_scan.py` — candidate-only static pressure scanner.
- `tools/run_workflow_pressure_campaign.py` — composed-stack Codex trial runner.
- `tests/pressure/workflow-contracts/red-baseline.md` — initial RED inventory.
- `tests/pressure/workflow-contracts/pressure-scan.json` — raw scan.
- `tests/pressure/workflow-contracts/pressure-scan.md` — classified scan.
- `tests/pressure/workflow-contracts/workflow-inventory.md` — complete Actions/reusable-caller inventory.
- `tests/pressure/workflow-contracts/ci-parity.md` — hook/hosted parity and trigger proof.
- `tests/pressure/workflow-contracts/README.md` — campaign execution/evidence rules.
- `tests/pressure/workflow-contracts/campaign.json` — scenarios and fixed model matrix.
- `tests/pressure/workflow-contracts/prompts/` — scenario prompts.
- `tests/pressure/workflow-contracts/runs/` — raw per-trial evidence.
- `tests/pressure/workflow-contracts/results.md` — reviewed per-family/per-scenario outcomes.

## Checkpoint and Compaction Protocol

Initialize `.agents/plans/2026-09-06-mark-373-operating-system.checkpoint.md` before Task 1 source mutation. After **every task**, update plan checkboxes and rewrite the checkpoint with:

```text
plan: .agents/plans/2026-09-06-mark-373-operating-system.md
branch: <current branch>
head: <git rev-parse HEAD>
last_completed_task: <N>
next_task: <N+1>
next_step: <exact step number/title>
working_tree_status: <git status --short output or clean>
working_diff_sha: <hash of git diff --binary HEAD, or none when clean>
last_green_evidence:
  - <command> => <result> [artifact/reference]
evaluation_head: <sha or not-set>
unresolved_blockers: <none or concrete blocker>
resume_reads:
  - <exact plan section/task/reference needed next>
```

After each green exit: mark task boxes `[x]`; run `git diff --check`; record `HEAD`, `git status --short`, a content hash of `git diff --binary HEAD`, untracked paths, and only evidence establishing that task's claim; then point `next_task`, `next_step`, and `resume_reads` to the minimum next material.

After compaction/restart/handoff: read checkpoint first; then this plan's Luna contract, Global Constraints, the named next task, and checkpoint `resume_reads`; compare live `git rev-parse HEAD` and `git status --short` to checkpoint; inspect/reconcile any difference; reuse completed evidence while relevant state/environment is unchanged; continue at `next_step`.

Task 6 creates a normal hooked **evaluation checkpoint commit** after structural green. Task 7 trials run from exactly that immutable commit. If Task 7 exposes an instruction-composition defect, repair the owner, run its focused test, make another hooked repair commit, update `evaluation_head`, and rerun only affected trials.

## Structural Test Partition

`tests/test_workflow_contracts.py` uses these pytest classes:

- `TestAuthorityBootstrapPortability` — Task 3.
- `TestValidationTddPublication` — Task 4.
- `TestPlanningDelegationReview` — Task 5.
- `TestRepositoryCallersAndPressure` — Task 6.
- `TestEvaluationCampaign` — Task 2 fixture/runner schema and Task 7 evidence shape.

Task 2 runs the whole file once to record RED. Tasks 3-6 run only their owned class and require it green; later-task failures are expected. Task 6 runs the whole structural file once and requires full green before the evaluation checkpoint commit.

## Canonical Evaluation Matrix and Codex Semantics

The baseline is one general-purpose run per family, not every profile/effort combination.

| Family | Codex `--model` | Requested reasoning effort | API reasoning mode evidence |
|---|---|---|---|
| Luna | `gpt-5.6-luna` | `medium` | observed value if emitted; otherwise `unobservable` |
| Terra | `gpt-5.6-terra` | `medium` | observed value if emitted; otherwise `unobservable` |
| Sol | `gpt-5.6-sol` | `medium` | observed value if emitted; otherwise `unobservable` |
| Astra | `gpt-6-astra` | `medium` | observed value if emitted; otherwise `unobservable` |

Do **not** use `standard` as a claimed observed Codex property. Current Codex exposes model selection and reasoning-effort configuration; Responses API `standard`/`pro` reasoning mode is a separate API concept and is not assumed observable from CLI. The runner requests no Pro override. Absence of a Pro request is not proof that an underlying API mode was `standard`. Store `api_reasoning_mode: "unobservable"` unless runtime event/metadata explicitly supplies it. Do not substitute service tier or profile name for reasoning mode.

No specialist profile is used for baseline. Direct `--model` selects each family. If the exact requested model is unavailable, record `unavailable` with CLI evidence and do not substitute another family. Additional profiles/efforts are diagnostic only after a baseline failure.

## Pressure Campaign Runner Contract

Task 2 creates `tools/run_workflow_pressure_campaign.py` with:

```text
py -3 tools/run_workflow_pressure_campaign.py \
  --campaign tests/pressure/workflow-contracts/campaign.json \
  --output-root tests/pressure/workflow-contracts/runs \
  --head <evaluation-head>
```

Optional diagnostic filters: `--family luna|terra|sol|astra` and `--scenario <scenario-id>`.

For each family/scenario pair the runner must:

1. Create a fresh disposable detached git worktree at exactly `--head` under the system temp directory. Trials never share mutated worktrees.
2. Create `runs/<head>/<family>/<scenario-id>/` in the controlling worktree.
3. Compose prompt from `campaign.json` plus `prompts/<scenario>.md`; one trial equals one fresh Codex conversation.
4. Launch with `subprocess` argv, never shell interpolation:

```text
codex exec
  -C <disposable-worktree>
  --ephemeral
  --json
  --model <exact matrix model>
  -c model_reasoning_effort="medium"
  -c hide_agent_reasoning=true
  --sandbox <scenario sandbox from campaign.json>
  --output-last-message <absolute-run-dir>/final.txt
  -
```

Prompt goes on stdin. Do not request/persist hidden chain-of-thought. `--json` stdout is the observable event/tool-state trace.

5. Capture stdout verbatim as `events.jsonl`, stderr as `stderr.txt`, final output as `final.txt`, metadata as `meta.json`.
6. `meta.json` contains schema version, scenario, family, requested model, observed/resolved model if emitted, requested/observed effort, `api_reasoning_mode` or `unobservable`, Codex version, sanitized argv, sandbox, trial head, controlling head, timestamps, exit code, availability status.
7. Remove disposable worktree only after evidence is safely written. Record cleanup failure without deleting evidence.
8. Reserve `unavailable` for observed model/runtime capability absence; a scenario failure is a failed result.

After each trial, Luna adjudicates observable `events.jsonl` + `final.txt` against the predeclared rubric and writes `score.json`. This is executor scoring from evidence, never model self-rating. `results.md` summarizes/links raw runs.

## Task 1: Rebase Superpowers+ onto pinned upstream v6.3

**Files:** `codex-marketplace/plugins/superpowers-plus/`, `.agents/docs/mark-373-superpowers-v6.3-rebase.md`, derivative provenance, checkpoint.

- [ ] **1. Initialize checkpoint.** Record current branch/head/status; `last_completed_task: 0`; `next_task: 1`.
- [ ] **2. Retrieve upstream by one fixed mechanism.** Resolve system temp with `py -3 -c "import tempfile; print(tempfile.gettempdir())"`; use `<system-temp>/mark-373-superpowers-upstream`; clone `https://github.com/obra/superpowers.git` with history sufficient for both pinned commits, e.g. `git clone --filter=blob:none <url> <temp-dir>`.

  Do not add an upstream remote to marketplace; do not merge/cherry-pick/subtree-import upstream history. Verify both objects with `git -C <temp-dir> cat-file -e <sha>^{commit}` and compare exactly `3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9` -> `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`. If pinned v6.3 cannot be retrieved or does not match the audited source, stop with that concrete blocker. Newer upstream is record-only.

- [ ] **3. Write rebase record before source mutation.** Table columns: `upstream path | upstream change | existing first-party delta | disposition | canonical destination | validation`. Disposition: `accept-upstream`, `preserve-first-party`, `manual-merge`, or `not-applicable`.
- [ ] **4. Classify every upstream-changed skill/path.** Pay particular attention to brainstorming scaling, SDD rulings/not-stalls, pre-dispatch conflict scan, microtask batching, reviewer evidence reuse, worktree cleanup, compression, testing guidance, Codex/event behavior. No changed path remains unclassified.
- [ ] **5. Apply classified changes deliberately to canonical Superpowers+ source.** Temporary clone is read-only source material; manually merge/copy accepted content; preserve first-party owners where classified; update active provenance to v6.3.
- [ ] **6. Run smallest existing marketplace/skill structural/regeneration checks proving rebased baseline well formed.** Record exact commands/results; no broad repo gate solely because Task 1 ended.
- [ ] **7. Remove temporary clone** after durable record/source application no longer needs it.
- [ ] **8. Green exit/checkpoint.** All changed paths classified; active provenance pinned v6.3; focused checks green; checkpoint -> Task 2.

## Task 2: Create staged RED tests, scanner, campaign fixture, and runner

**Files:** `tests/test_workflow_contracts.py`, `tools/workflow_pressure_scan.py`, `tools/run_workflow_pressure_campaign.py`, `tests/pressure/workflow-contracts/**`, checkpoint.

- [ ] **1. Create five fixed pytest classes.** Assert classify-before-bootstrap; authority; owner applicability; autonomy; state-bound evidence; focused/hooked/hosted proof; Draft-first publication; recipient-relative planning; evidence-backed adjudication; delegation/model separation; proportionate TDD; non-universal design approval; branch-finish evidence reuse; repo caller behavior; scanner/evaluation schemas; workflow inventory coverage; Draft-CI anti-bypass.
- [ ] **2. Create pressure scanner.** Candidate patterns include approval waits, `full test suite`, repeated validation, every-function testing, universal startup reads, `MUST READ`, unconditional connector/skill calls, personal paths, repo commands in portable skills. JSON fields: `path`, `line`, `pattern`, `context`. Raw hits do not fail the scanner.
- [ ] **3. Classify scan findings** as `defect`, `intended`, `repo-local`, or `deferred`; deferred requires reason/owner; unresolved `defect` blocks Task 6.
- [ ] **4. Create campaign scenarios/prompts.** Include trivial docs correction; specified bug/focused RED; genuine ambiguity; wrong reviewer finding; authorized Draft PR creation; compaction resume; unauthorized destructive work; bounded parallel work; small reversible change; repo vs portable rule; tiny no-approval design case; branch finish with valid evidence; no-independent-behavior helper. Each declares expected authority, next action, evidence scope, sandbox, rubric.
- [ ] **5. Implement runner exactly to the contract above.** Add `TestEvaluationCampaign` unit tests for argv construction, model mapping, run schema, `unobservable` mode, unavailable handling, worktree isolation, filters. Use fake Codex process; no live model spend in Task 2.
- [ ] **6. Capture initial RED:** `py -3 -m pytest tests/test_workflow_contracts.py -q`; write failing tests/classes and owning tasks to `red-baseline.md`.
- [ ] **7. Run scanner/classify hits.**
- [ ] **8. Green exit/checkpoint.** Fixture/runner/scanner schema tests green; RED durably recorded; checkpoint -> Task 3.

## Task 3: Establish authority, applicability, bounded reading, autonomy

- [ ] Add `base-doctrine/references/operating-contract.md` with authority order, owner applicability, reversible-work autonomy, human stop boundary, model-agnostic scope.
- [ ] Reduce `base-doctrine/SKILL.md` to bounded routing without eager reference loading.
- [ ] Refactor `using-superpowers-plus`: classify first; inspect only environment dimensions that can change route; read only selected owner references; stop when next lawful action known.
- [ ] Repair only scanner/source-demonstrated progressive-disclosure/portability defects in broad roots such as `connector-safety`/`writing-skills`.
- [ ] Run `py -3 -m pytest tests/test_workflow_contracts.py::TestAuthorityBootstrapPortability -q`.
- [ ] **Green exit/checkpoint:** owned class green; no unresolved Task-3 defect; checkpoint -> Task 4.

## Task 4: Export validation, TDD, evidence reuse, Draft publication

- [ ] Add `repo-worker-base/references/repository-validation-contract.md`: consumer supplies focused map, tracked gate, hosted workflow, Draft anti-bypass, state identifiers. Sequence: focused slice -> normal hooked commit -> reuse unchanged proof -> Draft local review/repair -> Ready on current local proof -> hosted confirmation.
- [ ] Update `repo-worker-base` as bounded choreography owner; consumers own commands/domain evidence.
- [ ] Make verification state-bound: tested state, command/scope, relevant environment, result; repeat only for change, failure, unresolved concern, nondeterminism, environment drift, or different claim.
- [ ] Preserve RED/GREEN while removing every-function ceremony; trivial glue may be transitively covered.
- [ ] Branch finish reuses valid proof and follows already-authorized publication route; destructive discard/unknown destination still requires human decision.
- [ ] Readiness is recipient/stage-relative; authorized implementation PR defaults Draft; Ready is later evidence-backed transition.
- [ ] Encode billed-CI contract and parity-drift semantics.
- [ ] Run `py -3 -m pytest tests/test_workflow_contracts.py::TestValidationTddPublication -q`.
- [ ] **Green exit/checkpoint:** class green; checkpoint -> Task 5.

## Task 5: Make design, planning, delegation, review recipient-relative

- [ ] Scale brainstorming to uncertainty/consequence; remove universal approval for clear bounded work while preserving human product/canon choices.
- [ ] `writing-plans`: always specify observable goal, exclusions, seams, invariants, interfaces, authority, acceptance, task exits. For Luna/lower-capability executors, pre-resolve consequential alternatives, exact evidence homes/commands where known, and finite decision tables. Exact implementation code is optional unless code shape itself is the contract.
- [ ] SDD may make evidence-backed technical ruling before churn cap; preserve ledger/no-silent-discard/reviewer loop; human owns unresolved requirements/authority.
- [ ] Workflow/stage decides whether delegation is warranted; selector chooses least-escalated adequate profile/model/reasoning/context. Sol remains ordinary strong reviewer/orchestrator; Astra exceptional escalation, not renamed default.
- [ ] Agent evaluation uses composed instruction stack, observable outcome rubric, per-scenario/per-model reporting, no model self-score.
- [ ] Run `py -3 -m pytest tests/test_workflow_contracts.py::TestPlanningDelegationReview -q`.
- [ ] **Green exit/checkpoint:** class green; checkpoint -> Task 6.

## Task 6: Align callers and prove complete workflow/CI parity

**Files:** `.agents/runbooks/implementing.md`, `.agents/runbooks/testing.md`, `.agents/runbooks/pr.md` only if required, every `.github/workflows/*.yml|*.yaml`, hook/CI registry, workflow inventory, CI parity, scan classifications, checkpoint.

At plan time the repo has one executable workflow `.github/workflows/marketplace-validation.yml` plus non-executable `INDEX.md`. Current expected facts: PR events `opened/synchronize/reopened/ready_for_review`; job guard `${{ github.event_name != 'pull_request' || github.event.pull_request.draft == false }}`; push `main` only; explicit `workflow_dispatch`; hosted command `tools/run ci --check`. Verify rather than assume this snapshot.

- [ ] Remove ritual freshness/repetition and caller-strengthened conditional workflows; repo callers do not force `iterative-review`, full debugging, stronger TDD, or model routes beyond owner contracts.
- [ ] Return Linear mutation authority to Linear owner; scope honesty remains. Bound fix-while-here to low-risk mechanically bounded touched-surface fixes, not new product/architecture/migration/validation campaigns.
- [ ] **Enumerate complete workflow surface** into `workflow-inventory.md`: every tracked workflow YAML path; triggers; `workflow_call`; jobs; validation command/called workflow; Draft guard; branch push; manual/scheduled/dispatch behavior; paid-equivalent status.
- [ ] Search repo for local reusable `uses: ./.github/workflows/...`, `workflow_call`, `workflow_run`, `pull_request_target`, `repository_dispatch`, `schedule`, scripted `gh workflow run`, Actions dispatch API calls, and other automation invoking equivalent CI. Classify each hit as executable caller, manual-only, docs/test fixture, or irrelevant. `TestRepositoryCallersAndPressure` must fail if a tracked workflow YAML is absent from inventory.
- [ ] **Prove command parity** in `ci-parity.md`: hosted workflow/command, hook sequence, shared CI registry source, hosted `ci --check` target sequence, local `ci --apply` + `ci --check --diagnostics` target sequence, differences. Material mirror means both check paths use the same canonical CI registry after mechanical apply; diagnostics/fail-fast may differ; local may not omit hosted target.
- [ ] **Prove anti-bypass from full inventory** with table `workflow/caller | event | branch/state | automatic? | paid-equivalent? | runs during Draft? | rationale`. Green requires Draft PR validation skipped; Ready may run; feature branch push cannot auto-run equivalent paid validation; explicit manual dispatch classified separately; no inventory row auto-runs equivalent paid validation during Draft iteration.
- [ ] Run `py -3 -m pytest tests/test_validate_agent_mesh.py tests/test_review_preflight.py tests/test_review_preflight_extensions.py -q`, `py -3 tools/run.py mesh --check`, and `py -3 -m pytest tests/test_workflow_contracts.py::TestRepositoryCallersAndPressure -q`.
- [ ] Run full `py -3 -m pytest tests/test_workflow_contracts.py -q` once. Repair earlier-owner failure at owner; rerun failing class; then full file once.
- [ ] No unresolved scanner `defect` remains.
- [ ] **Create hooked evaluation checkpoint commit.** Update plan/checkpoint through Task 6, stage intended Tasks 1-6, commit normally without `--no-verify`; do not duplicate full gate immediately before/after successful hook.
- [ ] After commit, set checkpoint `evaluation_head` to `git rev-parse HEAD`; checkpoint -> Task 7.

**Green exit:** full structural file green; workflow inventory complete; parity/anti-bypass green; no scanner defect; hooked evaluation checkpoint commit exists.

## Task 7: Run fixed composed-stack pressure campaign

- [ ] Read immutable `evaluation_head` from checkpoint; do not run from dirty/moving state.
- [ ] Run:

```text
py -3 tools/run_workflow_pressure_campaign.py \
  --campaign tests/pressure/workflow-contracts/campaign.json \
  --output-root tests/pressure/workflow-contracts/runs \
  --head <evaluation_head>
```

  Runner directly selects family via Codex `--model`; Luna does not switch itself/search profiles. It requests medium reasoning and captures JSONL observable event/tool traces, stderr, final output, metadata.

- [ ] Review each run against predeclared rubric; write `score.json`; summarize in `results.md` per family/scenario: unnecessary questions, reads before useful work, redundant verification, premature stop, completion quality, scope/authority violations, delegation/model quality, context/time cost.
- [ ] Record reasoning-mode evidence honestly: explicit runtime value if emitted, else `api_reasoning_mode: "unobservable"`; never infer `standard` from no Pro request/service tier/profile.
- [ ] Diagnose only baseline failures: instruction composition vs harness capability vs model behavior. Repair owner + focused test + hooked repair commit + new `evaluation_head`; rerun only affected trials. Alternate profiles/efforts are diagnostic, not baseline requirements.
- [ ] Only actual inability to run exact family is `unavailable`; scenario failure remains failure; no substitution.
- [ ] Run `py -3 -m pytest tests/test_workflow_contracts.py::TestEvaluationCampaign -q`.
- [ ] **Green exit/checkpoint:** one observed baseline per scenario per available family; unavailable families concretely evidenced; remaining failed baseline honestly recorded as model limitation; checkpoint -> Task 8.

## Task 8: Regenerate, review, hook-validate, publish, promote PR #311

- [ ] Confirm human approval to implement and PR #311 still open Draft. If merged/closed before implementation, create fresh branch from then-current `main` carrying approved plan instead of mutating closed/merged branch.
- [ ] `py -3 tools/run.py marketplace --apply`; inspect generated diff for canonical-source-derived changes only.
- [ ] Final focused/uncommitted checks: `py -3 -m pytest tests/test_workflow_contracts.py tests/test_validate_agent_mesh.py tests/test_review_preflight.py tests/test_review_preflight_extensions.py -q`, `py -3 tools/run.py review-preflight --check`, `py -3 tools/run.py mesh --check`. No duplicate full CI when normal hooked commit follows.
- [ ] Whole-change self-review: shared semantics only; downstream specifics downstream; no secret/private corpus; no Astra fork; no generated hand edit; no stale active v6.2; no caller-strengthened owner; no portable machine/repo assumption; no scanner defect; inventory/parity/evaluation honest.
- [ ] Update plan/checkpoint to final local state, stage intended tree, commit normally. Hook is broad local proof; do not bypass/duplicate.
- [ ] Verify committed state with `git status --short --branch`, `git diff --check HEAD^`, `py -3 tools/run.py review-preflight --check`, `py -3 tools/run.py mesh --check`; record full SHA. If hook absent/not canonical, run canonical CI as named fallback and repair cause.
- [ ] Push/update PR #311. Body links MARK-373/BUNCH-152/ROOMS-55/PORT-15/PATCH-53; names portable surfaces; summarizes rebase, structural/scanner/workflow/parity/evaluation evidence; downstream adoption out of scope; branch/full SHA.
- [ ] Verify GitHub base `main`, Draft, head SHA, scope, and no paid-equivalent validation ran automatically during Draft sync. Skipped Draft job acceptable; automatic equivalent job is defect.
- [ ] Keep Draft through further local repair; each repair gets focused validation then hooked commit; reuse unchanged evidence.
- [ ] Promote Ready only when current head has canonical hook proof, local review complete, available-model pressure evidence complete, workflow/parity green, no parity defect. Hosted CI then confirms.
- [ ] Hosted failure that local hook reasonably should catch is hook/CI parity drift to repair.

## Acceptance Evidence

- Superpowers+ is based on exactly `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`, compared from `3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9`, retrieved by off-repo temporary clone with no persistent upstream remote/history import.
- Every upstream-changed path has durable disposition/rationale.
- Structural tests prove shared authority/bootstrap/validation/planning/publication/caller contracts.
- Pressure candidates are classified, not silently ignored.
- Universal design approval, message-bound verification, unconditional branch-finish full-suite reruns, blanket every-function testing, caller-forced conditional workflows, automatic Linear mutation, and unbounded cheap-fix behavior no longer contradict owners.
- Checkpoint survives compaction with branch/head/dirty-state/evidence/next-step; compaction does not trigger evidence replay.
- Campaign runner launches one ephemeral Codex trial per family/scenario from fresh detached worktrees at `evaluation_head`, selects exact models with `--model`, requests medium reasoning, captures JSONL event/tool traces/final output without hidden chain-of-thought, and records API reasoning mode only when observable.
- One baseline result per scenario exists for each available Luna/Terra/Sol/Astra family; unavailable families are evidenced; no aggregate hides weaker-family regression.
- Workflow inventory enumerates every current executable Actions workflow and discovered reusable/dispatch caller capable of paid-equivalent validation; structural test detects unrecorded workflow YAML.
- CI parity is proven through shared canonical CI registry, not command-string similarity; Draft PRs/feature pushes cannot automatically burn equivalent paid loop; manual dispatch classified separately.
- Hooked evaluation checkpoint and final commits provide broad local proof over exact states; unchanged-state equivalent reruns are not required.
- PR #311 stays Draft during implementation and becomes Ready only after local completion; hosted CI is confirmation, not debugging loop.
- Consumer adoption remains out of scope.

## Explicit Deferrals

- BUNCH-152, ROOMS-55, PORT-15, PATCH-53 implementation.
- Superpowers revisions beyond pinned v6.3.0.
- `iterative-review` redesign unless its owning applicability contract is proven internally wrong; stale callers remain in scope.
- Broad progressive-disclosure cleanup outside scanner-demonstrated roots.
- Extra reasoning/profile matrix runs except baseline-failure diagnostics.

## Plan-Readiness Self-Review

Consequential choices are pinned for Luna-medium: upstream source/import mechanism, comparison SHAs, evidence homes, test partition, scanner vocabulary, checkpoint/resume, model IDs, Codex invocation, reasoning-mode evidence semantics, trial isolation/trace capture, complete workflow inventory, CI parity, commit boundaries, and Draft lifecycle. Remaining discovery is bounded to observed facts: exact upstream overlap, scanner-demonstrated roots, live Codex model availability, and current workflow/caller inventory.

**Plan-readiness rating:** 9.5/10. Remaining uncertainty is execution evidence, not unresolved planner choice.
