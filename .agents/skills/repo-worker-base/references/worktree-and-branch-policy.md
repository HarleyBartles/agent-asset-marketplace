# Worktree and branch policy

## Read when

Read before repository work, worktree creation, branching, scratch use, a PR,
or publication decision.

## Portable location algorithm

Use this exact Git-derived algorithm. Future tooling must consume this
algorithm rather than independently walking filesystem parents.

~~~text
current_checkout = git rev-parse --show-toplevel
common_git = git rev-parse --git-common-dir
main_checkout = parent(resolve(current_checkout / common_git))
external_worktree_root = main_checkout / ".." / "_agent-worktrees" / repo_name
external_scratch_root = main_checkout / ".." / "_agent-scratch" / repo_name / branch_name
~~~

First run git rev-parse --show-superproject-working-tree. Any non-empty result
is a submodule: reject it unconditionally for this workflow. Do not allow a
shared-checkout override, inferred path, or fallback parent walk to bypass that
rejection.

## Worker boundary

Use a dedicated worktree and task branch unless the user explicitly authorizes
another route. Before mutation, record the checkout, branch, base commit, and
initial status; preserve pre-existing dirty state. Keep disposable artifacts
under external_scratch_root, never inside the repository. Scratch is external,
per-repository, per-branch, disposable, and never durable custody.

Fetch the required base, make a focused commit, push the branch, and open a PR
unless direct-main work is explicitly authorized. Local edits, test logs, and
commit hashes are not publication proof; GitHub-visible PR or authorized
direct-main evidence is.
