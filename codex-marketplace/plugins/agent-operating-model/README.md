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
The operating model is an ordinary plugin: subscribing to it supplies its
bundled skills. Consumer repos do not maintain a second list of operating-model
skills to install. The conformance contract checks required plugin subscriptions,
mandatory repository surfaces, and dead workflow skill links; it does not compare
consumer documents byte-for-byte with these starter templates.
