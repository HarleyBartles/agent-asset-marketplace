# MARK-373 workflow pressure results

The revised campaign preflight is `harness-blocked` at evaluation head
`8f6280aa5dad59b33124f50af37b7f7150ea2afa`. Codex CLI `0.153.4` accepted the
required executable and flag checks, but the effective MCP inventory was
non-empty. The runner therefore stopped before the read-only Luna smoke,
model classification, and matrix rerun.

The 52 retained score records are historical traces from earlier heads. They
remain useful diagnostic artifacts, but are explicitly superseded and must not
be presented as a valid post-preflight behavioral baseline. Their prior 14
pass / 38 `harness-capability` verdicts are not completion evidence for the
revised campaign.

The preflight ran from a disposable worktree resolved to the requested head;
the recorded `preflight_head` matches the evaluation head and the worktree was
clean before inventory inspection.

## Revised campaign status

| field | value |
|---|---|
| preflight | `harness-blocked` |
| completed trials | `0` |
| retained diagnostic traces | `52` |
| model-unavailable verdicts | `0` — no trial reached model availability classification |
| external-tool evidence | MCP inventory output recorded in `campaign-meta.json` with SHA-256 |
| smoke evidence | not run because MCP/plugin isolation was not proven |
| raw run custody | ignored and local-only |

The blocking condition is environmental/harness capability, not a model
behavior verdict. A future run may establish a behavioral baseline only after
the same controlled read-only smoke completes successfully.
