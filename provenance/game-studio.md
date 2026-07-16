# Game Studio Provenance

## Summary

The Game Studio plugin packages the retained `game-studio` source snapshot from the OpenAI plugins repository as a market-facing Codex plugin.

## Upstream Basis

- **Repo**: `openai/plugins`
- **URL**: <https://github.com/openai/plugins.git>
- **Pinned commit**: `c33199897758cab145bb7fdab1ca8fb1cbd9de50`
- **License**: `MIT`
- **Source custody**: `sources/third_party/game-studio/upstream/`
- **Marketplace package**: `codex-marketplace/plugins/game-studio/`

## Source Surfaces Copied

- `.codex-plugin/plugin.json`
- `assets`
- `skills`

## Marketplace Adaptation

- **Status**: `imported`
- **Plugin name**: `game-studio`
- **Display name**: `Game Studio`
- **Marketplace category**: `Productivity`
- **Content mode**: `verbatim` for all upstream content
- **Adaptation notes**:
  - Copied the upstream root tree intact into the marketplace surface
  - Normalized the plugin manifest category to Productivity for registry compatibility
  - Normalized the plugin icon fields to `./assets/icon.svg` for validator compatibility
  - Generated a marketplace README wrapper because the upstream root did not provide one
  - Generated a root LICENSE notice because the upstream root did not provide a root license file
  - Added a bundle-manifest inventory for the copied skill directories

## Rights and Attribution

- **License**: MIT
- **Upstream attribution**: OpenAI plugins repository
- **Redistribution rights**: Per MIT license terms
- **Modifications**: Marketplace normalization only (category, icon paths, README, LICENSE, bundle manifest)

## Notes

The retained upstream snapshot lives under `sources/third_party/game-studio/upstream/`. All upstream content is preserved verbatim in the marketplace projection with only structural normalization for Codex marketplace compatibility.
