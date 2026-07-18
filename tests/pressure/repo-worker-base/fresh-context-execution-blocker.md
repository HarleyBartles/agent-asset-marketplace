# Fresh-context pressure execution blocker

The repository contains the reproducible pressure campaign definition in
`campaign.json`, but this worktree could not execute the requested model-based
campaign.

## Attempts

1. A fresh, read-only `claude -p` process was started for the
   `local-green-publication-pressure` no-guidance control. It exited before a
   model response. `claude auth status` reported `loggedIn: false` and
   `authMethod: none`.
2. The installed Codex CLI was probed as an alternate fresh-context runner. Its
   executable returned `Access is denied` before producing a response.

No RED, guided GREEN, REFACTOR, or repeated micro-test model output is claimed.
`campaign.json` therefore keeps `runtime_results` empty and records these
availability attempts under `runtime_execution.runner_attempts`.

## Required continuation

With an authenticated fresh-context runner, execute every no-guidance control
and guided variant in independent contexts, repeat each micro-test variant at
least five times, record raw responses and rationalizations in the declared
RED/GREEN/REFACTOR evidence shape, and leave the campaign's results empty if
any run was not actually completed.
