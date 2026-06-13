---
name: adventures-storyboard-preflight-v1
description: >-
  prepare GPT/project-side Adventures storyboards, prompt boards, PSA handoff packets, and deterministic no-credit visual planning. use when Harley asks ordinary GPT to storyboard frames, make prompt boards, map slide visuals, preflight story beats, or produce visual planning packets, or route planned/multi-board pre-vis work to PSA before image generation; may produce packets for PSA or PIG, but never grants generation authority or governs either agent's internal production.
---

# Adventures Storyboard Preflight v1

Use this skill when Harley asks ordinary GPT/project workflow to storyboard Adventures frames, make prompt boards, map slide visuals, prepare visual planning packets, or preflight story beats before image generation. Use it to produce deterministic handoff inputs that may later be given to PIG, but not to govern PIG internal production planning.

## Owned decision

Create or review deterministic storyboard/prompt-board planning outputs, decide whether the board is preflight-ready, needs repair, should be routed to PSA for specialist deterministic production, or should route to another visual skill.

## Hard boundaries

Do not generate, regenerate, or edit images from this skill. Storyboards and prompt boards are deterministic no-credit planning artifacts. For ordinary GPT/project workflow, an accepted board does not authorize image generation; visible mutation still routes through Adventures visual intent and image preflight. For PSA, a handoff produced here is only a paste-ready work packet; PSA rendering authority remains in the PSA stack. For PIG, a board produced by GPT or returned by PSA is only an input to a separately bounded PIG production job; PIG planning authority remains in the PIG skill stack, especially pig-planning-surface-selector, not in this skill.

Do not let operator context, issue text, QA notes, or session continuity leak into board copy or image prompts.


## Actor boundary

This is a GPT/project-side deterministic planning skill. It may create lightweight storyboard, prompt-board, reference-lock, and prompt-safe handoff packets directly. For planned, multi-board, batch, or specialist pre-vis work, it should prepare a self-contained PSA handoff packet instead of trying to act as PSA. It may also prepare prompt-safe handoff packets for later PIG use, but it is not PSA rendering doctrine and not PIG execution doctrine. Do not import this skill's no-generation posture into PIG's bounded production loop. PIG may use its own planning-surface selector inside an assigned image-production job.

## Progressive references

Read `references/storyboard-operating-contract.md` when you need the full storyboard/prompt-board workflow, output schemas, QA-ready criteria, source-route posture, or failure handling.

Read `references/prompt-board-contract.md` before producing or validating a prompt board.

Read `references/psa-handoff-contract.md` before writing a GPT-to-PSA handoff packet or reviewing PSA board returns.

For normal deterministic script execution, do not read scripts. Use the operating contract command recipes. Inspect scripts only after execution fails, when validating package contents, or when explicitly editing them.

## Minimal workflow

1. Classify the requested board/planning artifact and decide direct GPT deterministic work versus PSA handoff.
2. Gather frame, world, visual bible, and source constraints.
3. Produce or validate lightweight deterministic storyboard/prompt-board output, or emit a paste-ready PSA handoff packet for larger/specialist board production.
4. State readiness or exact repairs.
5. Stop before image generation.
