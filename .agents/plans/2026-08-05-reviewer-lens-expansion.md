# Reviewer lens expansion — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use /subagent-driven-development (recommended) or /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `reviewer-plans`, `reviewer-mesh`, and `reviewer-scripts` portable subagent profiles, add `## Applies to` dispatch rules to lens profiles, update `selecting-a-subagent` and `iterative-review` to use those rules, and package the changes.

**Architecture:** Each `reviewer-*.md` profile owns its own `## Checklist`, `## Applies to`, and `## Stop condition and loop breaker` sections. `iterative-review` discovers every `.agents/agents/reviewer-*.md` at run time, reads its `## Applies to`, and dispatches only the lenses whose globs/keywords/inputs match the PR. `selecting-a-subagent` documents the contract. `reviewer-marketplace` is already repo-local and scoped to this repo; no rewrite is needed beyond confirming it does not duplicate `reviewer-mesh`. `reviewer-mesh` is the canonical portable lens for generated `INDEX.md`, mesh, scaffolder output, and `repo-standards` surfaces; it replaces the separate `reviewer-scaffolders` profile.

**Tech Stack:** Devin Desktop custom subagent `.md` profiles, `codex-marketplace` plugin source, `py -3 tools/run.py` for regeneration/validation.

**Global Constraints**
- Portable skill sources are edited under `codex-marketplace/plugins/superpowers-plus/skills/`; `.agents/skills/` are generated installed copies.
- `.agents/agents/reviewer-*.md` runtime profiles are the consumer-visible surface; their canonical product source is `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/`.
- Do not reintroduce `reviewer-known-findings.md` or any shared findings ledger; each lens owns its own `## Checklist`.
- This branch already moves completed plans/specs to `.agents/plans/completed/` and `.agents/specs/completed/`; do not modify those historical files.

**Spec:** `.agents/specs/2026-08-05-reviewer-lens-expansion-design.md`
**Spec handoff rating:** 9/10

---

### Task 0: Verify the existing lens profiles and source-of-truth locations

**Files:**
- Read: `.agents/agents/reviewer-skills.md`
- Read: `.agents/agents/reviewer-security.md`
- Read: `.agents/agents/reviewer-marketplace.md`
- Read: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/SKILL.md`
- Read: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`
- Read: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/` (list the directory)

**Interfaces:**
- Consumes: current lens profiles and skill sources.
- Produces: confirmed paths for edits in later tasks.

- [x] **Step 0.1: Confirm the source skill paths**

Run: `Get-ChildItem 'codex-marketplace\plugins\superpowers-plus\skills\' | Select-Object -ExpandProperty Name`
Expected: `selecting-a-subagent` and `iterative-review` directories are present.

- [x] **Step 0.2: Confirm the pack profile source path**

Run: `Get-ChildItem 'codex-marketplace\plugins\superpowers-plus\skills\selecting-a-subagent\assets\' | Select-Object -ExpandProperty Name`
Expected: Existing portable profiles (`reviewer.md`, `reviewer-fast.md`, `reviewer-strong.md`, `reviewer-security.md`, `reviewer-skills.md`) are present; `reviewer-marketplace.md` is repo-local and lives in `.agents/agents/`.

- [x] **Step 0.3: Commit the baseline verification**

Run: `git status --short`
Expected: No unexpected modifications other than the plan/spec files and the completed/ moves from this branch.

```bash
git add -A
git commit -m "Verify baseline for reviewer lens expansion work"
```

---

### Task 1: Create or update `.agents/agents/reviewer-plans.md`

**Files:**
- Create: `.agents/agents/reviewer-plans.md`

**Interfaces:**
- Consumes: spec `Contract and file targets` for `reviewer-plans`.
- Produces: a portable `reviewer-plans` lens profile.

- [x] **Step 1.1: Write the file with the following exact content**

