# Superpowers+ First-Party Conversion — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the `superpowers-plus` Codex plugin's 14 currently-adapted third-party skills into first-party authored skills, retire their adapter overlays, and regenerate the marketplace surfaces so the bundle is first-party `verbatim`.

**Architecture:** Promote the current projected `codex-marketplace/plugins/superpowers-plus/skills/<name>/` content into `sources/first_party/skills/<name>/`, swap to canonical first-party `SKILL.md` frontmatter and `agents/openai.yaml`, migrate adapter scripts and `using-superpowers` to `using-superpowers-plus`, update the custody registry and provenance, delete the overlay tree, and run the deterministic regeneration pipeline.

**Tech Stack:** Markdown skill docs, YAML agent wrappers, `codex-marketplace/custody-pack-registry.json`, `tools\run.ps1` deterministic build pipeline, git.

## Global Constraints

- `sources/third_party/superpowers/` remains immutable. Do not edit it.
- First-party source becomes the editable custody for `superpowers-plus` skills.
- Do not hand-edit generated plugin skill trees, bundle manifests, source maps, or provenance maps; edit the registry and source, then regenerate.
- All first-party skills must pass the marketplace shape validators and `normalize_first_party_skill_sources.py`.
- `using-superpowers` becomes `using-superpowers-plus`; downstream references in first-party skills (e.g. `inspecting-the-environment`) must be updated.
- The `superpowers-plus` plugin root and marketplace identity stay the same; only the source custody and provenance mode change.
- License posture stays honest: first-party skills are MIT, and each skill's provenance metadata names the upstream `obra/superpowers` v6.2.0 MIT source it derives from.

---

### Canonical first-party `SKILL.md` frontmatter

Use this exact frontmatter for every new first-party `SKILL.md`. The implementer copies the body from the projected `codex-marketplace/plugins/superpowers-plus/skills/<name>/SKILL.md` (everything after the existing frontmatter), then replaces the frontmatter with the shape below and prepends the provenance block.

```markdown
---
name: <skill-name>
description: <trigger description>
metadata:
  source-id: <skill-name>
  source-path: sources/first_party/skills/<skill-name>/SKILL.md
  provenance-name: <Skill Name> first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: <trigger description>
  use_when:
    - ...
  do_not_use_when:
    - ...
  related_skills:
    - ...
license: MIT
---

## Provenance

This skill is a first-party authored derivation of `obra/superpowers` v6.2.0, released under the MIT License. The original upstream snapshot is retained in `sources/third_party/superpowers/obra-superpowers/v6.2.0/skills/<original-skill-name>/` for reference.

<projected body follows here>
```

For each skill, `<original-skill-name>` is the same as `<skill-name>` except `using-superpowers`, whose original is `using-superpowers` and whose new `<skill-name>` is `using-superpowers-plus`.

### Canonical first-party `agents/openai.yaml` shape

Create this exact `agents/openai.yaml` in every new first-party skill root.

```yaml
version: 1
metadata:
  skill_name: <skill-name>
  source_category: first_party

interface:
  display_name: <Skill Name>
  short_description: <use when phrasing>
  default_prompt: Use /<skill-name> to <use when phrasing>.

policy:
  products:
    - codex
  allow_implicit_invocation: true
```

For `using-superpowers-plus`, set `skill_name: using-superpowers-plus`, `display_name: Using Superpowers Plus`, and the short description / default prompt to reference `using-superpowers-plus`.

---

### Task 1: Bulk-create the 10 lightweight first-party skill roots

