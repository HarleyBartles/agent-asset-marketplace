# Source

This Codex marketplace plugin is the repo-canonical copy of the locally created
Repo Worker Base asset.

## Local source

- Local source path: `C:\Users\Harls\plugins\repo-worker-base`
- Source files:
  - `.codex-plugin/plugin.json`
  - `skills/repo-worker-base/SKILL.md`
  - `skills/repo-worker-base/agents/openai.yaml`

## Projected skills

- `boring-loop` projected from `sources/first_party/core/boring-loop`
- `connector-safety` projected from `sources/first_party/core/connector-safety`
- `github-operations` projected from `sources/first_party/core/github-operations`

## Source files

- `skills/boring-loop/SKILL.md`
- `skills/boring-loop/agents/openai.yaml`
- `skills/connector-safety/SKILL.md`
- `skills/connector-safety/agents/openai.yaml`
- `skills/github-operations/SKILL.md`
- `skills/github-operations/agents/openai.yaml`
- `skills/github-operations/assets/icon.svg`
- `skills/github-operations/references/source-route-posture.md`
- `skills/github-operations/references/pr-review-writes.md`
- `references/source-map.md`

## Scope

This asset is intentionally thin:

- fresh-main discipline before repo edits;
- branch-from-current-main workflow;
- validation and publication evidence;
- honest status reporting for repo-backed work;
- generic connector safety and GitHub proof helpers needed by workers.

It does not include project-specific doctrine for any particular repo.
The `boring-loop` skill is a projected first-party coordination skill for
keeping work small, honest, and routed to the right specialist.
The `connector-safety` and `github-operations` skills are projected as the
generic safety/proof helper surfaces that no longer need House Skills as the
install surface. Their canonical source roots live under
`sources/first_party/core/<skill>/`.
