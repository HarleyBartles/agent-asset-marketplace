# Codex Marketplace Compatibility

This note applies to the active Codex projection of the first-party Superpowers+ workflow skill bundle.

## Instruction precedence

- Repo `AGENTS.md` files, platform/runtime policy, and user instructions remain authoritative.
- Superpowers skills are workflow guidance inside that governing stack.
- The projection must not claim that Superpowers overrides system, developer, runtime, or repo instructions.

## Projection contract

- `superpowers-plus` is the first-party projection-lane bundle for the Superpowers+ workflow skill family.
- The active plugin projects the first-party Superpowers+ skills, including the `using-superpowers-plus` workflow-selection entrypoint, plus the compositional helper skills (`handoff-gates`, `inspecting-the-environment`, `requesting-code-review`, `selecting-a-subagent`, `working-with-epics`).
- The retained `obra/superpowers` v6.2.0 MIT snapshot under `sources/third_party/superpowers/` is reference-only; it is not the editable surface and no adapter overlay is applied.
- Editable custody lives in `sources/first_party/skills/<name>/`. When a Superpowers+ skill needs to change, edit the first-party source and regenerate the projection.
- The repo-specific adaptation text lives only in the projection layer; the first-party source custody root is the editable surface and is not folded into the retained upstream snapshot.
- Source custody remains a verbatim retained upstream snapshot for reference. Do not fold Codex-safe wording, frontmatter normalization, marketplace policy, or adaptation into the retained source tree.
- Keep only the latest retained upstream source snapshot in custody. Older version directories are replaced, not accumulated.
- Installation and export artifacts are derived from the projection layer. Do not hand-edit generated zips or registry entries.
- Frontmatter contract: [docs/contracts/skill-frontmatter.md](../../../docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [docs/contracts/openai-agent-yaml.md](../../../docs/contracts/openai-agent-yaml.md)
- Do not place first-party expert or domain skills directly in the Superpowers+ plugin.
- Do not use this plugin as a dumping ground for House Skills, project doctrine, verification experts, GitHub/Linear mechanics, or other first-party expert surfaces.
- Do not use this plugin as a dumping ground for retired workflow doctrine; defer that routing to follow-up reprojection work instead.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.
- Any future first-party skill proposed for projection into `superpowers-plus` must be justified as a compositional wrapper over the Superpowers+ workflow family, not as an expert skill being relocated into the workflow plugin.

## Branch and publication flow

- In this repository, Linear issue contracts and the GitHub-visible PR gate define publication proof.
- Follow the repo's marketplace and review rules when they differ from generic Superpowers branch or merge guidance.
- Do not treat local merge, branch cleanup, or shell-driven PR creation as the canonical closeout path if repo policy requires a different gate.

## Purpose

This file keeps the active projection aligned with the Asset Marketplace operating model without changing the retained upstream source custody snapshot.
