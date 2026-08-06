# using-playwright-mcp Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `using-playwright-mcp` skill to `mcp-usage-pack`, vendor the existing `using-discord-mcp` user skill into the same pack, rename `using-linear` to `using-linear-mcp`, and record the MCP-wrapper pattern in `.agents/runbooks/skill-authoring.md`.

**Actual executed scope (expanded):** The branch also codified pressure-testing standards in `.agents/doctrine/skill-standards-policy.md` and `tests/pressure/README.md`, cleaned up stale `intake.json`/`decisions.md` files in `mcp-usage-pack` and `repo-worker-pack`, fixed `sdd-workspace` canonical scratch resolution to `Z:\_agent-scratch`, and extracted a new `subagent-workspace` skill from `subagent-driven-development` so that both `subagent-driven-development` and `iterative-review` reference a single workspace source of truth.

**Architecture:** Follow the `using-linear` / `using-github-mcp` router-reference pattern. Each skill has a short `SKILL.md` with frontmatter, a router table, and use-case reference files. The `using-playwright-mcp` references are built from the `mcp-playwright` tool surface plus a `references/other-playwright-tools.md` soft-escape hatch.

**Tech Stack:** Markdown skill files, YAML `agents/openai.yaml` pack metadata, `py -3 tools/run.py` for validation.

## Global Constraints

- Source custody is `codex-marketplace/plugins/mcp-usage-pack/skills/<name>/`; do not hand-edit `.agents/skills/` installed surfaces.
- All new skills need `SKILL.md`, `agents/openai.yaml`, and a `references/` directory.
- Commit only the focused source changes; `py -3 tools/run.py marketplace --apply` regenerates downstream indexes and bundles.
- Do not run `git commit --no-verify`; the pre-commit hook runs `py -3 tools/run.py ci --check`.

---

### Task 1: Scaffold `using-playwright-mcp`

**Files:**
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/SKILL.md`
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/agents/openai.yaml`
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/references/surface-map.md`
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/references/navigation-and-discovery.md`
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/references/interactions.md`
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/references/inspection.md`
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/references/tabs-and-lifecycle.md`
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/references/other-playwright-tools.md`

**Step 1: Create `SKILL.md` with this content:**

```markdown
---
name: using-playwright-mcp
description: Use when working with the Playwright MCP server, choosing the right browser tool call, or falling back to non-MCP Playwright surfaces when the MCP does not cover the task.
metadata:
  source-id: using-playwright-mcp
  source-path: codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/SKILL.md
  provenance-name: Using Playwright MCP first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when working with the Playwright MCP server, choosing the right browser tool call, or falling back to non-MCP Playwright surfaces when the MCP does not cover the task.
  use_when:
  - Use when working with the Playwright MCP server, choosing the right browser tool call, or falling back to non-MCP Playwright surfaces when the MCP does not cover the task.
  do_not_use_when:
  - Do not use when another more specific skill owns the task.
  related_skills:
  - playwright-testing
license: MIT
---
# Using Playwright MCP

Use this skill to pick the right `mcp-playwright` tool for browser automation or web inspection, and to fall back safely to other Playwright surfaces when the MCP does not have what you need.

## Router

| Intent | Read first |
| --- | --- |
| Open a page, search for text, or capture a page snapshot | [`references/navigation-and-discovery.md`](references/navigation-and-discovery.md) |
| Click, type, hover, drag/drop, fill forms, select options, upload files, or handle dialogs | [`references/interactions.md`](references/interactions.md) |
| Evaluate JavaScript, read console, inspect network, or take screenshots | [`references/inspection.md`](references/inspection.md) |
| Manage tabs, resize, wait, or close the browser | [`references/tabs-and-lifecycle.md`](references/tabs-and-lifecycle.md) |
| The MCP does not cover the task; use another Playwright surface | [`references/other-playwright-tools.md`](references/other-playwright-tools.md) |
| Need the complete callable surface | [`references/surface-map.md`](references/surface-map.md) |

## Fast rules

1. **MCP first.** Start by routing to the use-case file that matches your intent.
2. **Confirm absence before exit.** Before opening `references/other-playwright-tools.md`, check `references/surface-map.md` or run `mcp_list_tools` for `mcp-playwright` to confirm the needed tool is not there.
3. **Environment check for fallbacks.** Before using a non-MCP Playwright tool, run `/inspecting-the-environment` to confirm it is installed and available.
```

**Step 2: Create `agents/openai.yaml` with this content:**

