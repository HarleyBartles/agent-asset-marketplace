---
name: worker-dispatch-linear
description: gpt-wide coding dispatch control plane for Linear plus Codex Cloud. Use for coding implementation requests, repo-backed worker dispatch, checking Codex worker status, Linear issue handoff, PR-gate handling, or any user phrase such as dispatch, worker, Codex, Linear issue, worker returned, ready for PR, verify PR, or landed. Owns the decision to route coding work through Linear/Codex by default, and the golden gate that blocks Codex delegation when the task is not executable from a Codex Cloud repo environment. GitHub Issues and chat/YAML dispatch are legacy fallback only.
metadata:
  source-id: worker-dispatch-linear
  source-path: plugins/house-skills/skills/worker-dispatch-linear/SKILL.md
  provenance-name: "MARK-9 chunk ledger \xC3\xA2\xE2\u201A\xAC\xE2\u20AC\x9D base and control plane"
license: "MIT"
---
# Worker Dispatch Linear

This skill is the GPT-wide front door for coding dispatch. The boring default is: shape the task in Linear, delegate to Codex only after the golden gate passes, watch Linear comments/attachments for worker state, use the Codex UI `Create PR` human gate when needed, then verify the GitHub PR or merged main state.

## Non-negotiable route

For normal coding work, `dispatch` means Linear issue plus Codex Cloud delegation, not a chat YAML packet.

Run the golden gate before delegating. If the task is GPT-native skill maintenance, connector setup, research, UI-only configuration, planning, or any surface that Codex Cloud cannot edit and publish from its repo-bound environment, do not delegate to Codex. Use the appropriate native route instead.

Read `references/golden-gate.md` before any delegation, worker launch, nudge, or conversion of planning into execution.

## Normal workflow

1. Classify the request.
   - `coding_dispatch`: create/update a Linear issue and consider Codex delegation.
   - `status_check`: fetch the Linear issue, comments, attachments, delegate, and state.
   - `pr_verification`: inspect GitHub only after Linear has a PR attachment/comment or the user gives a PR.
   - `native_or_planning`: do not delegate; route to the native skill, connector, research, or planning path.
2. For coding dispatch, read `references/issue-readiness.md` and make the issue boring enough for a worker.
3. Run `references/golden-gate.md`.
4. If the gate passes and the latest user turn authorizes dispatch, delegate the Linear issue to Codex.
5. For follow-up or session pickup, read `references/state-machine.md`, then inspect Linear before asking Harley for worker status.
6. If Linear shows `returned/pr-gate`, tell Harley to open the Codex task link from the Linear thread and click `Create PR`.
7. If Linear shows `pr-created`, switch to GitHub verification. Use GitHub tools/skills only for repo proof.
8. Use `references/legacy-plan-b.md` only when Linear/Codex is unavailable, not connected, explicitly rejected by Harley, or the task fails the golden gate but still needs a non-Linear handoff.

## Linear as event log

Treat the Linear issue as the durable task contract. Treat Linear comments and attachments as the worker event log. Do not require Harley to say "the worker returned" before checking; if the current task is status, pickup, worker follow-up, or PR readiness, fetch Linear and decide from observable state.

Important signals:

- Codex delegate or Codex thread exists: worker may be running.
- Codex completion/report comment exists and no PR link exists: human PR gate.
- `Created pull request` comment or PR attachment exists: verify GitHub PR.
- PR merged and main verified: landed.

## GitHub boundary

GitHub proves repo facts: PR metadata, diff, statuses, review comments, merge state, commits, files, and main head. GitHub Issues are not the default coding control plane when Linear/Codex is available.

Do not use shell GitHub credentials, PATs, or raw `git push` as the normal fix for Codex Cloud publication. The normal publication route is Codex-native PR creation behind the human `Create PR` gate.

## Skill-read stop rule

After this skill classifies the route, do not read old dispatch skills or GitHub issue skills merely for comfort. Load another skill only for a named unresolved decision that this skill does not own:

- skill creation/update/package work: use the skill-maintenance stack;
- GitHub PR/repo proof: use GitHub verification tooling;
- validation choice after code/PR evidence exists: use validation guidance;
- project-specific domain constraints: use only the matching project wrapper.

If Harley says the route is too wide, wrong, or not boring, stop expanding the skill set and return to Linear/Codex state plus the golden gate.
