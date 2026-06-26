# MARK-305 Worker Skill Stack Recommendation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preflight a narrow repo-local `.agents/skills` worker set for `agent-asset-marketplace`, publish the approved recommendation in MARK-305, and then install/project that approved set into this repository's `.agents/skills` surface after approval so workers benefit immediately. The repo must also carry worker-facing guidance at `.agents/INDEX.md`, `.agents/skills/INDEX.md`, and `.agents/skills/AGENTS.md` so the local worker set is discoverable and maintainable. MARK-305 also has to update the route-state doctrine in `work-mode-router` so the preflight/execution split is sourced from durable markers, not chat memory, and so `/using-superpowers` receives the discovered mode context as the workflow-lane chooser. MARK-303 is folded into this same execution pass by renaming the Linear shaping control-plane skill to `linear-issue-shaping`, repointing active references, and promoting connector-safe Linear shaping BAU. MARK-306 will canonicalize the same approved set as the `marketplace-project-pack` plugin after MARK-305 lands.

**Architecture:** Treat `sources/first_party/skills/` as canonical source custody and `.agents/skills/` as an immediate repo-local install/projection surface. The installed tree should be sourced from durable repo skill custody, not copied as a raw dump, and each installed entry should remain traceable back to an exact canonical source path. Keep the recommended set narrow: only worker control-plane, safety, publication, and anti-slop skills that materially help repo workers in this repository.

**Tech Stack:** Markdown, Linear, Git, PowerShell, first-party skill source custody, and repo-local projection/validation checks.

## Global Constraints

- `.agents/skills` is an immediate repo-local projection surface, not canonical source.
- Worker-facing guidance must live in the repo at `.agents/INDEX.md`, `.agents/skills/INDEX.md`, and `.agents/skills/AGENTS.md`.
- Do not vendor core Superpowers+ skills into the repo-local worker set.
- Keep the recommended set narrow and worker-facing.
- Treat `work-mode-router` as the canonical worker entrypoint for durable mode classification. It classifies route state from Linear/repo evidence and hands off the discovered mode to `/using-superpowers`; it does not choose the Superpowers implementation lane itself.
- Use exact source paths for every included skill.
- MARK-306 owns canonicalizing the approved set as `marketplace-project-pack`; MARK-305 must leave clean evidence, not finish canonicalization.
- There is no dedicated `.agents/skills` validator in this repo yet; use the best available source-grounded checks rather than pretending `git diff --check` proves projection correctness.

---

### Task 1: Audit the worker-relevant skill surface

**Files:**
- Inspect: `sources/first_party/skills/work-mode-router/SKILL.md`
- Inspect: `sources/first_party/skills/repo-worker-base/SKILL.md`
- Inspect: `sources/first_party/skills/linear-issue-shaping/SKILL.md`
- Inspect: `sources/first_party/skills/linear-superpowers/SKILL.md`
- Inspect: `sources/first_party/skills/boring-loop/SKILL.md`
- Inspect: `sources/first_party/skills/connector-safety/SKILL.md`
- Inspect: `sources/first_party/skills/github-operations/SKILL.md`
- Inspect: `sources/first_party/skills/unslop-plus/SKILL.md`
- Inspect: `sources/first_party/skills/safe-large-file-writing/SKILL.md`
- Inspect: `sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/using-superpowers/SKILL.md`
- Inspect: `sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/linear-superpowers/SKILL.md`
- Inspect: `sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/writing-plans/SKILL.md`
- Inspect: `sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/executing-plans/SKILL.md`
- Inspect: `sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/inspecting-the-environment/SKILL.md`
- Inspect: `sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/unslop-superpowers/SKILL.md`
- Inspect: `sources/first_party/skills/crew-buster/SKILL.md`
- Inspect: `sources/first_party/skills/crew/SKILL.md`
- Inspect: `sources/first_party/skills/base-doctrine/SKILL.md`
- Inspect: `sources/first_party/skills/bootstrap-router/SKILL.md`

**Interfaces:**
- Consumes: current repo AGENTS guidance, MARK-305 Linear issue, and the first-party plus third-party source custody above.
- Produces: a source-grounded classification table that separates install candidates from exclusions.

- [x] **Step 1: Read the repo worker surfaces**

Confirm the relevant source files and repo guidance before proposing anything:

