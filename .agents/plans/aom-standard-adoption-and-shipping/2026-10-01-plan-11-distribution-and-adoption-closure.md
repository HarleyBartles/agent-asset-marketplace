# Distribution and Adoption Closure Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Status:** completed-awaiting-retirement

**Goal:** Close the Marketplace's AOM migration with direct evidence that the generated plugin installs in isolation, standards remain independently selectable and pinned, and the complete tracked gate passes on Windows and hosted Linux.

**Architecture:** Use the generated plugin package as the installable product and test it with the Codex CLI under a disposable `CODEX_HOME`, keeping the user's normal plugin state untouched. Resolve the repository's exact standard pins from Git history and assess one-standard and mixed-standard examples without creating a universal checker or implying that plugin refresh updates a standard pin. Publish the reviewed branch as a Draft PR so the hosted workflow can prove the exact submitted commit; only then update the repository-owned certification and close the roadmap.

**Tech Stack:** Codex CLI plugin marketplace commands, generated Marketplace plugin package, repository-owned AOM record and checker, GitHub hosted workflow, Windows tracked pre-commit hook.

**Spec:** [Approved AOM design](../../specs/2026-09-30-aom-standard-adoption-and-shipping.md), especially sections 2-9. **Roadmap:** [AOM Standard Adoption and Shipping](roadmap.md), Plan 11.

**Execution Strategy:** `executing-plans` - the adoption, pin-resolution, certification, and publication steps form one evidence chain, so keeping the same executor preserves the exact artifact and commit context across gates.

## Global Constraints

- Do not modify the primary checkout or any other repository.
- Keep AOM standard subscriptions immutable and separate from ambient plugin installation or refresh.
- Repositories self-certify; structural checks must not claim semantic compliance.
- Do not add a standard subscription, mandatory starter artifact, copied scaffolder, or automatic update warning.
- Use a disposable `CODEX_HOME` under the repository's declared scratch location for local plugin-install proof; never modify the user's configured Codex installation.
- Preserve the complete Windows and Linux `tools/run.py ci` gate through the tracked `githooks/pre-commit` entrypoint.
- Publish only as a Draft PR; do not merge or change it to Ready.
- Do not claim hosted Linux success until GitHub reports success for the exact tested PR head.

## Review Focus

- A local plugin install accidentally writes into the user's normal Codex state; use a disposable `CODEX_HOME` and verify it before invoking plugin commands.
- Plugin refresh is mistaken for standard upgrade; keep plugin inventory and immutable standard authority checks separate.
- A one-standard example silently acquires unrelated standards or empty certification duties; inspect the declared selection and its explicit responsibilities.
- CI is green for an earlier commit only; use the final Draft PR head as the hosted evidence key and report any later commits accurately.

---

### Task 1: Prove isolated installation of the generated AOM plugin

**Files:**

- Read: `.agents/docs/distribution.md`, `.agents/plugins/marketplace.json`, `dist/plugins/agent-operating-model/.codex-plugin/plugin.json`, and the generated AOM bundle manifest.
- Modify only under: the plan's off-repo workspace returned by `workspace.py --apply PLAN_FILE`.

**Consumes:** Plan 10 commit `45a718ae4` and its generated Marketplace projection.

**Produces:** A recorded local proof that Codex can resolve and install the self-contained AOM package from this checkout without user-global state changes.

- [x] Resolve the shared off-repo plan workspace with `workspace.py --apply PLAN_FILE` and keep its returned path in `$workspacePath`; create `$workspacePath\codex-home` for this proof.
- [x] From PowerShell, set `$repoRoot = (git rev-parse --show-toplevel).Trim()` and `$env:CODEX_HOME = Join-Path $workspacePath 'codex-home'`, then run `codex plugin marketplace add $repoRoot --json` and `codex plugin add agent-operating-model@agent-asset-marketplace --json`.
- [x] Run `codex plugin list --json` and inspect the isolated installed package; confirm the package manifest and standard skills are present and retired `repo-shape` and `markdown-formatting` payloads are absent.
- [x] Record the command results and installed package path in `$workspacePath\evidence.md`; keep temporary Codex state outside the repository and preserve it until the evidence is recorded.

### Task 2: Verify selectable standards and exact source authority

**Files:**

