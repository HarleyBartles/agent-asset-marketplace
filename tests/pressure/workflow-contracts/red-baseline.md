# MARK-373 initial RED baseline

Command: `py -3 -m pytest tests/test_workflow_contracts.py -q`

Result at the start of Task 2: **15 failed, 7 passed**.

The failures are intentional and map to the owning tasks:

| failing area | owning task |
|---|---|
| missing `operating-contract.md`; bootstrap loads doctrine before classification; portable root assumptions | Task 3 |
| missing repository validation contract; message-bound verification; branch evidence reuse; transitive glue coverage | Task 4 |
| universal approval wording; recipient-relative plans; delegation/model separation | Task 5 |
| missing workflow inventory, CI parity, and classified pressure scan | Task 6 |
| committed score/raw-evidence schema expectation | Task 7 |

The seven passing tests cover the newly created campaign shape, runner argv
controls, preflight missing-harness classification, unobservable metrics, and
candidate-only scanner behavior. No live model trial was run.
