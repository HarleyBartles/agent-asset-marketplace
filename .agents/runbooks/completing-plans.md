# Completing plans and specs

Use this runbook when a plan and its associated spec(s) are delivered and the work is fully merged. It keeps `.agents/plans/` and `.agents/specs/` focused on in-flight work while preserving the historical record in a generated, indexed archive.

## When to archive

Archive a plan and its related artifacts once:

- the work described by the plan is merged to `main`;
- the spec is fully realized in the merged implementation;
- any roadmap or design notes tied to the same work slice are no longer active;
- the plan is marked completed: every top-level checkbox (`- [ ]`) is checked (`- [x]`), OR the plan records a merged implementation PR.

Do not archive a plan while its work is still in an open branch, draft PR, or unresolved review.

> **Historical records:** Plans already in `.agents/plans/completed/` are historical snapshots. Do not re-litigate their checkboxes or update them to match the new completion rule. Going forward, only plans that are fully checked off or linked to a merged PR should be moved into `completed/`.

## What to archive

Move the complete work slice together. The set is deterministic:

1. **The plan file** — `<plan-name>.md` from `.agents/plans/` to `.agents/plans/completed/`.
2. **The spec file** — if the plan lists `**Spec:** <path>`, move that file from `.agents/specs/` to `.agents/specs/completed/`.
3. **Any explicitly referenced `.agents/` artifact** — roadmap, research, or design files named in the plan body under `**Roadmap:**`, `**Research:**`, `**Design:**`, or a `Related` section. Move each to `.agents/plans/completed/` if it is a plan or roadmap, or to `.agents/specs/completed/` if it is a spec.
4. **Epic folders** — if the plan is the parent of an epic and there is a folder under `.agents/plans/<epic-name>/` containing multiple plans and a roadmap, move the entire folder into `.agents/plans/completed/<epic-name>/` so the archive keeps the same structure.

If a referenced file does not exist, note the missing file in the PR body rather than leaving it in the active tree.

## How to archive

```bash
# 1. Move the plan and spec together
git mv .agents/plans/<plan-name>.md .agents/plans/completed/
git mv .agents/specs/<spec-name>.md .agents/specs/completed/    # if there is one

# 2. Move any related .agents/ artifacts referenced by the plan
#    (roadmaps, research, design files, epic sub-folders)

# 3. Update stale internal references
#    The following one-liner prints files that still reference active-plan or
#    active-spec paths. Fix any output before committing.

py -3 -c "import re, pathlib; pats=[r'\.agents/plans/[^/]+\.md', r'\.agents/specs/[^/]+\.md']; stale=[]; check=lambda f: any(re.search(p, f.read_text(encoding='utf-8')) for p in pats); [stale.append(str(f.relative_to('.'))) for d in ['.agents/plans/completed/', '.agents/specs/completed/'] for f in pathlib.Path(d).rglob('*.md') if check(f)]; (print('No stale references.') if not stale else [print(s) for s in stale])"

# 4. Regenerate the mesh and marketplace surfaces
py -3 tools/run.py mesh --apply
py -3 tools/run.py marketplace --apply

# 5. Verify the tree passes CI before committing
py -3 tools/run.py ci --check

# 6. Commit and publish
git add -A
git commit -m "archive: complete <plan-name>"
```

## Mesh behavior

The `generating-agent-mesh` skill discovers `.agents/plans/completed/` and `.agents/specs/completed/` automatically and writes `INDEX.md` files for both. The parent `.agents/plans/INDEX.md` and `.agents/specs/INDEX.md` list only in-flight files and a single `completed/` directory link, so agents reviewing current plans/specs no longer load the full historical index.
