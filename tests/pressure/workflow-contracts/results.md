# MARK-373 workflow pressure results

The revised campaign preflight is `harness-blocked` at evaluation head
`6cdcabce6e5ffbc88a6f51a528705b8a75473e67`. Codex CLI `0.153.4` accepted the
required executable and flag checks, but a real read-only Luna smoke invocation
exited 0 without producing the required `SMOKE_OK` response. The runner
therefore stopped before model classification and did not rerun the matrix.

The 52 retained score records are historical traces from earlier heads. They
remain useful diagnostic artifacts, but are explicitly superseded and must not
be presented as a valid post-preflight behavioral baseline. Their prior 14
pass / 38 `harness-capability` verdicts are not completion evidence for the
revised campaign.

The preflight ran from a disposable worktree resolved to the requested head;
the recorded `preflight_head` matches the evaluation head and the worktree was
clean before the smoke.

## Revised campaign status

| field | value |
|---|---|
| preflight | `harness-blocked` |
| completed trials | `0` |
| retained diagnostic traces | `52` |
| model-unavailable verdicts | `0` — no trial reached model availability classification |
| smoke evidence | recorded in `campaign-meta.json` with SHA-256 |
| raw run custody | ignored and local-only |

The blocking condition is environmental/harness capability, not a model
behavior verdict. A future run may establish a behavioral baseline only after
the same controlled read-only smoke completes successfully.