```yaml
version: 1
metadata:
  skill_name: using-playwright-mcp
  source_category: first_party
interface:
  display_name: Using Playwright MCP
  short_description: Route Playwright MCP work by intent and fall back safely to non-MCP surfaces.
  default_prompt: Use /using-playwright-mcp when working with the Playwright MCP server. Start with the MCP use-case file that matches the intent, and only use references/other-playwright-tools.md after confirming the MCP does not cover the task.
policy:
  products:
  - chatgpt
  - codex
  - api
  - atlas
  allow_implicit_invocation: true
```

**Step 3: Populate `references/surface-map.md` from `mcp-playwright` tools.**

Run `mcp_list_tools` for `mcp-playwright` and record all tool names in grouped lists: Navigate, Interact, Inspect, Tabs/Lifecycle, Console/Network/Advanced. Keep the file as a quick at-a-glance inventory; use the use-case files for guidance.

**Step 4: Populate the four MCP use-case reference files from the `mcp-playwright` tool list.**

For each tool, include a table: `Tool`, `Use when`, `Required params`, `Optional params`. Use the `using-linear` reference style. Use `mcp_list_tools` output or `https://glama.ai/mcp/servers/microsoft/playwright-mcp/schema` as the source of truth. Group tools as follows:

- `navigation-and-discovery.md`: `browser_navigate`, `browser_navigate_back`, `browser_find`, `browser_snapshot`
- `interactions.md`: `browser_click`, `browser_hover`, `browser_drag`, `browser_drop`, `browser_type`, `browser_press_key`, `browser_select_option`, `browser_fill_form`, `browser_file_upload`, `browser_handle_dialog`
- `inspection.md`: `browser_evaluate`, `browser_console_messages`, `browser_network_requests`, `browser_network_request`, `browser_take_screenshot`
- `tabs-and-lifecycle.md`: `browser_tabs`, `browser_resize`, `browser_wait_for`, `browser_close`

**Step 5: Create `references/other-playwright-tools.md` with this content:**

```markdown
# Other Playwright tools

Use this file only after you have confirmed the `mcp-playwright` server does not cover the task.

## Exit hatch hierarchy

1. **Human-visible preview** — Devin `browser_preview` and `close_browser_preview`. Use when the user needs to see or interact with a live page in their browser.
2. **Static raw page content** — `webfetch`. Use for pages that do not depend on JavaScript.
3. **Installed Playwright library / CLI** — `npx playwright` or project-local Playwright code. Use `/inspecting-the-environment` to verify Node, `npx`, and the project Playwright installation before running.
4. **Writing Playwright test suites** — the `playwright-testing` skill in `frontend-pack`.

## Confirmation rule

Before using any fallback, record why the MCP did not cover the task and the result of `/inspecting-the-environment` for the chosen tool.
```

**Step 6: Stage and commit with this command:**

```text
git add codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp
git commit -m "Add using-playwright-mcp skill"
```

---

### Task 2: Vendor `using-discord-mcp` into `mcp-usage-pack`

**Files:**
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-discord-mcp/SKILL.md`
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-discord-mcp/agents/openai.yaml`
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-discord-mcp/references/authed-tool-map.md`
- Create: `codex-marketplace/plugins/mcp-usage-pack/skills/using-discord-mcp/references/tool-map.md`

**Step 1: Copy `<devin-skills-dir>\using-discord-mcp` files (e.g. `%USERPROFILE%\AppData\Roaming\devin\skills\using-discord-mcp` on Windows or `~/.config/devin/skills/using-discord-mcp` elsewhere) into the new skill directory.**

**Step 2: Update the frontmatter in `SKILL.md` to first-party pack custody.**

Change `source-path`, `provenance-name`, and `source-category` to:

```yaml
  source-path: codex-marketplace/plugins/mcp-usage-pack/skills/using-discord-mcp/SKILL.md
  provenance-name: Using Discord MCP first-party skill
  source-category: first_party
```

**Step 3: Create `agents/openai.yaml`:**

```yaml
version: 1
metadata:
  skill_name: using-discord-mcp
  source_category: first_party
interface:
  display_name: Using Discord MCP
  short_description: Pick the right Discord MCP tool and stay inside the bot's current permissions.
  default_prompt: Use /using-discord-mcp when working with the Discord MCP server. Prefer references/authed-tool-map.md for read actions; ask the human partner before any write/moderation tool.
policy:
  products:
  - chatgpt
  - codex
  - api
  - atlas
  allow_implicit_invocation: true
