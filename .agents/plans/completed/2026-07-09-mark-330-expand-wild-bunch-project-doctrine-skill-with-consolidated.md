# MARK-330: Expand wild-bunch-project-doctrine skill with consolidated rule sets

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the `wild-bunch-project-doctrine` first-party skill so it consolidates the rule sets and guidance currently scattered across the wild-bunch repo's root `AGENTS.md`. The skill becomes the central discovery surface for Wild Bunch working knowledge, skill routing, script discovery, and policy references — while the repo `AGENTS.md` shrinks to a thin pointer that defers to the skill.

**Source issue:** [MARK-330](https://linear.app/harleys-workspace/issue/MARK-330)

## Source evidence pin

**Source repo:** `HarleyBartles/wild-bunch`
**Pinned commit:** `a65ca6c2` — "Implementation: Town hub deterministic layout resolver and salt controls (#159)" on `main`
**Source file:** `AGENTS.md` (94 lines at that commit)

**Sections being consolidated:**
- `## Required Working Knowledge` (lines 11-31) — worktree/scratch locations, script discovery, required reading before specific work types
- `## Required Skills - Workflow Routing` (lines 33-79) — session bootstrap, Linear/GitHub, anti-slop/quality, planning/execution, repo-specific, architecture skills
- `## Script Discovery` (lines 81-92) — script routing for PostgreSQL, dev servers, index mesh, skill sync, image assets
- `## Specialist Skill Discovery` (lines 94-100) — inspect source first, use skill discovery, skills catalog reference
- `## Policy Reference` (lines 102-115) — workflow, validation, artifact, architecture guardrails, coding discipline, worker environment, repo-skills, mesh policy, guides
- `## ADR Log Freshness` (lines 117-118) — ADR freshness requirement

**Pre-implementation check (Step 0):** Before writing any reference doc content, verify that every referenced script, guide, policy, ADR, and skill exists at commit `a65ca6c2`. The following 21 docs and 8 scripts have been verified to exist at that commit:

Docs: `scripts/AGENTS.md`, `.agents/docs/architecture-hygiene.md`, `.agents/unslop/backend-architecture.md`, `.agents/docs/architecture-guardrails.md`, `docs/adr/ADR-0036-dev-enabled-action-pattern.md`, `.agents/docs/coding-discipline.md`, `.agents/docs/frontend-standards.md`, `.agents/docs/validation-policy.md`, `.agents/docs/guides/design-guide.md`, `.agents/docs/guides/implementing-guide.md`, `.agents/docs/guides/planning-guide.md`, `.agents/docs/guides/code-review-guide.md`, `src/WildBunch.Web/AGENTS.md`, `src/WildBunch.Web/.agents/unslop/play-surface-ui.md`, `.agents/docs/dev-overlay-doctrine.md`, `.agents/unslop/dev-overlay.md`, `.agents/docs/workflow-policy.md`, `.agents/docs/artifact-policy.md`, `.agents/docs/worker-environment.md`, `.agents/docs/repo-skills-policy.md`, `.agents/doctrine/mesh-policy.md`, `.agents/docs/skills-catalog.md`

Scripts: `scripts/postgres-dev.ps1`, `scripts/dev-servers.ps1`, `scripts/generate_index_mesh.py`, `scripts/generate_index_mesh.ps1`, `scripts/install_agent_skills.py`, `scripts/install_agent_skills.ps1`, `scripts/image_asset_pipeline.py`, `scripts/image_asset_pipeline.ps1`

Skills: all 22 skills referenced in the skill-routing doc exist under `.agents/skills/` at that commit.

**Deviation from source:** Three intentional deviations from the source AGENTS.md content:
1. The `/using-superpowers` trigger is narrowed from "starting any conversation" to "workflow-sensitive project/repo work" to preserve the ordinary-chat escape hatch.
2. The statement "The skills and ADRs are the authority, not the repo's current code" is removed. Current live source is truth about current behaviour; skills and ADRs provide constraints and intended architecture, and their freshness must be checked against source and current requirements.
3. The claim that "The aggregate root enforces invariants and returns Result objects for failures" is removed unless verified against Wild Bunch source. The DDD skill description is shortened to remove this unsupported detail.

## Scope boundaries

- **In scope:** Edit `sources/first_party/skills/wild-bunch-project-doctrine/` (SKILL.md, agents/openai.yaml, references/). Create 3 new reference docs. Update `references/repo-posture.md`. Regenerate marketplace projections. Run full rebuild + validation.
- **Out of scope:** Editing the wild-bunch repo's `AGENTS.md` directly (that is a separate repo — `HarleyBartles/wild-bunch`). The skill source lives in this marketplace repo and is projected to the wild-bunch repo via the marketplace plugin.
- **Not in scope:** Changing other wild-bunch skills (`wild-bunch-dotnet-architecture`, `wild-bunch-domain-modeling`, `wild-bunch-browser-game`).

## Plan

- [x] Step 0: Pre-implementation source evidence check
- [x] Step 1: Replace SKILL.md frontmatter and body
- [x] Step 2: Create `references/working-knowledge.md`
- [x] Step 3: Create `references/skill-routing.md`
- [x] Step 4: Create `references/policy-references.md`
- [x] Step 5: Update `references/repo-posture.md`
- [x] Step 6: Update `agents/openai.yaml`
- [x] Step 7: Regenerate marketplace projections and run full rebuild + validation

---

## Step 0: Pre-implementation source evidence check

Before writing any reference doc content, verify that every path referenced in the plan exists at the pinned wild-bunch commit `a65ca6c2`. Run:

```bash
cd Z:\wild-bunch
git ls-tree --name-only a65ca6c2 -- <path>
```

for each path listed in the "Source evidence pin" section above. If any path is missing, stop and update the plan before proceeding. All 21 docs, 8 scripts, and 22 skills have been pre-verified as of plan creation, but the implementing agent must re-verify in case the wild-bunch repo has been rebased or force-pushed.

- [x] Step 0 complete

---

## Step 1: Replace SKILL.md frontmatter and body

Replace the entire contents of `sources/first_party/skills/wild-bunch-project-doctrine/SKILL.md` with the following. This expands the frontmatter with rich `use_when` triggers, adds `do_not_use_when` entries that preserve the doctrine skill's bootstrap role (it establishes posture then routes to specialists — it is not excluded when a specialist subsequently owns the task), adds two new rules, and replaces the References section with routing for all 5 reference docs.

**File:** `sources/first_party/skills/wild-bunch-project-doctrine/SKILL.md`

**Exact replacement content:**

```markdown
---
name: wild-bunch-project-doctrine
description: Use when bootstrapping the Wild Bunch repo posture before any repo-sensitive
  change. Establishes source-truth posture, worker dispatch and return verification,
  issue-goal conformance, world setup, seeded identity, difficulty, entropy, working
  knowledge (worktree and scratch locations, script discovery), skill routing (session
  bootstrap, Linear/GitHub, anti-slop, planning/execution, repo-specific, architecture),
  and policy references (workflow, validation, artifact, architecture guardrails,
  coding discipline, worker environment, mesh, guides, ADR freshness). Use when chat
  summaries, session busters, worker reports, or issue comments might be mistaken
  for live repo truth. This skill establishes posture first, then routes to specialist
  skills (wild-bunch-dotnet-architecture, wild-bunch-domain-modeling, wild-bunch-browser-game)
  for domain-specific work.
metadata:
  source-id: wild-bunch-project-doctrine
  source-path: sources/first_party/skills/wild-bunch-project-doctrine/SKILL.md
  provenance-name: Wild Bunch Project Doctrine first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when bootstrapping the Wild Bunch repo posture before any repo-sensitive
    change. Establishes source-truth posture, worker dispatch and return verification,
    issue-goal conformance, world setup, seeded identity, difficulty, entropy, working
    knowledge (worktree and scratch locations, script discovery), skill routing (session
    bootstrap, Linear/GitHub, anti-slop, planning/execution, repo-specific, architecture),
    and policy references (workflow, validation, artifact, architecture guardrails,
    coding discipline, worker environment, mesh, guides, ADR freshness). Use when chat
    summaries, session busters, worker reports, or issue comments might be mistaken
    for live repo truth. This skill establishes posture first, then routes to specialist
    skills (wild-bunch-dotnet-architecture, wild-bunch-domain-modeling, wild-bunch-browser-game)
    for domain-specific work.
  use_when:
  - Use when bootstrapping the Wild Bunch repo posture before any repo-sensitive change.
  - Use when work touches HarleyBartles/wild-bunch, worker dispatch, worker return
    verification, source-truth claims, or issue-goal conformance.
  - Use when work touches world setup, seeded identity, difficulty, entropy, or starting
    inventory.
  - Use when an agent needs Wild Bunch working knowledge — worktree/scratch locations,
    script discovery, or environmental issue resolution.
  - Use when an agent needs skill routing for the Wild Bunch repo — session bootstrap,
    Linear/GitHub work, anti-slop/quality, planning/execution, repo-specific, or
    architecture skills.
  - Use when an agent needs policy reference routing — workflow policy, validation
    policy, artifact policy, architecture guardrails, coding discipline, worker
    environment, repo-skills policy, mesh policy, or guides.
  - Use when chat summaries, session busters, worker reports, or issue comments might
    be mistaken for live repo truth.
  do_not_use_when:
  - Do not use for ordinary chat or questions that do not touch repo-sensitive work.
  - Do not use as a substitute for the specialist skill that owns the actual task
    (wild-bunch-dotnet-architecture, wild-bunch-domain-modeling, wild-bunch-browser-game,
    ddd, cqrs-event-sourcing, ef-core, clean-architecture, etc.). Establish posture
    with this skill, then invoke the specialist for the domain-specific work.
license: MIT
---

# Wild Bunch Project Doctrine

Use this skill first when working on `HarleyBartles/wild-bunch`, or when a task needs the Wild Bunch setup doctrine. The live repo state on current `main` is the source of truth. Chat summaries, issue comments, session busters, and worker reports are support material only.

This skill establishes posture and then routes to specialist skills for domain-specific work. It does not replace `wild-bunch-dotnet-architecture`, `wild-bunch-domain-modeling`, `wild-bunch-browser-game`, or other specialist skills — it precedes them.

## Rules

- Treat `HarleyBartles/wild-bunch` as a mainline-only C#/.NET game project.
- Inspect live source before claiming current state.
- GPT prepares worker packets; Harley sends them; workers execute.
- When a task touches world setup, seed identity, difficulty, entropy, random selection, or starting inventory, read `references/difficulty-entropy-seeded-world-setup.md` first and keep it as the canonical anchor.
- Returns must include branch, commit, PR, validation, and issue-goal conformance notes.
- Scripts in `scripts/` are first-class surfaces. Before reporting environmental issues or running ad-hoc commands, read `references/policy-references.md` for the script discovery map.
- For specialist work (architecture, domain modeling, browser delivery, etc.), inspect current source and canonical repo decisions first, then invoke the smallest relevant specialist skill. See `references/skill-routing.md` for the full routing map.

## References

Read [Live repo posture](references/repo-posture.md) when a task needs source-truth posture, worker route boundaries, return/verification expectations, or script discovery guidance.

Read [Working Knowledge](references/working-knowledge.md) when a task needs Wild Bunch worktree/scratch locations, environmental issue resolution, or the required working knowledge checklist (architecture guardrails, coding discipline, frontend standards, validation policy, guides, dev overlay, web UI surfaces).

Read [Skill Routing](references/skill-routing.md) when a task needs the Wild Bunch skill routing map: session bootstrap, Linear/GitHub work, anti-slop/quality, planning/execution, repo-specific skills, or architecture skills.

Read [Policy References](references/policy-references.md) when a task needs the Wild Bunch policy reference map: workflow policy, validation policy, artifact policy, architecture guardrails, coding discipline, worker environment, repo-skills policy, mesh policy, guides, or ADR log freshness.

Read [Difficulty, Entropy, and Seeded Setup Doctrine](references/difficulty-entropy-seeded-world-setup.md) when a task needs world-start setup, seeded world identity, entropy, or difficulty posture.
```

- [x] Step 1 complete

---

## Step 2: Create `references/working-knowledge.md`

Create a new reference doc consolidating the "Required Working Knowledge" section from the wild-bunch AGENTS.md. All paths are relative to the wild-bunch repo root.

**File:** `sources/first_party/skills/wild-bunch-project-doctrine/references/working-knowledge.md`

**Exact content to write:**

```markdown
# Working Knowledge

Consolidated from the Wild Bunch repo root `AGENTS.md` at commit `a65ca6c2`. All paths are relative to the wild-bunch repo root.

## Worktree and Scratch locations

- Worktrees for this repo should be placed in `Z:\_agent-worktrees\wild-bunch` (centralized location outside the repo). This is a declared preference that should be respected by the using-git-worktrees skill.
- **CRITICAL: Scratch files must be placed in `Z:\_agent-scratch\wild-bunch\<branch-name>`** where `<branch-name>` matches the worktree/branch name. This scratch space is disposable and not persistent beyond the agent's session. Agents must clean up their scratch folder when cleaning up their worktree. **Never commit scratch artifacts to the repo root** — see `.agents/docs/artifact-policy.md` for details.

## Scripts are first-class surfaces

Before reporting environmental issues (PostgreSQL not running, dev servers not started, etc.), read `scripts/AGENTS.md` and use the provided scripts.

- **Deterministic workflow scripts (dev servers, PostgreSQL, skill sync, index mesh)**: `scripts/AGENTS.md` — **MUST read before running ad-hoc commands or reporting environmental issues**. Scripts handle PostgreSQL setup, dev server management, and other repo operations idempotently.

## Required reading before specific work types

- Architecture-sensitive work: `.agents/INDEX.md`, `.agents/docs/architecture-hygiene.md`, `.agents/unslop/backend-architecture.md`
- **Architecture guardrails (must read before touching GameSession, persistence, or domain logic)**: `.agents/docs/architecture-guardrails.md`
- **Dev-enabled action pattern (must read before implementing dev controls that affect play actions)**: `docs/adr/ADR-0036-dev-enabled-action-pattern.md`
- **Coding discipline (must read before writing code)**: `.agents/docs/coding-discipline.md`
- **Frontend standards (must read before implementing or reviewing frontend work)**: `.agents/docs/frontend-standards.md`
- **Validation policy (must read before writing or reviewing tests)**: `.agents/docs/validation-policy.md`
- **Design guide (must read before brainstorming or writing a design spec)**: `.agents/docs/guides/design-guide.md`
- **Implementing guide (must read before implementing or dispatching implementer subagents)**: `.agents/docs/guides/implementing-guide.md`
- **Planning guide (must read before planning multi-step work)**: `.agents/docs/guides/planning-guide.md`
- **Code review guide (must read for code reviewers)**: `.agents/docs/guides/code-review-guide.md`
- Web UI/play-surface work: `src/WildBunch.Web/AGENTS.md`, `src/WildBunch.Web/.agents/unslop/play-surface-ui.md`
- Dev overlay work: `.agents/docs/dev-overlay-doctrine.md`, `.agents/unslop/dev-overlay.md`
```

- [x] Step 2 complete

---

## Step 3: Create `references/skill-routing.md`

Create a new reference doc consolidating the "Required Skills - Workflow Routing" section from the wild-bunch AGENTS.md. Three intentional deviations from the source (documented in the "Source evidence pin" section above):
1. `/using-superpowers` trigger narrowed from "starting any conversation" to "workflow-sensitive project/repo work" to preserve the ordinary-chat escape hatch.
2. The statement "The skills and ADRs are the authority, not the repo's current code" is removed. Current live source is truth about current behaviour; skills and ADRs provide constraints and intended architecture whose freshness must be checked against source.
3. The claim that "The aggregate root enforces invariants and returns Result objects for failures" is removed as unsupported Wild Bunch-specific doctrine. The DDD skill description is shortened to tactical patterns only.

**File:** `sources/first_party/skills/wild-bunch-project-doctrine/references/skill-routing.md`

**Exact content to write:**

```markdown
# Skill Routing

Consolidated from the Wild Bunch repo root `AGENTS.md` at commit `a65ca6c2`. Invoke these skills before relevant work. `/using-superpowers` is the primary workflow entrypoint and routes to specialist skills.

## Session Bootstrap

- `/using-superpowers` — Use for workflow-sensitive project/repo work. Establishes how to find and use skills, requiring skill invocation before repo-sensitive responses. Not required for ordinary chat or questions that do not touch repo work.
- `/work-mode-router` — Use when a project context begins, a session resumes, or a request may involve coding dispatch, workers, issues, artifacts, verification, or publication.
- `/inspecting-the-environment` — Use when about to take action and environment constraints could change the next step. Discovers shell syntax, worktree state, repo state, path style, CLI availability, auth, connectors, mutation authority, and protected surfaces before proceeding.
- `/using-git-worktrees` — Use when starting feature work that needs isolation from current workspace or before executing implementation plans.

**Note**: `/inspecting-the-environment` is part of the trimmed `superpowers+` surface and should be kept explicit for environment-constraint discovery.

## Linear & GitHub Work

- `/using-linear` — Use when working with the Linear connector surface, choosing the right tool call, or finding create/update tools exposed under `save_*` rather than `create_*` or `update_*`.
- `/linear-issue-shaping` — Use when Linear-backed issue, project, and document shaping: create or update worker-ready Linear issues, inspect Linear comments/attachments/state, prepare paste-ready worker handoffs when explicitly requested, and route GitHub PR proof after a PR exists.
- `/github-operations` — Use when verifying GitHub repository evidence without taking over coding workflow routing. Use after a Linear/Codex task has a GitHub PR, branch, commit, review, merge, status, or file-state question; when checking publication proof, PR diff scope, mergeability, CI/status evidence, final main state, or GitHub-specific closure proof.
- `/repo-worker-base` — Use for fresh-main discipline, worktree isolation, branch and PR hygiene, validation evidence, or publication proof.

## Anti-Slop & Quality

- `/unslop-plus` — Use when applying domain-specific anti-slop profiles for common software development workflows, with thirteen portable profiles for writing, technical-writing, implementation-plans, code-review, worker-returns, debugging, frontend-react, frontend-ui, api-design, architecture, testing, security-review, and cleanup-custody.
- `/connector-safety` — Use when a connector or tool call is blocked, rejected, safety-filtered, permission-rejected, or when a planned action could be sensitive or destructive.
- `/verification-before-completion` — Use before claiming work is complete, fixed, or passing, before committing or creating PRs.

## Planning & Execution

- `/brainstorming` — Use before any creative work: creating features, building components, adding functionality, or modifying behavior.
- `/writing-plans` — Use when you have a spec or requirements for a multi-step task, before touching code.
- `/test-driven-development` — Use when implementing any feature or bugfix, before writing implementation code.
- `/systematic-debugging` — Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes.

## Repo-Specific Skills

- `/wild-bunch-project-doctrine` — Use before any repo-sensitive change, when work touches worker dispatch, worker return verification, source-truth claims, or issue-goal conformance. Establishes posture first, then routes to specialist skills.
- `/repo-worker-base` — Use for fresh-main discipline, worktree isolation, branch and PR hygiene, validation evidence, or publication proof.
- `/wild-bunch-dotnet-architecture` — Use when applying Wild Bunch .NET architecture guardrails for C#/.NET repo work touching GameSession live-play flows, persistence, or CQRS/read models.
- `/wild-bunch-domain-modeling` — Use when applying Wild Bunch project-scoped domain guidance for DDD tactical modeling, GameSession boundaries, player wallet or inventory, or travel rules.
- `/wild-bunch-browser-game` — Use when work touches browser delivery, HUD design, Phaser/TypeScript/Vite, DOM overlays, playtest evidence, or dev-server checks.

**Note**: For Linear/GitHub/architecture/anti-slop routing, use direct skills and repo-local doctrine instead of compositional middlemen. The retired `*-superpowers` compositional skills have been removed from the marketplace.

## Architecture Skills (must invoke before touching domain, persistence, or command/query handlers)

- `/ddd` — DDD tactical patterns: aggregates, value objects, domain events, strongly-typed IDs.
- `/cqrs-event-sourcing` — CQRS and Event Sourcing patterns: command/query separation, events as source of truth, projections for reads.
- `/event-driven-architecture` — Event-driven architecture patterns for domain events and projections.
- `/clean-architecture` — Layered .NET system structure: Domain, Application, Infrastructure, Api projects, dependency inversion.
- `/wild-bunch-dotnet-architecture` — Wild Bunch-specific .NET architecture guardrails: GameSession as aggregate root, event-sourced command flows, JSON snapshot cache, persistence boundaries.
- `/wild-bunch-domain-modeling` — Wild Bunch domain modeling: GameSession boundaries, player wallet/inventory, travel rules, clue/journal flows, hidden culprit truth.
- `/ef-core` — Entity Framework Core patterns when persistence work touches DbContext, migrations, or queries.
- For architecture work, inspect current source and canonical repo decisions, then invoke the smallest relevant specialist skill above. Do not hand-roll non-DDD, non-CQRS, or non-event-sourced solutions. Current live source is truth about current behaviour; skills and ADRs provide constraints and intended architecture whose freshness must be checked against source and current requirements.

## Specialist Skill Discovery

When work touches architecture, domain modeling, persistence, frontend, browser-game delivery, testing, or other specialist areas:
1. First inspect the current repo source and canonical repo decisions.
2. Use `/using-superpowers` or skill discovery to find and invoke the smallest relevant specialist skill.
3. Do not treat the skills catalog as a complete list of specialist skills.

For the complete skills inventory, see `.agents/docs/skills-catalog.md` in the wild-bunch repo.
```

- [x] Step 3 complete

---

## Step 4: Create `references/policy-references.md`

Create a new reference doc consolidating the "Script Discovery", "Policy Reference", and "ADR Log Freshness" sections from the wild-bunch AGENTS.md. All paths are relative to the wild-bunch repo root.

**File:** `sources/first_party/skills/wild-bunch-project-doctrine/references/policy-references.md`

**Exact content to write:**

```markdown
# Policy References

Consolidated from the Wild Bunch repo root `AGENTS.md` at commit `a65ca6c2`. All paths are relative to the wild-bunch repo root.

## Script Discovery

Scripts in `scripts/` are first-class surfaces. Before reporting environmental issues or running ad-hoc commands, read `scripts/AGENTS.md` and use the provided scripts.

When you encounter:
- PostgreSQL connection errors or missing database → read `scripts/AGENTS.md` and use `postgres-dev.ps1`
- Dev servers not running → read `scripts/AGENTS.md` and use `dev-servers.ps1`
- Need to regenerate index mesh → read `scripts/AGENTS.md` and use `generate_index_mesh.py` or `generate_index_mesh.ps1`
- Need to sync marketplace skills → read `scripts/AGENTS.md` and use `install_agent_skills.py` or `install_agent_skills.ps1`
- Need image asset processing → read `scripts/AGENTS.md` and use `image_asset_pipeline.py` or `image_asset_pipeline.ps1`

**Do not report "environmental issue" or "missing tooling" without first checking `scripts/AGENTS.md`.** The scripts folder is the canonical way to perform these operations and must be treated as a first-class discovery surface.

## Policy Reference

Use these reference files when working in specific areas:

- **[`.agents/docs/workflow-policy.md`](.agents/docs/workflow-policy.md)** — Use when managing git workflow, claiming completion, publishing PRs, or verifying issue-goal alignment.
- **[`.agents/docs/validation-policy.md`](.agents/docs/validation-policy.md)** — Use when running validation, debugging CI failures, or deciding test coverage scope. Documents the repo's five test kinds (unit, integration, game-content, API, brute-force) and when to use each.
- **[`.agents/docs/artifact-policy.md`](.agents/docs/artifact-policy.md)** — Use when creating agent artifacts, managing screenshots/evidence, or working with unslop profiles.
- **[`.agents/docs/architecture-guardrails.md`](.agents/docs/architecture-guardrails.md)** — Use when making architecture decisions, touching GameSession, modifying persistence, or working with seed codecs.
- **[`.agents/docs/coding-discipline.md`](.agents/docs/coding-discipline.md)** — Use when writing code, deciding scope boundaries, or refactoring.
- **[`.agents/docs/worker-environment.md`](.agents/docs/worker-environment.md)** — Use when working with connectors, handling images, running dev services, or managing worker cleanup.
- **[`.agents/docs/repo-skills-policy.md`](.agents/docs/repo-skills-policy.md)** — Use when syncing marketplace skills or working with the skill vendoring system.
- **[`.agents/doctrine/mesh-policy.md`](.agents/doctrine/mesh-policy.md)** — Use when working with the documentation mesh (AGENTS.md, INDEX.md, README files).
- **[`.agents/docs/guides/implementing-guide.md`](.agents/docs/guides/implementing-guide.md)** — **Must read for implementers.** Standards to read before coding, skills to invoke, TDD discipline, pre-completion verification, PR/Linear/plan honesty, and subagent dispatch guidance.
- **[`.agents/docs/guides/planning-guide.md`](.agents/docs/guides/planning-guide.md)** — **Must read for planners.** Standards to read before planning, skills to invoke, plan structure requirements, artifact placement, and plan review checklist.
- **[`.agents/docs/guides/design-guide.md`](.agents/docs/guides/design-guide.md)** — **Must read for brainstormers and spec authors.** Standards to read before turning ideas into design specs, including the spec self-review and handoff confidence floor.

## ADR Log Freshness

The ADR log at `docs/adr/` must represent the system as it exists today. See [`.agents/docs/workflow-policy.md`](.agents/docs/workflow-policy.md) for freshness check requirements.
```

- [x] Step 4 complete

---

## Step 5: Update `references/repo-posture.md`

Replace the entire contents of `references/repo-posture.md` with the following. This keeps the existing posture rules and adds script discovery + specialist skill discovery guidance, plus pointers to the companion reference docs.

**File:** `sources/first_party/skills/wild-bunch-project-doctrine/references/repo-posture.md`

**Exact replacement content:**

```markdown
# Repo Posture

- Wild Bunch is a mainline-only C#/.NET game project in `HarleyBartles/wild-bunch`.
- Current `main` is the live truth.
- Do not rely on chat summaries, issue comments, or worker reports as final state.
- Inspect live source before asserting what the repo does today.
- GPT prepares the worker packet.
- Harley sends the packet.
- The worker executes the packet and reports the result.
- Return payloads should include branch, commit SHA, PR URL or number, validation commands, and issue-goal conformance notes.

## Script discovery

Scripts in `scripts/` are first-class surfaces. Before reporting environmental issues or running ad-hoc commands, read `scripts/AGENTS.md` and use the provided scripts. See [Policy References](policy-references.md) for the full script discovery map.

## Specialist skill discovery

For specialist work (architecture, domain modeling, browser delivery, testing, etc.), inspect current source and canonical repo decisions first, then invoke the smallest relevant specialist skill. See [Skill Routing](skill-routing.md) for the full routing map.

## Companion references

- [Working Knowledge](working-knowledge.md) — worktree/scratch locations, required reading before specific work types.
- [Skill Routing](skill-routing.md) — full skill routing map for the Wild Bunch repo.
- [Policy References](policy-references.md) — policy reference map, script discovery, ADR log freshness.
- [Difficulty, Entropy, and Seeded Setup Doctrine](difficulty-entropy-seeded-world-setup.md) — world-start setup, seeded identity, entropy, difficulty.
```

- [x] Step 5 complete

---

## Step 6: Update `agents/openai.yaml`

Replace the entire contents of `agents/openai.yaml` with the following. This aligns the display name, short description, and default prompt with the expanded skill scope.

**File:** `sources/first_party/skills/wild-bunch-project-doctrine/agents/openai.yaml`

**Exact replacement content:**

```yaml
interface:
  display_name: Wild Bunch Project Doctrine
  short_description: Bootstrap the Wild Bunch repo posture, working knowledge, skill routing,
    and policy references before any change
  default_prompt: Establish the live repo posture for HarleyBartles/wild-bunch before
    making changes. Covers working knowledge, skill routing, script discovery, and policy
    references.
policy:
  products:
  - chatgpt
  - codex
  - api
  - atlas
  allow_implicit_invocation: true
```

- [x] Step 6 complete

---

## Step 7: Regenerate marketplace projections and run full rebuild + validation

After all source edits are complete, regenerate the marketplace projections and run the full rebuild + validation gate. Final completion requires both commands to succeed with no unresolved drift.

**Commands:**
```bash
py -3 tools/rebuild_marketplace.py
py -3 tools/check_marketplace.py
```

**Completion criteria (all must be met):**
- `rebuild_marketplace.py` exits 0 with all validation lines reporting OK
- `check_marketplace.py` exits 0 — this includes `git diff --exit-code` passing, which means all generated surfaces are committed and there is no drift between source and generated state
- Repo index validation passed
- Index mesh current (no stale INDEX.md files)
- All projection-lane plugins validated
- No drift between source and generated surfaces

If `check_marketplace.py` fails on `git diff --exit-code`, it means generated files were not committed. Stage and commit the regenerated files, then re-run `check_marketplace.py` until it exits 0. A failing `git diff --exit-code` is not an acceptable final result.

**Verify the projected skill reflects changes:**
After rebuild, confirm that `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-project-doctrine/SKILL.md` contains the expanded frontmatter and reference routing, and that the `references/` directory there contains the 4 reference files (working-knowledge.md, skill-routing.md, policy-references.md, repo-posture.md) plus the existing difficulty-entropy-seeded-world-setup.md.

- [x] Step 7 complete

---

## Verification checklist

- [x] Step 0: Pre-implementation source evidence check completed (all paths verified at `a65ca6c2`)
- [x]SKILL.md frontmatter has 7 `use_when` entries and 2 `do_not_use_when` entries that preserve the bootstrap-then-route contract
- [x]SKILL.md body has 2 new rules (script discovery, specialist skill discovery)
- [x]SKILL.md References section routes to all 5 reference docs
- [x]`references/working-knowledge.md` exists with worktree/scratch locations and required reading list
- [x]`references/skill-routing.md` exists with all 6 skill routing categories + specialist discovery, with narrowed `/using-superpowers` trigger, removed "authority not repo code" claim, and removed unsupported "returns Result objects" detail
- [x]`references/policy-references.md` exists with script discovery, policy reference map, and ADR freshness
- [x]`references/repo-posture.md` updated with script discovery, specialist skill discovery, and companion references
- [x]`agents/openai.yaml` updated with expanded scope language
- [x]`py -3 tools/rebuild_marketplace.py` exits 0 (all validation OK)
- [x]`py -3 tools/check_marketplace.py` exits 0 (all validation OK, `git diff --exit-code` passes — no drift)
- [x]Projected skill in `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-project-doctrine/` reflects all changes
