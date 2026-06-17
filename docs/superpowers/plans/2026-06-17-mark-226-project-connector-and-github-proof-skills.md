# Project Connector and GitHub Proof Skills Beyond House Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Project `connector-safety` and `github-operations` into `repo-worker-base` so the skills are available outside the House Skills mega-plugin and the marketplace registry reflects that projection.

**Architecture:** Keep the existing `repo-worker-base` plugin thin and first-party. Add canonical projection copies of the two House Skills sources under `codex-marketplace/plugins/repo-worker-base/skills/`, add a repo-worker-base bundle manifest and source map, and update the repo index generator so the new bundle manifest is surfaced consistently. Regenerate the skill zips and repository index from tooling rather than hand-editing generated outputs.

**Tech Stack:** PowerShell, Python 3, marketplace JSON/Markdown manifests, generated `skill.zip` artifacts.

---

### Task 1: Add the projected skill directories

**Files:**
- Create: `codex-marketplace/plugins/repo-worker-base/skills/connector-safety/SKILL.md`
- Create: `codex-marketplace/plugins/repo-worker-base/skills/connector-safety/agents/openai.yaml`
- Create: `codex-marketplace/plugins/repo-worker-base/skills/connector-safety/CHANGELOG.md`
- Create: `codex-marketplace/plugins/repo-worker-base/skills/github-operations/SKILL.md`
- Create: `codex-marketplace/plugins/repo-worker-base/skills/github-operations/agents/openai.yaml`
- Create: `codex-marketplace/plugins/repo-worker-base/skills/github-operations/assets/icon.svg`
- Create: `codex-marketplace/plugins/repo-worker-base/skills/github-operations/references/source-route-posture.md`
- Create: `codex-marketplace/plugins/repo-worker-base/skills/github-operations/references/pr-review-writes.md`
- Modify: `codex-marketplace/plugins/repo-worker-base/SOURCE.md`
- Modify: `codex-marketplace/plugins/repo-worker-base/README.md`
- Modify: `provenance/repo-worker-base.md`

- [ ] **Step 1: Copy the House Skills source into the new repo-worker-base projection paths**

Use the current House Skills files as the source of truth for the projected skill content:

```powershell
Get-Content codex-marketplace/plugins/house-skills/skills/connector-safety/SKILL.md
Get-Content codex-marketplace/plugins/house-skills/skills/connector-safety/agents/openai.yaml
Get-Content codex-marketplace/plugins/house-skills/skills/connector-safety/CHANGELOG.md
Get-Content codex-marketplace/plugins/house-skills/skills/github-operations/SKILL.md
Get-Content codex-marketplace/plugins/house-skills/skills/github-operations/agents/openai.yaml
Get-Content codex-marketplace/plugins/house-skills/skills/github-operations/assets/icon.svg
Get-Content codex-marketplace/plugins/house-skills/skills/github-operations/references/source-route-posture.md
Get-Content codex-marketplace/plugins/house-skills/skills/github-operations/references/pr-review-writes.md
```

- [ ] **Step 2: Update repo-worker-base surface docs**

Make `README.md`, `SOURCE.md`, and `provenance/repo-worker-base.md` explicitly list the new projected skills and describe the repo-worker-base bundle as the canonical non-House-Skills home for repo hygiene and GitHub proof.

- [ ] **Step 3: Verify the new tree shape**

Run:

```powershell
rg --files codex-marketplace/plugins/repo-worker-base
```

Expected: the new `connector-safety` and `github-operations` directories appear under `skills/` with the copied source files.

### Task 2: Add repo-worker-base bundle inventory and source mapping

**Files:**
- Create: `codex-marketplace/plugins/repo-worker-base/references/bundle-manifest.json`
- Create: `codex-marketplace/plugins/repo-worker-base/references/source-map.md`

- [ ] **Step 1: Add the bundle manifest entries**

Record the canonical source paths and local projection paths for:

```json
{
  "canonical_name": "connector-safety",
  "source_path": "codex-marketplace/plugins/house-skills/skills/connector-safety/SKILL.md",
  "local_path": "skills/connector-safety/SKILL.md"
}
```

and

```json
{
  "canonical_name": "github-operations",
  "source_path": "codex-marketplace/plugins/house-skills/skills/github-operations/SKILL.md",
  "local_path": "skills/github-operations/SKILL.md"
}
```

- [ ] **Step 2: Add the human-readable source map**

Summarize the same mapping in Markdown and note that `repo-worker-base` already owns repo hygiene plus `codex-repo-receipts` and `boring-loop`.

- [ ] **Step 3: Re-run repo index generation after the manifest is in place**

The generator update in Task 3 depends on this file existing.

### Task 3: Wire the new bundle into the repo index and generated artifacts

**Files:**
- Modify: `tools/generate_repo_index.py`
- Modify: `repo-index/repo-index.json`
- Modify: `generated/skill-zips/registry.json`
- Generate: `generated/skill-zips/repo-worker-base/connector-safety/skill.zip`
- Generate: `generated/skill-zips/repo-worker-base/github-operations/skill.zip`

- [ ] **Step 1: Teach the repo index generator about the bundle manifest**

Set the `repo-worker-base` entry to point at `codex-marketplace/plugins/repo-worker-base/references/bundle-manifest.json`.

- [ ] **Step 2: Regenerate the repo index**

Run:

```powershell
py -3 tools/generate_repo_index.py
```

Expected: `repo-index/repo-index.json` updates and the `repo-worker-base` entry now includes the bundle manifest path.

- [ ] **Step 3: Regenerate the affected skill zips**

Run:

```powershell
py -3 tools/update_skill_artifacts.py --skill repo-worker-base/connector-safety
py -3 tools/update_skill_artifacts.py --skill repo-worker-base/github-operations
```

Expected: the two new `generated/skill-zips/repo-worker-base/.../skill.zip` artifacts appear and `generated/skill-zips/registry.json` gains matching entries.

### Task 4: Validate and publish

**Files:**
- None new; verify the edited surfaces

- [ ] **Step 1: Validate the marketplace and generated drift**

Run:

```powershell
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/validate_generated_drift.py --base origin/main
git diff --check HEAD~1 HEAD
```

Expected: all commands pass.

- [ ] **Step 2: Commit, push, and open the PR**

Commit the projection and index updates on the branch, push it, and open a GitHub PR into `main`.
