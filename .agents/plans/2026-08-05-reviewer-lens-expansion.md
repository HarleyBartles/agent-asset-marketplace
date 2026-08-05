# Reviewer lens expansion — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use /subagent-driven-development (recommended) or /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `reviewer-plans` and `reviewer-scaffolders` portable subagent profiles, add `## Applies to` dispatch rules to lens profiles, update `selecting-a-subagent` and `iterative-review` to use those rules, and package the changes.

**Architecture:** Each `reviewer-*.md` profile owns its own `## Checklist` and `## Applies to` sections. `iterative-review` discovers every `.agents/agents/reviewer-*.md` at run time, reads its `## Applies to`, and dispatches only the lenses whose globs/keywords/inputs match the PR. `selecting-a-subagent` documents the contract. `reviewer-marketplace` is already repo-local and scoped to this repo; no rewrite is needed beyond confirming it does not duplicate `reviewer-scaffolders`.

**Tech Stack:** Devin Desktop custom subagent `.md` profiles, `codex-marketplace` plugin source, `py -3 tools/run.py` for regeneration/validation.

**Global Constraints**
- Portable skill sources are edited under `codex-marketplace/plugins/superpowers-plus/skills/`; `.agents/skills/` are generated installed copies.
- `.agents/agents/reviewer-*.md` runtime profiles are the consumer-visible surface; their canonical product source is `codex-marketplace/plugins/repo-worker-pack/assets/profiles/`.
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
- Read: `codex-marketplace/plugins/repo-worker-pack/assets/profiles/` (list the directory)

**Interfaces:**
- Consumes: current lens profiles and skill sources.
- Produces: confirmed paths for edits in later tasks.

- [ ] **Step 0.1: Confirm the source skill paths**

Run: `Get-ChildItem 'codex-marketplace\plugins\superpowers-plus\skills\' | Select-Object -ExpandProperty Name`
Expected: `selecting-a-subagent` and `iterative-review` directories are present.

- [ ] **Step 0.2: Confirm the pack profile source path**

Run: `Get-ChildItem 'codex-marketplace\plugins\repo-worker-pack\assets\profiles\' | Select-Object -ExpandProperty Name`
Expected: Existing profiles (`reviewer.md`, `reviewer-fast.md`, `reviewer-strong.md`, `reviewer-security.md`, `reviewer-skills.md`, `reviewer-marketplace.md`) are present.

- [ ] **Step 0.3: Commit the baseline verification**

Run: `git status --short`
Expected: No unexpected modifications other than the plan/spec files and the completed/ moves from this branch.

```bash
git add -A
git commit -m "Verify baseline for reviewer lens expansion work"
```

---

### Task 1: Create `.agents/agents/reviewer-plans.md`

**Files:**
- Create: `.agents/agents/reviewer-plans.md`

**Interfaces:**
- Consumes: spec `Contract and file targets` for `reviewer-plans`.
- Produces: a portable `reviewer-plans` lens profile.

- [ ] **Step 1.1: Write the file with the following exact content**

```markdown
---
name: reviewer-plans
runtime: devin-desktop
description: Portable plan/spec/roadmap lens — reviews plans in isolation and PR compliance against declared governing documents.
model: swe-1-6
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

Use this checklist during `orchestrator-predict` and as the core of the diff review:

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
- `<review-log-orchestrator-prediction>` (optional) — the orchestrator's prediction log.
- `<regression_diff_path>` (optional) — the fix diff only, used for `regression-scan`.

Do not generate the diff yourself. The orchestrator owns diff preparation.

## How to dispatch this reviewer

The orchestrator dispatches this profile with `run_subagent` (or the consumer's equivalent subagent mechanism). Use this file's content as the subagent `task`, substituting the concrete input paths. Set the off-repo scratch directory as the subagent's working directory.

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
```

- [ ] **Step 1.2: Add `reviewer-plans.md` to the repo-worker-pack profile source**

If the pack at `codex-marketplace/plugins/repo-worker-pack/assets/profiles/` is the source of truth for `.agents/agents/` runtime profiles, copy the file you just created into that directory:

