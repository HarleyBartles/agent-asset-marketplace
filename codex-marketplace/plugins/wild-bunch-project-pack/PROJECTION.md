# Projection

This bundle is an installable bridge/overlay projection of the Wild Bunch project workflow.

## Included skills

- The exact current inventory is defined centrally in `references/bundle-manifest.json`.
- See `references/source-map.md` for the rendered keep/remove membership and source/projection paths.
- Dependency plugins stay separate install surfaces. This pack only carries the Wild Bunch bridge/native skills.

## Projection rule

- Copy the retained component trees, with any declared manifest normalization, into this plugin root.
- Keep first-party provenance in the bundle manifest and provenance map.
- Do not absorb whole dependency-plugin inventories into this pack.
- Keep dependency plugins separate unless the manifest explicitly documents a narrow, rationale-backed selected-skill projection.
- Pack-local Codex hooks live under `hooks/` using the default discovery path, and they stay outside GPT skill export text.
