---
name: tps-ingress
description: Use when verify review, verifier, worker, issue, PR, automated-check,
  or external feedback before it becomes action, scope, evidence, closure posture,
  or worker instruction. use after Linear/Codex or GitHub feedback appears and the
  question is whether to accept, clarify, reject, route, or block it; do not use for
  ordinary worker-status polling, PR-gate detection, dispatch routing, or GitHub proof
  already owned by linear-issue-shaping and the repo/GitHub proof surface.
metadata:
  source-id: tps-ingress
  source-path: sources/first_party/skills/tps-ingress/SKILL.md
  provenance-name: Tps Ingress first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when verify review, verifier, worker, issue, PR, automated-check, or
    external feedback before it becomes action, scope, evidence, closure posture,
    or worker instruction. use after Linear/Codex or GitHub feedback appears and the
    question is whether to accept, clarify, reject, route, or block it; do not use
    for ordinary worker-status polling, PR-gate detection, dispatch routing, or GitHub
    proof already owned by linear-issue-shaping and the repo/GitHub proof surface.
  use_when:
  - Use when verify review, verifier, worker, issue, PR, automated-check, or external
    feedback before it becomes action, scope, evidence, closure posture, or worker
    instruction. use after Linear/Codex or GitHub feedback appears and the question
    is whether to accept, clarify, reject, route, or block it; do not use for ordinary
    worker-status polling, PR-gate detection, dispatch routing, or GitHub proof already
    owned by linear-issue-shaping and the repo/GitHub proof surface.
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
license: MIT
---
# Tps Ingress

Use this skill when feedback must be evaluated before it becomes action, scope, evidence, closure posture, or a worker instruction.

## Owned decision

Decide whether each feedback item should be accepted, clarified, rejected, routed, or blocked after checking current source reality, authority, protected-surface impact, and issue-goal relevance.

## Linear/Codex boundary

Linear/Codex workflow state is not review feedback by itself.

- Use `linear-issue-shaping` to check whether a Linear issue is planned, delegated/running, returned/pr-gate, pr-created, or landed.
- Use the repo/GitHub proof surface to verify a GitHub PR, commit, branch, status, review thread, merge, or main head.
- Use this skill when a Codex return, PR review, verifier note, issue comment, automated check, or external suggestion could change scope, become evidence, justify closure, or become a new worker instruction.

Do not convert feedback into a Codex dispatch. If feedback creates a new implementation task, first route through the Linear/Codex golden gate and issue-readiness path.

## Hard boundaries

Feedback is input for evaluation. It is not an order and not evidence by itself. Do not implement, dispatch, mutate protected surfaces, or upgrade closure posture from feedback text alone.

Do not apply the easy part of feedback while leaving related ambiguous or authority-sensitive parts unresolved if that would create partial compliance that looks green.

## Progressive references

Read `references/review-feedback-policy.md` when evaluating feedback for action, scope, evidence, closure posture, protected surfaces, worker instructions, or issue-goal conformance.

Do not read additional skills merely because feedback mentions a repo, issue, worker, PR, validation, or closure. Load another skill only when a named unresolved decision is outside this skill's ownership and the candidate skill directly owns it.

## Minimal workflow

1. Read all relevant feedback before acting on any item.
2. Classify each item by source, clarity, authority, risk, source evidence needed, protected-surface impact, and whether it affects Linear/Codex state, GitHub proof, validation, implementation scope, or closure.
3. Inspect current source, repo state, issue goal, durable Linear/GitHub evidence, and relevant law before accepting factual, technical, or closure claims.
4. Decide: accept, clarify, reject, route, or block.
5. Keep feedback text, verified evidence, planned correction, implementation, validation, publication proof, issue-goal conformance, and closure posture separate.
6. Push back with source-grounded reasoning when feedback is wrong, stale, unsafe, out of scope, or conflicts with authority.

## Source posture

For issue-backed work, feedback can support closure only after issue-goal conformance is checked against observable Linear/GitHub/repo state. Feedback is not a substitute for falsification checks.
