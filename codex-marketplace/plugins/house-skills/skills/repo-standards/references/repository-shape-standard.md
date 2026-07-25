# Repository Shape Standard

This file describes the surfaces `repo-standards` checks and can apply. It is the human-readable companion to `repository-shape-manifest.json`.

## Required surfaces

- `.agents/plugins/marketplace-source` as a git submodule pointing at the marketplace source.
- `.agents/plugins/marketplace.json` with `repo.local_skill_prefixes` configured.
- `scripts/ci-preflight.ps1` and `scripts/ci-preflight.sh` for the default preflight bundle.
- `.git/hooks/pre-commit` wired to `scripts/ci-preflight.sh -Check`.
- `.agents/docs/repo-guide-policy.md` mapping the repo to `repo-standards`.
- `REVIEW.md` at the repo root pointing to the review guide and required skill invocations.
- `CONTRIBUTING.md` at the repo root as the contributor entry point.
- `.gitignore` containing the `.agents/superpowers/sdd/**` and `!.agents/superpowers/sdd/.gitignore` rule.
- `.agents/guides/<standard-guide>.md` for the core and declared guide set.

## Scaffold helpers

Use these idempotent scripts to create missing user-content surfaces. The agent remains responsible for repo-specific content.

- `scaffold-review` generates `REVIEW.md`.
- `scaffold-contributing` generates `CONTRIBUTING.md`.
- `scaffold-gitignore` ensures the sdd rule is in root `.gitignore`.
- `scaffold-guides` generates missing `.agents/guides/*.md` files from `repo-guide-policy.md`.
- `scaffold-all` runs the above in sequence.

`repo-standards --apply` also invokes the appropriate scaffold when a surface has `scaffold` set in the manifest.

## Local overrides

Each repo supplies its own `repo.local_skill_prefixes` in `.agents/plugins/marketplace.json` so local skills are not pruned by `refreshing-installed-skills`.

## Local-only agent surfaces

The `.agents/superpowers/` directory has mixed residency:

- `superpowers/specs/**` is repo resident.
- `superpowers/plans/**` is repo resident.
- `superpowers/sdd/` and all subdirectories are intentionally ignored; SDD outputs are not repo resident.

A repo that follows this standard must have a root `.gitignore` rule equivalent to:

```gitignore
.agents/superpowers/sdd/**
!.agents/superpowers/sdd/.gitignore
```

This keeps the `sdd/` scaffold (only its `.gitignore`) while ignoring all session content at any depth.
