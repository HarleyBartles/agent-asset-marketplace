# Semantic Planning-Artifact Custody Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make completed-artifact custody a semantically discoverable, opt-in standard with portable guidance that preserves active future work and does not require a marker or an automatic deletion checker.

**Architecture:** Keep the standard definition in the Agent Operating Model plugin and the optional completion capability in the repo-worker pack. The standard says what adopters pledge and self-certify; the capability teaches agents how to recognize completion from whole-artifact scope and repository evidence, then follow the adopter's local lifecycle. Workflow skills route to it only when the repo has adopted the standard or explicitly asks for that process.

**Tech Stack:** Markdown standards and skills, evaluator-only scenarios, existing Marketplace build and validation tools.

**Spec:** [Approved AOM design](../../specs/2026-09-30-aom-standard-adoption-and-shipping.md), sections 4.1-4.2 and 6.10, with acceptance outcomes in section 8.

**Roadmap:** [AOM adoption and shipping](roadmap.md), Plan 5. This plan is written against Plan 4 head `cd9f3fc75`.

**Execution Strategy:** `executing-plans` - the standard, portable behavior, and workflow routing must agree; semantic evaluator cases then exercise their shared contract. Inline execution keeps the linked documentation coherent, with one focused validation cycle and one independent whole-range review.

## Global Constraints

- AOM owns the selectable standard definition; adopters own their implementation, compliance chain, and continuing self-certification.
- Adopting completed-artifact custody requires next-slice retirement for completed plans, specifications, roadmaps, checkpoints, and similar execution artifacts.
- Completion is semantic: assess the entire artifact scope against repository evidence. A marker may record state but is neither the only discovery route nor a prerequisite for recognizing completion.
- Preserve still-live future work. A completed child plan does not complete its parent roadmap; a mixed-scope artifact stays live until its whole scope is complete.
- Preserve planning artifacts through their completing PR. Retire eligible artifacts in the first commit of a later substantive slice only when they are present in that slice's current base tree; branch-only artifacts remain for canonical PR history.
- Promote enduring knowledge before removal, distinguish explicit abandonment from inactivity or rejected scratch work, and remove stale links when artifacts retire.
- The standard is opt-in. Ambient skill availability or a repo selecting another standard does not adopt completed-artifact custody or impose its two-slice lifecycle.
- AOM ships portable guidance as optional support. Do not add a marker-counting or automatic-deletion checker as a substitute for agent judgment and repo self-certification.
- Keep Marketplace source canonical under `skills/`; regenerate plugin projections with the existing build. Do not edit `dist/` by hand.
- Preserve the broader AOM specification and roadmap while future slices remain active. Do not migrate other repositories.

## Review Focus

- Fully checked boxes without repository evidence must not trigger retirement; evaluator scenarios cover stale or misleading completion signals.
- Unchecked boxes with implementation and delivery evidence for the whole scope can still be complete; a merged Plan 3 from the current base is the concrete example.
- A completed leaf plan inside a roadmap with future stages must not retire the roadmap; evaluator scenarios cover both scopes.
- Markers present on active or contradicted work must not authorize deletion; evaluator scenarios cover stale markers.
- A repo without this subscription must not receive the two-slice obligation merely because a portable workflow skill is installed.

## File and Interface Map

| Owner                                                                                                      | Deliverable                                                                                                                                                  |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `skills/completed-artifact-custody`                                                                        | Clear opt-in pledge, semantic requirements, self-certification, and optional-support boundary                                                                |
| `skills/completing-planning-artifacts`                                                                     | Portable completing/successor-slice procedure, semantic candidate classification, and evaluator-only scenarios                                               |
| `skills/repo-worker-base`, `skills/writing-plans`, `skills/executing-plans`, `skills/linear-issue-shaping` | Conditional routing that defers to explicit repo adoption and local policy                                                                                   |
| `skills/iterative-review`                                                                                  | Closeout guidance that follows the consumer's adopted custody policy rather than always deleting before Ready                                                |
| `.agents/plans/iterative-review-trustworthy-green`                                                         | Supply concrete semantic-completion evidence for evaluator scenarios; defer this repo's consumer-side migration to Plan 7                                    |
| Plugin composition and legacy deployment catalog                                                           | Verify the standard and capability are in their owning plugins; identify the old repo-shape completion assets as legacy and leave their retirement to Plan 7 |
| Generated plugins                                                                                          | Agent Operating Model and repo-worker-pack projections only                                                                                                  |

