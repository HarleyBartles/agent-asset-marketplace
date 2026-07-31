# First-Party Skill Source Format

This directory is the active source-custody surface for first-party skills.

Use these rules when editing or adding a first-party skill under
`sources/first_party/skills/<skill-name>/`.

## Canonical source shape

- One current root per skill.
- The current root is the source of truth; plugin projections and generated
  surfaces are derived from it.
- Historical or retired names belong in provenance, archive, or history
  surfaces, not in active first-party source roots.

## `SKILL.md` frontmatter

- `name` is required and should be the current kebab-case skill name.
- `description` is required and should be discoverable, concise, and rich
  enough to surface explicit `use when` and `do not use when` triggers.
- `metadata` is required for first-party skills in this repo and should be a
  mapping, not a loose grab bag.
- Prefer rich structured metadata under `metadata` when it helps provenance,
  routing, or cataloging.
- `metadata` may contain arbitrary nested objects, arrays, and fields as long
  as they stay consistent with the skill's canonical role.
- Keep canonical identity fields stable:
  - `source-id`
  - `source-path`
  - `provenance-name`
  - `source-category`
  - `status`
  - `owner`
- Additional fields are welcome when they help routing or provenance:
  - `scope`
  - `use_when`
  - `do_not_use_when`
  - `related_skills`
  - `notes`
- The `normalize_first_party_skill_sources.py` tool only preserves whitelisted
  metadata fields. When adding new metadata fields, update the whitelist in
  `tools/normalize_first_party_skill_sources.py` or the field will be silently
  stripped on the next rebuild.
- Do not write projection-target state back into canonical source frontmatter;
  projection surfaces belong in catalog or generator outputs.

## `agents/openai.yaml`

- Use it for the Codex-facing wrapper metadata.
- Keep `interface.display_name`, `interface.short_description`, and
  `interface.default_prompt` aligned to the canonical skill name and trigger
  language.
- Prefer explicit `use when` phrasing in the short description and default
  prompt.
- Keep `policy.allow_implicit_invocation` explicit.
- Add dependencies only when the skill actually needs them.

## Repo usage

- The first-party source is edited directly.
- Generators and projection tooling should read from this source, not from
  hand-maintained plugin duplicates.
- Active generated surfaces must stay in sync with the canonical source.
- If a historical name remains anywhere, it must be quarantined to provenance
  or archive material.
- Skill-root `INDEX.md` files do not belong in this tree.


