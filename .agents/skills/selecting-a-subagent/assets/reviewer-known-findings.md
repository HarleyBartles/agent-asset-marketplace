# Reviewer known-findings reference

Read this at the start of every full-branch/PR review. It lists the concrete bug classes that Devin auto review tends to catch and that `reviewer-strong` should therefore explicitly look for.

These patterns are repository-agnostic. Marketplace-specific examples (e.g. `tools/new_plugin.py`, `codex-marketplace`) are concrete instances from the authoring repo; in a different consumer repo, map them to the analogous surfaces the PR touches.

## 1. Secrets / real identifiers in source (CWE-200)

- **Title:** Secrets / real identifiers in source
- **Severity:** blocking
- **Owner preflight:** `tools/review_preflight.py` (`_scan_security`).
- **Owner lens:** `reviewer-security`.
- **Portable:** yes (concept; examples are repo-local).

- A real Discord guild, server, channel, or user snowflake ID in a `.md` reference file. These are 17–20 digit numbers, often paired with words like `guild_id`, `server_id`, `channel_id`, `user_id`, or a specific server name.
- API keys, tokens, `password`, `secret`, `private_key`, or email addresses anywhere in the diff.
- Any identifier that is redacted in one file but present in another.
- **Correct pattern:** `<DISCORD_GUILD_ID>` or an instruction to read from the `DISCORD_GUILD_ID` environment variable.

## 2. `SKILL.md` frontmatter schema

- **Title:** `SKILL.md` frontmatter schema
- **Severity:** important
- **Owner preflight:** `tools/review_preflight.py` (`_scan_skill_frontmatter`).
- **Owner lens:** `reviewer-skills`.
- **Portable:** yes (all `SKILL.md` files carry this schema).

- `license` must be a top-level key, not inside `metadata:`.
- `name` and `description` must be top-level.
- `metadata` should only contain skill-policy fields (`source-id`, `source-path`, `provenance-name`, `source-category`, `status`, `owner`, `scope`, `use_when`, `do_not_use_when`, `related_skills`).

## 3. Marketplace tooling (`tools/new_plugin.py`, `tools/run.py`, scaffolders)

- **Title:** Marketplace tooling
- **Severity:** important
- **Owner preflight:** `tools/review_preflight.py` (`_scan_new_plugin`).
- **Owner lens:** `reviewer-marketplace`.
- **Portable:** no (this repo's tooling).

- Error paths must return a non-zero exit code; `--check` / dry-run paths should not mask errors with `0`.
- The `--sync` / manifest-refresh command must not refuse to run in a normal repository clone.
- `new_plugin.py` should not scaffold packs with `enabled: True` by default; new packs should be opt-in.
- Manifest regeneration (`--sync`) must preserve existing top-level author, license, notes, and provenance fields.

## 4. Cross-skill script paths

- **Title:** Cross-skill script paths
- **Severity:** important
- **Owner preflight:** `tools/review_preflight.py` (`_scan_stale_paths`, `_scan_canonical_paths`).
- **Owner lens:** `reviewer-marketplace`.
- **Portable:** no (paths are repo-local conventions).

- References to helper scripts and skill assets must use the current canonical path. In this repo, use `.agents/skills/...` for skill assets and `subagent-workspace/scripts/...` for workspace helpers such as `sdd-workspace`, `task-brief`, and `review-package`.
- Watch for stale `subagent-driven-development/scripts/...` paths in prompts and `SKILL.md` files.

## 5. Reference file hygiene

- **Title:** Reference file hygiene
- **Severity:** important
- **Owner preflight:** `tools/review_preflight.py` (`_scan_markdown_tables`, `_scan_py3_convention`).
- **Owner lens:** `reviewer-skills`.
- **Portable:** yes (markdown and `py -3` conventions).

- Markdown table rows must begin and end with `|`. A line with `|` that does not end with `|` is a malformed table row.
- Prefer the repo's `py -3` convention in runnable examples (e.g. `py -3 -m playwright`). Do not omit the `-3` qualifier.
- No real IDs or secrets in examples or maps.

## 6. Script path safety

- **Title:** Script path safety
- **Severity:** important
- **Owner preflight:** `n/a`.
- **Owner lens:** `reviewer-skills`.
- **Portable:** yes (script safety patterns).

- A PowerShell script that `Push-Location`s into a repo root and then writes to a relative `$OutFile` must resolve `$OutFile` to a full path before changing location.
- Bash/PowerShell scripts that write UTF-8 text for subagent `read` should not emit a BOM.

## 7. Spec / plan drift

- **Title:** Spec / plan drift
- **Severity:** blocking
- **Owner preflight:** `n/a`.
- **Owner lens:** `reviewer-strong`.
- **Portable:** yes (scope must match the documented design).

- If the PR references a plan or spec, the implemented scope must match it. New packs, renamed surfaces, or dropped features that are not in the plan should be flagged as out of scope.

## 8. Prompt robustness

- **Title:** Prompt robustness
- **Severity:** important
- **Owner preflight:** `n/a`.
- **Owner lens:** `reviewer-skills`.
- **Portable:** yes (read-only prompt conventions).

- Read-only review prompts should not instruct the subagent to run `git` commands or `find_file_by_name` to recreate a missing diff package. The prompt should say: if the package is missing, report it and stop.
- Subagent prompts should not ask a read-only profile to install, write, or mutate files.

## 9. `SKILL.md` `metadata` block

- **Title:** SKILL.md metadata block
- **Severity:** important
- **Owner preflight:** `tools/review_preflight.py` (`_scan_skill_metadata`).
- **Owner lens:** `reviewer-skills`.
- **Portable:** yes (all `SKILL.md` files carry this schema).
- **Permitted `metadata` keys:** `source-id`, `source-path`, `provenance-name`, `source-category`, `status`, `owner`, `scope`, `use_when`, `do_not_use_when`, `related_skills`.
- A missing `metadata:` key is allowed.
- Reject present `metadata: `, `metadata: null`, `metadata: ~`, and `metadata: {}` values.
- Reject any unexpected keys inside `metadata`; only the permitted skill-policy keys listed above are allowed.
