# review-branch-diff retired

## Provenance

- **Retired:** 2026-08-04
- **Original source:** `~/.config/devin/skills/review-branch-diff/` (macOS/Linux) or `%APPDATA%\devin\skills\review-branch-diff\` (Windows)
- **New home:** Whole-branch diff review is performed by a `subagent_explore`-based reviewer or by invoking `/requesting-code-review` with the branch/PR diff review lane.
- **Reason:** The `review-branch-diff` skill was a local helper that ran entirely as the `branch-reviewer` subagent and could not gather an explicit branch and worktree on the main agent. The canonical branch diff review flow now uses the main agent to prepare the diff and dispatch a reviewer subagent.

## What changed

| Old path | New state |
| --- | --- |
| `~/.config/devin/skills/review-branch-diff/SKILL.md` (or `%APPDATA%\devin\skills\review-branch-diff\SKILL.md`) | deleted |
| `sources/first_party/skills/review-branch-diff/` | not in repo custody; confirmed absent |
| `codex-marketplace/plugins/*/skills/review-branch-diff/` | not projected; confirmed absent |
| `.agents/skills/review-branch-diff/` | not installed; confirmed absent |

## Routing updates

- Branch diff review is no longer a dedicated skill invocation.
- `/requesting-code-review` owns the branch/PR diff review lane.
- `subagent-driven-development` final whole-branch review uses `subagent_explore` or `/requesting-code-review`, not `/review-branch-diff`.
- `selecting-a-subagent` uses `reviewer-strong` for full branch/PR diff reviews.

## User-local deletion

- **Status:** deleted
- **Blocker (if any):** none

## Source of truth

Branch diff review behavior is now owned by `sources/first_party/skills/requesting-code-review/` and `sources/first_party/skills/subagent-driven-development/`.
