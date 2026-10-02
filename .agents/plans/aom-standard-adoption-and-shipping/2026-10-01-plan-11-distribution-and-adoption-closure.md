# Distribution and Adoption Closure Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Status:** completed-awaiting-retirement. Final reviewed implementation head: `d9bafd3c6dde0f9b6cf8d60892103c8cd7523f79`.

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
- [x] Exercise one-standard runbook adoption with an edited optional starter, one-standard playbook adoption with complete inline guidance and no ambient capability, and combined runbook-to-playbook routing using assets from the isolated installed package. Keep the disposable fixtures explicitly uncertified; record the semantic review and schema evidence in the Plan 11 scratch evidence.
- [x] Refresh the current Git marketplace after the branch advances while a disposable consumer still pins the older definition. Confirm the plugin snapshot updates, the consumer subscription remains unchanged, and the pinned reader still resolves the exact older definition bytes. The isolated snapshot advanced from `3c0ba4197` to `c2d83492c`; the fixture pin and its SHA-256 were unchanged. The pinned definition bytes matched the refreshed plugin because no standard definition file changed between those commits.

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
- [x] Update the `tracked-validation-hook` certification with the exact commit whose hosted Linux gate passed and the Windows hook evidence for its staged tree; retain semantic and runtime limits. After the final hook wording correction, certification records `48d3bd78ae34a5a83e1a1361a54f0b2fa43bcc05` and exact-head hosted run `36938920670`.
- [x] Commit and push the certification/roadmap closeout. Confirm Windows hook and hosted Linux gate status for the resulting head, and report any hosted result that is still pending without claiming certification prematurely. Documentation closeout `1a8574100e79a11f6843e772d526754716313872` passed Windows and hosted run `36935001410`; roadmap-status head `5aab5ea4040de0f1613ee1afd5e1c87447eec2a2` passed run `36935593512`; later exact-head runs passed for hook wording `48d3bd78a` / `36938920670`, evidence citation `3c0ba4197` / `36939383009`, and product-scenario plan update `c2d83492c` / `36965407664`.
- [x] Complete a final whole-range review, ensure the working tree is clean, and report the Draft PR URL, exact reviewed head, local and hosted evidence, and any remaining human-owned post-handoff action. Fresh review of `3b39cc051..0b072f7c0` found missing new-skill discovery metadata and stale custody guidance; both were corrected. A focused review of the custody correction at `d9bafd3c6` found no actionable issue. The Plan 11 reviewer found no further Critical or Important plan issues. Windows tracked hook passed on `d9bafd3c6`; exact-head hosted Linux run `36967809975` passed and verified the checkout SHA. PR #345 remains open and Draft with that exact head and evidence in its description. Product fixtures and moving-marketplace evidence are in the declared scratch `evidence.md`. Remaining action: human review and merge; retain the plan, roadmap, and approved spec through merge.

### Task 4: Repair whole-branch review findings before final handoff

**Files:**

- Modify: `githooks/pre-commit` and tests that exercise the actual repository hook and hosted workflow.
- Modify: `.github/workflows/marketplace-validation.yml` to check out and assert the proposed commit SHA.
- Modify: `requirements.txt`, `.agents/plugins/marketplace.json`, `src/plugin-definitions/marketplace-policy.json`, the marketplace registry builder/validator, and the obsolete tracked wheel.
- Modify: skill-authoring guidance, repository routing/doctrine, the approved spec, and workflow pressure fixtures where review found retired behavior still stated as current.
- Modify: Marketplace custody doctrine where the final whole-branch review found obsolete `.agents/standards/` and local-skill declaration guidance.
- Modify: Plan 2 and Plan 8 completion records and this plan's evidence.
- Modify: the eight new AOM standard skill frontmatters and their Codex wrappers when whole-branch review verifies their required discovery metadata is missing; add a focused packaging-contract test.

**Consumes:** The final range review of `3b39cc051..9927c4464349ec23827980075721a61709f9813e`, exact live GitHub run evidence, the approved AOM spec, and the recorded Plan 8 execution ledger.

**Produces:** A hosted gate that proves the exact proposed commit, a repository hook that validates Git's actual commit candidate, no retired formatter payload or local-skill registration contract, and internally consistent adoption guidance and plan records.

- [x] Add behavior tests for a real `git commit --only` using Git's temporary index, exact proposed-SHA checkout/validation, and repository-authored skills under `.agents/skills/` without a separate registration. Observe the expected failures before changing the implementation.
- [x] Preserve `GIT_INDEX_FILE` in the hook's superproject candidate operations while preventing it from leaking into nested submodule commands. Confirm both path-limited commit behavior and preservation of separately staged work.
- [x] Make the hosted workflow check out `${{ github.event.pull_request.head.sha || github.sha }}`, assert `HEAD` equals that exact SHA in a clean detached checkout, and pass the same SHA to hosted hook mode.
- [x] Remove the retired Markdown formatter dependencies and tracked wheel; remove the `repo.local_skills` declaration and consumer requirement from the marketplace policy, generator, validator, and authoring routes while retaining repository-owned `.agents/skills/` content as valid.
- [x] Reconcile the approved Markdown authoring decision and existing-pin upgrade sequence across the spec, repo-standards adoption guide, skill-authoring guidance, and pressure fixtures. Keep historical plan records but resolve their incomplete completion checkboxes using recorded commit evidence.
- [x] Regenerate only canonical downstream Marketplace projections, remove stale active references, and run the complete normal Windows hook through a commit. Commit `f7e322063` passed.
- [x] Add the required `use_when` and `do_not_use_when` metadata and `agents/openai.yaml` Codex wrapper for each of the eight new standard skills. A focused package-contract test failed before the metadata existed and passed after the source changes and marketplace regeneration.
- [x] Update Marketplace custody doctrine to describe repository-authored skill custody without a declaration inventory and v2 standard pin/certification ownership, removing the retired `.agents/standards/` claim. Whole-branch review identified the stale authority pointer; fresh review of the correction remains pending.
- [x] Push the correction commit to Draft PR #345, verify hosted Linux checks the exact head SHA and passes, then update certification and roadmap evidence. Commit/push the documentation closeout and verify the final PR head again. Certification records the latest source-gate evidence at `48d3bd78ae34a5a83e1a1361a54f0b2fa43bcc05`, run `36938920670`; documentation closeout head `3c0ba41975e78217a655a6e8012fcb1deaf985bd` passed the exact-head workflow as run `36939383009`.
- [x] Build a fresh final review package for the exact final range, obtain fresh read-only whole-branch and plan review, resolve all Critical/Important findings, run completion-readiness, and leave the checkout clean. Earlier reviews identified the stale certification citation, missing product-level scenario evidence, missing Codex discovery metadata, and obsolete custody guidance. The certification, fixtures, skill metadata, and custody doctrine now address those findings. Fresh review found no remaining Critical or Important findings; the focused custody review was clean. Final implementation head `d9bafd3c6` passed the complete Windows hook and exact-head hosted Linux run `36967809975`. The worktree was clean at handoff; retain all planning artifacts through Draft PR review and merge.