**Files:**
- Create (copy/adapt from projected `codex-marketplace/plugins/superpowers-plus/skills/<name>/`):
  - `sources/first_party/skills/brainstorming/SKILL.md`
  - `sources/first_party/skills/brainstorming/agents/openai.yaml`
  - `sources/first_party/skills/brainstorming/scripts/start-server.ps1`
  - `sources/first_party/skills/brainstorming/scripts/stop-server.ps1`
  - `sources/first_party/skills/brainstorming/references/script-shell-selection.md` (or delete if it only served the overlay)
  - `sources/first_party/skills/dispatching-parallel-agents/SKILL.md`
  - `sources/first_party/skills/dispatching-parallel-agents/agents/openai.yaml`
  - `sources/first_party/skills/executing-plans/SKILL.md`
  - `sources/first_party/skills/executing-plans/agents/openai.yaml`
  - `sources/first_party/skills/finishing-a-development-branch/SKILL.md`
  - `sources/first_party/skills/finishing-a-development-branch/agents/openai.yaml`
  - `sources/first_party/skills/receiving-code-review/SKILL.md`
  - `sources/first_party/skills/receiving-code-review/agents/openai.yaml`
  - `sources/first_party/skills/requesting-code-review/SKILL.md`
  - `sources/first_party/skills/requesting-code-review/agents/openai.yaml`
  - `sources/first_party/skills/test-driven-development/SKILL.md`
  - `sources/first_party/skills/test-driven-development/agents/openai.yaml`
  - `sources/first_party/skills/verification-before-completion/SKILL.md`
  - `sources/first_party/skills/verification-before-completion/agents/openai.yaml`
  - `sources/first_party/skills/writing-plans/SKILL.md`
  - `sources/first_party/skills/writing-plans/agents/openai.yaml`
  - `sources/first_party/skills/writing-skills/SKILL.md`
  - `sources/first_party/skills/writing-skills/agents/openai.yaml`
- Copy from adapters to the new `brainstorming` root:
  - `adapters/codex/superpowers-plus/brainstorming/scripts/start-server.ps1` -> `sources/first_party/skills/brainstorming/scripts/start-server.ps1`
  - `adapters/codex/superpowers-plus/brainstorming/scripts/stop-server.ps1` -> `sources/first_party/skills/brainstorming/scripts/stop-server.ps1`
- Inspect and either copy or delete:
  - `adapters/codex/superpowers-plus/script-shell-selection.md` -> `sources/first_party/skills/brainstorming/references/script-shell-selection.md`

**Interfaces:**
- Produces: 10 first-party skill source roots with canonical `SKILL.md` and `agents/openai.yaml`.

- [x] **Step 1: Create the 10 first-party directories.**

```powershell
$names = @("brainstorming", "dispatching-parallel-agents", "executing-plans", "finishing-a-development-branch", "receiving-code-review", "requesting-code-review", "test-driven-development", "verification-before-completion", "writing-plans", "writing-skills")
$names | ForEach-Object { New-Item -ItemType Directory -Path "sources/first_party/skills/$_" -Force }
$names | ForEach-Object { New-Item -ItemType Directory -Path "sources/first_party/skills/$_/agents" -Force }
New-Item -ItemType Directory -Path "sources/first_party/skills/brainstorming/scripts" -Force
New-Item -ItemType Directory -Path "sources/first_party/skills/brainstorming/references" -Force
```

- [x] **Step 2: For each of the 10 skills, write `sources/first_party/skills/<name>/SKILL.md`.**

For each skill:
1. Read `codex-marketplace/plugins/superpowers-plus/skills/<name>/SKILL.md`.
2. Discard the existing frontmatter (everything before `# ...`).
3. Write the canonical frontmatter above, substituting `<skill-name>`, `<Skill Name>`, the `description`, and the `use_when` / `do_not_use_when` / `related_skills` values from the projected frontmatter.
4. Prepend the `## Provenance` block.
5. Append the projected body.

- [x] **Step 3: For each of the 10 skills, create `sources/first_party/skills/<name>/agents/openai.yaml`.**

Use the canonical `agents/openai.yaml` shape. Set `display_name` to the kebab-case name converted to title case (e.g. `Dispatching Parallel Agents`), `short_description` to the `description`, and `default_prompt` to `Use /<skill-name> to <description>.`.

