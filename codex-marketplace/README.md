# codex-marketplace

Canonical source location for Codex marketplace assets.

Codex plugin first.

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
projection-lane bundle over Superpowers source.

Editable source custody lives under `sources/first_party/` and
`sources/third_party/`. The marketplace roots under `codex-marketplace/plugins/`
are the installable projections.

The editable active-root inventory is `codex-marketplace/plugin-roots.json`.
The manifest export and the protected-root validators derive their active root
set from that generated file instead of duplicating the active roots in Python
constants. Pack bundle-manifest generation, active-root generation, and
projection materialization are driven by
`codex-marketplace/custody-pack-registry.json`.

Use `py -3 tools/update_skill_artifacts.py --all` for full regeneration. The
`--skill` and `--pack` flags remain as backwards-compatible aliases. Unrelated
generated drift is not acceptable.
Use `py -3 tools/generate_marketplace.py --check` and
`py -3 tools/generate_repo_index.py --check` to prove the marketplace registry,
Codex marketplace manifest, and repo index are current without rewriting them.
