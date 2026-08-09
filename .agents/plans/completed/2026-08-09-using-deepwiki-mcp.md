# Using DeepWiki MCP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use /subagent-driven-development (recommended) or /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a `using-deepwiki-mcp` first-party skill in `codex-marketplace/plugins/mcp-usage-pack/` that teaches agents when and how to invoke the `deepwiki` MCP, with current-repo detection, multi-repo support, golden question examples, and source verification.

**Architecture:** Mirror the existing `using-<x>-mcp` skills in the `mcp-usage-pack` plugin: one `SKILL.md`, one `agents/openai.yaml`, one `assets/icon.svg`, and a `references/` directory with use-case and surface-map docs. No Python tooling changes are required; the skill is authored in Markdown and YAML and regenerated through the marketplace pipeline.

**Tech Stack:** Markdown, YAML, SVG, `tools/new_plugin.py --sync mcp-usage-pack`, `tools/run.py marketplace --apply`, `tools/run.py ci --check`.

## Global Constraints

- License is MIT; author is Harley Bartles; source category is `first_party`; content mode is `verbatim`.
- All canonical source files live in `codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp/`.
- Do not hand-edit generated surfaces (`codex-marketplace/plugins/mcp-usage-pack/.codex-plugin/`, `.agents/skills/using-deepwiki-mcp/`, etc.).
- Regenerate `bundle-manifest.json` with `py -3 tools/new_plugin.py --sync mcp-usage-pack` after creating the source directory.
- Run `py -3 tools/run.py marketplace --apply` and `py -3 tools/run.py ci --check` before committing.
- Open the final PR as a draft.

---

### Task 1: Create `SKILL.md`

**Files:**
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp/SKILL.md`

**Interfaces:**
- Consumes: none
- Produces: the main skill router and rules

- [ ] **Step 1: Write `SKILL.md`**

~~~markdown
---
name: using-deepwiki-mcp
description: Use when you need high-level orientation, conventions, architecture, or cross-repo context for a GitHub repo and need to choose the right DeepWiki MCP tool and question phrasing.
metadata:
  source-id: using-deepwiki-mcp
  source-path: codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp/SKILL.md
  provenance-name: Using DeepWiki MCP first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when you need high-level orientation, conventions, architecture, or cross-repo context for a GitHub repo and need to choose the right DeepWiki MCP tool and question phrasing.
  use_when:
  - Use when you need high-level orientation, conventions, architecture, or cross-repo context for a GitHub repo.
  - Use when you need to decide whether to ask a targeted question, list wiki topics, or read the full generated wiki.
  - Use when you want to compare or contrast up to 10 public repos.
  do_not_use_when:
  - Do not use when you need exact, current source or version-specific behavior.
  - Do not use when the repo is private, not indexed by DeepWiki, or the answer has safety/security implications without verification.
  - Do not use when another more specific skill owns the task.
license: MIT
---

# Using DeepWiki MCP

Use this skill to decide when and how to call the `deepwiki` MCP server for a GitHub repo, with good question phrasing, current-repo detection, multi-repo support, and safe verification.

## When to use

- You need a map of a repo's architecture, conventions, or release process.
- You want a high-level answer to "how do I...?" in the repo you're working in.
- You want to compare or contrast a few public repos.
- You are picking a repo to investigate.

## When not to use

- You need exact, current source or a guarantee of version-specific behavior.
- The repo is private or not indexed by DeepWiki.
- The answer has safety, security, or deployment implications — verify first.

## Current-repo flow

1. If the user doesn't specify a repo, derive `owner/repo` from the current git remote. See [`references/current-repo-detection.md`](references/current-repo-detection.md).
2. Call `read_wiki_structure` to orient yourself on the available topics.
3. Call `ask_question` for targeted specifics, or `read_wiki_contents` if you genuinely need the full generated wiki.

## Tool selection

| Situation | Tool | Read first |
|---|---|---|
| "How do I...?" / "What is...?" / compare | `ask_question` | [`references/golden-questions.md`](references/golden-questions.md) |
| "What docs exist for this repo?" | `read_wiki_structure` | [`references/surface-map.md`](references/surface-map.md) |
| "I want the whole generated wiki" | `read_wiki_contents` | [`references/surface-map.md`](references/surface-map.md) |
| Need the complete callable surface | — | [`references/surface-map.md`](references/surface-map.md) |

## Multi-repo questions

For up to 10 repos, pass `repoName` as an array of `owner/repo` strings to `ask_question`. See [`references/multi-repo.md`](references/multi-repo.md).

## Trust and verification

DeepWiki content is AI-generated from public source. `ask_question` returns a `result`, suggested wiki pages, and a DeepWiki search URL. Use them as starting points, then verify critical facts with the live repo. See [`references/verifying-against-source.md`](references/verifying-against-source.md).
~~~

- [ ] **Step 2: Verify the file was created and has no leading/trailing blank lines around the frontmatter delimiters**

---

### Task 2: Create `agents/openai.yaml`

**Files:**
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp/agents/openai.yaml`

