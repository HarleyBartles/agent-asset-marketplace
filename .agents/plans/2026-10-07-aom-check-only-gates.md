# AOM Candidate-Preserving Gates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make pre-commit and hosted CI preserve the proposed candidate, fail at the first cheap failing check, and expose precise focused repair and recheck commands.

**Architecture:** The optional hook and Marketplace integration validate a disposable checkout of the original candidate with a private index. The repository adapter runs an ordered check-only bus gate; preparation and maintained generation remain explicit bus operations. Disposable build/test outputs are permitted, while maintained-file or candidate-index mutation rejects the gate even when a child also fails.

**Tech Stack:** Git, Bash/Git Bash, Python 3.12, pytest, Ruff 0.9.0, existing deterministic Marketplace generators, GitHub Actions.

**Spec:** [Approved specification](../specs/2026-10-07-aom-check-only-gates-design.md). Read both artifacts and the [implementation runbook](../runbooks/implementing.md) before execution.

**Execution Strategy:** `executing-plans`. Hook materialization, staged lint scope, bus diagnostics, command-contract validation, and source-pin publication share state and must migrate together. Inline execution preserves that context; obtain a fresh whole-branch review before publication.

Status: Approved implementation in progress.

## Global Constraints

- The hook and hosted CI execute the same complete set of required checks, in a dependency-safe order that prioritizes cheap checks before expensive ones.
- Failure stops the gate before later checks or their expensive setup starts.
- Neither gate repairs or stages repository content. Disposable outputs are allowed; changes to maintained repository files or the intended index are not.
- Configuration, adapters, and checked inputs come from the candidate. Preserve the original staged, unstaged, untracked, and protected ignored state on success and failure.
- Mutation detection runs on failing child exits as well as successful exits. Restoration or cleanup errors reject the commit and provide recovery information.
- Preserve meaningful child output and nonzero status. A focused recheck does not replace the final complete hook or hosted gate.
- Standards remain independently selectable. Do not add a mandatory AOM registry, ABI, command JSON, Python starter, runtime checkout, or scaffold to the portable pledge.
- Existing consumers follow their immutable pins until explicitly upgraded. Do not change other repositories or installed user plugins.
- Edit canonical `skills/` and repository-owned integration; regenerate `dist/` through the existing bus. Do not hand-edit packages or store test results as tracked receipts.
- Keep Markdown prose and list items on one physical source line. Use no emoji or em-dashes.

## Review Focus

- A path-limited commit supplies a temporary index: validate that candidate and leave separately staged work alone. Covered by Tasks 1 and 3.
- A check corrupts a maintained file or stages it before returning nonzero: report the child and mutation failures and preserve source state. Covered by Tasks 1 and 3.
- Ignored local content makes a broken candidate look valid: do not import that content into the disposable gate. Covered by Task 1.
- A repair command contains paths with spaces or changes only unstaged content: the printed command must execute against the author's checkout, and the next hook must still assess the staged candidate. Covered by Tasks 2 and 3.
- A new hook definition is pinned before its source commit exists: use a source commit followed by an explicit pin/certification commit, preserving other standards' pins. Covered by Task 4.

## Source Map and Working Boundary

Use the existing worktree `Z:/_agent-worktrees/agent-asset-marketplace/codex/aom-check-only-gates`, branch `codex/aom-check-only-gates`. The base inspected for planning is `c72751a0ac2893a3968b70111fbc21bdd3b119f3`; the committed specification is `af22712de891e60ccbff9ab886b5f52f98d3fe64`. PowerShell login initialization can reset the current directory: use a non-login shell and verify `git rev-parse --show-toplevel`, branch, and status before each mutation. Preserve this branch's planning commits when refreshing the remote base.

