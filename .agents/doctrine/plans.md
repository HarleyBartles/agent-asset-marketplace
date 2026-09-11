
## Scope

`.agents/plans/`

Defer to the repository root `AGENTS.md` for global repo and publication rules.

- Keep an active plan current enough that another worker can distinguish finished
  work from the next action. Checkbox bookkeeping is an in-flight aid, not a
  publication artifact or permanent reporting duty.
- Order implementation tasks so that all source and adapter/overlay edits are complete before any `tools/run * --apply` regeneration step. Run `tools/run heal --check` after overlay edits and before regeneration to catch line-number drift early.
- Do not run `tools/run ci --check` immediately before a normal commit or immediately after a successful hooked commit. Regenerate surfaces, stage the intended tree, commit, and let the pre-commit hook materialize the staged snapshot, run `ci --apply`, stage the owned generated surfaces, and run `ci --check --diagnostics`. Do not use `git commit --no-verify` to bypass the hook.
- If a plan is intentionally incomplete or left open, say why inside the plan itself.
- This is local worker guidance, not a future PR-blocker doctrine.
- Do not invent receipt requirements.

## Maintenance responsibility

This file must stay aligned with the repo's plan documentation practices. When
plan formats change or new guidance is needed for plan structure, review and
update this file to reflect current expectations. After completion, archive all
finished planning artifacts off-repo under the completed-artifact custody
doctrine; do not preserve them as mutable tracked history.
