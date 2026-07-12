# Code Review Guide

Use this reference when reviewing work in the agent-asset-marketplace repo — PRs, task diffs, or whole-branch reviews. This is a review methodology, not a merge checklist. It defines the lenses, skills, policies, and checks a reviewer must apply.

## 1. Review Lenses

Apply three core lenses to every review.

### Core Lenses (every review)

**Principal Architect** — architectural alignment, marketplace structure conformance, source custody discipline, projection correctness. Does the work respect the established patterns? Does it follow custody and projection doctrine? Are skills properly structured with correct metadata? Does the work leak implementation details into source custody?

**Senior QA Engineer** — validation adequacy, test quality, edge cases, regression risk. Are the right validation commands used (check_marketplace.py, rebuild_marketplace.py)? Do validation steps assert on observable behavior? Are edge cases covered? Does the diff introduce unvalidated changes?

**Senior Software Engineer** — code quality, naming, error handling, DRY without premature abstraction, YAGNI, existing pattern conformance, file organization. Are names accurate? Is error handling at the right boundary? Does each file have one clear responsibility? Is the work following the file structure from the plan?

## 2. Architecture Review

Reviewers must invoke the architecture skills before reviewing work that touches marketplace generation, validation, or tooling:

- `/repo-worker-base` — fresh-main discipline, worktree isolation, branch and PR hygiene, validation evidence
- `/base-doctrine` — cross-runtime doctrine for workspace patterns, tool/source evidence honesty

Reviewers must check the repo's architectural choices in `docs/custody-and-projection-doctrine.md` and assess work against alignment with those standards. The skills and documentation are the authority, not the repo's current code — if code and skills disagree, the skills win.

**Manifest freshness check:** If the work changes marketplace configuration or source custody, the marketplace must be regenerated via `py -3 tools/rebuild_marketplace.py` and validated via `py -3 tools/check_marketplace.py`.

## 3. Marketplace Review

Reviewers must verify that marketplace work aligns with the marketplace generation and validation standards documented in [`tools/AGENTS.md`](../../tools/AGENTS.md). That document covers the canonical rebuild and validation entrypoints, the deterministic pack rule, and the editable custody inputs. Reviewers should read it before reviewing marketplace work and check the diff against each applicable standard.

## 4. Unslop Application

Reviewers must review the repo's unslop profiles and apply the relevant ones to work under review:

- The portable profiles from `/unslop-plus` — `code-review`, `testing`, `security-review`, `cleanup-custody`, `architecture`, etc.

Apply the profile that matches the work's domain. A tooling-only PR does not need the testing profile, and vice versa.

## 5. Agent Discovery and Durable Guidance

Reviewers must ensure that anything important for future agents to understand is recorded in durable agent guidance:

- If the work introduces a new pattern, convention, or gotcha that future agents would trip over without knowing, it should be documented in AGENTS.md or a doctrine document
- If the work changes the build/test workflow, update the relevant AGENTS.md section
- If the work discovers a tooling issue, it must be recorded in durable guidance so future agents don't trip over it
- INDEX.md files must be regenerated if files were added/removed (via `py -3 tools/generate_index_mesh.py`)

Durable agent guidance is for "agents will trip over this if they don't know." Deferred work is NOT durable agent guidance — it belongs in Linear issues (see section 7).

## 6. Tooling Hygiene

Reviewers must verify the workspace is clean — no stray files, no uncommitted debug artifacts, no phantom files in parent directories.

## 7. Repo Improvement Check

Every PR should leave the repo in a better state than before, not just add functionality on top of existing patterns. The reviewer must evaluate whether the work perpetuates legacy patterns that could have been modernized with minimal additional effort.

The test is not "is the repo better in the abstract" — it's three concrete questions:

