# Tools CLI contract validator

## Problem

`tools/` is the repo's local build and validation harness, but there is no
machine check that the tools share a consistent CLI shape. Some tools are
invoked directly by `tools/run.py`; some are never meant to be run directly.
There is no validation that:

- direct-invocation tools support `--help`, `--check`, and `--apply` consistently.
- `tools/run.py` passes `--check`, `--apply`, and `--allow-shared-checkout` down
  to the sub-tools it calls.
- flags like `--force` and `--allow-shared-checkout` are documented consistently.

This is the same class of problem the skill-bundled validator already solves for
`.agents/skills/*/scripts/*.py`, but for a different surface.

## Goal

Add a validator for `tools/*.py` that mirrors the skill-bundled validator. It
should run as part of `py -3 tools/run.py ci --check` and fail the build if a
tool's CLI contract is broken or if `tools/run.py` miscomposes flags.

## Non-goals

- Do not validate `tools/run.py` itself recursively.
- Do not validate helper modules inside `tools/` (e.g. `marketplace_utils.py`).
- Do not change the skill-bundled validator.
- Do not require tools to be importable as library modules.

## Design

### Lane discriminator

Use the same convention as the skill-bundled validator: a `tools/*.py` file is a
**CLI** if it contains an `if __name__ == "__main__":` block; otherwise it is a
helper and is ignored by this validator.

### Tool CLI contract

Direct-invocation `tools/*.py` must support:

- `--help` exits `0` and contains a `usage:` line.
- `--help` text states whether the tool is `read-only`, `mutating`, or `mixed`.
- `--check` is the default, read-only, idempotent mode:
  - reports what the tool would do,
  - exits `0` when no changes are needed,
  - exits non-zero when work would be required or an error is detected.
- `--apply` is the explicit mutating mode, where the tool can make changes.
- `--force` is supported by tools that may overwrite existing, drifted surfaces.
- `--allow-shared-checkout` is supported by tools that may write to a shared or
  main worktree, and it must require `--apply`.

Tools that are purely read-only (e.g. validators) do not need `--apply`,
`--force`, or `--allow-shared-checkout`.

### `tools/run.py` composition contract

`tools/run.py` is the composition point. It must:

- Forward `--check`, `--apply`, and `--allow-shared-checkout` to the
  sub-invocation of any `tools/*.py` that supports those flags.
- Not silently drop `--apply` or `--allow-shared-checkout` when a task
  delegates to a Python tool.
- Support `--help` and `--check` for every task in `_TASKS`.
- Report each sub-tool's return code in `--verbose` mode.

The validator does not need to execute every task; it can inspect `_TASKS` and
the argument-parsing code in `tools/run.py` to confirm the flags are declared.
End-to-end forwarding is exercised by `tools/run.py ci --check`.

### Validator

Create `.agents/skills/repo-standards/scripts/validate_tool_cli.py` or a new
tool `tools/validate_tool_cli.py` (decision for the planning agent). The
validator:

- Globs `tools/*.py`.
- Splits each file into CLI or helper using the `__main__` guard.
- For CLI files, runs `--help` and `--check`, checks for the classification
  string, and records `OK / WARN / FAIL`.
- For `tools/run.py`, statically or dynamically checks that the standard flags
  are defined and that every task in `_TASKS` has `check` and `apply` steps.
- Prints a summary line: `OK: N  WARN: N  FAIL: N`.
- Exits `0` only if no `FAIL` findings.

### Files to touch

- New validator: `tools/validate_tool_cli.py` or
  `.agents/skills/repo-standards/scripts/validate_tool_cli.py`.
- `tools/run.py` to register the new check under the `ci` task.
- `tools/run.py` argument forwarding, if gaps are found.
- Individual `tools/*.py` files that fail the new validator.
- `tools/README.md` to document the contract.

### Validation

- `py -3 tools/validate_tool_cli.py --check` runs locally with no FAILs.
- `py -3 tools/run.py ci --check` includes the new validator and passes.

### Handoff

The planning agent should produce a plan that first drafts the validator, then
fixes each failing tool one at a time. The `tools/run.py` composition check may
require a separate task.
