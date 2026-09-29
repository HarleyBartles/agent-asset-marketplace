---
name: using-github-mcp
description: Use when choosing the right GitHub or Git surface for a task, picking between the GitHub MCP server, gh CLI, REST API, GraphQL, or plain git commands.
metadata:
  source-id: using-github-mcp
  source-path: skills/using-github-mcp/SKILL.md
  provenance-name: Using GitHub MCP first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  use_when:
    - choosing the right GitHub or Git surface for a task, picking between the GitHub MCP server, gh CLI, REST API, GraphQL, or plain git commands.
  do_not_use_when:
    - another more specific skill owns this task.
license: MIT
---

# Using GitHub MCP

Use this skill to pick the right GitHub or Git surface from the task intent, then open the matching reference.

## Runtime availability

Inspect the tools exposed in the current runtime before choosing MCP. This guidance is available independently of repository subscriptions. If a needed MCP operation is absent, use the documented `gh`, REST, GraphQL, or Git alternative only when that surface is available and suitable; otherwise report the missing capability and stop the dependent action.

## Router

| Intent                                                                          | Read first                                                         |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Search, list, or read repositories, files, commits, branches, tags, or releases | [`references/read-discover.md`](references/read-discover.md)       |
| Create, update, merge, or review pull requests                                  | [`references/pull-requests.md`](references/pull-requests.md)       |
| Read or write PR reviews, review threads, and inline review comments            | [`references/reviews.md`](references/reviews.md)                   |
| Read or write issues and issue/PR timeline comments                             | [`references/issues-comments.md`](references/issues-comments.md)   |
| Work with commits, branches, tags, or low-level git refs                        | [`references/commits-branches.md`](references/commits-branches.md) |
| Create, update, or delete files, repositories, labels, or other mutations       | [`references/mutations.md`](references/mutations.md)               |
| Run a GitHub GraphQL query or mutation                                          | [`references/graphql.md`](references/graphql.md)                   |
| Use the `gh` command-line interface                                             | [`references/gh-cli.md`](references/gh-cli.md)                     |
| Pick the right GitHub MCP tool                                                  | [`references/mcp-surface.md`](references/mcp-surface.md)           |
| Need the complete callable surface                                              | [`references/surface-map.md`](references/surface-map.md)           |

## Fast rule

If you need exact current repository state, prefer `gh api` or `gh api graphql`. If the intent is still unclear after the first pass, open `references/surface-map.md` and return to the use-case file that matches the object you are touching.

Before changing a PR's draft state, discover and follow the consuming repository's declared PR policy at its own path. If no applicable local policy is declared, use the portable policy in the pull-request guidance.
