# Notice

`generating-images` is a substantially modified derivative of the installed
OpenAI bundled `imagegen` Agent Skill instructions. The upstream source was
retrieved on 2026-09-15 from the installed bundled OpenAI `imagegen` skill. A
byte-identical source snapshot is retained under
`assets/authority/reference-source/openai-imagegen/SKILL.md`.

Upstream source snapshot:

- File SHA-256: `706D4D96E1D5C9E6023FE3CCABBA1BB34B364024D344FD25B8515EC7D28FE3C4`
- Source file length: 19,516 bytes
- Source licence: Apache License 2.0; the complete licence text is retained in
  [`LICENSE.txt`](LICENSE.txt).

This repository does not claim the upstream instructions as wholly original. The
derivative retains and reorganises useful concepts concerning image-generation
versus editing, explicit input-image roles, prompt structuring, invariant
preservation, inspection, targeted iteration, transparency, and asset handoff.

The substantial modifications for this repository are:

- capability- and behaviour-based routing instead of a fixed execution tool;
- removal of Codex tool names, `$CODEX_HOME`, built-in save paths, and
  OpenAI-only environment assumptions from the portable core;
- removal of the bundled OpenAI CLI and its scripts, dependencies, model details,
  and network instructions;
- separation of unresolved creative direction into `directing-visual-stories`;
- a provider-neutral contract for truthful missing-capability and incomplete-brief
  outcomes;
- explicit preservation of frame and story invariants;
- repository-neutral provenance, custody, and field-learning reporting.

Provider- or harness-specific adapters, if added later, must retain their own
source attribution and must not be treated as part of this portable core.