```markdown
---
name: reviewer-plans
runtime: devin-desktop
description: Portable plan/spec/roadmap lens — reviews plans in isolation and PR compliance against declared governing documents.
model: glm-5-2
allowed-tools:
  - read
  - grep
  - find_file_by_name
  - exec
  - mcp_list_servers
  - mcp_list_tools
  - mcp_call_tool
  - write
---

You are `reviewer-plans`, a focused read-only reviewer for plans, specs, roadmaps, and for PR compliance against them. In isolation mode, read only the plan/spec/roadmap and verify it is ready for implementation planning. In PR compliance mode, read the diff plus the governing documents and flag where the implementation drifts from what was declared.

## Applies to

Use this section to decide whether `reviewer-plans` should be dispatched for a PR.

- globs:
  - `.agents/specs/**`
  - `.agents/plans/**`
  - `.agents/roadmaps/**`
  - `**/*-design.md`
  - `**/*-plan.md`
  - `**/*-roadmap.md`
- keywords:
  - plan
  - spec
  - roadmap
  - scope
- inputs:
  - `<plan_path>`
  - `<spec_path>`
  - `<roadmap_path>`

## Checklist

Use this checklist during `orchestrator-self-review` and as the core of the diff review:

1. **Completeness** — no TODOs, TBD, placeholders, or incomplete sections in the plan/spec.
2. **Consistency** — no internal contradictions.
3. **Clarity** — requirements are concrete enough that an implementer would not build the wrong thing.
4. **Scope** — fits in one plan; no YAGNI or speculative features.
5. **Buildability** — tasks are actionable and independently verifiable.
6. **PR scope fidelity** — the implemented scope in the diff matches the declared plan/spec.
7. **Surface drift** — new packs, renamed surfaces, or dropped features that are not in the plan are flagged.
8. **Roadmap order** — later-phase items are not implemented before their prerequisites.
9. **Traceability** — every changed surface can be mapped to a governing document item.

## Invariants

- You are read-only. Do not modify repo files or run build/install/write commands. You may write the off-repo `review-log-plans.md` report.
- You may use `exec` for non-mutating `git` queries and canonical verification commands, and `mcp_call_tool` for non-mutating lookups. Use these only to resolve refs or confirm state — not to generate the diff, not to fetch a missing package, and not to install/change anything.
- If a governing document path is provided but is not a file, report that and stop.
- If the prepared diff package is missing or the `diff_path` is not a file, report that and stop; do not use `git` or `exec` to recreate it.
- Cite specific files and line numbers for every issue you find.
- If you cannot verify something, say so clearly rather than guessing.
- Keep feedback focused, concrete, and actionable.

## Inputs the orchestrator must provide

- `<diff_path>` (optional) — path to a prepared diff file when reviewing a branch.
- `<plan_path>` (optional) — path to the governing plan file.
- `<spec_path>` (optional) — path to the governing spec file.
- `<roadmap_path>` (optional) — path to the governing roadmap file.
- `<pr_description>` (optional) — the PR title, body, and any linked issue/spec context.
- `<scan_findings>` (optional) — the consumer repo's preflight output.
- `<review-log-orchestrator-self-review>` (optional) — the orchestrator's prediction log.
- `<regression_diff_path>` (optional) — the fix diff only, used for `regression-scan`.

Do not generate the diff yourself. The orchestrator owns diff preparation.

## How to dispatch this reviewer

The orchestrator dispatches this profile with `run_subagent` (or the consumer's equivalent subagent mechanism). The `task` should list the concrete input paths and the off-repo output path. Do not ask the subagent to read this profile; the profile body is the injected instruction set. Set the off-repo scratch directory as the subagent's working directory.

In isolation mode, dispatch without `<diff_path>` and with the relevant `<plan_path>` / `<spec_path>` / `<roadmap_path>`.
In PR compliance mode, dispatch with `<diff_path>` plus the relevant governing document paths.

## What to write

Write `review-log-plans.md` in the off-repo scratch. Begin with a brief `## Inputs` section, then list findings with `file:line`, severity, description, and remediation. End with `reviewer-plans: N issue(s)` or `reviewer-plans: clean`.

## Procedure

1. If `<scan_findings>` is provided, read it first and do not duplicate its findings; verify the preflight caught the pattern in the right place.
2. If `<pr_description>` is provided, read it for scope.
3. If any of `<plan_path>`, `<spec_path>`, or `<roadmap_path>` is provided, read them in that order and keep them as the governing scope.
4. If `<diff_path>` is provided, read it. If it truncates, use the overflow file or re-read with `offset` and `limit`.
5. Apply the `## Checklist`.
6. Use `grep` and `find_file_by_name` to confirm canonical paths and traceability claims.
7. Report only plan/spec/roadmap or scope issues. Cite `file:line`, severity, and remediation.
8. End with `reviewer-plans: N issue(s)` or `reviewer-plans: clean`.

## Output format

For each issue:
- `file:line` reference.
- Severity: **blocking** / **important** / **minor**.
- What is wrong and why it matters for the plan/spec/roadmap.
- How to fix.

Do not include non-plan findings.