1. **Did the work touch code with a legacy pattern that could be modernized in-scope?** If the diff already modifies a file that has an old pattern (e.g. a hardcoded path that should use a constant, a missing error handler that should be added, a stale comment that should be removed), and the modernization would be a small change within that file, the reviewer should flag it as "fix-while-here" — the cost of fixing it now is near-zero because you're already in the file, but the cost of a separate follow-up PR is high (context switch, review overhead, risk of forgetting).

2. **Did the work discover a problem that has a cheap fix?** If during implementation the worker encountered a problem (a confusing API, a missing validation, a stale comment, a tooling issue) and deferred it, the reviewer should ask: could this have been fixed in under 10 minutes? If yes, it should have been included. If the fix is genuinely large, it should be tracked as a Linear issue — the worker should flag the deferred work in their report, plan, or PR body, and a Linear issue should be created to track it (when requested). Silent deferral is not acceptable.

3. **Is the work perpetuating a pattern the repo is actively moving away from?** If the repo has an established better pattern (e.g. deterministic marketplace regeneration over partial refresh, source custody over hand-edited projections) and the PR adds new code using the old pattern, that's a finding — even if the old pattern still exists elsewhere. New code should always use the better pattern. "The rest of the file does it this way" is not a justification when the repo has decided to move away from that pattern.

**What this is NOT:**
- It is not a license to scope-creep into unrelated refactors. The test is "am I already here, and is the fix small?" — not "should I refactor everything that bothers me."
- It is not a requirement to fix pre-existing tech debt that the PR didn't touch. If you're not in the file, you're not obligated to fix it.
- It is not a blocker for PRs that are scoped correctly but don't happen to touch legacy patterns. A clean, well-scoped PR that adds a new feature without touching legacy patterns passes this check.

**The deferral trap:** The most common failure mode is "I'll fix this in a follow-up." Follow-ups don't happen unless they're tracked. The reviewer should treat a deferred fix that meets the "already here + small" test as a P1 finding, not a P2. If the worker wants to defer a larger fix, they must flag it in their return, plan, or PR body so it can be tracked as a Linear issue — silent deferral is not acceptable.

## 8. Validation Coverage

Reviewers must verify that the work is adequately validated. The validation standards are documented in [`tools/AGENTS.md`](../../tools/AGENTS.md) — reviewers should read that section and check the diff against each applicable standard.

Key validation checks:
- **Marketplace regeneration:** Did the work include `py -3 tools/rebuild_marketplace.py` when source custody changed?
- **CI validation:** Did the work pass `py -3 tools/check_marketplace.py`?
- **Skill installation:** Did the work refresh installed skills via `py -3 tools/install_agent_skills.py` when skills changed?
- **Index mesh:** Did the work regenerate the index mesh via `py -3 tools/generate_index_mesh.py` when files were added/removed?
- **Published vendored output:** If the PR claims to update a vendored asset or projection, verify the generated or installed vendored output changed on the PR head. An overlay, generator tweak, or manifest edit is not sufficient by itself if the published asset still matches the stale behavior.

## 9. Publication Proof

Reviewers must verify that the work includes proper publication proof per the root `AGENTS.md`:

- **PR URL and head SHA** for ordinary worker execution
- **Verified direct-main commit SHA** when direct-main work was explicitly authorized
- **Concrete publication blocker** explaining why local changes could not be pushed or turned into a PR

Local file changes are not repo completion. A worker must not return GREEN, claim repo work is done, or ask for issue closure from local paths, local commit hashes, local validation output, or an unpublished branch alone.

## 10. Issue-Goal Conformance

Reviewers must verify that the work actually delivers what the Linear issue requested. This is not a formality — it is the core check for whether the work is complete.

- Read the Linear issue's goal and scope
- Compare the final repo state against the issue's requirements
- If the issue targets a vendored or projected asset, inspect the published asset itself. If the overlay changed but the vendored output did not, that is a failed implementation, not a pass.
- If the work diverged from the issue's scope, verify the divergence is documented in the PR body and the issue is updated
- If the work is incomplete or missing key deliverables, flag it as a finding

The issue goal is the authority, not the plan. If the plan and issue disagree, the issue wins.
