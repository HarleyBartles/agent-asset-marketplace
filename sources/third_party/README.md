# third_party

Retained third-party source custody lives here.

The expected custody shape is the upstream skill tree only. Keep the retained
third-party root as small as possible, and move or drop non-skill upstream
scaffolding unless a projection surface or validation rule explicitly depends
on it.

Keep each retained plugin or package in its own root under this directory, with
upstream snapshots, patches, normalized copies, and custody notes separated
from the installable marketplace projections under `codex-marketplace/`.

Current retained roots include `unslop/`, `superpowers/`, and `feature-sliced/`.
