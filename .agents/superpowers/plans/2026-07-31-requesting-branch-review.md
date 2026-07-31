# Requesting Branch Review — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the subagent-locked `review-branch-diff` skill with a main-agent `requesting-branch-review` skill that dispatches the `branch-reviewer` subagent for a specific branch and worktree.

**Architecture:** Rename the first-party source tree, rewrite the `SKILL.md` without the `agent:` frontmatter, update all marketplace and adapter references, then run `tools/run marketplace --apply` to regenerate the Codex projection and installed skills. The `branch-reviewer` subagent profile and its `AGENT.md` stay unchanged.

**Tech Stack:** Devin Desktop skill frontmatter, `run_subagent` dispatch, `tools/run` marketplace and CI, git.

## Global Constraints

- `requesting-branch-review/SKILL.md` must have **no `agent:`** frontmatter; it runs on the main agent.
- `assets/branch-reviewer/AGENT.md` remains read-only and restricts `exec` to git commands.
- Edit only `sources/`, `adapters/`, and `codex-marketplace/custody-pack-registry.json`; generated surfaces under `codex-marketplace/plugins/`, `.agents/skills/`, `generated/skill-zips/`, and indexes are downstream.
- All text files use LF only; `core.autocrlf` is `false`.
- Canonical local green proof: `tools/run marketplace --apply` then `tools/run ci --check`.
- The repo pre-commit hook runs `tools/run ci --check`; if a commit is made without the hook, run `tools/run ci --check` separately afterward.

---

### Task 1: Create the new first-party skill source and remove the old one

**Files:**
- Create: `sources/first_party/skills/requesting-branch-review/SKILL.md`
- Create: `sources/first_party/skills/requesting-branch-review/agents/openai.yaml`
- Create: `sources/first_party/skills/requesting-branch-review/assets/branch-reviewer/AGENT.md`
- Delete: `sources/first_party/skills/review-branch-diff/`

**Interfaces:**
- Produces: `requesting-branch-review` source tree with `SKILL.md`, `agents/openai.yaml`, and `assets/branch-reviewer/AGENT.md`.

- [x] **Step 1: Create `sources/first_party/skills/requesting-branch-review/SKILL.md`**

```markdown
---
name: requesting-branch-review
description: Use when an agent should dispatch a whole-branch diff review for a
  specific branch and worktree against main.
metadata:
  source-id: requesting-branch-review
  source-path: sources/first_party/skills/requesting-branch-review/SKILL.md
  provenance-name: Requesting Branch Review first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when an agent should dispatch a whole-branch diff review for a specific
    branch and worktree against main.
  use_when:
  - Use when an agent should dispatch a whole-branch diff review for a specific branch.
  - Use when the user asks to review a branch diff against main and the branch or worktree is not the current one.
  - Use when the main agent can gather the target branch and worktree and then launch the branch-reviewer subagent.
  do_not_use_when:
  - Do not use when the current branch has no commits ahead of main.
  - Do not use when only a single file or small diff needs review; use a file-level reviewer instead.
  related_skills:
  - selecting-a-subagent
  - subagent-driven-development
  - finishing-a-development-branch
  - requesting-code-review
license: MIT
triggers:
- user
- model
---

# Requesting Branch Review

Use the `branch-reviewer` subagent to review a branch diff for a specific branch and worktree.

1. Determine the target branch and worktree:
   - If the user provided them, use those values.
   - Otherwise, default to the current git branch and current working directory.
   - If any value is ambiguous or missing, ask the user before proceeding.
2. Verify the branch exists: run `git rev-parse --verify <branch>` (or `git rev-parse --verify refs/heads/<branch>`). If it does not exist, stop and report.
3. Verify the worktree exists: check that `<worktree>` is a directory and contains a `.git` directory or file. If it does not exist, stop and report.
4. Determine the base ref. In the worktree, run `git rev-parse --verify main` and, if that fails, `git rev-parse --verify origin/main`. Use the first one that succeeds as `<base>`.
5. If the global `branch-reviewer` subagent profile is missing or does not match the bundled `assets/branch-reviewer/AGENT.md`, install or overwrite it by copying `assets/branch-reviewer/AGENT.md` to `~/.config/devin/agents/branch-reviewer/AGENT.md` (macOS/Linux) or `%APPDATA%\devin\agents\branch-reviewer\AGENT.md` (Windows).
6. Dispatch the subagent:

```
run_subagent profile: branch-reviewer
  title: "Review <branch> vs <base>"
  task: "Review the diff of branch <branch> against <base> in the worktree at <worktree> for correctness, style, consistency, and risk. If the subagent is not already in that worktree, run `cd <worktree>` before running any git commands. Use `git diff --no-color <base>...<branch>` to obtain the diff. Cite specific files and line numbers. Do not modify files."
