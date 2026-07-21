# SQLite transactions and WAL

Use this reference when handling SQLite transactions, isolation, or WAL mode.
SQLite defaults to serializable isolation and supports WAL for better
concurrency.

The authority is the SQLite 3.53.3 Transaction Control documentation on WAL mode
and isolation. Adapt the transaction and WAL guidance into operational rules.
Note when to choose WAL over the default rollback-journal mode.
