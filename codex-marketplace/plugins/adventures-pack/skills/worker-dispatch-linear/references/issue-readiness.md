# Linear Issue Readiness

Read when creating or updating a Linear issue for future worker execution.

A Linear issue is worker-ready when a future execution actor can read it and know:

- repository or implementation surface;
- exact goal as observable state;
- in-scope changes;
- out-of-scope/protected surfaces;
- validation commands or acceptable validation evidence;
- expected return evidence;
- publication or PR expectations, if any;
- GREEN/AMBER/RED/BLOCKED criteria when useful.

Do not require YAML unless the target worker or user explicitly asks for it. Boring means executable, bounded, and falsifiable, not verbose.

## Compact issue shape

Use ordinary markdown headings:

- Problem
- Goal
- Scope
- Guardrails
- Validation
- Return evidence
- Success criteria

For small tasks, collapse headings into concise paragraphs.

## Worker lane wording

Use lightweight lane wording only when it changes execution:

- `worker-ready`: issue is clear enough for a future worker.
- `planning-only`: do not implement yet.
- `native-gpt-route`: belongs to ChatGPT skill, connector, UI, research, or packaging work rather than repo work.
- `external-worker-handoff`: user wants paste-ready text for a worker outside this chat.

Do not name or imply an execution provider unless the user explicitly names one.

## Publication wording

When PR publication is expected, include:

`When implementation is complete, return evidence in Linear, including validation output and any PR/branch/commit link if one is created. Do not require hidden credentials or unmentioned publication routes.`
