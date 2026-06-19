# Source

This plugin packages the retained `NickCrew/Claude-Cortex` frontend
application skills from the retained `claude-cortex` custody root as a
market-facing Codex plugin focused on React and frontend implementation
guidance.

## Upstream basis

- Repo: `NickCrew/Claude-Cortex`
- URL: <https://github.com/NickCrew/Claude-Cortex.git>
- Pinned commit: `7892d00e7cb6adf00144a535103b930c772fb2c0`
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
- Projected the retained `NickCrew/Claude-Cortex` frontend application, accessibility, UX review, interaction design, and browser testing guidance into the market-facing `frontend-pack` surface.
- Kept the pack boundary narrow and imported only the exact MARK-214 frontend candidates.
- Generated a marketplace README wrapper because the upstream root did not provide one.
- Generated a root LICENSE notice because the upstream root did not provide a root license file.
- Added a bundle-manifest inventory for the copied skill directories.

## Notes

The retained upstream snapshot now lives under
`sources/third_party/claude-cortex/upstream/`.
The project intentionally keeps the source-custody record separate from the
installable marketplace root so the bundle can be regenerated from live source
bytes.
