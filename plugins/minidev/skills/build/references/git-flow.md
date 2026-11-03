# Git flow

How a feature or a fix gets its own branch and how that branch reaches the main branch. Used by the `build` skill (branch `feature/<short-name>`) and the `fix` skill (branch `fix/<short-name>`).

## The main branch

If the repository has a remote, it's the remote's default branch: `git symbolic-ref --short refs/remotes/origin/HEAD`, without the `origin/` prefix. Otherwise it's `main` or `master`, whichever exists. Project instructions that name another branch win.

## Start the branch

From the main branch, brought up to date (`git pull --ff-only` if it has a remote) and with a clean working tree, run `git switch -c <branch>`. All the work and its commit happen there, so the main branch only ever receives finished, verified work.

- If there are uncommitted changes, ask the user what to do with them first.
- If the work is already on this branch (e.g. resuming), stay on it.

## Stage the work

Before staging, run `git status --short` and read the list: only this work's files should be there. Anything that shouldn't be committed (build output, local reports, secrets like `.env`) goes into `.gitignore`, or ask the user about it. Then stage with `git add -A`.

## Merge and push

Once the user confirms everything works (or right after the commit, if there's nothing to check by hand):

1. Switch to the main branch and bring it up to date (`git pull --ff-only` if it has a remote).
2. `git merge <branch>`. If the merge has conflicts, stop and show them instead of resolving them on your own.
3. Run the test suite and the build on the merged main branch. If the main branch moved since the branch started, this is the first time the combined code runs. If anything fails, don't push: show the user, and fix it as a bug.
4. Delete the branch with `git branch -d <branch>`, and push the main branch if the repository has a remote.
