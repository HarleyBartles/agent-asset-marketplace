# Awesome Codex Plugins Vendor Bundle Custody

## Source

- Upstream repo: <https://github.com/hashgraph-online/awesome-codex-plugins.git>
- Pinned commit: `b4dd3ac78e50c9cdfd3dbb3fea4ec3a75d8e2daa`
- Upstream license: `Apache-2.0`

## Purpose

This note documents the vendor-bundle custody slice for MARK-41. It mirrors only
the selected MARK-39 bundle candidates as third-party source/provenance.

## Mirrored bundles

- `bundles/archcore-ai/plugin`
- `bundles/epicsagas/epic-harness`
- `bundles/hashgraph-online/hol-guard-plugin`
- `bundles/hashgraph-online/registry-broker-codex-plugin`
- `bundles/Kanevry/session-orchestrator`
- `bundles/sendbird/cc-plugin-codex`

## Rights posture

The mirrored bundles were selected because their `.codex-plugin/plugin.json`
metadata advertises permissive licenses:

- `Apache-2.0` for Archcore, Claude Code for Codex, Epic Harness, HOL Guard
  Plugin, and Registry Broker
- `MIT` for Session Orchestrator

The mirrored trees preserve upstream source paths, bundled licenses, and bundle
local notices or security documents where present.

## Boundary

This is custody only. It does not activate these bundles in marketplace
configuration and does not relabel upstream content as Harley-owned source.
