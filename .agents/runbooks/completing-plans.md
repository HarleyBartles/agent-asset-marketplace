# Completing planning artifacts

## When

An implementation PR completes an in-flight plan, specification, roadmap,
checkpoint, or similar planning artifact.

## Required skills

- `cleanup-custody` - custody classification and the promotion-before-removal
  step.
- `generating-agent-mesh` - regenerate the index mesh after removal.
- `verification-before-completion` - completion evidence.

## Composition

1. Invoke `cleanup-custody` and classify each artifact. In-flight artifacts
   stay `keep_live` while they govern implementation and review.
2. Apply promotion-before-removal: enduring architecture decisions to `adr/`,
   operating rules to `.agents/doctrine/` or `.agents/runbooks/`.
3. Remove the exact tracked artifacts with Git-aware deletion.
4. Optionally place a disposable convenience copy under
   `_agent-scratch/<repo-name>/completed/<artifact-type>/`. This centralized
   disposable store is the only scratch custody for finished paperwork; a copy
   is optional and proves nothing.
5. Regenerate the mesh and commit the resulting tree in the completing PR.

## Doctrine and contracts

- `.agents/doctrine/completed-artifacts.md` - completed artifacts are not
  retained, are not authority, and git history is the immutable record.

## Local commands and paths

- `py -3 tools/run.py mesh --apply` regenerates the index mesh.
- `adr/` holds durable architecture decisions.

## Evidence contract

Git history is the immutable record. Completion creates no manifest, count,
archive index, or recurring PR-reporting duty.

## Prohibited combinations

- Do not treat a completed artifact as a source of canonical commands, an
  implementation template, or an example of current conventions.
- Do not retain completed artifacts under a `completed/` directory inside
  `.agents/plans/`, `.agents/specs/`, or `.agents/roadmaps/`.
