# MARK-373 Quorum exam

This is the behavioral exam for Task 7, expressed in the local Quorum harness
from `prime-radiant-inc/superpowers-evals`. The harness clone lives at the
repository root's ignored `evals/` directory; the exam itself is tracked here
so the campaign remains part of this repository's evidence contract.

The thirteen scenario directories map one-to-one to the scenarios in
`../campaign.json`. Each fixture copies the exact committed `.agents/skills`
tree into its disposable checkout and records both the marketplace evidence
head and a deterministic aggregate skill hash. Codex plugins stay disabled;
the composed skills are exercised as project-local assets rather than through
the remote plugin surface.

Each scenario has a fenced Gauntlet-Agent story, disposable setup, and
independent deterministic checks. The stories grade judgment and authority;
`checks.sh` corroborates observable skill calls, files, and prohibited actions
without exposing the rubric answer to the subject.

## WSL and OpenAI authentication

Run the wrapper from PowerShell with `OPENAI_API_KEY` present in the operator
environment. The wrapper projects that one named credential into WSL. The
tracked Quorum patch permits it in the isolated Gauntlet grader channel, where
the grader is pinned to GPT-5.4; Quorum's `openai_responses_56luna` credential
places it in the coding agent's private per-run credential file. No token enters
this repository or an unrelated child environment.

```powershell
pwsh -File tests/pressure/workflow-contracts/quorum/run-mark373-quorum.ps1
```

The default action is static exam validation. A later live run must be an
explicit `-Run` invocation. Before spending a model call, the wrapper requires
a clean immutable source tree and probes disposable Codex homes for empty MCP
and plugin inventories. It runs each selected scenario separately with
`--no-superpowers` and the declared `openai_responses_56luna` credential; each
scenario's `codex.config.toml` pins Luna-medium and disables plugins/apps. The
fixed MARK-373 runner remains the owner of the later Terra/Sol/Astra matrix.