- [x] **Step 4: Migrate `brainstorming` scripts.**

```powershell
Copy-Item -Path "adapters/codex/superpowers-plus/brainstorming/scripts/start-server.ps1" -Destination "sources/first_party/skills/brainstorming/scripts/start-server.ps1"
Copy-Item -Path "adapters/codex/superpowers-plus/brainstorming/scripts/stop-server.ps1" -Destination "sources/first_party/skills/brainstorming/scripts/stop-server.ps1"
```

If `script-shell-selection.md` is still referenced in the `brainstorming` body, copy it to `sources/first_party/skills/brainstorming/references/script-shell-selection.md`; otherwise delete it.

- [x] **Step 5: Verify the new roots.**

```powershell
$names = @("brainstorming", "dispatching-parallel-agents", "executing-plans", "finishing-a-development-branch", "receiving-code-review", "requesting-code-review", "test-driven-development", "verification-before-completion", "writing-plans", "writing-skills")
$ok = $true
$names | ForEach-Object {
    if (-not (Test-Path "sources/first_party/skills/$_/SKILL.md")) { Write-Host "Missing SKILL.md for $_"; $ok = $false }
    if (-not (Test-Path "sources/first_party/skills/$_/agents/openai.yaml")) { Write-Host "Missing agents/openai.yaml for $_"; $ok = $false }
}
if (-not (Test-Path "sources/first_party/skills/brainstorming/scripts/start-server.ps1")) { $ok = $false }
if (-not (Test-Path "sources/first_party/skills/brainstorming/scripts/stop-server.ps1")) { $ok = $false }
if (-not $ok) { throw "Verification failed" }
git diff --check
git diff --stat
```

- [x] **Step 6: Commit.**

```powershell
git add sources/first_party/skills
git commit -m "feat: create first-party source roots for 10 lightweight superpowers-plus skills"
```

---

### Task 2: Migrate `subagent-driven-development` with its adapter scripts

**Files:**
- Create: `sources/first_party/skills/subagent-driven-development/SKILL.md`
- Create: `sources/first_party/skills/subagent-driven-development/agents/openai.yaml`
- Create: `sources/first_party/skills/subagent-driven-development/scripts/review-package`
- Create: `sources/first_party/skills/subagent-driven-development/scripts/review-package.ps1`
- Create: `sources/first_party/skills/subagent-driven-development/scripts/sdd-workspace`
- Create: `sources/first_party/skills/subagent-driven-development/scripts/sdd-workspace.ps1`
- Create: `sources/first_party/skills/subagent-driven-development/scripts/task-brief`
- Create: `sources/first_party/skills/subagent-driven-development/scripts/task-brief.ps1`
- Copy from adapter: `adapters/codex/superpowers-plus/subagent-driven-development/scripts/*` -> `sources/first_party/skills/subagent-driven-development/scripts/`

**Interfaces:**
- Produces: first-party `subagent-driven-development` source root with scripts.

- [x] **Step 1: Create `sources/first_party/skills/subagent-driven-development/SKILL.md`.**

Use the canonical frontmatter with `name: subagent-driven-development` and `provenance-name: Subagent Driven Development first-party skill`. Copy the projected body from `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/SKILL.md` and prepend the provenance block.

- [x] **Step 2: Create `sources/first_party/skills/subagent-driven-development/agents/openai.yaml`.**

Use the canonical `agents/openai.yaml` shape with `skill_name: subagent-driven-development`, `display_name: Subagent Driven Development`, and the short description / default prompt from the projected frontmatter.

- [x] **Step 3: Copy the adapter scripts into the first-party root.**

```powershell
New-Item -ItemType Directory -Path "sources/first_party/skills/subagent-driven-development/scripts" -Force
Get-ChildItem -Path "adapters/codex/superpowers-plus/subagent-driven-development/scripts" | Copy-Item -Destination "sources/first_party/skills/subagent-driven-development/scripts/"
```

