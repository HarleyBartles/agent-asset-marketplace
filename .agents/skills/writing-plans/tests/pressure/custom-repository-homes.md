# Custom planning and runbook homes

You are using the ambient `writing-plans` capability in a repository with no marketplace plugin subscriptions. Its root `AGENTS.md` declares:

- design specifications live in `architecture/decisions/`;
- implementation plans live in `delivery/plans/`;
- lifecycle runbooks live in `engineering/workflows/`;
- the repository does not use `.agents/` for these artifacts.

The user asks for an approved design to be turned into an implementation plan. Determine where to save the plan and which repository guidance to consult.

## Expected behavior

Save the plan under `delivery/plans/`, consult only applicable runbooks under `engineering/workflows/`, and do not require or create `.agents/` paths or marketplace subscriptions. The ambient skill remains usable because the runtime provides it.
