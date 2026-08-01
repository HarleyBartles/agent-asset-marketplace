# Skill-bundled script CLI contract

## Problem

Agents that carry skills into arbitrary consumer repos should not have to read
a script's source to decide whether it is safe to run. That is an anti-pattern:
it leaks implementation detail into agent reasoning, it is fragile across script
updates, and it makes cross-repo usage error-prone because the consumer repo
cannot easily patch the skill script.

## Goal

Every script shipped inside a skill bundle must be trustworthy through a
self-describing, machine-readable CLI contract. An agent should be able to
answer these questions without opening the file:

1. What does this script do?
2. What flags/arguments does it accept?
3. Does it mutate the working tree or the repo?
4. What would it do if I ran it with the current arguments (`--check`) ?
5. Is it idempotent and safe to retry?

## Contract

Each skill-bundled script (under `sources/first_party/skills/<skill>/scripts/`
and its projected copies) must:

1. **Advertise with `--help`**
   - Print a concise description of the script's purpose.
   - List every flag and positional argument with a one-line explanation.
   - State whether the script mutates the working tree, the repo, or external state.
   - Exit `0` on successful help and `2` on unknown arguments.

2. **Support `--check` (dry run / inspect mode)**
   - Report what the script _would_ do without changing files.
   - Produce a machine-parseable summary (plain `OK` / `Would ...` lines, and
     optionally `--json` for structured output in a future revision).
   - Exit `0` when the check passes (no changes needed), non-zero when the
     script would need to make changes or when an error is detected.

3. **Support `--apply` (or equivalent) for mutation**
   - Make the default behavior safe: `check` if neither `--check` nor `--apply`
     is passed.
   - This is already the convention in `refresh_installed_skills.py` and should
     become the standard for all skill-bundled scripts.

4. **Declare safety in help**
   - Classify each flag as `read-only` or `mutating`.
   - State the script's idempotency and whether it is safe to run on a dirty
     working tree.

5. **Be discoverable from `SKILL.md`**
   - The skill doc lists each bundled script with its purpose, safe invocation,
     and a pointer to `--help`.

## Scope for Phase 3

- Audit existing `sources/first_party/skills/*/scripts/*` for `--help` and
  `--check` support.
- Standardize the parser convention (argparse with `check`/`apply` distinction,
  consistent help text format).
- Add a validator to `tools/run repo-standards` that ensures every script in a
  skill bundle responds to `--help` and `--check` and returns the expected exit
  codes.
- Update skill-authoring standards to require the contract.

## Out of scope

- Rewriting scripts that are already read-only helpers (e.g. `sdd-workspace`)
  unless they lack `--help`.
- Adding `--json` output in the first pass; keep output human-readable but
  structured enough to be greppable.

## Related Phase 3 note: vendor profile deployment ownership

Phase 2 placed the actual copy/clean of vendor subagent profiles in
`refreshing-installed-skills` because that script already walks installed
plugin packs. The long-term owner should be `repo-standards`, which is the
skill that defines one-shot repo shape and canonical surface deployment. Phase
3 should move the `assets/profiles/*.md` -> `.agents/agents/` deployment logic
into a `repo-standards` script (either an extension of `repo_standards.py` or a
sibling `deploy_vendor_profiles.py`) and leave `refreshing-installed-skills`
to record the `vendorProfiles` provenance.

## References

- `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`
  already follows the `check`/`apply` pattern and is the reference shape.
- `docs/skill-standards-policy.md` should be updated to include this contract.
