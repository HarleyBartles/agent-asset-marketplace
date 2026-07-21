# PostgreSQL indexing

Use this reference when creating or tuning PostgreSQL indexes. Start by
identifying the query patterns and predicates the index must serve, then choose
an access method and index definition that matches them.

The authority is the PostgreSQL 18.4 SQL Language chapter on indexes. Adapt the
B-tree, hash, GiST, GIN, and BRIN descriptions into operational rules. Mention
partial and expression indexes only as targeted optimizations after the query
plan has been reviewed.
