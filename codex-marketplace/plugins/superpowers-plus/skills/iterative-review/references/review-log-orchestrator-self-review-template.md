# Orchestrator self-review

## Inputs

- diff: `<diff_path>`
- pr_description: `<pr_description>`
- reviewer_profiles: the relevant `reviewer-*.md` files from the Devin Desktop agents search path

## Reviewed lens profiles

- [ ] `reviewer-security.md` (or the consumer repo's equivalent)
- [ ] `reviewer-skills.md` (or the consumer repo's equivalent)
- [ ] `reviewer-marketplace.md` (or the consumer repo's equivalent)
- [ ] `reviewer-strong.md` (or the consumer repo's equivalent)
- [ ] `reviewer-plans.md` (or the consumer repo's equivalent)
- [ ] `reviewer-mesh.md` (or the consumer repo's equivalent)
- [ ] `reviewer-scripts.md` (or the consumer repo's equivalent)

## Predicted and fixed

| Checklist item | Lens | Action | Rationale |
|---|---|---|---|
| | | | |

## Uncertain (send to lens)

| Checklist item | Lens | Why uncertain |
|---|---|---|
| | | |

## Next node

Proceed to `lens-dispatch` and dispatch the relevant lens reviewers. A clean prediction log does not bypass this node.

## Review artifacts

The orchestrator writes all review inputs and logs to the off-repo `iterative-review-<pr_number>` directory. The canonical file names are:

- `review-<base7>..<head7>.diff`
- `pr_description`
- `review-log-orchestrator-self-review.md`
- `review-log-<lens>.md`
- `review-metrics.json`

These files are never committed. They are the review proto-memory: later reviewers and the orchestrator read them to avoid re-deriving earlier work, to verify claimed fixes, and to detect regressions.

## Metrics snapshot

```json
{
  "orchestrator_self_review_findings_fixed": 0,
  "orchestrator_self_review_items_uncertain": 0
}
```
