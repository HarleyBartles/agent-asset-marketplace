---
name: observability
description: Use when building or reviewing OpenTelemetry instrumentation, trace/metric/log pipeline design, or observability architecture. Do not use when the work is vendor-specific backend configuration, incident response runbooks, or testing strategies owned by another skill.
metadata:
  source-id: observability
  source-path: codex-marketplace/plugins/engineering-pack/skills/observability/SKILL.md
  provenance-name: Observability first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Guidance for designing and reviewing OpenTelemetry-based observability.
  use_when:
    - Use when building or reviewing OpenTelemetry instrumentation.
    - Use when designing trace, metric, and log pipelines.
    - Use when deciding sampling, context propagation, and resource attributes.
  do_not_use_when:
    - Do not use when configuring a specific vendor backend or dashboard.
    - Do not use when authoring incident response runbooks.
    - Do not use when the task is performance or load testing.
  related_skills:
    - deployment-patterns
license: MIT
---

# Observability

## Overview

Use OpenTelemetry to collect distributed traces, metrics, and logs with a single vendor-neutral pipeline. Instrument code once, then export telemetry through the OpenTelemetry Collector to backends.

## When to Use

- Add or review traces, metrics, and logs in an application or library.
- Design SDK, Collector, or exporter configuration.
- Choose sampling strategies, context propagation formats, and resource attributes.
- Apply semantic conventions for spans, metrics, and log attributes.

## Core Pattern

1. **Instrument** with the OpenTelemetry API: create tracers, record spans, add metrics, and emit logs.
2. **Configure** the SDK with resource attributes, exporters, and samplers.
3. **Propagate** context across process boundaries using W3C Trace Context and Baggage.
4. **Export** via OTLP to the OpenTelemetry Collector or directly to a backend.
5. **Enrich** telemetry with semantic conventions and custom attributes.

## Common Mistakes

- Over-instrumenting hot paths or recording high-cardinality attributes.
- Mixing manual context propagation with auto-instrumentation inconsistently.
- Sampling all traces at head without considering tail-based sampling for errors.
- Hard-coding vendor-specific exporters in library code.
- Forgetting resource attributes that identify service, version, and environment.

## Scope Boundary

Prefer backend-specific skills for query languages, alerting, and dashboards. Prefer testing skills for load tests and SLO verification. Prefer SRE skills for incident response and runbooks.
