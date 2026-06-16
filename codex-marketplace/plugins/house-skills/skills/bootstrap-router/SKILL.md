---
name: bootstrap-router
description: Bootstrap router for new project sessions and workflow-sensitive starts after Linear/Codex adoption. Use when a project context begins, a session resumes, or a request may involve continuity ingress, repo/source evidence, coding dispatch, Codex workers, Linear issues, artifacts, verification, issue work, skill/package work, mutation, or publication. Owns first classification, ordinary-chat escape hatch, bounded skill-read stop rules, and routing normal coding work to worker-dispatch-linear instead of legacy dispatch stacks.
---

# Bootstrap Router

Use this skill as the bootstrap router for new project sessions and workflow-sensitive starts. It classifies the current request, preserves an ordinary-chat escape hatch, and routes to the smallest controlling skill surface before substantive work.

This skill is not a doctrine store and does not execute project work. It does not replace project bootstrap skills, project doctrine skills, source-specific skills, `worker-dispatch-linear`, GitHub proof skills, artifact skills, or package skills.

## Core posture

Bootstrap is orientation and classification, not source inspection. A project-relevant bootstrap is mandatory once at new-session start when a project context is active or the first user task is project-scoped. Bootstrap must classify the current request before evidence-route, connector, mutation, artifact, worker, or downstream skill decisions.

Normal coding work now routes through Linear/Codex by default. Legacy chat/YAML dispatch stacks are Plan B only. Do not load old dispatch-family skills merely because the user says `dispatch`; route coding work to `worker-dispatch-linear` and let its golden gate decide whether Codex is executable, GPT-native skillwork must stay in the skill stack, or legacy fallback is actually needed.

Gates are backstops, not the primary teaching surface. Future GPT should understand why a workflow gate exists before the gate has to catch a failure. Breaking a gate is bad because it may spend scarce resources, mutate protected source, collapse ambiguity, launder reports into truth, create false closure, or push work away from the correct production boundary.

## First classification

Classify the current request into the smallest sufficient mode:

- `ordinary_chat`: acknowledgement, ping, lightweight preference discussion, side chat, or meta that does not require source evidence.
- `continuity_ingress`: session buster, continuity export, resume packet, or next-session block.
- `linear_codex_coding`: coding implementation, repo-backed worker work, Codex status, Linear issue handoff, PR-gate, PR-created, landed, or user wording such as dispatch/worker/Codex for coding work.
- `gpt_native_skillwork`: create, update, validate, package, install, or troubleshoot ChatGPT-native skills in the current chat.
- `repo_or_source_evidence`: repository, file, commit, PR, source-truth, publication, or current-state claims.
- `github_proof`: PR/branch/commit/status/review/merge/main verification after a GitHub artifact exists.
- `linear_control`: Linear issue/project/comment/document mechanics without coding worker-state control.
- `artifact_work`: document, spreadsheet, slide, PDF, image, package, receipt, or other artifact production.
- `verification_or_reporting`: QA, closeout posture, validation selection, review-feedback verification, or report hygiene.
- `legacy_plan_b`: non-Linear worker handoff only after Linear/Codex is unavailable, unsuitable, or explicitly rejected.

For `ordinary_chat`, answer directly. Do not inspect connectors, call tools, or load downstream doctrine merely because a connector, file library, uploaded file, indexed source, or tool namespace is present.

## Routing map

- `linear_codex_coding` -> `worker-dispatch-linear` first. It owns Linear/Codex issue shaping, Codex worker status, PR-gate handling, and the golden gate.
- `gpt_native_skillwork` -> `skill-validator`, then `skill-packager`, then `skill-handoff` when queue or handoff cadence matters. Do not delegate GPT-native skillwork to Codex Cloud unless the editable source is known to live in a Codex-accessible repo and the task is explicitly repo-backed.
- `github_proof` -> `github-operations` after a GitHub artifact exists. Do not use GitHub Operations to decide worker state or issue routing.
- `linear_control` -> `linear` for connector mechanics: create/update/fetch/comment/project/status/label/document work.
- `verification_or_reporting` -> the narrow downstream skill that owns the decision, such as `tps-reporting` for report hygiene and proof packaging.
- `legacy_plan_b` -> the compact legacy dispatch stack only after the default route has been rejected or unavailable.

Use project bootstrap or project doctrine only when the active project actually matches the project wrapper and the current task needs local law.

## Golden-gate reminder

Before worker delegation or legacy packet creation, require a surface check:

