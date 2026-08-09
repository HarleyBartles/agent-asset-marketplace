# Design: `using-deepwiki-mcp` skill

Date: 2026-08-09
Worktree: `Z:/_agent-worktrees/agent-asset-marketplace/using-deepwiki-mcp`

## Problem

The `deepwiki` MCP server provides AI-generated documentation and Q&A for public GitHub repositories. It has only three tools, but using it well requires judgment: when to ask a targeted question, when to list wiki topics, when to read the full (often very large) generated wiki, how to detect the current repo, how to compare up to 10 repos, and how to verify the generated answers against real source. Without guidance, agents either under-use DeepWiki or dump huge `read_wiki_contents` outputs into context.

## Goal

Create a `using-deepwiki-mcp` skill in `codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp/` that:

1. Teaches when and how to invoke the `deepwiki` MCP server, not just what each tool is called.
2. Provides a zero-friction current-repo flow: derive `owner/repo` from the local git remote when none is supplied.
3. Captures the multi-repo comparison capability in `ask_question` (`repoName` up to 10 repos).
4. Shows good and bad question patterns with concrete examples.
5. Includes a verification/fallback guide so agents do not treat generated docs as ground truth.

## Scope

- `SKILL.md` with frontmatter, when-to-use, current-repo flow, tool selection, multi-repo note, and trust section.
- `agents/openai.yaml` for pack metadata.
- `assets/icon.svg` — simple 24x24 search-over-document motif.
- `references/surface-map.md` — the three `deepwiki` tools and their schemas.
- `references/golden-questions.md` — good and bad questions with fixes.
- `references/current-repo-detection.md` — deriving `owner/repo` from git remotes.
- `references/multi-repo.md` — using `repoName` arrays for cross-repo questions.
- `references/verifying-against-source.md` — cross-checking generated answers with live source.
- Update `codex-marketplace/plugins/mcp-usage-pack/references/bundle-manifest.json` by running `py -3 tools/new_plugin.py --sync mcp-usage-pack`.

## Non-goals

- DeepWiki is read-only; there are no write or moderation concerns to cover.
- No non-MCP fallback surface is needed beyond "verify with the live repo" (GitHub, `git`, file reads).
- Do not install or configure the MCP server; the skill assumes it is already exposed.

## Design

### Current-repo flow

If the user does not name a repo, the agent runs `git remote -v` in the current checkout, picks `origin` (or `upstream` if the question is about upstream policy), and extracts `owner/repo`. The skill provides the exact regex/pattern. If the checkout is not a git repo or the remote cannot be parsed, the agent asks for `owner/repo` explicitly.

### Tool selection

| Situation | Tool |
|---|---|
| High-level "how do I...?" or cross-repo compare | `ask_question` |
| "What docs exist?" | `read_wiki_structure` |
| "I want the whole generated wiki" (large) | `read_wiki_contents` |

### Golden questions

The skill separates good questions (focused, verifiable) from bad ones (too specific for live files, asks for implementation, assumes live version data) and gives a better rephrasing for each.

### Multi-repo

`ask_question` accepts `repoName` as a string or an array of up to 10 `owner/repo` strings. The skill explains when to use an array and how to keep the question focused.

### Trust

DeepWiki answers include suggested wiki pages and a DeepWiki search URL. Critical facts must be verified with the live repo via `using-github-mcp`, `webfetch`, or file reads. `read_wiki_contents` output can be 10,000+ lines and should only be used intentionally.

## Source and custody

- First-party skill source lives in `codex-marketplace/plugins/mcp-usage-pack/skills/using-deepwiki-mcp/` (canonical product custody per `.agents/AGENTS.md`).
- `bundle-manifest.json` is a derived manifest; regenerate it with `tools/new_plugin.py --sync mcp-usage-pack`, then run `tools/run.py marketplace --apply`.
- Generated marketplace and installed-skill trees are downstream outputs; do not hand-edit.

## Validation

- `py -3 tools/new_plugin.py --sync mcp-usage-pack`
- `py -3 tools/run.py marketplace --apply`
- `py -3 tools/run.py ci --check`

## Handoff confidence

9/10 — the design is constrained to three tools, the MCP-usage pack pattern is well established, and the live MCP surface has already been explored.
