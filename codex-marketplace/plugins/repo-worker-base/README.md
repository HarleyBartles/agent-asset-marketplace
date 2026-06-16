# Repo Worker Base

This plugin packages the thin, first-party repo hygiene skill for Codex workers
in Harley's workspace.

## Contents

- one skill under `skills/repo-worker-base/`
- the projected `codex-repo-receipts` skill under `skills/codex-repo-receipts/`
- the projected `boring-loop` skill under `skills/boring-loop/`
- plugin metadata in `.codex-plugin/plugin.json`
- provenance note in `SOURCE.md`
- MIT license in `LICENSE`

## Source

The canonical source for this plugin was created locally at:

- `C:\Users\Harls\plugins\repo-worker-base`

The vendored copy in this repository keeps the plugin thin and scoped to
generic repo-worker behavior only.
`boring-loop` is projected from the canonical first-party source at
`sources/first_party/skills/boring-loop/` so repo-backed work can keep the
next move small, honest, and routed to the right specialist.
