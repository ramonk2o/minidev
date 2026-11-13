# Setup's commit

Where setup's commit goes and how it reaches the main branch. It holds only setup's changes: the user's own work, and the main branch's history, stay apart from it. `git-flow.md` below is the `build` skill's `references/git-flow.md` (`../../build/references/git-flow.md` from this file).

## Before writing (steps 2 and 3)

In step 2, in a repository with commits, note where the session stands: the current branch and whether it's the main branch (`git-flow.md`, The main branch), uncommitted changes (`git status`), whether the main branch is behind the remote, and `git worktree list`.

Add to step 3's round, when step 2 found them:
- **Uncommitted changes:** they're someone's work. Ask the user to commit them on a branch of their own or stash them, themselves, before setup writes anything; setup doesn't move them. Committed on the main branch, they'd ride along in setup's pull request or squash. If the user wants neither, stop: setup can't keep its commit apart from them.
- **The session's branch,** when it isn't the main branch, has no commits of its own beyond it and nothing uncommitted (often a worktree the app made): whether setup may use it as its branch (`git-flow.md`, Worktrees). A branch with commits of its own isn't used: they'd ride along.

## Where it goes (step 9.1)

A new repository's first commit goes on the main branch. Otherwise it goes on the main branch, brought up to date (`git-flow.md`, The main branch), unless the main branch only takes pull requests (either pull request mode, with the main branch on the remote) or the session is on another branch. Then start a `chore/minidev-setup` branch as `git-flow.md` says (Start the branch, Worktrees, with step 3's answer), and write everything there.

## Bring it in (step 9.3)

- **On the main branch:** commit there. Push only when setup just created the remote, as `references/remote.md` says.
- **On `chore/minidev-setup`, with the main branch on the remote in either pull request mode:** commit there and bring it in as `git-flow.md` says (Merge and push), with setup's message as its final message, the push and the pull request each on the user's OK.
- **On `chore/minidev-setup` otherwise:** `git-flow.md`'s Local merge, steps 2 to 5 and 7, with setup's message as the final message. Step 1 runs only when the remote has the main branch. Step 6 doesn't run: setup doesn't push the main branch, except as `references/remote.md` says when it just created the remote.
