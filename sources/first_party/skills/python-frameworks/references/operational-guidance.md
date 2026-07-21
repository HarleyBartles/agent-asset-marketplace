# Python Frameworks operational guidance

## When to apply

Use when the Python Frameworks skill loaded and the question is deeper than a single sentence:
- choosing a web framework,
- structuring Django apps or FastAPI services,
- designing Celery tasks,
- testing framework boundaries.

## Django patterns

- Keep apps small and focused; each app owns models, views, templates, and tests.
- Use class-based views for CRUD and function-based views for one-off behavior.
- Prefer QuerySet optimization (`select_related`, `prefetch_related`) over raw SQL.
- Write tests with Django's test client and factories; use `setUpTestData` for shared state.

## FastAPI patterns

- Define request/response contracts with Pydantic models and dependency injection.
- Use async route handlers for I/O-bound endpoints; run blocking calls in `loop.run_in_executor`.
- Mount sub-routers by domain and version the API path (`/api/v1/...`).
- Test with `TestClient` against the `FastAPI` app instance.

## Celery patterns

- Design tasks as idempotent functions with clear inputs and outputs.
- Set `max_retries`, `default_retry_delay`, and `autoretry_for` for transient failures.
- Use chains and groups for workflows; avoid long chains by calling helper tasks directly when simpler.
- Monitor workers with Flower or broker metrics; keep result backend TTLs short.

## Choosing a framework

- Django when you need an ORM, admin, form handling, or server-rendered pages.
- FastAPI when the surface is HTTP APIs with async I/O and OpenAPI contracts.
- Celery when work must run outside the request cycle; it pairs with either web framework.

## Related references

- Django docs: https://docs.djangoproject.com/en/stable/
- FastAPI docs: https://fastapi.tiangolo.com/
- Celery docs: https://docs.celeryq.dev/en/stable/
