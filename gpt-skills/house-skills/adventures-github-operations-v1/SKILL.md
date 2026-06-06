---
name: adventures-github-operations-v1
description: verify adventures of patch github, repo, publication, asset, deck, receipt, issue-to-pptx, patch lane, PIG production returns, and visual qa evidence after the repo/GitHub proof surface. use for worker returns, remote heads, changed files, source package indexes, accepted images, visual bibles, pptx/sidecar packages, receipt manifests, issue-goal conformance, and green/amber/red closure judgments in harleybartles/adventures-of-patch.
---

# Adventures GitHub Operations v1

Use this skill to verify Adventures of Patch GitHub and repo evidence after the repo/GitHub proof surface has established the base evidence discipline.

This is an Adventures wrapper. It adds local repo, Patch, asset, deck, receipt, image QA, visual bible, and issue-to-PPTX proof law. It does not replace generic GitHub evidence discipline, Adventures issue management, Adventures reporting hygiene, dispatch skills, image QA, deck QA, receipt generation, or repo mutation routes.

## Core lesson

A pushed commit, a worker GREEN, a receipt zip, or a deck package is not enough by itself.

Adventures work is often package-shaped: source zips, accepted images, candidate images, contact sheets, proof decks, final decks, sidecars, receipt zips, manifests, and issue comments. Verification must prove that the observed source state satisfies the issue goal and that the correct Adventures production lane was respected.

## Progressive references

Read `references/source-route-posture.md` only when verification depends on repository/source evidence, route coverage, connector availability, exact source reads, broad discovery, local evidence, or a route failure.

Read `references/adventures-proof-surfaces.md` only when package, receipt, image, asset, deck, visual bible, or issue-to-PPTX evidence is central to verification.

## Required composition

1. Use the generic GitHub operations capability first for repo evidence partitioning, issue-goal conformance, publication proof, and GREEN/AMBER/RED posture.
2. Return here for Adventures-local proof surfaces.
3. Load source-route posture only when the verification needs source evidence or route coverage.
4. Do not treat one route failure as proof of absence. State the route capability that failed.

## Canonical project posture

The canonical repo for Adventures project source is `HarleyBartles/adventures-of-patch` unless Harley names another repo.

Use this skill for evidence review, not mutation. Do not edit repo files, post issue comments, close issues, build decks, create receipts, generate images, or dispatch workers from this skill alone.

## Adventures evidence lanes

Keep these lanes separate:

- `worker_claim`: what Patch, a worker, or a return says happened.
- `github_evidence`: issue, PR, commit, file, branch, compare, ref, and comment state visible through source routes.
- `patch_lane_evidence`: the named Patch route, issue authority, source root, return contract, and publication context.
- `asset_evidence`: asset indexes, source-package indexes, accepted source images, candidate images, rejected images, contact sheets, and asset-sheet outputs.
- `image_qa_evidence`: Adventures image QA decisions, acceptance state, repair requirements, and blocked image states.
- `pig_production_evidence`: PIG-generated candidates, PIG self-QA status, deviations, blockers, and return-contract notes. Treat this as production-return evidence, not external image QA, Harley acceptance, canon lock, deck-ready status, or issue-goal closure proof.
- `visual_bible_evidence`: visual bible status, cited source basis, prompt/QA/repair guidance, and whether it was treated as guidance rather than mutation authority.
- `deck_package_evidence`: proof, full, and final PPTX package state, sidecar state, notes state, embedded-image expectations, and package naming.
- `receipt_evidence`: receipt zips, manifests, hashes, embedded-image extraction, summary files, and source-package maps.
- `validation_evidence`: checks selected, checks run, skipped checks, visible logs or artifacts, and whether they test the issue goal.
- `issue_goal_conformance`: whether the observable repo/package state satisfies the actual GitHub issue goal.
- `verifier_judgment`: GREEN, AMBER, RED, or BLOCKED.