**Interfaces:**
- Consumes: none
- Produces: pack metadata for Codex/ChatGPT loading

- [ ] **Step 1: Write `agents/openai.yaml`**

~~~yaml
version: 1
metadata:
  skill_name: using-deepwiki-mcp
  source_category: first_party
interface:
  display_name: Using DeepWiki MCP
  short_description: Decide when and how to query DeepWiki-generated documentation for a GitHub repo.
  default_prompt: Use /using-deepwiki-mcp when you need high-level orientation, conventions, or cross-repo context from the DeepWiki MCP. Start by detecting the current repo or confirming the owner/repo, then route to the right tool and verify critical facts.
policy:
  products:
  - chatgpt
  - codex
  - api
  - atlas
  allow_implicit_invocation: true
~~~

- [ ] **Step 2: Validate with `py -3 -c "import yaml; yaml.safe_load(open(...))"` if Python YAML is available, or visually confirm two-space indentation**

---

### Task 3: Create `assets/icon.svg`

**Files:**
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp/assets/icon.svg`

**Interfaces:**
- Consumes: none
- Produces: composer icon for the skill

- [ ] **Step 1: Write `assets/icon.svg`**

~~~svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="2" y="3" width="14" height="18" rx="2" fill="#4D4D4D"/>
<path d="M5 8h8M5 12h8M5 16h5" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
<circle cx="16" cy="15" r="4" stroke="#2E9EFF" stroke-width="2"/>
<path d="M19 18l3 3" stroke="#2E9EFF" stroke-width="2" stroke-linecap="round"/>
</svg>
~~~

- [ ] **Step 2: Open the file in a browser or image viewer to confirm it renders a document-with-search icon**

---

### Task 4: Create `references/surface-map.md`

**Files:**
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp/references/surface-map.md`

**Interfaces:**
- Consumes: none
- Produces: at-a-glance `deepwiki` tool inventory

- [ ] **Step 1: Write `references/surface-map.md`**

~~~markdown
# Surface map — DeepWiki MCP

| Tool | Use when | Required inputs | Optional inputs | Notes |
| --- | --- | --- | --- | --- |
| `ask_question` | Ask a natural-language question about one or more repos | `question`, `repoName` | — | `repoName` can be a string or an array of up to 10 `owner/repo` strings. |
| `read_wiki_structure` | List available wiki topics for a repo | `repoName` | — | One `owner/repo` only. |
| `read_wiki_contents` | Read the full generated wiki for a repo | `repoName` | — | Output can be very large; prefer `ask_question` or `read_wiki_structure` first. |

Always check the live `mcp_list_tools` output for the authoritative list and schemas; this map is a routing guide, not a schema dump.
~~~

---

### Task 5: Create `references/golden-questions.md`

