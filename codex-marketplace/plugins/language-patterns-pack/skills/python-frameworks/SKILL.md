---
name: python-frameworks
description: Use when building, reviewing, or choosing Python web or task frameworks,
  and the task calls for Django, FastAPI, or Celery patterns.
metadata:
  source-id: python-frameworks
  source-path: sources/first_party/skills/python-frameworks/SKILL.md
  provenance-name: Python Frameworks first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when building, reviewing, or choosing Python web or task frameworks,
    and the task calls for Django, FastAPI, or Celery patterns.
  use_when:
  - Use when building or reviewing Django applications.
  - Use when designing FastAPI services.
  - Use when adding Celery task queues.
  - Use when choosing between Django, FastAPI, and Celery for a component.
  do_not_use_when:
  - Do not use when the question is about pure Python language patterns (see python).
  - Do not use when another framework-specific skill owns the task.
  related_skills:
  - python
  - typescript
  - database-engines
license: MIT
---

# Python Frameworks

Use this skill when choosing or applying Python web and task-queue frameworks.

## When to Use

- Building or reviewing Django applications.
- Designing FastAPI APIs and services.
- Adding Celery background tasks or scheduled jobs.
- Choosing among Django, FastAPI, and Celery for a component.

## Core Pattern

1. Choose Django for full-stack server-rendered or admin-heavy applications that need an ORM, migrations, and batteries-included conventions.
2. Choose FastAPI for API-first services that benefit from async endpoints, automatic OpenAPI docs, and Pydantic validation.
3. Use Celery to offload work to background workers when the response path must stay fast; broker with Redis or RabbitMQ and use result backends only when callers need results.
4. Keep framework code decoupled from business rules; put domain logic in services, models, or repositories and call it from views or tasks.
5. Test at the framework boundary with the FastAPI `TestClient` or Django test client; unit-test domain logic without loading the framework.

## Common Mistakes

- Putting business logic directly in views or tasks. → Move it to services or domain modules.
- Using Celery for synchronous, latency-sensitive work. → Keep real-time work in the request path or use async APIs.
- Mixing sync and async ORM calls in FastAPI. → Use async engines and sessions or route sync calls through executors.
- Ignoring Django migrations in tests. → Run migrations and use fixtures that reflect schema state.

Load `references/operational-guidance.md` for deeper Django, FastAPI, and Celery patterns.
