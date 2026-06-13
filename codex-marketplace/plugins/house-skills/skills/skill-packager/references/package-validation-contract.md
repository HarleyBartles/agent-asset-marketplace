# Package Validation Contract

Use this contract before handing a skill package to `skill-buster` or the user.

## Normal command

Use the wrapper for ordinary packaging:

```bash
python /home/oai/skills/skill-packager/scripts/package_and_verify_skill.py <skill-folder> <external-dist-dir>
```

The wrapper is the normal agent-facing route. It runs the required checks in order inside one integrated single-target process, applies per-step timeouts plus a wrapper-level budget, records the active `current_step`, and writes machine evidence. Do not replace it with a hand-written sequence unless you are debugging the wrapper itself.

## Required successful outputs

A successful run must leave these files in the external dist directory:

- `skill.zip`
- `package-evidence.json`
- `package-run-receipt.json`

Before handoff, confirm:

1. `skill.zip` exists, is a regular file, and is nonzero.
2. `package-evidence.json` exists and its `package_path` equals the exact `skill.zip` path.
3. A freshly recomputed SHA-256 of `skill.zip` equals `package_sha256` in `package-evidence.json`.
4. `package-run-receipt.json` has `ok: true` and names the same package path and SHA.
5. If the skill has bundled scripts, the receipt contains a passing `script_architecture_lint` step.
6. The archive inspection step passed and the archive contains exactly one top-level folder.

## Timeout behavior

If a wrapper substep times out or the wrapper budget is exceeded, classify it as a preparation-efficiency event unless the receipt shows a real staged-source defect. The wrapper receipt should identify the active or timed-out step and elapsed time. Reduce the preparation window, retry the same item in isolation, and use the receipt to diagnose repeated failures. Do not route around the timeout with manual zipping, stale package paths, copied receipts, or assistant-written ledger text.

Common timeout causes are unbounded source-tree scans, generated output directories inside the staged skill root, large text files that should be assets or external data, and accidental nested package artifacts. The current scripts use bounded traversal and skip known output/cache folders, but staged source still must not contain build or package output.

## Handoff facts

Package evidence proves archive identity. It does not prove user-visible handoff success. Skill-buster owns assistant-message handoff surface, cursor cadence, optional inert cursor-advance pulses, and presentation state.

## Performance and receipt hardening

The wrapper should not rely on the outer tool timeout as its first failure signal. It records `current_step` before each step begins, clears it after the step is recorded, and writes `total_elapsed_seconds` on success. Wrapper performance regressions should be repaired in the wrapper rather than by asking agents to run the internal scripts manually.


## Script architecture lint

When a staged skill contains `scripts/`, the wrapper runs `scripts/script_architecture_lint.py`. This check protects normal agent use from script-backed skills that force implementation reading, custom helper scripts, or inefficient execution.

The lint fails high-confidence defects: scripts not named from `SKILL.md` or references, missing normal-use/discovery recipes, Python scripts that can create `__pycache__`, recursive walks outside `safe_skill_tree` helpers, and subprocess helper calls without explicit timeouts. It may warn on whole-file reads, multiple-script lane ambiguity, or subprocess process-tree cleanup concerns.

A script-backed skill should expose the normal command, input shape, output/receipt shape, and debug-only script-reading rule outside script source. The lint is not a substitute for semantic validation; it is a packaging-time architecture guard that makes bad script surfaces visible before handoff.
