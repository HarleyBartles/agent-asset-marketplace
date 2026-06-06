# Linear/Codex State Machine

Read when checking worker status, resuming a session, handling a worker return, or deciding whether to verify a PR.

## States

`planned`
: Linear issue exists and is not delegated. Next action: make it worker-ready or ask for dispatch authority.

`delegated/running`
: Issue has Codex delegate or Codex thread exists, but no completion/report comment. Next action: report that Codex appears to be running, or poll later if the user asked for monitoring.

`returned/pr-gate`
: Codex completion/report comment exists, but no PR attachment and no `Created pull request` comment exists. Next action: tell Harley to open the Codex task link from the Linear thread and click `Create PR`.

`pr-created`
: Linear has a PR attachment or a Codex `Created pull request` comment. Next action: verify the GitHub PR diff, state, checks, and issue-goal conformance.

`landed`
: PR is merged and final main state is verified. Next action: report landed state; update/close Linear only when authorized by latest instruction or durable project policy.

## Evidence order

For status checks, inspect Linear before GitHub:

1. issue fields: state, delegate, assignee, project, attachments;
2. comments: Codex thread, completion/report comment, `Created pull request` comment;
3. PR attachment URL, if present;
4. GitHub PR only after a PR URL/number exists.

## Report shape

Use the smallest useful report:

- `Linear`: issue state, delegate, relevant comment/attachment signal.
- `Codex`: running, returned/pr-gate, or published.
- `GitHub`: PR state only when present.
- `Next gate`: exact next action.