- Read: `.agents/contracts/operating-standards.json`, `.agents/contracts/standards-certification.md`, `skills/repo-standards/references/source-resolution.md`, each selected `standard.md`, and the behavior cases under `skills/repo-standards/tests/behavior/`.
- Modify only under: the off-repo plan workspace resolved by `workspace.py --apply PLAN_FILE` if a disposable consumer fixture is needed.

**Consumes:** The isolated installed package from Task 1 and the immutable source pins in the repository subscription record.

**Produces:** Evidence that a single standard and a chosen combination remain distinguishable, that unrelated standards are not implicitly required, and that old pins resolve from their exact Git commits.

- [x] Set a PowerShell `$definitions` array to exactly `skills/agents-routing/references/standard.md`, `skills/runbook-composition/references/standard.md`, `skills/playbook-composition/references/standard.md`, `skills/tracked-repo-hooks/references/standard.md`, `skills/review-entrypoint/references/standard.md`, `skills/contribution-entrypoint/references/standard.md`, `skills/completed-artifact-custody/references/standard.md`, and `skills/unslop/references/standard.md`. For each `$definition`, run `py -3 skills/repo-standards/scripts/pinned_definition.py --source-root . --commit 3d59506dbd7a02266dedc9251b396dd60e5cc37d --definition $definition --check`; stop on the first nonzero exit and record each successful retrieval.
- [x] Inspect the package's runbook, playbook, review, contribution, and Unslop definitions together with the one-standard and mixed-selection behavior cases; record which requirements are conditional and which require routing only when that standard is selected.
- [x] In the disposable consumer fixture, create one version 2 subscription record selecting only `review-entrypoint` and a second selecting `runbook-composition`, `playbook-composition`, and `unslop`. Give each fixture a root `AGENTS.md` that routes to its subscription and certification record, and include certification headings only for the IDs selected by that fixture. Use these exact ID, definition, and certification mappings: `review-entrypoint` to `skills/review-entrypoint/references/standard.md` and `.agents/contracts/standards-certification.md#review-entrypoint`; `runbook-composition` to `skills/runbook-composition/references/standard.md` and `.agents/contracts/standards-certification.md#runbook-composition`; `playbook-composition` to `skills/playbook-composition/references/standard.md` and `.agents/contracts/standards-certification.md#playbook-composition`; `unslop` to `skills/unslop/references/standard.md` and `.agents/contracts/standards-certification.md#unslop`. Every source repository is `https://github.com/HarleyBartles/agent-asset-marketplace.git`, and every source commit is `3d59506dbd7a02266dedc9251b396dd60e5cc37d`. Validate both records against `skills/repo-standards/references/subscriptions.schema.json` with Python `jsonschema`; confirm no other catalog ID is added implicitly.
- [x] Resolve the historical v1 definition `skills/repo-shape/references/unslop-standard.md` and its referenced deployed copy from commit `0af5d4da6a594458bc2bad1b8e9e013a66ea8e20`; confirm current plugin contents do not replace that authority.
- [x] Keep semantic certification as a human assessment; do not describe a schema parse, package install, or repository checker as proof of semantic compliance.

### Task 3: Publish the reviewed head and close certification

**Files:**

- Modify: `.agents/contracts/standards-certification.md` and `.agents/plans/aom-standard-adoption-and-shipping/roadmap.md` after exact hosted evidence is available.
- Modify: `.github/workflows/marketplace-validation.yml` so Draft PRs receive the same Linux gate as other PRs.
- Preserve: all existing subscription records unless direct evidence identifies an error.

**Consumes:** Tasks 1-2, the full Windows hooked commit gate, and the hosted workflow result for the exact Draft PR head.

**Produces:** A truthful self-certification of the migrated tracked gate, a reviewed Draft PR, and a completed roadmap with exact evidence references.

