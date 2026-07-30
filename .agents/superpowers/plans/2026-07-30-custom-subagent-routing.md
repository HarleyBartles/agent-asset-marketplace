# Custom Subagent Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the `agent-asset-marketplace` repo to support Devin Desktop custom subagent profiles, vend a `review-branch-diff` repo-worker-pack skill, and adapt the `subagent-driven-development` overlay to dispatch `implementer`, `reviewer`, and `branch-reviewer`.

**Architecture:** Add `review-branch-diff` as a first-party skill in `sources/first_party/skills/`, register it in `codex-marketplace/custody-pack-registry.json`, and let `tools/run marketplace --apply` project it. Update the `subagent-model-routing` reference doc and the `subagent-driven-development` adapter overlay. All changes are validated with `tools/run ci --check`.

**Tech Stack:** Markdown, YAML, JSON, Python (tooling), `tools/run`.

## Global Constraints

- Do not edit `sources/third_party/**` directly. All third-party changes go through `adapters/codex/superpowers-plus/subagent-driven-development/overlay.yaml`.
- Do not hand-edit generated projection surfaces (`codex-marketplace/plugins/**`, `.agents/skills/**`, `references/bundle-manifest.json`, etc.). Regenerate with `tools/run`.
- Preserve `byte_identical` for first-party skills.
- LF line endings on written text files.
- Work on the `spec/custom-subagent-routing` branch and open a PR to `main`.
- Global subagent profiles stay in `~/.config/devin/agents/`; the repo only ships the `review-branch-diff` skill and a static fallback `branch-reviewer` asset.

---

### Task 1: Create `review-branch-diff` first-party skill source

**Files:**
- Create: `sources/first_party/skills/review-branch-diff/SKILL.md`
- Create: `sources/first_party/skills/review-branch-diff/agents/openai.yaml`
- Create: `sources/first_party/skills/review-branch-diff/assets/branch-reviewer/AGENT.md`

**Interfaces:**
- Consumes: spec `2026-07-30-custom-subagent-routing-design.md` and the global `~/.config/devin/agents/branch-reviewer/AGENT.md` as the fallback asset reference.
- Produces: source tree for the `review-branch-diff` marketplace skill.

- [ ] **Step 1: Create the skill directory**

Run:
```powershell
New-Item -ItemType Directory -Path "Z:\agent-asset-marketplace\sources\first_party\skills\review-branch-diff\agents" -Force
New-Item -ItemType Directory -Path "Z:\agent-asset-marketplace\sources\first_party\skills\review-branch-diff\assets\branch-reviewer" -Force
```

- [ ] **Step 2: Write `sources/first_party/skills/review-branch-diff/SKILL.md`**

```markdown
---
name: review-branch-diff
description: Review the current branch diff against main for correctness, style, consistency, and risk. Use when a branch is complete and a whole-branch diff review is needed before merge.
license: MIT
metadata:
  source-id: review-branch-diff
  source-path: sources/first_party/skills/review-branch-diff
  provenance-name: Review Branch Diff first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  use_when:
    - Use when a feature branch is complete and a whole-branch diff review is needed.
    - Use when the user asks to review the current branch diff against main.
  do_not_use_when:
    - Do not use when the current branch has no commits ahead of main.
    - Do not use when only a single file or small diff needs review; use a file-level reviewer instead.
  related_skills: [subagent-driven-development, finishing-a-development-branch, requesting-code-review]
agent: branch-reviewer
triggers:
  - user
  - model
---

# Review Branch Diff

Review the current branch diff against `main` (or `origin/main`) for correctness, style, consistency, and risk.

1. Determine the base ref. Run `git rev-parse --verify main` and, if that fails, `git rev-parse --verify origin/main`. Use the first one that succeeds as `<base>`.
2. Run `git diff --no-color <base>...HEAD` to obtain the full diff.
3. If the diff is too large to review at once, run `git diff --stat <base>...HEAD`, then review changed files in batches using `git diff --no-color <base>...HEAD -- <path>`.
4. Identify correctness, style, consistency, and risk issues. Cite specific files and line numbers.
5. Do not modify files and do not run commands other than the git commands above.

**Fallback:** If the global `branch-reviewer` subagent profile is not available, an agent can install `assets/branch-reviewer/AGENT.md` from this skill as `~/.config/devin/agents/branch-reviewer/AGENT.md` before invoking this skill.
```

- [ ] **Step 3: Write `sources/first_party/skills/review-branch-diff/agents/openai.yaml`**

```yaml
version: 1
metadata:
  skill_name: review-branch-diff
  source_category: first_party
interface:
  display_name: Review Branch Diff
  short_description: Use when a branch is complete and a whole-branch diff review against main is needed.
  default_prompt: Use review-branch-diff when a branch is complete and you need a whole-branch diff review against main.
policy:
  allow_implicit_invocation: false
```