```

7. Report the findings returned by the subagent.
```

- [x] **Step 2: Create `sources/first_party/skills/requesting-branch-review/agents/openai.yaml`**

```yaml
version: 1
metadata:
  skill_name: requesting-branch-review
  source_category: first_party
interface:
  display_name: Requesting Branch Review
  short_description: Use when an agent should dispatch a whole-branch diff review for a specific branch and worktree against main.
  default_prompt: Use /requesting-branch-review when an agent should dispatch a whole-branch diff review for a specific branch and worktree against main.
policy:
  allow_implicit_invocation: false
```

- [x] **Step 3: Create `sources/first_party/skills/requesting-branch-review/assets/branch-reviewer/AGENT.md`**

```markdown
---
name: branch-reviewer
description: Branch diff reviewer — reviews the diff of an explicitly named branch and worktree against main for correctness, style, consistency, and risk, and cites specific files and line numbers.
model: swe-1-7
allowed-tools:
  - read
  - grep
  - exec
---

You are a branch diff reviewer. Your job is to review a branch diff against `main` (or `origin/main`) for correctness, style, consistency, and risk, and to report focused, actionable findings with specific file and line citations.

## Invariants

- You are read-only. Do not modify files, create files, or run build/install/write commands.
- You may use `exec` only for git commands and non-mutating canonical verification commands (e.g. the consumer's CI command such as `scripts/ci-preflight.ps1 -Check`, `tools/run ci --check`, or `py -3 -m pytest ...`).
- Cite specific files and line numbers for every issue you find.
- Keep feedback focused, concrete, and actionable.

## Procedure

1. Read the dispatch task. The calling agent should name a `<branch>` and a `<worktree>`. If either is missing, fall back to the current branch and current working directory, and ask for confirmation if it is still unclear.
2. Determine the base ref. In the named worktree, run `git rev-parse --verify main` and, if that fails, `git rev-parse --verify origin/main`. Use the first one that succeeds as `<base>`.
3. Obtain the diff. If `<worktree>` is not the current directory, run `cd <worktree>` before any git command. Then run `git diff --no-color <base>...<branch>`.
4. If the diff is too large to review at once, run `git diff --stat <base>...<branch>`, then review changed files in batches using `git diff --no-color <base>...<branch> -- <path>`.
5. Identify correctness, style, consistency, and risk issues. Cite specific files and line numbers.
6. Do not modify files. Do not run build, install, or write commands.

## Rules

- Use `exec` primarily for git commands needed to produce or navigate the diff: `git diff`, `git rev-parse`, `git log`, `git show`, `git status`, `git branch`.
- You may also run non-mutating canonical verification commands (e.g. the consumer's CI command such as `scripts/ci-preflight.ps1 -Check`, `tools/run ci --check`, or `py -3 -m pytest ...`) when they are needed to verify a claim.
- Do not modify files. Do not run build, install, or write commands.
- Cite specific files and line numbers for every issue you find.
- Keep feedback focused, concrete, and actionable.
- If the diff is large, start with `git diff --stat` and review files in batches.
```

- [x] **Step 4: Install the updated `branch-reviewer` profile to the global agents directory**

