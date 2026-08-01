# Completing plans and specs

Use this runbook when a plan and its associated spec(s) are delivered and the work is fully merged. It keeps `.agents/plans/` and `.agents/specs/` focused on in-flight work while preserving the historical record in a generated, indexed archive.

## When to archive

Archive a plan and its related artifacts once:

- the work described by the plan is merged to `main`;
- the spec is fully realized in the merged implementation;
- any roadmap or design notes tied to the same work slice are no longer active.

Do not archive a plan while its work is still in an open branch, draft PR, or unresolved review.

## What to archive

Move the complete work slice together:

- the plan from `.agents/plans/` to `.agents/plans/completed/`;
- the spec from `.agents/specs/` to `.agents/specs/completed/`;
- any related roadmap, design, or research file that was created for the same slice and lives under `.agents/`.

## How to archive

```bash
# 1. Move the plan and spec together
git mv .agents/plans/<plan-name>.md .agents/plans/completed/
git mv .agents/specs/<spec-name>.md .agents/specs/completed/

# 2. Update stale internal references
# Search the moved files for cross-references that still use the old
# .agents/plans/ or .agents/specs/ paths and rewrite them to include
# the completed/ segment (e.g., .agents/plans/phase-2.md -> .agents/plans/completed/phase-2.md).

grep -ER "\.agents/\(plans\|specs\)/[^/]+\.md" .agents/plans/completed/ .agents/specs/completed/ || true

# 3. Regenerate the mesh and marketplace surfaces
py -3 tools/run.py mesh --apply
py -3 tools/run.py marketplace --apply

# 4. Verify the tree passes CI before committing
py -3 tools/run.py ci --check

# 5. Commit and publish
git add -A
git commit -m "archive: complete <plan-name>"
```

## Mesh behavior

The `generating-agent-mesh` skill discovers `.agents/plans/completed/` and `.agents/specs/completed/` automatically and writes `INDEX.md` files for both. The parent `.agents/plans/INDEX.md` and `.agents/specs/INDEX.md` list only in-flight files and a single `completed/` directory link, so agents reviewing current plans/specs no longer load the full historical index.
