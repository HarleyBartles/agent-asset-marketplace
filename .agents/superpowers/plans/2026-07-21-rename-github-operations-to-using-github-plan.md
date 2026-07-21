# Rename github-operations to using-github implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename `github-operations` to `using-github`, restructure it as a router skill mirroring `using-linear`, update source references, regenerate marketplace projections, and publish the change.

**Architecture:** Move source custody from `sources/first_party/skills/github-operations` to `sources/first_party/skills/using-github`, replace the verification-heavy monolith with a top-level router `SKILL.md` and focused per-intent reference docs, update the `codex-marketplace/custody-pack-registry.json` and hand-maintained provenance notes, then run the canonical rebuild pipeline.

**Tech Stack:** Markdown, YAML, JSON, Python rebuild tooling (`py -3 tools/rebuild_marketplace.py`, `py -3 tools/check_marketplace.py`), `gh` CLI, GitHub MCP server.

## Global Constraints

- Edit only canonical source custody and hand-maintained provenance; never hand-edit generated projections, bundle manifests, source maps, provenance maps, zip artifacts, or installed `.agents/skills/` trees.
- Run the full canonical rebuild after source changes.
- Line endings in generated or hand-written text files must be LF (`newline="\n"` in Python; write files accordingly).
- Keep first-party skill frontmatter fields consistent: `name`, `description`, `metadata.source-id`, `metadata.source-path`, `metadata.provenance-name`, `metadata.source-category`, `metadata.status`, `metadata.owner`, `metadata.scope`, `metadata.use_when`, `metadata.do_not_use_when`, `license`.

## Task 1: Create `sources/first_party/skills/using-github/` skill root

**Files:**
- Create: `sources/first_party/skills/using-github/SKILL.md`
- Create: `sources/first_party/skills/using-github/agents/openai.yaml`
- Create: `sources/first_party/skills/using-github/intake.json`
- Create: `sources/first_party/skills/using-github/decisions.json`
- Create: `sources/first_party/skills/using-github/decisions.md`
- Create: `sources/first_party/skills/using-github/assets/icon.svg`
- Create: `sources/first_party/skills/using-github/references/read-discover.md`
- Create: `sources/first_party/skills/using-github/references/pull-requests.md`
- Create: `sources/first_party/skills/using-github/references/reviews.md`
- Create: `sources/first_party/skills/using-github/references/issues-comments.md`
- Create: `sources/first_party/skills/using-github/references/commits-branches.md`
- Create: `sources/first_party/skills/using-github/references/mutations.md`
- Create: `sources/first_party/skills/using-github/references/graphql.md`
- Create: `sources/first_party/skills/using-github/references/gh-cli.md`
- Create: `sources/first_party/skills/using-github/references/mcp-surface.md`
- Create: `sources/first_party/skills/using-github/references/surface-map.md`
- Copy and update: `sources/first_party/skills/using-github/assets/icon.svg` from the existing `github-operations` icon.

**Interfaces:**
- Produces: a complete first-party skill source tree for `using-github`.

- [ ] **Step 1: Write `SKILL.md` router**

```markdown
---
name: using-github
description: Use when choosing the right GitHub or Git surface for a task, picking
  between the GitHub MCP server, gh CLI, REST API, GraphQL, or plain git commands.
metadata:
  source-id: using-github
  source-path: sources/first_party/skills/using-github/SKILL.md
  provenance-name: Using GitHub first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when choosing the right GitHub or Git surface for a task, picking between
    the GitHub MCP server, gh CLI, REST API, GraphQL, or plain git commands.
  use_when:
  - Use when choosing the right GitHub or Git surface for a task, picking between the
    GitHub MCP server, gh CLI, REST API, GraphQL, or plain git commands.
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
license: MIT
---
# Using GitHub

Use this skill to pick the right GitHub or Git surface from the task intent, then open the matching reference.

## Router

| Intent | Read first |
| --- | --- |
| Search, list, or read repositories, files, commits, branches, tags, or releases | [`references/read-discover.md`](references/read-discover.md) |
| Create, update, merge, or review pull requests | [`references/pull-requests.md`](references/pull-requests.md) |
| Read or write PR reviews, review threads, and inline review comments | [`references/reviews.md`](references/reviews.md) |
| Read or write issues and issue/PR timeline comments | [`references/issues-comments.md`](references/issues-comments.md) |
| Work with commits, branches, tags, or low-level git refs | [`references/commits-branches.md`](references/commits-branches.md) |
| Create, update, or delete files, repositories, labels, or other mutations | [`references/mutations.md`](references/mutations.md) |
| Run a GitHub GraphQL query or mutation | [`references/graphql.md`](references/graphql.md) |
| Use the `gh` command-line interface | [`references/gh-cli.md`](references/gh-cli.md) |
| Pick the right GitHub MCP tool | [`references/mcp-surface.md`](references/mcp-surface.md) |
| Need the complete callable surface | [`references/surface-map.md`](references/surface-map.md) |

## Fast rule

If you need exact current repository state, prefer `gh api` or `gh api graphql`. If the intent is still unclear after the first pass, open `references/surface-map.md` and return to the use-case file that matches the object you are touching.
```

- [ ] **Step 2: Write `references/surface-map.md` inventory**

