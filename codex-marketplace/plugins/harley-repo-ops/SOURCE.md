# Source

This bundle packages the shared House Skills needed for safe cross-repo worker
dispatch and connector-safe side effects.

## Canonical basis

- Canonical root: `gpt-skills/house-skills`
- Source ledger: `sources/house-skills/decisions.json`
- Human registry: `sources/house-skills/decisions.md`
- Structured registry mirror: `sources/house-skills/intake.json`
- License posture: first-party Harley-owned source

## Source roots inspected

- `gpt-skills/house-skills/connector-safety/SKILL.md`
- `gpt-skills/house-skills/gpt-base-doctrine/SKILL.md`
- `gpt-skills/house-skills/work-mode-router/SKILL.md`
- `gpt-skills/house-skills/worker-dispatch-linear/SKILL.md`
- `gpt-skills/house-skills/linear/SKILL.md`
- `gpt-skills/house-skills/tps-reporting/SKILL.md`
- `gpt-skills/house-skills/tps-ingress/SKILL.md`
- `gpt-skills/house-skills/don-logan-boundary/SKILL.md`
- `gpt-skills/house-skills/crew/SKILL.md`
- `gpt-skills/house-skills/crew-buster/SKILL.md`

## Bundle inventory

| Bundle | Decision | Reason |
| --- | --- | --- |
| `codex-marketplace/plugins/house-skills/` | included | This is the shared aggregate projection and now carries `connector-safety` in the base/control-plane lane. |
| `codex-marketplace/plugins/adventures-pack/` | included | This project pack already composes repo-work helpers and benefits from connector-safe side-effect handling. |
| `codex-marketplace/plugins/wild-bunch-project-pack/` | included | This project pack benefits from the same shared safety component when workers touch Wild Bunch source or perform side effects. |
| `codex-marketplace/plugins/harley-repo-ops/` | included | This is the curated cross-repo worker bundle for Harley repos and is the cleanest home for the shared worker-control-plane skills. |
| other project-specific bundles | excluded | They were not needed to make the shared worker route boring and would widen scope without helping the current issue. |

## Notes

- The bundle records the canonical source paths and versions in
  `references/source-map.md`.
- The bundle is a projection, not the source of truth.
