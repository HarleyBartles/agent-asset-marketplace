# Source

This plugin packages the upstream OpenAI Skills root `skills/.curated/linear` as a market-facing Codex plugin.

## Upstream basis

- Repo: `openai/skills`
- URL: <https://github.com/openai/skills.git>
- Pinned commit: `a8924c2a35cfa290458852c4fad17c9133054c2e`
- License: `MIT`

## Source surfaces copied

- `skills`

## Marketplace adaptation

- Status: `imported`
- Plugin name: `openai-skills-linear`
- Display name: `Linear`
- Marketplace category normalized to `Productivity`
- Icon paths normalized to `./assets/icon.svg`
- Copied the upstream root tree intact into the marketplace surface.
- Generated a marketplace README wrapper.
- Generated a root LICENSE notice.
- Added a bundle-manifest inventory for the copied skill root.

## Notes

The upstream tree was copied into its own market-facing plugin directory without splitting the package boundary.
