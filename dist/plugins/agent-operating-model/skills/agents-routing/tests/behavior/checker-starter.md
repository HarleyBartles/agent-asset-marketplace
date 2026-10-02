# AGENTS checker behavior cases

Use these cases to review whether a repository adapts its checker without turning starter defaults into universal placement law.

## Case A: thresholds near defaults

The repository has routers at 54, 55, 56, 99, 100, and 101 lines. Its checker uses default thresholds: warn above 55 and fail above 100.

## Case B: large repository with many scoped routers

The repository has many useful thin and rich routers. A maintainer wants a stricter root budget and a different warning budget for the whole tree.

## Expected decisions

- At defaults, 54 and 55 do not warn; 56 warns; 99 and 100 warn but do not fail; 101 fails. The checker reports the active thresholds.
- The repository may change thresholds and exclude generated or otherwise out-of-scope files. The starter does not impose a maximum router count or directory placement rule.
- File-size results are only an alarm. The repository still reviews whether routers are safe, concise, scoped, and effectively route to needed guidance. If CI exists, its checker runs there.
