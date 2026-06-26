# MARK-305 Worker Skill Stack Recommendation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Recommend a narrow, repo-local `.agents/skills` set that materially improves worker flow in `agent-asset-marketplace`, then carry that recommendation through MARK-305 as a planning artifact rather than a code change.

**Architecture:** Treat `sources/first_party/skills/` as the source of truth and the repo-local `.agents/skills` folder as a projected worker convenience layer, not canonical source. Keep the recommended set biased toward worker control-plane, environment safety, planning, and publication proof, since this repository spends a lot of time shaping Linear issues, planning work, and publishing Git evidence.

**Tech Stack:** Markdown, Linear, Git, repo-local first-party skills, and the existing `docs/superpowers/plans/` convention.

## Global Constraints

- Repo-local `.agents/skills` is a convenience projection, not canonical source.
- Keep the worker set narrow and reusable.
- Prefer first-party repo skills over external or generic system skills when the repo already has a first-party equivalent.
- Do not turn the recommendation into a full skill catalog.
- Do not broaden beyond worker-facing repo use.

---

### Task 1: Audit the worker-relevant skill surface

**Files:**
- Inspect: `sources/first_party/skills/work-mode-router/SKILL.md`
- Inspect: `sources/first_party/skills/repo-worker-base/SKILL.md`
- Inspect: `sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/using-superpowers/SKILL.md`
- Inspect: `sources/first_party/skills/linear-superpowers/SKILL.md`
- Inspect: `sources/first_party/skills/worker-dispatch-linear/SKILL.md`
- Inspect: `sources/first_party/skills/boring-loop/SKILL.md`
- Inspect: `sources/first_party/skills/inspecting-the-environment/SKILL.md`
- Inspect: `sources/first_party/skills/connector-safety/SKILL.md`
- Inspect: `sources/first_party/skills/github-operations/SKILL.md`
- Inspect: `sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/writing-plans/SKILL.md`
- Inspect: `sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/executing-plans/SKILL.md`
- Inspect: `sources/first_party/skills/unslop-superpowers/SKILL.md`
- Inspect: `sources/first_party/skills/safe-large-file-writing/SKILL.md`

**Interfaces:**
- Consumes: current repo AGENTS guidance, current MARK-305 Linear issue, current first-party skill source tree.
- Produces: a ranked list of skills that are genuinely valuable for workers in this repo.

- [x] **Step 1: Read the repo worker surfaces**

Confirm the relevant source files and repo guidance before proposing anything:

```powershell
rg -n "worker-dispatch-linear|linear-superpowers|repo-worker-base|work-mode-router|using-superpowers|writing-plans|executing-plans|inspecting-the-environment|connector-safety|github-operations|boring-loop|unslop-superpowers" sources\first_party\skills AGENTS.md docs\AGENTS.md docs\custody-and-projection-doctrine.md
```

- [x] **Step 2: Classify each skill by worker value**

Use three buckets:

```text
core = should be in the worker set by default
optional = useful but not essential in every repo-local worker session
exclude = not worth putting in the local worker set
```

- [x] **Step 3: Keep the local set narrow**

Prefer skills that help workers:

```text
- choose the right route;
- stay on fresh main;
- write a bounded plan;
- handle Linear safely;
- prove GitHub publication;
- avoid false green.
```

### Task 2: Recommend the `.agents/skills` set

**Files:**
- Modify: `docs/superpowers/plans/2026-06-26-mark-305-worker-skill-stack-recommendation.md`

**Interfaces:**
- Consumes: the audit from Task 1.
- Produces: a repo-local worker skill set recommendation suitable for a future `.agents/skills` projection.

- [x] **Step 1: Recommend the core worker set**

Recommended core set:

```text
work-mode-router
repo-worker-base
using-superpowers
inspecting-the-environment
linear-superpowers
worker-dispatch-linear
boring-loop
connector-safety
github-operations
writing-plans
executing-plans
unslop-superpowers
safe-large-file-writing
```

- [x] **Step 2: Explain why each core skill earns its slot**

Short version:

```text
- work-mode-router: session bootstrap and route classification.
- repo-worker-base: fresh-main, worktree, branch, and PR hygiene.
- using-superpowers: mandatory workflow entrypoint and skill discovery.
- inspecting-the-environment: shell/worktree/auth/path/mutation constraints.
- linear-superpowers: compact Linear issue shaping.
- worker-dispatch-linear: worker readiness, preflight/execution split, and Linear worker state.
- boring-loop: smallest safe move and false-green prevention.
- connector-safety: safe writes and blocked-write recovery.
- github-operations: PR, branch, merge, and publication proof.
- writing-plans: bounded implementation-plan structure before edits.
- executing-plans: task-by-task implementation once approved.
- unslop-superpowers: repo-specific anti-slop and evidence discipline.
- safe-large-file-writing: safer writes for large markdown or generated artifacts.
```

- [x] **Step 3: Keep optional skills out of the baseline**

Do not put these in the baseline unless the local worker stack is intentionally expanded:

```text
- crew-buster
- crew
- base-doctrine
- bootstrap-router
```

Reason:

```text
They are useful, but they add route/interrogation doctrine that is broader than the minimal repo worker set.
```

### Task 3: Note the scope widening in Linear and keep the plan aligned

**Files:**
- Update: `MARK-305` Linear comment thread

**Interfaces:**
- Consumes: the recommendation from Task 2.
- Produces: an issue record that matches the widened planning surface.

- [x] **Step 1: Record the widened scope in Linear**

Leave a short comment on MARK-305 noting that the plan now includes a recommendation for a repo-local `.agents/skills` set for workers in this repository.

- [x] **Step 2: Keep the recommendation narrow**

State explicitly that the recommendation is for worker-facing repo use, not a full skill catalog.

## Review Check

- [x] The plan names exact files and exact skills.
- [x] The recommendation is narrow enough to be useful.
- [x] The plan preserves the repo rule that `.agents/skills` is a projection, not canonical source.
- [x] The scope-widening comment exists in Linear.
