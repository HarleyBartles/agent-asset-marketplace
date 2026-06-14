# External Worker Handoff

Read only when Harley explicitly asks for paste-ready worker instructions, a worker dispatch text, or a handoff that will be copied outside this chat.

This reference prepares text only. It does not launch a worker, assign a task, publish a branch, or mutate repository state.

## Handoff shape

Create the smallest durable handoff that names:

- target repo or surface;
- issue identifier or source context;
- goal as observable state;
- in-scope files or areas;
- out-of-scope/protected surfaces;
- validation expectations;
- required return evidence;
- publication expectation, if any.

Avoid large YAML packets unless the target worker requires that exact format. Ordinary markdown is preferred.

## Return evidence wording

Require the worker to return:

- branch name and commit SHA, if code changed;
- PR URL, if published;
- files changed summary;
- validation commands run and outputs;
- skipped validation with reason;
- known blockers or ambiguity.