```

**Step 4: Stage and commit:**

```text
git add codex-marketplace/plugins/mcp-usage-pack/skills/using-discord-mcp
git commit -m "Vendor using-discord-mcp into mcp-usage-pack"
```

---

### Task 3: Rename `using-linear` to `using-linear-mcp` and move it to `mcp-usage-pack`

**Files:**
- Move: `codex-marketplace/plugins/repo-worker-pack/skills/using-linear/` to `codex-marketplace/plugins/mcp-usage-pack/skills/using-linear-mcp/`
- Modify: `SKILL.md` frontmatter `name`, `source-path`, `source-id`
- Modify: `agents/openai.yaml`
- Delete: the old `using-playwright` scaffold if it still exists

**Step 1: Rename the directory and update source references:**

```text
git mv codex-marketplace/plugins/repo-worker-pack/skills/using-linear codex-marketplace/plugins/mcp-usage-pack/skills/using-linear-mcp
```

**Step 2: Update `SKILL.md` frontmatter so `name` is `using-linear-mcp`, `source-id` is `using-linear-mcp`, and `source-path` ends with `using-linear-mcp/SKILL.md`.**

**Step 3: Update `agents/openai.yaml` `skill_name` to `using-linear-mcp` and `display_name` to `Using Linear MCP`.**

**Step 4: Remove the empty `using-playwright` scaffold directory if it exists in the shared checkout:**

```text
rm -rf codex-marketplace/plugins/repo-worker-pack/skills/using-playwright
```

**Step 5: Stage and commit:**

```text
git add -A
git commit -m "Rename using-linear to using-linear-mcp"
```

---

### Task 4: Record the MCP wrapper pattern in `skill-authoring.md`

**Files:**
- Modify: `.agents/runbooks/skill-authoring.md`

**Step 1: Add the following section before `## Generated-surface commands`:**

```markdown
## MCP wrapper skill pattern

Skills that wrap a Model Context Protocol (MCP) server should follow this pattern. Examples include `using-linear-mcp`, `using-github-mcp`, `using-playwright-mcp`, and `using-discord-mcp`.

1. **MCP-first coverage.** The skill's primary job is to teach agents how to use the MCP server for the task. The `SKILL.md` begins with a use-case router, not an alphabetical tool list.
2. **Use-case reference files.** Create one reference file per intent (read, mutate, inspect, etc.), grouping tools by the job the agent is trying to do.
3. **Soft escape hatch.** Include a reference file or section that explains how to fall back to non-MCP tools that do the same job — REST API, Node library, CLI, or native Devin tools. This is not a license to skip the MCP; the agent must confirm the MCP cannot cover the task before leaving it.
4. **Environment confirmation.** Before using an installable or external fallback, run `/inspecting-the-environment` to verify the tool is present.
5. **Naming as guide, not rule.** `using-<x>-mcp` is a useful convention for this family, but the pattern does not require the name.
```

**Step 2: Stage and commit:**

```text
git add .agents/runbooks/skill-authoring.md
git commit -m "Record MCP wrapper skill pattern in skill-authoring runbook"
```

---

### Task 5: Regenerate marketplace and validate

**Step 1: Run marketplace regeneration:**

```text
py -3 tools/run.py marketplace --apply
```

**Step 2: Run CI check:**

```text
py -3 tools/run.py ci --check
```

**Step 3: If both pass, stage all regenerated artifacts and commit:**

```text
git add -A
git commit -m "Regenerate marketplace indexes"
```

---

### Task 6: Publication handoff

**Step 1: Push the `spec/using-playwright` branch:**

```text
git push -u origin spec/using-playwright
```

**Step 2: Create a draft PR into `main` with the branch name and head SHA in the body, per `.devin/rules/pr.md`.**

## Notes on executed scope

- Tasks 1-4 reflect the original MCP-pack work.
- The branch also carried: pressure-test policy (`.agents/doctrine/skill-standards-policy.md`, `tests/pressure/README.md`), `intake.json`/`decisions.md` cleanup in `mcp-usage-pack` and `repo-worker-pack`, `sdd-workspace` canonical scratch resolution, and `subagent-workspace` extraction.
- `subagent-workspace` is now the single source of truth for off-repo scratch resolution and owns the `sdd-workspace` scripts.

## Plan-readiness rating

9/10 — the design spec is concrete, the pattern and examples are explicit, and each task names exact files, commands, and commit messages.
