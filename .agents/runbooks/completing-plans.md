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
# Move the plan and spec together
git mv .agents/plans/<plan-name>.md .agents/plans/completed/
git mv .agents/specs/<spec-name>.md .agents/specs/completed/

# Regenerate the mesh so the new completed/ INDEX.md files are current
py -3 .agents/skills/generating-agent-mesh/scripts/generate_index_mesh.py --apply

# Verify the tree passes CI before committing
py -3 tools/run.py ci --check

# Commit and publish
git add -A
git commit -m "archive: complete <plan-name>"
```

## Mesh behavior

The `generating-agent-mesh` skill discovers `.agents/plans/completed/` and `.agents/specs/completed/` automatically and writes `INDEX.md` files for both. The parent `.agents/plans/INDEX.md` and `.agents/specs/INDEX.md` list only in-flight files and a single `completed/` directory link, so agents reviewing current plans/specs no longer load the full historical index.
