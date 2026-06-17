# Repo Worker Base Source Map

This plugin keeps the repo-worker-base project thin and first-party while adding the generic safety and GitHub proof helpers that repo-backed work needs.

Current source roots:

- `codex-marketplace/plugins/repo-worker-base/skills/repo-worker-base/SKILL.md`
- `codex-marketplace/plugins/repo-worker-base/skills/boring-loop/SKILL.md`
- `codex-marketplace/plugins/repo-worker-base/skills/codex-repo-receipts/SKILL.md`
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
| Base | repo-worker-base | 1.0.0 | `codex-marketplace/plugins/repo-worker-base/skills/repo-worker-base/SKILL.md` | `skills/repo-worker-base/SKILL.md` | repo worker hygiene |
| Dependency | boring-loop | v1 | `codex-marketplace/plugins/repo-worker-base/skills/boring-loop/SKILL.md` | `skills/boring-loop/SKILL.md` | boring loop routing |
| Dependency | codex-repo-receipts | v1 | `codex-marketplace/plugins/repo-worker-base/skills/codex-repo-receipts/SKILL.md` | `skills/codex-repo-receipts/SKILL.md` | repo receipts |
| Dependency | connector-safety | current | `sources/first_party/skills/connector-safety/SKILL.md` | `skills/connector-safety/SKILL.md` | connector safety |
| Dependency | github-operations | current | `sources/first_party/skills/github-operations/SKILL.md` | `skills/github-operations/SKILL.md` | GitHub proof |

All live current roots are unversioned plugin folders.
