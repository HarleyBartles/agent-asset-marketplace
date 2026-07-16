# MARK-160 Repo Receipt Skill Plan

Goal: add `codex-repo-receipts` as a first-party receipt skill with canonical source custody in House Skills, required projection into the `repo-worker-base` plugin, and optional projection into `superpowers` only where that bundle already carries first-party compositional workflow skills.

## Scope

- Canonical editable source: `codex-marketplace/plugins/house-skills/skills/codex-repo-receipts`
- Required delivery target: `codex-marketplace/plugins/repo-worker-base/skills/codex-repo-receipts`
- Optional delivery target: `codex-marketplace/plugins/superpowers/skills/codex-repo-receipts`
- Repo-root registration: `codex-marketplace/plugin-roots.json`, generated marketplace manifest, and zip registry
- Source/projection evidence: House Skills decisions, intake, and provenance records

## Non-goals

- Do not create `sources/first_party/skills/superpowers/`
- Do not move canonical first-party custody out of House Skills
- Do not broaden validators to invent a new source-custody lane
- Do not edit the Linear "Open in Codex Desktop" prompt template

## Work plan

1. Confirm the current repo-worker-base vendored plugin surface from the existing remote branch and bring it into the working branch.
2. Mirror `codex-repo-receipts` from the canonical House Skills source into the repo-worker-base plugin.
3. Keep the existing Superpowers projection only as an optional first-party projection from the House Skills source.
4. Register the new active plugin root and regenerate the marketplace manifests and generated skill artifacts.
5. Refresh the House Skills source ledger and provenance notes so the canonical source and projections remain aligned.
6. Write the matching implementation record under `docs/superpowers/records/`.

## Validation

- `py -3 tools/update_skill_artifacts.py --all`
- `py -3 tools/validate_marketplace.py`
- `py -3 tools/validate_repo_index.py`
- `py -3 tools/validate_generated_drift.py --base origin/main`
- `git diff --check`

## Evidence to capture

- final branch name
- starting main SHA
- final head SHA
- changed files
- generated artifacts
- validation commands and results
- any skipped checks and the reason