Before execution, fetch `origin/main` and compare the worktree's base; integrate new upstream work safely if it has advanced. Read root/scoped `AGENTS.md`, [Marketplace doctrine](../doctrine/marketplace-worker-doctrine.md), [custody doctrine](../doctrine/custody-and-marketplace-doctrine.md), [test contract](../contracts/skill-tests.md), [test playbook](../playbooks/testing.md), and applicable code-style/skill-authoring guidance. Planning ingress found no explicitly completed artifacts eligible for retirement; do not remove active or ambiguously marked predecessor artifacts.

Canonical behavior owners are `skills/tracked-repo-hooks/` and `skills/command-bus/`. Existing contradictory hook guidance is limited to the affected paragraphs in `skills/repository-validation/SKILL.md`, `skills/handoff-gates/SKILL.md`, and `skills/publishing-source/SKILL.md`; update those paragraphs without redesigning their workflows. Product definitions already include these skills; no new plugin membership or mandatory assets are required.

Repository integration owners are `githooks/pre-commit`, `tools/run.py`, `tools/check_agent_standards.py`, `.agents/contracts/repo-standards-commands.json`, `.agents/contracts/operating-standards.json`, `.agents/contracts/standards-certification.md`, and `.github/workflows/marketplace-validation.yml`. Add `tools/hook_gate_adapter.sh` as the repository-owned adapter seam. Update the corresponding hook explanations in `.agents/doctrine/tools.md` and `.agents/doctrine/plans.md`.

Run focused RED/GREEN cycles within each task. Do not pay for a full hooked commit between implementation tasks: Tasks 1-3 converge as one source/integration commit after regeneration and review. Task 4 then makes the separate immutable-pin commit that cannot reference its own future hash. Both commits use the normal hook. Never bypass it or run redundant full CI immediately before or after a successful hooked commit.

## Task 1: Make the Portable Hook Preserve Its Candidate

**Files:** Modify `skills/tracked-repo-hooks/references/standard.md`, `skills/tracked-repo-hooks/SKILL.md`, `skills/tracked-repo-hooks/assets/hooks/pre-commit`, `skills/tracked-repo-hooks/assets/targets/repository_gate.py`, `skills/tracked-repo-hooks/assets/workflows/github-actions-hosted-gate.yml`, `skills/command-bus/references/standard.md`, `skills/command-bus/SKILL.md`, the three affected guidance paragraphs named above, and both skills' `tests/evaluator-only/adoption-scenarios.md`. Extend `skills/tracked-repo-hooks/tests/assets/test_pre_commit_starter.py` and adjust `test_bus_target.py` and `test_hosted_workflow.py` where their old contracts change. The optional normalizer stays a preparation utility; its implementation does not need to change for this task.

**Interfaces:** Preserve `pre-commit`, `pre-commit --hosted <commit>`, and `pre-commit --help`. The candidate-owned `tools/hook_gate_adapter.sh` defines only `run_repository_check_gate()`, returning the actual check status and printing named failure/repair/recheck diagnostics. Export `REPO_ROOT` as the disposable checkout root, never the author checkout. Remove `run_repository_apply_gate()` and automatic staging from the seed. Missing adapters still fail closed with status 2.

- [x] Rewrite the standard's normalization/generation clause around candidate preservation, permitted disposable outputs, fail-fast cheap-first checks, and exact focused failure guidance. Make bus guidance explicitly own preparation when a bus is adopted. Replace the bus sample's blanket read-only description with check-only candidate-preserving behavior. Preserve no-skip policy and independently selectable assets; update the adjacent workflow paragraphs so they cannot send an agent back to an apply-in-hook workflow.
- [x] Adapt the hook fixtures and place observer logs outside the disposable checkout. Replace tests that expect normalized candidate retention with original-candidate preservation tests; do not retain apply callback assumptions.
- [x] Witness the legacy apply callback RED and prove GREEN never calls it, observes the original staged bytes, preserves the original index tree and working bytes, and returns status 17.
- [x] Add a failing mutation callback test and assert the source index, tracked bytes, untracked bytes, and protected ignored bytes are unchanged after rejection.

