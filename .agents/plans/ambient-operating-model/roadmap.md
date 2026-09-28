# Ambient Operating Model and Selectable Standards Roadmap

## Goal

Make the five intended ambient plugins available as distinct agent capabilities while letting every repository choose its own standards composition, including no Agent Operating Model standards. Ship deployment and validation resources that consumers can run in hosted CI without ambient plugins.

## Plan sequence

| #   | Title                                                  | Status  | Plan File                                          | Commit | PR  | Rating | Notes                                                                                                                                                                                                                                            |
| --- | ------------------------------------------------------ | ------- | -------------------------------------------------- | ------ | --- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Retire the generated index mesh                        | pending | `2026-09-28-retire-generated-index-mesh.md`        | -      | -   | -      | Retire both Markdown mesh files and generated JSON index sidecars, remove all `INDEX.md`/`INDEX.json` files and their runner/consumer requirements, and preserve distinct marketplace manifests.                                                 |
| 2   | Selectable standards and consumer runner bridge        | blocked | `2026-09-28-selectable-standards-runner-bridge.md` | -      | -   | -      | Replan after Plan 1: the current draft deploys a mesh bridge, but index-mesh retirement makes preserving mesh behavior obsolete. Keep the refresh runner compatibility requirement and remove mesh generation from the consumer runner contract. |
| 3   | Ambient pack boundaries and capability-based workflows | pending | -                                                  | -      | -   | -      | Audit and correct Superpowers+, Repo Worker Pack, MCP Usage Pack, and Unslop+; make runbook/playbook composition capability-based. Treat index-mesh retirement as settled scope.                                                                 |
| 4   | Consumer migration and marketplace release             | pending | -                                                  | -      | -   | -      | Publish migration guidance and release proof; consumer-specific migrations remain separate work in each consumer repository.                                                                                                                     |

## Handoff notes

- The approved design is [Ambient Operating Model and Selectable Standards Design](../../specs/2026-09-28-ambient-operating-model-and-selectable-standards-design.md).
- Rooms-Mostly was inspected read-only on `main`. Its `tools/run.py` invokes installed `refreshing-installed-skills` and `generating-agent-mesh` scripts; its tracked hook invokes the declared `tools/run.py ci` apply/check commands. This roadmap does not authorize editing Rooms.
- Keep Superpowers+ as workflow composition, Repo Worker Pack as ambient general-purpose agent capabilities, and Agent Operating Model as the catalog of deployable standards and implementation resources.
- New roadmap scope from the human: remove the index mesh because its value does not justify the generated file burden. The retirement plan must inventory source, plugin membership, generated `INDEX.md`/`INDEX.json` files, tests, documentation, command-bus/CI references, and consumer migration effects before deletion. Do not preserve any generated index files as compatibility copies.
- Write each later plan just in time from current repository and consumer evidence. Do not prewrite all roadmap plans.