```powershell
rg -n "worker-dispatch-linear|linear-issue-shaping|repo-worker-base|work-mode-router|boring-loop|connector-safety|github-operations|unslop-plus|safe-large-file-writing|using-superpowers|linear-superpowers|writing-plans|executing-plans|inspecting-the-environment|unslop-superpowers|crew-buster|bootstrap-router" sources\first_party\skills sources\third_party\superpowers\obra-superpowers\v6.0.3\skills AGENTS.md docs\AGENTS.md docs\custody-and-projection-doctrine.md
```

- [x] **Step 2: Complete the route-state audit**

Search terms used during preflight:

```text
preflight
execution
route state
worker route
plan PR
plan-only PR
approved plan
merged plan
staleness check
stale plan
current main
fresh main
chat memory
false green
worker dispatch
repo-resident plan
docs/superpowers/plans
```

Completed audit:

| Skill name | Source path | Relevant section or grep hit | Classification | Reason |
| --- | --- | --- | --- | --- |
| `work-mode-router` | `sources/first_party/skills/work-mode-router/SKILL.md` | `Core posture`, `First classification`, `Routing map`, `Golden-gate reminder`, `Bounded skill-read stop rule` | Update in MARK-305 | This is the canonical worker entrypoint for durable mode classification. It must classify route state from Linear/repo evidence and hand off the discovered mode to `/using-superpowers`, not pick the implementation lane itself. |
| `linear-issue-shaping` | `sources/first_party/skills/linear-issue-shaping/SKILL.md` | `description`, `Connector-safe Linear shaping BAU`, `Issue-type classification`, `Worker event-log handling`, `Route classification` | Update in MARK-305 | It is the renamed Linear shaping control-plane skill. MARK-303 folds into MARK-305 so the active references point at `linear-issue-shaping`, the connector-safe discover/read/mutate/discover/readback law is explicit, and the worker packet/readiness doctrine stays aligned with the route-state model. |
| `linear-superpowers` | `sources/first_party/skills/linear-superpowers/SKILL.md` | `Core job`, `Composition`, `Linear shaping rules`, `Authority split` | Update in MARK-305 | It already shapes Linear packets, but it must define and carry the compact Linear route-state block instead of directing workers into a Superpowers implementation lane from the plan-shaping surface. |
| `boring-loop` | `sources/first_party/skills/boring-loop/SKILL.md` | `Readiness`, `False-green prevention`, `Route to specialist skills`, `Variant boundary` | Update in MARK-305 | It already prevents false-green, but it must name the route-state false greens and the stale-plan repair split explicitly so route safety is visible in the worker loop. |
| `repo-worker-base` | `sources/first_party/skills/repo-worker-base/SKILL.md` | `Fresh-main invariant`, `Worktree isolation gate`, `Branch and PR discipline`, `GREEN gate` | Checked compatible / no update | It already requires fresh-main discipline, worktree isolation, PR evidence, and explicit blockers. The route-state split is upstream of this skill, so no change is required. |
| `github-operations` | `sources/first_party/skills/github-operations/SKILL.md` | `Default coding workflow boundary`, `Verification workflow`, `Publication proof`, `Issue-goal conformance` | Checked compatible / no update | It already keeps GitHub evidence separate from routing and does not own dispatch. It is compatible with the plan/approval/execution split as written. |
| `connector-safety` | `sources/first_party/skills/connector-safety/SKILL.md` | `Automatic trigger`, `Discovery-before-mutation rule`, `Blocked-write recovery ladder`, `Handoff and evidence` | Checked compatible / no update | It narrows side effects and handles blocked writes safely, but it does not set or interpret the preflight route states. |
| `unslop-plus` | `sources/first_party/skills/unslop-plus/SKILL.md` | `Available Profiles`, `Profile Selection Guide`, `Deliverable` | Checked compatible / no update | It provides anti-slop profiles for planning and worker returns, which supports the plan but does not govern route-state doctrine. |
| `safe-large-file-writing` | `sources/first_party/skills/safe-large-file-writing/SKILL.md` | `Core rule`, `Safe sequence`, `Decision test` | Checked compatible / no update | It reduces write risk for large docs and generated payloads. It is orthogonal to route-state selection and approval flow. |
| `tps-reporting` | `sources/first_party/skills/tps-reporting/SKILL.md` | `Linear/Codex boundary`, `Compact coding report shape`, `Report laundering hard stops` | Checked compatible / no update | It is a report-partitioning skill that keeps claims separate from evidence. It explicitly defers dispatch and proof to the control-plane skills, so it does not need a MARK-305 update. |
| `crew-buster` | `sources/first_party/skills/crew-buster/SKILL.md` | `description`, `route interrogation`, `do not use dispatch-shaped YAML` | Out of scope | It is a pre-action Crew lens for route/authority/fallback reasoning, but it is not the repo-local worker baseline and it does not own the durable router update. |
| `crew` | `sources/first_party/skills/crew/SKILL.md` | `description`, `doctrine source`, `not an execution surface` | Out of scope | It is a general Crew doctrine source, not a worker-installed repo skill for MARK-305. |
| `using-superpowers` | `sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/using-superpowers/SKILL.md` | `implementation skills second` and workflow entrypoint content | Out of scope | It is a core Superpowers+ environment capability, not a repo-local install candidate. |
| `writing-plans` | `sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/writing-plans/SKILL.md` | `Save plans to`, `After saving the plan, offer execution choice` | Out of scope | It is a core planning skill already available in the worker environment and not part of the repo-local baseline. |
| `executing-plans` | `sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/executing-plans/SKILL.md` | execution-workflow content | Out of scope | It is the core execution companion to `writing-plans`, so it is intentionally not vendored into `.agents/skills`. |
| `inspecting-the-environment` | `sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/inspecting-the-environment/SKILL.md` | environment/branch/worktree inspection content | Out of scope | It is a core environment-check capability already present in the worker environment, not a repo-local install target. |
| `unslop-superpowers` | `sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/unslop-superpowers/SKILL.md` | anti-slop doctrine content | Out of scope | Do not substitute it for `unslop-plus` without separate proof that it is the correct repo-local surface. |
| `bootstrap-router` | `sources/first_party/skills/bootstrap-router/SKILL.md` | bootstrap and routing doctrine content | Out of scope | It is broader bootstrap doctrine and does not own the repo-local durable route-state split. |