**Files:**
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp/references/golden-questions.md`

**Interfaces:**
- Consumes: none
- Produces: question phrasing guidance

- [ ] **Step 1: Write `references/golden-questions.md`**

~~~markdown
# Golden questions for DeepWiki

## Good questions

These produce focused, verifiable answers:

- "What is the canonical build/test command for this repo?"
- "How are new skills added to this marketplace?"
- "What is the release process and versioning policy?"
- "How does this repo handle dependency injection?"
- "Compare the PR workflow in repo A and repo B."

## Bad questions and how to fix them

| Bad | Why it is bad | Better |
| --- | --- | --- |
| "What does this file do?" | DeepWiki is high-level; use a file read for a specific file. | "What is the role of the `src/scheduler` package?" |
| "Implement X for me." | DeepWiki answers questions; it does not generate code. | "What is the recommended pattern for adding a new scheduler task?" |
| "Is the latest version of Y compatible with Z?" | DeepWiki is not a live registry. | "What dependencies does this repo declare for Y?" |
| "Dump the full wiki." | Wastes context; use targeted questions. | "List the wiki topics for this repo first." |

## Follow-up pattern

After `ask_question`, the tool returns a `result` plus suggested wiki pages and a DeepWiki search URL. Use the suggested pages to refine the next question.
~~~

---

### Task 6: Create `references/current-repo-detection.md`

**Files:**
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp/references/current-repo-detection.md`

**Interfaces:**
- Consumes: none
- Produces: current repo derivation guide

- [ ] **Step 1: Write `references/current-repo-detection.md`**

~~~markdown
# Detecting the current repo for DeepWiki

When the user does not name a repo, derive `owner/repo` from the current git checkout.

1. Run `git remote -v`.
2. Pick `origin` unless the question is about upstream policy, then use `upstream`.
3. Convert the URL to `owner/repo`:
   - HTTPS: `https://github.com/owner/repo.git` → `owner/repo`
   - SSH: `git@github.com:owner/repo.git` → `owner/repo`
4. If the remote cannot be parsed, or the checkout is not a git repo, ask the user for `owner/repo` explicitly.

Use this derived value as the default `repoName` for `ask_question`, `read_wiki_structure`, and `read_wiki_contents`.
~~~

---

### Task 7: Create `references/multi-repo.md`

**Files:**
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp/references/multi-repo.md`

**Interfaces:**
- Consumes: none
- Produces: multi-repo comparison guidance

- [ ] **Step 1: Write `references/multi-repo.md`**

~~~markdown
# Multi-repo questions with DeepWiki

`ask_question` accepts `repoName` as a single string or an array of up to 10 `owner/repo` strings.

Use an array when:
- Comparing two or more public repos.
- Asking how a pattern in one repo maps to another.
- "How do repo A and repo B handle side effects?"

Keep the question focused on a single theme. Do not use more than 10 repos.

The response will synthesize across the repos and may cite specific source files or wiki topics for each.
~~~

---

### Task 8: Create `references/verifying-against-source.md`

**Files:**
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp/references/verifying-against-source.md`

**Interfaces:**
- Consumes: none
- Produces: trust/verification guide

- [ ] **Step 1: Write `references/verifying-against-source.md`**

~~~markdown
# Verifying DeepWiki answers

DeepWiki answers are AI-generated from public source. They can be stale, incomplete, or overconfident. Verify before acting on critical information.

1. Check the suggested wiki pages and the DeepWiki search URL returned by `ask_question`.
2. For code-level facts, open the actual file with `using-github-mcp`, `webfetch`, or a local file read.
3. For version or dependency facts, read `package.json`, `pyproject.toml`, or the equivalent in the actual repo.
4. For security or deployment decisions, confirm with live source or ask your human partner.

Do not treat DeepWiki output as ground truth for exact current behavior.
~~~

---

### Task 9: Regenerate marketplace manifests

**Files:**
- Modify (generated): `codex-marketplace/plugins/mcp-usage-pack/references/bundle-manifest.json`
- Modify (generated): `.agents/skills/INDEX.md`, `.agents/plugins/marketplace.json`, and related downstream indexes

