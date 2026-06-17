# Repo Worker Base Source Map

This plugin keeps the repo-worker-base project thin and first-party while adding the generic safety and GitHub proof helpers that repo-backed work needs.

Current source roots:

- `sources/first_party/skills/repo-worker-base/SKILL.md`
- `sources/first_party/skills/boring-loop/SKILL.md`
- `sources/first_party/skills/codex-repo-receipts/SKILL.md`
- `sources/first_party/skills/connector-safety/SKILL.md`
- `sources/first_party/skills/github-operations/SKILL.md`

Local bundle paths:

- `skills/repo-worker-base/SKILL.md`
- `skills/boring-loop/SKILL.md`
- `skills/codex-repo-receipts/SKILL.md`
- `skills/connector-safety/SKILL.md`
- `skills/github-operations/SKILL.md`

Component summary:

| Lane | Canonical name | Component version | Source path | Local path | Role |
| --- | --- | --- | --- | --- | --- |
| Base | repo-worker-base | 1.0.0 | `sources/first_party/skills/repo-worker-base/SKILL.md` | `skills/repo-worker-base/SKILL.md` | repo worker hygiene |
| Dependency | boring-loop | v1 | `sources/first_party/skills/boring-loop/SKILL.md` | `skills/boring-loop/SKILL.md` | boring loop routing |
| Dependency | codex-repo-receipts | v1 | `sources/first_party/skills/codex-repo-receipts/SKILL.md` | `skills/codex-repo-receipts/SKILL.md` | repo receipts |
| Dependency | connector-safety | current | `sources/first_party/skills/connector-safety/SKILL.md` | `skills/connector-safety/SKILL.md` | connector safety |
| Dependency | github-operations | current | `sources/first_party/skills/github-operations/SKILL.md` | `skills/github-operations/SKILL.md` | GitHub proof |

Live install surfaces are unversioned plugin folders, but this map also includes canonical first-party source roots when a skill is sourced from `sources/first_party/skills/<skill>/`.
