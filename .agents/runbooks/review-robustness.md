# Review Robustness Runbook

Use this runbook before flipping a PR from draft to ready in `agent-asset-marketplace`.

## Goal

Run the fastest, cheapest checks first so that `iterative-review` and Devin auto-review only see the issues that require judgment, not the pattern classes the repo can catch deterministically.

## Procedure

1. **Fast preflight first.**
   - `py -3 tools/run.py review-preflight --check`
   - `py -3 tools/run.py ci --check`
   - If either is red, fix the findings and re-run. Do not dispatch `iterative-review` while preflight is red.

2. **Scope honesty.**
   - Compare the branch diff to the PR description, the linked spec, and any linked plan.
   - If the implemented scope differs, update the spec/plan or PR body to match before reviewers see the diff.

3. **Iterative review.**
   - Only after preflight is green, run `iterative-review` with the lens profiles:
     - `reviewer-skills` for SKILL.md, reference files, and prompt robustness.
     - `reviewer-marketplace` for scaffolders, generated surfaces, and this-repo tooling.
     - `reviewer-security` for secrets and real identifiers.
     - `reviewer-strong` for whole-branch design and scope.
   - For each finding, use `receiving-code-review` before applying.

4. **Post-fix re-preflight.**
   - After each fix, re-run `py -3 tools/run.py ci --check`.
   - Prepare a new fix diff and re-run the relevant lens (e.g., `reviewer-skills` for a skill-fix re-review, `reviewer-marketplace` for a marketplace fix, or `reviewer-strong` for a scope/design re-review).

5. **Ready to review.**
   - Only flip the PR out of draft when:
     - `ci --check` is green on the staged tree,
     - `iterative-review` reports no blocking or important issues,
     - the PR body and spec/plan are honest about the final scope.

6. **Wait for PR CI.**
   - GitHub Actions does not run on draft PRs in this repo. As soon as the PR is marked ready, it will queue `marketplace-validation`.
   - After flipping to ready and pushing, wait for the run and verify it passes:
     - `gh pr checks <number>`
     - `gh run view <run-id>`
   - Do not report the PR as reviewed or green until the GitHub CI is actually passing. A green `ci --check` locally does not prove the remote gate passes.

## Common mistakes

- Running `iterative-review` on a red preflight.
- Letting a targeted re-review lens drift into a full-branch review.
- Skipping re-preflight after a fix.
- Flipping to ready before a final clean `ci --check`.
- Reporting the PR as green/ready based on local `ci --check` without waiting for the GitHub Actions `marketplace-validation` run.
