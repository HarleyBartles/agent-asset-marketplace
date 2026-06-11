# Source

This bundle packages the clean Adventures v1.1 House Skills line as a
project-scoped Codex plugin.

## Canonical basis

- Canonical root: `gpt-skills/house-skills`
- Active projection lane: Adventures v1.1
- License posture: first-party Harley-owned source

## Source roots inspected

- `gpt-skills/house-skills/adventures-project-doctrine/SKILL.md`
- `gpt-skills/house-skills/adventures-bootstrap/SKILL.md`
- `gpt-skills/house-skills/adventures-github-operations/SKILL.md`
- `gpt-skills/house-skills/adventures-visual-preproduction/SKILL.md`
- `gpt-skills/house-skills/adventures-storyboard-preflight/SKILL.md`
- `gpt-skills/house-skills/adventures-visual-bible-creator/SKILL.md`
- `gpt-skills/house-skills/adventures-visual-bible-interpreter/SKILL.md`
- `gpt-skills/house-skills/adventures-image-qa/SKILL.md`
- `gpt-skills/house-skills/adventures-asset-sheet-compiler/SKILL.md`
- `gpt-skills/house-skills/adventures-frame-buster/SKILL.md`

## Generic dependencies

- `gpt-skills/house-skills/don-logan-boundary/SKILL.md`
- `gpt-skills/house-skills/gpt-base-doctrine/SKILL.md`
- `gpt-skills/house-skills/worker-dispatch-linear/SKILL.md`
- `gpt-skills/house-skills/connector-safety/SKILL.md`
- `gpt-skills/house-skills/linear/SKILL.md`
- `gpt-skills/house-skills/tps-reporting/SKILL.md`
- `gpt-skills/house-skills/tps-ingress/SKILL.md`

## Outcome

- Clean active Adventures v1.1 skills projected: 10
- Generic dependencies projected: 7
- Historical v1 imports projected as active inventory: 0

## Bundle inventory

| Bundle | Decision | Reason |
| --- | --- | --- |
| `plugins/house-skills/` | excluded from this PR | The House Skills aggregate is driven by `sources/house-skills/*`, and `connector-safety` is not currently part of that active source-ledger projection. Adding it there would require a separate source-ledger decision rather than a bundle-only edit. |
| `codex-marketplace/plugins/adventures-pack/` | included | This is the existing project-scoped bundle that already composes side-effecting repo-work helpers, so `connector-safety` is useful and lawful here. |
| `harley-repo-ops` / cross-repo worker bundle | excluded | No existing repo convention or source/component mapping made a new curated cross-repo bundle boring for this issue. |
| other project-specific bundles | excluded | They were not required to make this issue useful, and the current scope did not justify inventing more bundle surfaces. |

## Notes

The bundle records the canonical source paths and versions in
`references/bundle-manifest.json` and the source map in
`references/source-map.md`.
