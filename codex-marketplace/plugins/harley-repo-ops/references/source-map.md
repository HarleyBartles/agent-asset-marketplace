# Harley Repo Ops Source Map

This bundle projects the shared House Skills used for cross-repo worker
dispatch and connector-safe side effects.

Authoritative source references:

- `sources/house-skills/decisions.json`
- `sources/house-skills/decisions.md`
- `sources/house-skills/intake.json`
- `provenance/house-skills.md`

Lane summary:

- Shared worker/control plane: connector-safety, gpt-base-doctrine, work-mode-router, worker-dispatch-linear, linear, tps-reporting, tps-ingress, don-logan-boundary, crew, crew-buster

Component map:

| Lane | Canonical name | Source path | Local path |
| --- | --- | --- | --- |
| Shared worker/control plane | connector-safety | `gpt-skills/house-skills/connector-safety/SKILL.md` | `skills/connector-safety/SKILL.md` |
| Shared worker/control plane | gpt-base-doctrine | `gpt-skills/house-skills/gpt-base-doctrine/SKILL.md` | `skills/gpt-base-doctrine/SKILL.md` |
| Shared worker/control plane | work-mode-router | `gpt-skills/house-skills/work-mode-router/SKILL.md` | `skills/work-mode-router/SKILL.md` |
| Shared worker/control plane | worker-dispatch-linear | `gpt-skills/house-skills/worker-dispatch-linear/SKILL.md` | `skills/worker-dispatch-linear/SKILL.md` |
| Shared worker/control plane | linear | `gpt-skills/house-skills/linear/SKILL.md` | `skills/linear/SKILL.md` |
| Shared worker/control plane | tps-reporting | `gpt-skills/house-skills/tps-reporting/SKILL.md` | `skills/tps-reporting/SKILL.md` |
| Shared worker/control plane | tps-ingress | `gpt-skills/house-skills/tps-ingress/SKILL.md` | `skills/tps-ingress/SKILL.md` |
| Shared worker/control plane | don-logan-boundary | `gpt-skills/house-skills/don-logan-boundary/SKILL.md` | `skills/don-logan-boundary/SKILL.md` |
| Shared worker/control plane | crew | `gpt-skills/house-skills/crew/SKILL.md` | `skills/crew/SKILL.md` |
| Shared worker/control plane | crew-buster | `gpt-skills/house-skills/crew-buster/SKILL.md` | `skills/crew-buster/SKILL.md` |

The bundle version is separate from the component versions. The component
versions stay recorded in the source ledger and SKILL.md frontmatter metadata.
