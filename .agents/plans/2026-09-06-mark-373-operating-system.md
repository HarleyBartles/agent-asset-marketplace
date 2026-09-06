# MARK-373 Operating-System Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish a single model-agnostic operating-system contract in the marketplace so later repository adoption work can inherit clear authority, bounded reading, proportionate validation, review, and publication semantics.

**Architecture:** Keep the existing skill ownership graph and repair the original owners of contradictory behavior. Put cross-runtime authority and autonomy in `base-doctrine`, repository-facing validation choreography in `repo-worker-base`, and stage-specific behavior in the owning Superpowers+ skills. Add a compact composed-stack evaluation fixture to prove the contract at the workflow level while leaving domain evidence and repository commands to downstream repos.

**Tech Stack:** Markdown skill/reference assets, JSON evaluation fixtures, pytest structural contract tests, the repository marketplace/index generators, and the tracked pre-commit hook.

**Execution Strategy:** `executing-plans` — the contract edits are coupled through shared authority and generated marketplace surfaces; one executor should make the semantic changes in dependency order and run the full repository gate once at the commit boundary.

## Global Constraints

- MARK-373 is the shared operating-system layer; it does not implement Bunch, Rooms, Portfolio, or Patch repository adoption.
- The contract is model-agnostic and must remain viable for Luna, Terra, Sol, and Astra.
- The owning skill defines its own applicability and safety conditions; callers may request a capability but may not bypass or strengthen that owner gate.
- The authority order is: explicit human instruction; repository canon/policy for the touched surface; owning-skill applicability and safety contract; caller/runbook routing advice; generic defaults.
- Reversible investigation, diagnosis, repair, focused verification, and already-authorized publication preparation continue without synthetic approval pauses.
- Human input is required only for unresolved requirements/authority or before unauthorized destructive, irreversible, permission-changing, or externally consequential actions.
- Portable skills must not encode this repository's `Z:/` paths or `tools/run.py` commands; consumer repositories supply their own concrete paths, focused checks, canonical commit gate, and hosted-CI details.
- Canonical skill source is under `codex-marketplace/plugins/<plugin>/`; generated bundles, manifests, installed skills, indexes, and mesh files are regenerated outputs.
- Implementation PRs are Draft-first. A PR becomes ready only after the current committed head has local canonical hook evidence and completed local review/repair work.
- Do not introduce an Astra-only branch, model conditional, overlay skill, or alternate workflow stack.

---

## Downstream Contract Map

The implementation must make these later adoption boundaries explicit in the plan and PR description:

| Related issue | Later repository responsibility | MARK-373 export |
|---|---|---|
| `BUNCH-152` | DDD, CQRS, event sourcing, persistence, replay, API, and statistical/domain evidence | Authority, applicable-skill routing, focused-slice choreography, hooked commit gate, state-bound proof, and Draft-first publication |
| `ROOMS-55` | Three-domain authority, canon, custody, retired workflow cleanup, and ambiguity ownership | Owning-skill applicability, human-authority boundary, progressive reading, model/delegation separation, and review/readiness distinction |
| `PORT-15` | Visual, accessibility, editorial, public-route, and concrete hooked-gate evidence | Generic validation choreography and publication state; no visual/editorial policy |
| `PATCH-53` | Thin creative-repo adoption, story/canon boundaries, compact validation, and regression proof | The smallest shared baseline; no imported domain hierarchy or creative canon |

## Planned File Map

### Canonical portable source

- Modify `codex-marketplace/plugins/repo-worker-pack/skills/base-doctrine/SKILL.md` to route the new operating contract without duplicating it.
- Create `codex-marketplace/plugins/repo-worker-pack/skills/base-doctrine/references/operating-contract.md` for precedence, owning-skill applicability, model-agnostic autonomy, and the boundary between internal resolution and human-owned decisions.
- Modify `codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/SKILL.md` to expose the repository-facing validation contract.
- Create `codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/references/repository-validation-contract.md` for consumer-supplied focused checks, canonical commit gate, hosted-CI parity, state-bound evidence, and Draft-first lifecycle.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/SKILL.md` to classify before broad environment/doctrine loading and to route only the references needed by the selected mode.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/verification-before-completion/SKILL.md` to bind evidence to tested state instead of conversational message boundaries and to distinguish focused, hooked, and hosted proof.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/publishing-source/SKILL.md` to make an authorized Draft PR the default publication surface without a second Draft/Ready permission question.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/handoff-gates/SKILL.md` to make readiness recipient-relative and require local canonical proof plus completed local review before Draft promotion.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/SKILL.md` to require observable goals, seams, invariants, authority, and acceptance evidence while making implementation-level code recipient-relative.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/SKILL.md` to preserve no-silent-discard and durable rulings while allowing evidence-backed technical adjudication before the churn cap.
- Modify `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/SKILL.md` to state that workflow ownership decides whether to delegate and this skill decides the exact exposed profile/model/reasoning/context route.
- Modify `codex-marketplace/plugins/agentic-evaluation/skills/agent-evaluation/SKILL.md` or its operational reference to describe composed instruction-stack evaluations and per-scenario/per-dimension reporting without claiming model-generalized scores.

