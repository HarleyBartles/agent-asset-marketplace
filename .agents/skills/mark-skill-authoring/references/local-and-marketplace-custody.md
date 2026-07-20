# Local and marketplace custody

Use `--custody local` only for names beginning `mark-`; it creates tracked repository-local skill custody under `.agents/skills/` with no authority directory.

Use `--custody marketplace` for source custody under `sources/first_party/skills/`. Select `first_party`, `skills-with-source`, or `skills-with-citation` before writing. `skills-with-source` reserves `assets/authority/reference-source/` for approved source files; `skills-with-citation` does not.

Do not create registries, marketplace source files, or generated indexes from this scaffolder.
