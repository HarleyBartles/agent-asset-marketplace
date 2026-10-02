## This repository's policy

This repository declares no repo-local skills and no marketplace skill subscriptions. Agents use the ambient plugins available in their runtime; plugin availability does not install skill copies into this checkout. `.agents/skills/` should be absent.

The generated `.agents/plugins/marketplace.json` remains the source for catalog availability, while `src/plugin-definitions/marketplace-policy.json` owns this repository's local plugin installation defaults. Keep `install_defaults` empty. Repository-authored skills belong under `.agents/skills/` without a separate inventory.

## Marketplace source and product output

Canonical skill source lives under `skills/<skill-id>/`; plugin membership is declared in `src/plugin-definitions/<plugin>/contents.json`. Generated, self-contained plugin packages live under `dist/plugins/`. Edit canonical source and definitions, then rebuild through `tools/run.py marketplace --apply`.

Do not edit generated plugin packages or create local copies under `.agents/skills/` as a substitute for ambient capabilities.

## Repo-local skills

This repository authors canonical skills under `skills/` and packages them through plugin definitions. It has no repo-local skills and no `.agents/skills/` projections. Consumers that need plugins should declare them in native repo configuration; the Marketplace projection updater is retired.
