---
name: adventures-image-qa-v1
description: >-
  review Adventures visual candidates and compiled asset sheets as external GPT/Harley/project QA without spending image credits. use when Harley asks to QA, accept, reject, repair, compare, or diagnose generated images, PIG-returned candidates, Patch-in-world proofs, storyboards, prompt-board outputs, or deterministic visual packages; keep this separate from PIG self-qa.
---

# Adventures Image QA v1

Use this skill when Harley asks ordinary GPT to QA, accept, reject, compare, diagnose, or repair-plan an Adventures image candidate, PIG-returned candidate, PSA-returned board, Patch-in-world proof, source image, storyboard visual, prompt-board output, or compiled asset sheet.

## Actor boundary

This is external Adventures image QA for GPT, Harley, and project workflow. It is not PIG self-QA and does not govern PIG's internal production loop.

PSA self-QA belongs to the PSA-only board QA skill. A PSA self-QA pass means only that PSA believes a deterministic board is worth returning as a planning/control artifact. PIG self-QA belongs to the PIG-only `pig-self-qa-regeneration` skill. A PIG self-QA pass means only that PIG believes a candidate is worth returning. This skill may later review that returned candidate and issue the project-facing QA decision: `accepted`, `edit_required`, `regenerate_required`, or `blocked`.

Do not treat PSA self-QA or PIG self-QA as Harley acceptance, GPT QA, canon lock, deck-ready status, asset-ready status, repo/project acceptance, or issue closure. A PSA board may be suitable for PIG grounding without being final art.

## Owned decision

Return an external project-facing QA decision for the visual artifact in the correct lane: `accepted`, `edit_required`, `regenerate_required`, or `blocked`. Explain the specific visual reason and the next safe route.

## Hard boundaries

Do not generate, regenerate, or edit images from this skill. Do not invoke or continue PIG production from this skill. QA is deterministic review and repair planning only. A QA failure, accepted repair packet, or obvious next prompt does not authorize a new image call. If Harley asks for new or changed pixels, route through the Adventures visual intent and image preflight path and stop after that skill owns authorization/readiness.

Do not treat operator context, session busters, issue comments, package state, or QA labels as visual content unless Harley explicitly asks for a status artifact.

## Progressive references

Read `references/qa-operating-contract.md` when you need the full QA workflow, decision schema, Patch identity checks, compiled-sheet review, repair-prompt guidance, or source-route requirements.

Read `references/lane-checks.md` when the lane-specific checks are needed for Patch identity, interaction/scale proof, source-image acceptance, compiled-sheet QA, or deck-readiness implications.

## Minimal workflow

1. Identify the artifact and QA lane.
2. Inspect the provided image or package directly when available.
3. Apply lane checks and preserve accepted features while isolating failures.
4. Return the decision and next route.
5. Stop without calling image generation.
