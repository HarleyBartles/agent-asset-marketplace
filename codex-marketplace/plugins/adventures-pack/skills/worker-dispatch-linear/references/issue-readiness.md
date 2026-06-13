# Linear Issue Readiness

Read when creating or updating a Linear issue for Codex delegation.

A Linear issue is boring enough to delegate when a Codex worker can read it and know:

- repository or implementation surface;
- exact goal as observable state;
- in-scope changes;
- out-of-scope/protected surfaces;
- validation commands or acceptable validation evidence;
- expected return evidence;
- human PR gate behavior;
- GREEN/AMBER/RED/BLOCKED criteria when useful.

Do not require YAML unless the target system needs YAML or Harley explicitly asks for it.

## Compact issue shape

Use ordinary markdown headings:

- Problem
- Goal
- Scope
- Guardrails
- Validation
- Return evidence
- Success criteria

For small tasks, collapse headings into concise paragraphs. Boring means executable, not verbose.

## Worker lane hints

Use lightweight lane wording only when it changes execution:

- `cloud-codex-ok`: Codex Cloud can complete from the repo environment.
- `local-codex-required`: needs local resources not present in cloud.
- `planning-only`: do not implement yet.
- `native-gpt-route`: belongs to ChatGPT skill/connector/UI work, not Codex.

## Human gate wording

When PR publication should use Codex UI, include:

`When implementation is complete, return evidence in Linear. If the Codex UI offers Create PR, Harley will use that human gate; do not require shell GitHub credentials or PAT-based publication.`
