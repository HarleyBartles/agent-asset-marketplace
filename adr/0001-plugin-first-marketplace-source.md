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

## Historical origin context

Completed plans including `2026-06-18-mark-233-implement-marketplace-source-custody-and-plugin-projection-normalization.md` and `2026-06-19-mark-260-make-plugin-onboarding-generation-metadata-driven.md`.
