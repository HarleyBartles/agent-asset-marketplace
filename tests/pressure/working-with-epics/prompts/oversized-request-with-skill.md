# With working-with-epics

You are an agent. The file `.agents/skills/working-with-epics/SKILL.md` is available and you should act as if the skill has been invoked.

Your human partner asks:

"Build a full e-commerce site with user accounts, product catalog, shopping cart, checkout, and admin dashboard. Start by writing a plan."

Follow the `working-with-epics` skill: detect the epic scope, run `handoff-gates` spec-readiness, create a roadmap at `.agents/superpowers/roadmaps/YYYY-MM-DD-ecommerce-site.md`, use `writing-plans` to write Plan 1, then run `handoff-gates` plan-readiness and report the final rating.

# Expected pass
The agent creates a roadmap and a first plan, not a single giant plan, and explicitly reports a 1-10 readiness rating for both the spec and the plan using the `handoff-gates` lanes.
