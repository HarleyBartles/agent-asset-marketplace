# codex-marketplace

Canonical source location for Codex marketplace assets.

Codex plugin first; generated GPT-safe skill zips second.

The marketplace subtree follows the repo-wide index mesh rooted at
[../INDEX.md](../INDEX.md).

This repo now keeps the active Codex plugin bundles to one protected
convention: `codex-marketplace/plugins/house-skills/`,
`codex-marketplace/plugins/adventures-pack/`,
`codex-marketplace/plugins/unslop/`,
`codex-marketplace/plugins/game-studio/`,
`codex-marketplace/plugins/wild-bunch-project-pack/`,
`codex-marketplace/plugins/superpowers-plus/`,
`codex-marketplace/plugins/repo-worker-pack/`,
`codex-marketplace/plugins/dotnet-kit/`,
`codex-marketplace/plugins/codex-cortex/`,
`codex-marketplace/plugins/api-contracts-pack/`,
`codex-marketplace/plugins/architecture-pack/`,
`codex-marketplace/plugins/language-patterns-pack/`,
`codex-marketplace/plugins/security-pack/`,
`codex-marketplace/plugins/frontend-pack/`,
`codex-marketplace/plugins/agentic-workflows/`,
`codex-marketplace/plugins/agentic-evaluation/`,
`codex-marketplace/plugins/research-pack/`,
`codex-marketplace/plugins/engineering-pack/`, and
`codex-marketplace/plugins/everything-codex-code/`, in that order, with the source
manifest exposing only those roots and no legacy marketplace roots beside them.

Editable source custody lives under `sources/first_party/` and
`sources/third_party/`. The marketplace roots under `codex-marketplace/plugins/`
are the installable projections.

The editable active-root inventory is `codex-marketplace/plugin-roots.json`.
The manifest export and the protected-root validators derive their active root
set from that file instead of duplicating the active roots in Python constants.

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
