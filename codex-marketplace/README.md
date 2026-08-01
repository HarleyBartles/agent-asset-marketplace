# Codex Marketplace

This repo keeps the active Codex plugin bundles under
`codex-marketplace/plugins/`, and the authoritative active-root list lives in
`codex-marketplace/plugin-roots.json`. `superpowers-plus` is the retained mixed
first-party workflow bundle over Superpowers source.

Editable source custody lives under `codex-marketplace/plugins/<plugin>/skills/`.
The marketplace roots under `codex-marketplace/plugins/` are the installable
surfaces.

## Layout

- `plugin-roots.json` — canonical list of active plugin roots
- `plugins/<plugin>/.codex-plugin/plugin.json` — plugin metadata
- `plugins/<plugin>/skills/<skill>/` — canonical skill source trees
- `manifest.json` — generated aggregate marketplace manifest
