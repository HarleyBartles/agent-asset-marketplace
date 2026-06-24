# AGENTS.md

Scope: `tools/`

This scope covers repository validation and generation scripts.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

The skill-update path is now worker-facing through
`py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>`. The root
inventory that drives marketplace plugin ownership is
`codex-marketplace/plugin-roots.json`, GPT overlay sources live under
`adapters/gpt/`, and drift validation lives in
`tools/validate_generated_drift.py`.
The marketplace freshness proof is `py -3 tools/generate_marketplace.py --check`
for `.agents/plugins/marketplace.json` and
`codex-marketplace/manifest.json`, plus `py -3 tools/generate_repo_index.py
--check` for `repo-index/repo-index.json`. Projection-lane freshness is
proven by `py -3 tools/materialize_projection.py --check`, and the selected ECC
bundle-manifest surfaces are proven by `py -3 tools/generate_ecc_pack_manifests.py
--check`. `validate_repo_index.py` checks metadata alignment, not freshness by
itself.

Deterministic pack rule: if a skillset pack or projection lane lacks a
manifest-driven generator/validator path, add one to `tools/` and wire it into
the standard update/check entrypoints. Do not paper over missing pipeline
support with a pack-specific one-off script or a hand-edited output surface.

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
- Flag GPT export manifests that allow raw Codex-specific assumptions to leak
  into generated skill zips instead of using an overlay or exclusion.

## Maintenance responsibility

This file must stay aligned with the repo's validation and generation tooling.
When tooling paths change, new validation scripts are added, or worker-facing
commands evolve, review and update this file to reflect current expectations.
The skill-update path, marketplace inventory source, and drift validation
references must stay accurate—when those change, this file should be updated to
prevent drift.
