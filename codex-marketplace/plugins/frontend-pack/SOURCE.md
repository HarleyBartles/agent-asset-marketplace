# Source

This plugin packages the retained `game-studio` source snapshot as a market-facing Codex plugin focused on browser frontend implementation guidance.

## Upstream basis

- Repo: `openai/plugins`
- URL: <https://github.com/openai/plugins.git>
- Pinned commit: `c33199897758cab145bb7fdab1ca8fb1cbd9de50`
- License: `MIT`

## Source surfaces copied

- `.codex-plugin/plugin.json`
- `assets/icon.svg`
- `references`
- `skills`

## Marketplace adaptation

- Status: `imported`
- Plugin name: `frontend-pack`
- Display name: `Frontend Pack`
- Marketplace category normalized to `Productivity`
- Icon paths normalized to `./assets/icon.svg`
- Projected the retained `game-studio` browser frontend, React-hosted 3D, shared architecture, and playtest guidance into the market-facing `frontend-pack` surface.
- Kept the pack boundary narrow and deferred the exact issue-named candidates `react-performance-optimization`, `accessibility-audit`, `ux-review`, `interaction-design`, and `webapp-testing` because those names are not present in the retained source snapshot in this checkout.
- Generated a marketplace README wrapper because the upstream root did not provide one.
- Generated a root LICENSE notice because the upstream root did not provide a root license file.
- Added a bundle-manifest inventory for the copied skill directories.

## Notes

The retained upstream snapshot now lives under `sources/third_party/game-studio/upstream/`.
The project intentionally keeps the source-custody record separate from the installable marketplace root so the bundle can be regenerated from live source bytes.