```powershell
$globalDir = "$env:APPDATA\devin\agents\branch-reviewer"
New-Item -ItemType Directory -Path $globalDir -Force
Copy-Item -Path "sources/first_party/skills/requesting-branch-review/assets/branch-reviewer/AGENT.md" -Destination "$globalDir\AGENT.md" -Force
```

On macOS/Linux, use `mkdir -p ~/.config/devin/agents/branch-reviewer && cp sources/first_party/skills/requesting-branch-review/assets/branch-reviewer/AGENT.md ~/.config/devin/agents/branch-reviewer/AGENT.md`.

- [x] **Step 5: Remove the old source tree**

```powershell
Remove-Item -Recurse -Force sources/first_party/skills/review-branch-diff
```

- [x] **Step 6: Verify the new source tree exists and the global profile is installed**

```powershell
if (Test-Path sources/first_party/skills/review-branch-diff) { throw 'old path still exists' }
if (-not (Test-Path sources/first_party/skills/requesting-branch-review/SKILL.md)) { throw 'new SKILL.md missing' }
if (-not (Test-Path sources/first_party/skills/requesting-branch-review/agents/openai.yaml)) { throw 'new openai.yaml missing' }
if (-not (Test-Path sources/first_party/skills/requesting-branch-review/assets/branch-reviewer/AGENT.md)) { throw 'new AGENT.md missing' }
if (-not (Test-Path "$env:APPDATA\devin\agents\branch-reviewer\AGENT.md")) { throw 'global branch-reviewer profile not installed' }
Write-Host 'source tree and global profile ok'
```

On macOS/Linux, adjust the global profile path to `~/.config/devin/agents/branch-reviewer/AGENT.md`.

- [x] **Step 7: Mark all Task 1 steps `[x]` in this plan file**

Use the `edit` tool to update the checkboxes in Task 1 from `[ ]` to `[x]`.

---

### Task 2: Update marketplace wiring and skill references

**Files:**
- Modify: `codex-marketplace/custody-pack-registry.json`
- Modify: `adapters/codex/superpowers-plus/subagent-driven-development/overlay.yaml`
- Modify: `sources/first_party/skills/selecting-a-subagent/SKILL.md`
- Modify: `sources/first_party/skills/selecting-a-subagent/references/devin-desktop-profile.md`

**Interfaces:**
- Consumes: the new `sources/first_party/skills/requesting-branch-review/` source tree from Task 1.
- Produces: registry and adapter surfaces that point at `requesting-branch-review` instead of `review-branch-diff`.

- [ ] **Step 1: Rename registry entries in `codex-marketplace/custody-pack-registry.json`**

Use `edit` with `replace_all: true` on `codex-marketplace/custody-pack-registry.json` to replace every occurrence of the string `review-branch-diff` with `requesting-branch-review`.

After the replacement, the file should contain:
- `"canonical_name": "requesting-branch-review"`
- `"canonical_source_path": "sources/first_party/skills/requesting-branch-review"`
- `"local_path": "skills/requesting-branch-review"`
- `"source_path": "sources/first_party/skills/requesting-branch-review/SKILL.md"`
- `"sources/first_party/skills/requesting-branch-review"` in the `repo-worker-pack` `source_ledger`

Then update the `provenance_note` strings so they read `requesting-branch-review` rather than `branch-diff`:

Old:
```
"provenance_note": "First-party branch-diff review skill projected verbatim into the Superpowers bundle."
```

New:
```
"provenance_note": "First-party requesting-branch-review skill projected verbatim into the Superpowers bundle."
```

Old:
```
"provenance_note": "First-party branch-diff review skill projected verbatim into the repo-worker-pack."
```

New:
```
"provenance_note": "First-party requesting-branch-review skill projected verbatim into the repo-worker-pack."
```

- [ ] **Step 2: Update the SDD adapter overlay**

Use `edit` with `replace_all: true` on `adapters/codex/superpowers-plus/subagent-driven-development/overlay.yaml` to replace every occurrence of the string `/review-branch-diff` with `/requesting-branch-review`.

- [ ] **Step 3: Update `selecting-a-subagent` references**