- [x] Remove the workflow job condition that skips pull requests with `draft == true`; preserve the `ubuntu-latest` runner, clean detached commit check, dependency setup, and `githooks/pre-commit` hosted mode.
- [x] Run `py -3 tools/run.py marketplace --check` and `py -3 tools/run.py validate --check` for any uncommitted adoption or documentation changes; stage intended paths and commit through the normal tracked hook.
- [x] Push the completed branch and open a Draft PR against the repository's actual default branch; attach the PR to this Codex task.
- [x] Wait for `.github/workflows/marketplace-validation.yml` to report the tracked `githooks/pre-commit` gate green on the exact PR head. The earlier successful run checked GitHub's synthetic merge ref, not the PR head, so it is not exact-commit evidence. If the gate fails, repair the owning source, commit, push, and repeat against the new head. Exact head `f7e322063d31d16da04f66929b5974679b97121a` passed run `36934495302`.
- [x] Update the `tracked-validation-hook` certification with the exact commit whose hosted Linux gate passed and the Windows hook evidence for its staged tree; retain semantic and runtime limits. Certification records `f7e322063d31d16da04f66929b5974679b97121a` and run `36934495302`.
- [x] Commit and push the certification/roadmap closeout. Confirm Windows hook and hosted Linux gate status for the resulting head, and report any hosted result that is still pending without claiming certification prematurely. Documentation closeout `1a8574100e79a11f6843e772d526754716313872` passed Windows and hosted run `36935001410`; the final roadmap-status head `5aab5ea4040de0f1613ee1afd5e1c87447eec2a2` passed Windows and hosted run `36935593512`.
- [x] Complete a final whole-range review, ensure the working tree is clean, and report the Draft PR URL, exact reviewed head, local and hosted evidence, and any remaining human-owned post-handoff action. Fresh read-only reviews of `3b39cc051..5aab5ea4040de0f1613ee1afd5e1c87447eec2a2` found no actionable branch findings and no Critical or Important plan findings. Independently confirmed the Plan 11 `evidence.md` exists at the declared scratch path. The final head passed Windows hook and hosted Linux run `36935593512`.

### Task 4: Repair whole-branch review findings before final handoff

**Files:**

- Modify: `githooks/pre-commit` and tests that exercise the actual repository hook and hosted workflow.
- Modify: `.github/workflows/marketplace-validation.yml` to check out and assert the proposed commit SHA.
- Modify: `requirements.txt`, `.agents/plugins/marketplace.json`, `src/plugin-definitions/marketplace-policy.json`, the marketplace registry builder/validator, and the obsolete tracked wheel.
- Modify: skill-authoring guidance, repository routing/doctrine, the approved spec, and workflow pressure fixtures where review found retired behavior still stated as current.
- Modify: Plan 2 and Plan 8 completion records and this plan's evidence.

**Consumes:** The final range review of `3b39cc051..5aab5ea4040de0f1613ee1afd5e1c87447eec2a2`, exact live GitHub run evidence, the approved AOM spec, and the recorded Plan 8 execution ledger.

**Produces:** A hosted gate that proves the exact proposed commit, a repository hook that validates Git's actual commit candidate, no retired formatter payload or local-skill registration contract, and internally consistent adoption guidance and plan records.

- [x] Add behavior tests for a real `git commit --only` using Git's temporary index, exact proposed-SHA checkout/validation, and repository-authored skills under `.agents/skills/` without a separate registration. Observe the expected failures before changing the implementation.
- [x] Preserve `GIT_INDEX_FILE` in the hook's superproject candidate operations while preventing it from leaking into nested submodule commands. Confirm both path-limited commit behavior and preservation of separately staged work.
- [x] Make the hosted workflow check out `${{ github.event.pull_request.head.sha || github.sha }}`, assert `HEAD` equals that exact SHA in a clean detached checkout, and pass the same SHA to hosted hook mode.
- [x] Remove the retired Markdown formatter dependencies and tracked wheel; remove the `repo.local_skills` declaration and consumer requirement from the marketplace policy, generator, validator, and authoring routes while retaining repository-owned `.agents/skills/` content as valid.
- [x] Reconcile the approved Markdown authoring decision and existing-pin upgrade sequence across the spec, repo-standards adoption guide, skill-authoring guidance, and pressure fixtures. Keep historical plan records but resolve their incomplete completion checkboxes using recorded commit evidence.
- [x] Regenerate only canonical downstream Marketplace projections, remove stale active references, and run the complete normal Windows hook through a commit. Commit `f7e322063` passed.
- [x] Push the correction commit to Draft PR #345, verify hosted Linux checks the exact head SHA and passes, then update certification and roadmap evidence. Commit/push the documentation closeout and verify the final PR head again. Certification records `f7e322063d31d16da04f66929b5974679b97121a` and run `36934495302`; final roadmap-status head `5aab5ea4040de0f1613ee1afd5e1c87447eec2a2` passed exact-head run `36935593512`.
- [x] Build a fresh final review package for the exact final range, obtain fresh read-only whole-branch and plan review, resolve all Critical/Important findings, run completion-readiness, and leave the checkout clean. The whole-branch review found no actionable findings; plan review found no Critical or Important inconsistencies. The checkout was clean at review.