- [x] **Step 4: Verify.**

```powershell
$expected = @("SKILL.md", "agents/openai.yaml", "scripts/review-package", "scripts/review-package.ps1", "scripts/sdd-workspace", "scripts/sdd-workspace.ps1", "scripts/task-brief", "scripts/task-brief.ps1")
$expected | ForEach-Object { if (-not (Test-Path "sources/first_party/skills/subagent-driven-development/$_")) { throw "Missing $_" } }
git diff --check
git diff --stat
```

- [x] **Step 5: Commit.**

```powershell
git add sources/first_party/skills/subagent-driven-development
git commit -m "feat: migrate subagent-driven-development to first-party source"
```

---

### Task 3: Migrate `systematic-debugging` with its PowerShell helper

**Files:**
- Create: `sources/first_party/skills/systematic-debugging/SKILL.md`
- Create: `sources/first_party/skills/systematic-debugging/agents/openai.yaml`
- Create: `sources/first_party/skills/systematic-debugging/scripts/find-polluter.ps1`
- Copy: `adapters/codex/superpowers-plus/systematic-debugging/scripts/find-polluter.ps1` -> `sources/first_party/skills/systematic-debugging/scripts/find-polluter.ps1`

**Interfaces:**
- Produces: first-party `systematic-debugging` source root.

- [x] **Step 1: Create `SKILL.md` and `agents/openai.yaml`.**

Use the canonical shapes. `name: systematic-debugging`, `provenance-name: Systematic Debugging first-party skill`.

- [x] **Step 2: Copy the adapter script.**

```powershell
New-Item -ItemType Directory -Path "sources/first_party/skills/systematic-debugging/scripts" -Force
Copy-Item -Path "adapters/codex/superpowers-plus/systematic-debugging/scripts/find-polluter.ps1" -Destination "sources/first_party/skills/systematic-debugging/scripts/find-polluter.ps1"
```

- [x] **Step 3: Verify.**

```powershell
$expected = @("SKILL.md", "agents/openai.yaml", "scripts/find-polluter.ps1")
$expected | ForEach-Object { if (-not (Test-Path "sources/first_party/skills/systematic-debugging/$_")) { throw "Missing $_" } }
git diff --check
git diff --stat
```

- [x] **Step 4: Commit.**

```powershell
git add sources/first_party/skills/systematic-debugging
git commit -m "feat: migrate systematic-debugging to first-party source"
```

---

### Task 4: Migrate `using-git-worktrees` with its worktree scripts

**Files:**
- Create: `sources/first_party/skills/using-git-worktrees/SKILL.md`
- Create: `sources/first_party/skills/using-git-worktrees/agents/openai.yaml`
- Create: `sources/first_party/skills/using-git-worktrees/scripts/new-worktree.ps1`
- Create: `sources/first_party/skills/using-git-worktrees/scripts/new-worktree.sh`
- Create: `sources/first_party/skills/using-git-worktrees/scripts/new_worktree.py`
- Create: `sources/first_party/skills/using-git-worktrees/scripts/remove-worktree.ps1`
- Create: `sources/first_party/skills/using-git-worktrees/scripts/remove-worktree.sh`
- Create: `sources/first_party/skills/using-git-worktrees/scripts/remove_worktree.py`
- Copy: `adapters/codex/superpowers-plus/using-git-worktrees/scripts/*` -> `sources/first_party/skills/using-git-worktrees/scripts/`

**Interfaces:**
- Produces: first-party `using-git-worktrees` source root.

- [x] **Step 1: Create `SKILL.md` and `agents/openai.yaml`.**

Use the canonical shapes. `name: using-git-worktrees`, `provenance-name: Using Git Worktrees first-party skill`.

- [x] **Step 2: Copy the adapter scripts.**

