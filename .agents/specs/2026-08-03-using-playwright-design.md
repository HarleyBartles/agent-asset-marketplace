# Design: `using-playwright-mcp` skill

Date: 2026-08-03
Worktree: `<worktree-path>`

## Problem

Agents need to choose the right Playwright surface for browser automation or web inspection. The `mcp-playwright` MCP server exposes a large tool set, but its names are not always obvious and some tasks (e.g., writing a Playwright test file, running `npx playwright`, or letting a human see a live page) are not covered by the MCP. Without guidance, agents either guess the wrong tool or leave the MCP lane too early.

## Goal

Create a `using-playwright-mcp` skill in `codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/` that:

1. Mirrors the `using-linear` pattern: a short `SKILL.md` router plus use-case reference files.
2. Teaches the `mcp-playwright` tool surface as the default.
3. Provides a controlled exit hatch to non-MCP Playwright tools when the MCP cannot cover the task.
4. Prevents early exit by requiring the agent to confirm the MCP does not have the needed tool before using other surfaces.

## Scope

- `SKILL.md` with frontmatter, router table, and fast rule.
- `references/surface-map.md` — complete at-a-glance `mcp-playwright` inventory by capability.
- Use-case reference files:
  - `references/navigation-and-discovery.md` — `browser_navigate`, `browser_navigate_back`, `browser_find`, `browser_snapshot`
  - `references/interactions.md` — `browser_click`, `browser_hover`, `browser_drag`, `browser_drop`, `browser_type`, `browser_press_key`, `browser_select_option`, `browser_fill_form`, `browser_file_upload`, `browser_handle_dialog`
  - `references/inspection.md` — `browser_evaluate`, `browser_console_messages`, `browser_network_requests`, `browser_network_request`, `browser_take_screenshot`
  - `references/tabs-and-lifecycle.md` — `browser_tabs`, `browser_resize`, `browser_wait_for`, `browser_close`
  - `references/other-playwright-tools.md` — non-MCP fallbacks: Devin `browser_preview`/`close_browser_preview`, `webfetch`, Playwright CLI/`npx` against an installed library, and the `playwright-testing` skill
- `agents/openai.yaml` for pack metadata.

## Non-goals

- Duplicate the `playwright-testing` skill (end-to-end test authoring).
- Cover MCP vision-mode or PDF/devtools-only capabilities in detail; list them but defer to future skills.
- Install or configure the MCP server; the skill assumes it is already exposed.

## Design

### Router

The `SKILL.md` router table maps common intents to the correct reference file, just like `using-linear`.

### Core behavior rules

1. **MCP first.** The agent must start by routing to an MCP use-case file.
2. **Confirm absence before exit.** Before leaving the MCP lane, the agent must check the surface map or run `mcp_list_tools` to confirm the needed tool is not there.
3. **Fallback hierarchy.** If the MCP does not cover the task, open `references/other-playwright-tools.md` and pick the cheapest matching surface:
   - Human-visible live preview → `browser_preview` / `close_browser_preview`
   - Static raw page content → `webfetch`
   - Installed library / local test script → `npx playwright` or project Playwright code
   - Playwright test authoring → `playwright-testing` skill
4. **Environment check for non-MCP tools.** Before using a non-MCP Playwright tool, run `/inspecting-the-environment` to confirm it is installed and available.

### Validation

- `py -3 tools/run.py ci --check`
- `py -3 tools/run.py marketplace --apply`

## Source and custody

- Source skill lives in `codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/` (canonical product custody per `.agents/AGENTS.md`).
- Generated mesh indexes are downstream outputs; do not hand-edit.

## Handoff confidence

9/10 — the design is small, the `using-linear` pattern is already established, and the MCP tool surface has been discovered.

## Pattern: MCP wrapper skills

This skill follows a reusable pattern for agent-facing MCP wrappers:

1. **Start with the MCP.** The skill's default and primary coverage is the MCP server tool surface.
2. **Use-case references.** Break the tool list into use-case files, not alphabetical lists. `SKILL.md` routes by intent.
3. **Soft escape hatch.** Include a reference file that teaches agents how to fall back to non-MCP tools that do the same job (REST API, Node library, CLI, native Devin tools), but only after confirming the MCP does not cover the task.
4. **Environment check.** Before using an installable fallback, run `/inspecting-the-environment` to confirm it is present.
5. **Naming convention as guide, not rule.** `using-<x>` is a useful convention but not a hard requirement; other names may fit.

Examples: `using-linear-mcp` (renamed from `using-linear`), `using-github-mcp`, and `using-playwright-mcp`.

This pattern should be recorded in `.agents/runbooks/skill-authoring.md` so future MCP-wrapper skills follow it consistently. As part of this work, the existing `using-linear` skill will be renamed `using-linear-mcp` to align with the convention.
