---
name: tps-reporting
description: Use when partition reports, worker returns, Linear/Codex status notes,
  issue comments, verification summaries, publication notes, and continuity notes
  so claims do not become truth. Use when drafting or reviewing language that could
  mix source evidence, Codex/worker claims, Linear state, GitHub proof, inference,
  validation, closure posture, or next action. Do not use for ordinary coding dispatch
  routing; Linear/Codex state checks belong to the dispatch front door, and GitHub
  proof belongs to GitHub Operations after a PR or repo artifact exists.
metadata:
  source-id: tps-reporting
  source-path: sources/first_party/skills/tps-reporting/SKILL.md
  provenance-name: Tps Reporting first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when partition reports, worker returns, Linear/Codex status notes, issue
    comments, verification summaries, publication notes, and continuity notes so claims
    do not become truth. Use when drafting or reviewing language that could mix source
    evidence, Codex/worker claims, Linear state, GitHub proof, inference, validation,
    closure posture, or next action. Do not use for ordinary coding dispatch routing;
    Linear/Codex state checks belong to the dispatch front door, and GitHub proof
    belongs to GitHub Operations after a PR or repo artifact exists.
  use_when:
  - Use when partition reports, worker returns, Linear/Codex status notes, issue comments,
    verification summaries, publication notes, and continuity notes so claims do not
    become truth. Use when drafting or reviewing language that could mix source evidence,
    Codex/worker claims, Linear state, GitHub proof, inference, validation, closure
    posture, or next action. Do not use for ordinary coding dispatch routing; Linear/Codex
    state checks belong to the dispatch front door, and GitHub proof belongs to GitHub
    Operations after a PR or repo artifact exists.
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
license: MIT
---
# Tps Reporting

Use this skill to draft or review report-like surfaces without laundering claims into truth.

## Owned decision

Decide how a report should partition authority. Keep source evidence, worker claims, Linear/Codex state, GitHub proof, validation evidence, inference, verifier judgment, and next action visibly separate.

This skill does not dispatch workers, check running status, validate code, verify GitHub artifacts, mutate issues, close work, or own project doctrine.

## Linear/Codex boundary

For normal coding work, Linear/Codex is the control plane and GitHub is the proof surface after publication. Reporting Hygiene only shapes how to say what is known.

Do not use this skill to decide whether a task should be delegated to Codex Cloud. That golden gate belongs to the Linear/Codex dispatch front door.

Do not use this skill to poll Linear comments or attachments for worker state. Use the Linear/Codex route. Once that route has evidence, use this skill only if the response needs report partitioning.

Do not use this skill to inspect a GitHub PR, branch, commit, status, or merge state. Use GitHub Operations for proof, then use this skill only to phrase the report without overclaiming.

## Compact coding report shape

For Linear/Codex coding workflow reports, prefer this short shape:

```text
Linear state: issue/delegate/comment/attachment evidence.
Codex state: running, returned/pr-gate, or PR-created, with source basis.
GitHub state: PR/branch/main proof if a GitHub artifact exists.
Next gate: the one action now needed.
```

Use GREEN/AMBER/RED only when the user asks for verification, closure readiness, or issue-goal conformance. Do not turn every worker return into a tribunal.

## Report laundering hard stops

Reports are compressed custody surfaces, not source truth.

Do not let any of these become stronger than their source:

- a Codex completion comment;
- a Linear issue comment;
- a PR body;
- a worker's validation summary;
- a clean worktree claim;
- a package receipt;
- a passed test summary;
- a session buster;
- a prior GPT report.

When publication is claimed, name the publication proof: Linear PR attachment, GitHub PR, pushed branch, merged PR, exact package evidence, or other durable artifact.

When closure is claimed, compare observable state against the issue goal. Validation, comments, and PR existence are not closure by themselves.

## Skill-read stop rule

After classifying the report and the evidence lanes needed, stop reading skills. Do not load dispatch, validation, session-buster, GitHub, artifact, image, or wrong-project skills merely because the report mentions them.

Load another skill only when a named unresolved decision is outside this skill's ownership and the candidate skill directly owns it. Use only project-compatible wrappers when local report law is actually required.

If the user says to stop reading skills, stop immediately and continue from already available context unless a safety blocker remains.

## Progressive references

Read `references/reporting-hygiene-contract.md` only when drafting or reviewing a full report, worker return, proof summary, continuity note, publication note, receipt summary, closure posture, or false-GREEN risk.

Do not load the reference for a simple known-target issue comment unless the comment asserts verification, publication, closure readiness, worker-return truth, or another report-like proof claim.

## Minimal workflow

1. Classify the artifact: status note, worker return, publication note, verification report, closure summary, continuity note, or simple comment.
2. Identify the source lanes actually present.
3. Keep evidence, claim, inference, judgment, and next action separate.
4. Challenge wording that upgrades claims into truth.
5. For Linear/Codex coding reports, use the compact coding report shape unless a full verification report is requested.
6. Stop before source mutation, repo mutation, closure, validation execution, or worker dispatch unless another workflow owns and authorizes that action.
