## This repository's policy

This repository declares no repo-local skills and no marketplace skill subscriptions. Agents use the ambient plugins available in their runtime; plugin availability does not install skill copies into this checkout. `.agents/skills/` should be absent.

The generated `.agents/plugins/marketplace.json` remains the source for catalog availability, while `src/plugin-definitions/marketplace-policy.json` owns this repository's local installation defaults. Keep both `repo.local_skills` and `install_defaults` empty.

## Marketplace source and product output

Canonical skill source lives under `skills/<skill-id>/`; plugin membership is declared in `src/plugin-definitions/<plugin>/contents.json`. Generated, self-contained plugin packages live under `dist/plugins/`. Edit canonical source and definitions, then rebuild through `tools/run.py marketplace --apply`.

Do not edit generated plugin packages or create local copies under `.agents/skills/` as a substitute for ambient capabilities.

## Projection invariant

The repository-owned `refresh-skills` check verifies the declared installation policy and removes stale projections when explicitly applied. With no subscribed plugins and no local skills, apply leaves `.agents/skills/` absent; check mode reports stale projection or provenance without writing.
