# Repo-worker-base pressure scenarios

`campaign.json` is a reproducible prompt-and-rubric fixture for fresh-context
evaluation of the repository-worker composition contract. It contains three
combined-pressure scenarios, no-guidance controls, guided variants, an explicit
RED/GREEN/REFACTOR evidence schema, and six micro-tests.

The fixture contains observed controller-orchestrated results from fresh Codex
subagent contexts: six scenario contexts (three no-guidance controls and three
guided variants) plus exactly five independent micro-test contexts. It does not
claim five-fold repetition or execution of the sixth fixture micro-test. The
supporting evidence report is
`fresh-context-pressure-results.md`; `campaign.json` preserves source rollout
filenames and raw response excerpts for audit. The existing pytest workflow
validates structure and retrieval coverage:

~~~text
py -3 -m pytest tests/test_repo_worker_base_contract.py -q
~~~
