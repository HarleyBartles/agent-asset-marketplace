# Post-Merge Closeout and Planning-Artifact Lifecycle Design

## Status

Approved in conversation on 2026-09-19. This specification is a committed,
in-flight execution artifact. It must leave the tracked tree in the completing
PR after any enduring decisions have been promoted to their owning surfaces.

## Problem

Portable branch closeout currently assumes ancestry-preserving integration,
while squash merge is common and externally merged PRs may return after the
original execution context has compacted. The worktree-removal helper is also
owned by `using-git-worktrees` and couples forced submodule deinitialization to
forced worktree removal.

Separately, `writing-plans` calls plans "durable, tracked files" even though the
portable and repository custody model requires completed plans, specifications,
roadmaps, and checkpoints to leave the tracked tree. Agent-operating-model
requires the completed-artifacts doctrine but does not scaffold the planning or
completion compositions that make the lifecycle actionable for consumers.

## Approved outcomes

1. `finishing-a-development-branch` owns both pre-integration decisions and
   post-merge branch/worktree retirement, including discovery language for an
   externally merged PR.
2. Post-merge retirement verifies the exact published head, merged state,
   expected base, and the recorded merge result in current base history.
   Preserved ancestry selects ordinary branch deletion; verified non-ancestry
   integration permits deliberate force deletion. A moved head or ambiguous
   integration stops cleanup.
3. The removal helper moves to `finishing-a-development-branch`.
   `using-git-worktrees` retains creation/setup ownership and points closeout to
   the finishing skill.
4. Consumer-owned worktree changes remain protected. Content dirt left inside
   consumer submodules has no source custody and is discarded during routine
   teardown with `git submodule deinit --all -f`; the containing worktree is
   then removed without Git's worktree `--force`.
5. Worktree `--force` remains a distinct, explicitly destructive route for
   consumer-owned modified or untracked state.
6. Portable planning skills call plans/specs/roadmaps/checkpoints committed,
   in-flight execution artifacts, never durable artifacts. They state at
   creation time that completion promotes enduring decisions and removes the
   finished artifacts from the tracked tree.
7. Agent-operating-model exposes reusable planning and completing-plan
   scaffolds, requires the completion playbook in its standard policy and
   default scaffold set, validates that requirement, and teaches consumers the
   same in-flight-to-retirement lifecycle for plans, specifications, roadmaps,
   checkpoints, and equivalent execution artifacts.
8. This repository's planning and completion compositions align with those
   reusable sources without weakening its existing completed-artifact doctrine.

## Non-goals

- Automating GitHub PR discovery or branch deletion in the helper.
- Treating squash as mandatory or inferring integration solely from convention.
- Preserving uncommitted content inside a consumer-owned submodule checkout.
- Retaining completed planning artifacts as repository evidence or examples.
- Creating a tracked completed-artifact archive.

## Acceptance evidence

- Focused tests witness RED then GREEN for helper ownership, clean submodule
  teardown, dirty consumer-worktree protection, and workflow language.
- Marketplace and installed projections converge from canonical sources.
- Agent-operating-model scaffold tests prove planning/completion templates and
  required policy are available to consumer repositories.
- The normal hooked commit proves the final staged snapshot.
- Before the PR is ready, this specification and its implementation plan are
  removed after promotion checks; Git history remains the record.
