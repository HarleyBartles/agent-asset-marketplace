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

Repo-resident canonical `skill.zip` artifacts are published as flat files under
`generated/skill-zips/<skill-name>.zip`. Each archive contains a single
`<skill-name>/` directory with `SKILL.md` and any supporting files.

That generated surface is the GPT-ready export surface. It is built as a
deterministic copy of the staged Codex projection. The marketplace plugin roots
are the canonical install surface.

Use `py -3 tools/update_skill_artifacts.py --all` for full regeneration. The
`--skill` and `--pack` flags remain as backwards-compatible aliases. Unrelated
generated drift is not acceptable.
Use `py -3 tools/generate_marketplace.py --check` and
`py -3 tools/generate_repo_index.py --check` to prove the marketplace registry,
Codex marketplace manifest, and repo index are current without rewriting them.
