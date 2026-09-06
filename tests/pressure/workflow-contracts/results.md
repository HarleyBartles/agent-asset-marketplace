# MARK-373 workflow pressure results

The fixed composed-stack campaign completed 52/52 trials: 13 scenarios across
Luna, Terra, Sol, and Astra. The requested trial models were fixed to
`gpt-5.6-luna`, `gpt-5.6-terra`, `gpt-5.6-sol`, and `gpt-6-astra`, each at
medium reasoning effort. Post-hoc scoring was performed inline by the Luna
executor; no second judge invocation was made.

The first run completed 45 trials at evaluation head `cc7341e47` before the
Windows capture layer raised a UTF-8 decoding error. The harness was repaired
in `82132d817`, and the seven affected Astra trials were resumed there. The
repair is a harness-capability correction, not a model-unavailable result.

## Verdicts

| family | pass | fail | failure class for failed trials |
|---|---:|---:|---|
| Luna | 3 | 10 | harness-capability |
| Terra | 2 | 11 | harness-capability |
| Sol | 4 | 9 | harness-capability |
| Astra | 5 | 8 | harness-capability |
| **total** | **14** | **38** | **harness-capability** |

The passing cases are the traces whose requested boundary remained observable
despite the managed runtime: authorized Draft publication dry-run, destructive
stop/decision custody, selected repository-canon responses, selected evidence
reuse responses, and one explicit proportionate no-approval response. The
failed cases are execution-dependent scenarios where the runtime blocked the
required local inspection before the requested action could be evidenced.
Those failures are retained rather than treated as green. The traces generally
stopped without fabrication or external side effects.

## Observable limits

`reads_before_useful_action` is `unobservable` for every score because the
event stream does not prove that ordering. The CLI/API does not expose an
effective observed model, reasoning mode, or separate judge identity beyond
the fixed requested configuration, so those fields retain their explicit
`unobservable`/pinned-contract values. Mechanical question, tool-call,
verification, elapsed-time, and SHA-256 values live in the per-trial score
records.

Raw event streams remain local and ignored. This report links only durable score
records, whose schema and evidence hashes are checked by
`tests/test_workflow_contracts.py`:

`scores/<evaluation-head>/<family>/<scenario-id>.json`

The campaign definition and durable run metadata are
[`campaign.json`](campaign.json) and
[`campaign-meta.json`](campaign-meta.json). No raw local run is presented as a
published artifact.
