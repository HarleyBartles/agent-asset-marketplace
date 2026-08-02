# Third-party upstream inventory (Claude-Cortex + ECC) v2

## Domain summary

| domain | total | projected | families |
|--------|-------|-----------|----------|
| ai-agents | 50 | 6 | claude-cortex, ecc |
| api-backend | 17 | 2 | claude-cortex, ecc |
| architecture-patterns | 15 | 4 | claude-cortex, ecc |
| business-ops | 9 | 0 | claude-cortex, ecc |
| cpp-rust-systems | 10 | 0 | claude-cortex, ecc |
| data-databases | 3 | 0 | claude-cortex, ecc |
| deployment-devops | 15 | 1 | claude-cortex, ecc |
| design-ux | 6 | 0 | claude-cortex, ecc |
| dotnet | 3 | 0 | ecc |
| java-jvm | 12 | 0 | ecc |
| javascript-typescript | 24 | 0 | claude-cortex, ecc |
| mobile-native | 9 | 0 | claude-cortex, ecc |
| ops-admin | 12 | 0 | ecc |
| other | 51 | 1 | claude-cortex, ecc |
| product-planning | 21 | 2 | claude-cortex, ecc |
| python | 14 | 3 | claude-cortex, ecc |
| research-intelligence | 9 | 1 | claude-cortex, ecc |
| security | 53 | 5 | claude-cortex, ecc |
| skills-meta | 1 | 0 | ecc |
| testing-qa | 48 | 2 | claude-cortex, ecc |
| web-frontend | 28 | 3 | claude-cortex, ecc |
| writing-docs | 15 | 0 | claude-cortex, ecc |

