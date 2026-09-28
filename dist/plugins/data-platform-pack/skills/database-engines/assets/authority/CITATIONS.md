# Authority record for database-engines

## Scholarly citation

- PostgreSQL 18.4 Documentation. https://www.postgresql.org/docs/18.4/ (accessed 2026-07-21). PostgreSQL License. Vendored snapshot: `assets/authority/reference-source/postgresql-docs/postgresql-18.4-docs.tar.gz`.
- SQLite 3.53.3 Documentation. https://sqlite.org/docs.html (accessed 2026-07-21). Public domain. Vendored snapshot: `assets/authority/reference-source/sqlite-docs/sqlite-doc-3530300.zip`.
- Microsoft SQL Server documentation. https://learn.microsoft.com/en-us/sql/ (accessed 2026-07-21). Proprietary; used as a selectable-option citation only.
- MySQL Reference Manual. https://dev.mysql.com/doc/refman/en/ (accessed 2026-07-21). Oracle proprietary; retained as a low-priority citation only for cases where MariaDB/MySQL semantics overlap with PostgreSQL.

## Derivation boundary

- Derived from vendored source: PostgreSQL connection/drivers, schema/data types, indexing, query patterns, transactions, backups, replication; SQLite connection/drivers, schema/data types, indexing, query patterns, transactions, backups, WAL.
- First-party synthesis: MS-SQL selectable guidance (T-SQL differences, tooling, Windows/Azure deployment notes) and MySQL overlap notes, supported only by the proprietary citations above.
- Outside scope: MySQL as a first-class engine; cloud-managed service operations beyond engine selection; NoSQL/document databases.

## Attribution

- PostgreSQL documentation is used under the PostgreSQL License.
- SQLite documentation is in the public domain.
- MS-SQL and MySQL citations are proprietary and are not vendored in this repository.

## Human review

- Reviewer: Harley Bartles
- Date: 2026-07-21
- Decision: Approved. Operational prose contains no inline citations; all source-grounded claims are recorded in `assets/authority/source-map.yaml`.
