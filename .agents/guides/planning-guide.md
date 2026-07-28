# Planning Guide

Use this reference when planning work in the agent-asset-marketplace repo — before writing an implementation plan, before touching code. This guide covers the planner workflow: what to read before planning, what skills to invoke, what a plan must contain, and where plan artifacts go.

## Before You Begin: Read the Standards

A plan that doesn't account for the repo's standards will produce implementations that fail review. Read these before planning:

- **[`docs/custody-and-projection-doctrine.md`](../../docs/custody-and-projection-doctrine.md)** — source custody rules, provenance modes, plugin curation rules
- **[`AGENTS.md`](../../AGENTS.md)** — repository source-of-truth and publication rules
- **[`tools/AGENTS.md`](../../tools/AGENTS.md)** — marketplace generation and validation tooling

## Skills to Invoke

- Invoke `/brainstorming` before any creative work, then invoke `/writing-plans` once the spec is ready
- Invoke `/repo-worker-base` before planning work that touches marketplace generation, validation, or tooling

## Plan Structure

Every implementation plan in this repo must contain:

- **Task breakdown** — the work divided into independently implementable tasks, each with a clear scope and no shared mutable state between tasks (for SDD parallel execution)
- **Exact code** — each task step contains the exact code to write, not prose descriptions. Implementers should be transcribing, not designing
- **File structure** — which files to create, modify, or delete. Each file has one clear responsibility
- **Test cases** — each task specifies the test cases to write, with TDD ordering (failing test first, then implementation). Specify the validation approach (marketplace regeneration, CI checks)
- **Commit messages** — each task specifies its commit message
- **Expected interim state** — tasks that leave the build in a temporarily broken state (e.g. validation errors fixed by a later task) must document this explicitly so the implementer knows it's expected
- **SDD confidence rating** — the plan includes a confidence rating (0-10) reflecting how well-specified the tasks are for subagent-driven execution. This rating must be the result of an honest execution confidence assessment (see below), not a self-assigned number

## Plan Artifact Placement

Plans go in `.agents/superpowers/plans/` with a descriptive filename (e.g. `2026-07-09-add-skill-pack.md`).

Session artifacts (task briefs, reports, review diffs) go in `.agents/superpowers/sdd/<plan-name>/`.

Do not create loose files at repo root. Do not place agent-generated artifacts under `docs/` or product source folders.

## Plan Review

Before executing a plan, run through this checklist. Each item is a general principle — the examples are illustrative, not exhaustive.

### Structural integrity
1. **Marketplace regeneration completeness.** If the plan adds or modifies skills, verify the plan includes marketplace regeneration steps. Skills must be regenerated via `tools/run marketplace --apply` to project changes into all packs.
2. **Validation command correctness.** Verify the plan uses the correct validation commands: `tools/run ci --check` for CI, `tools/run marketplace --apply` for local rebuild.
3. **Tooling integration.** If the plan modifies tooling, verify the plan updates the relevant AGENTS.md files to reflect the new commands or workflows.

### Test infrastructure
4. **Validation isolation.** Do the validation steps run independently without requiring external state? Marketplace validation should work in a clean checkout.
5. **Artifact placement.** Are generated artifacts (skill zips, manifests, source maps) placed in the correct derived locations, not hand-edited?
6. **Validation kind selection.** Is the right validation approach used? Marketplace changes require full regeneration and validation, not partial refresh.

### Execution safety
7. **Interim state documentation.** Are temporary validation failures between tasks documented so the implementer knows they're expected? An interim validation failure that's fixed by a later task is acceptable if documented.
8. **Task independence.** Can each task be executed independently without shared mutable state between tasks? SDD parallel execution requires independence.

## Execution Confidence Assessment (required before reporting ready)

Before reporting a plan as ready for execution, the planner must honestly assess the plan's execution confidence. This is not a formality — it is a verification step that catches gaps the planner would otherwise discover too late.

### How to assess

For each task in the plan, ask: **"If a competent implementer (or subagent) executed this task exactly as written, would they produce the right thing without needing to discover and solve problems in flight?"**

Verify the plan's assumptions against the actual source code, not against the planner's memory or earlier exploration. Specifically:

1. **Verify every file path, skill name, and tooling command the plan references.** Open the files. Confirm the paths, names, and commands match what the plan assumes.
2. **Verify every "follows the X pattern" claim.** Read the referenced pattern (e.g. existing skill structure). Is the pattern concrete enough to replicate?
3. **Verify every "new code" claim.** If the plan says "create new skill", confirm nothing similar already exists.
4. **Verify every marketplace configuration.** Read the current marketplace.json, plugin manifests, and registry. Are the fields the plan expects to extend actually there?
5. **Verify every integration site.** If the plan says "add to tools/run", open that script and confirm the integration is possible as described.
6. **Identify underspecified design decisions.** If a task requires the implementer to make design decisions that aren't specified in the plan, that's a gap.

### Gap closure obligation

If the assessment finds gaps, the planner must **close the obvious gaps before reporting the plan as ready**. This means:

- **Stale references** (renamed files, moved tools, changed commands): fix them in the plan
- **Missing verification**: verify against current source and update the plan with the correct paths and commands
- **Underspecified algorithms**: specify the algorithm concretely enough that the implementer is transcribing, not designing
- **Underspecified interfaces**: define the exact function signatures, type shapes, or configuration the implementer should write
- **Missing validation steps**: add the required marketplace regeneration and validation commands

If a gap cannot be closed without user input or discovery, flag it explicitly in the plan and lower the confidence rating accordingly. Do not hand off a plan with known gaps and hope the implementer will solve them.

## When Confidence is Below 8/10

If the honest confidence assessment is below 8/10, do not hand off the plan yet. Instead:

1. Close the obvious gaps (stale references, missing verification, underspecified decisions)
2. Verify against current source for every assumption
3. If remaining gaps require user input, surface them explicitly in the plan and lower the confidence rating
4. Only hand off when the plan is as de-risked as the current source allows

## What a Plan Is Not

- A plan is not a design spec
- A plan is not a commit log
- A plan is not permission to broaden the work beyond the asked slice
- A plan is not ready until it can hand off cleanly to implementation without forcing the implementer to invent the contract