```bash
run_repository_check_gate() {
  printf 'corruption\n' > "$REPO_ROOT/notes file.txt"
  git add -- 'notes file.txt'
  printf 'named check failed\n' >&2
  return 23
}
```

- [x] Implement candidate isolation with a temporary standalone local Git clone and private index while preserving the author checkout and path-limited index semantics. Hosted mode validates a clean detached exact SHA; local and hosted parent/tree selection, origin-ref copying, and root handling are covered.
- [x] Materialize the candidate after clearing inherited repository-local Git variables, set the private HEAD first, then load and checkout the candidate tree. The unborn-source path uses an object alternate to existing local objects.

```bash
git clone --quiet --shared --no-checkout -- "$SOURCE_ROOT" "$GATE_ROOT"
git -C "$GATE_ROOT" config core.autocrlf false
if [[ -n "$VALIDATION_PARENT" ]]; then
  git -C "$GATE_ROOT" update-ref --no-deref HEAD "$VALIDATION_PARENT"
else
  git -C "$GATE_ROOT" symbolic-ref HEAD refs/heads/gate-unborn
  git -C "$GATE_ROOT" update-ref -d refs/heads/gate-unborn
fi
git -C "$GATE_ROOT" read-tree "$CANDIDATE_TREE"
git -C "$GATE_ROOT" checkout-index --all --force
```

- [x] Delete clone-created origin refs and copy only the author's actual non-symbolic remote-tracking refs, without fetching or reconstructing refs.

- [x] Load the adapter only from the materialized candidate and exclude author-side ignored/stale files. Resolve submodules from staged gitlinks and local initialized object stores only, with no fetch.
- [x] Materialize root and nested submodules from NUL-safe index entries, require in-root source paths and exact local objects, and detect staged or working mutation in each private submodule.
- [x] Capture child status before mutation checks, compare private index/worktree against its initial candidate, allow ignored disposable outputs, preserve child status on combined failure, and reject other mutation. Cleanup verifies and reports the disposable path.
- [x] Exercise local/hosted pass and fail, candidate adapter selection, temporary index, root candidate, missing adapter, unavailable submodule, mutation on callback failure, ignored output, and fail-fast diagnostics.
- [x] Prove fail-fast through a consumer adapter with a named cheap check returning 17 and a later expensive callback writing an external marker. Assert the expensive marker does not exist, stderr contains the specific diagnostic and repair/recheck command, and the status is 17 in local and hosted modes. Update adoption scenarios to distinguish maintained regeneration from disposable builds and explicit repair from acceptance.
- [x] Run `py -3 -m pytest -q skills/tracked-repo-hooks/tests/assets skills/command-bus/tests/assets`. GREEN requires original-state preservation, no apply callbacks, same gate behavior in both modes, disposable-output success, and meaningful diagnostic/status propagation. Keep run output transient. Do not commit yet.

## Task 2: Expose Cheap Checks and Exact Repair Levers in the Marketplace Bus

**Files:** Modify `tools/run.py` and `tests/repository/test_run_cli.py`; touch `tools/ruff_diff.py` and `tests/repository/test_ruff_diff.py` only to share/correct candidate-aware scope while retaining changed-line lint policy. Extend existing test owners rather than add a second bus suite.

**Interfaces:** Retain `run_targets(targets: list[str], ctx: Ctx)`, existing target names, `--base-ref`, wrappers, and explicit diagnostic mode. Extend `Ctx` with `files: tuple[Path, ...] = ()` after existing default fields. Add focused `format` and `normalize` targets and a `--files PATH ...` scope accepted by `lint`, `format`, and `normalize`; reject it for unrelated targets before work. Extend `Task` with defaulted `description: str`, `prerequisites: tuple[str, ...]`, and `side_effects: str`; derive supported modes from its non-empty check/apply implementations. Add `_print_target_help(target: str) -> int`, `_render_command(argv: list[str]) -> str`, `_recheck_command(target: str, ctx: Ctx) -> str`, and `RunnerError.exit_code`. Render Windows hints as executable PowerShell invocations and POSIX hints with shell-safe quoting; hints use `tools/run.py` relative to the author checkout, not the temporary gate path.