In `sources/first_party/skills/selecting-a-subagent/SKILL.md`:

Old:
```
shipped with the `review-branch-diff` skill.
```

New:
```
shipped with the `requesting-branch-review` skill.
```

In `sources/first_party/skills/selecting-a-subagent/references/devin-desktop-profile.md`:

Old:
```
| Branch diff review | `run_subagent profile: branch-reviewer` or invoke `/review-branch-diff` |
```

New:
```
| Branch diff review | `run_subagent profile: branch-reviewer` or invoke `/requesting-branch-review` |
```

- [ ] **Step 4: Verify all references flipped**

```powershell
$refs = Select-String -Path 'codex-marketplace/custody-pack-registry.json' -Pattern 'review-branch-diff' -AllMatches
$refs += Select-String -Path 'adapters/codex/superpowers-plus/subagent-driven-development/overlay.yaml' -Pattern 'review-branch-diff' -AllMatches
$refs += Select-String -Path 'sources/first_party/skills/selecting-a-subagent/SKILL.md' -Pattern 'review-branch-diff' -AllMatches
$refs += Select-String -Path 'sources/first_party/skills/selecting-a-subagent/references/devin-desktop-profile.md' -Pattern 'review-branch-diff' -AllMatches
if ($refs) { throw "stale review-branch-diff references: $($refs | Out-String)" }
Write-Host 'all references updated'
```

- [ ] **Step 5: Mark all Task 2 steps `[x]` in this plan file**

Use the `edit` tool to update the checkboxes in Task 2 from `[ ]` to `[x]`.

---

### Task 3: Regenerate marketplace and installed-skill surfaces

**Files:**
- Derived: `codex-marketplace/plugins/repo-worker-pack/skills/requesting-branch-review/`
- Derived: `codex-marketplace/plugins/superpowers-plus/skills/requesting-branch-review/`
- Derived: `codex-marketplace/plugins/house-skills/skills/requesting-branch-review/`
- Derived: `.agents/skills/requesting-branch-review/`
- Derived: `generated/skill-zips/requesting-branch-review.zip`
- Derived: `provenance/first-party-skills.md`
- Derived: `sources/first_party/skills/INDEX.md`
- Derived: `repo-index/repo-index.json`

**Interfaces:**
- Consumes: source tree from Task 1 and registry/adapter edits from Task 2.
- Produces: projected and installed skill copies, plus updated indexes and provenance.

- [x] **Step 1: Run the overlay healing check**

```powershell
.\tools\run.ps1 heal --check
```

Expected: no line-number drift in `adapters/codex/superpowers-plus/subagent-driven-development/overlay.yaml` or any other overlay.

- [x] **Step 2: Run the full local regeneration**

```powershell
.\tools\run.ps1 marketplace --apply --allow-shared-checkout
```

Expected: all targets pass and the command reports `Marketplace validation passed.` for inventory, project, installed-skills, repo-index, mesh, catalog, and validate.

- [x] **Step 3: Confirm the projected skill lacks the `agent:` frontmatter**

```powershell
$agentLine = Select-String -Path 'codex-marketplace/plugins/repo-worker-pack/skills/requesting-branch-review/SKILL.md' -Pattern '^agent:'
if ($agentLine) { throw 'projected SKILL.md still has agent:' }
Write-Host 'projected SKILL.md is main-agent ready'
```

- [x] **Step 4: Confirm the installed skill exists and is main-agent ready**

```powershell
if (-not (Test-Path .agents/skills/requesting-branch-review/SKILL.md)) { throw 'installed skill missing' }
$agentLine = Select-String -Path '.agents/skills/requesting-branch-review/SKILL.md' -Pattern '^agent:'
if ($agentLine) { throw 'installed SKILL.md still has agent:' }
Write-Host 'installed skill is main-agent ready'
```

- [x] **Step 5: Mark all Task 3 steps `[x]` in this plan file**

Use the `edit` tool to update the checkboxes in Task 3 from `[ ]` to `[x]`.

---

### Task 4: Commit and run the CI gate

