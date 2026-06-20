# Reference: CQRS Patterns

CQRS works best when the write path and read path solve different problems.

## Command Side

- Commands express intent.
- Commands should be validated before aggregate mutation.
- Commands return success or failure, not read data.

## Query Side

- Queries should not mutate state.
- Read models can be denormalized for the specific question being answered.
- Query handlers can be cached independently of command handling.

## Architecture Notes

- Use aggregates as consistency boundaries.
- Use projections to shape the read model.
- Use IDs, not object graphs, to cross aggregate boundaries.

