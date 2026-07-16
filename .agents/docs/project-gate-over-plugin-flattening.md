# Project Gate Over Plugin Flattening

## Composition doctrine

- Project packs contain project-specific gate or orchestration skills.
- Domain plugins should stay separately installed when a repo needs a chunk of
  them.
- A project gate skill composes and constrains skills from separately installed
  domain plugins.
- Do not flatten whole domain plugins into project packs.
- If a project only needs one or two narrow adjuncts from a broad plugin, keep
  them narrow and explicit with provenance and rationale.

## Repo guidance

- This repo is a small golden exemplar of the base pattern only.
- Do not use this PR to implement the Wild Bunch decomposition.