**Files:**
- Branch: `feat/requesting-branch-review`

- [ ] **Step 1: Review the working tree**

```powershell
git status
git diff --stat
git log --oneline -5
```

- [ ] **Step 2: Stage and commit the implementation**

```powershell
git add -A
git commit -m "feat: replace review-branch-diff with requesting-branch-review" -m "requesting-branch-review is a main-agent dispatch skill that gathers a branch and worktree before launching the branch-reviewer subagent. The old review-branch-diff source is removed; the branch-reviewer profile and AGENT.md remain unchanged." -m "Generated with [Devin](https://devin.ai)" -m "Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
```

Expected: the repo pre-commit hook runs `tools/run ci --check` and the commit succeeds only if the CI gate passes.

- [ ] **Step 3: If the pre-commit hook was bypassed, run CI explicitly**

```powershell
.\tools\run.ps1 ci --check
```

Use this only if the commit in Step 2 was made with `--no-verify`.

- [ ] **Step 4: Mark all Task 4 steps `[x]` in this plan file**

Use the `edit` tool to update the checkboxes in Task 4 from `[ ]` to `[x]`.

---

### Task 5: Push and open a PR into `main`

**Files:**
- Branch: `feat/requesting-branch-review`

- [ ] **Step 1: Push the branch**

```powershell
git push -u origin feat/requesting-branch-review
```

- [ ] **Step 2: Open a PR**

```powershell
gh pr create --title "feat: replace review-branch-diff with requesting-branch-review" --body "## Summary`n- Renames first-party source from `review-branch-diff` to `requesting-branch-review`.`n- New `SKILL.md` runs on the main agent and dispatches `branch-reviewer` with an explicit branch and worktree.`n- Updates registry, SDD overlay, and `selecting-a-subagent` references.`n- Regenerates marketplace and installed-skill surfaces.`n`n## Test plan`n- [x] `tools/run heal --check` passed`n- [x] `tools/run marketplace --apply` passed`n- [x] `tools/run ci --check` passed" --base main
```

- [ ] **Step 3: Mark all Task 5 steps `[x]` in this plan file**

Use the `edit` tool to update the checkboxes in Task 5 from `[ ]` to `[x]`.

---

## Self-Review

1. **Spec coverage:**
   - Rename source tree — Task 1.
   - Rewrite `SKILL.md` without `agent:` — Task 1.
   - Update `agents/openai.yaml` — Task 1.
   - Keep `assets/branch-reviewer/AGENT.md` — Task 1.
   - Update `custody-pack-registry.json` — Task 2.
   - Update SDD overlay and `selecting-a-subagent` — Task 2.
   - Heal overlays before regeneration — Task 3.
   - Regenerate surfaces with `tools/run marketplace --apply` — Task 3.
   - Commit and run `tools/run ci --check` — Task 4.
   - Push and open PR — Task 5.

2. **Placeholder scan:** No `TBD`, `TODO`, or vague commands remain. Every file has its exact content or exact `edit` old/new string.

3. **Type consistency:** The `SKILL.md` `source-id`, `source-path`, and `name` all match `requesting-branch-review`. The registry `canonical_name`/`canonical_source_path`/`local_path`/`source_path` all match the new path. The adapter and `selecting-a-subagent` slash references all use `/requesting-branch-review`.

4. **Dependency order:** Task 1 must precede Task 2 because the registry now points at `requesting-branch-review`, which must exist. Task 2 must precede Task 3 because `heal` and `marketplace` use the registry and adapters. Task 3 must precede Task 4 because `ci --check` validates the committed, regenerated tree.

---

## Execution Handoff

**Plan complete and saved to `.agents/superpowers/plans/2026-07-31-requesting-branch-review.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — Execute tasks in this session using `superpowers:executing-plans`, batch execution with checkpoints.

**Before choosing an execution option, use `handoff-gates` plan-readiness lane.** Rate the plan for execution confidence (8/10 floor, 9/10 target). Report the final rating in the handoff. Do not execute below 8/10.
