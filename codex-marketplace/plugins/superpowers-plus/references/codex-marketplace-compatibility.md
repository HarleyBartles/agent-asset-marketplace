# Codex Marketplace Compatibility

This note applies to the active Codex projection of `obra/superpowers`.

## Instruction precedence

- Repo `AGENTS.md` files, platform/runtime policy, and user instructions remain authoritative.
- Superpowers skills are workflow guidance inside that governing stack.
- The projection must not claim that Superpowers overrides system, developer, runtime, or repo instructions.

## Projection contract

- `superpowers` is a third-party plugin projection with selected first-party compositional skills projected into the vendored marketplace plugin.
- The active plugin keeps the first-party `inspecting-the-environment` helper and the upstream Superpowers core; the router-only wrapper skills have been retired from the active projection.
- The remaining first-party helper is compositional and complementary. It keeps Superpowers workflow guidance narrow by adding environment inspection only.
- The repo-specific adaptation for `using-superpowers` lives only in the projection layer and is source-controlled in `adapters/codex/superpowers-plus/...`.
- When `using-superpowers` changes upstream, update the Codex adapter overlay and its `agents/openai.yaml` companion before regenerating. The reusable source updater will flag those files as stale if they still point at the old upstream version.
- The retired ECC router wrapper previously pointed to a dedicated ECC pack; that routing path is now deferred to follow-up reprojection work.
- Source custody remains a verbatim upstream snapshot. Do not fold Codex-safe wording, frontmatter normalization, marketplace policy, or adaptation overlays into the retained source tree.
- Keep only the latest retained upstream source snapshot in custody. Older version directories are replaced, not accumulated.
- Installation and export artifacts are derived from the projection layer plus overlays. Do not hand-edit generated zips or registry entries.
- Frontmatter contract: [docs/contracts/skill-frontmatter.md](../../../docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [docs/contracts/openai-agent-yaml.md](../../../docs/contracts/openai-agent-yaml.md)
- Do not place first-party expert or domain skills directly in the Superpowers plugin.
- Do not use this plugin as a dumping ground for House Skills, project doctrine, verification experts, GitHub/Linear mechanics, or other first-party expert surfaces.
- Do not use this plugin as a dumping ground for ECC workflow doctrine; defer that routing to follow-up reprojection work instead.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.
- Any future first-party skill proposed for projection into `superpowers` must be justified as a compositional wrapper over Superpowers, not as an expert skill being relocated into the third-party plugin.

## Branch and publication flow

- In this repository, Linear issue contracts and the GitHub-visible PR gate define publication proof.
- Follow the repo's marketplace and review rules when they differ from generic Superpowers branch or merge guidance.
- Do not treat local merge, branch cleanup, or shell-driven PR creation as the canonical closeout path if repo policy requires a different gate.

## Purpose

This file keeps the active projection aligned with the Asset Marketplace operating model without changing the upstream source custody snapshot.