```powershell
New-Item -ItemType Directory -Path "sources/first_party/skills/using-git-worktrees/scripts" -Force
Get-ChildItem -Path "adapters/codex/superpowers-plus/using-git-worktrees/scripts" | Copy-Item -Destination "sources/first_party/skills/using-git-worktrees/scripts/"
```

- [x] **Step 3: Verify.**

```powershell
$expected = @("SKILL.md", "agents/openai.yaml", "scripts/new-worktree.ps1", "scripts/new-worktree.sh", "scripts/new_worktree.py", "scripts/remove-worktree.ps1", "scripts/remove-worktree.sh", "scripts/remove_worktree.py")
$expected | ForEach-Object { if (-not (Test-Path "sources/first_party/skills/using-git-worktrees/$_")) { throw "Missing $_" } }
git diff --check
git diff --stat
```

- [x] **Step 4: Commit.**

```powershell
git add sources/first_party/skills/using-git-worktrees
git commit -m "feat: migrate using-git-worktrees to first-party source"
```

---

### Task 5: Rename and migrate `using-superpowers` to `using-superpowers-plus`

**Files:**
- Create: `sources/first_party/skills/using-superpowers-plus/SKILL.md`
- Create: `sources/first_party/skills/using-superpowers-plus/agents/openai.yaml`
- Delete (after source is promoted): `adapters/codex/superpowers-plus/using-superpowers/`

**Interfaces:**
- Produces: first-party `using-superpowers-plus` source root.
- Consumes: the projected `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers/` content, with all `using-superpowers` references renamed.

- [x] **Step 1: Create `sources/first_party/skills/using-superpowers-plus/SKILL.md`.**

Use the canonical frontmatter with `name: using-superpowers-plus`, `provenance-name: Using Superpowers Plus first-party skill`, and `source-path: sources/first_party/skills/using-superpowers-plus/SKILL.md`. Copy the body from `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers/SKILL.md` (after its frontmatter), then replace every occurrence of `using-superpowers` with `using-superpowers-plus` and every `@using-superpowers` with `@using-superpowers-plus`. Prepend the provenance block with `original-skill-name` set to `using-superpowers`.

- [x] **Step 2: Create `sources/first_party/skills/using-superpowers-plus/agents/openai.yaml`.**

Use the canonical shape with `skill_name: using-superpowers-plus`, `display_name: Using Superpowers Plus`, `short_description` and `default_prompt` referencing `using-superpowers-plus`.

- [x] **Step 3: Verify.**

```powershell
$expected = @("SKILL.md", "agents/openai.yaml")
$expected | ForEach-Object { if (-not (Test-Path "sources/first_party/skills/using-superpowers-plus/$_")) { throw "Missing $_" } }
Select-String -Path "sources/first_party/skills/using-superpowers-plus/SKILL.md" -Pattern "using-superpowers" -SimpleMatch | ForEach-Object { throw "Un-renamed reference found: $($_.Line)" }
git diff --check
git diff --stat
```

- [x] **Step 4: Commit.**

```powershell
git add sources/first_party/skills/using-superpowers-plus
git commit -m "feat: promote using-superpowers as using-superpowers-plus first-party source"
```

---

### Task 6: Update first-party skill bodies that reference `@using-superpowers`

**Files:**
- Modify: `sources/first_party/skills/inspecting-the-environment/SKILL.md` (line 107)
- Any other `sources/first_party/skills/*/SKILL.md` that contain `@using-superpowers`

**Interfaces:**
- Consumes: the newly-created `using-superpowers-plus` skill.

- [x] **Step 1: Find all first-party references.**

```powershell
grep -R "@using-superpowers" sources/first_party
```

On Windows PowerShell without `grep`, use:

```powershell
Select-String -Path "sources/first_party/skills/*/SKILL.md" -Pattern "@using-superpowers" -SimpleMatch
```

- [x] **Step 2: Update `inspecting-the-environment/SKILL.md`.**

On line 107, change:

