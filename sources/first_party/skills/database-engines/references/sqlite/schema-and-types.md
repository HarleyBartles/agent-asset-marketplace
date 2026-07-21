# SQLite schema and data types

Use this reference when designing a SQLite schema or choosing storage classes.
SQLite's type system is dynamic; storage class affinity matters more than
declared type, but strict tables are available when stronger typing is needed.

The authority is the SQLite 3.53.3 SQL Language documentation on data types and
CREATE TABLE. Adapt the affinity and strict-table guidance into design rules.
Warn against assuming SQLite enforces declared types by default.
