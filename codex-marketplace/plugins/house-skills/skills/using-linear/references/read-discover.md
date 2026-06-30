# Read and discover

Use this when you want current Linear state without mutating anything.

## Pick the tool

| Tool | Use when | Required params | Optional params |
| --- | --- | --- | --- |
| `_search` | Natural-language or keyword search across issues, projects, initiatives, and documents. | `query` | `includeArchived`, `limit`, `type` |
| `_list_issues` | Structured issue lookup with filters. | None | `assignee`, `createdAt`, `cursor`, `cycle`, `delegate`, `includeArchived`, `label`, `limit`, `orderBy`, `parentId`, `priority`, `project`, `query`, `state`, `team`, `updatedAt` |
| `_list_projects` | Structured project lookup with filters. | None | `createdAt`, `cursor`, `includeArchived`, `includeMembers`, `includeMilestones`, `initiative`, `label`, `limit`, `member`, `orderBy`, `query`, `state`, `team`, `updatedAt` |
| `_list_documents` | Find documents by workspace, team, project, or initiative. | None | `createdAt`, `creatorId`, `cursor`, `includeArchived`, `initiativeId`, `limit`, `orderBy`, `projectId`, `query`, `teamId`, `updatedAt` |

## When to choose search

Use `_search` when the user gives you a phrase, a loose title, or a human description.
Use a list tool when you already know the filter shape and need reliable structure.

## Notes

- `limit` defaults are small; use pagination when the result set may be large.
- `includeArchived` is available on the list/search tools that expose it.
- If you need the exact current object before a write, read it by the smallest stable filter you have and then read back from that durable surface after the mutation.

