# Agent Operating Model

This plugin makes first-party repository operating capabilities available to agents and publishes selectable standard definitions.

## Bundle contents

### Documentation

- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`

## Boundary

- Plugin availability provides capabilities and a menu of standards. It does not adopt any standard for a consumer.
- Each consumer chooses the standards it wants, implements them in its own repository, and self-certifies against the requirements it pins.
- A standard skill carries its current definition, adoption and assessment guidance, and any optional starter assets. It may supply no deployable asset.
- Repositories may take, adapt, replace, or omit optional starters. Adopted files and tools become repository-owned; matching AOM starter bytes is not a compliance requirement.
- `repo-standards` helps agents select and assess focused capabilities. It does not make every repository capability mandatory by default.
- The selectable standards catalog includes independent `gitflow` and `semver` choices. Gitflow supplies branch routes; SemVer supplies compatibility and one-source version identity. Only adopting both adds merge-triggered `dev.N` and release-candidate cadence.
- Worker custody, worktrees, risk, and publication remain in the ambient `repo-worker-pack`.

## Install shape

Skills are installed from the Codex plugin roots under `dist/plugins/agent-operating-model/skills/<skill>/`. The plugin makes authoring capabilities available. A repository adopting a standard records its immutable source commit and definition path separately from plugin refresh, maintains a readable certification, and routes agents to those records. Root `AGENTS.md` is created or updated for every AOM adoption. The repository owns implementation and compliance.
