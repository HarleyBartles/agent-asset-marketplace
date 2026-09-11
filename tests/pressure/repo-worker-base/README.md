# Repo-worker-base pressure scenarios

`campaign.json` is a reproducible prompt-and-rubric fixture for fresh-context
evaluation of the repository-worker composition contract. It contains three
combined-pressure scenarios, no-guidance controls, guided variants, an explicit
RED/GREEN/REFACTOR evidence schema, and six micro-tests.

Run each variant in a fresh context and judge it against `expected_behavior`.
Report the judgment in the current handoff; do not add responses, rollout
identifiers, scores, or verdicts to this fixture. The existing pytest workflow
validates structure and retrieval coverage:

~~~text
py -3 -m pytest tests/test_repo_worker_base_contract.py -q
~~~
