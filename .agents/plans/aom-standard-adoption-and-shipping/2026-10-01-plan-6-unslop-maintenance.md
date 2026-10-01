# Unslop Maintenance Across Agents Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make AOM's Unslop standard usable as a durable, cross-agent feedback loop without requiring a particular profile schema, ambient authoring capability, or migration of this repository's legacy adoption.

**Architecture:** Keep the pledge and portable lifecycle guide in the Agent Operating Model plugin, and update Unslop+ capabilities to discover profiles using the repository's pinned standard authority while preserving historical v1 behavior. When a repository has adopted Unslop, profile application will help each agent record distinct occurrences and assess routing, reach, and effectiveness; proposals remain consumer-reviewable and generic ambient profiles remain independently usable.

**Tech Stack:** Markdown standard and skills, evaluator/pressure scenarios, existing Marketplace package builder and repository gate.

**Spec:** [Approved AOM design](../../specs/2026-09-30-aom-standard-adoption-and-shipping.md), section 6.11 and acceptance criterion in section 8.

**Roadmap:** [AOM adoption and shipping](roadmap.md), Plan 6. Plan authored after Plan 5 closeout at `b9302b508`; implementation baseline is Plan 5 reviewed head `535c04253`.

**Execution Strategy:** `executing-plans` - profile discovery, occurrence recording, and engine guidance share the same pinned-authority and lifecycle boundary. The focused scenarios should be authored first and used to keep the connected skill guidance coherent; independent task handoffs would add context reconstruction without a useful review seam.

## Global Constraints

- `.agents/unslop/` is canonical; a small repository may use `.agents/unslop/repo.md`, and larger repositories may split by slop class.
- Adoption requires durable observations across agents and sessions that distinguish distinct occurrences from duplicate reports and capture whether a guard was reached, read, followed, and effective when knowable.
- Profiles are actionable guards for encountered recurring mistakes, with recognition cues, corrective behavior, applicability, and false-positive boundaries; no fixed heading schema is required.
- Profile lifecycle decisions are evidence-based and dynamic. Do not turn profiles into incident logs, counters, telemetry, static speculative inventories, or automatic edits.
- Missing routing, ineffective guidance, and useful-but-ignored guidance are distinct diagnoses. Runbooks/playbooks route profiles where those surfaces exist; otherwise use another effective repository route.
- Each adopter owns implementation and self-certification. Ambient Unslop+ availability does not imply adoption or require a particular skill invocation.
- Respect each repository's immutable pinned definition. Preserve legacy v1 behavior; a current skill refresh cannot silently apply a newer standard or migrate this Marketplace's consumer implementation.
- Do not change `.agents/contracts/operating-standards.json`, `.agents/contracts/unslop.json`, `.agents/standards/`, Marketplace consumer routing, or other repositories. Plan 7 owns this repository's migration.
- Edit canonical source under `skills/`; regenerate plugin projections with `py -3 tools/run.py marketplace --apply`. Do not edit `dist/` directly.

## Review Focus

- Repeated reports of one incident must not manufacture recurrence; the occurrence scenario covers duplicate reports versus distinct evidence.
- A profile that exists but was never routed must be diagnosed as a reachability failure, while a read but ineffective guard needs revision and a useful ignored guard needs a decision-point correction.
- A v2 adopter's behavior must be governed by its immutable pinned definition even when the current skill package is newer; preserve the existing v1 deployed-contract route.
- Without an adopted Unslop subscription, generic ambient profiles remain usable, but repository-specific occurrence logging and certification obligations must not be inferred.
- The fallback lifecycle guide and maintenance process must remain usable with no Unslop+ authoring skill available.

## File and Interface Map

| Owner                                                                      | Deliverable                                                                                                                                   |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `skills/unslop/references/standard.md`                                     | Correct, self-contained Unslop pledge and optional-support boundary, updated only if scenario review exposes a gap                            |
| `skills/unslop/references/profile-management.md`                           | Portable instructions for distinct occurrence capture, cross-agent pattern evaluation, guard effectiveness diagnosis, and lifecycle decisions |
| `skills/unslop-profiles/SKILL.md`                                          | Pinned-version-aware consumer profile discovery and conditional maintenance loop, preserving generic profile application outside adopters     |
| `skills/unslop-profiles/tests/pressure/`                                   | Evaluator scenarios for v1/v2 authority, cross-agent recurrence, diagnoses, and ambient-provider absence                                      |
| `skills/unslop-engine/SKILL.md` and `skills/unslop-engine/tests/pressure/` | Pinned authority routing and consumer-reviewable profile lifecycle proposal boundary                                                          |
| Generated Unslop, Unslop+ plugins                                          | Rebuilt projections only                                                                                                                      |

