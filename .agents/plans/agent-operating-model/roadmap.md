# Agent Operating Model Roadmap

## Goal

Deliver the approved `agent-operating-model` plugin as a sequence of green,
reviewable changes while preserving the accepted runbook/playbook taxonomy and
the public `repo-standards` invocation contract.

## Plan sequence

| # | Title | Status | Plan File | Commit | PR | Rating | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Finish runbook/playbook separation | done | `2026-09-18-plan-1-finish-pr-321.md` | `f111c3f02` | [#321](https://github.com/HarleyBartles/agent-asset-marketplace/pull/321) | - | Merged to `main` as `daee89c1a`. |
| 2 | Build Agent Operating Model plugin | ready | `2026-09-18-plan-2-build-agent-operating-model.md` | - | [#322](https://github.com/HarleyBartles/agent-asset-marketplace/pull/322) | - | One implementation plan for plugin creation, custody moves, focused skills, regeneration, and validation. |

## Global sequencing constraints

- Plan 1 owns PR #321's disposition. No later plan may assume the
  runbook/playbook taxonomy exists on `main` until GitHub proves it.
- Every custody move has one canonical source home and regenerates downstream
  manifests, installed projections, indexes, and mesh surfaces.
- Each plan must leave the marketplace installable and the complete local gate
  green.
- Existing public skill names and consumer-facing command contracts remain
  compatible unless a later approved design explicitly changes them.
- Plan 2 is written just-in-time from current repository and GitHub state.

## Handoff notes

- The design is recorded in
  `.agents/specs/2026-09-18-agent-operating-model-design.md` and Draft PR #322.
- PR #321 currently has a valid published head plus uncommitted review
  corrections and an abandoned standalone `python-pack` experiment in its
  worktree. Plan 1 separates those states rather than discarding the worktree.
- If #321 cannot be completed, update this roadmap before writing a
  superseding plan. Replacement proof must include the entire accepted
  runbook/playbook separation.
