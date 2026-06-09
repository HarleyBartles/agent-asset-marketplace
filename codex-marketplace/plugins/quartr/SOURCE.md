# Source

        This plugin packages the upstream OpenAI Plugins root `plugins/quartr` as a market-facing Codex plugin.

        ## Upstream basis

        - Repo: `openai/plugins`
        - URL: <https://github.com/openai/plugins.git>
        - Pinned commit: `c33199897758cab145bb7fdab1ca8fb1cbd9de50`
        - License: `MIT`

        ## Source surfaces copied

        - `.codex-plugin/plugin.json`
- `.app.json`
- `assets`

        ## Marketplace adaptation

        - Status: `imported`
        - Plugin name: `quartr`
        - Display name: `Quartr`
        - Marketplace category normalized to `Productivity`
        - Icon paths normalized to `./assets/icon.svg`
- Copied the upstream root tree intact into the marketplace surface.
- Normalized the plugin manifest category to Productivity for registry compatibility.
- Normalized the plugin icon fields to ./assets/icon.svg for validator compatibility.
- Generated a marketplace README wrapper because the upstream root did not provide one.
- Generated a root LICENSE notice because the upstream root did not provide a root license file.

        ## Notes

        The upstream tree was copied into its own market-facing plugin directory without splitting the plugin boundary.