- [ ] **Step 4: Write `sources/first_party/skills/review-branch-diff/assets/branch-reviewer/AGENT.md`**

```markdown
---
name: branch-reviewer
description: Branch diff reviewer — reads the current branch diff against main, reviews it for correctness, style, consistency, and risk, and cites specific files and line numbers.
model: swe-1-7
allowed-tools:
  - read
  - grep
  - find_file_by_name
  - exec
---

You are a branch diff reviewer. Your job is to review the current branch's diff against `main` (or `origin/main`) for correctness, style, consistency, and risk.

Rules:
- Use `exec` only for git commands needed to produce or navigate the diff: `git diff`, `git rev-parse`, `git log`, `git show`, `git status`, `git branch`.
- Do not modify files. Do not run build, install, test, or write commands.
- Cite specific files and line numbers for every issue you find.
- Keep feedback focused, concrete, and actionable.
- If the diff is large, start with `git diff --stat` and review files in batches.
```

- [ ] **Step 5: Verify the skill directory shape**

Run:
```powershell
Set-Location "Z:\agent-asset-marketplace"; Get-ChildItem -Recurse sources\first_party\skills\review-branch-diff
```

Expected output: `SKILL.md`, `agents/openai.yaml`, and `assets/branch-reviewer/AGENT.md` are present.

- [ ] **Step 6: Commit the new skill source**

```bash
git add sources/first_party/skills/review-branch-diff
git commit --no-verify -m "feat: add review-branch-diff first-party skill source"
```

---

### Task 2: Register `review-branch-diff` in `repo-worker-pack`

**Files:**
- Modify: `codex-marketplace/custody-pack-registry.json`

**Interfaces:**
- Consumes: the new `sources/first_party/skills/review-branch-diff` tree from Task 1.
- Produces: updated registry that the marketplace generator uses to project `review-branch-diff` into `repo-worker-pack`.

- [ ] **Step 1: Add `sources/first_party/skills/review-branch-diff` to the `repo-worker-pack` `source_ledger`**

In `codex-marketplace/custody-pack-registry.json`, find the `repo-worker-pack` bundle's `source_ledger` array and append:

```json
        "sources/first_party/skills/review-branch-diff",
```

- [ ] **Step 2: Add an `entries` object for `review-branch-diff` in the `repo-worker-pack` `entries` array**

Append the following JSON object to the `entries` array of the `repo-worker-pack` bundle:

```json
        {
          "canonical_name": "review-branch-diff",
          "source_category": "first_party",
          "content_mode": "verbatim",
          "source_family": "first_party",
          "canonical_source_path": "sources/first_party/skills/review-branch-diff",
          "local_path": "skills/review-branch-diff",
          "provenance_note": "First-party branch-diff review skill projected verbatim into the repo-worker-pack.",
          "copy_expectation": "byte_identical"
        }
```

- [ ] **Step 3: Commit the registry change**

```bash
git add codex-marketplace/custody-pack-registry.json
git commit --no-verify -m "chore: register review-branch-diff in repo-worker-pack"
```

---

### Task 3: Update `subagent-model-routing` Devin Desktop reference

**Files:**
- Modify: `sources/first_party/skills/subagent-model-routing/references/devin-desktop-profile.md`

**Interfaces:**
- Consumes: the existing reference doc and the spike findings in the spec.
- Produces: updated reference doc that documents custom subagent profiles, `model:` inheritance, and the `write` limitation.

- [ ] **Step 1: Insert the custom-profiles section before `### What not to do`**

In `sources/first_party/skills/subagent-model-routing/references/devin-desktop-profile.md`, locate the `### What not to do` heading and insert the following block immediately before it:

```markdown
### Custom subagent profiles

Devin Desktop supports custom subagent profiles under `~/.config/devin/agents/` (or `%APPDATA%\devin\agents\` on Windows). Each profile is a directory containing an `AGENT.md` file: `reviewer/`, `implementer/`, `branch-reviewer/`, etc. A skill can dispatch to a custom profile using the `agent:` frontmatter field.

| Task | Dispatch |
|---|---|
| Review / architecture challenge | `run_subagent profile: reviewer` |
| Bounded implementation / bugfix | `run_subagent profile: implementer` |
| Branch diff review | `run_subagent profile: branch-reviewer` or invoke `/review-branch-diff` |
| Broad read-only exploration | `subagent_explore` |
| Broad mixed work | `subagent_general` |

Custom profiles may declare `model:` in their `AGENT.md`. The runtime honors that model when the subagent is launched. Do not pass a `model:` argument to `run_subagent`; the tool has no such parameter.

Custom subagents are not granted the `write` tool, even if listed in their `allowed-tools`. To create new files from a custom subagent, use `exec` with a shell redirect or another allowed mechanism.
```

