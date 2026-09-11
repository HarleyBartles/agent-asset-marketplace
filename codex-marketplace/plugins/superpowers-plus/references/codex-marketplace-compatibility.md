# Codex Marketplace Compatibility

This note applies to the active Codex distribution of the first-party Superpowers+ workflow skill bundle.

## Instruction precedence

- Repo `AGENTS.md` files, platform/runtime policy, and user instructions remain authoritative.
- Superpowers skills are workflow guidance inside that governing stack.
- The `superpowers-plus` plugin must not claim that Superpowers overrides system, developer, runtime, or repo instructions.

## Plugin contract

- `superpowers-plus` is the first-party plugin bundle for the Superpowers+ workflow skill family.
- The active plugin includes the first-party Superpowers+ skills, including the `using-superpowers-plus` workflow-selection entrypoint, plus the compositional helper skills (`handoff-gates`, `inspecting-the-environment`, `iterative-review`, `requesting-code-review`, `receiving-code-review`, `selecting-a-subagent`, `writing-roadmaps`).
- `SOURCE.md` records the `obra/superpowers` v6.3.0 MIT commit used as the comparison basis. The upstream source tree is not vendored here.
- Editable custody lives in `codex-marketplace/plugins/superpowers-plus/skills/<name>/`. When a Superpowers+ skill needs to change, edit the canonical plugin skill directly.
- The repo-specific adaptation text lives only in the plugin skill; the canonical plugin skill is the editable surface and remains separate from the upstream comparison basis.
- Keep provenance and comparison instructions in `SOURCE.md`; do not describe that record as a retained source snapshot.
- Keep only the current upstream comparison pin in `SOURCE.md`. Replace older pins rather than accumulating them.
- Installation and export artifacts are derived from the plugin tree. Do not hand-edit generated zips or registry entries.
- Frontmatter contract: [.agents/contracts/skill-frontmatter.md](../../../.agents/contracts/skill-frontmatter.md)
- OpenAI agent contract: [.agents/contracts/openai-agent-yaml.md](../../../.agents/contracts/openai-agent-yaml.md)
- Do not place first-party expert or domain skills directly in the Superpowers+ plugin.
- Do not use this plugin as a dumping ground for House Skills, project doctrine, verification experts, GitHub/Linear mechanics, or other first-party expert surfaces.
- Do not use this plugin as a dumping ground for retired workflow doctrine; defer that routing to follow-up reworking instead.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe plugin wording.
- Any future first-party skill proposed for the `superpowers-plus` plugin must be justified as a compositional wrapper over the Superpowers+ workflow family, not as an expert skill being relocated into the workflow plugin.

## Branch and publication flow

- In this repository, Linear issue contracts and the GitHub-visible PR gate define publication proof.
- Follow the repo's marketplace and review rules when they differ from generic Superpowers branch or merge guidance.
- Do not treat local merge, branch cleanup, or shell-driven PR creation as the canonical closeout path if repo policy requires a different gate.

## Purpose

This file keeps the active plugin aligned with the Asset Marketplace operating model while preserving a precise upstream comparison pin.
