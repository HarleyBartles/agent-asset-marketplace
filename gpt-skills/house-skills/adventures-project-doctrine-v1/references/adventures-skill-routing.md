# Adventures skill routing

Use the most specific current capability for the task.

## Direct-name rule

Do not hard-code ordinary downstream skill names when a task-capability handoff is enough. Direct skill names are allowed here only when the name is part of a stable composition or safety contract.

Allowed direct names in this routing surface:

- `adventures-bootstrap-v1`: the project arrival and routing pointer.
- `adventures-project-doctrine-v1`: this shared doctrine store.
- `adventures-visual-intent-gate`: the locked GPT-side Adventures current-turn image-credit authorization gate. Image-related GPT/project skills may name this directly as a must-read gate before GPT-side visible image mutation.
- PSA stack names (`psa-bootstrap`, `psa-board-production-doctrine`, `psa-brief-expander`, `psa-layout-planner`, `psa-deterministic-renderer`, `psa-board-qa`, `psa-return-contract`) may be named directly only when composing or describing Patch Storyboard Agent's assigned GPT-native deterministic pre-vis stack.
- PIG stack names (`pig-bootstrap`, `pig-image-production-doctrine`, `pig-brief-expander`, `pig-planning-surface-selector`, `pig-generation-execution`, `pig-self-qa-regeneration`, `pig-return-contract`) may be named directly only when composing or describing Patch Image Gen's assigned GPT-native production stack.

For other downstream work, describe the capability so future renames or wrapper replacements do not break routing.

## Capability routing map

- Shared Adventures repo, Patch, source-package, image-credit, presentation, and skill-routing doctrine: use this doctrine surface, then route to the specific current capability.
- Adventures GitHub issue shaping, durable issue comments, migration, triage, and closure posture: use the current Adventures GitHub issue-management capability.
- GitHub/repo evidence verification, commit/ref/package proof, and GREEN/AMBER/RED repo judgment: use the current Adventures GitHub operations evidence capability.
- GitHub issue ingestion into a production brief: use the current Adventures issue-ingestion capability.
- Frame/world verification or interactive shaping: use the Adventures frame-readiness capability and its theme, lesson, story, cast, environment, prop/state, and greenlight sub-capabilities as needed.
- Finished-deck contract checks: use the Adventures deck-doctrine capability.
- Slide/story/notes/sidecar planning: use the Adventures deck-planning capability.
- Body-slide image inventory, shot list, prompt pack, generation order, and QA-lane planning: use the Adventures deck image-planning capability.
- GPT-side current-turn image generation or generative-editing authority: use `adventures-visual-intent-gate`. This gate decides only whether the latest user turn authorizes ordinary GPT-side visible mutation now; it does not own readiness, QA, prompt quality, asset inspection, or PIG's internal production loop.
- PSA deterministic pre-vis production: route through the assigned PSA stack when a task needs storyboard panels, prompt boards, transition diagrams, route/geometry boards, repair boards, or other deterministic visual grounding artifacts. GPT should prepare paste-ready PSA packets; PSA owns deterministic PNG rendering and PSA self-QA only.
- PIG image production: route through the assigned PIG stack. GPT should prepare bounded PIG production packets, optionally including reviewed PSA board outputs as grounding inputs; PIG owns production-positive generation, self-QA, and bounded regeneration inside that job. GPT/Harley/project workflow owns external QA, acceptance, canon lock, deck-ready status, publication, and issue closure.
- Source/style/prompt readiness and credit-spend justification before an authorized GPT-side image call: use the Adventures image-preflight capability.
- Deterministic storyboards, prompt boards, diagrams, reference locks, and prompt-board packages: use the Adventures storyboard/prompt-board preflight capability for ordinary GPT-side lightweight work and PSA handoff preparation. For planned, multi-board, or specialist pre-vis production, prepare a self-contained paste-ready PSA handoff packet and route to PSA; PSA returns deterministic planning/control PNGs, not final art.
- Post-generation image candidate QA, compiled-sheet QA, and package image review: use the Adventures image-QA capability. QA and repair plans never mutate images.
- Deterministic accepted-image template compilation and blank template package authoring: use the Adventures asset-sheet compilation capability.
- Visual asset readiness before PPTX production: use the Adventures visual-preproduction capability.
- PPTX assembly after accepted image QA and deck-plan readiness: use the Adventures PPTX build capability.
- Presentation/package/stage QA: use the Adventures presentation-QA capability.
- Embedded-image receipt generation from PPTX artifacts: use the Adventures receipt-generation capability.
- Receipt/source-package zip ingress and evidence mapping: use the Adventures receipt/package ingress capability.
- Worker-facing execution packets, Patch dispatches, replacement dispatches, and material nudges: use the current Adventures dispatch route and its preparation/boundary capabilities.

## Broken-link degradation lesson

A routing map should not fossilize replaceable implementation names. When an ordinary handoff can be described as a capability, use the capability description. Name a skill directly only when the exact installed surface is the contract, as with the locked image-credit gate or an explicit base/wrapper composition.
