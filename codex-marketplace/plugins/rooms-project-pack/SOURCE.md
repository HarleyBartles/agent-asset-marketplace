# Source

This bundle packages the retained Rooms first-party skills plus one retained
Claude-Cortex database skill as a Codex plugin projection.

## Canonical basis

- First-party Rooms source custody: `sources/first_party/skills/`
- Retained Claude-Cortex source custody: `sources/third_party/claude-cortex/upstream/skills/`
- License posture: mixed first-party and third-party custody for the active pack surface

## Source roots copied

- `references/bundle-manifest.json`
- `references/source-map.md`
- `references/provenance-map.json`
- `skills/`
- The bundle keeps the Rooms-native project skills together and adds one generic database guidance skill for the canonical sqlite surface.

## Marketplace adaptation

- Status: `projected`
- Plugin name: `rooms-project-pack`
- Display name: `Rooms Project Pack`
- Marketplace category normalized to `Productivity`
- Icon paths normalized to `./assets/icon.svg`
- The pack installs as a focused Rooms/project-routing surface and keeps repo-worker, superpowers, unslop, and architecture bundles separate.

## Notes

The active projection inventory lives in `references/bundle-manifest.json` and
`references/source-map.md`.
