# Repo Guide Policy

This repo follows the `repo-standards` skill. Invoke `/using-superpowers-plus` first to route to the relevant stage skill, then invoke `/repo-standards` when the task touches repo shape, runbook layout, or scaffolds.

## Standard-to-local mapping

| Standard guide | Local path | Status |
|---|---|---|
| design.md | `.agents/runbooks/design.md` | required |
| planning.md | `.agents/runbooks/planning.md` | required |
| implementing.md | `.agents/runbooks/implementing.md` | required |
| code-review.md | `.agents/runbooks/code-review.md` | required |
| marketplace-generation.md | `.agents/runbooks/marketplace-generation.md` | exists |
| skill-authoring.md | `.agents/runbooks/skill-authoring.md` | exists |
| security.md | `.agents/runbooks/security.md` | exists |
| testing.md | `.agents/runbooks/testing.md` | exists |
| pr.md | `.agents/runbooks/pr.md` | required |
| code-style.md | `.agents/runbooks/code-style.md` | exists |

Root `AGENTS.md` is a router. The 12 canonical topics are covered by the union of root headings and the listed guides/routed surfaces.

## Additional repo-specific guides

- `marketplace-generation.md` — because this repo is an asset marketplace.
- `skill-authoring.md` — because this repo authors skills.

## Root contributor and review surfaces

- `REVIEW.md` is the review entry point. It contains first-class review concerns and routes to `.agents/runbooks/code-review.md` for detailed review methodology and to `/requesting-code-review` for execution.
- `CONTRIBUTING.md` is the substantive contributor entry point. It routes to the design, planning, implementation, and review guides and to the relevant repo-worker-pack and Superpowers skills.

## Exceptions

- `marketplace-source-submodule` — this repo is the marketplace source and does not vendor itself as a submodule.
- `ci-preflight-ps1` — removed; replaced by `tools/run ci --check`.
- `ci-preflight-sh` — removed; replaced by `tools/run ci --check`.
- `pre-commit-hook` — local hook now calls `tools/run ci --check`; repo-standards should not overwrite it.
