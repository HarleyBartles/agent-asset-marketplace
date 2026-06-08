# AGENTS.md

Scope: `gpt-skills/`

This scope covers the GPT-native skill source tree and its supporting assets.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

## Review guidelines

- Flag skill roots whose `SKILL.md` references missing assets, scripts, or
  references.
- Flag any third-party-origin material that is placed in the GPT skill tree
  without provenance or an explicit first-party authorization trail.
- Flag path drift between skill metadata, support files, and the actual on-disk
  layout before minor content edits.
- Treat `gpt-skills/house-skills/` as first-party-only territory; imported or
  adapted material does not belong there unless Harley explicitly authored it as
  first-party source.

## Versioned updates

- Treat imported skill versions as historical source records, not live inventory.
- When a House Skill needs a semantic update, create a new version line such as
  `v1.1/<skill-name>-v1.1/` rather than overwriting the imported version.
- Check the current source ledger and generated projection before assuming what
  is active.
- A new folder is only a staging step. The update is complete only when the
  active bundle, registry, and projection point at the new version and the old
  one is historical or provenance-only.
