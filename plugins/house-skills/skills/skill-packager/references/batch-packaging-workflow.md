# Batch Packaging Workflow

Use this reference when packaging multiple skills, especially under `skill-buster` batch mode.

## Preparation before handoff

Prepare every package in the current batch before emitting the handoff stack. Package each skill independently with the wrapper:

```bash
python /home/oai/skills/skill-packager/scripts/package_and_verify_skill.py <skill-folder> <external-dist-dir>
```

Use a separate external dist directory for each skill. Do not put dist, build, `skill.zip`, or `package-evidence.json` inside the staged skill root.

A package is prepared only after the wrapper succeeds and the exact `skill.zip`, `package-evidence.json`, and `package-run-receipt.json` agree on path, size, SHA-256, target skill, and archive inspection.


## Preparation unit and throughput posture

`skill-packager` is a single-target packager. Even in batch work, one wrapper invocation packages one skill folder into one target-specific external dist directory. Batch mode means repeated independent preparation units, not a multi-root package operation.

```yaml
preparation_unit:
  target_skill: one skill
  staged_source_path: one folder
  dist_dir: one target-specific external directory
  wrapper_invocation: one
  expected_outputs:
    - skill.zip
    - package-evidence.json
    - package-run-receipt.json
```

Use a bounded preparation window to avoid wasting wall-clock time on overloaded multi-package runs. Default to a window of one skill when the session has recently seen timeouts, slow package runs, or heavy context load. A larger window is an efficiency choice only when recent wrapper runs are quick and clean; it is never a validation shortcut.

If a timeout occurs or a wrapper run approaches timeout, treat it as wasted-wall-clock prevention rather than queue poison. Reduce the preparation window to one, retry that same item in isolation, and continue serially after success. Park only the repeatedly slow item if a real repair is needed. Do not manually zip, reuse stale package evidence, skip validator evidence, or treat timeout retries as package proof.

## No-improvisation rule

Do not hand-run six scripts for every batch item during normal work. Do not build a local alternate packager. Do not reuse stale archives from earlier poisoned or interrupted batches. The wrapper exists so agents have one deterministic packaging route and one machine receipt per item.

If the wrapper reports a timeout or slow substep, classify it as a preparation efficiency problem unless the receipt shows a real source/package defect. The normal response is to shrink the preparation window, rerun the same item in isolation, and use the receipt to identify the slow step. A timed-out run is not handoff evidence and the item is not prepared, but the queue itself is not poisoned before the handoff cursor starts.

## Handoff boundary

Packager supplies archive identity evidence; skill-buster owns lifecycle state. The package handoff surface must be a normal assistant message controlled by skill-buster.

Do not treat an inert cursor-advance pulse as package evidence, package validation, or package mutation. A pulse with no package link, no package path, no source inspection, no external side effect, and no manifest change does not alter package validity.

A wrong-surface package link is different: if a `skill.zip` link is printed in tool output, logs, comments, canvas, widgets, or another non-assistant-message surface, the package may still be valid on disk but the handoff is not valid.

## Confirmation

A package handoff is `presented`, not `done`, until the user confirms install or acceptance, unless the user explicitly made packaging alone the completion condition.

## Wrapper efficiency expectation

The normal wrapper is expected to avoid duplicate validation and avoid one subprocess per local check when integrated local calls are available. If package preparation repeatedly consumes the outer tool timeout, repair wrapper performance or shrink the preparation window; do not make agents litigate a custom packaging route.