- [x] Establish a RED reachability test for the current late `validate` stage. Inject a named cheap validation failure with `subprocess.CalledProcessError(17, ['validator', '--check'])`, make the test-suite runners record execution, and call `_run_ci(Ctx('check', 'origin/main', False, False))`. Assert the failure is propagated and no test-suite runner executes. Add a second failing lint/format case with the same unreachable expensive work. Exercise `main` so the exact code 17 reaches the caller, not just an internal exception.

```python
def test_validation_failure_stops_before_tests(monkeypatch):
    started = []
    original_steps = run._run_steps

    def probe(target, task, steps, ctx):
        if target == "ci":
            return original_steps(target, task, steps, ctx)
        started.append(target)
        if target == "validate":
            failure = subprocess.CalledProcessError(17, ["validator", "--check"])
            raise run.RunnerError(target, "Manual repair required", failure)
        if target.startswith("tests-"):
            pytest.fail("expensive tests ran before the cheap failure")

    monkeypatch.setattr(run, "_run_steps", probe)
    monkeypatch.setattr(run, "_resolve_base_ref", lambda args: "origin/main")
    assert run.main(["ci", "--check"]) == 17
    assert "validate" in started
```
- [x] Split Ruff lint from formatting, keep changed-line lint policy, and add focused `--files` handling over candidate-aware committed/staged scope.
- [x] Add explicit UTF-8 line-ending normalization that excludes binary content, preserves terminal newline count, rejects invalid scopes, and prints selected-path repair/recheck commands.
- [x] Set the complete cheap-first check order and keep every existing validator and test suite; remove duplicate formatting and line-ending work from old stages.
- [x] Preserve child status and original errors, stream output, report failed commands and focused repair/recheck commands, and reject unsupported modes/scopes before target work.
- [x] Replace bare or misleading hints; check-only validation/test targets offer focused rechecks and state when repair is manual.
- [x] Add top-level discovery and target help with truthful mode, prerequisite, side-effect, and scope information; require explicit modes and retain wrappers.
- [x] Exercise real bus repair/recheck commands for inventory, format, and normalization; selected space-containing paths leave other files unchanged.
- [x] Reject outside-root and binary normalization scopes, retain launch failure command/prerequisite context, and prove staged candidate lint fails despite an unstaged repair.
- [x] Run `py -3 -m pytest -q tests/repository/test_run_cli.py tests/repository/test_ruff_diff.py`; 52 tests passed. Do not commit yet.

## Task 3: Migrate the Marketplace Hook and Its Contract Together

**Files:** Modify `githooks/pre-commit`, `.agents/contracts/repo-standards-commands.json`, `tools/check_agent_standards.py`, `tests/repository/test_tracked_hook_candidate.py`, `tests/repository/test_agent_standards.py`, `tests/repository/test_hosted_validation_workflow.py`, `.agents/contracts/standards-certification.md`, `.agents/doctrine/tools.md`, and `.agents/doctrine/plans.md`. Create `tools/hook_gate_adapter.sh`. Change `.github/workflows/marketplace-validation.yml` only as needed to preserve the existing hosted entrypoint, candidate parity, and prerequisite/fail-fast boundaries.

**Interfaces:** Consume Task 1's standalone candidate-preserving seed and check callback plus Task 2's `ci --check` and diagnostic/repair interfaces. Keep Git's no-argument hook entrypoint and this repository's `REPO_STANDARDS_HOSTED_COMMIT=<commit>` workflow input; translate the latter into the seed's hosted mode before validation. Set `REPO_STANDARDS_STAGED_SNAPSHOT=1` for bus checks inside the candidate copy, not as permission to apply. The repository-owned command declaration becomes:

```json
{
  "check": [
    ["@python", "tools/run.py", "ci", "--check"]
  ]
}
```

