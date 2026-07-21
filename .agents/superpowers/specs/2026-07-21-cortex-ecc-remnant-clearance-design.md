---
name: cortex-ecc-remnant-clearance-design
description: >-
  Drain Claude-Cortex and ECC third-party retained source into source-backed
  first-party skills, then remove the residual upstream snapshots.
---

# Cortex/ECC remnant clearance design

## Goals

1. Inventory the retained `claude-cortex` and `ecc` upstream source so the
   first-party skill design set covers every core domain we want to keep.
2. Design first-party skills that represent coherent core domains and are
   backed by canonical references (bundled or cited).
3. Delete all retained third-party source that is **not** currently projected
   in any marketplace pack.
4. Convert the 30 currently projected remnants into first-party skills, then
   delete their upstream snapshots.

## Inventory summary

- **Claude-Cortex upstream** (`sources/third_party/claude-cortex/upstream/skills/skill-index.json`):
  154 skills listed in the index, 147 directories currently retained in source
  custody. 7 index entries no longer have a local directory.
- **ECC upstream** (`sources/third_party/ecc/upstream/manifest.json`): 271
  skills copied into local custody.
- **Total retained source skills**: 418 (147 Cortex + 271 ECC).
- **Currently projected**: 30 (16 Cortex + 14 ECC).
- **Heuristic domain classification** and full skill list are in the scratch
  inventory: `.agents/superpowers/specs/2026-07-21-cortex-ecc-retained-upstream-inventory.md`.

## Domain distribution

| domain | retained total | currently projected | notes |
|--------|---------------:|--------------------:|-------|
| security | 53 | 5 | Strongest core domain. Merge the three Cortex security skills + ECC `security-review` + `safety-guard` into `secure-development` / `risk-gates`. |
| ai-agents | 50 | 6 | Large but fragmented. Consolidate into `agentic-harness` and `agent-evaluation`. |
| testing-qa | 48 | 2 | Many are language/framework-specific and will be absorbed into language skills. The generic `release-prep` belongs under release engineering. |
| python | 14 | 3 | Convert to `python` + `python-frameworks`. |
| javascript-typescript | 24 | 0 | Backlog candidate; consider a `javascript` / `node-js` skill after Tier 1. |
| web-frontend | 28 | 3 | Convert `interaction-design`, `ux-review`, `webapp-testing` into `frontend-ux` and `playwright-testing`. |
| api-backend | 17 | 2 | Convert `api-design-patterns` into `api-design`; absorb `api-design` (ECC) and `api-gateway-patterns` later. |
| architecture-patterns | 15 | 2 | Convert `event-driven-architecture` into `event-driven-systems`; `system-design` is a backlog candidate. |
| deployment-devops | 15 | 1 | Convert `release-analysis`, `release-prep`, `deployment-patterns` into `release-engineering`. |
| product-planning | 21 | 2 | Convert `development-estimation` and `requirements-discovery` into `estimation` and `requirements-elicitation`. |
| research-intelligence | 9 | 1 | Convert `research-ops` into a first-party `research-ops` skill. |
| other | 51 | 1 | Mostly process/content/vibe skills with no clear canonical source. `ai-first-engineering` folds into `agentic-harness`. |
| dotnet / java-jvm / mobile-native / cpp-rust-systems / data-databases | 49 | 0 | Backlog candidates for language/platform skills. |
| writing-docs / design-ux / business-ops / ops-admin | 43 | 0 | Out of scope for source-backed technical skills; will be deleted. |

## Design principles

- **One skill per core domain**, not one per upstream skill.
- **Skill body under 500 words** per `docs/skill-standards-policy.md`; detailed
  guidance lives in `references/operational-guidance.md`.
- **Authority is explicit** in `assets/authority/authority.yaml` and
  `assets/authority/CITATIONS.md`.
- **Projected remnants first**, then retained backlog. We only keep upstream
  snapshots while a skill is actively projected.
