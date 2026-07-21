# SQLite indexing

Use this reference when creating or tuning SQLite indexes. SQLite's query
planner uses a cost model that differs from larger engines; small table changes
can shift plan choices.

The authority is the SQLite 3.53.3 Query Planning documentation on the
optimizer and indexes. Adapt the covering-index and query-optimization guidance
into practical rules. Emphasize running EXPLAIN QUERY PLAN before adding
indexes.
