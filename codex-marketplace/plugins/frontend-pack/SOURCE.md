# Source

This plugin packages frontend skills from two upstream sources:
1. The retained `NickCrew/Claude-Cortex` frontend application skills from the retained `claude-cortex` custody root
2. The retained `affaan-m/ECC` frontend skills from the retained `ecc` custody root

These are projected as a market-facing Codex plugin focused on React and frontend implementation guidance.

## Upstream basis

### NickCrew/Claude-Cortex

- Repo: `NickCrew/Claude-Cortex`
- URL: <https://github.com/NickCrew/Claude-Cortex.git>
- Pinned commit: `7892d00e7cb6adf00144a535103b930c772fb2c0`
- License: `MIT`

### affaan-m/ECC

- Repo: `affaan-m/ECC`
- URL: <https://github.com/affaan-m/ECC.git>
- Pinned commit: `ceca28852e5b31edbbf66ebccc8fd163dd14208e`
- License: `MIT`

## Source surfaces copied

### From NickCrew/Claude-Cortex

- `.codex-plugin/plugin.json`
- `assets/icon.svg`
- `references`
- `skills/accessibility-audit`
- `skills/interaction-design`
- `skills/react-performance-optimization`
- `skills/ux-review`
- `skills/webapp-testing`

### From affaan-m/ECC

- `skills/accessibility`
- `skills/angular-developer`
- `skills/browser-qa`
- `skills/design-system`
- `skills/e2e-testing`
- `skills/make-interfaces-feel-better`
- `skills/react-patterns`
- `skills/react-testing`
- `skills/swiftui-patterns`
- `skills/vue-patterns`
- `skills/windows-desktop-e2e`

## Marketplace adaptation

- Status: `imported`
- Plugin name: `frontend-pack`
- Display name: `Frontend Pack`
- Marketplace category normalized to `Productivity`
- Icon paths normalized to `./assets/icon.svg`
- Projected the retained `NickCrew/Claude-Cortex` frontend application, accessibility, UX review, interaction design, and browser testing guidance into the market-facing `frontend-pack` surface.
- Projected the retained `affaan-m/ECC` frontend skills (accessibility, angular-developer, browser-qa, design-system, e2e-testing, make-interfaces-feel-better, react-patterns, react-testing, swiftui-patterns, vue-patterns, windows-desktop-e2e) into the market-facing `frontend-pack` surface as part of MARK-245.
- Kept the pack boundary narrow and imported only the exact MARK-214 frontend candidates from Claude-Cortex and MARK-245 frontend candidates from ECC.
- Generated a marketplace README wrapper because the upstream root did not provide one.
- Generated a root LICENSE notice because the upstream root did not provide a root license file.
- Added a bundle-manifest inventory for the copied skill directories.

## Notes

The retained upstream snapshots now live under:
- `sources/third_party/claude-cortex/upstream/`
- `sources/third_party/ecc/upstream/`

The project intentionally keeps the source-custody record separate from the
installable marketplace root so the bundle can be regenerated from live source
bytes.
