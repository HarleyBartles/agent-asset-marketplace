# first_party

Editable first-party source custody lives here.

Use `first_party/skills/` as the single tree for all first-party skills,
including generic reusable worker machinery and family-owned or bundle-specific
roots. Every directory under `skills/` must contain a `SKILL.md`; governance-only
metadata (decisions, intake) for plugins that do not ship a skill lives under
`provenance/<plugin>-governance/` instead.