- [x] **Step 3: Freeze the source-update set**

Final MARK-305 source-update set:

| File | Decision | Why |
| --- | --- | --- |
| `sources/first_party/skills/work-mode-router/SKILL.md` | Update | It must classify preflight, pending approval, execution-ready, stale-plan repair, and blocked/ambiguous routes from durable evidence, then hand off to `/using-superpowers` with the discovered mode. |
| `sources/first_party/skills/linear-issue-shaping/SKILL.md` | Update | It must carry the worker-facing route-state/readiness doctrine and keep plan PRs distinct from implementation PRs. |
| `sources/first_party/skills/linear-superpowers/SKILL.md` | Update | It must carry the compact Linear route-state block as the control/index surface rather than a Superpowers lane chooser. |
| `sources/first_party/skills/boring-loop/SKILL.md` | Update | It must explicitly name the route-state false greens and the stale-plan repair split instead of only the general small-safe-move loop. |
| `sources/first_party/skills/repo-worker-base/SKILL.md` | No update | Current wording already enforces fresh-main, worktree, branch, PR, and validation discipline. |
| `sources/first_party/skills/github-operations/SKILL.md` | No update | Current wording already owns GitHub proof only after a GitHub artifact exists. |
| `sources/first_party/skills/connector-safety/SKILL.md` | No update | Current wording already keeps connector-side effects narrow and auditable. |
| `sources/first_party/skills/unslop-plus/SKILL.md` | No update | Current wording already supplies anti-slop profiles without controlling route state. |
| `sources/first_party/skills/safe-large-file-writing/SKILL.md` | No update | Current wording already covers safe write mechanics only. |
| `sources/first_party/skills/tps-reporting/SKILL.md` | No update | Current wording already partitions claims from evidence and defers dispatch to other skills. |

- [x] **Step 4: Keep the local set narrow**

Prefer skills that help workers:

```text
- choose the right route;
- stay on fresh main;
- write a bounded plan;
- handle Linear safely;
- prove GitHub publication;
- avoid false green;
- keep large writes safe.
```

### Task 2: Publish the revised recommendation

