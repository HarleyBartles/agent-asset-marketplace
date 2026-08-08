# Skill-bundled script two-lane validator

## Problem

`.agents/skills/<skill>/scripts/*.py` contains two kinds of files, but
`validate_skill_scripts.py` treats every `.py` as a CLI. This produces two kinds
of noise:

- **WARN** on 13 CLI scripts whose `--help` does not declare a
  `read-only` / `mutating` / `mixed` classification.
- **DEFERRED** on 6 helper modules (`_agents_md.py`, four `shared_checkout.py`
  files, and `validate_skill_scripts.py` itself) that are imported by other
  scripts, not executed from the command line.

The `DEFERRED` list is an explicit workaround. It tells the validator to ignore
files that should never have been checked as CLIs in the first place.

## Goal

Make `validate_skill_scripts.py` validate the right contract for the right
file. The `py -3 tools/run.py ci --check` output should show only `OK` lines for
skill `scripts/`, with no `WARN` or `DEFERRED` entries.

## Non-goals

- Do not introduce a new skill directory such as `lib/`; skill canonical
  directories are `SKILL.md`, `agents/`, `references/`, `scripts/`, `assets/`.
- Do not move helper modules out of `scripts/`.
- Do not expand the validator to `tools/` or root `scripts/`.

## Design

### Lane discriminator

A file is a **CLI** if it contains an `if __name__ == "__main__":` block.
Otherwise it is a **helper**.

The current `.agents/skills/*/scripts/*.py` already follows this convention:
- CLI scripts have `if __name__ == "__main__":`.
- `_agents_md.py` and `shared_checkout.py` do not.
- `validate_skill_scripts.py` does, so it belongs in the CLI lane.

### CLI lane contract

Same contract as today, in `2026-08-04-skill-script-cli-contract-design.md`:

- `--help` exits `0` and contains a `usage:` line.
- `--help` declares a classification: `read-only`, `mutating`, or `mixed`.
- `--check` does not exit `2` (which means the parser rejected the argument).
- The default mode is `--check` when neither `--check` nor `--apply` is passed.

### Helper lane contract

Helpers are not expected to support `--help` or `--check`. They must:

- Be importable without side effects.
- Have a leading module docstring.
- Not import `argparse` or define a command-line parser.
- Not contain an `if __name__ == "__main__":` block (this is the lane signal).

### Validator changes

- Rename the `DEFERRED` set to `HELPERS` or remove it entirely; the validator
  determines the lane from the file content.
- For each `scripts/*.py`:
  - If it has `if __name__ == "__main__":`, run the CLI lane.
  - Otherwise, run the helper lane.
- Report status per lane: `CLI OK / CLI WARN / CLI FAIL / HELPER OK / HELPER FAIL`.
- Overall exit code is `0` only if there are no `FAIL` findings.
- Remove stale `DEFERRED` entries for files that are not in `.agents/skills/*/scripts/`
  (`unslop.py`, `validate_package.py`, `validate_unslop_output.py`).

### Affected CLI scripts for the WARN fix

Add a classification string to the `--help` output of these 13 scripts, usually
in the `argparse.ArgumentParser(description=...)` or `epilog=`:

- `.agents/skills/generating-agent-mesh/scripts/generate_index_mesh.py` — `mixed`
- `.agents/skills/iterative-review/scripts/next_node.py` — `mixed`
- `.agents/skills/iterative-review/scripts/resolved_ledger.py` — `mixed`
- `.agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py` — `mixed`
- `.agents/skills/repo-standards/scripts/repo_standards.py` — `mixed`
- `.agents/skills/repo-standards/scripts/scaffold_agents_md.py` — `mixed`
- `.agents/skills/repo-standards/scripts/scaffold_ci_preflight.py` — `mixed`
- `.agents/skills/repo-standards/scripts/scaffold_contributing.py` — `mixed`
- `.agents/skills/repo-standards/scripts/scaffold_gitignore.py` — `mixed`
- `.agents/skills/repo-standards/scripts/scaffold_marketplace_json.py` — `mixed`
- `.agents/skills/repo-standards/scripts/scaffold_repo_runbook_policy.py` — `mixed`
- `.agents/skills/repo-standards/scripts/scaffold_review.py` — `mixed`
- `.agents/skills/repo-standards/scripts/scaffold_runbooks.py` — `mixed`

Classification choices:
- `mixed` for scripts with `--check` (read-only) and `--apply` / `--force`
  (mutating).
- `read-only` for scripts that only report and never mutate.
- `mutating` for scripts that write by default and have no `--check`.

All 13 above are `mixed`.

### Files to touch

- `.agents/skills/repo-standards/scripts/validate_skill_scripts.py`
- The 13 CLI scripts listed above.
- `.agents/skills/repo-standards/references/skill-script-contract-validator.md`
- `.agents/doctrine/skill-standards-policy.md` (helper contract paragraph)

### Validation

- `py -3 .agents/skills/repo-standards/scripts/validate_skill_scripts.py --check`
  reports only `OK` and `HELPER OK` lines.
- `py -3 tools/run.py ci --check` passes and the `repo-standards` section shows no
  `WARN` or `DEFERRED` lines.

### Handoff

The planning agent should use `writing-plans` to produce a task plan with the
smallest possible task-per-file: one task for the validator rewrite, one task
per skill to add the 13 classifications, one task for reference updates.
