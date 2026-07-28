# AGENTS.md

Scope: `tools/`

This scope covers repository validation and generation scripts.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

The canonical task runner is `tools/run`. It composes the individual
generator and validator scripts into a dependency-aware task graph.

- `./tools/run ci --check` (or `.\tools\run.ps1 ci --check` on Windows PowerShell) is the full non-mutating CI gate (lint, repo-standards, marketplace).
- `./tools/run marketplace --apply` (or `.\tools\run.ps1 marketplace --apply` on Windows PowerShell) is the canonical local full regeneration and validation entrypoint.
- `tools/run <target> --apply` / `tools/run.ps1 <target> --apply` regenerates only the named target and its prerequisites.
- `tools/run <target> --check` / `tools/run.ps1 <target> --check` validates only the named target and its prerequisites without writing.
- `tools/run --help` / `tools/run.ps1 --help` lists all targets and flags.
- `py -3 tools/run.py` or `python tools/run.py` works on any platform as a fallback.

Targets are: `inventory`, `heal`, `project`, `installed-skills`, `repo-index`, `mesh`, `catalog`, `validate`, `marketplace`, `lint`, `repo-standards`, `ci`, `all`.

The underlying scripts are implementation details:

- `generate_marketplace.py` regenerates `.agents/plugins/marketplace.json` and `codex-marketplace/manifest.json` from the local plugin bundle and source ledger, and `--check` compares both files without writing.
- `update_skill_artifacts.py` is the canonical generator orchestrator for full regeneration. Use `--all` to regenerate every installable skill artifact, or `--check` to validate without writing.
- `project_skills.py` stages overlays, materializes plugin skill trees under `codex-marketplace/plugins/<pack>/skills/`, and writes flat deterministic `generated/skill-zips/<skill>.zip` archives. `--check` validates projected trees and zip shape without writing.
- `validate_skill_zips.py` checks the canonical flat `skill.zip` surface and fails on stale, missing, or malformed artifacts.
- `validate_marketplace.py` checks the marketplace export, plugin manifest, bundle manifest, source ledger, repo index, local path references, projection materialization, and selected pack bundle-manifest freshness for the protected marketplace shape.
- `validate_repo_index.py` checks that the repo index stays aligned with the current marketplace and scoped guidance surfaces, but it is not the freshness proof for `repo-index/repo-index.json`.
- `generate_repo_index.py` regenerates `repo-index/repo-index.json` and `--check` compares the rendered file without writing.
- `generate_pack_manifests.py` regenerates the selected pack bundle-manifest surfaces and `--check` compares them without writing.
- `heal_overlays.py` adjusts `overlay.yaml` line-edit entries when source normalization shifts line numbers or whitespace. It runs in the `heal` target.
- `normalize_first_party_skill_sources.py` normalizes first-party `SKILL.md` and `agents/openai.yaml` content.
- `generate_first_party_skill_catalog.py` regenerates `provenance/first-party-skills.md`.
- `tools/ruff_diff.py` reports ruff findings only on added or modified lines when given `--changed-from <ref>`.
- `tools/run` uses `ruff_diff.py` for `lint --check` and runs `ruff check --fix` / `ruff format` for `lint --apply`.
- `python .agents/skills/repo-standards/scripts/repo_standards.py --check` checks repo shape; `python .agents/skills/repo-standards/scripts/repo_standards.py --apply --yes` applies missing surfaces.
- `python .agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --apply` refreshes skills in `.agents/skills` based on plugins with `INSTALLED_BY_DEFAULT` policy. In the main shared checkout, pass `--apply --allow-shared-checkout` to approve; linked worktrees do not need the flag.
- `python .agents/skills/generating-agent-mesh/scripts/generate_index_mesh.py --apply` regenerates repo-wide `INDEX.md` files; `--check` validates them.
- `python .agents/skills/generating-agent-mesh/scripts/validate_agent_mesh.py --check` validates mesh link reachability and doctrine.

Codex plugin first; generated GPT-safe skill zips second.

Current scope note: `generated/skill-zips/` is the flat GPT-ready export surface
for skill zips. It is a deterministic copy of the staged Codex projection.

Common worker commands:

```bash
# Full local regeneration and validation (Linux/macOS/WSL/Git Bash)
./tools/run marketplace --apply

# Full CI gate (read-only) (Linux/macOS/WSL/Git Bash)
./tools/run ci --check

# Regenerate only the mesh (Linux/macOS/WSL/Git Bash)
./tools/run mesh --apply
```

