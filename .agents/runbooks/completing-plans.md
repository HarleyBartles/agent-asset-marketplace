# Completing plans and specs

Use this runbook when a plan and its associated spec(s) are delivered in the same PR as the implementation. Close out the artifacts in the completing PR so that when it merges the plan, spec, and related files move to the generated, indexed archive and `.agents/plans/` / `.agents/specs/` stay focused on in-flight work.

## When to archive

Archive a plan and its related artifacts as part of the same PR that completes the work, so that when the PR merges the artifacts it completes are closed out.

Archive once:

- the implementation is complete and the PR is ready for final review;
- the spec is fully realized in the implementation;
- any roadmap or design notes tied to the same work slice are no longer active;
- the plan is marked completed: every top-level checkbox (`- [ ]`) is checked (`- [x]`), OR the plan records the implementation PR.

Do not archive a plan before its implementation is ready for final review or while it has unresolved review findings.

> **Historical records:** Plans already in `.agents/plans/completed/` are historical snapshots. Do not re-litigate their checkboxes or update them to match the new completion rule. Going forward, only plans that are fully checked off or linked to a merged PR should be moved into `completed/`.

## What to archive

Move the complete work slice together. The set is deterministic:

1. **The plan file** — `<plan-name>.md` from `.agents/plans/` to `.agents/plans/completed/`.
2. **The spec file** — if the plan lists `**Spec:** <path>`, move that file from `.agents/specs/` to `.agents/specs/completed/`.
3. **Any explicitly referenced `.agents/` artifact** — roadmap, research, design, or spec files the plan names. Use the following command to list every `.agents/` path and bare `2026-...md` name the plan mentions, then move each one that still lives in the active tree:

   ```bash
   py -3 -c "import re, pathlib; plan=pathlib.Path('.agents/plans/<plan-name>.md'); text=plan.read_text(encoding='utf-8'); paths=sorted(set(re.findall(r'\.agents/(?:plans|specs|roadmaps|research)/\d{4}-\d{2}-\d{2}-[a-zA-Z0-9_\-]+\.md', text))); bare=sorted(set(re.findall(r'\b\d{4}-\d{2}-\d{2}-[a-zA-Z0-9_\-]+\.md\b', text))); print('Explicit .agents/ references:'); [print('  '+p) for p in paths] or print('  (none)'); print('Bare date-marked references:'); [print('  '+b) for b in bare] or print('  (none)')"
   ```

4. **Epic folders** — if the plan is the parent of an epic and there is a folder under `.agents/plans/<epic-name>/` containing multiple plans and a roadmap, move the entire folder into `.agents/plans/completed/<epic-name>/` so the archive keeps the same structure.

If a referenced file does not exist, note the missing file in the PR body rather than leaving it in the active tree.

## How to archive

```bash
# 1. Move the plan and spec together
git mv .agents/plans/<plan-name>.md .agents/plans/completed/
git mv .agents/specs/<spec-name>.md .agents/specs/completed/    # if there is one

# 2. Move any related .agents/ artifacts referenced by the plan
#    (roadmaps, research, design files, epic sub-folders)

# 3. Heal in-boundary archive links, then verify the remaining stale links
#    - heal_archive_links.py rewrites relative links inside completed/ files
#      to point at completed/ counterparts.
#    - check_archive_links.py reports any remaining active .agents/plans/ or
#      .agents/specs/ references in completed/ files, or active files that still
#      reference an old active path of a completed file.
py -3 tools/heal_archive_links.py --apply
py -3 tools/check_archive_links.py

# 4. Regenerate the mesh and marketplace surfaces
py -3 tools/run.py mesh --apply
py -3 tools/run.py marketplace --apply

# 5. Verify the tree passes CI before committing
py -3 tools/run.py ci --check

# 6. Commit the archive to the completing PR branch and publish
git add -A
git commit -m "archive: complete <plan-name>"
git push origin <pr-branch>
```

## Mesh behavior

The `generating-agent-mesh` skill discovers `.agents/plans/completed/` and `.agents/specs/completed/` automatically and writes `INDEX.md` files for both. The parent `.agents/plans/INDEX.md` and `.agents/specs/INDEX.md` list only in-flight files and a single `completed/` directory link, so agents reviewing current plans/specs no longer load the full historical index.