## Task 1: Capture the cross-agent maintenance contract in scenarios

**Files:**

- Create: `skills/unslop-profiles/tests/pressure/cross-agent-occurrence-maintenance.md`
- Modify: `skills/unslop-profiles/tests/pressure/consumer-profile-discovery.md`
- Modify: `skills/unslop-profiles/tests/pressure/optional-provider-absent.md`
- Read: `skills/unslop/references/standard.md`
- Read: `skills/unslop/references/profile-management.md`
- Read: `skills/repo-standards/references/source-resolution.md`

**Consumes:** Approved section 6.11, current profile discovery behavior, and pinned v1/v2 source resolution.

**Produces:** Concrete evaluator inputs and expected behaviors before changing skill guidance.

- [x] Add a scenario with multiple agents/sessions encountering distinct instances of the same failure, plus duplicate reports of one incident. Require the agent to connect distinct evidence, avoid double-counting duplicates, and decide whether independent recurrence warrants a profile change.
- [x] Include a profile that was absent from the workflow route, a profile that was reached/read but ineffective, and useful guidance that was ignored. Require different responses for each case.
- [x] Extend consumer discovery coverage for v2 subscriptions to use the exact pinned definition and certification, including a pin older than the currently installed definition; preserve the existing v1 deployed-contract scenario.
- [x] State that non-adopters may still apply matching generic ambient profiles but do not gain repository occurrence-recording obligations from that availability.
- [x] Ensure the provider-absent scenario demonstrates that the AOM fallback guide is sufficient to maintain the process without an authoring skill.

## Task 2: Make the AOM management guide an executable fallback

**Files:**

- Modify: `skills/unslop/references/profile-management.md`
- Modify only if needed: `skills/unslop/references/standard.md`
- Test: Task 1 pressure scenarios

**Consumes:** Task 1 scenarios and spec section 6.11.

**Produces:** A standalone lifecycle guide that an adopter can follow without Unslop+.

- [x] Define the minimum useful occurrence record in prose: enough task/surface/evidence context to distinguish an incident, connect it to a candidate or existing pattern, and record guard availability/reach/read/follow/effect when known. Do not prescribe fixed fields or a new observation schema.
- [x] Explain how agents across sessions compare occurrences, distinguish independent recurrence from duplicate reports, and retain candidate observations while evidence is insufficient.
- [x] Give distinct next actions for missing routing, ineffective correction, and ignored useful guidance; include revision, narrowing, consolidation, and retirement based on evidence.
- [x] Preserve `.agents/unslop/repo.md` as a sufficient small-repository shape and explain splitting by class only when it improves discovery or ownership.
- [x] Keep profile authoring and edits reviewable by the repository's human/agent-owned process; do not imply automatic file modification, counters, or telemetry.
- [x] Re-read standard and guide together; the standard already states the pledge clearly and required no change.

## Task 3: Update profile discovery and adopter maintenance behavior

**Files:**

- Modify: `skills/unslop-profiles/SKILL.md`
- Test: `skills/unslop-profiles/tests/pressure/consumer-profile-discovery.md`
- Test: `skills/unslop-profiles/tests/pressure/cross-agent-occurrence-maintenance.md`
- Test: `skills/unslop-profiles/tests/pressure/optional-provider-absent.md`

**Consumes:** Task 1 scenarios, Task 2 portable guide, and repo-standards source-resolution contract.

**Produces:** An application capability that preserves version authority and participates in an adopter's feedback loop.

