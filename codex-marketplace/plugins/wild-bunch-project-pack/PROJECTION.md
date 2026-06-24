# Projection

This bundle is a self-contained projection of the Wild Bunch project workflow.

## Included skills

- The exact current inventory is defined centrally in `references/bundle-manifest.json`.
- See `references/source-map.md` for the rendered keep/remove membership and source/projection paths.

## Excluded skill

- `agent-browser` is excluded because this repository does not retain an approved projection copy for it.

## Projection rule

- Copy the retained component trees, with any declared manifest normalization, into this plugin root.
- Keep first-party and third-party provenance separate in the bundle manifest and provenance map.
- Do not introduce linked-bundle or dependency semantics.
- Pack-local Codex hooks live under `hooks/` using the default discovery path, and they stay outside GPT skill export text.
