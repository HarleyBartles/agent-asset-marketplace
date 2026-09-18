# Build Agent Operating Model Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan sequentially. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the `agent-operating-model` plugin, move `repo-standards` and `python` into it, and expose focused skills for shape, composition, command bus, validation, hooks, and agent assets.

**Architecture:** `repo-standards` becomes a thin router. `repo-shape` owns the existing check/apply coordinator and compatibility scripts; the remaining skills own focused guidance and assets. Existing public repo-standards script entrypoints remain as forwarding wrappers so consumer repositories do not break during adoption.

**Tech Stack:** Codex plugins, Markdown skills, Python 3, JSON manifests, PowerShell/shell compatibility wrappers, pytest.

**Spec:** `.agents/specs/2026-09-18-agent-operating-model-design.md`

**Execution Strategy:** `executing-plans` — custody moves, manifest regeneration, and compatibility proof are sequential.

## Constraints

- Canonical plugin source lives under `codex-marketplace/plugins/agent-operating-model/`.
- `repo-worker-pack` retains worker hygiene, custody, risk, and publication skills.
- `language-patterns-pack` retains `python-frameworks` and `typescript`; `python` moves once.
- `repo-standards` remains the public routing skill name.
- Existing `.agents/skills/repo-standards/scripts/*` command paths remain callable through wrappers.
- First-party installed projections remain byte-identical to their canonical source owner.
- The repository subscribes to `agent-operating-model` by default and stops receiving `repo-standards` from `repo-worker-pack`.
- Do not migrate consumer repositories in this plan.

### Task 1: Create and register the plugin

- [ ] Run `py -3 tools/new_plugin.py agent-operating-model --check`, then `--apply`.
- [ ] Enable the new root in `codex-marketplace/plugin-roots.json` and add `agent-operating-model` to `install_defaults` in `codex-marketplace/repo-local-marketplace-policy.json`.
- [ ] Replace scaffold metadata with the approved display name, purpose, first-party source notes, and focused plugin description.

### Task 2: Move canonical skills and establish focused owners

- [ ] Move `repo-standards` from `repo-worker-pack` into `agent-operating-model` and replace its body with the thin capability router.
- [ ] Move `python` from `language-patterns-pack` into `agent-operating-model`; update its `metadata.source-path`.
- [ ] Create `repo-shape`, `repo-composition`, `command-bus`, `repository-validation`, `tracked-repo-hooks`, and `repo-agent-assets` skills with concrete trigger descriptions and ownership boundaries from the spec.
- [ ] Move the existing repo-standards implementation tree into `repo-shape`; place composition references/templates/scaffolds under `repo-composition`, validation guidance under `repository-validation`, hook assets under `tracked-repo-hooks`, and marketplace/profile assets under `repo-agent-assets` where doing so does not break the coordinator.
- [ ] Keep narrow forwarding wrappers under `repo-standards/scripts/` for existing consumer entrypoints; wrappers delegate to the owning skill and contain no policy.

### Task 3: Rewire coordinator, manifests, and tests

- [ ] Update cross-skill paths used by the shape manifest and coordinator.
- [ ] Update tests to import the canonical owning modules while adding compatibility tests for legacy `repo-standards/scripts/*` paths.
- [ ] Add focused tests proving the router names every owner, the new plugin owns each moved skill exactly once, and old packs no longer declare `repo-standards` or `python`.
- [ ] Run focused tests for plugin inventory, repo standards, installed-skill projection, command dispatch, hooks, and composition.

### Task 4: Regenerate and publish

- [ ] Run `py -3 tools/new_plugin.py --sync` for the three affected packs.
- [ ] Run `py -3 tools/run.py marketplace --apply`, `installed-skills --apply`, `repo-index --apply`, and `mesh --apply`.
- [ ] Verify no duplicate canonical skill custody, no orphan installed skill, and no stale link to the old owners.
- [ ] Commit through the tracked hook, push the branch, update PR #322 to describe implementation as well as design, and verify the exact remote head and hosted check.
