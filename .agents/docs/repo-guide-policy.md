# Repo Guide Policy

This repo follows the `repo-guide-standard` skill. Invoke `/repo-guide-standard` before reading, creating, or updating any repo guide.

## Standard-to-local mapping

| Standard guide | Local path | Status |
|---|---|---|
| design-guide.md | `.agents/guides/design-guide.md` | exists |
| planning-guide.md | `.agents/guides/planning-guide.md` | exists |
| implementing-guide.md | `.agents/guides/implementing-guide.md` | exists |
| code-review-guide.md | `.agents/guides/code-review-guide.md` | exists |
| marketplace-generation-guide.md | `.agents/guides/marketplace-generation-guide.md` | exists |
| skill-authoring-guide.md | `.agents/guides/skill-authoring-guide.md` | exists |
| security-guide.md | `.agents/guides/security-guide.md` | to create |
| testing-guide.md | `.agents/guides/testing-guide.md` | to create |
| pr-guide.md | `.agents/guides/pr-guide.md` | to create |
| code-style-guide.md | `.agents/guides/code-style-guide.md` | to create |

## Additional repo-specific guides

- `marketplace-generation-guide.md` — because this repo is an asset marketplace.
- `skill-authoring-guide.md` — because this repo authors skills.

## Root contributor and review surfaces

- `REVIEW.md` is the review entry point. It contains first-class review concerns and routes to `.agents/guides/code-review-guide.md` for detailed review methodology and to `/requesting-code-review` for execution.
- `CONTRIBUTING.md` is the substantive contributor entry point. It routes to the design, planning, implementation, and review guides and to the relevant repo-worker-pack and Superpowers skills.

## Exceptions

None.
