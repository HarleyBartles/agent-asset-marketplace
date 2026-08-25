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

## Closeout result

The blinded judge found material improvement on the declared behaviour rubric:
the treatment arm passed 2 of 3 trials versus 1 of 3 for control, and its median
observed pattern-family count fell from 2 to 1. One treatment trial also omitted
a required fact, so the intervention did not improve every output.

This is observational evidence, not a valid causal experiment. The evaluator
freeze was breached after outputs were produced, and the frozen deterministic
evaluator did not discriminate between arms. The complete chronology, runtime
configuration for every trial, blind judgments, hashes, and limitations are in
[`blinded/results.md`](blinded/results.md). The result supports only the practical
claim agreed for MARK-371: material improvement in desired behaviour in this
campaign. It does not establish universal prose quality or prove that the skill
caused the difference.

Each fixture is synthetic or records its provenance limitation. No pressure
artifact contains a private author corpus.

The scenarios do not authorize detector evasion, authorship inference, or intentional degradation of prose.