**Files:**
- Modify: `docs/superpowers/plans/2026-06-26-mark-305-worker-skill-stack-recommendation.md`
- Modify: `sources/first_party/skills/work-mode-router/SKILL.md`
- Modify: `sources/first_party/skills/linear-issue-shaping/SKILL.md`
- Modify: `sources/first_party/skills/linear-superpowers/SKILL.md`
- Modify: `sources/first_party/skills/boring-loop/SKILL.md`

**Interfaces:**
- Consumes: the audit from Task 1.
- Produces: a repo-local worker set recommendation plus a completed classification table, source-grounded install rules, and route-state doctrine that matches the durable preflight/execution split.

- [x] **Step 1: Include the repo-local baseline**

Recommended core set for `.agents/skills`:

| Skill | Canonical source path | Why workers need it locally |
| --- | --- | --- |
| `work-mode-router` | `sources/first_party/skills/work-mode-router/SKILL.md` | Session bootstrap and route classification before any repo action. |
| `repo-worker-base` | `sources/first_party/skills/repo-worker-base/SKILL.md` | Fresh-main, worktree, branch, and PR hygiene for repo work. |
| `linear-issue-shaping` | `sources/first_party/skills/linear-issue-shaping/SKILL.md` | Worker readiness, Linear state handling, and the connector-safe shaping split. |
| `boring-loop` | `sources/first_party/skills/boring-loop/SKILL.md` | Smallest safe move selection and false-green prevention. |
| `connector-safety` | `sources/first_party/skills/connector-safety/SKILL.md` | Safe Linear/GitHub writes and blocked-write recovery. |
| `github-operations` | `sources/first_party/skills/github-operations/SKILL.md` | PR, branch, merge, and publication proof. |
| `unslop-plus` | `sources/first_party/skills/unslop-plus/SKILL.md` | Portable anti-slop profiles for planning, review, and worker-return discipline. |
| `safe-large-file-writing` | `sources/first_party/skills/safe-large-file-writing/SKILL.md` | Safer writes for large markdown or generated payloads. |

- [x] **Step 2: Exclude core Superpowers+ and worker-environment skills**

| Skill | Why it should not be installed locally |
| --- | --- |
| `using-superpowers` | Core Superpowers+ workflow entrypoint; workers already have it in their environment. |
| `inspecting-the-environment` | Core environment-inspection capability; do not vendor it into repo-local worker baseline. |
| `linear-superpowers` | Core Superpowers+ Linear shaping skill; not a repo-local install candidate. |
| `writing-plans` | Core Superpowers+ planning skill already available to workers. |
| `executing-plans` | Core Superpowers+ execution skill already available to workers. |
| `unslop-superpowers` | Do not substitute this for `unslop-plus` unless separately proven to be the right repo-local surface. |

- [x] **Step 3: Exclude tempting but non-baseline skills**

| Skill | Reason |
| --- | --- |
| `crew-buster` | Useful route interrogation, but broader than the narrow repo worker baseline. |
| `crew` | Doctrine source, not an installable worker baseline skill for this repo. |
| `base-doctrine` | Cross-project doctrine store, not a repo-local worker baseline skill. |
| `bootstrap-router` | Global bootstrap router, but too broad for the narrow `.agents/skills` worker set. |

- [x] **Step 4: Update the route-state doctrine**

Revise `work-mode-router` to classify from durable markers only, not chat memory. It should inspect or require evidence for:

```text
- route-state block in the Linear preflight/implementation brief;
- plan PR URL and current PR state;
- plan repo path under docs/superpowers/plans/;
- plan approval and merge evidence;
- approved plan commit;
- last staleness-check evidence.
```

It should route to the same route states used by `linear-issue-shaping`:

```text
preflight_needed
preflight_complete_pending_approval
approved_plan_execution_ready
stale_plan_repair_needed
blocked_ambiguous
```

It must preserve the rule that a merged plan is an approved starting point, not current source truth. Execution still requires a staleness check against current source before edits.

The audit above shows that `linear-issue-shaping`, `linear-superpowers`, and `boring-loop` do not yet fully carry the route-state block, false-green naming, and stale-plan split the user asked us to prove, so they belong in the MARK-305 execution update set with `work-mode-router`. MARK-303 folds into the same execution pass through `linear-issue-shaping`, so execution should update that source file together with the route-state doctrine rather than treating the rename as a separate surface.

