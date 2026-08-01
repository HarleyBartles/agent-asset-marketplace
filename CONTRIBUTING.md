# Contributing

This guide is the contributor entry point for `agent-asset-marketplace`. It routes to the stage guides and the relevant repo-worker-pack and Superpowers skills.

## Before you begin

- Read root [`AGENTS.md`](./AGENTS.md) for source-of-truth and publication rules.
- Read [`.agents/docs/repo-guide-policy.md`](./.agents/docs/repo-guide-policy.md) for this repo's mapping to the cross-repo runbook standard.
- Invoke `/using-superpowers-plus` to classify the request and route to the correct stage.
- The owning stage skill will tell you when to invoke `/repo-standards` (repo shape/runbook alignment) or `/repo-worker-base` (worktree, branch, validation, publication).

## Contributor workflow

1. **Start with `/using-superpowers-plus`** to classify the request and route to the correct stage.
2. **Design** — read [`.agents/runbooks/design.md`](./.agents/runbooks/design.md) and invoke `/brainstorming` to produce a spec.
3. **Planning** — read [`.agents/runbooks/planning.md`](./.agents/runbooks/planning.md) and invoke `/writing-plans` to produce an implementation plan.
4. **Implementation** — read [`.agents/runbooks/implementing.md`](./.agents/runbooks/implementing.md) and invoke `/executing-plans` or `/subagent-driven-development`.
5. **Review** — read [`REVIEW.md`](./REVIEW.md) and [`.agents/runbooks/code-review.md`](./.agents/runbooks/code-review.md), then invoke `/requesting-code-review`.

Always work in an isolated worktree. Local file changes are not repo completion; publish a PR or authorized direct-main commit before claiming done.

## Routing to skills

- `/using-superpowers-plus` for workflow classification.
- `/repo-worker-base` for worktree, branch, validation, and publication boundaries.
- `/repo-standards` for repo shape and runbook layout, when the stage skill requires it.
- Stage skills: `/brainstorming`, `/writing-plans`, `/executing-plans`, `/subagent-driven-development`, `/requesting-code-review`.
