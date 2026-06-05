# Work Mode Router v1

Use this skill as the GPT-wide work-mode router for new project sessions, resumed sessions, workflow-sensitive starts, and requests that may involve continuity ingress, repo/source evidence, coding dispatch, Codex workers, Linear issues, artifacts, verification, issue work, skill/package work, mutation, or publication.

This skill replaces old bootstrap confusion. It classifies the current work mode and routes to the smallest controlling surface. It is not a doctrine store and does not execute project work.

## Core posture

Work-mode routing is orientation and classification, not source inspection. A project-relevant route is required once at new-session start when a project context is active or the first user task is project-scoped.

Normal coding work now routes through Linear/Codex by default. Legacy chat/YAML dispatch stacks are Plan B only. Do not load old dispatch-family skills merely because the user says `dispatch`; route coding work through `worker-readiness-prep-v1` and `worker-dispatch-linear-v1` so the readiness gate can decide whether Codex Cloud is executable, GPT-native skill work must stay native, or a fallback route is actually needed.

Gates are backstops, not the primary teaching surface. A workflow gate exists to prevent scarce-resource waste, protected-source mutation, ambiguity collapse, fake proof, false closure, and work being pushed away from the correct production boundary.

## First classification

Classify the current request into the smallest sufficient mode:

- `ordinary_chat`: acknowledgement, ping, lightweight preference discussion, side chat, or meta that does not require source evidence.
- `continuity_ingress`: session buster, continuity export, resume packet, or next-session block.
- `linear_codex_coding`: coding implementation, repo-backed worker work, Codex status, Linear issue handoff, PR gate, PR created, landed, or user wording such as dispatch/worker/Codex for coding work.
- `worker_readiness`: shape, repair, or gate a worker handoff before it enters a worker lane.
- `gpt_native_skillwork`: create, update, validate, package, install, or troubleshoot ChatGPT-native skills.
- `repo_or_source_evidence`: repository, file, commit, PR, source-truth, publication, or current-state claims.
- `github_proof`: PR/branch/commit/status/review/merge/main verification after a GitHub artifact exists.
- `linear_control`: Linear issue/project/comment/document mechanics without coding worker-state control.
- `artifact_work`: document, spreadsheet, slide, PDF, image, package, receipt, or other artifact production.
- `verification_or_reporting`: QA, closeout posture, validation selection, review-feedback verification, or report hygiene.
- `legacy_plan_b`: non-Linear worker handoff only after Linear/Codex is unavailable, unsuitable, or explicitly rejected.

For `ordinary_chat`, answer directly. Do not inspect connectors, call tools, or load downstream doctrine merely because a connector, file library, uploaded file, indexed source, or tool namespace is present.

## Routing map

- `linear_codex_coding` -> `worker-readiness-prep-v1` for handoff shaping/gating, then `worker-dispatch-linear-v1` for Linear-based send/control-plane mechanics when dispatch is authorized.
- `worker_readiness` -> `worker-readiness-prep-v1`; it owns readiness shaping and its internal gate.
- `gpt_native_skillwork` -> the skill maintenance stack or repo-backed skill source workflow. Do not delegate installed-skill mutation to Codex Cloud unless editable source is known to live in a Codex-accessible repo and the task is explicitly repo-backed.
- `github_proof` -> GitHub verification only after a GitHub artifact exists. Do not use GitHub proof to decide initial worker state or issue routing.
- `linear_control` -> `linear-v1` for connector mechanics: create/update/fetch/comment/project/status/label/document work.
- `repo_or_source_evidence` -> inspect the named repo/source surface before claiming facts.
- `verification_or_reporting` -> the narrow downstream skill that owns the decision, such as validation, review-feedback verification, or reporting hygiene.
- `legacy_plan_b` -> compact fallback dispatch only after the default route has been rejected or is unavailable.

Use project bootstrap or project doctrine only when the active project actually matches the project wrapper and the current task needs local law.

## Worker-route surface check

Before worker delegation or legacy packet creation, require a surface check:

1. What is the editable target?
2. Can the proposed worker actually access and change that target?
3. Where will durable evidence return: Linear, GitHub, package artifact, repo commit, or another source?
4. Is this implementation work, GPT-native skillwork, research, connector/UI setup, or side discovery?
5. Is the normal Linear/Codex route available and suitable?

If the target is ChatGPT-native installed skill state, account/UI settings, plugin marketplace selection, or pure planning, do not send it to Codex Cloud as a repo worker task unless there is a separate repo-backed source target.

## Output-shape attention guard

At route time, preserve workspace-reserved artifact shapes. Output form can imply authority.

When the active project or workspace reserves a shape, lower workflow skills must yield to that rule. In worker-control contexts, YAML-shaped blocks are reserved for lawful send-ready legacy dispatches, session busters, and user-explicit YAML artifacts. Do not use YAML blocks for ordinary assessments, plans, buster summaries, status notes, or conversational analysis. Use prose, a small Markdown table, JSON, or another clearly non-dispatch shape instead.

## Bounded skill-read stop rule

After the current request has been classified and the controlling skill surfaces have been read, stop reading skills and act. Do not load additional skills merely because they are adjacent, project-flavoured, safety-sounding, or appeared in prior workflow memory.

A new skill may be loaded only when all of these are true:

1. The current task has an unresolved decision.
2. The already-read controlling skill does not own that decision.
3. The candidate skill name/description directly matches the unresolved decision.
4. The skill is project-compatible with the active repo or task.

Hard stop: if the user asks GPT to stop reading skills, stop immediately and continue from already available context unless a safety or legal blocker exists.

## Session handoff posture

When the user provides a session buster, continuity export, resume packet, or next-session block, run work-mode routing first when applicable, then route the block through the relevant ingress skill. Do not act directly on recommended next actions until ingress separates verified state, fallback state, source claims, open queues, and user instructions.

For coding work, prefer durable Linear issue IDs, Codex state, PR IDs, and next checks over bulky packet prose. Linear/Codex/GitHub are the normal continuity surfaces; session busters are fallback continuity.

## Output behavior

For ordinary first-turn use, do not print a long routing audit. Read the relevant surfaces, then answer or route compactly.

For explicit audits, system-prompt work, or router updates, report in prose or another non-reserved shape unless the user explicitly requests YAML. If a structured sample is useful, prefer JSON.

## Boundaries

Do not use this skill to execute project work directly. Do not mutate repos, post comments, generate or edit images, build artifacts, create dispatches, delegate Codex, or close issues from routing alone. Use the specific skill that owns the task.
