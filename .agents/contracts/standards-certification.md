# AOM Standards Certification

This is the repository-owned assessment of its selected standards. The structural checker reports observable records and paths; it does not certify semantic usefulness. Each entry states what this checkout can currently claim and what remains unverified.

## root-agent-router

**Status:** Self-certified.

- **Implementation:** Root and scoped `AGENTS.md` routers; `tools/validate_agents_md.py` owns the repository's eight-file allow-list, 55-line warning, and 100-line error budget.
- **Must preserve:** Keep routers brief, scoped, and useful; route to owned guidance rather than duplicating it.
- **Drift controls:** The validator is part of `tools/run.py validate`, which is included in the complete CI target and tracked hook. Semantic router quality is reviewed when guidance changes.
- **Evidence and limits:** The Windows gate reported eight allowed routers with no line-budget warning on commit `5725b79`. Counts and thresholds do not prove useful routes.

## runbook-composition

**Status:** Self-certified.

- **Implementation:** `.agents/runbooks/` contains the repository's selected lifecycle guides for design, planning, implementation, code review, and PR publication. `.agents/doctrine/repo-runbook-policy.md` records this repository-owned inventory.
- **Must preserve:** Each guide remains a lifecycle-stage document with useful entry conditions, procedure, completion evidence, and applicable playbook routing. The local inventory is this repository's choice, not an AOM-required set.
- **Drift controls:** The root and scoped `AGENTS.md` routers direct agents to stage guidance; `tools/validate_markdown_links.py --check` verifies links. Agents changing a runbook review its lifecycle purpose and certification entry.
- **Evidence and limits:** The current guides were read against the pinned definition. Link validation and the local inventory do not prove that every stage guide remains useful.

## playbook-composition

**Status:** Self-certified.

- **Implementation:** `.agents/playbooks/` contains the repository's concern guides for code style, testing, security, skill authoring, Marketplace generation, and repository doctrine.
- **Must preserve:** Keep reusable concern guidance distinct from stage procedure. Routes and capability claims must match available repository or ambient capability; no universal headings or empty composition slot is required.
- **Drift controls:** Stage runbooks route applicable playbooks, and `tools/validate_markdown_links.py --check` verifies references. Agents changing a guide assess concern scope and its routes.
- **Evidence and limits:** Current playbooks and cross-links were reviewed against the pinned definition. Link resolution cannot establish semantic usefulness or ambient capability availability.

## tracked-validation-hook

**Status:** Self-certified.

- **Implementation:** `githooks/pre-commit` materializes and checks the candidate tree. `.agents/contracts/repo-standards-commands.json` declares apply and check commands. `.github/workflows/marketplace-validation.yml` invokes the same hook in hosted mode.
- **Must preserve:** Keep the complete `tools/run.py ci` gate on Windows and Linux, fail on missing prerequisites, preserve unrelated working changes, and prohibit agents from bypassing the hook.
- **Drift controls:** The tracked hook and hosted workflow are both reviewed with command-contract changes. `.agents/runbooks/pr.md` and `.agents/doctrine/tools.md` prohibit bypassing the hook.
- **Evidence and limits:** The complete Windows tracked hook passed on commit `48d3bd78ae34a5a83e1a1361a54f0b2fa43bcc05`. The hosted Linux workflow checked out and passed that exact detached PR head on Draft PR #345, run `36938920670` (`https://github.com/HarleyBartles/agent-asset-marketplace/actions/runs/36938920670`). This certifies the gate at that commit; later source changes require fresh evidence. Hosted success demonstrates committed Linux parity, not that future local commits will pass.

## review-entrypoint

**Status:** Self-certified.

- **Implementation:** Root `REVIEW.md` routes reviewers to `.agents/runbooks/code-review.md` and the repository's review workflow.
- **Must preserve:** Keep the root entrypoint useful and update its route when review guidance moves.
- **Drift controls:** The root `AGENTS.md` routes review work to the code-review runbook; Markdown link validation checks local references.
- **Evidence and limits:** The entrypoint and destination were read together. Harness-specific automatic loading is not claimed as universal.

## contribution-entrypoint

**Status:** Self-certified.

- **Implementation:** Root `CONTRIBUTING.md` explains the contribution entry path and links to the repository's orientation and runbook policy.
- **Must preserve:** Keep it sufficient for contributors to find and follow the applicable contribution process.
- **Drift controls:** Root links are checked by the repository Markdown-link validator and reviewed when the contribution process changes.
- **Evidence and limits:** The current root guide and its linked procedure were read together; this check does not measure contributor outcomes.

## completed-artifact-custody

**Status:** Self-certified.

- **Implementation:** `.agents/doctrine/completed-artifacts.md`, `.agents/runbooks/planning.md`, and `.agents/runbooks/pr.md` bind the portable semantic lifecycle to repository paths and delivery practice.
- **Must preserve:** Keep active future plans; discover completion from whole-scope evidence; retain branch-only plans through their completing PR; promote durable knowledge before retirement. A marker may record state but does not decide completion.
- **Drift controls:** Planning and PR agents classify artifacts at the next substantive slice. Review the current pinned definition when changing the local lifecycle.
- **Evidence and limits:** The current plan and runbook instructions were reviewed against the pinned definition. MARK-379 classified the AOM adoption roadmap, eleven plans and specification against their completed scope, current durable skill/contract owners and merged PR #345 at `b481f98ae90aa45e5271d10fe1f7aaeb6c7047aa`, and retired them in its first substantive implementation commit. Active and uncertain predecessor work remains. The repository has not added an automatic semantic deletion checker.

## unslop

**Status:** Process established; profile effectiveness and cross-agent recurrence remain unproven.

- **Implementation:** `.agents/unslop/repository.md` holds the current guard and a candidate-observation section. Planning, implementation, review, and PR runbooks link to it directly; `$unslop-profiles` remains optional ambient assistance.
- **Must preserve:** Record concrete distinct observations, keep duplicate reports linked, and note guard availability, reach, reading, following, and effect when known. Do not turn one observation into a recurrence claim or an automatic profile edit.
- **Drift controls:** The runbook links are checked by `tools/check_agent_standards.py`; each agent at a routed work point reviews and maintains matching evidence.
- **Evidence and limits:** One near miss from one agent session was recorded during this migration. It is a candidate observation, not cross-agent recurrence and not proof that the profile is effective. Later agents must assess distinct evidence before strengthening the recurrence claim.
