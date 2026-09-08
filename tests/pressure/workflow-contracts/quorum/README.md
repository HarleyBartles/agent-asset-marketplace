# MARK-373 Quorum exam

This is the behavioral exam for Task 7, expressed in the local Quorum harness
from `prime-radiant-inc/superpowers-evals`. The harness clone lives at the
repository root's ignored `evals/` directory; the exam itself is tracked here
so the campaign remains part of this repository's evidence contract.

The thirteen scenario directories map one-to-one to the scenarios in
`../campaign.json`. Each scenario has a fenced Gauntlet-Agent story, a
disposable fixture setup, and independent deterministic checks. The stories
grade judgment and authority; `checks.sh` corroborates observable skill calls,
files, and prohibited actions without exposing the rubric answer to the
subject.

## WSL and desktop ChatGPT auth

Run the wrapper from PowerShell. It converts this checkout and the Windows
profile's `.codex` directory to WSL paths, exports `CODEX_AUTH_HOME`, and then
executes Quorum inside WSL. Quorum copies the subscription `auth.json` into a
throwaway per-run home; no token is copied into this repository or passed as a
general environment variable.

```powershell
pwsh -File tests/pressure/workflow-contracts/quorum/run-mark373-quorum.ps1
```

The default action is static exam validation. A later live run must be an
explicit `-Run` invocation after the MARK-373 fail-closed preflight is green.
The current Quorum subscription credential uses the account-selected Codex
model; exact Luna/Terra/Sol/Astra model claims remain owned by the fixed
MARK-373 runner unless the harness gains a reviewed subscription model-threading
adapter.
