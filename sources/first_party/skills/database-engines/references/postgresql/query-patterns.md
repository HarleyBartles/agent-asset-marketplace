# PostgreSQL query patterns

Use this reference when writing or optimizing PostgreSQL SELECT, JOIN, CTE, or
window-function queries. Start with the query's intent and the existing schema,
then inspect the plan before adding complexity.

The authority is the PostgreSQL 18.4 SQL Language chapter on queries. Adapt the
query-construction guidance into a pattern catalog. Avoid reproducing full
syntax diagrams; instead, give the shape of the common pattern and a short
example.