## Task 1: Establish the consumer and base-tree boundary

**Files:**

- Read: `.agents/contracts/operating-standards.json`
- Read: `.agents/plans/iterative-review-trustworthy-green/2026-09-13-plan-3-impact-coverage.md`
- Read: `.agents/plans/iterative-review-trustworthy-green/roadmap.md`
- Read: `src/plugin-definitions/agent-operating-model/contents.json`
- Read: `src/plugin-definitions/repo-worker-pack/contents.json`
- Read: `skills/repo-shape/references/operating-standards-catalog.json`
- Read: `skills/repo-shape/references/repository-shape-manifest.json`
- Read: generated Agent Operating Model skill projections for the current base
- Preserve: current consumer-owned legacy implementation until the explicitly reviewed Plan 7 migration

**Consumes:** Current `origin/main` planning-artifact inventory and repository implementation evidence.

**Produces:** Verified semantic-discovery cases and no accidental application of a new AOM definition to this repo's older pinned implementation.

- [x] Reconfirm the worktree is based on current `origin/main` and inventory the base's plans/specs. Plan 3 in the iterative-review epic has unchecked tasks but its full deliverable is in merged commit `e067435d7` (PR #316); its parent roadmap retains Plans 4-7. The separate deeper-smell plan remains `ready-for-execution` and its fixture/skill changes are absent. The new AOM roadmap/spec/Plans 1-4 are branch-only.
- [x] Preserve those files during this standards-source slice. The Marketplace's old `completed-artifact-custody` subscription is pinned to its current legacy implementation; ambiently changing the standard source does not migrate the consumer. Plan 7 owns the reviewed subscription/certification migration. Use Plan 3 as a semantic test case rather than silently applying the new definition to the consumer.
- [x] Confirm plugin membership: the selectable definition belongs to `agent-operating-model`, the optional behavior capability belongs to `repo-worker-pack`, and the existing repo-shape catalog/checker/template are legacy deployment surfaces. Do not silently migrate their current consumer pins or duplicate their assets into the new standard.

## Task 2: Define the adopter's pledge and AOM support boundary

**Files:**

- Modify: `skills/completed-artifact-custody/SKILL.md`
- Modify: `skills/completed-artifact-custody/references/standard.md`

**Consumes:** Approved spec section 6.10.

**Produces:** A selectable standard that is self-contained and does not imply adoption through ambient capability.

- [ ] State the pledge in terms of what the repo requires agents to do: semantically classify completed artifacts at the next substantive slice, preserve active future work, promote durable knowledge, retire eligible artifacts from current-base history, and maintain safeguards through self-certification.
- [ ] Define completion as the whole artifact's governed scope being done, supported by repository evidence. Name checkboxes, state labels, PR metadata, and similar markers as useful clues only; none is a sole discovery route or deletion authority.
- [ ] Clarify that a roadmap with later work remains live while a completed child plan may be retired, and that artifacts absent from the current base are retained for their completing PR's canonical history.
- [ ] Make runbook/playbook routing conditional on those surfaces existing; make checker and workflow-skill deployment optional; state that ambient availability and other standard subscriptions do not impose this standard.
- [ ] Keep repository self-certification about its actual route, lifecycle measure, and drift controls. Do not prescribe a universal checker, status schema, artifact inventory, or automatic deletion command.
- [ ] State the global discovery requirement: a repo adopting this standard routes root `AGENTS.md` to its subscription and readable certification record, without forcing adoption of the broader doctrine/contracts standard beyond the required record location.

## Task 3: Implement semantic discovery in the optional capability