```powershell
# Full local regeneration and validation (Windows PowerShell)
.\tools\run.ps1 marketplace --apply

# Full CI gate (read-only) (Windows PowerShell)
.\tools\run.ps1 ci --check

# Regenerate only the mesh (Windows PowerShell)
.\tools\run.ps1 mesh --apply
```

Use `--check` to validate the current generated surface without rewriting it.
`--allow-shared-checkout` is approved once by `tools/run` and forwarded to child
scripts that require explicit approval to write in the main shared checkout
(`generate_index_mesh.py`, `refresh_installed_skills.py`, `repo_standards.py`).
It is not needed in a linked worktree. `--allow-shared-checkout` alone is
rejected by those scripts.

`py -3 tools/generate_pack_manifests.py --check` also verifies any
manifest-declared generated inventory blocks in pack `README.md`, `SOURCE.md`
and `PROJECTION.md` surfaces.

## Routing pointers

- `../.agents/docs/mesh-policy.md` before changing generator or validator behavior
- `../.agents/guides/planning-guide.md` before planning tool changes
- `../.agents/guides/implementing-guide.md` before implementing tool changes
- `../.agents/guides/marketplace-generation-guide.md` before changing marketplace regeneration behavior
- `../.agents/guides/code-review-guide.md` before reviewing tooling changes

Policy for agent work:

- Any change to source custody, adapter files, projection plugin shapes, bundle manifests,
  source maps, provenance maps, or generated zips requires a full market regeneration
  followed by validation before a PR may be called green.
- The canonical completion path is the full regeneration stack, not a partial refresh.
- Partial regeneration paths are fallback-only repair tools and should not be
  advertised as a normal completion route.
- The expected local green-path proof is `tools/run marketplace --apply`.
- The expected CI green-path proof is `tools/run ci --check`.
- Both commands must be aligned so check mode fails if regeneration would be
  needed and write mode still performs the actual regeneration locally.
- If a worker cannot run the full stack, it must say so explicitly instead of
  assuming CI will catch the missing regeneration.

Deterministic pack rule: if a skillset pack or projection lane lacks a
manifest-driven generator/validator path, add one to `tools/` and wire it into
the standard update/check entrypoints. Do not paper over missing pipeline
support with a pack-specific one-off script or a hand-edited output surface.
The editable source custody for marketplace generation is the trio of source
trees, adapters/overlays, and `codex-marketplace/custody-pack-registry.json`.
Treat generated manifests, projection trees, source maps, provenance maps, and
zip artifacts as derived outputs only. If a convention can be expressed in the
registry and generator, do that instead of hand-rolling per-pack output
conventions in the generated surfaces.

## Line-ending policy for generated files

This repo normalizes to LF. `core.autocrlf` is `false` so git does not
translate line endings. Generators and agents that write text files must
write LF explicitly, not the platform default (CRLF on Windows).

When writing text files, prefer `open("w")` with `newline="\n"`:
```python
with path.open("w", encoding="utf-8", newline="\n") as f:
    f.write(content)
```

Do not pass `newline=` to `Path.read_text()` in scripts that must run under
Python 3.12; the `newline` keyword for `Path.read_text()` was added in Python
3.13. For consistent LF-only reads and writes across `Path.read_text()` and
`Path.write_text()`, prefer `Path.open(..., newline="\n")` or the built-in
`open(..., newline="\n")` (or `newline=""` if the text already contains explicit
`\n` and you want no translation) instead.

Without the explicit `newline` parameter, Python translates `\n` to
`os.linesep` (CRLF on Windows), which `git diff --check` flags as trailing
whitespace and which churns every generated file on every rebuild.

Do not add CRLF detection or preservation logic to generators. Always
write LF.

## Review guidelines

- Flag validators that can pass while indexed paths, plugin manifests, or
  registry entries have already drifted.
- Flag generator changes that are not paired with matching validation updates.
- Flag JSON or path parsing that could silently skip missing files, stale
  references, or unsupported plugin entries.
- Flag tooling changes that do not keep the marketplace export, repo index,
  and validation command documentation aligned.
- Flag targeted skill-update helpers that rewrite unrelated generated state or
  that hide full-regeneration behavior behind an ordinary update path.
- Flag flat skill.zip artifacts that do not match the staged Codex projection
  or that contain stale adapter, gpt, or per-pack zip references.

## Maintenance responsibility

This file must stay aligned with the repo's validation and generation tooling.
When tooling paths change, new validation scripts are added, or worker-facing
commands evolve, review and update this file to reflect current expectations.
The skill-update path, marketplace inventory source, and drift validation
references must stay accurate—when those change, this file should be updated
to prevent drift.
