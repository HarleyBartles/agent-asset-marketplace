# repo-standards cross-repo application programme

> **For agentic workers:** This is a programme of consecutive, self-contained implementation plans. Each plan delivers a working increment and may be executed independently, but the intended order is fixed because later plans depend on surfaces delivered by earlier ones.

**Goal:** Roll out a hardened `repo-standards` skill and a renamed `generating-agent-mesh` skill to the `agent-asset-marketplace` source repo and then to the sister repos.

## Plan sequence

1. **[2026-07-25-01-generating-agent-mesh.md](2026-07-25-01-generating-agent-mesh.md)** — Rename `generating-index-mesh` to `generating-agent-mesh` and ship a generic `validate-agent-mesh` command with repo extension hook.
2. **2026-07-25-02-repo-standards-alignment.md** — Harden `repo-standards` for cross-repo alignment: router `AGENTS.md`, canonical guides, canonical `marketplace.json`, scaffold-based pre-commit, `ci-preflight` extension points and `--changed-from` support.
3. **2026-07-25-03-rollout-adventures-of-patch.md** — Apply the updated skills to `adventures-of-patch`.
4. **2026-07-25-04-rollout-portfolio.md** — Apply the updated skills to `portfolio`.
5. **2026-07-25-05-rollout-wild-bunch.md** — Apply the updated skills to `wild-bunch`.
6. **2026-07-25-06-rollout-rooms-mostly.md** — Apply the updated skills to `rooms-mostly`.

## Global constraints (apply to every plan in the programme)

- Work in the isolated worktree at `Z:\_agent-worktrees\agent-asset-marketplace\repo-standards-design` unless the plan explicitly moves to a sister repo.
- All text files must be written with LF line endings (`newline="\n"`).
- Any source-custody or skill change requires `py -3 tools/rebuild_marketplace.py` and `py -3 tools/check_marketplace.py` before the plan may be called green.
- Projection surfaces (plugin roots, bundle manifests, source maps, installed skills) are generated, not hand-edited.
- Each plan ends with a green validation run and a commit.
