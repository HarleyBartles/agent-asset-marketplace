# Metadata and admin surfaces

Use this when the task is about Linear-owned taxonomy, workspace structure, or status metadata.

## Tools

| Tool | Use when | Required params | Optional params |
| --- | --- | --- | --- |
| `_list_teams` | Find workspace teams. | None | `createdAt`, `cursor`, `includeArchived`, `limit`, `orderBy`, `query`, `updatedAt` |
| `_get_team` | Resolve one team by key, UUID, or name. | `query` | None |
| `_list_users` | Find users in the workspace. | None | `cursor`, `limit`, `orderBy`, `query`, `team` |
| `_list_issue_labels` | Inspect issue labels, optionally scoped to a team. | None | `cursor`, `limit`, `name`, `orderBy`, `team` |
| `_list_project_labels` | Inspect project labels. | None | `cursor`, `limit`, `name`, `orderBy` |
| `_create_issue_label` | Create a new issue label. | `name` | `color`, `description`, `isGroup`, `parent`, `teamId` |
| `_list_issue_statuses` | Inspect issue statuses for a team. | `team` | None |
| `_list_cycles` | Inspect cycles for a team. | `teamId` | `type` |
| `_list_milestones` | Inspect milestones for a project. | `project` | None |
| `_get_status_updates` | Read project or initiative status updates. | `type` | `createdAt`, `cursor`, `id`, `includeArchived`, `initiative`, `limit`, `orderBy`, `project`, `updatedAt`, `user` |
| `_save_status_update` | Create or update a project or initiative status update. | `type` | `body`, `health`, `id`, `initiative`, `isDiffHidden`, `project` |
| `_list_customers` | Inspect customers in the workspace. | None | `createdAt`, `cursor`, `includeArchived`, `includeNeeds`, `limit`, `orderBy`, `owner`, `query`, `status`, `tier`, `updatedAt` |

## Notes

- Use the team key or verified team UUID when a team-scoped read is picky.
- Use `list_*` tools for discovery, then switch to the matching `save_*` tool when you need to mutate.
- Project status update work belongs here because it is project/initiative metadata, not issue body content.