Create `sources/first_party/skills/using-github/references/surface-map.md` with:
- `## MCP server tools` grouped by toolset (`context`, `repos`, `issues`, `pull_requests`, `users`, `actions`, `code_security`, `dependabot`, `discussions`, `gists`, `git`, `labels`, `notifications`, `orgs`, `projects`, `secret_protection`, `security_advisories`, `stargazers`, `dynamic`, `copilot`, `copilot_spaces`, `github_support_docs_search`). List tool names and one-sentence descriptions.
- `## gh CLI` grouped by intent (`read`, `pr`, `issue`, `repo`, `release`, `workflow`, `api`, `auth`).
- `## REST API` grouped by endpoint family.
- `## GraphQL` grouped by common query/mutation patterns.
- `## Native git` grouped by intent.

- [ ] **Step 3: Write per-intent reference docs**

Create the remaining `references/*.md` files. Each file follows the `using-linear` pattern: a short intro, a `## Pick the tool` table (tool/command, use when, required params, optional params/notes), and a `## When to choose X vs Y` section.

- [ ] **Step 4: Write `agents/openai.yaml`, `intake.json`, `decisions.json`, `decisions.md`**

Mirror the existing `github-operations` files but with `using-github` names, source paths, and the new scope. Update `decisions.md` to record the rename from `github-operations`/`MARK-226` to `using-github`.

- [ ] **Step 5: Copy `assets/icon.svg`**

Copy `sources/first_party/skills/github-operations/assets/icon.svg` to `sources/first_party/skills/using-github/assets/icon.svg` unchanged.

## Task 2: Remove the old `github-operations` source root

**Files:**
- Delete: `sources/first_party/skills/github-operations/`

**Interfaces:**
- Consumes: Task 1 complete.

- [ ] **Step 1: `git rm -r sources/first_party/skills/github-operations`**

Run: `git -C "Z:\_agent-worktrees\agent-asset-marketplace\using-github-skill-rename-and-restructure" rm -r sources/first_party/skills/github-operations`

## Task 3: Update source references to `using-github`

**Files:**
- Modify: `codex-marketplace/custody-pack-registry.json`
- Modify: `sources/first_party/skills/repo-worker-base/SKILL.md`
- Modify: `sources/first_party/skills/house-skills/SKILL.md`
- Modify: `sources/first_party/skills/house-skills/intake.json`
- Modify: `sources/first_party/skills/bootstrap-router/SKILL.md`
- Modify: `sources/first_party/skills/inspecting-the-environment/SKILL.md`
- Modify: `sources/first_party/skills/risk-gates/references/gates/feedback-gate.md`
- Modify: `sources/first_party/skills/base-doctrine/references/report-hygiene.md`
- Modify: `sources/first_party/skills/wild-bunch-project-doctrine/references/skill-routing.md`
- Modify: `.agents/guides/pr-guide.md`
- Modify: `provenance/repo-worker-pack.md`
- Modify: `provenance/house-skills.md`
- Modify: `provenance/wild-bunch-project-pack.md`

**Interfaces:**
- Consumes: Task 1 and Task 2 complete.

- [ ] **Step 1: Update `codex-marketplace/custody-pack-registry.json`**

In the `repo-worker-pack` and `house-skills` bundle entries, change the `github-operations` entry to `using-github`:
- `canonical_name`: `using-github`
- `canonical_source_path`: `sources/first_party/skills/using-github`
- `local_path`: `skills/using-github`
- `provenance_note`: references `using-github`.

Also update the `source_ledger` array under `repo-worker-pack` from `sources/first_party/skills/github-operations` to `sources/first_party/skills/using-github`.

- [ ] **Step 2: Update skill source references**

Replace `github-operations` with `using-github` in the listed source files, preserving sentence meaning and link targets.

- [ ] **Step 3: Update provenance notes**

Replace `github-operations` with `using-github` and `sources/first_party/skills/github-operations` with `sources/first_party/skills/using-github` in the listed `provenance/*.md` files.

## Task 4: Normalize and rebuild marketplace projections

**Files:**
- Generated downstream surfaces updated by the rebuild pipeline.

**Interfaces:**
- Consumes: Tasks 1-3 complete.

- [ ] **Step 1: Run `py -3 tools/rebuild_marketplace.py`**

This regenerates plugin projections, bundle manifests, source maps, provenance maps, skill zips, installed skills, repo index, and index mesh.

- [ ] **Step 2: Run `py -3 tools/check_marketplace.py`**

Confirm no stale generated state remains.

- [ ] **Step 3: Run `py -3 tools/install_agent_skills.py --check`**

Confirm installed skills are current (or run `py -3 tools/install_agent_skills.py` if stale).

## Task 5: Commit and publish

**Files:**
- All changed source and generated files.

- [ ] **Step 1: Stage and commit**

Run:
```bash
git -C "Z:\_agent-worktrees\agent-asset-marketplace\using-github-skill-rename-and-restructure" add -A
git -C "Z:\_agent-worktrees\agent-asset-marketplace\using-github-skill-rename-and-restructure" commit -m "feat: rename github-operations to using-github and restructure as router"
```

- [ ] **Step 2: Push branch**

Run:
```bash
git -C "Z:\_agent-worktrees\agent-asset-marketplace\using-github-skill-rename-and-restructure" push origin using-github-skill-rename-and-restructure
```

- [ ] **Step 3: Create PR**

Use `gh pr create` with title "Rename github-operations to using-github" and a summary listing the rename, restructure, and validation steps.

## Verification

- [ ] `py -3 tools/rebuild_marketplace.py` passes.
- [ ] `py -3 tools/check_marketplace.py` passes.
- [ ] `py -3 tools/install_agent_skills.py --check` passes.
- [ ] `git diff --check` passes.
- [ ] `grep -R "github-operations" sources/first_party` returns only historical/archive contexts (none expected).