Append the `## Stop condition and loop breaker` section from Task 9 to the end of the file.
```

- [x] **Step 1.2: Add `reviewer-plans.md` to the repo-worker-pack profile source**

If the pack at `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/` is the source of truth for `.agents/agents/` runtime profiles, copy the file you just created into that directory:

```bash
cp ".agents\agents\reviewer-plans.md" "codex-marketplace\plugins\superpowers-plus\skills\selecting-a-subagent\assets\reviewer-plans.md"
```

- [x] **Step 1.3: Commit the new profile**

Run: `git status --short`
Expected: `reviewer-plans.md` is staged.

```bash
git add .agents/agents/reviewer-plans.md
git add codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-plans.md
git commit -m "Add portable reviewer-plans lens profile"
```

---

### Task 2: Create `.agents/agents/reviewer-mesh.md`

**Files:**
- Create: `.agents/agents/reviewer-mesh.md`

**Interfaces:**
- Consumes: spec `Contract and file targets` for `reviewer-mesh`.
- Produces: a portable `reviewer-mesh` lens profile.

- [x] **Step 2.1: Copy the `reviewer-mesh` profile from the pack source**

Use the pack source at `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-mesh.md`.
It is the canonical scaffolder/mesh lens and absorbs the old `reviewer-scaffolders` responsibilities; do not hand-edit `.agents/agents/reviewer-mesh.md`.


- [x] **Step 2.2: Add `reviewer-mesh.md` to the repo-worker-pack profile source**

```bash
cp ".agents\agents\reviewer-mesh.md" "codex-marketplace\plugins\superpowers-plus\skills\selecting-a-subagent\assets\reviewer-mesh.md"
```

- [x] **Step 2.3: Commit the new profile**

```bash
git add .agents/agents/reviewer-mesh.md
git add codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-mesh.md
git commit -m "Add portable reviewer-mesh lens profile"
```

- [x] **Step 2.4: Write the portable `reviewer-scripts.md` pack source**

Use the spec checklist and the same frontmatter/structure as `reviewer-plans.md` and `reviewer-mesh.md`. The profile must:
- Declare `## Applies to` with `globs` for `**/scripts/**`, `**/tools/**`, `**/*.py`, `**/*.sh`, `**/*.ps1`, and `**/*.bash`.
- Declare `## Checklist` covering CLI flag contracts, read-only/mutating/mixed classification, exit-code hygiene, shebang/invocation, path safety, and cross-skill script path existence.
- Require only `<diff_path>` and optional `<pr_description>` / `<scan_findings>` / `<review-log-orchestrator-self-review>` inputs.
- Write `review-log-scripts.md` to the off-repo scratch.
- Append the `## Stop condition and loop breaker` section from Task 9 to the end of the file.

- [x] **Step 2.5: Run `py -3 tools/run.py marketplace --apply`**

Expected: `.agents/agents/reviewer-scripts.md` is installed from the pack source and `.provenance.json` is updated.

- [x] **Step 2.6: Commit the new profile**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-scripts.md
git add .agents/agents/reviewer-scripts.md
git commit -m "Add portable reviewer-scripts lens profile"
```

---

### Task 3: Add `## Applies to` sections to the existing portable lens profiles

**Files:**
- Modify: `.agents/agents/reviewer-skills.md`
- Modify: `.agents/agents/reviewer-security.md`
- Modify: `.agents/agents/reviewer-marketplace.md`

**Interfaces:**
- Consumes: current lens profiles.
- Produces: profiles with `## Applies to` for `iterative-review` dispatch.

- [x] **Step 3.1: Update `reviewer-skills.md`**

Insert `## Applies to` immediately after the frontmatter `---` and before `## Checklist`. Use the `edit` tool with the following `old_string` / `new_string`:

```text
old_string: |
  ---

  You are `reviewer-skills`, a focused read-only reviewer for `SKILL.md` and reference files. Inspect the prepared diff for frontmatter schema, markdown tables, repo conventions, and prompt robustness. Do not broaden to marketplace tooling or secrets; those are handled by other lens reviewers.

  ## Checklist
new_string: |
  ---

  You are `reviewer-skills`, a focused read-only reviewer for `SKILL.md` and reference files. Inspect the prepared diff for frontmatter schema, markdown tables, repo conventions, and prompt robustness. Do not broaden to marketplace tooling or secrets; those are handled by other lens reviewers.

  ## Applies to

  - globs:
    - `**/*.md`
    - `**/.agents/skills/**`
  - keywords:
    - skill
    - SKILL.md
    - reference
  - inputs:
    - `<diff_path>`

  ## Checklist
```

- [x] **Step 3.2: Update `reviewer-security.md`**

Insert `## Applies to` immediately after the frontmatter `---` and before `## Checklist`:

```text
old_string: |
  ---

  You are `reviewer-security`, a focused read-only security/PII reviewer. Inspect a prepared branch/PR diff for secrets and real identifiers that should not be in source. Do not broaden the review to design, style, or marketplace concerns; those are handled by other lens reviewers.

  ## Checklist
new_string: |
  ---

  You are `reviewer-security`, a focused read-only security/PII reviewer. Inspect a prepared branch/PR diff for secrets and real identifiers that should not be in source. Do not broaden the review to design, style, or marketplace concerns; those are handled by other lens reviewers.

  ## Applies to

  - globs:
    - `**/*`
  - keywords:
    - secret
    - token
    - key
    - credential
  - inputs:
    - `<diff_path>`

  ## Checklist
```

