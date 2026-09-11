# With writing-roadmaps

You are an agent. The file `.agents/skills/writing-roadmaps/SKILL.md` is available and you should act as if the skill has been invoked.

Your human partner asks:

"Build a full e-commerce site with user accounts, product catalog, shopping cart, checkout, and admin dashboard. Start by writing a plan."

Follow the `writing-roadmaps` skill: detect the epic scope, run `handoff-gates`
spec-readiness, create a roadmap at `.agents/plans/ecommerce-site/roadmap.md`,
use `writing-plans` to write Plan 1, then run `handoff-gates` plan-readiness and
report the current rating without storing it in the roadmap.

# Expected pass
The agent creates a roadmap and a first plan rather than one giant plan, and
hands off only after both readiness ratings meet the floor.
