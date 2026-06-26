# Source

This bundle packages the clean Adventures first-party line as a
project-scoped Codex plugin.

## Canonical basis

- Canonical roots: `sources/first_party/skills/`
- Active projection lane: Adventures
- License posture: first-party Harley-owned source

## Source roots inspected

- `sources/first_party/skills/adventures-project-doctrine/SKILL.md`
- `sources/first_party/skills/adventures-bootstrap/SKILL.md`
- `sources/first_party/skills/adventures-github-operations/SKILL.md`
- `sources/first_party/skills/adventures-visual-preproduction/SKILL.md`
- `sources/first_party/skills/adventures-storyboard-preflight/SKILL.md`
- `sources/first_party/skills/adventures-visual-bible-creator/SKILL.md`
- `sources/first_party/skills/adventures-visual-bible-interpreter/SKILL.md`
- `sources/first_party/skills/adventures-image-qa/SKILL.md`
- `sources/first_party/skills/adventures-asset-sheet-compiler/SKILL.md`
- `sources/first_party/skills/adventures-frame-buster/SKILL.md`

## Generic dependencies

- `sources/first_party/skills/don-logan-boundary/SKILL.md`
- `sources/first_party/skills/base-doctrine/SKILL.md`
- `sources/first_party/skills/linear-issue-shaping/SKILL.md`
- `sources/first_party/skills/connector-safety/SKILL.md`
- `sources/first_party/skills/linear/SKILL.md`
- `sources/first_party/skills/tps-reporting/SKILL.md`
- `sources/first_party/skills/tps-ingress/SKILL.md`

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