Do not upgrade a weaker lane into a stronger one. A receipt manifest is evidence of package contents, not proof that the deck teaches the lesson. An accepted image QA result is evidence of image state, not permission to generate or edit another image.

## Verification workflow

For issue-backed Adventures work:

1. Identify the issue, repo, claimed final branch/head, changed files, package paths, and claimed artifacts.
2. Load source-route posture only if source evidence or route coverage must be selected or explained.
3. Inspect exact issue, comment, commit, PR, compare, file, package, or route evidence needed for the claim.
4. Restate the issue goal as observable Adventures state.
5. Name the falsification surfaces: source indexes, asset folders, visual bibles, deck packages, sidecars, receipts, manifests, QA notes, or issue comments.
6. Check whether the observed state proves the goal, merely supports the worker claim, contradicts the goal, or leaves a required surface unverified.
7. Partition package evidence from production-quality evidence.
8. Return GREEN, AMBER, RED, or BLOCKED with the shortest evidence summary that supports the judgment.

Use this required closure shape for issue-backed verification:

```yaml
issue_goal_as_observable_state: <what must be true in repo or package state>
repo_surfaces_that_should_reflect_goal:
  - <path, issue, commit, package, receipt, or index>
falsification_checks_run:
  - <check and route capability used>
worker_claim_vs_observed_state: <match, partial, mismatch, or unavailable>
adventures_local_evidence:
  asset_evidence: <state or not applicable>
  image_qa_evidence: <state or not applicable>
  deck_package_evidence: <state or not applicable>
  receipt_evidence: <state or not applicable>
judgment: GREEN | AMBER | RED | BLOCKED
```

## Package and receipt rules

When a return mentions a PPTX package, sidecar, receipt zip, or source package, verify the exact artifact family that the issue requires.

- A proof deck is not a final deck unless the issue accepts proof state.
- A final deck is not complete if required sidecars, notes, receipts, or image receipts are missing.
- A receipt zip proves only what its manifest and hashes prove.
- An embedded-image receipt helps verify image custody, but it does not prove image QA acceptance unless the QA evidence is present.
- A source package can support visual work, but it is not canon acceptance by itself.
- A contact sheet or asset sheet is deterministic pixel work unless a separate accepted image-generation lane says otherwise.

Read `references/adventures-proof-surfaces.md` when package, receipt, image, asset, or deck evidence is central to the judgment.

## Image-credit boundary

Verification is deterministic no-credit work.

Do not call image generation, generative editing, visual mutation capabilities, or prompt-board generation from this skill. If visual QA is needed, route to the Adventures image QA or presentation QA capability as appropriate. QA and repair guidance do not authorize image mutation.

## Issue and comment boundary

Use Adventures issue-management capability for creating, shaping, commenting on, migrating, or closing issues. This skill can supply the evidence partition and closure judgment, but it does not post it unless a separate issue-management route is invoked and Harley has authorized that mutation.

## Dispatch boundary

If the next step is worker execution, repo mutation, package creation, receipt generation, deck building, or Patch work, route through Adventures dispatch classification, preparation, and preflight. Do not turn a verification report into a worker dispatch.

## False-green risks

- Treating a worker GREEN as issue-goal conformance.
- Treating a pushed commit as proof that the deck, asset, receipt, or visual QA goal is satisfied.
- Treating a receipt zip as proof of acceptance instead of proof of package contents.
- Treating generated image candidates as accepted source images.
- Treating image QA repair guidance as permission to spend an image credit.
- Treating a proof deck as a final deck without checking the issue goal.
- Treating issue comments as source truth rather than durable reports.
- Treating broad repo search misses as proof of absence.
- Verifying `adventures-of-patch` from memory or old session summaries instead of current source routes.

## Output posture

Keep the user-facing answer compact unless Harley asks for a full audit. Say what was checked, what route capability was used, what remains unverified, and why the judgment is GREEN, AMBER, RED, or BLOCKED.