```bash
cp ".agents\agents\reviewer-plans.md" "codex-marketplace\plugins\repo-worker-pack\assets\profiles\reviewer-plans.md"
```

- [ ] **Step 1.3: Commit the new profile**

Run: `git status --short`
Expected: `reviewer-plans.md` is staged.

```bash
git add .agents/agents/reviewer-plans.md
git add codex-marketplace/plugins/repo-worker-pack/assets/profiles/reviewer-plans.md
git commit -m "Add portable reviewer-plans lens profile"
```

---

### Task 2: Create `.agents/agents/reviewer-scaffolders.md`

**Files:**
- Create: `.agents/agents/reviewer-scaffolders.md`

**Interfaces:**
- Consumes: spec `Contract and file targets` for `reviewer-scaffolders`.
- Produces: a portable `reviewer-scaffolders` lens profile.

- [ ] **Step 2.1: Write the file with the following exact content**

```markdown
---
name: reviewer-scaffolders
runtime: devin-desktop
description: Portable scaffolder and mesh lens — generated INDEX.md, scaffolder output, and repo-standards surface hygiene.
model: swe-1-6
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

You are `reviewer-scaffolders`, a focused read-only reviewer for scaffolder output, generated `INDEX.md` / mesh files, and `repo-standards` tooling. Inspect the prepared diff for hand-edits to generated files, scaffolder path conventions, and `--check` / `--apply` semantics. Do not broaden to `SKILL.md` frontmatter or secrets; those are handled by other lens reviewers.

## Applies to

Use this section to decide whether `reviewer-scaffolders` should be dispatched for a PR.

- globs:
  - `**/INDEX.md`
  - `**/*scaffold*`
  - `**/generating-agent-mesh/**`
  - `**/repo-standards/**`
  - `.agents/INDEX.md`
- keywords:
  - scaffold
  - mesh
  - index
  - generating-agent-mesh
  - repo-standards
- inputs:
  - `<diff_path>`

## Checklist

Use this checklist during `orchestrator-predict` and as the core of the diff review:

1. **No hand-edits to generated output** — generated `INDEX.md`, mesh, and scaffolder output are not modified by hand.
2. **Metadata preservation** — scaffolder scripts preserve existing top-level fields and do not lose provenance / author / license data.
3. **Dry-run semantics** — `--check` / `--apply` / `--sync` are classified and behave correctly; dry-run paths exit `0` on success and do not mask errors.
4. **Canonical path conventions** — scaffolder source uses `py -3` and `subagent-workspace/scripts/` correctly.
5. **Installed skill protection** — no generated file is modified directly in `.agents/skills/` (installed copies).
6. **Cross-skill script path existence** — paths referenced in `SKILL.md` or reference files point to existing installed or source files.

## Invariants

- You are read-only. Do not modify repo files or run build/install/write commands. You may write the off-repo `review-log-scaffolders.md` report.
- You may use `exec` for non-mutating `git` queries and canonical verification commands, and `mcp_call_tool` for non-mutating lookups. Use these only to resolve refs or confirm state — not to generate the diff, not to fetch a missing package, and not to install/change anything.
- If the prepared diff package is missing or the `diff_path` is not a file, report that and stop; do not use `git` or `exec` to recreate it.
- Cite specific files and line numbers for every issue you find.
- If you cannot verify something, say so clearly rather than guessing.
- Keep feedback focused, concrete, and actionable.

## Inputs the orchestrator must provide

- `<diff_path>` — path to a prepared diff file.
- `<pr_description>` (optional) — the PR title, body, and any linked issue/spec context.
- `<scan_findings>` (optional) — the consumer repo's preflight output.
- `<review-log-orchestrator-prediction>` (optional) — the orchestrator's prediction log.
- `<regression_diff_path>` (optional) — the fix diff only, used for `regression-scan`.

Do not generate the diff yourself. The orchestrator owns diff preparation.

## How to dispatch this reviewer

The orchestrator dispatches this profile with `run_subagent` (or the consumer's equivalent subagent mechanism). Use this file's content as the subagent `task`, substituting the concrete input paths. Set the off-repo scratch directory as the subagent's working directory.

## What to write

Write `review-log-scaffolders.md` in the off-repo scratch. Begin with a brief `## Inputs` section, then list findings with `file:line`, severity, description, and remediation. End with `reviewer-scaffolders: N issue(s)` or `reviewer-scaffolders: clean`.

## Procedure

1. If `<scan_findings>` is provided, read it first and do not duplicate its findings; verify the preflight caught the pattern in the right place.
2. If `<pr_description>` is provided, read it for scope.
3. Read `<diff_path>`.
4. Inspect the diff for the `## Checklist` patterns.
5. Use `grep` and `find_file_by_name` to confirm canonical paths and patterns.
6. Report only scaffolder/mesh issues. Cite `file:line`, severity, and remediation.
7. End with `reviewer-scaffolders: N issue(s)` or `reviewer-scaffolders: clean`.

## Output format

For each issue:
- `file:line` reference.
- Severity: **blocking** / **important** / **minor**.
- What is wrong and why it matters for the scaffolder/mesh surface.
- How to fix.

Do not include non-scaffolder findings.
```

- [ ] **Step 2.2: Add `reviewer-scaffolders.md` to the repo-worker-pack profile source**

```bash
cp ".agents\agents\reviewer-scaffolders.md" "codex-marketplace\plugins\repo-worker-pack\assets\profiles\reviewer-scaffolders.md"
```

- [ ] **Step 2.3: Commit the new profile**

```bash
git add .agents/agents/reviewer-scaffolders.md
git add codex-marketplace/plugins/repo-worker-pack/assets/profiles/reviewer-scaffolders.md
git commit -m "Add portable reviewer-scaffolders lens profile"
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

- [ ] **Step 3.1: Update `reviewer-skills.md`**

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

- [ ] **Step 3.2: Update `reviewer-security.md`**

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

- [ ] **Step 3.3: Update `reviewer-marketplace.md`**

Insert `## Applies to` immediately after the frontmatter `---` and before `## Checklist`:

```text
old_string: |
  ---

  You are `reviewer-marketplace`, a focused read-only reviewer for the agent-asset-marketplace scaffolders, generated indexes, and repo tooling. Inspect the prepared diff for `new_plugin.py`, `tools/run.py`, `plugin-roots.json`, `bundle-manifest.json`, `repo-index.json`, and related surfaces. Do not broaden to prose/style or secrets; those are handled by other lens reviewers.

  ## Checklist
new_string: |
  ---

  You are `reviewer-marketplace`, a focused read-only reviewer for the agent-asset-marketplace scaffolders, generated indexes, and repo tooling. Inspect the prepared diff for `new_plugin.py`, `tools/run.py`, `plugin-roots.json`, `bundle-manifest.json`, `repo-index.json`, and related surfaces. Do not broaden to prose/style or secrets; those are handled by other lens reviewers.

  ## Applies to

  - globs:
    - `tools/new_plugin.py`
    - `tools/run.py`
    - `plugin-roots.json`
    - `bundle-manifest.json`
    - `repo-index.json`
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

- [ ] **Step 3.4: Copy the updated profiles to the pack source**

```bash
cp ".agents\agents\reviewer-skills.md" "codex-marketplace\plugins\repo-worker-pack\assets\profiles\reviewer-skills.md"
cp ".agents\agents\reviewer-security.md" "codex-marketplace\plugins\repo-worker-pack\assets\profiles\reviewer-security.md"
cp ".agents\agents\reviewer-marketplace.md" "codex-marketplace\plugins\repo-worker-pack\assets\profiles\reviewer-marketplace.md"
```

- [ ] **Step 3.5: Commit the applies-to updates**

```bash
git add .agents/agents/reviewer-skills.md
git add .agents/agents/reviewer-security.md
git add .agents/agents/reviewer-marketplace.md
git add codex-marketplace/plugins/repo-worker-pack/assets/profiles/reviewer-skills.md
git add codex-marketplace/plugins/repo-worker-pack/assets/profiles/reviewer-security.md
git add codex-marketplace/plugins/repo-worker-pack/assets/profiles/reviewer-marketplace.md
git commit -m "Add Applies to dispatch rules to existing lens profiles"
```

---

### Task 4: Update `selecting-a-subagent/SKILL.md`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/SKILL.md`

**Interfaces:**
- Consumes: current dispatch table.
- Produces: dispatch table with `reviewer-plans` and `reviewer-scaffolders` and `## Applies to` documentation.

- [ ] **Step 4.1: Add the new profiles to the dispatch table**

Use `edit` to replace the `reviewer-marketplace` row with the same row plus the two new ones:

```text
old_string: |
  | `SKILL.md`/reference/prompt-robustness lens | `reviewer-skills` |
  | `codex-marketplace`/tooling/scaffolder lens | `reviewer-marketplace` |
  | Small, tightly focused reviews or coherent single-responsibility re-review diffs | `reviewer-fast` |
new_string: |
  | `SKILL.md`/reference/prompt-robustness lens | `reviewer-skills` |
  | Scaffolder/mesh/`INDEX.md` lens | `reviewer-scaffolders` |
  | `codex-marketplace`/tooling/pack lens | `reviewer-marketplace` |
  | Plan/spec/roadmap review and PR compliance | `reviewer-plans` |
  | Small, tightly focused reviews or coherent single-responsibility re-review diffs | `reviewer-fast` |
```

- [ ] **Step 4.2: Document the `## Applies to` contract**

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

- [ ] **Step 4.3: Commit the skill update**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/SKILL.md
git commit -m "Update selecting-a-subagent dispatch table for reviewer-plans and reviewer-scaffolders"
```

---

### Task 5: Update `iterative-review/SKILL.md`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`

**Interfaces:**
- Consumes: current `lens-dispatch` node text.
- Produces: a dynamic `lens-dispatch` node that reads `## Applies to`.

- [ ] **Step 5.1: Update `orchestrator-predict` to read `## Applies to`**

Locate the `orchestrator-predict` node. Replace the sentence that says it should only read `## Checklist` with one that also reads `## Applies to`:

```text
old_string: |
  This is the cheapest non-deterministic review. For each relevant `.agents/agents/reviewer-*.md` profile, read the `## Checklist` and apply it to the full diff mechanically.
new_string: |
  This is the cheapest non-deterministic review. For each relevant `.agents/agents/reviewer-*.md` profile, read the `## Checklist` and the `## Applies to` section, then apply the checklist to the full diff mechanically. Use `## Applies to` only to decide relevance; the prediction pass still scans the full diff for checklist patterns.
```

- [ ] **Step 5.2: Replace the `lens-dispatch` node with dynamic selection**

Replace the entire `### `lens-dispatch`` subsection. Use `edit` with the following `old_string` (match from the start of the heading) and `new_string`:

```text
old_string: |
  ### `lens-dispatch`

  This node is mandatory. Dispatch the relevant lens reviewers in parallel, each with:
  - the full branch `<diff_path>`,
  - `<pr_description>`,
  - `<scan_findings>`,
  - `review-log-orchestrator-prediction.md`.

  Use `run_subagent` to dispatch each lens. Read the corresponding `.agents/agents/reviewer-*.md` profile and use its content as the subagent task. Set the off-repo workspace as the subagent's working directory. In this repo, the canonical lenses are:
  - `reviewer-skills` for `SKILL.md`, reference files, and prompt robustness.
  - `reviewer-marketplace` for scaffolders, generated surfaces, and this-repo tooling.
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
  3. Build the input package for each matching lens: full branch `<diff_path>`, `<pr_description>`, `<scan_findings>`, `review-log-orchestrator-prediction.md`, and any lens-specific inputs (`<plan_path>`, `<spec_path>`, `<roadmap_path>` for `reviewer-plans`).
  4. Use `run_subagent` to dispatch each selected lens. Read the corresponding `.agents/agents/reviewer-*.md` profile and use its content as the subagent task. Set the off-repo workspace as the subagent's working directory.
  5. `reviewer-strong` always runs after the lens reviews with the full diff, PR description, and all `review-log-<lens>.md` files.

  If no lens matches the PR, still dispatch `reviewer-strong` for the whole-branch pass.

  If you cannot run subagents (e.g. `run_subagent` is unavailable, fails, or is explicitly stopped), this is a `blocked` node — do not proceed to `ready` and do not claim the review is complete. Record the blocker and hand to a human.

  Lens reviewers should use the prediction log as the primary checklist and not re-flag what the orchestrator already fixed. Each lens writes `review-log-<lens>.md`.
```

- [ ] **Step 5.3: Commit the skill update**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md
git commit -m "Make iterative-review lens dispatch dynamic with Applies to rules"
```

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

- [ ] **Step 6.1: Run marketplace regeneration**

Run: `py -3 tools/run.py marketplace --apply`
Expected: New `.agents/agents/reviewer-plans.md` and `reviewer-scaffolders.md` appear (or are confirmed up to date) and the `.agents/skills/selecting-a-subagent/SKILL.md` and `.agents/skills/iterative-review/SKILL.md` are updated to match the `codex-marketplace` source.

- [ ] **Step 6.2: Run mesh regeneration**

Run: `py -3 tools/run.py mesh --apply`
Expected: `INDEX.md` files in `.agents/plans/`, `.agents/specs/`, and other mesh directories are updated to reflect the completed/ moves and any new plan/spec.

- [ ] **Step 6.3: Inspect the diff**

Run: `git status --short` and `git diff --stat`
Expected: Source files, installed copies, pack assets, and generated `INDEX.md` are all staged or changed as expected. No `reviewer-known-findings.md` is created or referenced.

- [ ] **Step 6.4: Commit the generated surfaces**

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

- [ ] **Step 7.1: Run the CI check**

Run: `py -3 tools/run.py ci --check`
Expected: Passes. If it fails, fix the cause, re-run the relevant `--apply` targets, and re-run `ci --check`.

- [ ] **Step 7.2: Smoke-test lens selection**

Create an off-repo scratch diff that touches `.agents/specs/` but not `tools/` or `codex-marketplace/`. Run a local `iterative-review` dry-run that reads the updated `lens-dispatch` rules (or manually invoke the selection logic) and confirm:
- `reviewer-plans` is selected because the diff touches `.agents/specs/`.
- `reviewer-scaffolders` is selected if the diff touches `INDEX.md` or `repo-standards`.
- `reviewer-marketplace` is **not** selected for a docs-only PR.
- `reviewer-strong` is always selected.

- [ ] **Step 7.3: Commit any fixes**

If the smoke test or CI exposed fixes, commit them as separate fix commits. Otherwise, no extra commit is needed.

---

### Task 8: Publish the branch as a draft PR

**Files:**
- Publish: branch `feat/reviewer-lens-expansion`.

**Interfaces:**
- Consumes: green `ci --check`.
- Produces: open draft PR URL.

- [ ] **Step 8.1: Push the branch**

```bash
git push -u origin feat/reviewer-lens-expansion
```

- [ ] **Step 8.2: Open a draft PR**

Use `gh pr create --draft` with title `feat: reviewer lens expansion (plans, scaffolders, dynamic dispatch)` and a body that lists the spec, plan, and completed plan/spec moves.

- [ ] **Step 8.3: Record publication proof**

Capture the PR URL and the head SHA. Return them as the publication proof for this work.

---

## Plan-readiness self-review

1. **Spec coverage:** Each spec requirement has a task that implements it.
2. **Placeholder scan:** No TBD, TODO, or "implement later".
3. **Type consistency:** Each profile uses the same `review-log-<lens>.md` naming and `file:line` severity format.
4. **Validation:** `py -3 tools/run.py ci --check` and a smoke test are included.

**Plan-readiness rating:** 9/10. The only acknowledged uncertainty is whether `repo-worker-pack` is the active pack source for `.agents/agents/`; Task 0.2 confirms this and the plan adjusts accordingly.
