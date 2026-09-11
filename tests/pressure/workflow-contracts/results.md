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

## Temporary external Luna evaluation

Quorum was brought into ignored local storage as temporary external test
tooling; it is not part of this repository and no Quorum source, adapter,
scenario, result, or raw trace is committed.

The strongest retained observation was a native-WSL Luna run with 11 grader
passes and two failures, followed by targeted repair trials. One apparent
compaction pass was later contradicted by a same-head failure, so the honest
historical tally is 12 pass / 1 fail / 0 indeterminate, not 13/13. The remaining
failure was compaction continuity.

These observations are diagnostic rather than a reproducible final-head
baseline. The external launcher bypassed the Codex sandbox, and separate empty
MCP/plugin inventory probes did not prove that the evaluated process was
isolated. Raw output also contained credential material and token-shaped text,
so it remains uncommitted. Further paid evaluation stopped on human instruction
after grader credits were exhausted. Subsequent confidence comes from local
contract tests, the canonical hooked gate, and adversarial code review.
