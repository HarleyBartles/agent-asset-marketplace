---
name: adventures-visual-bible-interpreter-v1
description: interpret Adventures visual bibles into actor-safe canon-backed prompt, QA, repair, preserve, and extrapolation packets for GPT, PSA, or PIG visual work. Use when downstream visual or pre-vis work needs repo-indexed bible constraints while keeping constraint extraction separate from generation, deterministic rendering, self-QA, final acceptance, compilation, or repo mutation authority.
---

# Adventures Visual Bible Interpreter v1

Use this skill to extract operational constraint packets from a current Adventures visual bible for downstream GPT or PIG visual work.

## Owned decision

Decide whether the requested downstream task has enough bible-grounded constraints, needs a narrower extraction packet, is blocked by missing/stale bible evidence, or must route to bible creation/update, visual preproduction, image preflight, image QA, or deck/image planning.

## Hard boundaries

This is deterministic no-credit canon interpretation shared by actor-safe constraint use. GPT, PSA, and PIG may use the extracted constraints, but this skill does not generate or edit images, render PSA boards, perform PSA or PIG self-QA, accept or reject images, compile sheets, build decks, mutate repos, or treat extracted prompt/repair text as generation or acceptance authority.


## Actor boundary

This is the primary shared-safe image-adjacent Adventures skill. It carries constraints, evidence, preserve clauses, negative steers, QA gates, repair guidance, and allowed variation. It does not carry generation authority.

Ordinary GPT may use the packet for visual preproduction, PSA handoff packets, image preflight, image QA, deck-image planning, or repair planning. PSA may use the packet inside deterministic storyboard/prompt-board work as canon/style/constraint input. PIG may use the packet inside a bounded PIG production job as canon input. Neither actor may use this skill to claim final Adventures acceptance, canon lock, deck-ready status, repo/project acceptance, or issue closure.

## Progressive references

Read `references/visual-bible-interpretation-contract.md` when interpreting a bible, extracting positive/negative prompt blocks, QA gates, preserve clauses, repair blocks, sensitive-detail micro-specs, or downstream handoff packets.

## Minimal workflow

1. Identify the visual bible, asset class, downstream lane, and source basis.
2. Read current bible/source evidence needed for that lane.
3. Extract reusable positive constraints, negative constraints, sensitive details, preserve clauses, QA hard gates, repair guidance, and allowed variation.
4. Mark any missing/stale/ambiguous bible evidence and downstream risks.
5. Return the interpretation packet; stop before preflight execution, QA acceptance, or image mutation.

## Source posture

Use repo-indexed bible and current visual evidence when canon matters. Do not reconstruct bible constraints from memory or generic style language when a current bible should exist.
