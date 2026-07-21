---
name: database-engines
description: Use when choosing, connecting to, querying, or operating a relational
  database engine. Do not use when the task is database design theory, NoSQL, or
  engine-agnostic data modeling.
metadata:
  source-id: database-engines
  source-path: sources/first_party/skills/database-engines/SKILL.md
  provenance-name: Database Engines first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: First-party guidance for PostgreSQL, SQLite, and selective MS-SQL
  use_when:
  - Use when choosing or operating a relational SQL engine
  - Use when connecting drivers, managing schemas, writing queries, or tuning indexes
  - Use when the user names PostgreSQL, SQLite, or MS-SQL
  do_not_use_when:
  - Do not use for database design theory; prefer database-design-patterns
  - Do not use for NoSQL or document databases
  - Do not use for cloud-managed operational tasks beyond engine selection
license: MIT
---

# Database Engines

Use this skill when the work is tied to a specific relational engine. Ask which
engine the user is using, then route to the matching reference files. PostgreSQL
and SQLite are first-class; MS-SQL is available when the user explicitly selects
it. MySQL is out of scope.

## Engine selection

1. Ask the user which engine they are using.
2. If PostgreSQL, load `references/postgresql/*.md`.
3. If SQLite, load `references/sqlite/*.md`.
4. If MS-SQL, load `references/mssql/selectable-engine.md`.
5. If MySQL or another engine, decline and suggest the appropriate source.

## Shared SQL concepts

Read `references/operational-guidance.md` for cross-engine topics: connection
management, transactions, indexing principles, and backup strategies. Keep
engine-specific semantics in the engine-specific references.

## Common mistakes

- Treating PostgreSQL and SQLite as interchangeable.
- Applying MS-SQL T-SQL guidance to PostgreSQL or SQLite.
- Optimizing before checking the query plan or schema.
- Ignoring transaction isolation and locking behavior.

For source-grounded detail, read `assets/authority/CITATIONS.md` and
`assets/authority/source-map.yaml`.
