# Linear Worker State Machine

Read when checking worker-shaped issue status, resuming a session, handling a worker return, or deciding whether to verify a PR.

## States

`planned`
: Linear issue exists but is not yet worker-ready. Next action: make it worker-ready or ask what should be clarified.

`worker-ready`
: Issue is shaped for a future worker, but no execution evidence exists. Next action: report that it is ready; do not claim it has been sent.

`in-progress`
: Linear state, assignee, labels, or comments indicate someone is working. Next action: report observable Linear state only.

`returned`
: A worker report, completion note, or validation summary exists. Next action: summarize claims and identify required proof or follow-up.

`pr-created`
: Linear has a PR attachment/comment/URL, or the user provides a PR. Next action: verify the GitHub PR diff, state, checks, and issue-goal conformance.

`landed`
: PR is merged and final main state is verified. Next action: report landed state; update or close Linear only when authorized by latest instruction or durable project policy.

`blocked`
: Required source, authority, access, validation, or publication proof is missing. Next action: name the blocker and the smallest safe next step.

## Evidence order

For status checks, inspect Linear before GitHub:

1. issue fields: state, assignee, project, labels, links, attachments;
2. comments: worker reports, validation notes, PR links, blockers;
3. PR attachment/URL, if present;
4. GitHub PR only after a PR URL/number/branch/commit exists.

## Report shape

Use the smallest useful report:

- `Linear`: issue state and relevant comment/attachment signal.
- `Worker`: only what Linear or user-provided evidence supports.
- `GitHub`: PR/branch/commit state only when present.
- `Next gate`: exact next action.
