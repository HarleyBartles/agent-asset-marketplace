# Repo Worker Base

This plugin packages the thin, first-party repo hygiene skill for Codex workers
in Harley's workspace and now carries the generic safety and GitHub proof
helpers needed to keep repo-backed work self-contained.

## Contents

- one skill under `skills/repo-worker-base/`
- the projected `boring-loop` skill under `skills/boring-loop/`
- the projected `connector-safety` skill under `skills/connector-safety/`
- the projected `github-operations` skill under `skills/github-operations/`
- plugin metadata in `.codex-plugin/plugin.json`
- provenance note in `SOURCE.md`
- canonical source mapping in `references/source-map.md`
- MIT license in `LICENSE`

## Source

The canonical source for this plugin was created locally at:

- `C:\Users\Harls\plugins\repo-worker-base`

The vendored copy in this repository keeps the plugin thin and scoped to
generic repo-worker behavior plus the generic safety/proof helpers that repo
work routinely needs.
`boring-loop` is a projected first-party coordination skill for keeping work
small, honest, and routed to the right specialist.
`connector-safety` is projected from `sources/first_party/skills/connector-safety/`
as the generic connector/tool safety surface.
`github-operations` is projected from `sources/first_party/skills/github-operations/`
as the generic GitHub proof surface.
