# codex-marketplace

Canonical source location for Codex marketplace assets.

Codex plugin first; generated GPT-safe skill zips second.

The marketplace subtree follows the repo-wide index mesh rooted at
[../INDEX.md](../INDEX.md).

Repo-local marketplace posture lives in
[../.agents/plugins/marketplace.json](../.agents/plugins/marketplace.json) and
`repo-local-marketplace-policy.json`; the generator keeps those surfaces
current.

This repo keeps the active Codex plugin bundles under
`codex-marketplace/plugins/`, and the authoritative active-root list lives in
`codex-marketplace/custody-pack-registry.json` and the derived
`codex-marketplace/plugin-roots.json`. `superpowers-plus` is the retained mixed
projection-lane bundle over Superpowers source; `superpowers-mega-pack` is not
an active maintained marketplace root.

Editable source custody lives under `sources/first_party/` and
`sources/third_party/`. The marketplace roots under `codex-marketplace/plugins/`
are the installable projections.

The editable active-root inventory is `codex-marketplace/plugin-roots.json`.
The manifest export and the protected-root validators derive their active root
set from that generated file instead of duplicating the active roots in Python
constants. Pack bundle-manifest generation, active-root generation, and any
remaining mega-pack generation are driven by
`codex-marketplace/custody-pack-registry.json`; mega-pack nodes are marked with
`is_mega_pack: true`.

Repo-resident canonical `skill.zip` artifacts are published separately under
`generated/skill-zips/<pack-or-plugin>/<skill-name>/skill.zip`, with
`generated/skill-zips/registry.json` mapping each archive back to the source
skill tree that produced it.

That generated surface is the GPT-ready export surface. It packages the source
skill tree plus any repo-owned GPT overlay declared under `adapters/gpt/`.
Direct exports stay direct when the source is already GPT-safe; overlay exports
apply the overlay before packaging; excluded skills are recorded in the
registry with a reason instead of being exported raw.

The marketplace plugin roots are the canonical install surface. `adapters/gpt/`
exists to keep generated exports GPT-safe without changing Codex plugin
behavior.

Targeted updates should use `py -3 tools/update_skill_artifacts.py --skill
<pack>/<skill>`; `--all` is only for explicit full regeneration. Unrelated
generated drift is not acceptable.
Use `py -3 tools/generate_marketplace.py --check` and
`py -3 tools/generate_repo_index.py --check` to prove the marketplace registry,
Codex marketplace manifest, and repo index are current without rewriting them.