- [x] **Step 5: End-to-end route scenario**

| Start state from short prompt | Durable markers the worker reads | Owning skill | Worker action |
| --- | --- | --- | --- |
| `preflight_needed` | No approved repo-resident plan exists, route-state block says preflight or is absent, and there is no approved plan commit or fresh staleness evidence. | `work-mode-router` | Classify preflight, route to `/using-superpowers` with preflight context, produce the plan-only PR, update Linear route state, and stop before implementation. |
| `preflight_complete_pending_approval` | Plan file exists under `docs/superpowers/plans/`, plan PR exists, route-state block says pending approval, but approval/merge evidence is absent. | `work-mode-router` | Classify pending approval and stop/report pending approval. No implementation lane should be selected. |
| `approved_plan_execution_ready` | Approved plan is merged to `main`, plan path/commit/PR evidence exists, and the staleness check passes against current source. | `work-mode-router` | Classify execution-ready, route to `/using-superpowers` with execution context, and execute from the approved plan. |
| `stale_plan_repair_needed` | Approved merged plan exists, but current source drift makes the plan stale. | `work-mode-router` | Classify stale-plan repair, route to `/using-superpowers` with repair-then-execute context, repair the plan in the execution branch if the drift stays within scope, and publish the repaired plan with the implementation. |
| `blocked_ambiguous` | Durable markers disagree, plan path is missing, approval evidence is unclear, PR state cannot be proven, or the route state cannot be classified safely. | `work-mode-router` | Classify blocked/ambiguous, stop, and report the exact missing or contradictory durable evidence. |

- [x] **Step 6: State the install/projection rule**

The repo-local `.agents/skills` surface should be built by copying the approved skill directories from durable source custody into `.agents/skills/<skill>/` with the same directory names and the same skill file layout, not by hand-editing or dumping arbitrary folders.

The plan should leave a source-grounded manifest or source map in the repo-local surface that records the exact canonical source path for each installed skill, so later workers can verify where each local folder came from. The Adventures Pack bundle manifest is now regenerated by the canonical update stack via `tools/generate_adventures_pack_manifest.py`, which `tools/update_skill_artifacts.py` calls before projection so the pack is not a manual one-off.

### Task 3: Define the execution phase after approval

**Files:**
- Modify: `docs/superpowers/plans/2026-06-26-mark-305-worker-skill-stack-recommendation.md`
- Create: `.agents/INDEX.md`
- Create: `.agents/skills/INDEX.md`
- Create: `.agents/skills/AGENTS.md`

**Interfaces:**
- Consumes: the approved recommendation from Task 2.
- Produces: an execution phase that installs the approved set into `.agents/skills` without treating that tree as canonical source.

- [x] **Step 1: Keep preflight and execution separate**

```text
1. PREFLIGHT: inspect source, revise the recommended set, publish the plan/recommendation, and stop for approval.
2. EXECUTION after approval: install/project the approved set into this repo's `.agents/skills` folder using source-grounded repo conventions.
3. FOLLOW-UP: MARK-306 canonicalizes the final approved set as the marketplace plugin `marketplace-project-pack`.
```

- [x] **Step 2: Keep MARK-305 from broadening into canonicalization**

MARK-305 should leave the exact approved skill list, source paths, and local projection shape ready for MARK-306. It should not design the final marketplace plugin beyond clean source evidence and a stable approved set.

- [x] **Step 3: Name the drift-avoidance rule**

The install phase must not become a raw folder dump. Every installed local folder should be traceable back to one approved source path, and any mismatch between local content and source custody should be treated as drift, not as accepted variation.

- [x] **Step 4: Leave worker-facing guidance in the repo**

`.agents/INDEX.md` should point workers to the local skill surface. `.agents/skills/INDEX.md` should enumerate the approved skill folders and point to the `SKILL.md` inside each folder. `.agents/skills/AGENTS.md` should explain how to use the installed skills, how to keep them aligned when the matching vendored market skills change, and how the local skill surface composes with the repository root [AGENTS.md](../../AGENTS.md).

### Task 4: Add validation for the local projection surface

**Files:**
- Modify: `docs/superpowers/plans/2026-06-26-mark-305-worker-skill-stack-recommendation.md`

