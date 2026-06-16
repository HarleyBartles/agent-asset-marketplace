# Source

This bundle packages the clean Adventures House Skills line as a
project-scoped Codex plugin.

## Canonical basis

- Canonical root: `codex-marketplace/plugins/house-skills/skills`
- Active projection lane: Adventures
- License posture: first-party Harley-owned source

## Source roots inspected

- `codex-marketplace/plugins/house-skills/skills/adventures-project-doctrine/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/adventures-bootstrap/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/adventures-github-operations/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/adventures-visual-preproduction/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/adventures-storyboard-preflight/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/adventures-visual-bible-creator/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/adventures-visual-bible-interpreter/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/adventures-image-qa/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/adventures-asset-sheet-compiler/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/adventures-frame-buster/SKILL.md`

## Generic dependencies

- `codex-marketplace/plugins/house-skills/skills/don-logan-boundary/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/base-doctrine/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/worker-dispatch-linear/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/connector-safety/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/linear/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/tps-reporting/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/tps-ingress/SKILL.md`

## Outcome

- Clean active Adventures skills projected: 10
- Generic dependencies projected: 7
- Historical v1 imports projected as active inventory: 0

## Bundle inventory

| Bundle | Decision | Reason |
| --- | --- | --- |
| `codex-marketplace/plugins/house-skills/` | included | This is the shared House Skills aggregate projection, and it now carries `connector-safety` as a base/control-plane safety component for side-effecting connector/tool work. |
| `codex-marketplace/plugins/adventures-pack/` | included | This is the existing project-scoped bundle that already composes side-effecting repo-work helpers, so `connector-safety` is useful and lawful here. |
| `harley-repo-ops` / cross-repo worker bundle | excluded | No existing repo convention or source/component mapping made a new curated cross-repo bundle boring for this issue. |
| other project-specific bundles | excluded | They were not required to make this issue useful, and the current scope did not justify inventing more bundle surfaces. |

## Notes

The bundle records the canonical source paths and versions in
`references/bundle-manifest.json` and the source map in
`references/source-map.md`.
