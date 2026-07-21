# Review Guidelines

This file is the review entry point for `agent-asset-marketplace`. It contains first-class review concerns; for the full review methodology, see [`.agents/guides/code-review-guide.md`](.agents/guides/code-review-guide.md).

## Before you review

- Read root [`AGENTS.md`](./AGENTS.md) `## Publication proof for repo work`.
- Read [`.agents/docs/repo-guide-policy.md`](./.agents/docs/repo-guide-policy.md) for this repo's guide mappings.
- Invoke `/repo-guide-standard` and `/repo-worker-base`.

## First-class review concerns

- The requested change is backed by an approved design spec and implementation plan.
- The diff is limited to the stated scope; no unrelated refactoring or generated-surface hand-editing.
- Source custody is respected: first-party source is edited, generated projections are regenerated, and third-party source is untouched.
- Validation evidence is present and current: `py -3 tools/check_marketplace.py`, `py -3 tools/generate_index_mesh.py --check`, and any relevant tests.
- Publication proof is present: an open PR or authorized direct-main commit with head SHA.
- No secrets, credentials, or sensitive data are committed or logged.
- Generated artifacts are downstream outputs only; they are not used to bypass source review.

## Routing to skills

- For the full review methodology, read [`.agents/guides/code-review-guide.md`](.agents/guides/code-review-guide.md).
- To request review, invoke `/requesting-code-review`.
- For risk gates, invoke `/risk-gates`.
- For repo hygiene and publication boundaries, invoke `/repo-worker-base`.
