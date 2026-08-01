# Contributing

This guide is the contributor entry point for `agent-asset-marketplace`. It routes to the stage guides and the relevant repo-worker-pack and Superpowers skills.

## Before you begin

- Read root [`AGENTS.md`](./AGENTS.md) for source-of-truth and publication rules.
- Read [`.agents/docs/repo-guide-policy.md`](./.agents/docs/repo-guide-policy.md) for this repo's mapping to the cross-repo guide standard.
- Invoke `/repo-standards` and `/repo-worker-base` before starting work.

## Contributor workflow

1. **Start with `/using-superpowers-plus`** to classify the request and route to the correct stage.
2. **Design** — read [`.agents/guides/design-guide.md`](./.agents/guides/design-guide.md) and invoke `/brainstorming` to produce a spec.
3. **Planning** — read [`.agents/guides/planning-guide.md`](./.agents/guides/planning-guide.md) and invoke `/writing-plans` to produce an implementation plan.
4. **Implementation** — read [`.agents/guides/implementing-guide.md`](./.agents/guides/implementing-guide.md) and invoke `/executing-plans` or `/subagent-driven-development`.
5. **Review** — read [`REVIEW.md`](./REVIEW.md) and [`.agents/guides/code-review-guide.md`](./.agents/guides/code-review-guide.md), then invoke `/requesting-code-review`.

Always work in an isolated worktree. Local file changes are not repo completion; publish a PR or authorized direct-main commit before claiming done.

## Routing to skills

- `/using-superpowers-plus` for workflow classification.
- `/repo-worker-base` for worktree, branch, validation, and publication boundaries.
- `/repo-standards` for guide layout and workflow order.
- Stage skills: `/brainstorming`, `/writing-plans`, `/executing-plans`, `/subagent-driven-development`, `/requesting-code-review`.
