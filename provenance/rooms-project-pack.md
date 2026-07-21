# Rooms Project Pack Provenance

## Source anchor

- First-party source custody: `sources/first_party/skills/`
- License: MIT

## Custody surface

- First-party Rooms skill custody: `sources/first_party/skills/rooms-*`
- First-party database guidance skill custody:
  `sources/first_party/skills/database-design-patterns`

## Projection surface

- Installable plugin projection: `codex-marketplace/plugins/rooms-project-pack/`
- Generated install units: `generated/skill-zips/rooms-project-pack/<skill-name>/skill.zip`

## Keep / Skip Matrix

| Skill | Include in `rooms-project-pack` | Source bundle | Why |
| -- | -- | -- | -- |
| `rooms-project-doctrine` | Yes | House Skills / Rooms | Shared Rooms doctrine and truth-boundary routing. |
| `rooms-risk-gates` | Yes | House Skills / Rooms | Rooms-specific canon, analogy, ambiguity, zoom-outs, and invariant gate profiles. |
| `rooms-character-investigation` | Yes | House Skills / Rooms | Broad Rooms lookup and source-partitioned investigation packets. |
| `rooms-sheet-creator` | Yes | House Skills / Rooms | Turns durable investigations into participant-facing sheets. |
| `rooms-image-sidecars` | Yes | House Skills / Rooms | Useful for image evidence starter packets before Pit/archive ingestion. |
| `database-design-patterns` | Yes | First-party | Relevant because this repo has a canonical sqlite database surface and needs generic schema/query guidance without taking a full architecture bundle. |
| `cleanup-custody` | No | repo-worker-pack | Already the right home for repo hygiene and cleanup-custody. |
| `repo-worker-pack` | No | Separate plugin | Keeps repo hygiene and worker routing separate from the Rooms pack. |
| `superpowers-plus` | No | Separate plugin | General workflow/process skills; not Rooms-project-pack material. |
| `unslop-plus` | No | Separate plugin | Anti-slop profiles should stay in their dedicated pack. |
| `architecture-pack` | No | Separate plugin | Too broad and not repo-specific; would muddy the Rooms pack. |

## Boundary

The pack is narrow and project-specific.

* Keep Rooms-native project skills together.
* Pull in one first-party database skill for the canonical sqlite surface.
* Do not duplicate repo-worker-pack.
* Do not duplicate superpowers-plus.
* Do not duplicate unslop-plus.
* Do not include architecture-pack.

## Notes

The active projection inventory lives in `references/bundle-manifest.json` and
`references/source-map.md`. The bundle manifest and provenance map are
maintained in `references/`.