**Interfaces:**
- Consumes: the approved set and the local projection rule from Tasks 2 and 3.
- Produces: explicit checks that verify `.agents/skills` exists, is source-grounded, and matches the approved set.

- [x] **Step 1: State the validation gap plainly**

There is no dedicated `.agents/skills` validator in this repo today.

- [x] **Step 2: Use the best available checks**

Planned checks after local install:

```powershell
Test-Path .agents\skills
Get-ChildItem .agents\skills -Directory | Sort-Object Name | Select-Object -ExpandProperty Name
rg -n "canonical_source_path|source_path|local_path" .agents\skills
git diff --check
```

If the projection includes a repo-local manifest or source map file, compare its declared source paths against the approved source list in this plan before calling the surface good.

- [x] **Step 3: Keep marketplace validation separate**

`py -3 tools/validate_marketplace.py` remains useful for marketplace surfaces, but it does not prove `.agents/skills` source grounding by itself. Use it only as a supporting check if the broader repo surface changes.

### Task 5: Keep MARK-306 clean

**Files:**
- Modify: `docs/superpowers/plans/2026-06-26-mark-305-worker-skill-stack-recommendation.md`

**Interfaces:**
- Consumes: the audit table from Task 1 and the route-state doctrine from Task 2.
- Produces: an approval-ready plan that leaves MARK-306 with clean source evidence and no canonicalization spillover.

- [x] **Step 1: Record the audit outcome explicitly**

The audit found four required source updates: `work-mode-router`, `linear-issue-shaping`, `linear-superpowers`, and `boring-loop`. MARK-303 folds into the same execution pass through `linear-issue-shaping`; all other named candidates and adjacent routing/proof skills listed above are checked compatible or out of scope, so execution should not rediscover scope.

- [x] **Step 2: Keep MARK-306 scoped correctly**

MARK-306 consumes the final approved MARK-305 set and the source evidence collected here. MARK-305 should not design the canonical marketplace plugin beyond the evidence needed to support MARK-306.

- [x] **Step 3: Add the plan-artifact invariant**

Every execution PR must include the updated repo-resident plan file with checkboxes checked to reflect completed work. If the plan was stale, the execution PR must include the repaired plan plus the implementation. If the plan was fresh, the execution PR must still include the updated checked-off plan.

### Task 6: Record the execution pass

**Files:**
- Modified: `sources/first_party/skills/work-mode-router/SKILL.md`
- Modified: `sources/first_party/skills/linear-issue-shaping/SKILL.md`
- Modified: `sources/first_party/skills/linear-superpowers/SKILL.md`
- Modified: `sources/first_party/skills/boring-loop/SKILL.md`
- Created: `.agents/INDEX.md`
- Created: `.agents/skills/INDEX.md`
- Created: `.agents/skills/AGENTS.md`
- Projected: `.agents/skills/<approved-skill>/...` from the approved source custody

**Interfaces:**
- Consumes: the approved MARK-305 execution set and the repo-local projection rules.
- Produces: the repo-local worker surface and the source updates that make the route boundary durable.

- [x] **Step 1: Project the approved skill set**

The approved worker skills were copied into `.agents/skills` from the canonical source custody and indexed with source paths.

- [x] **Step 2: Update the source custody**

`work-mode-router`, `linear-issue-shaping`, `linear-superpowers`, and `boring-loop` were updated to reflect the durable route-state boundary, the connector-safe Linear shaping rename from MARK-303, and the `/using-superpowers` handoff model.

- [x] **Step 3: Create the worker-facing repo guidance**

`.agents/INDEX.md`, `.agents/skills/INDEX.md`, and `.agents/skills/AGENTS.md` were added so workers can discover and maintain the local skill surface.

## Review Check

- [x] The recommended local set matches the user-corrected baseline.
- [x] The excluded set separates core Superpowers+ skills from narrow repo worker skills.
- [x] The plan now says `.agents/skills` is an immediate projection surface, not canonical source.
- [x] The plan now includes repo-facing `.agents` guidance files for discoverability and composition.
- [x] The plan now requires a route-state audit across first-party source custody and projected mirrors before finalizing the recommendation.
- [x] The plan now treats `work-mode-router` as a source-update target, not just a local install candidate.
- [x] The plan now routes MARK-306 as the canonicalization follow-up.
- [x] The plan names the best available checks because no dedicated `.agents/skills` validator exists yet.
