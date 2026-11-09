# Backlog in GitHub issues

When the project's CLAUDE.md says `Backlog: GitHub issues`, the backlog lives in the repository's GitHub issues instead of BACKLOG.md. The team sees what's wanted and what's being built as it changes, without waiting for a merge, and two people recording ideas don't conflict in a file. SPEC.md and CHANGELOG.md stay files, since they change in the same commit as the code.

Everything in `backlog.md` still holds (what each field is for, how to fill it, when to ask) except where entries are stored, which this file replaces. Each entry's issue body is the entry in the format of `backlog.md` (Entry format), without the Status and Type fields, which become labels. Use `gh`, signed in (`gh auth status`). If it isn't, or the repository has issues turned off, stop and tell the user: don't fall back to BACKLOG.md, or the backlog ends up in two places.

## Mapping

| BACKLOG.md | Issues |
|---|---|
| Area (`##`) | label `area:<name>` |
| Type Bug, Debt | label `bug`, `debt` (a feature has no type label) |
| Idea | open, without the `in progress` label |
| In progress (`feature/<name>`) | label `in progress`, assigned to whoever builds it; the branch is `feature/<number>-<name>` |
| Done: the entry leaves the file | `Closes #<number>` in the final message, so the issue closes when the change reaches the main branch |
| Discarded | closed as not planned, with a comment giving the reason and the date |

A label that doesn't exist yet (`gh label list`) is created the first time it's needed (`gh label create`); say so. A new area label is a new area, so it's confirmed first, as in `backlog.md`.

## Writing to issues

Everyone who can see the repository sees an issue as soon as it's written. The confirmation table in SKILL.md applies to issues as it does to BACKLOG.md: a user's direct request ("note this idea") is the OK to create the issue, and a capture that interprets the conversation shows the draft first. One rule is added: changing the body of an issue someone else opened shows the change and waits for the OK, since it rewrites a colleague's text. What the cycle writes inside a step the user already approved doesn't ask again: the Decisions from `build`'s start message, the tester's assumptions (confirmed at its end message), labels and assignees, closing, a revert's Open question. The rule is for other edits: merging a duplicate, a clean-up, an edit the user asks for on its own.

Write issues and comments in the documents' language (SKILL.md, Language), like BACKLOG.md.

Read an issue again before using it (`gh issue view <number> --comments`): others edit and comment on it. If a comment newer than the body changes what the body says (a Decision, the scope), ask the user which holds (in `build`, as an open point of its start message); then update the body, so it keeps being the entry.

Wherever another skill copies the entry (into a checkpoint's body, for the tester, for the reviewer), it copies the issue's body read at that moment, with its number.

Nothing about the backlog is committed in this mode: the issue is the record. Commits of SPEC.md and CHANGELOG.md follow SKILL.md, Commits.

## Operations

Each operation of `backlog.md` does the same thing, stored this way:

- **Capture, record a bug or debt, add an idea:** as in `backlog.md`, then `gh issue create --title "<entry name>" --body-file <file> --label <labels>`. Give the user the issue's link.
- **Check for duplicates:** `gh issue list --state all --search "<key words>"`. A closed issue is either done or discarded (closed as not planned): handle it as `backlog.md` handles a Discarded entry or an implemented one.
- **Present:** `gh issue list --state open --limit 200 --json number,title,labels,assignees`, grouped by area label, each with its number, its status (Idea, or In progress and who builds it) and its type.
- **Start a feature:**
  1. Check for overlap as in `backlog.md`, among the open issues labeled `in progress`, whoever builds them (the branch may be only on the remote: `git branch -r --list '<remote>/feature/<number>-*'`).
  2. `gh issue edit <number> --add-label "in progress" --add-assignee @me`. Nothing goes to the main branch: the issue is where the team looks to see what is being built.
  3. The branch is `feature/<number>-<short-name>`.
  4. The Decisions the start message approves, and the tester's assumptions `build` adopts, go in the issue's body as they're made. An assumption the user confirms or changes at the end message is written in the body too, without its "assumed" mark or with the new answer. **To check by hand** doesn't go in the issue: it goes in the branch's checkpoint and, at the end, in the final message, which is the pull request's body.
- **Finish a feature:** steps 1 and 2 of `backlog.md` (SPEC.md and CHANGELOG.md). Instead of removing the entry, the skill that built it ends its final message with `Closes #<number>` (`../../build/references/git-flow.md`, The verification commit). GitHub closes the issue when that message reaches the repository's default branch, through the pull request's merge or the push of a local merge. When the main branch isn't the default one (a `Main branch:` line), GitHub doesn't close it: once the change is on the remote's main branch, close it with `gh issue close <number> --reason completed --comment "<the squashed commit's hash>"`.
- **A feature done outside `build`:** as in `backlog.md`; its commit's message ends with `Closes #<number>`, or close the issue as above once it's pushed.
- **Bug and Debt done by `fix` or `chore`:** the branch is `fix/<number>-<short-name>` or `chore/<number>-<short-name>`, and the final message (or a chore's one-line commit) ends with `Closes #<number>`.
- **Change status:** pausing removes the label and the assignee (`gh issue edit <number> --remove-label "in progress" --remove-assignee @me`); the branch stays, as in `backlog.md`.
- **Discard:** only on the user's word, as in `backlog.md`: `gh issue close <number> --reason "not planned" --comment "<why discarded> (<date>)"`. The branch, if any, is handled as `backlog.md` says.
- **Revert** (`../../build/references/git-flow.md`, When a merged change breaks): GitHub doesn't reopen an issue when its change is reverted. On the revert's branch, as part of the revert, reopen it (`gh issue reopen <number>`), remove the `in progress` label and its assignees, and add what went wrong to its Open questions. The revert's own final message has no `Closes` line: it would close the issue again.
- **Clean up and reorganize:** as in `backlog.md`, with the plan shown first; moving issues between areas is a change of labels, and the clean-up looks at open issues.
- **Debt entries from a spec audit or a test pruning** are created as issues, one per area, after the approval those steps already ask for.

## Migrate from BACKLOG.md

When `setup` switches a project to issues and BACKLOG.md exists, show the user the list: one issue per entry, in the file's order, with its title and labels. Discarded entries aren't migrated: they stay in git history. Creating them publishes the whole backlog at once, so wait for an explicit OK to the list (in `setup`, its step 8 message); it also covers the area labels the list names.

An In progress entry becomes an issue with the label, assigned to whoever builds it (the list asks; the user by default), and a comment naming its branch, which keeps its name: Resume finds the branch by that comment, and its final message ends with `Closes #<number>` like any other. When that branch next takes in the main branch, BACKLOG.md conflicts (deleted on one side, changed on the other): keep the deletion (`git rm BACKLOG.md`) and move the entry's To check by hand list into the next checkpoint's body.

Create them one by one with `gh issue create`, and show each link. Then remove BACKLOG.md (`git rm`) in the commit `setup` offers. Only then does the CLAUDE.md say the backlog is in issues (`setup`, Finish). If a creation fails halfway, stop: show which entries became issues and which didn't, and keep BACKLOG.md until all of them exist.
