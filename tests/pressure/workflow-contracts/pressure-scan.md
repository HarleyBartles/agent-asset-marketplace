# MARK-373 pressure scan classification

`pressure-scan.json` is the raw candidate output from
`tools/workflow_pressure_scan.py`. It contains 97 candidates. The raw scan is
not an automatic failure: every candidate has exactly one matching record in
`pressure-scan-dispositions.json`, with a classification, owner, and reason.

| classification | count | disposition |
|---|---:|---|
| `intended` | 12 | Deliberate operating-model contract retained as written. |
| `repo-local` | 42 | Repository-local runbook command or policy, owned by this repository's doctrine. |
| `deferred` | 43 | Portable command-syntax follow-up retained with an explicit owner and reason. |

No candidate is classified as `defect`. The deferred records are not silently
ignored: each identifies the exact path, line, pattern, `MARK-373 portability
follow-up` owner, and the command-slot abstraction still required before a
future portable-assets pass.
