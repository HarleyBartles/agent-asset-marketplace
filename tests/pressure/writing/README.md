# Writing pressure campaign

This campaign records three different evidence classes for MARK-371. It tests
instruction-following and boundary behaviour, not human authorship, universal
prose quality, or detector performance.

- `red.md` records the all-pass/inconclusive pre-skill baseline.
- `green-writing.md` and `green-style.md` record non-causal acceptance and
  regression evidence on unchanged scenarios whose baseline already passed.
- `blinded/` freezes a separate adversarial A/B campaign. Its workers see only
  `stimulus.md`; `hidden-rubric.md` remains judge-only. Task 4 does not run
  either arm. `campaign.json` predeclares the Task 5 route, metrics, and verdict
  thresholds.

Each fixture is synthetic or records its provenance limitation. No pressure
artifact contains a private author corpus.

The scenarios do not authorize detector evasion, authorship inference, or intentional degradation of prose.
