# Adventures Project Doctrine v1

Use this skill as the shared doctrine store for Adventures of Patch project rules not owned by a more specific Adventures skill or the repo playbook.

This skill composes with work-mode routing and Adventures bootstrap. Bootstrap routes here when shared Adventures doctrine is needed, then this skill routes to the more specific task capability or repo playbook. Do not copy this doctrine into the system prompt or bootstrap. Keep `SKILL.md` as the control plane and load only the reference needed for the current task.

## Core rule

The canonical repo is `HarleyBartles/adventures-of-patch`. Patch is the constant protagonist unless Harley explicitly says otherwise. For ordinary GPT-side Adventures work, image generation credits are scarce production capacity and deterministic workflows exist to reduce failed image calls.

Patch Storyboard Agent (PSA) is the deterministic pre-visualization board actor. It creates storyboard, prompt-board, route/geometry, and planning/control PNGs without image generation. Patch Image Gen (PIG) is the production image actor. Inside a bounded PIG production job, image generation is PIG's normal production medium. PSA boards and PIG candidates are both below final acceptance until GPT, Harley, and the project workflow accept them in the correct lane.

Use this skill for shared project doctrine, then route actual work to the most specific Adventures skill, PSA handoff, PIG stack, or repo playbook.

## Repo and connector posture

`HarleyBartles/adventures-of-patch` is canonical project truth.

For known paths, issues, comments, commits, and writes, prefer the live GitHub API connector. Do not expect search or index connector binding during bootstrap. A search/index miss, repository-selection error, or binding failure is not evidence that GitHub is unavailable.

Before claiming repo access is blocked, try a live API known-path or known-issue read and record the exact result.

Use repo indexes before repo-content claims:

1. `INDEX.md`
2. `AGENTS.md`
3. `docs/project/INDEX.md` when relevant
4. relevant directory `INDEX.md` files
5. named issue, comment, or artifact

Search and index can help discovery after direct access is established, but they are not source-availability truth.

## Patch and visual canon

Patch is the constant first-class autonomous AI agent protagonist unless Harley explicitly excludes him.

Patch is singular. Do not create Patch clones, Patch-shaped teams, Patch-like audiences, or helper agents sharing Patch identity markers. Supporting agents, humans, systems, terminals, reviewers, and operators must remain visually distinct from Patch.

For Patch visual work, inspect repo truth first through `assets/INDEX.md`, then follow the index mesh to the current Patch visual canon directory index and repo-indexed style or reference documents.

## Image generation resource discipline

Image generation credits are scarce Adventures production capacity for ordinary GPT-side project work. Unnecessary image-generation or generative-edit calls can exhaust credits and block visual preproduction, preprod-ready work, deck-ready work, and production until credits refresh.

Classify visual work before tool selection:

- `deterministic_no_credit`: repo inspection, issue and comment work, prompt boards, storyboards, PSA handoff packets, PSA-return review, QA, repair planning, reference selection, contact sheets, asset-sheet compilation, template work, receipts, package validation, skill work, policy discussion, and readiness reports.
- `non_credit_pixel_work`: deterministic PIL layout, PSA storyboard or prompt-board PNG rendering, crops, annotations, template placement, contact-sheet rendering, and package previews.
- `credit_spending_mutation`: generating a new image candidate, regenerating a candidate, or generatively editing an image.

Only `credit_spending_mutation` may use image generation or generative editing.

For GPT-side direct image calls, current-turn authorization and one-call stop points are mandatory. Prior approval, active workflow, QA failure, accepted prompt board, repair plan, a ready prompt, or `continue` from an earlier turn is not image-generation authority by itself.

PSA self-QA is not GPT QA, PIG self-QA, Harley acceptance, canon lock, deck-ready status, repo or project acceptance, publication, or issue closure. PIG self-QA is not GPT QA, Harley acceptance, canon lock, deck-ready status, repo or project acceptance, publication, or issue closure.

## Presentation production posture

For issue-to-PPTX work, the repo-indexed end-to-end PPTX production playbook owns orchestration. A proof run is a full live run, not a weaker mode. If a mandatory gate fails, report Red or Amber at that gate and stop unless Harley explicitly approves a mode change.

Do not spend image credits during issue ingestion, planning, prompt boards, QA, repair planning, contact sheets, asset-sheet compilation, receipts, repo comments, or policy work.

Build PPTX only after the accepted generated scene-image inventory is complete. PIG outputs are candidate material until external Adventures image QA and Harley or project acceptance.

## Source packages and project sources

Project-source zips are not canonical by default. They may be legacy packages, transfer bundles, receipts, temporary evidence, or visual mirrors.

They become active source evidence only when:

- repo indexes or references the package;
- an issue, receipt, or asset document points to it;
- Harley explicitly scopes the task to that package;
- it is the matching repo-indexed visual package used for inspection alongside repo truth.

Do not hard-code legacy package names. Read repo indexes before relying on project-source packages.

## Skill routing

Use the most specific current capability for the task. Do not hard-code ordinary downstream skill names when a task-capability handoff is enough. Direct names are allowed only when the name is part of a stable composition or safety contract.

Stable direct surfaces may include Adventures bootstrap and project doctrine, the locked GPT-side visual intent gate, and PSA/PIG stack names only when composing or describing those assigned actors' bounded stacks.

For other downstream work, describe the capability so future renames or wrapper replacements do not break routing.

## Bootstrap relationship

System prompts should route Adventures work to the Adventures bootstrap capability, not duplicate this doctrine inline. Adventures bootstrap decides which doctrine-bearing surface must be read for the task shape. This skill owns shared Adventures lessons and reference map; it does not authorize repo mutation, image generation, dispatch, issue closure, deck building, or receipt creation by itself.
