# Command Bus Standard Assets Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship an optional, repository-editable command bus starter that demonstrates the adopted CLI contract without requiring Python, a fixed filename, shared target ABI, or any other AOM standard.

**Architecture:** `command-bus` owns an optional Python CLI bootstrap, sample external-command targets, and behavior tests for dispatch semantics. The starter launches targets as subprocesses based on repository-owned metadata; it does not import a target module or install/register targets. Adoption guidance describes selecting, adapting, replacing, or omitting the starter and self-certifying the repository-owned CLI.

**Tech Stack:** Python standard library for the optional bootstrap, pytest for subprocess behavior coverage, existing Marketplace builder.

**Spec:** [Approved AOM design](../../specs/2026-09-30-aom-standard-adoption-and-shipping.md).

**Roadmap:** [AOM adoption and shipping](roadmap.md), Plan 3. Planning baseline is Plan 2 closeout commit `f31fa8136`; implementation baseline is Plan 2 reviewed head `d6f8947f1`.

**Execution Strategy:** `executing-plans`, because metadata, argument parsing, subprocess behavior, examples, and shipping tests share one CLI contract and require a connected end-to-end test loop. Inline continuity reduces the chance that the sample target protocol drifts from its dispatcher. Obtain a fresh whole-change review before handoff.

## Global Constraints

- Command bus is independently selectable. This plan does not adopt hook/CI or require any hook, workflow, or normalizer asset.
- The repository implements a CLI under `tools/`; its language, filename, target set, and integration structure are repository-owned.
- This Python implementation is an optional bootstrap. It is not a standard requirement or a permanent dependency on AOM.
- Provide top-level `--help`, discoverable targets, and `<target> --help`. Help states purpose, supported modes, prerequisites, side effects, and target-specific arguments without running target work.
- A selected target requires one explicit supported mode or a help request. Without a mode, show usage and exit nonzero. A bare bus invocation may show top-level help.
- `--check` assesses without correcting maintained repository files. `--apply` performs documented changes. Optional `--dry-run` previews a meaningful mutation; a proposed change alone is not failure.
- Check-only and apply-only targets are valid. Reject unknown targets, duplicate/conflicting modes, and unsupported modes before target work.
- Forward target arguments faithfully, inherit stdout/stderr, and return the target's exact exit status. Never report required failed or skipped work as success.
- Target integration is an explicit repository task. No automatic install, file scanning, multi-target orchestration, dependency graph, fixed config JSON, source submodule, or shared module ABI.
- Edit canonical skills and `src/plugin-definitions/`, regenerate `dist/`, and use the normal commit hook for the full repository gate.

## Review Focus

- Help and rejected requests must not start targets or mutate files; Task 1 uses side-effect counters for those paths.
- Arguments and exit codes must survive the bus unchanged, including when an argument resembles a mode after the `--` target-argument separator; Task 1 tests exact argv and status.
- Targets may be implemented in another language or expose only one mode; Task 1 verifies external subprocess dispatch and check-only/apply-only behavior without a shared Python ABI.
- The installed plugin must work without source-checkout imports or a Marketplace `PYTHONPATH`; Task 2 copies and executes the package in isolation.

## File and Interface Map

