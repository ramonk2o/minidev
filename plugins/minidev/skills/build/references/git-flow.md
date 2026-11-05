# Git flow

How a feature, a fix or a chore (except a prose-only chore in local merge mode, `chore` skill) gets its own branch and how that branch reaches the main branch. Used by the `build` skill (branch `feature/<short-name>`), the `fix` skill (branch `fix/<short-name>`), the `chore` skill (branch `chore/<short-name>`) and releases in pull request mode (branch `release/<version>`).

The branch may have as many commits as the work needs; the main branch gets **one squashed commit** per branch, whose message records the verification. So the branch's history is a working log, and the main branch's history is the record.

## Integration mode

The project's CLAUDE.md says how branches reach the main branch, in its Development cycle section:
- **Local merge** (the default, when it says nothing): the branch is squashed into the main branch locally, tested there and pushed.
- **Pull requests:** the branch is pushed, a pull request is opened, and it's squash-merged on GitHub once the user confirms and the checks pass. For repositories with a protected main branch, CI or more than one person. Needs `gh`, signed in (`gh auth status`).

## The main branch

The remote is the one `git remote` lists (`origin` if there are several, unless project instructions name another); below it's `<remote>`. If the repository has a remote, the main branch is the remote's default branch: `git symbolic-ref --short refs/remotes/<remote>/HEAD`, without the `<remote>/` prefix. That ref is often missing (a repository created locally and pushed later); then ask the remote: `git ls-remote --symref <remote> HEAD`, and set it for next time with `git remote set-head <remote> --auto`. With no remote, it's `main` or `master`, whichever exists. Project instructions that name another branch (the CLAUDE.md's `Main branch:` line) win.

To bring it up to date, `git pull --ff-only`. If that refuses because the main branch has local commits the remote doesn't (document changes waiting for the next merge, like a feature set In progress), use `git pull --rebase`: it only replays those commits, which never left this machine. If the rebase stops on a conflict, run `git rebase --abort` (the main branch is back as it was) and show the user what conflicted.

## Worktrees

Check `git worktree list` once at the start. Git won't switch to a branch that's checked out in another worktree, so (both cases often hold at once, in a worktree the app made: apply both):

- **The session started on a branch that isn't the main branch** (e.g. a worktree the app made for it, with no commits of its own beyond the main branch): ask the user whether to use it as this work's branch. If yes, rename it to the work's name (`git branch -m <branch>`) and work there; the entry's In progress status, which would go on the main branch, goes in its first commit instead.
- **The main branch is checked out in another worktree:** don't switch to it. Start a branch from it with `git switch -c <branch> <main branch>`, and run the steps that act on the main branch (bringing it up to date, the squash, its tests, the push) in its worktree, with `git -C <its path>` and the commands run from that folder. If that worktree has uncommitted changes, stop and ask the user: they're someone's work in progress.

At the end, the branch can't be deleted while this worktree has it checked out: first `git switch --detach <main branch>` (after the squash, it's the tested state), then delete it. The next piece of work in the same session starts its own branch from there.

## Start the branch

First check whether this work already has a branch (Resume, below). Otherwise, from the main branch, brought up to date (The main branch, above, if it has a remote) and with a clean working tree, run `git switch -c <branch>`. All the work happens there, so the main branch only ever receives finished, verified work.

- If there are uncommitted changes on the main branch, ask the user what to do with them first.
- If the work is already on this branch, stay on it.
- If another branch's work is under way (e.g. a bug fix in the middle of a feature), commit it there as a checkpoint, switch to the main branch and start from it. Go back later with `git switch <branch>`.

## Resume

Work stopped in an earlier session lives on its branch; the main branch doesn't show how far it got. When the user asks to continue something, or before starting a branch for work that may have been started already:

