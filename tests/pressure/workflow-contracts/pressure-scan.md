# MARK-373 pressure scan classification

`pressure-scan.json` is the raw candidate output from
`tools/workflow_pressure_scan.py`. It contains 54 candidates. The raw scan is
not an automatic failure: every candidate has exactly one matching record in
`pressure-scan-dispositions.json`, with a classification, owner, and reason.

| classification | count | disposition |
|---|---:|---|
| `intended` | 12 | Deliberate operating-model contract retained as written. |
| `repo-local` | 42 | Repository-local runbook command or policy, owned by this repository's doctrine. |

No candidate is classified as `defect` or postponed. Each candidate identifies
the exact path, line, pattern, classification, owner, and reason in the
disposition artifact. Portable sources contain no hardcoded marketplace
command-bus instructions; repository-local runbooks retain their own command
surface under local doctrine.