**Files:**

- Modify: `skills/completing-planning-artifacts/SKILL.md`
- Create: `skills/completing-planning-artifacts/tests/evaluator-only/semantic-discovery-scenario.md`
- Create: `skills/completing-planning-artifacts/tests/evaluator-only/semantic-discovery-rubric.md`

**Consumes:** Task 2 standard definition.

**Produces:** A portable, repo-owned-on-adoption guide for semantic completion review and two-slice handling.

- [ ] Before editing the capability, write the scenario inputs and scoring rubric. The input describes two fixture repos: one whose subscription record selects this standard and one without it whose local doctrine specifies its own closeout. In the adopter, include an unchecked plan whose full deliverable appears in merged source/PR evidence, a completed child inside a roadmap with future work, a fully checked plan whose code is absent, a stale completion marker contradicted by the repo, and a branch-only plan. Combine an end-of-day deadline, sunk implementation effort, and a conflicting PR cleanup instruction. Ask evaluators to return a table with artifact, whole-scope classification, repository evidence, adoption status, and next action. Keep expected dispositions out of the input file.
- [ ] Resolve the evaluator workspace with `py -3 skills/subagent-workspace/scripts/workspace.py --apply .agents/plans/aom-standard-adoption-and-shipping/2026-10-01-plan-5-semantic-planning-artifact-custody.md`. Use `selecting-a-subagent` to select one adequate fresh-context route and hold model, reasoning, prompt, and scenario bytes fixed across reps.
- [ ] Run five no-guidance control reps and five reps with the current capability. Give each a fresh context and only the scenario input. Capture decisions and exact rationalizations off-repo. Confirm the current capability misses the unchecked-but-merged case or wrongly applies the lifecycle without adoption. If the no-guidance control handles a case better, record that as evidence and fix only the existing capability's demonstrated harm; do not claim a behavior gain without it.
- [ ] Narrow the skill's applicability: use it when the repo adopted `completed-artifact-custody` or a human explicitly requests this process; otherwise follow the repository's own policy.
- [ ] Replace marker-only candidate discovery with a scope-first review of repository-declared planning locations plus artifacts explicitly linked by the active plan, issue, PR, or roadmap. Use a marker as a clue, never as the gate.
- [ ] Classify each candidate as complete, still active/mixed, explicitly abandoned, or uncertain. Verify the whole artifact scope against current code, tests, accepted delivery records, and linked future obligations; use `cleanup-custody` for genuinely ambiguous custody.
- [ ] Treat a fully checked plan as a completion signal to verify, not proof. Treat unchecked tasks as historical bookkeeping when repository evidence proves the governed scope shipped. A stale marker cannot override contrary evidence.
- [ ] Retire an artifact only if its whole scope is complete or its abandonment has been explicitly decided, durable content is promoted, and the artifact is present in the successor slice's current base. Keep completed PR plans in the completing PR and keep the parent of live future work.
- [ ] Specify that the successor-slice removal is the first substantive commit in that slice's eventual PR. Update surviving parent roadmaps and remove stale links in that same retirement change. Do not create cleanup-only PRs or automatic deletion machinery.
- [ ] Put expected outcomes and required evidence in the separate rubric: unchecked-but-merged is complete; its parent roadmap remains active; checked-but-unimplemented remains active; a contradicted marker does not authorize removal; a branch-only plan stays through its completing PR; the non-adopter follows only its local policy.
- [ ] Run five fresh-context treatment reps with the updated skill against the same case input and route. Require all classifications and local-policy boundaries in the rubric; use observed failures to refine the wording and repeat the affected reps. Keep only the scenario and rubric as evaluator-only authoring tests; delete evaluator transcripts and outputs from scratch.

## Task 4: Align portable worker routing with explicit adoption

**Files:**

- Modify: `skills/repo-worker-base/SKILL.md`
- Modify: `skills/writing-plans/SKILL.md`
- Modify: `skills/executing-plans/SKILL.md`
- Modify: `skills/linear-issue-shaping/SKILL.md`
- Modify: `skills/iterative-review/SKILL.md`
- Modify: `skills/iterative-review/references/node-closeout.md`