- **Mega-packs retire last**: once `codex-cortex` and `everything-codex-code`
  have no `claude-cortex`/`ecc` entries, remove those mega-pack plugin roots.

## Proposed first-party skill set

### Tier 1 — convert the currently projected remnants

| skill | domain | replaces (projected) | pack home | authority lane | canonical references |
|-------|--------|----------------------|-----------|----------------|----------------------|
| `python` | Python language | `async-python-patterns`, `python-performance-optimization`, `python-testing-patterns` | `language-patterns-pack` | `skills-with-citation` | Python docs (PSF), pytest docs, asyncio docs, mypy docs |
| `python-frameworks` | Python frameworks | retained `django-*`, `fastapi-patterns` | `language-patterns-pack` | `skills-with-citation` | Django docs (BSD), FastAPI docs (MIT), Celery docs (BSD) |
| `api-design` | API design | `api-design-patterns` | `api-contracts-pack` | `skills-with-mixed-source` | OpenAPI Specification (Apache-2.0, vendored), IETF HTTP/REST RFCs, OWASP API Security |
| `secure-development` | Security engineering | `secure-coding-practices`, `security-testing-patterns`, `threat-modeling-techniques`, `security-review` (ECC) | `security-pack` | `skills-with-citation` | OWASP Developer Guide, OWASP Testing Guide, CWE, CAPEC, NIST SP 800-53 |
| `risk-gates` (expanded) | Operational safety | `safety-guard` (ECC) | `repo-worker-pack` / `house-skills` | `skills-with-citation` | Safety/risk-gate literature, destructive-operation guard patterns |
| `frontend-ux` | Frontend & UX | `interaction-design`, `ux-review` | `frontend-pack` | `skills-with-citation` | WCAG (W3C), W3C HTML/CSS specs, MDN (CC-BY-SA), Material Design, Apple HIG |
| `playwright-testing` | Web app testing | `webapp-testing` | `frontend-pack` | `skills-with-source` or `skills-with-citation` | Playwright docs (MIT), W3C WebDriver |
| `mermaid-diagramming` | Technical diagramming | `mermaid-diagramming` | `planning-pack` | `skills-with-source` | Mermaid docs (MIT) |
| `event-driven-systems` | Event-driven architecture | `event-driven-architecture` | `architecture-pack` | `skills-with-citation` | Kafka docs (Apache-2.0), RabbitMQ docs, public EDA patterns |
| `release-engineering` | Release & deployment | `release-analysis`, `release-prep`, `deployment-patterns` (ECC) | `planning-pack` / `engineering-pack` | `skills-with-citation` | Docker docs, Kubernetes docs (CC-BY-4.0), GitHub Actions docs, SRE/public CI-CD resources |
| `requirements-elicitation` | Requirements | `requirements-discovery` | `planning-pack` | `skills-with-citation` | Public requirements-engineering references |
| `estimation` | Effort estimation | `development-estimation` | `planning-pack` | `skills-with-citation` | COCOMO, Agile estimation literature |
| `agentic-harness` | Agent harness & loops | `agentic-os`, `autonomous-agent-harness`, `continuous-agent-loop`, `agent-harness-construction`, `dynamic-workflow-mode`, `dmux-workflows`, `ai-first-engineering` | `agentic-workflows` | `skills-with-citation` | dmux repo (MIT), OpenAI/Anthropic docs, public agent-OS/harness papers |
| `agent-evaluation` | Agent evaluation | `agent-eval`, `agent-self-evaluation`, `agent-architecture-audit` | `agentic-evaluation` | `skills-with-citation` | SWE-bench, public agent-eval benchmark methodologies |
| `research-ops` | Research workflow | `research-ops` (ECC) | `research-pack` | `skills-with-citation` | Evidence-based research methods, public search/evaluation references |

### Tier 2 — backlog candidates driven by retained source

These are not currently projected and are only built if we decide the domain is
in scope. They would be created after Tier 1 is complete.