**Interfaces:**
- Consumes: `codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp/` (created in Tasks 1-8)
- Produces: updated bundle and installed-skill surfaces

- [ ] **Step 1: Run the bundle manifest sync to add the new skill to `bundle-manifest.json`**

Run:

```bash
py -3 tools/new_plugin.py --sync mcp-usage-pack
```

Expected: `bundle-manifest.json` now contains an `using-deepwiki-mcp` entry with `canonical_name`, `source_category: first_party`, `content_mode: verbatim`, `source_family: first_party`, `canonical_source_path: codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp`, `local_path: skills/using-deepwiki-mcp`, `source_path: codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp/SKILL.md`, `copy_expectation: byte_identical`.

- [ ] **Step 2: Run the full marketplace regeneration to project the new skill into installed trees and pack surfaces**

Run:

```bash
py -3 tools/run.py marketplace --apply
```

Expected: no errors; the installed skill tree `.agents/skills/using-deepwiki-mcp/`, the pack `bundle-manifest.json`, the pack skills `INDEX.md` (`codex-marketplace/plugins/mcp-usage-pack/skills/INDEX.md`), the installed skills `INDEX.md` (`.agents/skills/INDEX.md`), and the installed skills `.provenance.json` (`.agents/skills/.provenance.json`) reflect the new skill. Plugin-level `.codex-plugin/` and `.agents/plugins/marketplace.json` are not changed by a new skill.

- [ ] **Step 3: Run the CI preflight to prove the marketplace state is consistent**

Run:

```bash
py -3 tools/run.py ci --check
```

Expected: passes. If it fails, do not commit. Fix the source skill and re-run from Task 9 Step 1.

---

### Task 10: Commit, push, and open a draft PR

**Files:**
- Modify: none (source files already created and generated outputs now in tree)

**Interfaces:**
- Consumes: all prior tasks
- Produces: GitHub-visible publication proof

- [ ] **Step 1: Stage all canonical source and required generated files**

```bash
git add codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp/
git add codex-marketplace/plugins/mcp-usage-pack/references/bundle-manifest.json
git add .agents/skills/using-deepwiki-mcp/
git add .agents/plugins/
git status --short
```

- [ ] **Step 2: Review `git status` output to ensure no unrelated files are staged**

- [ ] **Step 3: Commit with the standard provenance footer**

```bash
git commit -m "$(cat <<'EOF'
feat: add using-deepwiki-mcp skill to mcp-usage-pack.

Adds the DeepWiki MCP usage skill: current-repo detection,
multi-repo support, golden question examples, and verification.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>
EOF
)"
```

- [ ] **Step 4: Push the branch**

```bash
git push -u origin using-deepwiki-mcp
```

- [ ] **Step 5: Open a draft PR into `main`**

```bash
gh pr create --draft --title "Add using-deepwiki-mcp skill" --body "$(cat <<'EOF'
## Summary
- Adds `using-deepwiki-mcp` first-party skill to `mcp-usage-pack`.
- Includes `SKILL.md`, `agents/openai.yaml`, `assets/icon.svg`, and five reference files.
- Regenerates marketplace and installed-skill indexes.

#### Test plan
- [ ] `py -3 tools/run.py ci --check` passes
- [ ] `py -3 tools/run.py marketplace --apply` is clean
- [ ] Draft PR opened against `main`

Generated with [Devin](https://devin.ai)
EOF
)"
```

---

## Execution confidence and handoff

- **SDD confidence:** 9/10 — the skill is small, the `using-<x>-mcp` pattern is established, and the MCP surface has already been discovered.
- **Plan-readiness rating:** 9/10 — all file paths, exact contents, and validation commands are specified; no Python tooling changes are required.

**Execution handoff:** the plan is saved to `.agents/plans/completed/2026-08-09-using-deepwiki-mcp.md`. A fresh subagent or implementer can execute task-by-task from Task 1. The design spec is at `.agents/specs/completed/2026-08-09-using-deepwiki-mcp-design.md`.
