# Planning Runbook

Use this reference for repository-specific plan custody, marketplace constraints,
and validation in `agent-asset-marketplace`. General planning semantics belong to
the `writing-plans` skill.

## Required repository context

- Read [`.agents/doctrine/custody-and-marketplace-doctrine.md`](../doctrine/custody-and-marketplace-doctrine.md) for source custody, provenance, and plugin curation.
- Read root [`AGENTS.md`](../../AGENTS.md) for source-of-truth and publication rules.
- Read [`.devin/rules/tools.md`](../../.devin/rules/tools.md) for canonical generation and validation commands.

Enter through `using-superpowers-plus` and follow its planning handoff. This
runbook does not select or sequence workflow skills.

## Plan custody

- Keep in-flight plans under `.agents/plans/`; epic plans may use
  `.agents/plans/<epic-name>/`.
- Keep session-only briefs, reports, and review diffs in the off-repo scratch
  workspace. Do not put the durable plan there.
- Commit the plan before execution handoff so workers read tracked state.
- On completion, use the `completing-plans` runbook to move the plan to
  `.agents/plans/completed/`, move any matching spec to
  `.agents/specs/completed/`, and run `tools/heal_archive_links.py --apply`.
- Do not create loose planning artifacts at repository root or under product
  source directories.

## Marketplace planning constraints

Plans that touch marketplace skills, prompts, or installers must:

- identify canonical source separately from generated installed copies;
- schedule source and local-overlay edits before regeneration;
- regenerate through the repository's canonical marketplace command;
- keep consumer-facing guidance independent of this repository's command bus;
- include focused contract proof and the normal hooked commit gate; and
- identify any intentionally broken interim state.
