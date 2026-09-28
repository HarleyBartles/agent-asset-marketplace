# Repo-worker-base pressure scenarios

`campaign.json` is a reproducible prompt-and-rubric fixture for fresh-context evaluation of the repository-worker composition contract. It contains three combined-pressure scenarios, no-guidance controls, guided variants, an explicit RED/GREEN/REFACTOR evidence schema, and six micro-tests.

Run each variant in a fresh context and judge it against `expected_behavior`. Report the judgment in the current handoff; do not add responses, rollout identifiers, scores, or verdicts to this fixture. These are model behavior cases, not part of the repository commit gate.
