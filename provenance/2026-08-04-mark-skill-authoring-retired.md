# mark-skill-authoring retired

## Provenance

- **Retired:** 2026-08-04
- **Original source:** `.agents/skills/mark-skill-authoring/` (local `mark-*` skill)
- **New home:** the deleted first-party skill tree `writing-skills/``
- **Reason:** The local `mark-skill-authoring` wrapper had no unique behavior beyond routing to the first-party `writing-skills` skill. Its references, scaffolder, and templates were folded into the canonical `writing-skills` source.

## What moved

| Old path | New path |
| --- | --- |
| `.agents/skills/mark-skill-authoring/SKILL.md` | removed; functionality merged into `writing-skills/SKILL.md` |
| `.agents/skills/mark-skill-authoring/references/local-and-marketplace-custody.md` | the deleted first-party skill tree `writing-skills/references/local-and-marketplace-custody.md`` |
| `.agents/skills/mark-skill-authoring/references/source-grounded-authoring.md` | the deleted first-party skill tree `writing-skills/references/source-grounded-authoring.md`` |
| `.agents/skills/mark-skill-authoring/scripts/new_skill.py` | the deleted first-party skill tree `writing-skills/scripts/new_skill.py`` |
| `.agents/skills/mark-skill-authoring/scripts/new-skill.sh` | the deleted first-party skill tree `writing-skills/scripts/new-skill.sh`` |
| `.agents/skills/mark-skill-authoring/scripts/new-skill.ps1` | the deleted first-party skill tree `writing-skills/scripts/new-skill.ps1`` |
| `.agents/skills/mark-skill-authoring/templates/` | the deleted first-party skill tree `writing-skills/templates/`` |

## Routing updates

- `docs/skill-standards-policy.md` now points to `writing-skills` for authoring method.
- `.agents/guides/skill-authoring-guide.md` now points to the deleted first-party skill tree `writing-skills/`` for custody, source-grounded authoring, and the scaffolder.

## Source of truth

Authoring lanes and scaffolding now live in the deleted first-party skill tree `writing-skills/``. The `.agents/skills/writing-skills/` installed surface is a generated projection.