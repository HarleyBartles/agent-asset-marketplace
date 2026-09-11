# Code Review Runbook

Use this reference for marketplace-specific review concerns. The routed review
skill owns general review method, sequencing, and reporting.

### Cross-repo consumer lens

When the diff touches vendored skills, prompts, or scripts that install into other repos, verify it does not hardcode this repo's paths, command names, or layouts; uses consumer-canonical commands; and is safe without this repo's context.

## Architecture and Doctrine

Reviewers must check the repo's architectural choices in `.agents/doctrine/custody-and-marketplace-doctrine.md`. Invoke `using-superpowers-plus` once and follow its review handoff; this runbook adds marketplace-specific review concerns.

If marketplace configuration or source custody changed, regenerate with `tools/run marketplace --apply` and validate with `tools/run ci --check`.

## Marketplace and Validation

- Marketplace standards live in `.devin/rules/tools.md`.
- Domain-specific review profiles live in `unslop-profiles`; the routed review owner selects the applicable profile.
- Durable guidance belongs in `AGENTS.md` or doctrine documents. Deferred work belongs in Linear issues, not durable guidance.
- Regenerate `INDEX.md` files via `tools/run mesh --apply` when files are added or removed.

## Marketplace validation coverage

Verify the work is validated. Key checks:

- Marketplace regeneration: `tools/run marketplace --apply` when source custody changes.
- CI validation: `tools/run ci --check`.
- Skill installation: `tools/run installed-skills --apply` when skills change.
- Index mesh: `tools/run mesh --apply` when files are added or removed.
- Vendored output: generated or installed vendored assets must reflect the change.

Publication proof is defined by root `AGENTS.md`; completed-artifact removal is
defined by [`completing-plans.md`](completing-plans.md). Do not duplicate either
contract here.