### Repository-local contract consumers

- Modify `.agents/runbooks/implementing.md` and `.agents/runbooks/testing.md` so this repository's concrete commands express focused checks during iteration and the hooked canonical gate at commit without ritual full-suite reruns.
- Retain the existing `.agents/runbooks/pr.md` Draft-first and hook policy unless the source edits expose a concrete contradiction; any change must remain a local command/policy overlay, not a second portable contract.
- Create `tests/test_workflow_contracts.py` for deterministic structural checks over the canonical source files and evaluation fixture.
- Create `tests/pressure/workflow-contracts/README.md`, `campaign.json`, `prompts/`, and `results.md` for the composed-stack pressure campaign. The fixture will record scenarios and rubric structure; any model run will be labelled by model, reasoning, environment, and evidence status.

### Generated outputs

- Regenerate `codex-marketplace/` manifests and bundle manifests, `.agents/plugins/marketplace.json`, `.agents/skills/`, repository indexes, and `INDEX.md` mesh only after all canonical source and test edits are complete.

## Task 1: Lock the contract with failing structural tests and an evaluation fixture

**Files:**

- Create: `tests/test_workflow_contracts.py`
- Create: `tests/pressure/workflow-contracts/README.md`
- Create: `tests/pressure/workflow-contracts/campaign.json`
- Create: `tests/pressure/workflow-contracts/prompts/`
- Create: `tests/pressure/workflow-contracts/results.md`

**Interfaces:**

- Consumes the canonical skill paths listed in the file map.
- Produces deterministic assertions that fail on the current contradictory wording and a reusable scenario schema for later RED/GREEN runs.

- [ ] **Step 1: Add structural contract assertions before changing source.**

  Assert that the canonical files expose these exact semantic anchors: classify-before-bootstrap routing; an explicit authority precedence; owning-skill applicability; model-agnostic autonomy; state-bound evidence; focused/hooked/hosted validation distinction; Draft-first publication; recipient-relative planning; early evidence-backed adjudication; and separate delegation/model decisions. Assert that the evaluation campaign contains all ten MARK-373 pressure scenario categories and records per-scenario/per-dimension evidence fields.

- [ ] **Step 2: Run the focused test file to capture RED evidence.**

  Run `py -3 -m pytest tests/test_workflow_contracts.py -q`. The test must fail because the current source still contains the message-bound verification rule, pre-classification bootstrap order, cap-only adjudication wording, and lacks the new repository contract/evaluation fixture.

- [ ] **Step 3: Write the evaluation fixture.**

  Define scenarios for: trivial docs correction; a specified bug whose first focused test fails; genuine ambiguity; a demonstrably wrong reviewer finding; authorized Draft PR creation; resume after compaction; unauthorized destructive work; parallelizable bounded work with mixed profile selection; a small reversible change where a full matrix is wasteful; and a repo-local rule conflicting with a portable skill. For each scenario, include expected authority decision, expected next action, applicable evidence scope, and rubric dimensions for unnecessary questions, instruction reads, redundant verification, premature stopping, completion quality, scope/authority violations, delegation quality, and context/time cost. Keep `results.md` explicit about which runs are observed, unavailable, or illustrative.

- [ ] **Step 4: Mark Task 1 checklist items complete in this plan.**

## Task 2: Establish shared authority, applicability, and autonomy ownership

**Files:**

- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/base-doctrine/SKILL.md`
- Create: `codex-marketplace/plugins/repo-worker-pack/skills/base-doctrine/references/operating-contract.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/SKILL.md`

**Interfaces:**

- Consumes Task 1's failing structural assertions.
- Produces the cross-runtime contract that every later stage and consumer repository can reference.

- [ ] **Step 1: Add the operating-contract reference.**

  State the authority precedence exactly as defined in Global Constraints. Define the owning-skill rule: callers route capability requests, while the skill that owns a capability decides applicability and safety. Define the autonomy rule in operational terms: continue through reversible investigation, diagnosis, repair, focused checks, and authorized publication preparation; ask only for unresolved human-owned requirements/authority or high-risk unauthorized actions. State that this contract applies across Luna, Terra, Sol, and Astra.

- [ ] **Step 2: Reduce `base-doctrine/SKILL.md` to a bounded router.**

  Keep only the reference-selection map, canonical source boundary, and the route to `operating-contract.md`; move cross-runtime operating law out of the root body. Preserve existing durable-doctrine and bounded-read routing without making the root skill load every reference.

- [ ] **Step 3: Refactor `using-superpowers-plus/SKILL.md`.**

  Make request classification the first semantic action. After classification, inspect only environment dimensions that can change the selected route, load the owning doctrine/skill references required by that route, and stop when the next lawful action is known. Remove the requirement to complete broad environment and doctrine loading before classification. Preserve the subagent stop rule and repository/user precedence.

- [ ] **Step 4: Run the focused structural test.**

  Run `py -3 -m pytest tests/test_workflow_contracts.py -q`. The authority/bootstrap assertions must pass while later task assertions remain the only expected failures.

- [ ] **Step 5: Mark Task 2 checklist items complete in this plan.**

## Task 3: Export the repository validation and publication contract

**Files:**

- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/SKILL.md`
- Create: `codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/references/repository-validation-contract.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/verification-before-completion/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/handoff-gates/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/publishing-source/SKILL.md`

**Interfaces:**

- Consumes Task 2's operating contract.
- Produces the portable choreography later repositories will adopt with their own commands and evidence.

- [ ] **Step 1: Add the repository-validation reference.**

  Define a consumer contract with four named inputs: change-class-to-focused-check mapping; canonical commit-gate command or executable; hosted-CI workflow and Draft-skip condition; and state/evidence identifiers. Define the sequence as focused falsifying slice while editing, normal hooked commit over the intended staged tree, reuse while the tested state is unchanged, and hosted CI confirmation after Draft promotion. State that consumer repos own domain-specific evidence and commands.

- [ ] **Step 2: Update `repo-worker-base`.**

  Add a bounded pointer to the new reference and state that repo-worker supplies choreography while each repository supplies concrete validation and path policy. Remove any portable command/path assumptions introduced by the edits.

- [ ] **Step 3: Update `verification-before-completion`.**

  Replace the conversational “run in this message” freshness rule with state-bound evidence: record the tested tree/head/staged state, command and scope, relevant environment, and result. Distinguish focused evidence from the broad hooked commit gate and hosted CI proof. Permit reuse of unchanged proof and require a named reason before broadening or repeating: new changes, failure, unresolved concern, nondeterminism, environment drift, or a different claim.

- [ ] **Step 4: Update `handoff-gates`.**

  Make readiness relative to the recipient and stage. Require current local canonical proof and completed local review/repair before a Draft PR is promoted. Keep the 8/10 floor as a diagnostic handoff threshold, not a reason to invent work or rerun unchanged validation.

- [ ] **Step 5: Update `publishing-source`.**

  Preserve the validation-before-publication gate and make an authorized implementation PR Draft-first by default. Remove any implication that the worker must ask whether an authorized PR should be Draft or Ready; Ready is a later evidence-backed transition.

- [ ] **Step 6: Run the focused structural test.**

  Run `py -3 -m pytest tests/test_workflow_contracts.py -q` and confirm the validation/publication assertions are green.

- [ ] **Step 7: Mark Task 3 checklist items complete in this plan.**

## Task 4: Make planning, delegation, and review composition recipient-relative

**Files:**

- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/SKILL.md`
- Modify: `codex-marketplace/plugins/agentic-evaluation/skills/agent-evaluation/SKILL.md` or its operational reference, selecting the smaller source seam after inspection

**Interfaces:**

- Consumes Tasks 2 and 3's shared authority and evidence semantics.
- Produces stage guidance that can be followed by different model capabilities without changing the contract.

- [ ] **Step 1: Refactor `writing-plans`.**

  Keep plans strong on observable goal, scope/exclusions, source seams, invariants, interfaces, acceptance evidence, authority boundaries, and genuine task decomposition. Make exact implementation code optional and recipient-relative: include it when contractual or when the selected recipient needs it, rather than requiring code transcription for every plan. Preserve the requirement for concrete file paths, commands, validation, and no placeholders when a plan is handed to an executor.

- [ ] **Step 2: Refactor SDD adjudication.**

  Preserve the finding ledger, no-silent-discard rule, reviewer-fix loop, and churn cap. Change the cap-only rule so a controller may record an evidence-backed technical ruling before dispatching a fix when source, tests, or contracts falsify the finding. Route unresolved requirement/authority disputes to the human; never use early adjudication to silently discard a finding.

- [ ] **Step 3: Tighten subagent selection.**

  State separately that the stage/workflow decides whether delegation is warranted and `selecting-a-subagent` chooses the least-escalated adequate exposed profile, model, reasoning, and context route. Preserve runtime inventory as authoritative and do not redefine `strongest` or `reviewer-strong` as Astra.

- [ ] **Step 4: Extend agent evaluation guidance.**

  Add composed instruction stacks as the evaluation unit, require held-out scenarios where practical, and require per-scenario/per-dimension reporting. Keep model-specific observations separate from cross-model conclusions and distinguish rubric evidence from model self-rating.

- [ ] **Step 5: Run the focused structural test.**

  Run `py -3 -m pytest tests/test_workflow_contracts.py -q`; all source-contract assertions must pass.

- [ ] **Step 6: Mark Task 4 checklist items complete in this plan.**

## Task 5: Align this repository's concrete worker and testing overlays

**Files:**

- Modify: `.agents/runbooks/implementing.md`
- Modify: `.agents/runbooks/testing.md`
- Modify: `.agents/runbooks/pr.md` only if a concrete contradiction is found

**Interfaces:**

- Consumes the portable contracts from Tasks 2–4.
- Produces the marketplace repository's concrete command and hook overlay without exporting those commands into portable skills.

- [ ] **Step 1: Define focused checks by touched surface.**

  Keep the repository's canonical `py -3 -m pytest` and `py -3 tools/run.py` commands, but state that focused checks are selected while editing and the full canonical gate is exercised by the normal tracked hook at commit. Preserve direct evidence for marketplace, mesh, script, and security changes where those surfaces are touched.

- [ ] **Step 2: Remove ritual freshness language.**

  Replace instructions that require repeated full suites merely because a new message or stage began. Repeat or broaden only after a new change, failure, unresolved concern, nondeterminism, environment drift, or a different proof claim.

- [ ] **Step 3: Verify the PR overlay remains Draft-first.**

  Keep repository-specific `review-preflight`, hook, hosted-CI skip, and PR-ready commands in the local runbook. Do not duplicate the portable authority contract or add a second Draft/Ready choice.

- [ ] **Step 4: Run local runbook and link checks.**

  Run `py -3 -m pytest tests/test_validate_agent_mesh.py tests/test_review_preflight.py tests/test_review_preflight_extensions.py -q` and `py -3 tools/run.py mesh --check` after the overlay edits. If the mesh check reports stale generated navigation, regenerate it in Task 6 rather than editing an index by hand.

- [ ] **Step 5: Mark Task 5 checklist items complete in this plan.**

## Task 6: Regenerate, validate, review, and publish the Draft PR

**Files:**

- Generated by tooling: marketplace manifests, bundle manifests, installed skills, repository indexes, and `INDEX.md` mesh.
- Modify: `.agents/plans/2026-09-06-mark-373-operating-system.md` to check off delivered steps.

**Interfaces:**

- Consumes all completed canonical source and test work from Tasks 1–5.
- Produces a committed, regenerated, GitHub-visible Draft PR into `main` with honest scope and head evidence.

- [ ] **Step 1: Run the marketplace rebuild.**

  Run `py -3 tools/run.py marketplace --apply` from the MARK-373 worktree. Inspect the diff to confirm generated surfaces reflect canonical source changes and no unrelated plugin content changed.

- [ ] **Step 2: Run focused and structural validation.**

  Run `py -3 -m pytest tests/test_workflow_contracts.py tests/test_validate_agent_mesh.py tests/test_review_preflight.py tests/test_review_preflight_extensions.py -q`. Run `py -3 tools/run.py review-preflight --check` and `py -3 tools/run.py mesh --check` for uncommitted proof. Record failures with their actual state and repair before proceeding.

- [ ] **Step 3: Perform self-review against the related-issue map.**

  Confirm the diff exports only generic workflow semantics; Bunch-specific architecture, Rooms-specific canon/custody, Portfolio-specific visual/public/editorial evidence, and Patch-specific creative-repo details remain downstream. Confirm no private corpus, credential, external secret, Astra-only conditional, or generated-surface hand edit is present.

- [ ] **Step 4: Stage the intended tree and commit normally.**

  Run `git add -A` and commit without `--no-verify`. The tracked hook must materialize the staged snapshot, run `ci --apply`, stage owned generated outputs, and run `ci --check --diagnostics`. Do not run an equivalent full `ci --check` immediately before or after a successful hooked commit.

- [ ] **Step 5: Verify the committed state.**

  Run `git status --short --branch`, `git diff --check HEAD^`, `py -3 tools/run.py review-preflight --check`, and `py -3 tools/run.py mesh --check`. Capture the committed head SHA and confirm the worktree is clean. If the hook was absent or failed to provide canonical evidence, run `py -3 tools/run.py ci --check --diagnostics` as the named diagnostic and repair the cause.

- [ ] **Step 6: Push and open the Draft PR.**

  Push `codex/mark-373-operating-system` to `origin` and create a Draft PR targeting `main`. The PR body must link MARK-373 and the four related issues, identify the portable contract surfaces changed, list the validation evidence, state that downstream repository adoption remains out of scope, and include the published branch and full head SHA.

- [ ] **Step 7: Verify GitHub publication state.**

  Read the created PR from GitHub and confirm its URL, base `main`, branch name, Draft status, head SHA, changed-file scope, and available checks. Do not claim publication from the local push alone.

- [ ] **Step 8: Mark all delivered plan steps complete.**

  Update every completed checkbox in this plan, leave any genuinely undelivered item unchecked with an explicit reason, commit the plan state through the same normal hook path, push the updated head, and re-read the PR before reporting.

## Acceptance Evidence

- The focused structural test demonstrates the shared operating contract and evaluation fixture.
- The marketplace rebuild passes and generated outputs are sourced from canonical plugin files.
- The repository's focused tests, review preflight, mesh check, and normal hooked commit provide fresh state-bound local evidence.
- The Draft PR is visible on GitHub against `main` with a verified head SHA.
- The PR description and plan explicitly preserve the four downstream issue boundaries.

## Explicit Deferrals

- `BUNCH-152`, `ROOMS-55`, `PORT-15`, and `PATCH-53` adoption changes are not implemented in this PR.
- Running the full Luna/Terra/Sol/Astra matrix is not claimed unless actual observed runs and environment details are recorded; the fixture and rubric establish the lane for later execution.
- This plan does not redesign `iterative-review` applicability, visual/public evidence, domain architecture, canon custody, or creative content beyond the shared ownership contracts required for later adoption.

## Plan-readiness self-review

- Spec coverage: all ten MARK-373 findings, the cross-repo contract, Draft-first policy, mixed-model evaluation lane, preservation list, non-goals, and four related adoption boundaries map to Tasks 1–6.
- Source custody: canonical plugin sources are the only authored skill edit points; generated surfaces are rebuilt after source edits.
- Ordering: tests/fixture precede source edits; source and local overlays precede marketplace regeneration; regeneration precedes the hooked commit; publication follows verified commit state.
- Validation: commands are repository-specific and named; portable contract references do not export those commands to consumers.
- Authority: human-owned decisions, repository-owned policy, owning-skill applicability, and downstream domain ownership remain distinct.
- No plan step relies on an unresolved user choice.

**Plan-readiness rating:** 9/10. The issue body and all four related Linear issues provide the contract and non-goals; live repository inspection verified the canonical plugin paths, generated-surface workflow, hook policy, and available test/mesh commands. The remaining uncertainty is limited to which single agent-evaluation operational reference is the smallest source seam, and Task 4 explicitly requires selecting it by inspection before editing.
