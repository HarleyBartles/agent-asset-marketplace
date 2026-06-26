# MARK-305 Worker Skill Stack Recommendation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preflight a narrow repo-local `.agents/skills` worker set for `agent-asset-marketplace`, publish the approved recommendation in MARK-305, and then install/project that approved set into this repository's `.agents/skills` surface after approval so workers benefit immediately. The repo must also carry worker-facing guidance at `.agents/INDEX.md`, `.agents/skills/INDEX.md`, and `.agents/skills/AGENTS.md` so the local worker set is discoverable and maintainable. MARK-306 will canonicalize the same approved set as the `marketplace-project-pack` plugin after MARK-305 lands.

**Architecture:** Treat `sources/first_party/skills/` as canonical source custody and `.agents/skills/` as an immediate repo-local install/projection surface. The installed tree should be sourced from durable repo skill custody, not copied as a raw dump, and each installed entry should remain traceable back to an exact canonical source path. Keep the recommended set narrow: only worker control-plane, safety, publication, and anti-slop skills that materially help repo workers in this repository.

**Tech Stack:** Markdown, Linear, Git, PowerShell, first-party skill source custody, and repo-local projection/validation checks.

## Global Constraints

- `.agents/skills` is an immediate repo-local projection surface, not canonical source.
- Worker-facing guidance must live in the repo at `.agents/INDEX.md`, `.agents/skills/INDEX.md`, and `.agents/skills/AGENTS.md`.
- Do not vendor core Superpowers+ skills into the repo-local worker set.
- Keep the recommended set narrow and worker-facing.
- Use exact source paths for every included skill.
- MARK-306 owns canonicalizing the approved set as `marketplace-project-pack`; MARK-305 must leave clean evidence, not finish canonicalization.
- There is no dedicated `.agents/skills` validator in this repo yet; use the best available source-grounded checks rather than pretending `git diff --check` proves projection correctness.

---

### Task 1: Audit the worker-relevant skill surface

**Files:**
- Inspect: `sources/first_party/skills/work-mode-router/SKILL.md`
- Inspect: `sources/first_party/skills/repo-worker-base/SKILL.md`
- Inspect: `sources/first_party/skills/worker-dispatch-linear/SKILL.md`
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
rg -n "worker-dispatch-linear|repo-worker-base|work-mode-router|boring-loop|connector-safety|github-operations|unslop-plus|safe-large-file-writing|using-superpowers|linear-superpowers|writing-plans|executing-plans|inspecting-the-environment|unslop-superpowers|crew-buster|bootstrap-router" sources\first_party\skills sources\third_party\superpowers\obra-superpowers\v6.0.3\skills AGENTS.md docs\AGENTS.md docs\custody-and-projection-doctrine.md
```

- [x] **Step 2: Classify each skill by worker value**

Use three buckets:

```text
included in .agents/skills
excluded because supplied by core Superpowers+
excluded as tempting but not appropriate for the narrow repo worker baseline
```

- [x] **Step 3: Keep the local set narrow**

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

**Interfaces:**
- Consumes: the audit from Task 1.
- Produces: a repo-local worker set recommendation plus a classification table and source-grounded install rules.

- [x] **Step 1: Include the repo-local baseline**

Recommended core set for `.agents/skills`:

| Skill | Canonical source path | Why workers need it locally |
| --- | --- | --- |
| `work-mode-router` | `sources/first_party/skills/work-mode-router/SKILL.md` | Session bootstrap and route classification before any repo action. |
| `repo-worker-base` | `sources/first_party/skills/repo-worker-base/SKILL.md` | Fresh-main, worktree, branch, and PR hygiene for repo work. |
| `worker-dispatch-linear` | `sources/first_party/skills/worker-dispatch-linear/SKILL.md` | Worker readiness, Linear state handling, and preflight/execution split. |
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

- [x] **Step 4: State the install/projection rule**

The repo-local `.agents/skills` surface should be built by copying the approved skill directories from durable source custody into `.agents/skills/<skill>/` with the same directory names and the same skill file layout, not by hand-editing or dumping arbitrary folders.

The plan should leave a source-grounded manifest or source map in the repo-local surface that records the exact canonical source path for each installed skill, so later workers can verify where each local folder came from.

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

## Review Check

- [x] The recommended local set matches the user-corrected baseline.
- [x] The excluded set separates core Superpowers+ skills from narrow repo worker skills.
- [x] The plan now says `.agents/skills` is an immediate projection surface, not canonical source.
- [x] The plan now includes repo-facing `.agents` guidance files for discoverability and composition.
- [x] The plan now routes MARK-306 as the canonicalization follow-up.
- [x] The plan names the best available checks because no dedicated `.agents/skills` validator exists yet.