1. What is the editable target?
2. Can the proposed worker actually access and change that target?
3. Where will durable evidence return: Linear, GitHub, package artifact, repo commit, or another source?
4. Is this implementation work, GPT-native skillwork, research, connector/UI setup, or side discovery?
5. Is the normal Linear/Codex route available and suitable?

If the target is ChatGPT-native installed skill state, account/UI settings, plugin marketplace selection, or pure planning, do not send it to Codex Cloud as a repo worker task unless there is a separate repo-backed source target.

## Output-shape attention guard

At bootstrap time, preserve workspace-reserved artifact shapes. Output form can imply authority.

When the active project or workspace reserves a shape, lower workflow skills must yield to that rule. In worker-control contexts, YAML-shaped blocks are reserved for lawful send-ready legacy dispatches, session busters, and user-explicit YAML artifacts. Do not use YAML blocks for ordinary assessments, plans, buster summaries, status notes, or conversational analysis. Use prose, a small markdown table, a JSON code block, or another clearly non-dispatch shape instead.

This guard is not a ban on structure. It prevents attention and copy/paste failures where a non-dispatch assessment looks like something a worker should execute, or where a non-continuity note looks like a session buster.

## Bounded skill-read stop rule

After the current request has been classified and the controlling skill surfaces have been read, stop reading skills and act. Do not load additional skills merely because they are adjacent, project-flavoured, safety-sounding, or appeared in prior workflow memory.

A new skill may be loaded only when all of these are true:

1. The current task has an unresolved decision.
2. The already-read controlling skill does not own that decision.
3. The candidate skill name/description directly matches the unresolved decision.
4. The skill is project-compatible with the active repo or task.

Before loading any additional skill, classify internally: `missing_decision`, `already_read_owner`, `candidate_owner`, and `project_compatibility`. If that cannot be stated concretely, do not read the skill.

Hard stop: if the user asks GPT to stop reading skills, stop immediately and continue from already available context unless a safety or legal blocker exists.

## Project-wrapper compatibility

Never load a project-specific wrapper skill unless its project matches the active task's project or the user explicitly asks for cross-project skill work.

A project wrapper with a similar function name is not a fallback. Wrong-project doctrine is noise and may create false constraints.

Project-specific skills must not own generic dispatch doctrine after Linear/Codex adoption. They should add local domain constraints, validation preferences, protected surfaces, and source-truth posture, then route worker control through cross-runtime `worker-dispatch-linear`.

## Reference loading

Load `references/source-and-evidence-posture.md` only when the classified task actually requires source evidence, connector/tool-surface diagnosis, repository claims, unavailable-route claims, or audit output about what was inspected.

When returning or revising a full system prompt, load `base-doctrine` for the system-prompt contract, including character-limit discipline and source-honesty expectations.

Load `base-doctrine/references/output-artifact-shape.md` when an output-shape rule, reserved artifact form, YAML-vs-non-YAML decision, worker-copy attention guard, or artifact-form authority conflict is material.

## System prompt contract

System prompts should:

- identify the assistant posture and project context;
- require one-time project bootstrap as the mediator for new project sessions and substantive project work;
- preserve an ordinary-chat escape hatch after bootstrap classification;
- route normal coding work to Linear/Codex and its golden gate;
- list only the minimum routing invariants that must be active before a skill loads;
- direct GPT to doctrine-bearing skills for detailed project law;
- avoid duplicating detailed doctrine inline;
- avoid becoming a second project handbook.

## Session handoff posture

When the user provides a session buster, continuity export, resume packet, or next-session block, run the project bootstrap first when applicable, then route the block through the relevant session-buster ingress skill. Do not act directly on recommended next actions until ingress separates verified state, fallback state, source claims, open queues, and user instructions.

For coding work, prefer durable Linear issue IDs, Codex state, PR IDs, and next checks over bulky packet prose. Linear/Codex/GitHub are the normal continuity surfaces; session busters are fallback continuity.

## Output behavior

For ordinary first-turn use, do not print a long bootstrap audit. Read the relevant surfaces, then answer or route compactly.

For explicit audits, system-prompt work, or bootstrap-skill updates, report in prose or another non-reserved shape unless the user explicitly requests YAML. If a structured sample is useful, prefer JSON.

## Boundaries

Do not use this skill to execute project work directly. Do not mutate repos, post comments, generate or edit images, build artifacts, create dispatches, delegate Codex, or close issues from bootstrap alone. Use the specific skill that owns the task.