- [x] **Step 3.3: Update `reviewer-marketplace.md`**

Insert `## Applies to` immediately after the frontmatter `---` and before `## Checklist`:

```text
old_string: |
  ---

  You are `reviewer-marketplace`, a focused read-only reviewer for `codex-marketplace` pack generation, generated indexes, and repo tooling. Inspect the prepared diff for `new_plugin.py`, `tools/run.py`, `plugin-roots.json`, `bundle-manifest.json`, `repo-index/**`, and related surfaces. Do not broaden to prose/style or secrets; those are handled by other lens reviewers.

  ## Checklist
new_string: |
  ---

  You are `reviewer-marketplace`, a focused read-only reviewer for `codex-marketplace` pack generation, generated indexes, and repo tooling. Inspect the prepared diff for `new_plugin.py`, `tools/run.py`, `plugin-roots.json`, `bundle-manifest.json`, `repo-index/**`, and related surfaces. Do not broaden to prose/style or secrets; those are handled by other lens reviewers.

  ## Applies to

  - globs:
    - `tools/new_plugin.py`
    - `tools/run.py`
    - `plugin-roots.json`
    - `bundle-manifest.json`
    - `repo-index/**`
    - `codex-marketplace/manifest.json`
    - `.agents/plugins/marketplace.json`
    - `codex-marketplace/**`
  - keywords:
    - marketplace
    - new_plugin
    - run.py
    - manifest
  - inputs:
    - `<diff_path>`

  ## Checklist
```

- [x] **Step 3.4: Copy the updated profiles to the pack source**

```bash
cp ".agents\agents\reviewer-skills.md" "codex-marketplace\plugins\superpowers-plus\skills\selecting-a-subagent\assets\reviewer-skills.md"
cp ".agents\agents\reviewer-security.md" "codex-marketplace\plugins\superpowers-plus\skills\selecting-a-subagent\assets\reviewer-security.md"
cp ".agents\agents\reviewer-marketplace.md" "codex-marketplace\plugins\superpowers-plus\skills\selecting-a-subagent\assets\reviewer-marketplace.md"
```

- [x] **Step 3.5: Commit the applies-to updates**

```bash
git add .agents/agents/reviewer-skills.md
git add .agents/agents/reviewer-security.md
git add .agents/agents/reviewer-marketplace.md
git add codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-skills.md
git add codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-security.md
git add codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-marketplace.md
git commit -m "Add Applies to dispatch rules to existing lens profiles"
```

---

### Task 4: Update `selecting-a-subagent/SKILL.md`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/SKILL.md`

**Interfaces:**
- Consumes: current dispatch table.
- Produces: dispatch table with `reviewer-plans`, `reviewer-mesh`, `reviewer-scripts`, and `## Applies to` documentation.

- [x] **Step 4.1: Add the new profiles to the dispatch table**

Use `edit` to replace the `reviewer-marketplace` row with the same row plus the two new ones:

```text
old_string: |
  | `SKILL.md`/reference/prompt-robustness lens | `reviewer-skills` |
  | `codex-marketplace`/tooling/pack lens | `reviewer-marketplace` |
  | Small, tightly focused reviews or coherent single-responsibility re-review diffs | `reviewer-fast` |
new_string: |
  | `SKILL.md`/reference/prompt-robustness lens | `reviewer-skills` |
  | Scaffolder/mesh/`INDEX.md` lens | `reviewer-mesh` |
  | New or changed scripts / CLI tooling | `reviewer-scripts` |
  | `codex-marketplace`/tooling/pack lens | `reviewer-marketplace` |
  | Plan/spec/roadmap review and PR compliance | `reviewer-plans` |
  | Small, tightly focused reviews or coherent single-responsibility re-review diffs | `reviewer-fast` |
```

- [x] **Step 4.2: Document the `## Applies to` contract**

Add a new short section after the dispatch table. Replace the paragraph that begins "The orchestrator must provide a `<diff_path>`" with the following:

```text
old_string: |
  The orchestrator must provide a `<diff_path>` and optional `<pr_description>` to any
  reviewer profile. The reviewer subagent does not resolve the diff itself.

  ## Repo-specific lens profiles
new_string: |
  The orchestrator must provide a `<diff_path>` and optional `<pr_description>` to any
  reviewer profile. The reviewer subagent does not resolve the diff itself.

  Each portable and repo-local `reviewer-*.md` profile declares an `## Applies to` section
  that `iterative-review` uses to decide whether the lens is relevant to a given PR. The
  section contains `globs`, `keywords`, and `inputs`. Do not point to any shared
  `reviewer-known-findings.md` file; it has been removed and each lens now owns its
  `## Checklist`.

  ## Repo-specific lens profiles
```

- [x] **Step 4.3: Commit the skill update**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/SKILL.md
git commit -m "Update selecting-a-subagent dispatch table for reviewer-plans, reviewer-mesh, and reviewer-scripts"
```

---

### Task 5: Update `iterative-review/SKILL.md`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`

**Interfaces:**
- Consumes: current `lens-dispatch` node text.
- Produces: a dynamic `lens-dispatch` node that reads `## Applies to`.

- [x] **Step 5.1: Update `orchestrator-self-review` to read `## Applies to`**

Locate the `orchestrator-self-review` node. Replace the sentence that says it should only read `## Checklist` with one that also reads `## Applies to`:

```text
old_string: |
  This is the cheapest non-deterministic review. For each relevant `.agents/agents/reviewer-*.md` profile, read the `## Checklist` and apply it to the full diff mechanically.
new_string: |
  This is the cheapest non-deterministic review. For each relevant `.agents/agents/reviewer-*.md` profile, read the `## Checklist` and the `## Applies to` section, then apply the checklist to the full diff mechanically. Use `## Applies to` only to decide relevance; the prediction pass still scans the full diff for checklist patterns.
```

- [x] **Step 5.2: Replace the `lens-dispatch` node with dynamic selection**

Replace the entire `### `lens-dispatch`` subsection. Use `edit` with the following `old_string` (match from the start of the heading) and `new_string`:

```text
old_string: |
  ### `lens-dispatch`

  This node is mandatory. Dispatch the relevant lens reviewers in parallel, each with:
  - the full branch `<diff_path>`,
  - `<pr_description>`,
  - `<scan_findings>`,
  - `review-log-orchestrator-self-review.md`.

  Use `run_subagent` to dispatch each lens. Read the corresponding `.agents/agents/reviewer-*.md` profile and use its content as the subagent task. Set the off-repo workspace as the subagent's working directory. In this repo, the canonical lenses are:
  - `reviewer-skills` for `SKILL.md`, reference files, and prompt robustness.
  - `reviewer-marketplace` for generated surfaces, pack generation, and this-repo tooling.
  - `reviewer-security` for secrets and real identifiers.

  If you cannot run subagents (e.g. `run_subagent` is unavailable, fails, or is explicitly stopped), this is a `blocked` node — do not proceed to `ready` and do not claim the review is complete. Record the blocker and hand to a human.

  Lens reviewers should use the prediction log as the primary checklist and not re-flag what the orchestrator already fixed. Each lens writes `review-log-<lens>.md`.
new_string: |
  ### `lens-dispatch`

  This node is mandatory. Dispatch only the lens reviewers whose `## Applies to` rules match the PR, plus the mandatory `reviewer-strong` whole-branch pass.

  1. Discover every `.agents/agents/reviewer-*.md` file in the consumer repo. This set is the portable profiles shipped by the marketplace pack plus any repo-local `.agents/agents/reviewer-*.md` overrides.
  2. For each lens profile, read its `## Applies to` section. Match the rules in this order:
     - If an `inputs` entry is provided by the orchestrator (e.g. `<plan_path>` for `reviewer-plans`), dispatch the lens.
     - If a `globs` pattern matches a changed file in the diff, dispatch the lens.
     - If a `keywords` string appears in the diff or in `<pr_description>`, dispatch the lens.
  3. Build the input package for each matching lens: full branch `<diff_path>`, `<pr_description>`, `<scan_findings>`, `review-log-orchestrator-self-review.md`, and any lens-specific inputs (`<plan_path>`, `<spec_path>`, `<roadmap_path>` for `reviewer-plans`).
  4. Use `run_subagent` to dispatch each selected lens. Read the corresponding `.agents/agents/reviewer-*.md` profile and use its content as the subagent task. Set the off-repo workspace as the subagent's working directory.
  5. `reviewer-strong` always runs after the lens reviews with the full diff, PR description, and all `review-log-<lens>.md` files.

  If no lens matches the PR, still dispatch `reviewer-strong` for the whole-branch pass.

  If you cannot run subagents (e.g. `run_subagent` is unavailable, fails, or is explicitly stopped), this is a `blocked` node — do not proceed to `ready` and do not claim the review is complete. Record the blocker and hand to a human.

  Lens reviewers should use the prediction log as the primary checklist and not re-flag what the orchestrator already fixed. Each lens writes `review-log-<lens>.md`.
```

- [x] **Step 5.3: Commit the skill update**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md
git commit -m "Make iterative-review lens dispatch dynamic with Applies to rules"
```

- [x] **Step 5.4: Add `reviewer-fast` as the cheap fix-re-review gate**

Locate the `targeted-re-review` and `regression-scan` subsections in `iterative-review/SKILL.md` and the matching edges/nodes in `references/review-state-graph.md`. Change them so:
- `targeted-re-review` runs `reviewer-fast` on the fix diff before a whole-branch `reviewer-strong`.
- `regression-scan` begins with a widened `reviewer-fast` pass on the touched area, and only escalates to `reviewer-strong` on that area if `reviewer-fast` finds a new issue.
- Round counting does not treat the cheap `reviewer-fast` passes as rounds.

Commit the update.

---

### Task 6: Regenerate installed skills and the agent mesh

**Files:**
- Regenerate: `.agents/skills/selecting-a-subagent/SKILL.md`
- Regenerate: `.agents/skills/iterative-review/SKILL.md`
- Regenerate: `.agents/agents/reviewer-*.md` (from pack)
- Regenerate: `INDEX.md` files in `.agents/plans/`, `.agents/specs/`, etc.

**Interfaces:**
- Consumes: source edits under `codex-marketplace/plugins/`.
- Produces: installed `.agents/` copies and updated `INDEX.md` files.

- [x] **Step 6.1: Run marketplace regeneration**

Run: `py -3 tools/run.py marketplace --apply`
Expected: New `.agents/agents/reviewer-plans.md`, `reviewer-mesh.md`, and `reviewer-scripts.md` appear (or are confirmed up to date) and the `.agents/skills/selecting-a-subagent/SKILL.md` and `.agents/skills/iterative-review/SKILL.md` are updated to match the `codex-marketplace` source.

- [x] **Step 6.2: Run mesh regeneration**

Run: `py -3 tools/run.py mesh --apply`
Expected: `INDEX.md` files in `.agents/plans/`, `.agents/specs/`, and other mesh directories are updated to reflect the completed/ moves and any new plan/spec.

- [x] **Step 6.3: Inspect the diff**

Run: `git status --short` and `git diff --stat`
Expected: Source files, installed copies, pack assets, and generated `INDEX.md` are all staged or changed as expected. No `reviewer-known-findings.md` is created or referenced.

- [x] **Step 6.4: Commit the generated surfaces**

```bash
git add -A
git commit -m "Regenerate installed skills and mesh"
```

---

### Task 7: Validate and close the loop

**Files:**
- Validate: the entire working tree with `ci --check`.

**Interfaces:**
- Consumes: all committed changes.
- Produces: a green or red CI result.

- [x] **Step 7.1: Run the CI check**

Run: `py -3 tools/run.py ci --check`
Expected: Passes. If it fails, fix the cause, re-run the relevant `--apply` targets, and re-run `ci --check`.

- [x] **Step 7.2: Smoke-test lens selection**

Create an off-repo scratch diff that touches `.agents/specs/` but not `tools/` or `codex-marketplace/`. Run a local `iterative-review` dry-run that reads the updated `lens-dispatch` rules (or manually invoke the selection logic) and confirm:
- `reviewer-plans` is selected because the diff touches `.agents/specs/`.
- `reviewer-mesh` is selected if the diff touches `INDEX.md` or `repo-standards`.
- `reviewer-marketplace` is **not** selected for a docs-only PR.
- `reviewer-strong` is always selected.

- [x] **Step 7.3: Commit any fixes**

If the smoke test or CI exposed fixes, commit them as separate fix commits. Otherwise, no extra commit is needed.

---

### Task 8: Pin reviewer model tiers and add runtime staging tool

**Files:**
- Edit: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-*.md`
- Edit: `tools/sync_runtime_agents.py`
- Edit: `tools/run.py`
- Edit: `AGENTS.md`, `.agents/runbooks/implementing.md`, `docs/non-repo-locations-policy.md`
- Edit: `.agents/specs/2026-08-05-reviewer-lens-expansion-design.md` to ratify these additions.

**Interfaces:**
- Consumes: the custom reviewer profiles and the need to test new/updated subagent profiles from a linked worktree.
- Produces: explicit model values per profile and a manual `runtime-agents` staging task.

- [x] **Step 8.1: Replace `inherit` and pin reviewer models**

Run: edit the frontmatter `model:` of every `reviewer-*.md` pack-source profile.
Expected: `reviewer-fast` uses `swe-1-6`; `reviewer` uses `glm-5-2`; `reviewer-strong` uses `swe-1-7`; all lens profiles use `glm-5-2`.

- [x] **Step 8.2: Add `tools/sync_runtime_agents.py`**

Run: create the script with `--check` and `--apply` semantics, `--allow-shared-checkout` gating, exact `refs/heads/main` worktree selection, and a dirty-state preview from the target main checkout.
Expected: `py -3 tools/run.py runtime-agents --check` reports drift without writing; `--apply --allow-shared-checkout` copies profiles after confirmation.

- [x] **Step 8.3: Wire `runtime-agents` into `tools/run.py` and docs**

Run: add the `runtime-agents` target; update `AGENTS.md`, `.agents/runbooks/implementing.md`, and `docs/non-repo-locations-policy.md` to document the staging flow.
Expected: `py -3 tools/run.py ci --check` passes and the staging command is documented.

- [x] **Step 8.4: Update the design spec**

Run: add the `Reviewer model tier pinning` and `Runtime staging tool` contract sections to `.agents/specs/2026-08-05-reviewer-lens-expansion-design.md`.
Expected: The spec ratifies the model changes and the staging tool's behavior.

---

### Task 9: Add the shared `## Stop condition and loop breaker` to every reviewer profile

**Files:**
- Edit: all `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-*.md`
- Edit: `.agents/agents/reviewer-*.md` via `marketplace --apply`

**Interfaces:**
- Consumes: the stop-condition contract in the spec.
- Produces: every reviewer profile uses the same termination rules and single-line final response contract.

- [x] **Step 9.1: Apply the shared section to each profile**

Append the following to every `reviewer-*.md` profile (and include it in the Task 1.1 / 2.1 / 2.5.1 exact-content blocks for new profiles):

```markdown
## Stop condition and loop breaker

You are a reviewer, not a ledger. Do not count tool calls. Read the items that your checklist and the diff require, then stop.

- The final step is to use `write` to produce the off-repo report (`review-log-<lens>.md`) in the scratch workspace.
- After the report is written, your final response must be exactly one line: `<profile>: N issue(s)` or `<profile>: clean`. Do not output the report body or any other text.
- If you are about to make the same `read`, `grep`, or `find_file_by_name` call again without a new question it can answer, write the report immediately.
- If the last two tool calls produced no new findings, write the report immediately.
- As a hard backstop, do not exceed 50 total tool calls after loading the inputs.

A partial, cited report is better than an infinite loop. Do not announce that you are writing the report — just write it.
```

Run: `py -3 tools/run.py marketplace --apply`
Expected: installed `.agents/agents/reviewer-*.md` copies match the pack source and include the stop-condition section.

---

### Task 10: Add `selecting-a-subagent/scripts/install_profiles.py`

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/scripts/install_profiles.py`
- Edit: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/SKILL.md`

**Interfaces:**
- Consumes: the profile `.md` assets now in `selecting-a-subagent/assets/`.
- Produces: a consumer helper that installs the shipped profiles into the repo's `.agents/agents/` directory without touching locally managed profiles.

- [x] **Step 10.1: Create `install_profiles.py`**

Run: implement `--source` and `--target` with a default target of `.agents/agents/`, a read-only drift preview by default, and `--apply` to overwrite changed shipped profiles. Leave any files in the target that are not in the source untouched.
Expected: `py -3 .agents/skills/selecting-a-subagent/scripts/install_profiles.py --help` and `--check` respond (0), and `--apply` lands files in `.agents/agents/`.

- [x] **Step 10.2: Update `selecting-a-subagent/SKILL.md` installation instructions**

Run: replace the manual-copy-only instructions with the helper command and keep the global Devin Desktop path as an alternative.
Expected: `py -3 tools/run.py ci --check` passes.

- [x] **Step 10.3: Normalize `implementer.md` and `implementer-strong.md` as part of the consolidation**

Run: move the duplicated `codex-marketplace/plugins/repo-worker-pack/assets/profiles/implementer*.md` files into the canonical `selecting-a-subagent/assets/` directory and restore their vendor baseline content. The marketplace helper and `installed-skills` will keep the repo-local `.agents/agents/` copies in sync.
Expected: `py -3 tools/run.py ci --check` passes and the diff shows only the expected implementer content changes.

---

### Task 11: Publish the branch as a draft PR

**Files:**
- Publish: branch `feat/reviewer-lens-expansion`.

**Interfaces:**
- Consumes: green `ci --check`.
- Produces: open draft PR URL.

- [x] **Step 11.1: Push the branch**

```bash
git push -u origin feat/reviewer-lens-expansion
```

- [x] **Step 11.2: Open a draft PR**

Use `gh pr create --draft` with title `feat: reviewer lens expansion (plans, mesh, dynamic dispatch)` and a body that lists the spec, plan, and completed plan/spec moves.

- [x] **Step 11.3: Record publication proof**

Capture the PR URL and the head SHA. Return them as the publication proof for this work.

- [ ] **Step 11.4: Archive the completed plan and spec before marking ready**

After `iterative-review` is green and `py -3 tools/run.py ci --check` passes, archive the completed planning artifacts per `.agents/runbooks/completing-plans.md`:

```bash
git mv .agents/plans/2026-08-05-reviewer-lens-expansion.md .agents/plans/completed/
git mv .agents/specs/2026-08-05-reviewer-lens-expansion-design.md .agents/specs/completed/
py -3 tools/heal_archive_links.py --apply

---

### Task 12: Enforce UTF-8 for iterative-review artifacts

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/normalize_review_inputs.py`
- Edit: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`
- Edit: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-graph.md`
- Edit: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-*.md`

**Interfaces:**
- Consumes: the off-repo review workspace; any lens report or preflight output.
- Produces: plain UTF-8 (no BOM) files that downstream subagents can `read` and `grep` reliably.

- [x] **Step 12.1: Create `normalize_review_inputs.py`**

Run: implement a helper that detects UTF-16LE/BE and UTF-8-with-BOM and rewrites files in place as plain UTF-8. Add `--help`, `--check`, and `--apply`; classify the script as `mixed`.
Expected: `py -3 .agents/skills/iterative-review/scripts/normalize_review_inputs.py --help` and `--check` respond, and `--apply` converts a test UTF-16 file.

- [x] **Step 12.2: Add `normalize-inputs` nodes to the review graph and skill**

Run: update `review-state-graph.md` to include `normalize-inputs` between `setup` and `preflight` and between `lens-dispatch` and `strong-review`. Update `iterative-review/SKILL.md` to document the `py -3 .agents/skills/iterative-review/scripts/normalize_review_inputs.py --apply <scratch_dir>` invocations.
Expected: `py -3 tools/run.py ci --check` passes.

- [x] **Step 12.3: Add UTF-8 report contract to the canonical reviewer profiles**

Run: add a contract to each `reviewer-*.md` `## Stop condition and loop breaker` section: write the off-repo log as plain UTF-8 (no BOM) using the `write` tool; do not use `Tee-Object`, `Out-File` without `-Encoding utf8`, or shell redirects that can emit UTF-16. Regenerate the marketplace and install the updated profiles into `.agents/agents/`.
Expected: `py -3 .agents/skills/selecting-a-subagent/scripts/install_profiles.py --apply` lands the profiles and `py -3 tools/run.py ci --check` passes.
py -3 tools/run.py mesh --apply
py -3 tools/run.py marketplace --apply
py -3 tools/run.py ci --check
```

Then commit the archive and only then flip the PR from draft to ready.

---

## Plan-readiness self-review

1. **Spec coverage:** Each spec requirement has a task that implements it.
2. **Placeholder scan:** No TBD, TODO, or "implement later".
3. **Type consistency:** Each profile uses the same `review-log-<lens>.md` naming and `file:line` severity format.
4. **Validation:** `py -3 tools/run.py ci --check` and a smoke test are included.

**Plan-readiness rating:** 10/10. Tasks 0.1-10.3 are checked. Task 0.2 confirmed `repo-worker-pack` as the active pack source and the `.provenance.json` diff records the new profiles. Step 10.4 (archive before flipping to ready) is intentionally deferred until `iterative-review` is green and `ci --check` passes.
