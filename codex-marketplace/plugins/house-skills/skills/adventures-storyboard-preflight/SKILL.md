---
name: adventures-storyboard-preflight
description: prepare GPT/project-side Adventures storyboards, prompt boards, and deterministic visual planning. use when Harley asks ordinary GPT to storyboard frames, make prompt boards, map slide visuals, preflight story beats, or produce visual planning packets before image generation; never grants image-generation authority.
metadata:
  source-id: adventures-storyboard-preflight
  source-path: codex-marketplace/plugins/house-skills/skills/adventures-storyboard-preflight/SKILL.md
  provenance-name: "MARK-9 chunk ledger \xC3\xA2\xE2\u201A\xAC\xE2\u20AC\x9D Adventures"
license: "MIT"
---
# Adventures Storyboard Preflight

Use this skill when Harley asks ordinary GPT/project workflow to storyboard Adventures frames, make prompt boards, map slide visuals, prepare visual planning packets, or preflight story beats before image generation. Use it to produce deterministic planning inputs that may later support image preflight, QA, deck planning, or asset work.

## Owned decision

Create or review deterministic storyboard/prompt-board planning outputs, decide whether the board is preflight-ready, needs repair, should be handled by direct GPT deterministic planning, or should route to another visual skill.

## Hard boundaries

Do not generate, regenerate, or edit images from this skill. Storyboards and prompt boards are deterministic planning artifacts. For ordinary GPT/project workflow, an accepted board does not authorize image generation; visible mutation still routes through Adventures visual intent and image preflight.

Do not let operator context, issue text, QA notes, or session continuity leak into board copy or image prompts.

## Actor boundary

This is a GPT/project-side deterministic planning skill. It may create lightweight storyboard, prompt-board, reference-lock, and prompt-safe planning packets directly. It is not an image-generation execution skill, and its no-generation posture applies only to this planning lane.

## Progressive references

Read `references/storyboard-operating-contract.md` when you need the full storyboard/prompt-board workflow, output schemas, QA-ready criteria, source-route posture, or failure handling.

Read `references/prompt-board-contract.md` before producing or validating a prompt board.

For normal deterministic script execution, do not read scripts. Use the operating contract command recipes. Inspect scripts only after execution fails, when validating package contents, or when explicitly editing them.

## Minimal workflow

1. Classify the requested board/planning artifact and decide the lightest deterministic planning route.
2. Gather frame, world, visual bible, and source constraints.
3. Produce or validate lightweight deterministic storyboard/prompt-board output.
4. State readiness or exact repairs.
5. Stop before image generation.
