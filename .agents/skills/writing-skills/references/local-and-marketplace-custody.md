# Local and marketplace custody

Use `--custody local` for any valid exact skill name. It creates tracked repository-local skill custody under `.agents/skills/`; add that exact name to `repo.local_skills` in `.agents/plugins/marketplace.json` to establish custody. Prefixes are optional naming choices, not custody mechanisms. Local skills are always `first_party` and have no authority directory.

Use `--custody marketplace` for canonical first-party source under `skills/<name>/`. Skill source does not belong to a plugin. Declare product membership separately in `src/plugin-definitions/<plugin>/contents.json`; the build copies the skill and any declared shared resource into each selected plugin. `first_party` means this repository maintains the authored skill, including an adapted work; record upstream attribution, source URL or revision, and license obligations in the skill's provenance and shipped notices. `skills-with-source`, `skills-with-mixed-source`, and `skills-with-citation` add authority records needed by source-backed workflows. Follow `source-grounded-authoring.md` for decomposition, legal approval, citations, reconciliation, and manual freshness review.

Do not create plugin definitions, marketplace manifests, `agents/openai.yaml`, third-party source categories, or generated indexes from this scaffolder. Skill source and plugin composition are separate actions.