- [ ] **Step 2: Commit the reference doc update**

```bash
git add sources/first_party/skills/subagent-model-routing/references/devin-desktop-profile.md
git commit --no-verify -m "docs: document Devin Desktop custom subagent profiles in subagent-model-routing"
```

---

### Task 4: Update `subagent-driven-development` overlay for Devin Desktop

**Files:**
- Modify: `adapters/codex/superpowers-plus/subagent-driven-development/overlay.yaml`

**Interfaces:**
- Consumes: the upstream `sources/third_party/superpowers/obra-superpowers/v6.2.0/skills/subagent-driven-development/*` files and the custom profile names.
- Produces: overlay edits that turn the generic subagent templates into Devin Desktop `run_subagent profile:` calls and a `/review-branch-diff` final review.

- [ ] **Step 1: Add an edit to `implementer-prompt.md`**

Add the following `edits` entry to the `adapters/codex/superpowers-plus/subagent-driven-development/overlay.yaml` `edits` list:

```yaml
- path: implementer-prompt.md
  op: replace
  start_line: 5
  end_line: 9
  expected_lines:
  - 'Subagent (general-purpose):'
  - '  description: "Implement Task N: [task name]"'
  - '  model: [MODEL — REQUIRED: choose per SKILL.md Model Selection; an omitted'
  - '         model silently inherits the session''s most expensive one]'
  - '  prompt: |'
  replace_lines:
  - 'run_subagent (Devin Desktop):'
  - '  profile: implementer'
  - '  title: "Implement Task N: [task name]"'
  - '  task: |'
```

- [ ] **Step 2: Add an edit to `task-reviewer-prompt.md`**

Add the following `edits` entry:

```yaml
- path: task-reviewer-prompt.md
  op: replace
  start_line: 10
  end_line: 14
  expected_lines:
  - 'Subagent (general-purpose):'
  - '  description: "Review Task N (spec + quality)"'
  - '  model: [MODEL — REQUIRED: choose per SKILL.md Model Selection; an omitted'
  - '         model silently inherits the session''s most expensive one]'
  - '  prompt: |'
  replace_lines:
  - 'run_subagent (Devin Desktop):'
  - '  profile: reviewer'
  - '  title: "Review Task N (spec + quality)"'
  - '  task: |'
```

- [ ] **Step 3: Add edits to `SKILL.md` to use `/review-branch-diff` for the final review**

Add these three `edits` entries to the `overlay.yaml` `edits` list:

```yaml
- path: SKILL.md
  op: replace
  start_line: 74
  end_line: 74
  expected_lines:
  - '    "Dispatch final code reviewer (../requesting-code-review/code-reviewer.md)" [shape=box];'
  replace_lines:
  - '    "Invoke /review-branch-diff for final whole-branch review" [shape=box];'
- path: SKILL.md
  op: replace
  start_line: 103
  end_line: 103
  expected_lines:
  - '    "More tasks remain?" -> "Dispatch final code reviewer (../requesting-code-review/code-reviewer.md)" [label="no"];'
  replace_lines:
  - '    "More tasks remain?" -> "Invoke /review-branch-diff for final whole-branch review" [label="no"];'
- path: SKILL.md
  op: replace
  start_line: 104
  end_line: 104
  expected_lines:
  - '    "Dispatch final code reviewer (../requesting-code-review/code-reviewer.md)" -> "Final findings? ONE fix dispatch, one scoped re-review, adjudicate residuals";'
  replace_lines:
  - '    "Invoke /review-branch-diff for final whole-branch review" -> "Final findings? ONE fix dispatch, one scoped re-review, adjudicate residuals";'
```

- [ ] **Step 4: Commit the overlay changes**

```bash
git add adapters/codex/superpowers-plus/subagent-driven-development/overlay.yaml
git commit --no-verify -m "feat: route SDD to custom implementer/reviewer/branch-reviewer profiles on Devin Desktop"
```

---

### Task 5: Regenerate marketplace and installed skill surfaces

**Files:**
- Generated: `codex-marketplace/plugins/repo-worker-pack/skills/review-branch-diff/`
- Generated: `codex-marketplace/plugins/repo-worker-pack/references/bundle-manifest.json`
- Generated: `.agents/skills/review-branch-diff/`
- Generated: `codex-marketplace/plugins/repo-worker-pack/INDEX.md` and mesh navigation

**Interfaces:**
- Consumes: the source edits from Tasks 1–4.
- Produces: projected and installed skill surfaces ready for use.

- [ ] **Step 1: Regenerate the repo mesh**

Run:
```bash
tools/run mesh --apply
```