| Owner                | Deliverable                                                                                                                                                             |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skills/command-bus` | `assets/tools/run.py`, `assets/tools/targets/` sample commands, `tests/assets/test_command_bus.py`, `tests/evaluator-only/adoption-scenarios.md`, and adoption guidance |
| AOM plugin package   | `tests/shipping/test_aom_command_bus_assets.py` proving the optional starter and sample commands work from an isolated plugin copy                                      |

The Python starter accepts `run.py [--help]` or `run.py <target> (--help|--check|--apply|--dry-run) [-- <target-arguments>...]`. A bare invocation prints top-level help. A selected target requires exactly one mode or a help request. Mode options are bus-owned; tokens after `--` are child arguments. The starter's local `TARGETS` mapping uses `command` (an argv vector), `description`, `supported_modes`, `prerequisites`, `side_effects`, and `argument_help`. It is an implementation detail of this Python starter, not a standard manifest or ABI. Other languages can be invoked as ordinary child processes. No other repository's bus is expected to consume this mapping.

## Task 1: Python bus bootstrap and CLI behavior

**Files:** Add `skills/command-bus/assets/tools/run.py`, sample targets `check_status.py`, `apply_change.py`, and `preview_change.py` under `assets/tools/targets/`, and `skills/command-bus/tests/assets/test_command_bus.py`. Update `skills/command-bus/SKILL.md` and `references/standard.md` only where needed to distinguish the sample registry from the standard interface.

**Consumes:** The `command-bus` definition and approved CLI requirements in spec section 6.7.

**Produces:** A standard-library-only dispatcher with a concrete but editable subprocess target table and sample targets exercising distinct mode subsets.

- [ ] Add subprocess behavior cases for bare bus help, target listing, target help, check-only target, apply-capable target, optional dry-run target, selected target with no mode, duplicate/conflicting modes, unknown target, unsupported mode, and malformed command metadata.
- [ ] Add target fixtures that record their received argv and a side-effect file. Assert help, missing mode, conflicting mode, unknown target, and unsupported mode never create or modify the side-effect file.
- [ ] Implement target selection syntax `run.py <target> <mode-or-help> [-- <target-arguments>...]`. Consume only the selected target and its single bus mode; forward argv tokens after `--` exactly and reject unexpected bus-level tokens before starting the target. Resolve relative command paths from the copied bus script's directory so the starter works when copied with its targets.
- [ ] Implement the `TARGETS` mapping fields `command`, `description`, `supported_modes`, `prerequisites`, `side_effects`, and `argument_help`. Require a non-empty supported-mode list containing only `check`, `apply`, or `dry-run`; validate that command is a non-empty argv list of strings and that all help fields are present before any command starts. Keep invocation subprocess-based and do not import Python target modules.
- [ ] Implement side-effect-free top-level and target help. Target help explains its supported modes and target arguments using registry metadata; it never invokes the child command.
- [ ] Invoke targets with inherited stdout and stderr. Return the child process's exact exit status. Reject unsupported or multiple mode arguments before process creation.
- [ ] Demonstrate check-only and apply-only targets. For the dry-run sample, report proposed state and return success when mutation would be proposed; fail only for an actual preview error.
- [ ] Run `py -3 -m pytest -q skills/command-bus/tests/assets/test_command_bus.py`, Ruff on changed Python files, and verify all scripts use only standard-library imports.

**Exit:** The starter exemplifies the interface while leaving target discovery/implementation language and orchestration policy under repository ownership.

## Task 2: Adoption and isolated package proof

**Files:** Add `skills/command-bus/tests/evaluator-only/adoption-scenarios.md`, `tests/shipping/test_aom_command_bus_assets.py`, and update the generated AOM plugin projection.

**Consumes:** Task 1 dispatcher, sample targets, and standard guidance.

**Produces:** Evidence that the bus starter is useful outside the Marketplace source checkout and remains optional.

- [ ] Record fresh-context adoption scenarios in `skills/command-bus/tests/evaluator-only/adoption-scenarios.md`: select and adapt the Python starter; implement another-language bus without AOM assets; and adopt command bus without hook/CI. Define expected decisions in terms of the standard and approved spec, not exact response wording.
- [ ] Run each adoption scenario in a fresh context. Confirm selection adds only the chosen standard to the subscription record and root AGENTS router, records certification only after the selected implementation exists, and does not require or imply neighboring standards.
- [ ] Verify the bus-only scenario does not create a pre-commit hook, CI workflow, or text-normalization policy.
- [ ] Copy the generated `dist/plugins/agent-operating-model` package to a temporary install location. Execute the copied bus and sample targets from a temporary consumer with Marketplace `PYTHONPATH` removed and no source checkout available.
- [ ] Verify package-internal skill links resolve, runtime files are generated from canonical source, sample subprocesses preserve arguments/status, and evaluator-only material is not shipped.
- [ ] Update the skill entrypoint to explain the optional Python starter, repository-owned target integration, agent-led deployment, no ABI promise, and explicit self-certification obligations.
- [ ] Run the focused CLI suite and shipping test, then `py -3 tools/run.py marketplace --apply`; inspect the generated package and source parity.

**Exit:** Repositories can opt into the bus contract without adopting the Python starter, and those selecting the starter can copy and modify it without access to the Marketplace source tree.

## Task 3: Commit and whole-change review

**Files:** Plan-tracked source, tests, evaluator-only notes, and generated AOM plugin projection from Tasks 1-2.

**Consumes:** Passing focused and isolated shipping evidence.

**Produces:** A reviewable, independently usable command-bus asset delivery.

- [ ] Inspect staged paths for scope and generated/source parity, then commit through the normal repository hook. Do not run the full gate redundantly before or after a successful hooked commit.
- [ ] Obtain a fresh whole-change review against this plan and the approved spec. Fix Critical and Important findings, regenerate outputs, rerun focused evidence, and request a fresh review after corrections.
- [ ] Mark this plan `completed-awaiting-retirement`; update its roadmap row with the final implementation head and review outcome.

**Exit:** The command-bus definition has a useful optional implementation starter and adoption evidence without implying repository installation or choosing consumer architecture.

## Handoff boundaries

- This plan ships command-bus assets only. It does not ship or adopt hook/CI, pre-commit launchers, hosted workflows, or normalization tooling.
- The following hook/CI slice may offer a standalone target command that a repository with a bus can integrate explicitly. It must also remain usable without command-bus adoption.
- The existing Marketplace implementation remains on its current v1/runtime path until the later Marketplace migration plan explicitly reconciles it.
