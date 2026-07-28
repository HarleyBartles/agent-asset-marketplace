# AGENTS.md

Scope: `tools/`

This scope covers repository validation and generation scripts.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

The skill-update path is now worker-facing through
`py -3 tools/update_skill_artifacts.py --all` for a full regeneration. The
`--skill` and `--pack` flags remain as backwards-compatible aliases that also
run the full pipeline. The root inventory that drives marketplace plugin
ownership is `codex-marketplace/plugin-roots.json`.
The marketplace freshness proof is `py -3 tools/generate_marketplace.py --check`
for `.agents/plugins/marketplace.json` and
`codex-marketplace/manifest.json`, plus `py -3 tools/generate_repo_index.py
--check` for `repo-index/repo-index.json`. Projection-lane and flat skill-zip
freshness are proven by `py -3 tools/project_skills.py --check`, and the selected
pack bundle-manifest surfaces are proven by `py -3 tools/generate_pack_manifests.py
--check`. `validate_repo_index.py` checks metadata alignment, not freshness by
itself. The repo-wide `INDEX.md` mesh is proven by `py -3 sources/first_party/skills/generating-agent-mesh/scripts/generate_index_mesh.py
--check`, and mesh law lives in `../.agents/docs/mesh-policy.md`.
Agent skills installation is handled by `py -3 sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --apply`,
which deterministically installs/refreshes skills in `.agents/skills` based on
plugins with `INSTALLED_BY_DEFAULT` policy in `.agents/plugins/marketplace.json`.
In the main shared checkout, pass `--apply --allow-shared-checkout` to
approve the operation; linked worktrees do not need the flag.
`--allow-shared-checkout` alone is rejected.
`py -3 tools/generate_pack_manifests.py --check` also verifies any
manifest-declared generated inventory blocks in pack `README.md`, `SOURCE.md`,
and `PROJECTION.md` surfaces.
The canonical full rebuild and validation entrypoint is
`py -3 tools/rebuild_marketplace.py --apply` (also accepts `--allow-shared-checkout`).
Use `py -3 tools/rebuild_marketplace.py --check` for a non-mutating check,
or `bash scripts/ci-preflight.sh --check` as the CI convenience wrapper.
The preflight and CI lint changed Python files with `py -3 tools/ruff_diff.py
--changed-from origin/main`, which reports only ruff findings on added or
modified lines.
Use `--phase <inventory|heal|project|index|catalog|validate|all>` to run a
single logical phase; `--skip-install`, `--skip-index`, `--skip-validate`,
and `--skip-whitespace-check` omit steps from a full run.
Partial validation is available with `py -3 tools/validate_marketplace.py --phase <inventory|project|index>`.
`py -3 tools/validate_authority_assets.py` is a non-mutating authority-shape
check. It does not perform freshness networking and does not fail because a
remote source has changed; it only validates recorded local evidence.
Overlay self-healing is handled by `py -3 tools/heal_overlays.py`, which
adjusts `overlay.yaml` line-edit entries when source normalization (CRLF→LF,
trailing whitespace stripping) shifts line numbers or whitespace. It runs
automatically in write mode during `rebuild_marketplace.py --apply` and in check mode
during `scripts/ci-preflight.sh --check`. If `heal_overlays.py --check` fails, run
`py -3 tools/rebuild_marketplace.py --apply` to auto-heal stale overlays.

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
- The expected local green-path proof is `py -3 tools/rebuild_marketplace.py --apply`.
- The expected CI green-path proof is `bash scripts/ci-preflight.sh --check`.
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
references must stay accurate—when those change, this file should be updated to
prevent drift.
