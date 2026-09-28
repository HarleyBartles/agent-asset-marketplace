# Source

The `repo-worker-pack` plugin is built from first-party maintained skills in the [agent asset marketplace](https://github.com/HarleyBartles/agent-asset-marketplace). Its composition is declared in `plugin-definitions/repo-worker-pack/contents.json` in that source repository. Canonical skill source lives under the repository's top-level `skills/` tree.

The plugin carries complete copies of its selected skills, including their ship-ready tests. The generated bundle manifest records each skill's source ID and provenance. The installed plugin does not depend on the source repository being present.

The plugin shell and first-party skills are MIT-licensed. Where a skill incorporates upstream material, its per-skill provenance and notices retain the applicable attribution and license terms.
