# Operational Guidance — Observability

This guidance is derived from the OpenTelemetry specification. It covers the vendor-neutral design of traces, metrics, logs, and the pipelines that move them from instrumentation to backends.

## Signals and concepts

OpenTelemetry unifies three telemetry signals:

- **Traces** capture the path of a request through a system as a tree of spans.
- **Metrics** record aggregatable measurements over time.
- **Logs** carry discrete events, optionally linked to traces.

Use resources to identify the service, version, environment, and host. Apply semantic conventions so backends can correlate and filter telemetry consistently.

## Instrumentation

Prefer automatic instrumentation when it covers the libraries and frameworks in use. Add manual instrumentation for domain-specific operations, custom business metrics, and spans that cross boundaries auto-instrumentation cannot see.

Keep instrumentation points focused:

- Create a span per meaningful operation, not per function call.
- Add attributes that are stable, low-cardinality, and useful for filtering.
- Avoid recording personally identifiable information or secrets.
- Use events within spans for timestamped sub-steps.

## Context propagation

Use W3C Trace Context and Baggage to carry context across process and network boundaries. Propagation must be explicit at every boundary: incoming requests, outgoing HTTP/gRPC calls, message producers and consumers, and background jobs. Do not rely on ambient context in async code without verifying the context is captured and restored.

## Sampling

Head-based sampling decides whether to record a trace at its start. Use it to control cost and volume. Tail-based sampling keeps spans until a trace completes and then decides based on properties like errors or latency. Use tail-based sampling when rare but important traces must be retained.

## SDK and Collector configuration

Separate configuration from code:

- Set resource attributes via environment variables or a declarative config.
- Configure exporters, batching, and retry behavior in one place.
- Use the OpenTelemetry Collector to receive, process, and export telemetry to multiple backends without changing application code.
- Keep collector pipelines simple: one receiver, optional processors, and one or more exporters.

## Exporters and backends

Export with OTLP when the backend supports it. Wrap vendor-specific exporters in configuration so application code stays portable. Do not emit vendor-specific formats from libraries or shared components.

## Semantic conventions

Use stable semantic conventions for HTTP, database, messaging, and cloud resource attributes. Only define custom conventions when no stable convention exists, and document them clearly.

## Common anti-patterns

- High-cardinality span attributes such as raw user IDs or timestamps.
- Mixing tracing, metrics, and log concerns in the same client call.
- Hard-coding endpoint URLs or backend credentials in SDK initialization.
- Ignoring propagation across message queues or batch processors.
- Treating the collector as a place for business logic or heavy transformation.

## When to defer

- Backend query languages, dashboards, and alerts: defer to backend-specific or SRE skills.
- Load testing, performance baselines, and SLO verification: defer to testing skills.
- Incident response and runbooks: defer to SRE skills.
