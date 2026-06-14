---
name: worker-dispatch-linear
description: Use for Linear-backed worker issue preparation and status handling: create or update worker-ready Linear issues, inspect Linear comments/attachments/state, prepare paste-ready worker handoffs when explicitly requested, and route GitHub PR proof after a PR exists. Do not launch, delegate, or assume any execution lane; treat worker-ready as issue-ready only.
---

# Worker Dispatch Linear

Use this skill as the GPT-wide control plane for Linear-backed worker readiness and worker event-log handling.

This skill does not launch workers, delegate execution, assume a worker provider, or treat any execution lane as available. It shapes durable Linear issue contracts and reads Linear state. A `worker-ready` issue is ready for a future execution actor to pick up; it is not proof that a worker has been sent.

## Core rule

Linear is the durable issue/control plane. The boring default is:

1. create or update a worker-ready Linear issue;
2. inspect Linear comments, attachments, assignee, labels, and status when checking progress;
3. prepare a paste-ready worker handoff only when Harley explicitly asks for one;
4. switch to GitHub proof only after a GitHub PR, branch, commit, or URL exists;
5. never claim execution, delegation, publication, merge, or closeout unless the target system proves it.

## Route classification

Classify the latest request before acting:

- `issue_shape`: create or update a Linear issue so a future worker can execute it.
- `worker_handoff_text`: draft a paste-ready worker handoff without mutating execution state.
- `status_check`: inspect Linear issue state, comments, and attachments.
- `pr_verification`: inspect GitHub only after a PR URL/number, branch, commit, or merged state exists.
- `native_or_planning`: route to the relevant GPT-native, connector, planning, or skill-maintenance path.

Phrases such as `worker ready`, `worker send ready`, `send-ready issue`, `worker-ready`, `make it boring`, or `make it executable` authorize issue shaping only. They do not authorize launching, assigning, delegating, or claiming that a worker is running.

## Normal workflow

1. For issue creation or update, read `references/issue-readiness.md` and make the issue boring enough for a future worker.
2. For status pickup, read `references/state-machine.md`, fetch Linear state first, then decide whether GitHub proof is available.
3. For paste-ready external handoff text, read `references/external-worker-handoff.md` and produce a compact handoff without mutating repo or issue state unless separately authorized.
4. For GitHub PR, branch, commit, merge, or main-state proof, hand off to GitHub verification tooling after the GitHub artifact is known.
5. Stop when the issue is shaped, the status is reported, or the next proof surface is named. Do not invent an execution lane to continue.

## Linear as event log

Treat Linear issue body, comments, attachments, links, assignee, labels, and status as the event log for worker-shaped work.

Useful signals:

- issue exists but lacks scope/validation/return evidence: make it worker-ready;
- issue has worker report/comment but no PR evidence: report returned state and ask for or prepare the next explicit handoff;
- issue has PR attachment/comment/URL: verify the GitHub PR;
- PR merged and main verified: report landed state and update/close Linear only when authorized.

## GitHub boundary

GitHub proves repo facts: PR metadata, diff, statuses, review comments, merge state, commits, files, and main head. GitHub Issues are not the default control plane when Linear is available.

Do not use Linear comments, worker reports, validation summaries, local paths, or generated package names as proof of repository state. Use GitHub proof after a GitHub artifact exists.

## Skill-read stop rule

After this skill classifies the route, do not read old dispatch or issue-management skills merely for comfort. Load another skill only for a named unresolved decision that this skill does not own:

- skill creation/update/package work: use the skill-maintenance stack;
- GitHub PR/repo proof: use GitHub verification tooling;
- validation choice after code/PR/package evidence exists: use validation guidance;
- project-specific domain constraints: use only the matching project wrapper.

If Harley says the route is too wide, wrong, or not boring, stop expanding the skill set and return to Linear issue state plus the smallest next safe action.
