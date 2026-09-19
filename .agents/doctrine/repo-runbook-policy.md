# Repository Runbook and Playbook Policy

This repository follows `repo-standards`. Lifecycle stages are runbooks; available topical workflows are playbooks.

## Standard runbooks

| Standard runbook | Local path | Status |
|---|---|---|
| design.md | `.agents/runbooks/design.md` | required |
| planning.md | `.agents/runbooks/planning.md` | required |
| implementing.md | `.agents/runbooks/implementing.md` | required |
| code-review.md | `.agents/runbooks/code-review.md` | required |
| pr.md | `.agents/runbooks/pr.md` | required |

## Standard playbooks

| Standard playbook | Local path | Status |
|---|---|---|
| code-style.md | `.agents/playbooks/code-style.md` | required |
| testing.md | `.agents/playbooks/testing.md` | required |
| security.md | `.agents/playbooks/security.md` | required |
| skill-authoring.md | `.agents/playbooks/skill-authoring.md` | required |
| marketplace-generation.md | `.agents/playbooks/marketplace-generation.md` | required |
| repo-doctrine.md | `.agents/playbooks/repo-doctrine.md` | required |

## Additional repository-specific playbooks

None.

## Root contributor and review surfaces

- `REVIEW.md` enters through `.agents/runbooks/code-review.md`.
- `CONTRIBUTING.md` enters through the applicable lifecycle runbook.

## Exceptions

- `marketplace-source-submodule` - this repository is the marketplace source and does not vendor itself.
