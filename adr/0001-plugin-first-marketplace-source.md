# ADR 0001: Plugin-first marketplace source

**Status:** Accepted

## Context

Historical marketplace-normalization plans established a recurring source versus
projection boundary. The repository now publishes agent assets from canonical
plugin trees while consuming installed copies locally.

## Decision

Canonical marketplace assets live under `codex-marketplace/plugins/`. Bundle
manifests declare shipped skills, while `.agents/skills/` is a generated local
consumer surface. Edit canonical source first and regenerate projections.

## Consequences

Reviews and validation must distinguish canonical source from generated output.
An installed copy is never an authority for a source edit.

## Current authority

Root `AGENTS.md` and `.agents/doctrine/custody-and-marketplace-doctrine.md`.
