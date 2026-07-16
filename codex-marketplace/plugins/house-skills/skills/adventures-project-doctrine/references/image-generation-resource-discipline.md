# Image generation resource discipline

Image generation credits are scarce Adventures production capacity for ordinary GPT-side project work. Unnecessary image-generation or generative-edit
calls can exhaust credits and block visual preproduction, preprod-ready work, deck-ready work, and production until
credits refresh.

Deterministic workflows exist to reduce failed GPT-side image calls and conserve those credits. Calling image generation during
deterministic GPT-side work defeats the purpose of those workflows and is a project-critical failure, not a harmless extra
attempt.

## Actor split

Do not apply GPT-side fear-of-generation posture to Patch Storyboard Agent (PSA) or Patch Image Gen (PIG) in the wrong way. PSA is deterministic-production-positive for storyboard, prompt-board, route/geometry, repair, and planning/control PNGs; it must not use generative image tools. PIG is production-positive for bounded image generation.

Do not apply GPT-side fear-of-generation posture to Patch Image Gen (PIG). PIG is a production image actor. Inside a valid bounded PIG production job, image generation and bounded regeneration are normal production actions, governed by the PIG skill stack and the job boundary. PIG still must not waste credits, drift beyond the brief, or claim final acceptance.

For GPT-side direct image calls, current-turn authorization and one-call stop points remain mandatory. For PSA jobs, GPT should provide paste-ready deterministic board packets and then review returned boards as planning/control artifacts. For PIG jobs, GPT should provide bounded production packets, optionally carrying reviewed PSA boards as grounding inputs, and external QA/acceptance after PIG returns candidates.

PSA self-QA is not GPT QA, PIG self-QA, Harley acceptance, canon lock, deck-ready status, repo/project acceptance, publication, or issue closure. PIG self-QA is not GPT QA, Harley acceptance, canon lock, deck-ready status, repo/project acceptance, publication, or issue closure.

Use the repo playbook `playbooks/image-generation-resource-discipline.md` as the full durable source when repo access is
available. This reference is the compact installed-skill doctrine for routing before the repo surface is loaded.

## Operation classes

Classify visual work before tool selection:

- `deterministic_no_credit`: repo inspection, issue/comment work, GPT-side prompt boards/storyboards, PSA handoff packets, PSA-return review, QA, repair planning,
  reference selection, contact sheets, asset-sheet compilation, template work, receipts, package validation, skill work,
  policy discussion, and readiness reports.
- `non_credit_pixel_work`: deterministic PIL layout, PSA storyboard/prompt-board PNG rendering, crops, annotations, template placement, contact-sheet rendering,
  and package previews.
- `credit_spending_mutation`: generate a new image candidate, regenerate a candidate, or generatively edit an image.

Only `credit_spending_mutation` may use image generation or generative editing.

## Why the gate exists

The visual intent gate is a production backstop, not the first place GPT should learn the rule. GPT should already understand that an image call creates new candidate state, consumes scarce production capacity, and can add QA, repair, cleanup, and continuity burden. The dangerous failure is visual-production momentum laundering itself into mutation because a prompt is ready, QA found a repair, a prompt board was accepted, the previous image failed, the workflow feels close, or the user said `continue`. None of those are current-turn authorization.

## Credit-spend rule

Do not call image generation merely because work involves images. Use image generation only when all are true:

- the latest user turn explicitly asks to create, regenerate, or edit pixels now;
- the workflow is at the proper visual-mutation stage;
- deterministic preparation is complete or explicitly waived;
- no deterministic route satisfies the request;
- spending the credit is expected to advance the production boundary rather than create churn.

Prior approval, active workflow, QA failure, accepted prompt board, repair plan, a ready prompt, or `continue` from an earlier turn is not image-generation authority by itself. Current-turn proof is required because older approval and assistant readiness go stale as soon as references, prompts, tools, or context shift.

## Deterministic routes

Route deterministic work to the owning skill:

- current-turn image-credit authorization: use the Adventures visual intent gate role;
- source/style readiness for an authorized image call: `adventures-image-preflight`;
- storyboards, prompt boards, diagrams, reference locks, and PSA handoff preparation: `adventures-storyboard-preflight-v1`; route planned or multi-board pre-vis production to PSA;
- image QA and repair packets: `adventures-image-qa-v1`;
- accepted-source asset-sheet compilation and template authoring: `adventures-asset-sheet-compiler-v1`;
- stage orchestration: `adventures-visual-preproduction-v1`.

If a deterministic route can satisfy the task, image generation is not merely unnecessary; it wastes the resource the
workflow is designed to conserve.