- [x] Replace v2 reliance on `.agents/contracts/unslop.json` with routing through `repo-standards` to the subscription's immutable pinned definition and certification. Read only profile locations and routes supported by that pinned definition and repository implementation.
- [x] Preserve the v1 path using its historical deployed definition/resources; never interpret an old pin through current AOM requirements or run today's scaffolder as an upgrade.
- [x] When Unslop is adopted, tell agents doing relevant repository work to record concrete, distinct recurring-failure evidence under `.agents/unslop/`, assess matching guards, and diagnose reach/read/follow/effect when known. Route to the standalone management guide for lifecycle decisions.
- [x] Keep observations concise and evidence-backed. Recognize duplicate reports, separate incidents, and near misses without asserting recurrence or violation beyond the available evidence.
- [x] Preserve independent application of matching bundled generic profiles when there is no consumer adoption; do not create repository-specific logging or certification obligations for non-adopters.
- [x] Preserve applicability boundaries, doctrine/user-intent authority, conflict reporting, and evidence-grounded review behavior.

## Task 4: Align the profile engine with pinned standards and the evidence loop

**Files:**

- Modify: `skills/unslop-engine/SKILL.md`
- Modify: `skills/unslop-engine/tests/pressure/profile-maintenance-boundary.md`
- Test: `skills/unslop-profiles/tests/pressure/cross-agent-occurrence-maintenance.md`

**Consumes:** Tasks 1-3 and the `repo-standards` pinned-source model.

**Produces:** Engine guidance that proposes changes from repository evidence without overriding pinned authority or adopter review.

- [x] Replace the unconditional `.agents/standards/unslop/references/unslop-standard.md` instruction with v1/v2 pinned authority resolution through `repo-standards`, preserving old-v1 deployed resources.
- [x] Clarify that profile proposals draw on the adopter's durable occurrence evidence and observed reach/effect, not merely a text sample count or one agent's impression; duplicates do not count as recurrence.
- [x] Preserve the consumer-review boundary: the engine may propose create/revise/narrow/consolidate/retire actions but does not automatically edit or publish consumer profiles.
- [x] Keep package/sample analysis and profile validation explicitly separate from evidence that an agent followed or violated guidance.
- [x] Update the pressure case to test pinned authority, duplicate versus distinct evidence, and a reviewable proposal based on demonstrated repeated failures.

## Task 5: Build the owning plugin projections and verify focused behavior

**Files:**

- Generate: `dist/plugins/agent-operating-model/`
- Generate: `dist/plugins/unslop-plus/`
- Test: Task 1-4 pressure scenario set

**Consumes:** Completed canonical skill and scenario changes.

**Produces:** Current plugin projections with no source/projection drift.

- [x] Run focused Marketplace validation for Unslop and Unslop+ source structures and linked Markdown resources.
- [x] Evaluate every pressure scenario against the final source guidance; resolve ambiguity where v1, v2, adoption, or provider absence could lead to a different result.
- [x] Regenerate with `py -3 tools/run.py marketplace --apply` and inspect the resulting owning-plugin diffs for source parity.
- [x] Run `py -3 tools/run.py marketplace --check`, `py -3 tools/build_marketplace.py --check`, and `py -3 tools/validate_markdown_links.py --check`. Evaluate the Markdown pressure scenarios with the relevant skill; this repository treats those as evaluator prompts, not pytest cases.
- [x] Do not run the full gate redundantly before a successful hooked commit; the normal commit hook owns it.
- [x] Confirm no consumer subscription, legacy contract, standard deployment, or other repository changed as a side effect.

## Task 6: Whole-range review and closeout

**Files:**

- Modify: this plan's task checkboxes and status
- Modify: `.agents/plans/aom-standard-adoption-and-shipping/roadmap.md`
- Review: full branch diff from the current merge base

**Consumes:** Tasks 1-5, current base, and fresh independent review.

**Produces:** A reviewed Plan 6 slice with accurate plan and roadmap status.

- [x] Run the normal hooked commit path for source changes; preserve the future roadmap and all still-live later work.
- [ ] Obtain a fresh whole-range review against the branch merge base, including standard authority, v1/v2 compatibility, adopter versus non-adopter boundaries, projection parity, and scenario coverage. Fix all Critical and Important findings, then request a fresh review of corrections.
- [ ] Record implementation head and review outcome in the Plan 6 row and mark this plan `completed-awaiting-retirement`; keep Plan 7 and Plan 8 pending.
- [ ] Use the repository planning-artifact completion workflow and task ledger to record each completed plan task with its evidence.
- [ ] Do not claim Linux or hosted-CI evidence here; Plan 8 owns cross-platform closure.