```markdown
Start with `@using-superpowers` as the workflow-selection entrypoint.
```

to:

```markdown
Start with `@using-superpowers-plus` as the workflow-selection entrypoint.
```

- [x] **Step 3: Update any other matches found in Step 1 using the same `@using-superpowers-plus` replacement.**

- [x] **Step 4: Verify.**

```powershell
grep -R "@using-superpowers" sources/first_party && throw "Unresolved @using-superpowers references remain"
```

or on PowerShell:

```powershell
if (Select-String -Path "sources/first_party/skills/*/SKILL.md" -Pattern "@using-superpowers" -SimpleMatch) { throw "Unresolved @using-superpowers references remain" }
git diff --check
git diff --stat
```

- [x] **Step 5: Commit.**

```powershell
git add sources/first_party/skills/inspecting-the-environment/SKILL.md
git commit -m "fix: update first-party references from @using-superpowers to @using-superpowers-plus"
```

---

### Task 7: Update `codex-marketplace/custody-pack-registry.json` for the `superpowers-plus` pack

**Files:**
- Modify: `codex-marketplace/custody-pack-registry.json`

**Interfaces:**
- Consumes: the new first-party source roots.
- Produces: registry entries that point projection at first-party `verbatim` custody.

- [x] **Step 1: Transform the 14 adapted entries to first-party `verbatim`.**

For each of these canonical names in the `superpowers-plus` pack:

`brainstorming`, `dispatching-parallel-agents`, `executing-plans`, `finishing-a-development-branch`, `receiving-code-review`, `requesting-code-review`, `subagent-driven-development`, `systematic-debugging`, `test-driven-development`, `using-git-worktrees`, `using-superpowers`, `verification-before-completion`, `writing-plans`, `writing-skills`.

Replace the entry with the following exact shape (example for `brainstorming`; substitute `<name>` and `<Skill Name>` for the others):

```json
{
  "canonical_name": "brainstorming",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/brainstorming",
  "local_path": "skills/brainstorming",
  "provenance_note": "First-party skill derived from the obra/superpowers v6.2.0 MIT upstream snapshot retained in third-party source custody.",
  "copy_expectation": "byte_identical"
}
```

For `using-superpowers` use `canonical_name: using-superpowers-plus`, `canonical_source_path: sources/first_party/skills/using-superpowers-plus`, and `local_path: skills/using-superpowers-plus`.

Remove the following obsolete fields from each of those 14 entries: `import_status`, `adaptation_overlay_path`, `adapted_author`, `adaptation_note`, `source_path`, `source_author`, `source_license`, `source_repo`. Keep `source_family` set to `first_party`.

- [x] **Step 2: Update the pack-level `notes`.**

Set the `superpowers-plus` pack `notes` array to:

```json
"notes": [
  "Superpowers+ is a first-party authored skill bundle. The upstream obra/superpowers v6.2.0 MIT snapshot is retained under sources/third_party/superpowers/ as reference."
]
```

- [x] **Step 3: Update the pack `source_ledger`.**

Replace the `superpowers-plus` pack `source_ledger` array with the list of all first-party source roots it projects:

```json
"source_ledger": [
  "sources/first_party/skills/brainstorming",
  "sources/first_party/skills/dispatching-parallel-agents",
  "sources/first_party/skills/executing-plans",
  "sources/first_party/skills/finishing-a-development-branch",
  "sources/first_party/skills/handoff-gates",
  "sources/first_party/skills/inspecting-the-environment",
  "sources/first_party/skills/receiving-code-review",
  "sources/first_party/skills/requesting-branch-review",
  "sources/first_party/skills/requesting-code-review",
  "sources/first_party/skills/selecting-a-subagent",
  "sources/first_party/skills/subagent-driven-development",
  "sources/first_party/skills/systematic-debugging",
  "sources/first_party/skills/test-driven-development",
  "sources/first_party/skills/using-git-worktrees",
  "sources/first_party/skills/using-superpowers-plus",
  "sources/first_party/skills/verification-before-completion",
  "sources/first_party/skills/working-with-epics",
  "sources/first_party/skills/writing-plans",
  "sources/first_party/skills/writing-skills"
]
```

