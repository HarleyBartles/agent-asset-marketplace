# Repo Guide Policy

This repo follows the `repo-standards` skill. Invoke `/repo-standards` before reading, creating, or updating any repo guide.

## Standard-to-local mapping

| Standard guide | Local path | Status |
|---|---|---|
| design-guide.md | `.agents/guides/design-guide.md` | required |
| planning-guide.md | `.agents/guides/planning-guide.md` | required |
| implementing-guide.md | `.agents/guides/implementing-guide.md` | required |
| code-review-guide.md | `.agents/guides/code-review-guide.md` | required |
| marketplace-generation-guide.md | `.agents/guides/marketplace-generation-guide.md` | exists |
| skill-authoring-guide.md | `.agents/guides/skill-authoring-guide.md` | exists |
| security-guide.md | `.agents/guides/security-guide.md` | exists |
| testing-guide.md | `.agents/guides/testing-guide.md` | exists |
| pr-guide.md | `.agents/guides/pr-guide.md` | required |
| code-style-guide.md | `.agents/guides/code-style-guide.md` | exists |

Root `AGENTS.md` is a router. The 12 canonical topics are covered by the union of root headings and the listed guides/routed surfaces.

## Additional repo-specific guides

- `marketplace-generation-guide.md` — because this repo is an asset marketplace.
- `skill-authoring-guide.md` — because this repo authors skills.

## Root contributor and review surfaces

- `REVIEW.md` is the review entry point. It contains first-class review concerns and routes to `.agents/guides/code-review-guide.md` for detailed review methodology and to `/requesting-code-review` for execution.
- `CONTRIBUTING.md` is the substantive contributor entry point. It routes to the design, planning, implementation, and review guides and to the relevant repo-worker-pack and Superpowers skills.

## Exceptions

- `marketplace-source-submodule` — this repo is the marketplace source and does not vendor itself as a submodule.
- `ci-preflight-sh` — replaced by the `tools/run` bash wrapper.
- `ci-preflight-ps1` — replaced by the `tools/run.ps1` PowerShell wrapper.
- `pre-commit-hook` — this worktree's pre-commit hook is wired to `tools/run ci --check` instead of the repo-standards template.
