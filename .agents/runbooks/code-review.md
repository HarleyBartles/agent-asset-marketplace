# Code Review Runbook

Use this reference when reviewing work in the agent-asset-marketplace repo. This is a review methodology, not a merge checklist.

## Review Lenses

Apply three core lenses to every review:

1. **Principal Architect** — alignment with marketplace structure, source custody discipline, marketplace correctness, and skill metadata.
2. **Senior QA Engineer** — validation adequacy, test quality, edge cases, and regression risk. Prefer observable assertions over claims.
3. **Senior Software Engineer** — code quality, naming, error handling, DRY without premature abstraction, YAGNI, and pattern conformance.

### Cross-repo consumer lens

When the diff touches vendored skills, prompts, or scripts that install into other repos, verify it does not hardcode this repo's paths, command names, or layouts; uses consumer-canonical commands; and is safe without this repo's context.

## Architecture and Doctrine

Reviewers must check the repo's architectural choices in `.agents/doctrine/custody-and-marketplace-doctrine.md`. If code and skills disagree, the skills win. Invoke `/repo-worker-base` and `/base-doctrine` when the work touches marketplace generation, validation, or tooling.

If marketplace configuration or source custody changed, regenerate with `tools/run marketplace --apply` and validate with `tools/run ci --check`.

## Marketplace and Validation

- Marketplace standards live in `.devin/rules/tools.md`.
- Unslop profiles live in `/unslop-profiles`; apply the profile matching the work's domain.
- Durable guidance belongs in `AGENTS.md` or doctrine documents. Deferred work belongs in Linear issues, not durable guidance.
- Regenerate `INDEX.md` files via `tools/run mesh --apply` when files are added or removed.

## Repo Improvement Check

Every PR should leave the repo in a better state than before. Flag a "fix-while-here" issue only when the PR already modifies the file and the fix is small. Track larger fixes as Linear issues; silent deferral is not acceptable.

Do not scope-creep into unrelated refactors or require fixing untouched tech debt.

## Validation Coverage

Verify the work is validated. Key checks:

- Marketplace regeneration: `tools/run marketplace --apply` when source custody changes.
- CI validation: `tools/run ci --check`.
- Skill installation: `tools/run installed-skills --apply` when skills change.
- Index mesh: `tools/run mesh --apply` when files are added or removed.
- Vendored output: generated or installed vendored assets must reflect the change.

## Publication Proof

Per the root `AGENTS.md`, the return must include a PR URL and head SHA, a verified direct-main commit SHA, or a concrete publication blocker. Local changes are not repo completion.

## Plan Completion Check

If the PR claims to implement a plan from `.agents/plans/`, verify the plan is marked completed before approving. The canonical rule is in [`completing-plans.md`](completing-plans.md):

- All top-level checkboxes in the plan (`- [ ]`) must be checked off (`- [x]`), or the plan must record a merged implementation PR.
- If the PR body claims the plan is "complete" but the plan is not fully checked off and does not record a merged PR, block completion until the author either checks off the delivered items or removes the completion claim.

## Documentation and surface hygiene

- No unjustified documentation duplication. If two runbooks, guides, or reference files cover the same concern, either merge them or split them by a logical boundary (e.g., author vs reviewer, local vs consumer, setup vs operation). Do not keep near-identical parallel documents because the names differ.
- A new document must justify why it cannot live in an existing canonical surface. Prefer extending `pr.md`, `code-review.md`, `AGENTS.md`, or `.devin/rules/*.md` over adding a new `.agents/runbooks/<topic>.md`.

## Clean Workspace

No stray files, uncommitted debug artifacts, or phantom files in parent directories.
