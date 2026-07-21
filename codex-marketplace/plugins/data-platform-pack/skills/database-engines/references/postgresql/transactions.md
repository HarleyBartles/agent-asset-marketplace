# PostgreSQL transactions and concurrency

Use this reference when handling PostgreSQL transactions, isolation levels, or
concurrency problems. Start by choosing an isolation level that matches the
consistency requirement without overserializing work.

The authority is the PostgreSQL 18.4 SQL Language chapters on transaction
isolation and concurrency control. Adapt the isolation-level descriptions and
lock behavior into guidance on when to use each level and how to detect
deadlocks.
