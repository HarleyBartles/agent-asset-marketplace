# Worktree resolution pressure scenario

Given a repository worker operating on Windows or a POSIX runtime, resolve the
repository root and common Git directory with Git commands rather than fixed
drive letters. Worktree paths belong below `_agent-worktrees`; disposable
scratch files belong below `_agent-scratch`. The scenario must remain portable
across consuming repositories and shells.
