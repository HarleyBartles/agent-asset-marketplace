---
name: release-engineering
description: Use when building, reviewing, or operating CI/CD pipelines, container images, releases, rollbacks, or deployment patterns.
metadata:
  source-id: release-engineering
  source-path: sources/first_party/skills/release-engineering/SKILL.md
  provenance-name: Release Engineering first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when building, reviewing, or operating CI/CD pipelines, container images, releases, rollbacks, or deployment patterns.
  use_when:
  - Use when designing or reviewing CI/CD pipelines.
  - Use when building, tagging, or promoting container images.
  - Use when planning blue/green, canary, or rolling deployments.
  - Use when preparing or rolling back a release.
  do_not_use_when:
  - Do not use when another more specific skill owns the task.
  related_skills:
  - observability
  - using-github
  - secure-development
license: MIT
---

# Release Engineering

## Overview

Treat releases as repeatable, observable pipelines: build once, promote artifacts through stages, and make rollback as easy as rollout.

## When to Use

- Designing or reviewing CI/CD pipelines.
- Building, tagging, or promoting container images.
- Planning blue/green, canary, or rolling deployments.
- Preparing or rolling back a release.

Do not use when another more specific skill owns the task.

## Core Pattern

1. Version everything: tag source, artifact, and deployment manifests with the same release identifier.
2. Build immutable artifacts in CI and promote them; avoid building per environment.
3. Use stages (dev, staging, production) with gates: automated tests, security scans, and approvals.
4. Prefer gradual rollouts (canary or blue/green) over all-at-once deploys; monitor health signals before increasing traffic.
5. Keep rollback one command away: retain the previous image or manifest and rehearse the rollback path.
6. Secure the supply chain: pin base images, sign artifacts, and audit runner permissions.

## Common Mistakes

- Building a new artifact per environment → build once and parameterize configuration.
- Skipping health checks between rollout stages → gate on metrics and smoke tests.
- Deploying without a rollback plan → keep the previous release ready and rehearse rollback.

Load `references/operational-guidance.md` for deeper coverage of Docker, Kubernetes, GitHub Actions, and SRE deployment patterns.