| skill | domain | covers (retained examples) | authority lane | canonical references |
|-------|--------|---------------------------|----------------|----------------------|
| `system-design` | System design | `system-design`, `microservices-patterns`, `api-gateway-patterns`, `architectural-analysis` | `skills-with-citation` | AWS Well-Architected, Azure Architecture Center, public patterns |
| `javascript` | JavaScript / Node.js | `nodejs-patterns`, `vite-patterns`, `nextjs-turbopack`, etc. | `language-patterns-pack` | MDN (CC-BY-SA), Node.js docs, Vite docs |
| `java` | Java / JVM | `java-coding-standards`, `springboot-patterns`, `kotlin-patterns`, `jpa-patterns` | `language-patterns-pack` | OpenJDK docs, Spring docs (Apache-2.0) |
| `mobile-development` | Mobile / native | `android-clean-architecture`, `flutter-dart-patterns`, `swiftui-patterns`, `ios-icon-gen` | `frontend-pack` | Android docs (Apache-2.0), Flutter docs (BSD), Apple HIG |
| `database-engines` (expanded) | Databases | `postgres-patterns`, `mysql-patterns`, `redis-patterns`, `database-migrations`, `clickhouse-io` | `data-platform-pack` | Vendor/project docs (varied; verify licenses) |
| `observability` (expanded) | Observability | `canary-watch`, `latency-critical-systems`, `cost-tracking` | `engineering-pack` | OpenTelemetry docs (Apache-2.0), Prometheus docs (Apache-2.0) |

## Deletion plan

1. **Delete non-projected retained source now.** Remove every directory under
   `sources/third_party/claude-cortex/upstream/skills/` and
   `sources/third_party/ecc/upstream/skills/` that is **not** in the currently
   projected set. Projected sets are listed in the inventory file.
2. **Keep projected snapshots until conversion.** The 30 projected upstream
   snapshots stay in place while their first-party replacements are authored and
   the `custody-pack-registry.json` entries are switched.
3. **Delete projected snapshots after switch.** Once each Tier 1 first-party
   skill is validated and the marketplace is rebuilt, remove its upstream
   snapshot and any now-stale adapter under `adapters/codex/`.

## Conversion sequence

1. **Delete non-projected upstream source** and commit.
2. **Author Tier 1 skills** in this order:
   1. `python` + `python-frameworks`
   2. `api-design`
   3. `secure-development` + `risk-gates` expansion
   4. `frontend-ux` + `playwright-testing`
   5. `mermaid-diagramming` + `event-driven-systems`
   6. `release-engineering` + `requirements-elicitation` + `estimation`
   7. `agentic-harness` + `agent-evaluation` + `research-ops`
3. **Regenerate and validate** with `py -3 tools/rebuild_marketplace.py` and
   `py -3 tools/check_marketplace.py` after each batch.
4. **Retire mega-packs**: remove `codex-cortex` and `everything-codex-code`
   from `plugin-roots.json` and `custody-pack-registry.json` once they have no
   active `claude-cortex`/`ecc` entries.
5. **Tier 2 backlog**: build only the domains approved after Tier 1.

## Risks and blockers

- **No single vendored source** for agentic workflows, estimation, requirements,
  and research-ops. These will be `skills-with-citation` and require careful
  clean-room synthesis.
- **License verification** for any vendored source (`api-design` OpenAPI spec,
  `playwright-testing`, `mermaid-diagramming`). Confirm redistribution rights
  before adding to `assets/authority/reference-source/`.
- **Word-count rewrite**: the upstream bodies are far over 500 words. Tier 1
  skills are rewrites, not normalisations.
- **Pack churn**: skill renames and pack moves must be reflected in
  `custody-pack-registry.json` and the generated plugin surfaces.
- **Destructive deletion**: removing upstream snapshots is irreversible. The
  inventory files and this design doc are the record of what was removed.

## Next steps

- Review this design set.
- Approve Tier 1 skill list and the deletion scope.
- Start with the `python` / `python-frameworks` cluster or the security cluster.
