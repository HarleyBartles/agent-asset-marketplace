# codex-marketplace

Canonical source location for Codex marketplace assets.

Codex plugin first; generated GPT-safe skill zips second.

This repo now keeps the active Codex plugin bundles to one protected
convention: `codex-marketplace/plugins/house-skills/`,
`codex-marketplace/plugins/adventures-pack/`,
`codex-marketplace/plugins/unslop/`,
`codex-marketplace/plugins/game-studio/`,
`codex-marketplace/plugins/wild-bunch-project-pack/`, and
`codex-marketplace/plugins/superpowers/`, in that order, with the source
manifest exposing only those roots and no legacy marketplace roots beside them.

Editable source custody lives under `sources/first_party/` and
`sources/third_party/`. The marketplace roots under `codex-marketplace/plugins/`
are the installable projections.

The editable active-root inventory is `codex-marketplace/plugin-roots.json`.
The manifest export and the protected-root validators derive their active root
set from that file instead of duplicating the six roots in Python constants.

Repo-resident canonical `skill.zip` artifacts are published separately under
`generated/skill-zips/<pack-or-plugin>/<skill-name>/skill.zip`, with
`generated/skill-zips/registry.json` mapping each archive back to the source
skill tree that produced it.

That generated surface is the GPT-ready export surface. It packages the source
skill tree plus any repo-owned GPT overlay declared under `gpt-overlays/`.
Direct exports stay direct when the source is already GPT-safe; overlay exports
apply the overlay before packaging; excluded skills are recorded in the
registry with a reason instead of being exported raw.

The marketplace plugin roots are the canonical install surface. `gpt-overlays/`
exists to keep generated exports GPT-safe without changing Codex plugin
behavior.

Targeted updates should use `py -3 tools/update_skill_artifacts.py --skill
<pack>/<skill>`; `--all` is only for explicit full regeneration. Unrelated
generated drift is not acceptable.