- [x] Witness RED in `test_tracked_hook_candidate.py`; the migrated hook commits exactly the `git commit --only` candidate and preserves separately staged work.
- [x] Exercise cheap local and hosted rejection with status 17, precise diagnostics, no expensive stage, and unchanged candidate state.
- [x] Migrate the executable root hook to candidate isolation, staged adapter/declaration loading, and the original submodule state guard with repair/recheck guidance.
- [x] Derive the disposable root from the Git common directory and main checkout under canonical `_agent-scratch/<repo>/`, create unique contained children, and clean only the verified candidate directory.
- [x] Implement the check-only adapter with runtime discovery, candidate declaration loading, exact vector validation, and child status propagation.

```python
for declared in commands:
    argv = [sys.executable, *declared[1:]] if declared[0] == "@python" else declared
    result = subprocess.run(argv, cwd=repo_root, check=False)
    if result.returncode:
        raise SystemExit(result.returncode)
```

- [x] Replace the mutative command declaration with the exact check-only vector and reject apply, diagnostics, generated paths, malformed, empty, and contradictory command contracts while retaining structural/semantic distinction.
- [x] Preserve standard selection and existing pins; prepare `HOOK_SOURCE_COMMIT` independently for the later adoption commit. Do not select command-bus as a standard.
- [x] Cover staged adapter/declaration selection, mutation on success/failure, disposable ignored output, protected ignored state, submodule dirty/head drift/uninitialized states, and unavailable submodule objects.
- [x] Run the hosted workflow fixture through the actual hook and adapter; prove exact SHA/clean/detached checks and missing-prerequisite failure before later work.
- [x] Update repository tools/plans doctrine and certification to describe explicit repair, candidate-preserving checks, fail-fast guidance, and current proof boundaries.
- [x] Run the Task 3 repository test command; 92 tests passed under the plan runner. Do not commit before Task 4 regenerates packages and obtains review.

## Task 4: Regenerate, Review, Publish, and Upgrade the Hook Pin

**Files:** Generate `dist/plugins/agent-operating-model/**`, `dist/plugins/superpowers-plus/**`, their existing manifests/catalog surfaces, and any other generator-owned outputs required by `tools/run.py marketplace --apply`. Modify only the tracked-hook entry in `.agents/contracts/operating-standards.json`, `HOOK_SOURCE_COMMIT` in `tools/check_agent_standards.py`, its realistic fixture pin in `tests/repository/test_agent_standards.py`, and the affected certification entry after an immutable source commit exists. Keep this plan and its approved specification in the PR and mark them complete only at agent-owned handoff.

**Interfaces:** Consume the completed canonical source and repository integration from Tasks 1-3. Publication produces a Draft PR against `main`, the exact published head, local hooked proof, fresh whole-diff review, and hosted Linux proof for that head. There is no consumer-wide rollout or user plugin refresh in this task.

- [x] Read the [review runbook](../runbooks/code-review.md), [PR runbook](../runbooks/pr.md), and canonical publication/review capabilities before their steps. Review the diff against the approved spec and this plan, preserving source custody and the scope of the five directly affected skills. Do not retire unrelated active plans or touch their policy text just to remove search hits.
- [x] Run focused tests from Tasks 1-3 and the existing package-build owners as needed for changed source. Run `py -3 tools/run.py marketplace --apply` explicitly outside the hook. Run `py -3 tools/run.py marketplace --check` and `py -3 -m pytest -q tests/shipping/test_aom_tracked_repo_hooks_assets.py tests/shipping/test_aom_command_bus_assets.py`. The packaged hook tests must execute from an isolated consumer without reaching canonical source or an installed cache. Fix source or the owning generator when packages disagree; never patch `dist/` by hand.
- [x] Obtain a fresh independent whole-branch review covering Git state, path containment/cleanup, submodules, staged scope, child failures, exact repair invocations, cheap-check reachability, Windows/Linux parity, and package closure. Use the repository's review workflow; later execution may resolve the required independent review capability through the available reviewer tool or selecting-a-subagent. Re-run a fresh review after corrections. A green test run is not a review. Keep review work products transient outside the repository.
- [ ] Stage the complete intended source, integration, generated outputs, and updated in-flight plan. Commit normally as `feat: make AOM gates preserve candidates and fail fast`. The migrated hook owns the complete staged gate. If it rejects, use its named focused repair/recheck path, inspect and stage the repair, and retry. Do not invoke apply automatically from the hook or skip it. Verify clean status, committed file list, and that the source definitions and generated package bytes are in this commit.
- [ ] Capture the immutable source commit and prove the revised definition exists before using it as a pin:

