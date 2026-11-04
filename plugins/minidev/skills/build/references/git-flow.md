# Git flow

How a feature, a fix or a chore gets its own branch and how that branch reaches the main branch. Used by the `build` skill (branch `feature/<short-name>`), the `fix` skill (branch `fix/<short-name>`), the `chore` skill (branch `chore/<short-name>`) and releases in pull request mode (branch `release/<version>`).

The branch may have as many commits as the work needs; the main branch gets **one squashed commit** per branch, whose message records the verification. So the branch's history is a working log, and the main branch's history is the record.

## Integration mode

The project's CLAUDE.md says how branches reach the main branch, in its Development cycle section:
- **Local merge** (the default, when it says nothing): the branch is squashed into the main branch locally, tested there and pushed.
- **Pull requests:** the branch is pushed, a pull request is opened, and it's squash-merged on GitHub once the user confirms and the checks pass. For repositories with a protected main branch, CI or more than one person. Needs `gh`, signed in (`gh auth status`).

## The main branch

If the repository has a remote, it's the remote's default branch: `git symbolic-ref --short refs/remotes/origin/HEAD`, without the `origin/` prefix. Otherwise it's `main` or `master`, whichever exists. Project instructions that name another branch win.

## Start the branch

From the main branch, brought up to date (`git pull --ff-only` if it has a remote) and with a clean working tree, run `git switch -c <branch>`. All the work happens there, so the main branch only ever receives finished, verified work.

- If there are uncommitted changes on the main branch, ask the user what to do with them first.
- If the work is already on this branch (e.g. resuming), stay on it.
- If another branch's work is under way (e.g. a bug fix in the middle of a feature), commit it there as a checkpoint, switch to the main branch and start from it. Go back later with `git switch <branch>`.

## Stage the work

Before staging, run `git status --short` and read the list: only this work's files should be there. Anything that shouldn't be committed (build output, local reports, secrets like `.env`) goes into `.gitignore`, or ask the user about it. Then stage with `git add -A`.

## Checkpoints

Commit on the branch whenever a step is done and before stopping, staged as above, with a message starting `wip:` (e.g. `wip: tests for empty cart, failing`). Checkpoints let the work be resumed in a new session and keep a working state to go back to. They're never pushed to the main branch: the squash replaces them.

## The verification commit

When the work is verified, the skill makes the branch's last commit with the verification message (the skill says what goes in it). If fixes come after it (e.g. from checking by hand), commit them as checkpoints.

The main branch gets the **final message**: the verification message (`git log -1 --format=%B <branch>` if it's still the last commit; otherwise find it in `git log <main branch>..<branch>`), plus a line for each fix made after it, plus a line for each document change made on the branch that isn't part of the work (e.g. an idea recorded meanwhile).

## Merge and push

Once the user confirms everything works (or right after the verification commit, if there's nothing to check by hand), follow the project's integration mode.

**Local merge:** the main branch only ever receives code that was already tested combined with it, so a failure is fixed on the branch, never on the main branch.
1. If the repository has a remote, bring the main branch up to date: `git switch <main branch>`, `git pull --ff-only`, `git switch <branch>`.
2. On the branch, `git merge <main branch>` (the squash flattens this merge). If it has conflicts, stop and show them instead of resolving them on your own.
3. Run the test suite and the build on the branch. If the main branch moved since the branch started, this is the first time the combined code runs. If anything fails, fix it on the branch (test first when it can be reproduced in one), commit it as a checkpoint and run them again. Tell the user what broke and how it was fixed, and add a line for it to the final message.
4. Switch to the main branch, `git merge --squash <branch>` and commit with the final message.
5. Run the test suite and the build once more, as a confirmation. If anything fails now, the commit hasn't left this machine: undo only that commit with `git reset --hard HEAD~1` (the working tree is clean, so nothing else is lost), switch back to the branch and show the user; continue from step 3.
6. Delete the branch with `git branch -D <branch>` (git doesn't see a squashed branch as merged, so `-d` refuses), and push the main branch if the repository has a remote.

**Pull requests:**
1. Push the branch: `git push -u origin <branch>`.
2. Open the pull request with `gh pr create --base <main branch> --head <branch>`, its title the final message's first line and its body the rest. If one is already open for the branch, update it instead (`gh pr edit`). Give the user its link.
3. Wait for the checks: `gh pr checks --watch`. A failing check is fixed on the branch, committed, pushed, and waited for again. If the repository has no checks, bring the main branch into the branch (`git fetch origin`, `git merge origin/<main branch>`; the squash flattens this merge too), run the test suite and the build, and push.
4. If the main branch requires a review, stop: tell the user the pull request is waiting for one.
5. Before merging, check that every commit the local main branch has is in the branch (`git merge-base --is-ancestor <main branch> <branch>`); if not, stop and show the user which commits are missing. Then merge with `gh pr merge --squash --subject "<first line>" --body "<rest>"`, from the final message as it stands now.
6. Update the local main branch: `git switch <main branch>`, `git fetch origin`. If the local main branch had commits not on the remote (document changes made on it before the branch started), they're now inside the squashed commit, as step 5 checked: `git reset --hard origin/<main branch>`. Otherwise `git pull --ff-only`.
7. Delete the local branch with `git branch -D <branch>`, and the remote one with `git push origin --delete <branch>` if GitHub didn't.

## When a merged change breaks

If a change that already reached the main branch on the remote turns out broken, show the user two ways and let them choose:
- **Fix forward** with the `fix` skill, when the cause is clear and the fix is small.
- **Revert** when the breakage hurts users now, or the cause isn't clear. Each branch reached the main branch as one commit, so reverting it removes the whole change at once: start a `fix/revert-<short-name>` branch as above, run `git revert --no-edit <sha>`, run the test suite and the build, and bring it in like any other branch. The revert also undoes what the change's commit wrote in BACKLOG.md, SPEC.md and CHANGELOG.md: the SPEC rules go, a feature's entry (or a fix's Bug entry) comes back as it was on the main branch before, and its changelog line goes. Then, with the `document` skill: if the change was already in a released version, put its line back in that version (released history isn't rewritten) and record the revert under `[Unreleased]` (Removed for a feature, Fixed for a fix); add what went wrong to the restored entry's Open questions. A reverted feature is built again later through `build`, from that entry.

Never rewrite the main branch's history once it's on the remote (no `reset` or force-push there): a revert is a new commit everyone can see.