**Consumes:** Task 2 definition and Task 3 capability.

**Produces:** No ambient workflow imposes next-slice retirement on non-adopters; subscribed repos receive routing at completion and new-slice entry.

- [ ] In repo-worker-base, route to the capability only when the repo declares this standard or local policy requests it. Tell non-adopters to follow their repo policy and explicitly state that installed capability is not adoption.
- [ ] In writing-plans and executing-plans, make completion-artifact handling conditional on adoption/local policy. Keep the exact marker available as a recording option, not as a universal completion condition.
- [ ] In linear-issue-shaping, defer retirement timing to repository policy. Describe the adopted two-slice case accurately: retain through the completing PR; retire in the next eligible substantive slice.
- [ ] In iterative-review, replace the unconditional rule against tracked planning artifacts before Ready. Its closeout node must apply the consumer's policy and preserve artifacts through a completing PR when that repo adopted the two-slice standard.
- [ ] Preserve review readiness, evidence, and durable-promotion obligations; change only artifact custody assumptions.

## Task 5: Regenerate and validate the standard package

**Files:**

- Regenerate: `dist/plugins/agent-operating-model/skills/completed-artifact-custody/**`
- Regenerate: `dist/plugins/repo-worker-pack/skills/completing-planning-artifacts/**` and other generated skill projections touched by Task 4
- Test: `tests/shipping/test_aom_standard_assets.py` and repository markdown/link validation
- Evaluator evidence: five no-guidance controls, five current-skill baselines, five treatment reps

**Consumes:** Tasks 1-4.

**Produces:** Consistent canonical skills, standard definitions, generated packages, and no broken planning links.

- [ ] Run evaluator-scenario self-review against every expected classification in the new file; verify no expected outcome depends only on exact marker text, checkbox totals, or a lexical detector.
- [ ] Run focused shipping validation: `py -3 -m pytest tests/shipping/test_aom_standard_assets.py -q`.
- [ ] Run `py -3 tools/run.py marketplace --apply`, then `py -3 tools/run.py marketplace --check`; verify source/generated parity for each changed skill and the standard reference.
- [ ] Run `py -3 tools/validate_markdown_links.py --check`. The changed capabilities do not add bundled executable scripts, so no skill-script validator is needed for this slice.
- [ ] Inspect `git diff --check`, staged paths, planning-artifact status, and generated source parity. Do not run the full CI gate immediately before a normal hooked commit.

## Task 6: Review and close the implementation slice

**Files:**

- Modify: this plan for completion state
- Modify: `.agents/plans/aom-standard-adoption-and-shipping/roadmap.md`

**Consumes:** Passing focused validation, normal hooked commit evidence, and whole-range review.

**Produces:** A reviewed Plan 5 slice recorded as `completed-awaiting-retirement`; no draft PR until Plan 8 closure.

- [ ] Commit Tasks 2-5 through the normal repository hook. Record the resulting implementation head and do not rerun the full gate after a successful hooked commit.
- [ ] Obtain a fresh whole-range review against the approved spec. Fix Critical and Important findings, rerun affected focused validation, and obtain a fresh review after each correction.
- [ ] Mark this plan `completed-awaiting-retirement`, keep it and the approved AOM spec/roadmap tracked for the eventual whole-roadmap PR, and update the Plan 5 roadmap row with commit and review evidence.

**Exit:** The selectable standard states its semantic pledge; an optional portable capability teaches agents to implement it; other standards and ambient skills do not silently impose it.

## Handoff boundaries

- This plan does not change the current Marketplace subscription set, legacy `.agents/standards/` runtime, or its certification. Plan 7 owns that migration after the user reviews the proposed subscription set.
- This plan does not add a script that estimates completion from headings, markers, or checkbox counts.
- Plans 6-8 remain pending and are written just in time; this slice does not create a draft PR or touch other repositories.