- [x] **Step 4: Verify the registry is valid JSON and matches the intended entries.**

```powershell
py -3 -c "import json; json.load(open('codex-marketplace/custody-pack-registry.json'))"
git diff --check
git diff --stat
```

- [x] **Step 5: Commit.**

```powershell
git add codex-marketplace/custody-pack-registry.json
git commit -m "refactor: declare superpowers-plus skills as first-party verbatim in custody registry"
```

---

### Task 8: Update `provenance/superpowers-plus.md`

**Files:**
- Modify: `provenance/superpowers-plus.md`

**Interfaces:**
- Produces: provenance prose that reflects the first-party authorship model.

- [x] **Step 1: Rewrite the `Marketplace projection` section and pack statement.**

Replace the contents of `provenance/superpowers-plus.md` with:

```markdown
# Superpowers Provenance

## Source anchor

- Upstream repository: `https://github.com/obra/superpowers`
- Release tag: `v6.2.0`
- Release commit: `3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9`
- Tag object: `0e5cc50e782429b95f933e46443898435b8b37a8`
- License: MIT

## Custody

The upstream release snapshot is retained in third-party source custody at
`sources/third_party/superpowers/obra-superpowers/v6.2.0/`.

## Marketplace projection

The Codex-facing marketplace projection lives at
`codex-marketplace/plugins/superpowers-plus/`.

`superpowers-plus` is now a first-party authored skill bundle. The upstream
`obra/superpowers` v6.2.0 MIT snapshot is retained under
`sources/third_party/superpowers/` as immutable reference and provenance.

The bundle projects the first-party skills listed in
`codex-marketplace/custody-pack-registry.json` from their
`sources/first_party/skills/<name>/` roots into
`codex-marketplace/plugins/superpowers-plus/skills/<name>/`.

Do not place first-party expert or domain skills directly in the Superpowers
plugin that are not already justified as compositional workflow wrappers.
Keep the upstream license and attribution intact in every skill provenance
surface.

## Excluded from the active projection

- `.claude-plugin/`
- `.cursor-plugin/`
- `.opencode/`
- `gemini-extension.json`
- `CLAUDE.md`
- `GEMINI.md`
- `hooks/`

