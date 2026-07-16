# Projection

This root is the Codex-facing marketplace projection of the mixed Superpowers+ workflow and routing helpers.

## Layer Model

- Source custody keeps the retained upstream snapshots.
- Projection layer holds the source-controlled marketplace copy.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- Frontmatter contract: [docs/contracts/skill-frontmatter.md](../../../docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [docs/contracts/openai-agent-yaml.md](../../../docs/contracts/openai-agent-yaml.md)

## Projection contract
- `superpowers-plus` is the mixed marketplace projection for the retained skills listed in `references/bundle-manifest.json`.
- The active plugin contains `brainstorming`, `dispatching-parallel-agents`, `executing-plans`, `finishing-a-development-branch`, `inspecting-the-environment`, `receiving-code-review`, `requesting-code-review`, `subagent-driven-development`, `systematic-debugging`, `test-driven-development`, `using-git-worktrees`, `using-superpowers`, `verification-before-completion`, `writing-plans`, and `writing-skills`.
- `superpowers-plus` is the retained mixed projection-lane bundle for the Superpowers source family.
- `codex-marketplace/custody-pack-registry.json` determines whether any Superpowers-derived root is actively projected.
- `superpowers-mega-pack` is not a maintained active projection surface.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/icon.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/bundle-manifest.json`
- `references/source-map.md`

## Excluded from the active install surface

- Upstream harness surfaces, tests, docs, and package metadata remain in source custody as support provenance and retained source custody.
- No separate maintained `superpowers-mega-pack` root is part of the active install surface.
