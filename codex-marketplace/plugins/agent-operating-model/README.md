# Agent Operating Model

This bundle projects the first-party agent-operating-model skills.

## Bundle contents

### Documentation
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`

## Boundary
- The bundle defines how a repository is shaped and operated: composition,
  command buses, validation, tracked hooks, agent assets, and Python guidance.
- `repo-standards` is the thin router across those focused capabilities;
  `repo-shape` owns their coordinated repository surface.
- Worker custody, worktrees, risk, and publication remain in `repo-worker-pack`.

## Install shape

Skills are installed from the Codex plugin roots under `codex-marketplace/plugins/<pack>/skills/<skill>/`.
