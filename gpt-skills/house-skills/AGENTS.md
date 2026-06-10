# AGENTS.md

Scope: `gpt-skills/house-skills/`

This scope covers Harley-authored first-party House Skills sources only.

Defer to the repository root `AGENTS.md` and the parent `gpt-skills/AGENTS.md`
for global doctrine and tree-level guidance.

## Review guidelines

- Flag missing support files referenced by `SKILL.md` before stylistic issues.
- Flag any third-party-origin material, copied excerpt, or adapted source that
  is being treated as first-party House Skills content.
- Flag path drift between the skill source, assets, references, and the source
  ledger used by the marketplace projection.
- Flag false claims that a House Skill was copied verbatim, fully upstream, or
  otherwise source-complete when the repository evidence shows otherwise.

## Unversioned active-root House Skills workflow

- Current active House Skills live at unversioned roots like `gpt-skills/house-skills/<skill-name>/SKILL.md`.
- Current version is recorded in `SKILL.md` frontmatter metadata and mirrored in the source ledger.
- Historical version folders may remain only as provenance or archive residue; do not project them as active names.
- Do not infer active inventory from import-era notes or reconstruction rows.
- Update the designated source, decision, and inventory surfaces that current tooling reads, then regenerate derived projections and validate the result.
- If multiple ledgers exist, treat them as mirrors unless the repo convention explicitly gives one authoritative authority over the others.
