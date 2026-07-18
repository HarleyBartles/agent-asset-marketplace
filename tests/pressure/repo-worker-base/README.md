# Repo-worker-base pressure scenarios

`campaign.json` is a reproducible prompt-and-rubric fixture for fresh-context
evaluation of the repository-worker composition contract. It contains three
combined-pressure scenarios, no-guidance controls, guided variants, an explicit
RED/GREEN/REFACTOR evidence schema, and six micro-tests.

The fixture contains no claimed runtime results. Evaluators append observed
results only after actual fresh-context runs; the checked-in `runtime_results`
array remains empty until such evidence is deliberately recorded. The existing
pytest workflow validates structure and retrieval coverage:

~~~text
py -3 -m pytest tests/test_repo_worker_base_contract.py -q
~~~
