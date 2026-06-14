# codex-marketplace

Canonical source location for Codex marketplace assets.

This repo now keeps the active Codex plugin bundles to one protected
convention: `codex-marketplace/plugins/house-skills/`,
`codex-marketplace/plugins/adventures-pack/`,
`codex-marketplace/plugins/unslop/`, and
`codex-marketplace/plugins/game-studio/`, in that order, with the source
manifest exposing only those roots and no legacy marketplace roots beside them.

Editable source custody lives under `sources/first_party/` and
`sources/third_party/`. The marketplace roots under `codex-marketplace/plugins/`
are the installable projections.

Repo-resident canonical `skill.zip` artifacts are published separately under
`generated/skill-zips/<pack-or-plugin>/<skill-name>/skill.zip`, with
`generated/skill-zips/registry.json` mapping each archive back to the source
skill tree that produced it.