```powershell
$aomGateSourceCommit = git rev-parse HEAD
git cat-file -e "$aomGateSourceCommit`:skills/tracked-repo-hooks/references/standard.md"
git show "$aomGateSourceCommit`:skills/tracked-repo-hooks/references/standard.md"
```

- [ ] Update only the tracked-validation-hook subscription to `$aomGateSourceCommit`, set the same exact `HOOK_SOURCE_COMMIT` in the repository checker, and keep the other seven standards on their existing pins. Make the positive adoption fixture source the tracked-hook pin from the checked-in subscription while retaining independently authored negative cases for a forged hook pin and malformed commits. The checker still rejects mismatched certified pins; no blanket arbitrary-SHA acceptance is introduced. Certification names the upgraded definition and current implementation without claiming hosted proof before GitHub provides it.
- [ ] Add or extend the existing adoption test to accept the mixed old/new source pins, reject a forged tracked-hook pin, and confirm `git show <recorded-hook-pin>:<definition-path>` resolves the changed definition. Assert semantic invariants or source resolution, not the exact implementation body or hash spelling. Run `py -3 -m pytest -q tests/repository/test_agent_standards.py` after this pin change; inspect the pin diff and verify other entries are untouched.
- [ ] Commit the adoption update normally as `chore: adopt the candidate-preserving hook standard`. This second hooked commit is required because an immutable pin cannot name its own future commit; it is not a per-task receipt or redundant preflight. Verify the final committed tree and clean status.
- [ ] Push the branch, open a Draft PR against `main` with the problem, resulting behavior, and validation boundaries, then attach it to this chat. Verify GitHub's PR head equals the pushed SHA. If the repo's required GitHub capability is unavailable, record that exact missing capability and stop publication rather than claiming the branch is published.
- [ ] Wait for the hosted Marketplace validation at that exact head. Investigate any failure through the same named check/repair path. Fix the owning source, regenerate if needed, commit normally, push, and obtain a fresh review on the corrected diff. If the pinned source definition changes after the source commit, refresh the hook pin to the new existing source commit and recheck pin integrity. Do not claim hosted parity from a local run or an earlier head.
- [ ] Use `completing-planning-artifacts` at closeout. Durable rules already belong in the affected canonical standards/skills and repository doctrine. Mark this plan and its approved specification `completed-awaiting-retirement`, complete every agent-owned checklist item, and retain both artifacts in the completing PR. Commit and push that final status change through the normal hook, verify the published files/head, obtain the final fresh review, and wait for hosted validation at the new final SHA. Report the actual PR URL, final head, local/hosted/review evidence, and any limitation in the chat. Do not add test logs or review scores to these artifacts.

## Handoff Boundary

The planning task ends with this saved, reviewed, committed plan. Implementation begins only after human review authorizes it. Execution recommends `executing-plans` for continuity across the tightly coupled gate migration; the nearest alternative is `subagent-driven-development`, which buys fresh per-task contexts but repeats reconstruction of Git state and diagnostic contracts. The selected lane still requires an independent final review.

The implementation slice ends at a fully reviewable Draft PR with exact-head proof and completed agent-owned obligations. Ready, merge, and verified post-merge worktree retirement remain human-controlled later actions, not unchecked implementation tasks. Keep the isolated branch/worktree available until those actions are authorized.
