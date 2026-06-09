# Source

        This plugin packages the upstream OpenAI Plugins root `plugins/build-macos-apps` as a market-facing Codex plugin.

        ## Upstream basis

        - Repo: `openai/plugins`
        - URL: <https://github.com/openai/plugins.git>
        - Pinned commit: `c33199897758cab145bb7fdab1ca8fb1cbd9de50`
        - License: `MIT`

        ## Source surfaces copied

        - `.codex-plugin/plugin.json`
- `README.md`
- `agents`
- `commands`
- `assets`
- `skills`

        ## Marketplace adaptation

        - Status: `imported`
        - Plugin name: `build-macos-apps`
        - Display name: `Build macOS Apps`
        - Marketplace category normalized to `Productivity`
        - Icon paths normalized to `./assets/icon.svg`
- Copied the upstream root tree intact into the marketplace surface.
- Normalized the plugin manifest category to Productivity for registry compatibility.
- Normalized the plugin icon fields to ./assets/icon.svg for validator compatibility.
- Generated a root LICENSE notice because the upstream root did not provide a root license file.
- Added a bundle-manifest inventory for the copied skill directories.

        ## Notes

        The upstream tree was copied into its own market-facing plugin directory without splitting the plugin boundary.
