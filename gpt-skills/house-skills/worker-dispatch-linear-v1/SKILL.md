# Worker Dispatch Linear v1

Use this skill as the GPT-wide front door for repo-backed coding dispatch through Linear and Codex Cloud. The boring default is: shape the task in Linear, delegate to Codex only after the readiness gate passes, watch Linear comments/attachments for worker state, use the Codex UI PR gate when needed, then verify the GitHub PR or merged main state before closing work.

## Non-negotiable route

For normal repo-backed coding work, dispatch means a Linear issue plus Codex Cloud delegation, not a chat YAML packet.

Run the readiness gate before delegating. If the task is GPT-native skill planning, connector setup, research, UI-only configuration, non-repo artifact work, or any surface that Codex Cloud cannot edit and publish from its repo-bound environment, do not delegate to Codex. Use the appropriate native route instead.

## Readiness gate

A task may be delegated to Codex only when all of these are true:

- the target repo is named;
- the issue goal is concrete;
- expected file/path surface is bounded enough for a worker;
- explicit non-goals are stated;
- validation expectations are stated;
- return contract is stated;
- source-of-truth route is clear;
- protected surfaces and mutation limits are clear;
- the work can be performed from the repo environment.

If the gate fails, keep shaping in Linear or route to the native/non-Codex path.

## Normal workflow

1. Classify the request.
   - `coding_dispatch`: create/update a Linear issue and consider Codex delegation.
   - `status_check`: fetch the Linear issue, comments, attachments, delegate, and state.
   - `pr_verification`: inspect GitHub only after Linear has a PR attachment/comment or the user gives a PR.
   - `native_or_planning`: do not delegate; route to the native skill, connector, research, or planning path.
2. For coding dispatch, make the issue boring enough for a worker.
3. Run the readiness gate.
4. If the gate passes and the latest user turn authorizes dispatch, delegate the Linear issue to Codex.
5. For follow-up or session pickup, inspect Linear before asking Harley for worker status.
6. If Linear shows returned work but no PR link, tell Harley to open the Codex task link from Linear and use the PR creation gate if needed.
7. If Linear shows a PR attachment or PR-created comment, switch to GitHub verification.
8. If the PR is green after verification and Harley has authorized the PR workflow, merge it, verify main, then close the Linear issue. Treat verification, merge, main proof, and issue closeout as one PR-completion workflow.

## Codex delegation mechanics

For Codex Cloud work in this workspace, set both human assignee and Codex delegate:

```json
{
  "assignee": "0f41920d-8499-4555-993d-066c003cf580",
  "delegate": "a1b0a6a6-48b3-4af6-9a99-744f5ae357d1"
}
```

The human assignee remains responsible for the issue. The Codex delegate is the coding worker. Do not delegate coding work to the Linear agent.

Connector mutation is not proof. After calling the Linear mutation, re-fetch the issue and require observable evidence before saying the worker is dispatched.

Valid dispatch evidence includes:

* `delegate: Codex`;
* expected human assignee;
* Todo or In Progress status;
* Codex activity/comment;
* PR attachment.

If mixed GitHub/Linear connector state causes Linear mutation or verification instability, prefer a Linear-only connector/tool context before retrying assignment/delegation. Do not blind retry.

## Linear as event log

Treat the Linear issue as the durable task contract. Treat Linear comments and attachments as the worker event log. Do not require Harley to say `the worker returned` before checking. If the current task is status, pickup, worker follow-up, PR readiness, or PR completion, fetch Linear and decide from observable state.

Important signals:

* Codex delegate or Codex thread exists: worker may be running.
* Codex completion/report comment exists and no PR link exists: human PR gate may be needed.
* `Created pull request` comment or PR attachment exists: verify GitHub PR.
* PR merged and main verified: landed.

## GitHub boundary

GitHub proves repo facts: PR metadata, diff, statuses, review comments, merge state, commits, files, and main head. GitHub Issues are not the default coding control plane when Linear/Codex is available.

Do not use shell GitHub credentials, PATs, or raw `git push` as the normal fix for Codex Cloud publication. The normal publication route is Codex-native PR creation behind the PR gate.

## PR completion workflow

When Harley gives a PR or Linear shows a PR attachment:

1. Inspect Linear issue state and PR attachment if needed.
2. Inspect GitHub PR metadata: open/closed, draft, mergeable, base, head SHA, changed files.
3. Inspect changed files or patch against the Linear issue goal.
4. Check validation evidence and status checks. If CI is absent, say so.
5. Decide RED/AMBER/GREEN.
6. If GREEN and Harley has authorized the PR workflow, merge with the verified head SHA.
7. Verify PR is closed/merged and main contains the expected landed state.
8. Close the Linear issue as Done only after merge/main proof.

## Stop rule

After this skill classifies the route, do not read old dispatch skills or GitHub issue skills merely for comfort. Load another skill only for a named unresolved decision that this skill does not own:

* skill creation/update/package work: use the skill maintenance stack;
* GitHub PR/repo proof: use GitHub verification tooling;
* validation choice after code/PR evidence exists: use validation guidance;
* project-specific domain constraints: use only the matching project wrapper.