## ai-agents

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | atomic-commits | no |  | Use this skill when a working tree contains uncommitted changes that need to be split into |
| claude-cortex | backlog-md | no |  | Task tracking system for agents via Backlog.md CLI. Use when creating deferred issues duri |
| claude-cortex | dispatching-parallel-agents | no |  | Use when facing 3+ independent failures that can be investigated without shared state or d |
| claude-cortex | docx | no |  | Comprehensive document creation, editing, and analysis with support for tracked changes, c |
| claude-cortex | knowledge-synthesis | no |  | Extract insights from multi-agent interactions, identify patterns, and build collective in |
| claude-cortex | model-comparator | no |  | Use this skill when comparing AI or LLM models on benchmarks, capability, cost, latency, c |
| claude-cortex | multi-llm-consult | no |  | Consult external LLMs (Gemini, OpenAI/Codex, Qwen) for second opinions, alternative plans, |
| claude-cortex | multi-perspective-analysis | no |  | Adopt multiple expert personas sequentially for complex problem analysis from diverse pers |
| claude-cortex | pdf | no |  | Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs,  |
| claude-cortex | pptx | no |  | Presentation creation, editing, and analysis. When Claude needs to work with presentations |
| claude-cortex | reasoning-controls | no |  | Use when adjusting reasoning depth, budgets, or metrics visibility - provides guidance for |
| claude-cortex | skill-creator | no |  | Guide for creating effective skills. Use when users want to create a new skill (or update  |
| claude-cortex | task-orchestration | no |  | Use when coordinating complex tasks with orchestration, delegation, or parallel workstream |
| claude-cortex | using-superpowers | no |  | Use when starting any conversation - establishes mandatory workflows for finding and using |
| claude-cortex | xlsx | no |  | Comprehensive spreadsheet creation, editing, and analysis with support for formulas, forma |
| ecc | agent-eval | yes | codex-cortex | Head-to-head comparison of coding agents (Claude Code, Aider, Codex, etc.) on custom tasks |
| ecc | agent-harness-construction | yes | superpowers | Design and optimize AI agent action spaces, tool definitions, and observation formatting f |
| ecc | agent-introspection-debugging | no | repo-worker-base | Structured self-debugging workflow for AI agent failures using capture, diagnosis, contain |
| ecc | agent-payment-x402 | no | superpowers | Add x402 payment execution to AI agents with per-task budgets, spending controls, and non- |
| ecc | agent-self-evaluation | yes | codex-cortex | Use after completing any non-trivial task. The agent self-rates its output on 5 axes — acc |
| ecc | agent-sort | no | repo-worker-base | Build an evidence-backed ECC install plan for a specific repo by sorting skills, commands, |
| ecc | agentic-engineering | no | codex-cortex | Operate as an agentic engineer using eval-first execution, decomposition, and cost-aware m |
| ecc | autonomous-agent-harness | yes | codex-cortex | Transform Claude Code into a fully autonomous agent system with persistent memory, schedul |
| ecc | autonomous-loops | no | codex-cortex | Patterns and architectures for autonomous Claude Code loops — from simple sequential pipel |
| ecc | blueprint | no | future-domain-pack | Turn a one-line objective into a step-by-step construction plan for multi-session, multi-a |
| ecc | claude-devfleet | no | repo-worker-base | Orchestrate multi-agent coding tasks via Claude DevFleet — plan projects, dispatch paralle |
| ecc | config-gc | no | repo-worker-base | Garbage collection for your Claude Code configuration. Periodically scans ~/.claude (skill |
| ecc | configure-ecc | no | future-domain-pack | Interactive installer for Everything Claude Code — guides users through selecting and inst |
| ecc | context-budget | no | codex-cortex | Audits Claude Code context window consumption across agents, skills, MCP servers, and rule |
| ecc | cost-tracking | no | repo-worker-base | Track and report Claude Code token usage, spending, and budgets from the local ECC cost-tr |
| ecc | data-scraper-agent | no | repo-worker-base | Build a fully automated AI-powered data collection agent for any public source — job board |
| ecc | dmux-workflows | yes | superpowers | Multi-agent orchestration using dmux (tmux pane manager for AI agents). Patterns for paral |
| ecc | dynamic-workflow-mode | yes | codex-cortex | Design task-local harnesses, eval gates, and reusable skill extraction for Claude dynamic  |
| ecc | flox-environments | no | repo-worker-base | Create reproducible, cross-platform (macOS/Linux) development environments with Flox, a de |
| ecc | lead-intelligence | no | superpowers | AI-native lead intelligence and outreach pipeline. Replaces Apollo, Clay, and ZoomInfo wit |
| ecc | nanoclaw-repl | no | future-domain-pack | Operate and extend NanoClaw v2, ECC's zero-dependency session-aware REPL built on claude - |
| ecc | openclaw-persona-forge | no | superpowers | 为 OpenClaw AI Agent 锻造完整的龙虾灵魂方案。根据用户偏好或随机抽卡， 输出身份定位、灵魂描述(SOUL.md)、角色化底线规则、名字和头像生图提示词。 如当前环 |
| ecc | orch-add-feature | no | codex-cortex | Orchestrate building a brand-new feature end to end — research, plan, TDD implementation,  |
| ecc | orch-pipeline | no | codex-cortex | Shared orchestration engine for the orch-* skill family. Defines the gated Research-Plan-T |
| ecc | plan-orchestrate | no | codex-cortex | Read a plan document, decompose it into steps, design a per-step agent chain from the ECC  |
| ecc | recursive-decision-ledger | no | superpowers | Use when the user asks for repeated rollouts, marked decision processes, high-dimensional  |
| ecc | regex-vs-llm-structured-text | no | future-domain-pack | Decision framework for choosing between regex and LLM when parsing structured text — start |
| ecc | santa-method | no | codex-cortex | Multi-agent adversarial verification with convergence loop. Two independent review agents  |
| ecc | search-first | no | superpowers | Research-before-coding workflow. Search for existing tools, libraries, and patterns before |
| ecc | skill-comply | no | repo-worker-base | Visualize whether skills, rules, and agent definitions are actually followed — auto-genera |
| ecc | social-publisher | no | superpowers | Agent-driven scheduling and publishing of social media posts across 13 platforms via Socia |
| ecc | team-agent-orchestration | no | superpowers | Run team-based orchestration for agent squads using work items, ownership, agent Kanban, m |
| ecc | team-builder | no | superpowers | Interactive agent picker for composing and dispatching parallel teams |
| ecc | verification-loop | no | codex-cortex | A comprehensive verification system for Claude Code sessions. |
| ecc | workspace-surface-audit | no | repo-worker-base | Audit the active repo, MCP servers, plugins, connectors, env surfaces, and harness setup,  |

## api-backend

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | api-design-patterns | yes |  | Comprehensive REST and GraphQL API design patterns with versioning, pagination, error hand |
| claude-cortex | documentation-production | no |  | Use when generating, updating, or organizing documentation (component/API docs, project in |
| claude-cortex | event-driven-architecture | yes |  | Event-driven architecture patterns with event sourcing, CQRS, and message-driven communica |
| claude-cortex | feature-implementation | no |  | Use when implementing a feature or multi-file code change - provides structured implementa |
| claude-cortex | microservices-patterns | no |  | Comprehensive microservices architecture patterns covering service decomposition, communic |
| claude-cortex | openapi-specification | no |  | OpenAPI 3.x specification design, schema patterns, and validation for REST API contracts.  |
| claude-cortex | reference-documentation | no |  | Create exhaustive technical references, API documentation, and searchable reference materi |
| ecc | ai-regression-testing | no | codex-cortex | Regression testing strategies for AI-assisted development. Sandbox-mode API testing withou |
| ecc | api-connector-builder | no | repo-worker-base | Build a new API connector or provider by matching the target repo's existing integration p |
| ecc | api-design | no | future-domain-pack | REST API design patterns including resource naming, status codes, pagination, filtering, e |
| ecc | canary-watch | no | codex-cortex | Use this skill to monitor and verify a deployed URL after releases — checks HTTP endpoints |
| ecc | cost-aware-llm-pipeline | no | codex-cortex | Cost optimization patterns for LLM API usage — model routing by task complexity, budget tr |
| ecc | ito-market-intelligence | no | superpowers | Research prediction-market events, venues, underliers, liquidity, and news context for Itô |
| ecc | jira-integration | no | codex-cortex | Use this skill when retrieving Jira tickets, analyzing requirements, updating ticket statu |
| ecc | laravel-patterns | no | codex-cortex | Laravel architecture patterns, routing/controllers, Eloquent ORM, service layers, queues,  |
| ecc | scientific-db-pubmed-database | no | codex-cortex | Direct PubMed and NCBI E-utilities search workflows for biomedical literature, MeSH querie |
| ecc | x-api | no | future-domain-pack | X/Twitter API integration for posting tweets, threads, reading timelines, search, and anal |

## architecture-patterns

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | code-explanation | no |  | Use when explaining code, concepts, or system behavior to a specific audience level - prov |
| claude-cortex | cqrs-event-sourcing | no |  | CQRS and Event Sourcing patterns for scalable, auditable systems with separated read/write |
| claude-cortex | doc-architecture-review | no |  | Evaluate documentation information architecture: navigation paths, discoverability, progre |
| claude-cortex | doc-health-audit | no |  | Orchestrate a full documentation health audit across five dimensions: structural health, s |
| claude-cortex | knowledge-stack | no |  | Use this skill whenever working inside any of Nick's repos (Atlas Crew, Inferno Lab, or an |
| claude-cortex | mermaid-diagramming | yes |  | Mermaid diagram creation covering flowcharts, sequence diagrams, ERDs, state machines, Gan |
| claude-cortex | release-analysis | yes |  | User-triggered analysis of how a system gets deployed and recovered — across local (Docker |
| claude-cortex | socratic-questioning | no |  | Guide discovery through questioning techniques and pattern recognition for Clean Code, GoF |
| ecc | agent-architecture-audit | yes | codex-cortex | Full-stack diagnostic for agent and LLM applications. Audits the 12-layer agent stack for  |
| ecc | agentic-os | yes | codex-cortex | Build persistent multi-agent operating systems on Claude Code. Covers kernel architecture, |
| ecc | architecture-decision-records | no | codex-cortex | Capture architectural decisions made during Claude Code sessions as structured ADRs. Auto- |
| ecc | code-tour | no | repo-worker-base | Create CodeTour `.tour` files — persona-targeted, step-by-step walkthroughs with real file |
| ecc | codebase-onboarding | no | repo-worker-base | Analyze an unfamiliar codebase and generate a structured onboarding guide with architectur |
| ecc | inherit-legacy-style | no | repo-worker-base | Legacy-project style inheritance skill. Use when the user types /inherit-legacy-style, or  |
| ecc | ito-data-atlas-agent | no | codex-cortex | Design background Data Atlas style agents for Itô basket research, market discovery, param |

## business-ops

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | user-journey-mapping | no |  | Create comprehensive user journey maps that identify pain points, opportunities, and emoti |
| ecc | customer-billing-ops | no | superpowers | Operate customer billing workflows such as subscriptions, refunds, churn triage, billing-p |
| ecc | ecc-tools-cost-audit | no | repo-worker-base | Evidence-first ECC Tools burn and billing audit workflow. Use when investigating runaway P |
| ecc | energy-procurement | no | future-domain-pack | Codified expertise for electricity and gas procurement, tariff optimization, demand charge |
| ecc | finance-billing-ops | no | superpowers | Evidence-first revenue, pricing, refunds, team-billing, and billing-model truth workflow f |
| ecc | healthcare-phi-compliance | no | codex-cortex | Protected Health Information (PHI) and Personally Identifiable Information (PII) complianc |
| ecc | investor-materials | no | superpowers | Create and update pitch decks, one-pagers, investor memos, accelerator applications, finan |
| ecc | investor-outreach | no | future-domain-pack | Draft cold emails, warm intro blurbs, follow-ups, update emails, and investor communicatio |
| ecc | logistics-exception-management | no | future-domain-pack | Codified expertise for handling freight exceptions, shipment delays, damages, losses, and  |

## cpp-rust-systems

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | constructive-dissent | no |  | Structured disagreement protocols that expose weaknesses, test assumptions, and generate a |
| claude-cortex | pre-mortem | no |  | Imagine failure first to surface guardrails and feature mitigations. |
| claude-cortex | product-strategy | no |  | Product vision, roadmap development, and go-to-market execution with structured prioritiza |
| ecc | council | no | future-domain-pack | Convene a four-voice council for ambiguous decisions, tradeoffs, and go/no-go calls. Use w |
| ecc | cpp-coding-standards | no | repo-worker-base | C++ coding standards based on the C++ Core Guidelines (isocpp.github.io). Use when writing |
| ecc | cpp-testing | no | codex-cortex | Use only when writing/updating/fixing C++ tests, configuring GoogleTest/CTest, diagnosing  |
| ecc | golang-patterns | no | future-domain-pack | Idiomatic Go patterns, best practices, and conventions for building robust, efficient, and |
| ecc | golang-testing | no | codex-cortex | Go testing patterns including table-driven tests, subtests, benchmarks, fuzzing, and test  |
| ecc | rust-patterns | no | future-domain-pack | Idiomatic Rust patterns, ownership, error handling, traits, concurrency, and best practice |
| ecc | rust-testing | no | codex-cortex | Rust testing patterns including unit tests, integration tests, async testing, property-bas |

## data-databases

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | legacy-modernization | no |  | Modernize legacy systems using proven migration patterns like strangler fig, feature flags |
| ecc | clickhouse-io | no | future-domain-pack | ClickHouse database patterns, query optimization, analytics, and data engineering best pra |
| ecc | scientific-db-uspto-database | no | superpowers | USPTO patent and trademark data workflow for official record lookup, PatentSearch queries, |

## deployment-devops

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | ai-tells-scan | no |  | Use when writing tasks produce prose artifacts (READMEs, docs, PR text, tutorials, guides, |
| claude-cortex | github-actions-workflows | no |  | GitHub Actions workflow patterns for CI/CD including matrix builds, reusable workflows, se |
| claude-cortex | gitops-workflows | no |  | GitOps workflows and patterns using ArgoCD and Flux for declarative Kubernetes deployments |
| claude-cortex | helm-chart-patterns | no |  | Helm chart development patterns for packaging and deploying Kubernetes applications. Use w |
| claude-cortex | incident-response | no |  | Incident triage, cascade prevention, and postmortem methodology. Use when handling product |
| claude-cortex | kubernetes-deployment-patterns | no |  | Kubernetes deployment strategies and workload patterns for production-grade applications.  |
| claude-cortex | terraform-best-practices | no |  | Terraform infrastructure-as-code best practices for scalable and maintainable cloud infras |
| ecc | dashboard-builder | no | future-domain-pack | Build monitoring dashboards that answer real operator questions for Grafana, SigNoz, and s |
| ecc | deployment-patterns | yes | superpowers | Deployment workflows, CI/CD pipeline patterns, Docker containerization, health checks, rol |
| ecc | hermes-imports | no | repo-worker-base | Convert local Hermes operator workflows into sanitized ECC skills and release-pack artifac |
| ecc | kubernetes-patterns | no | codex-cortex | Kubernetes workload patterns, resource management, RBAC, probes, autoscaling, ConfigMap/Se |
| ecc | mysql-patterns | no | future-domain-pack | MySQL and MariaDB schema, query, indexing, transaction, replication, and connection-pool p |
| ecc | opensource-pipeline | no | superpowers | Open-source pipeline: fork, sanitize, and package private projects for safe public release |
| ecc | production-audit | no | repo-worker-base | Local-evidence production readiness audit for shipped apps, pre-launch reviews, post-merge |
| ecc | redis-patterns | no | future-domain-pack | Redis data structure patterns, caching strategies, distributed locks, rate limiting, pub/s |

## design-ux

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | chart-builder | no |  | Use this skill when creating data visualizations, selecting the right chart type, or gener |
| claude-cortex | research-methodology | no |  | Structured research using sophisticated query design, source vetting, and synthesis techni |
| ecc | blender-motion-state-inspection | no | future-domain-pack | Use this skill when inspecting Blender characters, rigs, poses, animation retargeting, gro |
| ecc | brand-discovery | no | future-domain-pack | Use when a brand needs to discover or articulate its identity through structured multi-ses |
| ecc | recsys-pipeline-architect | no | future-domain-pack | Design composable recommendation, ranking, and feed pipelines using the six-stage Source→H |
| ecc | swift-actor-persistence | no | future-domain-pack | Thread-safe data persistence in Swift using actors — in-memory cache with file-backed stor |

## dotnet

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| ecc | csharp-testing | no | codex-cortex | C# and .NET testing patterns with xUnit, FluentAssertions, mocking, integration tests, and |
| ecc | dotnet-patterns | no | future-domain-pack | Idiomatic C# and .NET patterns, conventions, dependency injection, async/await, and best p |
| ecc | fsharp-testing | no | codex-cortex | F# testing patterns with xUnit, FsUnit, Unquote, FsCheck property-based testing, integrati |

## java-jvm

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| ecc | android-clean-architecture | no | repo-worker-base | Clean Architecture patterns for Android and Kotlin Multiplatform projects — module structu |
| ecc | hexagonal-architecture | no | codex-cortex | Design, implement, and refactor Ports & Adapters systems with clear domain boundaries, dep |
| ecc | java-coding-standards | no | future-domain-pack | Java coding standards for Spring Boot and Quarkus services: naming, immutability, Optional |
| ecc | jpa-patterns | no | codex-cortex | JPA/Hibernate patterns for entity design, relationships, query optimization, transactions, |
| ecc | kotlin-exposed-patterns | no | repo-worker-base | JetBrains Exposed ORM patterns including DSL queries, DAO pattern, transactions, HikariCP  |
| ecc | kotlin-testing | no | codex-cortex | Kotlin testing patterns with Kotest, MockK, coroutine testing, property-based testing, and |
| ecc | nestjs-patterns | no | codex-cortex | NestJS architecture patterns for modules, controllers, providers, DTO validation, guards,  |
| ecc | quarkus-patterns | no | codex-cortex | Quarkus 3.x LTS architecture patterns with Camel for messaging, RESTful API design, CDI se |
| ecc | quarkus-tdd | no | codex-cortex | Test-driven development for Quarkus 3.x LTS using JUnit 5, Mockito, REST Assured, Camel te |
| ecc | springboot-patterns | no | codex-cortex | Spring Boot architecture patterns, REST API design, layered services, data access, caching |
| ecc | springboot-tdd | no | codex-cortex | Test-driven development for Spring Boot using JUnit 5, Mockito, MockMvc, Testcontainers, a |
| ecc | tinystruct-patterns | no | codex-cortex | Expert guidance for developing with the tinystruct Java framework. Use when working on the |

## javascript-typescript

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | architectural-analysis | no |  | User-triggered deep architectural analysis of a codebase or scoped subtree across eight mo |
| claude-cortex | html-seo-review | no |  | Audit static HTML files for on-page SEO, content quality, easy-win performance signals, an |
| claude-cortex | react-performance-optimization | no |  | React performance optimization patterns using memoization, code splitting, and efficient r |
| ecc | angular-developer | no | codex-cortex | Generates Angular code and provides architectural guidance. Trigger when creating projects |
| ecc | backend-patterns | no | codex-cortex | Backend architecture patterns, API design, database optimization, and server-side best pra |
| ecc | bun-runtime | no | codex-cortex | Bun as runtime, package manager, bundler, and test runner. When to choose Bun vs Node, mig |
| ecc | ck | no | future-domain-pack | Persistent per-project memory for Claude Code. Auto-loads project context on session start |
| ecc | documentation-lookup | no | codex-cortex | Use up-to-date library and framework docs via Context7 MCP instead of training data. Activ |
| ecc | frontend-a11y | no | future-domain-pack | Accessibility patterns for React and Next.js — semantic HTML, ARIA attributes, form labeli |
| ecc | frontend-patterns | no | future-domain-pack | Frontend development patterns for React, Next.js, state management, performance optimizati |
| ecc | mcp-server-patterns | no | codex-cortex | Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation, st |
| ecc | motion-advanced | no | future-domain-pack | Advanced motion patterns for React / Next.js — drag & drop, gestures, text animations, SVG |
| ecc | motion-patterns | no | future-domain-pack | Production-ready animation patterns for React / Next.js — button, modal, toast, stagger, p |
| ecc | motion-ui | no | future-domain-pack | Production-ready UI motion system for React/Next.js. Use when implementing animations, tra |
| ecc | nextjs-turbopack | no | future-domain-pack | Next.js 16+ and Turbopack — incremental bundling, FS caching, dev speed, and when to use T |
| ecc | nodejs-keccak256 | no | future-domain-pack | Prevent Ethereum hashing bugs in JavaScript and TypeScript. Node's sha3-256 is NIST SHA3,  |
| ecc | prisma-patterns | no | future-domain-pack | Prisma ORM patterns for TypeScript backends — schema design, query optimization, transacti |
| ecc | react-patterns | no | codex-cortex | React 18/19 patterns including hooks discipline, server/client component boundaries, Suspe |
| ecc | react-performance | no | repo-worker-base | React and Next.js performance optimization patterns adapted from Vercel Engineering's Reac |
| ecc | react-testing | no | codex-cortex | React component testing with React Testing Library, Vitest/Jest, MSW for network mocking,  |
| ecc | remotion-video-creation | no | future-domain-pack | Best practices for Remotion - Video creation in React. 29 domain-specific rules covering 3 |
| ecc | ui-to-vue | no | future-domain-pack | Use when the user has UI screenshots or design exports that need batch conversion into Vue |
| ecc | vite-patterns | no | future-domain-pack | Vite build tool patterns including config, plugins, HMR, env variables, proxy setup, SSR,  |
| ecc | vue-patterns | no | codex-cortex | Vue.js 3 Composition API patterns, component architecture, reactivity best practices, Pini |

## mobile-native

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | terms-of-service | no |  | Use this skill when you need to draft Terms of Service, a Privacy Policy, or an End-User L |
| ecc | accessibility | no | codex-cortex | Design, implement, and audit inclusive digital products using WCAG 2.2 Level AA standards. |
| ecc | cisco-ios-patterns | no | codex-cortex | Cisco IOS and IOS-XE review patterns for show commands, config hierarchy, wildcard masks,  |
| ecc | foundation-models-on-device | no | superpowers | Apple FoundationModels framework for on-device LLM — text generation, guided generation wi |
| ecc | homelab-wireguard-vpn | no | future-domain-pack | WireGuard VPN server setup, peer configuration, key generation, split tunneling vs full tu |
| ecc | ios-icon-gen | no | superpowers | Generate iOS app icons as PNG imagesets for Xcode asset catalogs from SF Symbols (5000+ Ap |
| ecc | kotlin-coroutines-flows | no | codex-cortex | Kotlin Coroutines and Flow patterns for Android and KMP — structured concurrency, Flow ope |
| ecc | liquid-glass-design | no | superpowers | iOS 26 Liquid Glass design system — dynamic glass material with blur, reflection, and inte |
| ecc | swiftui-patterns | no | codex-cortex | SwiftUI architecture patterns, state management with @Observable, view composition, naviga |

## ops-admin

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| ecc | automation-audit-ops | no | codex-cortex | Evidence-first automation inventory and overlap audit workflow for ECC. Use when the user  |
| ecc | connections-optimizer | no | codex-cortex | Reorganize the user's X and LinkedIn network with review-first pruning, add/follow recomme |
| ecc | homelab-network-readiness | no | future-domain-pack | Readiness checklist for homelab VLAN segmentation, local DNS filtering, and WireGuard-styl |
| ecc | homelab-pihole-dns | no | future-domain-pack | Pi-hole installation, blocklist management, DNS-over-HTTPS setup, DHCP integration, local  |
| ecc | homelab-vlan-segmentation | no | future-domain-pack | Segmenting home networks into VLANs for IoT, guest, trusted, and server traffic using UniF |
| ecc | knowledge-ops | no | repo-worker-base | Knowledge base management, ingestion, sync, and retrieval across multiple storage layers ( |
| ecc | messages-ops | no | superpowers | Evidence-first live messaging workflow for ECC. Use when the user wants to read texts or D |
| ecc | network-bgp-diagnostics | no | future-domain-pack | Diagnostics-only BGP troubleshooting patterns for neighbor state, route exchange, prefix p |
| ecc | network-interface-health | no | future-domain-pack | Diagnose interface errors, drops, CRCs, duplex mismatches, flapping, speed negotiation iss |
| ecc | social-graph-ranker | no | superpowers | Weighted social-graph ranking for warm intro discovery, bridge scoring, and network gap an |
| ecc | terminal-ops | no | repo-worker-base | Evidence-first repo execution workflow for ECC. Use when the user wants a command run, a r |
| ecc | unified-notifications-ops | no | repo-worker-base | Operate notifications as one ECC-native workflow across GitHub, Linear, desktop alerts, ho |

## other

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | ai-tells-review | no |  | Use when public prose still sounds machine-written after ai-tells-scan. Complements ai-tel |
| claude-cortex | assumption-buster | no |  | Flip, remove, or exaggerate assumptions to unlock new solution angles. |
| claude-cortex | build-optimization | no |  | Build system optimization covering compilation, caching, incremental builds, and developer |
| claude-cortex | compliance-audit | no |  | Regulatory compliance auditing across GDPR, HIPAA, PCI DSS, SOC 2, and ISO frameworks with |
| claude-cortex | concept-forge | no |  | Score concepts on impact/delight/effort and pick a 1-day spike. |
| claude-cortex | condition-based-waiting | no |  | Use when tests have race conditions, timing dependencies, or inconsistent pass/fail behavi |
| claude-cortex | cortex-skills-loop | no |  | Drives the cortex skills recommend-feedback-rate loop. Use when a context change occurs (n |
| claude-cortex | executing-plans | no |  | Execution discipline that translates plans into tracked tasks with orchestration and verif |
| claude-cortex | fact-checker | no |  | Use this skill when verifying factual claims, checking accuracy of statements, or assessin |
| claude-cortex | finishing-a-development-branch | no |  | Use when implementation is complete, all tests pass, and you need to decide how to integra |
| claude-cortex | idea-lab | no |  | Timeboxed divergent ideation that outputs ranked options plus day-one experiments. |
| claude-cortex | internal-comms | no |  | A set of resources to help write all kinds of internal communications, using company-speci |
| claude-cortex | mashup | no |  | Force-fit patterns from other domains to spark novel concepts. |
| claude-cortex | receiving-code-review | no |  | Use when receiving code review feedback, before implementing suggestions, especially if fe |
| claude-cortex | root-cause-tracing | no |  | Use when errors occur deep in execution and you need to trace back to find the original tr |
| claude-cortex | session-management | no |  | Use when loading, saving, or reflecting on session context - provides structured workflows |
| claude-cortex | sharing-skills | no |  | Use when you've developed a broadly useful skill and want to contribute it upstream via pu |
| claude-cortex | template-skill | no |  | A template for creating new skills. Use when initializing a new skill to ensure proper str |
| claude-cortex | token-efficiency | no |  | Compressed communication using symbols and abbreviations. Use when context is limited or b |
| claude-cortex | workflow-bug-fix | no |  | Systematic approach to identifying, fixing, and validating bug fixes. Use when fixing bugs |
| claude-cortex | workflow-performance | no |  | Systematic performance analysis and optimization. Use when things are slow, need optimizat |
| ecc | ai-first-engineering | yes | superpowers | Engineering operating model for teams where AI agents generate a large share of implementa |
| ecc | click-path-audit | no | repo-worker-base | Trace every user-facing button/touchpoint through its full state change sequence to find b |
| ecc | compose-multiplatform-patterns | no | future-domain-pack | Compose Multiplatform and Jetpack Compose patterns for KMP projects — state management, na |
| ecc | content-engine | no | future-domain-pack | Create platform-native content systems for X, LinkedIn, TikTok, YouTube, newsletters, and  |
| ecc | content-hash-cache-pattern | no | future-domain-pack | Cache expensive file processing results using SHA-256 content hashes — path-independent, a |
| ecc | continuous-learning | no | superpowers | [DEPRECATED - use continuous-learning-v2] Legacy v1 stop-hook skill extractor. v2 is a str |
| ecc | continuous-learning-v2 | no | superpowers | Instinct-based learning system that observes sessions via hooks, creates atomic instincts  |
| ecc | crosspost | no | future-domain-pack | Multi-platform content distribution across X, LinkedIn, Threads, and Bluesky. Adapts conte |
| ecc | data-throughput-accelerator | no | future-domain-pack | Use when large data ingestion, backfill, export, ETL, warehouse loading, manifest catch-up |
| ecc | ecc-guide | no | repo-worker-base | Guide users through ECC's current agents, skills, commands, hooks, rules, install profiles |
| ecc | evm-token-decimals | no | future-domain-pack | Prevent silent decimal mismatch bugs across EVM chains. Covers runtime decimal lookup, cha |
| ecc | fal-ai-media | no | codex-cortex | Unified media generation via fal.ai MCP — image, video, and audio. Covers text-to-image (N |
| ecc | git-workflow | no | repo-worker-base | Git workflow patterns including branching strategies, commit conventions, merge vs rebase, |
| ecc | hookify-rules | no | future-domain-pack | This skill should be used when the user asks to create a hookify rule, write a hook rule,  |
| ecc | iterative-retrieval | no | codex-cortex | Pattern for progressively refining context retrieval to solve the subagent context problem |
| ecc | laravel-plugin-discovery | no | codex-cortex | Discover and evaluate Laravel packages via LaraPlugins.io MCP. Use when the user wants to  |
| ecc | latency-critical-systems | no | superpowers | Use for latency-sensitive systems such as realtime dashboards, market data, streaming agen |
| ecc | ml-adoption-playbook | no | superpowers | End-to-end methodology for AI agents and software engineers to add machine learning algori |
| ecc | orch-refine-code | no | codex-cortex | Orchestrate a behavior-preserving refactor — confirm tests are green, restructure without  |
| ecc | parallel-execution-optimizer | no | repo-worker-base | Use when the user wants a task done much faster through parallel work, concurrent agents,  |
| ecc | perl-patterns | no | future-domain-pack | Modern Perl 5.36+ idioms, best practices, and conventions for building robust, maintainabl |
| ecc | pytorch-patterns | no | codex-cortex | PyTorch deep learning patterns and best practices for building robust, efficient, and repr |
| ecc | rules-distill | no | repo-worker-base | Scan skills to extract cross-cutting principles and distill them into rules — append, revi |
| ecc | seo | no | codex-cortex | Audit, plan, and implement SEO improvements across technical SEO, on-page optimization, st |
| ecc | strategic-compact | no | future-domain-pack | Suggests manual context compaction at logical intervals to preserve context through task p |
| ecc | swift-concurrency-6-2 | no | future-domain-pack | Swift 6.2 Approachable Concurrency — single-threaded by default, @concurrent for explicit  |
| ecc | token-budget-advisor | no | superpowers | Offers the user an informed choice about how much response depth to consume before answeri |
| ecc | uncloud | no | future-domain-pack | Use when managing an Uncloud cluster — deploying services, configuring Caddy ingress, addi |
| ecc | video-editing | no | superpowers | AI-assisted video editing workflows for cutting, structuring, and augmenting real footage. |
| ecc | visa-doc-translate | no | future-domain-pack | Translate visa application documents (images) to English and create a bilingual PDF with o |

## product-planning

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | brainstorming | no |  | Rapid ideation skill adapted from obra/superpowers to kick off cortex sessions. Use when d |
| claude-cortex | business-analyst | no |  | Use this skill when gathering and documenting business requirements, mapping processes, pe |
| claude-cortex | competitor-analyst | no |  | Use this skill when analyzing competitors, building competitive positioning, creating feat |
| claude-cortex | copywriter | no |  | Use this skill when writing persuasive, conversion-focused copy—landing pages, product des |
| claude-cortex | decision-maker | no |  | Use this skill when you face a complex or high-stakes decision and need a structured frame |
| claude-cortex | development-estimation | yes |  | Use when estimating time, effort, or complexity for features or projects - provides struct |
| claude-cortex | product-manager | no |  | Use this skill when writing product requirements documents, prioritizing features, creatin |
| claude-cortex | requesting-code-review | no |  | Use when completing tasks, implementing major features, or before merging to verify work m |
| claude-cortex | requirements-discovery | yes |  | Stakeholder interviews, PRD structure, and scope definition for software requirements elic |
| claude-cortex | tool-selection | no |  | Use when selecting between MCP tools based on task complexity and requirements - provides  |
| claude-cortex | ux-writer | no |  | Use this skill when crafting microcopy, UI text, or in-product writing—error messages, too |
| claude-cortex | workflow-feature | no |  | Complete feature development workflow from design to deployment. Use when implementing new |
| ecc | homelab-network-setup | no | future-domain-pack | Practical home and homelab network planning for gateways, switches, access points, IP rang |
| ecc | ito-trade-planner | no | superpowers | Build a non-advisory prediction-market trade planning worksheet for Itô or venue workflows |
| ecc | manim-video | no | future-domain-pack | Build reusable Manim explainers for technical concepts, graphs, system diagrams, and produ |
| ecc | marketing-campaign | no | superpowers | End-to-end marketing campaign planning and execution. Covers audience research, positionin |
| ecc | orch-build-mvp | no | codex-cortex | Orchestrate bootstrapping a working MVP from a design or spec document — ingest the doc, p |
| ecc | orch-change-feature | no | codex-cortex | Orchestrate altering an existing, working feature to new desired behavior — update its tes |
| ecc | product-capability | no | future-domain-pack | Translate PRD intent, roadmap asks, or product discussions into an implementation-ready ca |
| ecc | project-flow-ops | no | repo-worker-base | Operate execution flow across GitHub and Linear by triaging issues and pull requests, link |
| ecc | scientific-thinking-literature-review | no | codex-cortex | Systematic literature-review workflow for academic, biomedical, technical, and scientific  |

## python

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | async-python-patterns | yes |  | Python asyncio and concurrent programming patterns for high-performance applications. Use  |
| claude-cortex | dev-workflows | no |  | Use when running builds, executing tests, or improving developer experience workflows - pr |
| claude-cortex | python-performance-optimization | yes |  | Python performance optimization patterns using profiling, algorithmic improvements, and ac |
| claude-cortex | python-testing-patterns | yes |  | Python testing patterns and best practices using pytest, mocking, and property-based testi |
| ecc | database-migrations | no | future-domain-pack | Database migration best practices for schema changes, data migrations, rollbacks, and zero |
| ecc | django-celery | no | codex-cortex | Django + Celery async task patterns — configuration, task design, beat scheduling, retries |
| ecc | django-patterns | no | codex-cortex | Django architecture patterns, REST API design with DRF, ORM best practices, caching, signa |
| ecc | django-tdd | no | codex-cortex | Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, cover |
| ecc | error-handling | no | future-domain-pack | Patterns for robust error handling across TypeScript, Python, and Go. Covers typed errors, |
| ecc | generating-python-installer | no | codex-cortex | Commercial-grade Python installer expert for Windows: Nuitka extreme compilation, dist sli |
| ecc | netmiko-ssh-automation | no | future-domain-pack | Safe Python Netmiko patterns for read-only collection, bounded batch SSH, TextFSM parsing, |
| ecc | python-patterns | no | future-domain-pack | Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, effi |
| ecc | python-testing | no | codex-cortex | Python testing strategies using pytest, TDD methodology, fixtures, mocking, parametrizatio |
| ecc | scientific-pkg-gget | no | superpowers | gget CLI and Python workflow for quick genomic database queries, sequence lookup, BLAST-st |

## research-intelligence

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | codanna-codebase-intelligence | no |  | Use codanna MCP tools for semantic code search, call graphs, and impact analysis before gr |
| claude-cortex | web-researcher | no |  | Use this skill when you need to research a topic online, gather information from multiple  |
| ecc | carrier-relationship-management | no | future-domain-pack | Codified expertise for managing carrier portfolios, negotiating freight rates, tracking ca |
| ecc | deep-research | no | repo-worker-base | Multi-source deep research using firecrawl and exa MCPs. Searches the web, synthesizes fin |
| ecc | exa-search | no | codex-cortex | Neural search via Exa MCP for web, code, and company research. Use when the user needs web |
| ecc | ito-basket-compare | no | future-domain-pack | Compare Itô prediction-market baskets against a user's knowledge base, portfolio notes, fi |
| ecc | market-research | no | repo-worker-base | Conduct market research, competitive analysis, investor due diligence, and industry intell |
| ecc | prediction-market-oracle-research | no | superpowers | Research prediction markets as data sources or oracle signals for products, agents, dashbo |
| ecc | research-ops | yes | superpowers | Evidence-first current-state research workflow for ECC. Use when the user wants fresh fact |

## security

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | api-gateway-patterns | no |  | API Gateway patterns for routing, authentication, rate limiting, and service composition i |
| claude-cortex | atlas-crew-tasks | no |  | Use when filing, updating, sequencing, or querying tasks in any atlas-crew repo (Facet + t |
| claude-cortex | brand-library-architect | no |  | Build a complete brand library for a product — visual asset render pipeline, brand documen |
| claude-cortex | code-quality-workflow | no |  | Use when assessing or improving code quality, maintainability, performance, or security hy |
| claude-cortex | defense-in-depth | no |  | Use when invalid data causes failures deep in execution, requiring validation at multiple  |
| claude-cortex | eval-designer | no |  | Use this skill when building evaluation frameworks to measure LLM quality, safety, accurac |
| claude-cortex | kubernetes-security-policies | no |  | Kubernetes security policies, RBAC, and Pod Security Standards for hardened cluster deploy |
| claude-cortex | multi-specialist-review | no |  | User-triggered multi-agent code review. Spawns 3-5 parallel specialist sub-agents that rea |
| claude-cortex | owasp-top-10 | no |  | OWASP Top 10 security vulnerabilities with detection and remediation patterns. Use when co |
| claude-cortex | secure-coding-practices | yes |  | Secure coding practices and defensive programming patterns for building security-first app |
| claude-cortex | security-testing-patterns | yes |  | Security testing patterns including SAST, DAST, penetration testing, and vulnerability ass |
| claude-cortex | threat-modeling-techniques | yes |  | Threat modeling methodologies using STRIDE, attack trees, and risk assessment for proactiv |
| claude-cortex | typescript-advanced-patterns | no |  | Advanced TypeScript patterns for type-safe, maintainable code using sophisticated type sys |
| claude-cortex | using-git-worktrees | no |  | Use when starting feature work that needs isolation from current workspace or before execu |
| claude-cortex | vibe-security | no |  | Comprehensive secure coding guide covering OWASP web vulnerabilities with prevention patte |
| claude-cortex | wiring-audit | no |  | User-triggered audit that finds wiring drift between a project's UI surfaces and backend c |
| claude-cortex | workflow-security-audit | no |  | Comprehensive security assessment and remediation. Use for security reviews, compliance ch |
| ecc | dart-flutter-patterns | no | codex-cortex | Production-ready Dart and Flutter patterns covering null safety, immutable state, async co |
| ecc | defi-amm-security | no | codex-cortex | Security checklist for Solidity AMM contracts, liquidity pools, and swap flows. Covers ree |
| ecc | django-security | no | codex-cortex | Django security best practices, authentication, authorization, CSRF protection, SQL inject |
| ecc | django-verification | no | repo-worker-base | Verification loop for Django projects: migrations, linting, tests with coverage, security  |
| ecc | docker-patterns | no | codex-cortex | Docker and Docker Compose patterns for local development, container security, networking,  |
| ecc | enterprise-agent-ops | no | codex-cortex | Operate long-lived agent workloads with observability, security boundaries, and lifecycle  |
| ecc | fastapi-patterns | no | codex-cortex | FastAPI best practices covering project structure, Pydantic v2 schemas, dependency injecti |
| ecc | flutter-dart-code-review | no | codex-cortex | Library-agnostic Flutter/Dart code review checklist covering widget best practices, state  |
| ecc | github-ops | no | repo-worker-base | GitHub repository operations, automation, and management. Issue triage, PR management, CI/ |
| ecc | healthcare-emr-patterns | no | superpowers | EMR/EHR development patterns for healthcare applications. Clinical safety, encounter workf |
| ecc | healthcare-eval-harness | no | codex-cortex | Patient safety evaluation harness for healthcare application deployments. Automated test s |
| ecc | hipaa-compliance | no | codex-cortex | HIPAA-specific entrypoint for healthcare privacy and security work. Use when a task is exp |
| ecc | intent-driven-development | no | codex-cortex | Turn ambiguous or high-impact product and engineering changes into scoped, verifiable acce |
| ecc | inventory-demand-planning | no | future-domain-pack | Codified expertise for demand forecasting, safety stock optimization, replenishment planni |
| ecc | kotlin-ktor-patterns | no | codex-cortex | Ktor server patterns including routing DSL, plugins, authentication, Koin DI, kotlinx.seri |
| ecc | kotlin-patterns | no | future-domain-pack | Idiomatic Kotlin patterns, best practices, and conventions for building robust, efficient, |
| ecc | laravel-security | no | codex-cortex | Laravel security best practices — authentication, authorization, Eloquent safety, CSRF, XS |
| ecc | laravel-tdd | no | codex-cortex | Laravel testing strategies with PHPUnit, Pest, model factories, HTTP tests, Sanctum authen |
| ecc | laravel-verification | no | repo-worker-base | Verification loop for Laravel projects: env checks, linting, static analysis, tests with c |
| ecc | llm-trading-agent-security | no | codex-cortex | Security patterns for autonomous trading agents with wallet or transaction authority. Cove |
| ecc | mle-workflow | no | codex-cortex | Production machine-learning engineering workflow for data contracts, reproducible training |
| ecc | motion-foundations | no | future-domain-pack | Motion tokens, spring presets, performance rules, device adaptation, accessibility enforce |
| ecc | network-config-validation | no | codex-cortex | Pre-deployment checks for router and switch configuration, including dangerous commands, d |
| ecc | nuxt4-patterns | no | future-domain-pack | Nuxt 4 app patterns for hydration safety, performance, route rules, lazy loading, and SSR- |
| ecc | perl-security | no | codex-cortex | Comprehensive Perl security covering taint mode, input validation, safe process execution, |
| ecc | postgres-patterns | no | codex-cortex | PostgreSQL database patterns for query optimization, schema design, indexing, and security |
| ecc | prediction-market-risk-review | no | codex-cortex | Review prediction-market, basket, oracle, and trading-agent workflows for compliance, safe |
| ecc | quarkus-security | no | codex-cortex | Quarkus Security best practices for authentication, authorization, JWT/OIDC, RBAC, input v |
| ecc | quarkus-verification | no | repo-worker-base | Verification loop for Quarkus projects: build, static analysis, tests with coverage, secur |
| ecc | returns-reverse-logistics | no | future-domain-pack | Codified expertise for returns authorization, receipt and inspection, disposition decision |
| ecc | safety-guard | yes | superpowers | Use this skill to prevent destructive operations when working on production systems or run |
| ecc | security-bounty-hunter | no | repo-worker-base | Hunt for exploitable, bounty-worthy security issues in repositories. Focuses on remotely r |
| ecc | security-review | yes | codex-cortex | Use this skill when adding authentication, handling user input, working with secrets, crea |
| ecc | security-scan | no | repo-worker-base | Scan your Claude Code configuration (.claude/ directory) for security vulnerabilities, mis |
| ecc | springboot-security | no | codex-cortex | Spring Security best practices for authn/authz, validation, CSRF, secrets, headers, rate l |
| ecc | springboot-verification | no | repo-worker-base | Verification loop for Spring Boot projects: build, static analysis, tests with coverage, s |

## skills-meta

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| ecc | skill-scout | no | repo-worker-base | Search existing local, marketplace, GitHub, and web skill sources before creating a new sk |

## testing-qa

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | agent-loops | no |  | Complete operational workflow for implementer agents (Codex, Gemini, etc.) making code cha |
| claude-cortex | codex-code-review | no |  | Automate code review remediation loops with the codex CLI. Requests reviews from codex, cl |
| claude-cortex | dataset-curator | no |  | Use this skill when designing, cleaning, deduplicating, or documenting datasets for model  |
| claude-cortex | doc-claim-validator | no |  | Validate that claims in documentation match codebase reality. Extracts verifiable assertio |
| claude-cortex | doc-maintenance | no |  | Systematic documentation audit and maintenance. This skill should be used when documentati |
| claude-cortex | doc-quality-review | no |  | Assess documentation quality across readability, consistency, audience fit, and prose clar |
| claude-cortex | evaluator-optimizer | no |  | Iterative refinement workflow for polishing code, documentation, or designs through system |
| claude-cortex | git-ops | no |  | Use when performing git operations or generating smart commit messages - provides safe git |
| claude-cortex | implementation-workflow | no |  | Use when turning PRDs or feature specs into actionable implementation workflows - provides |
| claude-cortex | justfile-author | no |  | Use this skill when authoring or refactoring a justfile (and matching Makefile wrapper) fo |
| claude-cortex | prompt-engineering | no |  | Optimize prompts for LLMs and AI systems with structured techniques, evaluation patterns,  |
| claude-cortex | quality-audit | no |  | Meta-skill for auditing and validating skill quality. Use when reviewing skills for consis |
| claude-cortex | regex-master | no |  | Use this skill when building, explaining, or debugging regular expressions for pattern mat |
| claude-cortex | release-prep | yes |  | Use when preparing a production release or release candidate - provides a checklist-driven |
| claude-cortex | repo-cleanup | no |  | Use when a repository needs cleanup of dead code, build artifacts, unused dependencies, ou |
| claude-cortex | subagent-driven-development | no |  | Use when executing implementation plans with independent tasks in the current session - di |
| claude-cortex | systematic-debugging | no |  | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixe |
| claude-cortex | template-skill-enhanced | no |  | Enhanced skill template with progressive disclosure, bundled resources, and quality rubric |
| claude-cortex | test-driven-development | no |  | Use when implementing any feature or bugfix, before writing implementation code - write th |
| claude-cortex | test-generation | no |  | Use when generating tests for new or existing code to improve coverage - provides a struct |
| claude-cortex | test-review | no |  | Review test quality and audit test coverage for any module. This skill should be used when |
| claude-cortex | testing-anti-patterns | no |  | Use when writing or changing tests, adding mocks, or tempted to add test-only methods to p |
| claude-cortex | testing-skills-with-subagents | no |  | Use when creating or editing skills, before deployment, to verify they work under pressure |
| claude-cortex | ux-researcher | no |  | Use this skill when planning or conducting user research, writing interview guides, design |
| claude-cortex | verification-before-completion | no |  | Use when about to claim work is complete, fixed, or passing, before committing or creating |
| claude-cortex | writing-skills | no |  | Use when creating new skills, editing existing skills, or verifying skills work before dep |
| ecc | benchmark | no | codex-cortex | Use this skill to measure performance baselines, detect regressions before/after PRs, and  |
| ecc | benchmark-optimization-loop | no | codex-cortex | Use when the user asks to make something faster, try many variants, run recursive optimiza |
| ecc | codehealth-mcp | no | codex-cortex | Real-time structural Code Health via CodeScene MCP — review before edits, verify score del |
| ecc | competitive-platform-analysis | no | future-domain-pack | Use when scoping a competitive landscape — identifying, categorising, and score-filtering  |
| ecc | competitive-report-structure | no | repo-worker-base | Use after benchmark-methodology has produced scored competitor profile cards. Assembles fi |
| ecc | continuous-agent-loop | yes | codex-cortex | Patterns for continuous autonomous agent loops with quality gates, evals, and recovery con |
| ecc | e2e-testing | no | codex-cortex | Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, arti |
| ecc | eval-harness | no | codex-cortex | Formal evaluation framework for Claude Code sessions implementing eval-driven development  |
| ecc | gan-style-harness | no | codex-cortex | GAN-inspired Generator-Evaluator agent harness for building high-quality applications auto |
| ecc | gateguard | no | codex-cortex | Fact-forcing gate that blocks Edit/Write/Bash (including MultiEdit) and demands concrete i |
| ecc | orch-fix-defect | no | codex-cortex | Orchestrate fixing a bug — reproduce it as a failing regression test, fix to green, review |
| ecc | perl-testing | no | codex-cortex | Perl testing patterns using Test2::V0, Test::More, prove runner, mocking, coverage with De |
| ecc | plankton-code-quality | no | codex-cortex | Write-time code quality enforcement using Plankton — auto-formatting, linting, and Claude- |
| ecc | product-lens | no | codex-cortex | Use this skill to validate the "why" before building, run product diagnostics, and pressur |
| ecc | prompt-optimizer | no | codex-cortex | Analyze raw prompts, identify intent and gaps, match ECC components (skills/commands/agent |
| ecc | quality-nonconformance | no | codex-cortex | Codified expertise for quality control, non-conformance investigation, root cause analysis |
| ecc | ralphinho-rfc-pipeline | no | codex-cortex | RFC-driven multi-agent DAG execution pattern with quality gates, merge queues, and work un |
| ecc | scientific-thinking-scholar-evaluation | no | codex-cortex | Structured scholarly-work evaluation for papers, proposals, literature reviews, methods se |
| ecc | skill-stocktake | no | repo-worker-base | Use when auditing Claude skills and commands for quality. Supports Quick Scan (changed ski |
| ecc | swift-protocol-di-testing | no | codex-cortex | Protocol-based dependency injection for testable Swift code — mock file system, network, a |
| ecc | tdd-workflow | no | codex-cortex | Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test- |
| ecc | windows-desktop-e2e | no | codex-cortex | E2E testing for Windows native desktop apps (WPF, WinForms, Win32/MFC, Qt) using pywinauto |

## web-frontend

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | accessibility-audit | no |  | Fast, high-signal accessibility triage for pages, components, or PRs targeting WCAG 2.2 AA |
| claude-cortex | canvas-design | no |  | Create beautiful visual art in .png and .pdf documents using design philosophy. Use when t |
| claude-cortex | color-palette | no |  | Use this skill when creating, evaluating, or documenting color palettes for brands, produc |
| claude-cortex | dashboard-designer | no |  | Use this skill when designing a data dashboard—choosing KPIs, structuring layout, applying |
| claude-cortex | design-system-architecture | no |  | Build scalable design systems with design tokens, component APIs, and documentation. Use w |
| claude-cortex | frontend-design | no |  | Use this skill when specifying, designing, or documenting UI components, layouts, and desi |
| claude-cortex | interaction-design | yes |  | User flow design, micro-interactions, and interface behavior patterns with state managemen |
| claude-cortex | mapping-suite | no |  | User-triggered orchestrator that walks the user through running multiple sibling mapping/a |
| claude-cortex | playwright-cli | no |  | Automates browser interactions for web testing, form filling, screenshots, and data extrac |
| claude-cortex | super-saiyan | no |  | Maximum visual excellence for any UI platform. Use when building user interfaces, styling  |
| claude-cortex | system-design | no |  | Use when designing system architecture, APIs, components, or data models - provides a stru |
| claude-cortex | ui-design-aesthetics | no |  | Generates high-quality, non-generic UI designs with a focus on performance, progressive di |
| claude-cortex | ux-review | yes |  | Multi-perspective UX review combining usability heuristics, WCAG accessibility checks, and |
| claude-cortex | visual-modes | no |  | Use when activating visual showcase modes (supersaiyan, kamehameha, over9000) for UI or in |
| claude-cortex | webapp-testing | yes |  | Toolkit for interacting with and testing local web applications using Playwright. Use when |
| ecc | benchmark-methodology | no | codex-cortex | Use after competitive-platform-analysis has produced a tiered competitor set. Scores each  |
| ecc | browser-qa | no | codex-cortex | Use this skill to automate visual testing and UI interaction verification using browser au |
| ecc | coding-standards | no | codex-cortex | Baseline cross-project coding conventions for naming, readability, immutability, and code- |
| ecc | design-system | no | codex-cortex | Use this skill to generate or audit design systems, check visual consistency, and review P |
| ecc | frontend-design-direction | no | future-domain-pack | Set an ECC-specific frontend design direction for production UI work. Use when building or |
| ecc | frontend-slides | no | future-domain-pack | Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoin |
| ecc | healthcare-cdss-patterns | no | superpowers | Clinical Decision Support System (CDSS) development patterns. Drug interaction checking, d |
| ecc | make-interfaces-feel-better | no | codex-cortex | Apply concrete design-engineering details that make interfaces feel polished. Use when rev |
| ecc | nutrient-document-processing | no | future-domain-pack | Process, convert, OCR, extract, redact, sign, and fill documents using the Nutrient DWS AP |
| ecc | production-scheduling | no | future-domain-pack | Codified expertise for production scheduling, job sequencing, line balancing, changeover o |
| ecc | repo-scan | no | repo-worker-base | Cross-stack source code asset audit — classifies every file, detects embedded third-party  |
| ecc | taste | no | superpowers | A creative-direction (taste) layer for music videos and short-form edits in the angelcore  |
| ecc | videodb | no | future-domain-pack | See, Understand, Act on video and audio. See- ingest from local files, URLs, RTSP/live fee |

## writing-docs

| family | name | projected | future lane | description |
|--------|------|-----------|-------------|-------------|
| claude-cortex | blog-post | no |  | Use this skill when writing blog posts, articles, or long-form web content—from quick how- |
| claude-cortex | design-critiquer | no |  | Use this skill when reviewing, evaluating, or giving structured feedback on UI designs, wi |
| claude-cortex | doc-completeness-audit | no |  | Audit documentation completeness by mapping what a doc set should cover against what it ac |
| claude-cortex | email-drafter | no |  | Use this skill when drafting professional or personal emails—cold outreach, follow-ups, in |
| claude-cortex | market-researcher | no |  | Use this skill when sizing a market, analyzing competitors, designing customer surveys, se |
| claude-cortex | proofreader | no |  | Use this skill when reviewing written content for grammar, spelling, punctuation, style co |
| claude-cortex | storyteller | no |  | Use this skill when writing fiction, narrative nonfiction, brand stories, or any content w |
| claude-cortex | tutorial-design | no |  | Design and write hands-on tutorials with progressive disclosure, exercises, and troublesho |
| claude-cortex | writing-plans | no |  | Structured plan-writing skill adapted from obra/superpowers. Produces actionable plans tha |
| ecc | article-writing | no | future-domain-pack | Write articles, guides, blog posts, tutorials, newsletter issues, and other long-form cont |
| ecc | brand-voice | no | superpowers | Build a source-derived writing style profile from real posts, essays, launch notes, docs,  |
| ecc | customs-trade-compliance | no | future-domain-pack | Codified expertise for customs documentation, tariff classification, duty optimization, re |
| ecc | email-ops | no | codex-cortex | Evidence-first mailbox triage, drafting, send verification, and sent-mail-safe follow-up w |
| ecc | google-workspace-ops | no | repo-worker-base | Operate across Google Drive, Docs, Sheets, and Slides as one workflow surface for plans, t |
| ecc | ui-demo | no | superpowers | Record polished UI demo videos using Playwright. Use when the user asks to create a demo,  |
