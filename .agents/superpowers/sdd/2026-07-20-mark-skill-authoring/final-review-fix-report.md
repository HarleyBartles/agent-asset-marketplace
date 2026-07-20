# Final review fix report: MARK skill authoring

## Scope

Applied the final whole-branch review fixes to `mark-skill-authoring` without
changing registry entries, `agents/openai.yaml`, third-party custody, network
checks, or freshness policy.

## TDD evidence

The initial focused regression run failed in the expected review-gap areas:
first-party marketplace scaffolding created authority files; source maps were
not parsed or reconciled; citation records accepted non-synthesis modes; local
skill directory identity and marketplace `mark-*` collisions were not enforced;
the Bash wrapper only used `py -3`; CLI `--check` used a nested directory; and
the authored guidance still omitted the required lane and custody detail.

After minimal implementation changes, the focused regression suite passed:

```text
py -3 -m pytest tests/test_install_agent_skills.py tests/test_mark_skill_authoring_contract.py tests/test_validate_authority_assets.py -q
28 passed
```

## Delivered corrections

1. Marketplace `first_party` scaffolds now contain only `SKILL.md` and
   `references/.gitkeep`; only source-backed lanes receive authority assets.
2. `source-map.yaml` now has the compact projection schema
   (`schema_version`, `reconciled_against`, `references`). The validator parses
   it, validates its records, and requires reconciliation and references to
   match `authority.yaml`.
3. Citation-lane reference records must use `first_party_synthesis` in both
   authority records.
4. The installer rejects local `mark-*` directories whose frontmatter name
   differs from the directory, and preflights every installed plugin for a
   reserved `mark-*` namespace collision before normal or check-mode mutation.
5. The Bash scaffold wrapper prefers `python3`, then falls back to `py -3`.
6. CLI scaffold preview resolves the Git top-level while programmatic
   temporary non-Git `--check` calls remain supported.
7. Source-grounded and custody references now provide executable lane,
   decomposition, licensing, clean-room, citation, reconciliation, freshness,
   and no-inline-citation guidance.
8. The standards policy identifies `superpowers-plus:writing-skills` as the
   installed projection and `superpowers:writing-skills` as upstream origin.
9. The design handoff floor now matches the router at 9/10.

## Validation

```text
py -3 -m pytest tests/ -x
127 passed

py -3 tools/generate_index_mesh.py
Wrote index mesh: 158 files
```

Final clean-head verification also passed:

```text
py -3 -m pytest tests/test_install_agent_skills.py tests/test_mark_skill_authoring_contract.py tests/test_validate_authority_assets.py -q
28 passed

py -3 tools/check_marketplace.py
passed

git diff --check
passed
```

The first clean-head marketplace attempt found the report directory's generated
indexes stale because the report was added after the original mesh run. Running
the generator again added the required indexes, and the repeated clean-head
marketplace check passed.

## Concerns

None identified. The authority validator remains local and advisory-only; it
does not fetch remote sources or make freshness decisions.

## Follow-up hardening evidence (2026-07-20)

The six follow-up review findings were fixed in one TDD wave without network
access or third-party changes.

### TDD evidence

The added regressions initially failed in all six requested areas:

```text
py -3 -m pytest tests/test_install_agent_skills.py tests/test_mark_skill_authoring_contract.py tests/test_validate_authority_assets.py -q
6 failed, 29 passed
```

They covered missing authority manifests across both custody roots; strict
authority typing, safe reference paths, duplicate YAML keys, undecodable YAML,
and non-placeholder citation sections; matching-provenance installs with a
missing or stale marketplace skill; normalization-stable marketplace
first-party scaffolds; and rollback after a later scaffold write failure.

### Delivered hardening

1. Authority discovery now visits every existing `assets/authority` directory
   beneath marketplace and local skill roots, so missing `authority.yaml` is a
   reported error.
2. The local-only authority validator rejects duplicate YAML keys, unreadable
   YAML, malformed typed values, invalid SHA/date values, unsafe or missing
   operational references, incomplete decomposition records, and placeholder
   citation records.
3. A matching installer provenance record only short-circuits when every
   expected non-`mark-*` marketplace skill is present and byte-identical;
   local `mark-*` custody remains excluded and preserved.
4. Marketplace first-party scaffold frontmatter now has the canonical
   first-party normalization metadata and license. Source-backed lane and
   custody remain durable in authority assets.
5. Scaffold creation now exclusively creates its destination and removes only
   the directory created by that invocation if a later output write fails.
6. The execution plan records all verified implementation, regeneration,
   validation, coverage-review, and commit work as complete; publication is
   the sole remaining unchecked step.

### Follow-up validation

```text
py -3 -m pytest tests/test_install_agent_skills.py tests/test_mark_skill_authoring_contract.py tests/test_validate_authority_assets.py -q
35 passed

py -3 -m pytest tests/ -x
134 passed

py -3 tools/rebuild_marketplace.py
passed; local mark-skill-authoring preserved

py -3 tools/generate_index_mesh.py
Wrote index mesh: 158 files
```

`py -3 tools/check_marketplace.py` first completed component validation and
then correctly failed only on its final intentional dirty-worktree guard. It
was rerun after staging the completed wave, as was `git diff --check`, before
the commit.

### Follow-up concerns

None. Validation remains read-only and advisory-only; no freshness lookup or
network activity was added.