1. List the work branches: `git branch --list 'feature/*' 'fix/*' 'chore/*' 'release/*'` and, if the repository has a remote, after `git fetch <remote>`, the ones only on it (`git branch -r --list '<remote>/feature/*'`, and so on; `git switch <branch>` creates the local one, tracking it). Also `git worktree list` (a branch checked out in another worktree is worked on there; tell the user and don't switch to it). In pull request mode, also `gh pr list --author @me`.
2. If one matches the work by name (or the user isn't sure which), show it and confirm. Ask before resuming work on a branch the user didn't name.
3. With a clean working tree (otherwise ask the user first), `git switch <branch>`. Read `git log --format='%h %s' <main branch>..<branch>`: the checkpoint messages say which steps are done, and their bodies hold what the next steps need (Checkpoints). Read the last checkpoint's diff and run the test suite to see where the work stands.
4. Tell the user where it stopped and continue from the next step of the skill. A step half done since the last checkpoint is redone from its start.
5. In pull request mode, if the branch has an open pull request, read its state (`gh pr view <branch>`): it may be waiting for checks or a review (Merge and push, steps 3 and 4).

A branch with no checkpoints beyond the main branch is resumed from the skill's first step on the branch. If no branch matches (it was deleted, or the work never got that far), start it as usual.

## Stage the work

Before staging, run `git status --short` and read the list: only this work's files should be there. Anything that shouldn't be committed (build output, local reports, secrets like `.env`) goes into `.gitignore`, or ask the user about it. Then stage with `git add -A`.

## Check after an agent

The `tester` and the `reviewer` are told not to touch the work or git state, but they have a shell. Before launching one, with the work staged, note `git rev-parse HEAD` and `git write-tree` (a hash of what is staged). When it returns:

1. **HEAD:** `git rev-parse HEAD` must be the same. If it moved, stop and show the user (`git log <noted HEAD>..HEAD`); undoing it (`git reset --soft <noted HEAD>`) is their call.
2. **Staged work:** `git write-tree` must be the same. If not, put it back with `git read-tree <noted tree>` and tell the user.
3. **Files git tracks:** `git diff --name-only` must be empty. Put back each file it lists with `git restore <file>` (it restores the staged version) and tell the user; a rewritten test snapshot counts.
4. **New files:** in `git status --short --untracked-files=all`, the tester may leave new test files with `tester` in their name; the reviewer, none. Output of running the tools (coverage reports, caches, build files) isn't a change: add its pattern to `.gitignore` and tell the user. Any other new file: show it to the user and ask before deleting it, since `git restore` doesn't remove untracked files.

## Checkpoints

Commit on the branch whenever a step is done and before stopping, staged as above, with a message starting `wip:` that names the step done and the state (e.g. `wip: tests first — empty cart, failing`, `wip: tester round 2 — no failures`). Checkpoints let the work be resumed in a new session and keep a working state to go back to. They're never pushed to the main branch: the squash replaces them.

A new session sees only the repository, not this conversation, so what a later step needs goes in the checkpoint's body: the approved critical test list, each tester report verbatim (with its round), which tests came from the tester and where they were moved, and the entry as it was before the documents step removed it. If a resumed branch lacks one of these, redo the step that produces it (e.g. a new tester round) rather than writing it from memory.

If a commit-msg hook enforces a message format (commitlint, a conventional-commits check), adapt only the first line to it and keep the marker: `chore(wip): <step>` for checkpoints, `feat(<name>): …` or `fix(<name>): …` for the final message, `docs(backlog): …` for document commits; the body stays as below. If the project's CLAUDE.md doesn't name it yet, add a `Commit messages:` line to its Development cycle section, and look for the adapted marker when resuming.

If a pre-commit hook rejects a checkpoint (it runs tests or lint, and the work is meant to be failing at that step), don't bypass it on your own. Ask the user once whether `wip:` checkpoints may skip hooks with `--no-verify`, and record the answer in the project's CLAUDE.md, Development cycle section, so it isn't asked again. If not, skip that checkpoint and commit at the next step that passes the hook. The verification commit and every commit on the main branch always run the hooks.

## The verification commit

When the work is verified, the skill makes the branch's last commit with the verification message (`git commit --allow-empty -F <file>`: the last checkpoint often already holds every change), in this format. Keep the sections in this order and leave out the ones the skill doesn't use; within each, write `(none)` when it applies but is empty. The block names (`Critical tests:`, `Regression tests:`, `Redundant older tests:`, `To check by hand:`) are searched with `git log --grep`, so write them exactly, alone on their line.

```
<Name>: <what changed, in a few words>

<what changed and why, in two or three lines>

Tests: <suite result, with counts>. Build: <result>.
<chore: the same before the change; an upgrade: versions and breaking changes handled>

Tester:
<build: one line per earlier round (what it found, how it was resolved, tester tests removed with the user's OK), then the last report verbatim; or "no tester: <why>">

Check of the tests:
- merged or removed: <file> — <test name> — <why>
- moved: <old tester file> → <new file> — <test name>
- changed with the user's OK: <file> — <test name> — <the rule that changed>
- sabotage: <rule> — <what was broken> — <the test that failed>

Review:
- blocking: <finding as the reviewer wrote it> — <how it was resolved>
- applied: <suggestion>
- declined: <suggestion> — <why>
<or "no review: <why>">

Critical tests:
<build: file> — <test name>

Regression tests:
<fix: file> — <test name>

Redundant older tests:
<file> — <test name> — <the test that covers it>

To check by hand:
<one item per line>
```

If fixes come after it (e.g. from checking by hand), commit them as checkpoints.

The main branch gets the **final message**: the verification message (`git log -1 --format=%B <branch>` if it's still the last commit; otherwise find it in `git log <main branch>..<branch>`), plus a line for each fix made after it, plus a line for each document change made on the branch that isn't part of the work (e.g. an idea recorded meanwhile).

## Merge and push

Once the user confirms everything works (or right after the verification commit, if there's nothing to check by hand), follow the project's integration mode.

**Local merge:** the main branch only ever receives code that was already tested combined with it, so a failure is fixed on the branch, never on the main branch.
1. If the repository has a remote, bring the main branch up to date: `git switch <main branch>`, update it as in The main branch, `git switch <branch>`.
2. On the branch, `git merge <main branch>` (the squash flattens this merge). If it has conflicts:
   - **Only in BACKLOG.md or CHANGELOG.md** (two changes adding lines at the same place, e.g. under `[Unreleased]`): keep both sides with the `document` skill, show the user the result, then `git add` those files and `git commit --no-edit`.
   - **Anywhere else:** stop and show them instead of resolving them on your own. Once the user has resolved them (or told you how), `git add` the files, `git commit --no-edit`, and go on with step 3.
3. Run the test suite and the build on the branch, unless step 2 brought nothing (`Already up to date`) and they already passed on the branch's last commit. If the main branch moved since the branch started, this is the first time the combined code runs. If anything fails, fix it on the branch (test first when it can be reproduced in one), commit it as a checkpoint and run them again; after 3 rounds still failing, stop and show the user what's left. Tell the user what broke and how it was fixed, and add a line for it to the final message.
4. Switch to the main branch, `git merge --squash <branch>` and commit with the final message.
5. Check that the main branch now holds exactly what was tested: `git diff --quiet <branch> HEAD`. It should, since step 2 merged the main branch into the branch; then the suite and build don't need to run again. Only if it shows a difference, run the test suite and the build. If anything fails, the commit hasn't left this machine: undo only that commit with `git reset --hard HEAD~1` (the working tree is clean, so nothing else is lost), switch back to the branch and show the user; continue from step 3.
6. Push the main branch, if the repository has a remote. Never force it. If it's rejected, the squashed commit hasn't left this machine: undo only it with `git reset --hard HEAD~1` and switch back to the branch. Then read why:
   - **The remote moved meanwhile** (`fetch first`, `non-fast-forward`): continue from step 1.
   - **The branch is protected** (`protected branch`, `GH006`, a rule or ruleset that requires pull requests): stop. Tell the user the main branch only takes pull requests, offer to switch the project's Integration line to pull requests, and if they agree, bring this branch in that way.
   - **Anything else** (permissions, a hook on the server): stop and show the user the message.
7. Delete the branch with `git branch -D <branch>` (git doesn't see a squashed branch as merged, so `-d` refuses). If it's checked out in this worktree, see Worktrees first.

**Pull requests:**
1. Push the branch: `git push -u <remote> <branch>`.
2. Open the pull request with `gh pr create --base <main branch> --head <branch>`, its title the final message's first line and its body the rest. If one is already open for the branch, update it instead (`gh pr edit`). Give the user its link.
3. Wait for the checks: `gh pr checks --watch`. A failing check is fixed on the branch, committed, pushed, and waited for again. If the repository has no checks, bring the main branch into the branch (`git fetch <remote>`, `git merge <remote>/<main branch>`; the squash flattens this merge too), run the test suite and the build, and push.
4. If the main branch requires a review, stop: tell the user the pull request is waiting for one. When review comments come back (`gh pr view <branch> --comments`), handle each change asked as a fix after the verification commit: test first when it changes behavior, the documents updated with `document`, a checkpoint and a line in the final message; push and wait for the checks again. A comment you disagree with goes to the user, not unanswered.
5. Before merging, check that every commit the local main branch has is in the branch (`git merge-base --is-ancestor <main branch> <branch>`); if not, stop and show the user which commits are missing. Then merge with `gh pr merge --squash --subject "<first line>" --body "<rest>"`, from the final message as it stands now.
6. Update the local main branch: `git switch <main branch>`, `git fetch <remote>`. If the local main branch had commits not on the remote (document changes made on it before the branch started), they're now inside the squashed commit, as step 5 checked: `git reset --hard <remote>/<main branch>`. Otherwise `git pull --ff-only`.
7. Delete the local branch with `git branch -D <branch>` (in a worktree, see Worktrees first), and the remote one with `git push <remote> --delete <branch>` if GitHub didn't.

## When a merged change breaks

If a change that already reached the main branch on the remote turns out broken, show the user two ways and let them choose:
- **Fix forward** with the `fix` skill, when the cause is clear and the fix is small.
- **Revert** when the breakage hurts users now, or the cause isn't clear. Each branch reached the main branch as one commit, so reverting it removes the whole change at once: start a `fix/revert-<short-name>` branch as above, run `git revert --no-edit <sha>`, run the test suite and the build, and bring it in like any other branch. The revert also undoes what the change's commit wrote in BACKLOG.md, SPEC.md and CHANGELOG.md: the SPEC rules go, a feature's entry (or a fix's Bug entry) comes back as it was on the main branch before, and its changelog line goes. It also undoes document changes that only rode along in that commit (the final message lists them, e.g. an idea recorded meanwhile): reapply those. Then, with the `document` skill, in the same branch: set a restored feature entry back to Idea (it comes back In progress, as it was before the squash); if the change was already in a released version, put its line back in that version (released history isn't rewritten) and record the revert under `[Unreleased]` (Removed for a feature, Fixed for a fix); add what went wrong to the restored entry's Open questions. A reverted feature is built again later through `build`, from that entry.

Never rewrite the main branch's history once it's on the remote (no `reset` or force-push there): a revert is a new commit everyone can see.
