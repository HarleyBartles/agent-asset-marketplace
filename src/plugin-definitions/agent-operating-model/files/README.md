# Agent Operating Model

This ambient bundle makes first-party repository operating capabilities available to agents. It also carries a catalog of individually deployable standards.

## Bundle contents

### Documentation

- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`

## Boundary

- Plugin availability provides capabilities and a menu of deployable standards. It does not require a consumer to implement the whole operating model.
- Each consumer explicitly chooses standards from the catalog, keeps its own standards separately, and runs only the checks and scaffolds it declared.
- `repo-standards` helps agents compose focused capabilities. It does not make every `repo-shape` surface mandatory by default.
- Worker custody, worktrees, risk, and publication remain in the ambient `repo-worker-pack`.

## Install shape

Skills are installed from the Codex plugin roots under `dist/plugins/<pack>/skills/<skill>/`. The operating model is an ordinary ambient plugin: subscribing makes its agent capabilities available. Consumer repositories do not need to install copies of these skills to adopt a standard. Deploy only the selected standard resources and pin the consumer-controlled checker inputs used by local and hosted validation.