Expected: `INDEX.md` files are updated. Check that `codex-marketplace/plugins/repo-worker-pack/INDEX.md` and `.agents/superpowers/specs/INDEX.md` include the new spec and skill.

- [ ] **Step 2: Regenerate the marketplace projection**

Run:
```bash
tools/run marketplace --apply
```

Expected: `codex-marketplace/plugins/repo-worker-pack/skills/review-branch-diff/` is created, `references/bundle-manifest.json` is updated, and `provenance/repo-worker-pack.md` and `references/source-map.md` are regenerated.

- [ ] **Step 3: Refresh installed skills**

Run:
```bash
tools/run installed-skills --apply
```

Expected: `.agents/skills/review-branch-diff/` is created or updated.

- [ ] **Step 4: Run the CI check**

Run:
```bash
tools/run ci --check
```

Expected: all checks pass. If `INDEX.md` or marketplace checks fail, run the corresponding `--apply` command from the error message and re-check.

- [ ] **Step 5: Commit the generated changes**

```bash
git add codex-marketplace/ .agents/skills/review-branch-diff .agents/skills/subagent-driven-development .agents/skills/subagent-model-routing .agents/superpowers/specs/INDEX.md
git commit --no-verify -m "chore: regenerate marketplace and installed skill surfaces"
```

---

### Task 6: Manual end-to-end test

**Files:**
- Use a throwaway branch and the local Devin Desktop environment.

**Interfaces:**
- Consumes: the updated installed skills and global subagent profiles.
- Produces: confidence that `review-branch-diff` and SDD dispatch work.

- [ ] **Step 1: Create a throwaway test branch and commit**

```bash
git checkout -b test/review-branch-diff
New-Item -ItemType File -Path "TEST_REVIEW_BRANCH_DIFF.txt" -Value "throwaway test" -Force
git add TEST_REVIEW_BRANCH_DIFF.txt
git commit --no-verify -m "test: throwaway change"
```

- [ ] **Step 2: Restart Devin Desktop/CLI**

Restart so the new `.agents/skills/review-branch-diff` and `.agents/skills/subagent-driven-development` projections are loaded.

- [ ] **Step 3: Test `/review-branch-diff`**

In the session, run:
```text
/review-branch-diff
```

Expected: the skill dispatches `branch-reviewer`, produces a diff review, and recommends not merging the throwaway file.

- [ ] **Step 4: Test an SDD plan**

Create or use an existing small plan and run:
```text
/subagent-driven-development .agents/superpowers/plans/<some-plan>.md
```

Expected: per-task implementer dispatches use `run_subagent profile: implementer` and per-task reviewers use `run_subagent profile: reviewer`; the final whole-branch step invokes `/review-branch-diff`.

- [ ] **Step 5: Clean up the test branch**

```bash
git checkout main
git branch -D test/review-branch-diff
```

---

### Task 7: Commit, push, and open a PR

**Files:**
- All committed changes on `spec/custom-subagent-routing`.

- [ ] **Step 1: Verify all commits are on the branch**

```bash
git log --oneline main..spec/custom-subagent-routing
```

Expected: all Task 1–6 commits are present.

- [ ] **Step 2: Push the branch**

```bash
git push origin spec/custom-subagent-routing
```

- [ ] **Step 3: Open a PR to `main` using the PR template**

Run:
```bash
gh pr create --base main --title "feat: custom Devin Desktop subagent routing and review-branch-diff skill" --body-file .github/PULL_REQUEST_TEMPLATE.md
```

Fill in every section of the template, including:
- **What this changes:** `subagent-model-routing` reference doc, `subagent-driven-development` overlay, new `review-branch-diff` skill bundled in `repo-worker-pack`.
- **Why:** the spike proved Devin Desktop custom subagents work; this makes the repo guidance and SDD workflow accurate.
- **Test evidence:** `tools/run ci --check` passed and the manual end-to-end test ran.
- **Co-Authored-By:** Generated with Devin.

---

## Self-Review Checklist

Before handing off for execution, verify the plan against the spec:

- [ ] Task 1 creates the `review-branch-diff` source with `SKILL.md`, `agents/openai.yaml`, and the `branch-reviewer` fallback asset.
- [ ] Task 2 adds the skill to `repo-worker-pack` through `custody-pack-registry.json`.
- [ ] Task 3 updates `devin-desktop-profile.md` with custom profiles, `model:` behavior, and `write` limitation.
- [ ] Task 4 updates the SDD overlay with `run_subagent profile: implementer`, `run_subagent profile: reviewer`, and `/review-branch-diff` for the final review.
- [ ] Task 5 regenerates surfaces and runs `tools/run ci --check`.
- [ ] Task 6 manually tests the new skill and SDD dispatch.
- [ ] Task 7 publishes the PR.