Those surfaces remain source evidence for the upstream package boundary and are
not part of the Codex install surface on this pass.
```

- [x] **Step 2: Verify.**

```powershell
if (-not (Test-Path "provenance/superpowers-plus.md")) { throw "File missing" }
git diff --check
git diff --stat
```

- [x] **Step 3: Commit.**

```powershell
git add provenance/superpowers-plus.md
git commit -m "docs: update superpowers-plus provenance for first-party authorship"
```

---

### Task 9: Remove the `adapters/codex/superpowers-plus/` overlay tree

**Files:**
- Delete: `adapters/codex/superpowers-plus/` and all children.

**Interfaces:**
- Consumes: the migrated adapter assets now live in `sources/first_party/skills/`.

- [x] **Step 1: Delete the tree.**

```powershell
Remove-Item -Recurse -Force "adapters/codex/superpowers-plus"
```

- [x] **Step 2: Verify nothing remains and `adapters/codex/` still houses other packs if needed.**

```powershell
if (Test-Path "adapters/codex/superpowers-plus") { throw "Overlay tree still present" }
git status --short
```

- [x] **Step 3: Commit.**

```powershell
git add adapters/codex/superpowers-plus
git commit -m "chore: retire superpowers-plus codex overlay tree"
```

---

### Task 10: Regenerate marketplace surfaces and run the CI gate

**Files:**
- Regenerate (do not hand-edit): `codex-marketplace/plugins/superpowers-plus/skills/`, `references/bundle-manifest.json`, `references/source-map.md`, `references/provenance-map.json`, `README.md`, `SOURCE.md`, `PROJECTION.md`.
- Regenerate: `provenance/first-party-skills.md`, `codex-marketplace/manifest.json`, `.agents/plugins/marketplace.json`, `repo-index/repo-index.json`.

**Interfaces:**
- Consumes: the updated first-party source roots and registry.
- Produces: the refreshed, deterministic marketplace projection.

- [ ] **Step 1: Regenerate all marketplace and index surfaces.**

```powershell
tools\run.ps1 marketplace --apply
```

- [ ] **Step 2: Stage the generated changes.**

```powershell
git add -A
git diff --check
git diff --cached --stat
```

- [ ] **Step 3: Commit the regenerated surfaces.**

```powershell
git commit -m "regenerate: marketplace and index surfaces for superpowers-plus first-party conversion"
```

- [ ] **Step 4: Run the CI gate.**

```powershell
tools\run.ps1 ci --check
```

Expected: PASS with no drift. If it fails, run `tools\run.ps1 marketplace --apply` again, commit any additional generated changes, and re-run `tools\run.ps1 ci --check`.

---

### Task 11 (Optional): Remove the overlay machinery from tooling

**Files:**
- Delete: `tools/skill_overlay_materializer.py`
- Delete: `tools/heal_overlays.py` and its `heal` target mapping in `tools/run` / `tools/run.ps1` / `tools/run.py`
- Modify: `tools/project_skills.py` to remove `adaptation_overlay_path` handling
- Modify: `tools/validate_marketplace.py` to remove overlay validation
- Modify: `tools/generate_pack_manifests.py` to remove `adaptation_overlay_path` support
- Modify: `adapters/AGENTS.md` to narrow its scope if `adapters/codex/` no longer holds active overlays

**Interfaces:**
- Consumes: confirmation that no remaining pack uses `adaptation_overlay_path` (the `feature-sliced-design` pack is already `verbatim` and `data-platform-pack` has no active overlays).

- [ ] **Step 1: Confirm no active overlays remain.**

```powershell
Select-String -Path "codex-marketplace/custody-pack-registry.json" -Pattern "adaptation_overlay_path" -SimpleMatch
```

If any matches remain, stop and update those packs first.

- [ ] **Step 2: Delete `tools/skill_overlay_materializer.py` and `tools/heal_overlays.py`.**

```powershell
Remove-Item -Force "tools/skill_overlay_materializer.py"
Remove-Item -Force "tools/heal_overlays.py"
```

- [ ] **Step 3: Remove `adaptation_overlay_path` and `content_mode: "adapted"` / `normalised` paths from `tools/project_skills.py`, `tools/validate_marketplace.py`, and `tools/generate_pack_manifests.py`.**

For each file, delete the overlay application, validation, and manifest-generation branches. Run `git diff --stat` after each file.

- [ ] **Step 4: Remove the `heal` target from the `tools/run` runner and `adapters/AGENTS.md` references to active overlays if no other pack uses adapters.**

- [ ] **Step 5: Regenerate and validate after tooling cleanup.**

```powershell
tools\run.ps1 marketplace --apply
git add -A
git commit -m "chore: remove overlay materializer and validation machinery"
tools\run.ps1 ci --check
```

---

## Plan Readiness (handoff-gates)

- [x] Spec coverage: every adapted skill, registry entry, provenance surface, downstream `@using-superpowers` reference, overlay tree removal, and regeneration step maps to a concrete task.
- [x] Placeholder scan: no `TBD`, `TODO`, or `fill in` strings; all file paths and frontmatter templates are explicit.
- [x] Task right-sizing: each task produces an independently verifiable commit.
- [x] Commands: `tools\run.ps1` Windows syntax used for all `tools/run` `--apply` / `--check` invocations.

**Execution confidence:** 9/10.