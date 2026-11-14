# Backlog in GitHub issues

When the project's CLAUDE.md says `Backlog: GitHub issues`, the backlog lives in the repository's GitHub issues instead of BACKLOG.md. The team sees what's wanted and what's being built as it changes, without waiting for a merge, and two people recording ideas don't conflict in a file. SPEC.md and CHANGELOG.md stay files, since they change in the same commit as the code.

Everything in `backlog.md` still holds (what each field is for, how to fill it, when to ask) except where entries are stored, which this file replaces. Each entry's issue body is the entry in the format of `backlog.md` (Entry format), without its heading (the title carries the name) and without the Status, Type, Version and Needs fields, which GitHub keeps outside the body (Mapping). Use `gh`, signed in (`gh auth status`). If it isn't, or the repository has issues turned off, stop and tell the user: don't fall back to BACKLOG.md, or the backlog ends up in two places.

## Mapping

| BACKLOG.md | Issues |
|---|---|
| Area (`##`) | label `area:<name>`, lowercase with hyphens (`area:time-tracking`); a second one when the entry changes that part too |
| Order inside an area | the issues' numbers, lowest first |
| A feature (no Type) | label `enhancement` |
| Type Bug, Debt | label `bug`, `debt` |
| Version | the milestone titled with the version |
| Needs | GitHub's "blocked by" relation to the issue it needs |
| Idea | open, without the `in progress` label |
| In progress (`feature/<name>`) | label `in progress`, assigned to whoever builds it; the branch is `feature/<number>-<name>`. The label comes off once the change is on the main branch |
| Done: the entry leaves the file | `Closes #<number>` in the final message, so the issue closes when the change reaches the main branch |
| Discarded | closed as not planned, with a comment giving the reason and the date |

**Labels.** A label that doesn't exist yet (`gh label list`) is created the first time it's needed, with a description of what it covers (`gh label create "area:editor" --description "Typing, formatting and autosave of a note"`): the label list is this backlog's legend. Say so. `enhancement` and `bug` come with a new repository: use them as they are. A new area label is a new area, so it's confirmed first, as in `backlog.md`. An open issue with no type label reads as a feature, as issues opened by hand often are: add `enhancement` the next time you write to it. Labels the cycle doesn't write (`documentation`, `question`, a team's own) are left alone.

**Versions.** When the user plans an entry for a version with no milestone yet, create it (`gh api repos/{owner}/{repo}/milestones -f title="<version>"`) and say so. Set it with `--milestone "<version>"` on `gh issue create` or `gh issue edit`; clear it with `gh issue edit <number> --remove-milestone`. The current version (`backlog.md`, Entry format) is read from the `milestone` of the open issues, so a milestone with nothing open in it is ignored.

**Relations.** Write a Needs with `--blocked-by <numbers>` on `gh issue create`, or `gh issue edit <number> --add-blocked-by <number>`; end it with `--remove-blocked-by <number>`, which is also what dropping a need writes; read it with `--json blockedBy,blocking` (what the issue waits for, and what waits for it). GitHub shows the relation on both issues, so the body has no Needs line. An issue waits only while one it's blocked by is still open: finishing an entry needs no edit to the ones that waited, while discarding one still asks (`backlog.md`, Relations between entries). If `gh` doesn't know these flags it's too old: tell the user to update it, and don't write the relation in the body instead, or it ends up in two places.

## Writing to issues

Everyone who can see the repository sees an issue as soon as it's written. The confirmation table in SKILL.md applies to issues as it does to BACKLOG.md: a user's direct request ("note this idea") is the OK to create the issue, and a capture that interprets the conversation shows the draft first. One rule is added: changing the body of an issue someone else opened shows the change and waits for the OK, since it rewrites a colleague's text. What the cycle writes inside a step the user already approved doesn't ask again: the Decisions from `build`'s start message, the tester's assumptions (confirmed at its end message), labels, assignees and relations, closing, a revert's Open question. The rule is for other edits: merging a duplicate, a clean-up, an edit the user asks for on its own.

Write issues and comments in the documents' language (SKILL.md, Language), like BACKLOG.md.

Read an issue again before using it (`gh issue view <number> --comments`): others edit and comment on it. If a comment newer than the body changes what the body says (a Decision, the scope), ask the user which holds (in `build`, as an open point of its start message); then update the body, so it keeps being the entry.

Wherever another skill copies the entry (into a checkpoint's body, for the tester, for the reviewer), it copies the issue's body read at that moment, with its number.

Nothing about the backlog is committed in this mode: the issue is the record. Commits of SPEC.md and CHANGELOG.md follow SKILL.md, Commits.

## Operations

Each operation of `backlog.md` does the same thing, stored this way:

- **Capture, record a bug or debt, add an idea:** as in `backlog.md`, then `gh issue create --title "<entry name>" --body-file <file> --label <labels>`, with `--milestone` and `--blocked-by` when the entry has a Version or a Needs. Give the user the issue's link.
- **Check for duplicates:** `gh issue list --state all --search "<key words>"`. A closed issue is either done or discarded (closed as not planned): handle it as `backlog.md` handles a Discarded entry or an implemented one.
- **Present:** `gh issue list --state open --limit 200 --json number,title,labels,milestone,assignees,blockedBy`, grouped by area label (an issue with two areas appears in both), each with its number, its status (Idea, or In progress and who builds it), its type, its version and the open issues it waits for.
- **Plan a version:** as in `backlog.md`, written as the milestone (Versions).
- **Start a feature:**
  1. Check for overlap as in `backlog.md`, among the open issues labeled `in progress`, whoever builds them (the branch may be only on the remote: `git branch -r --list '<remote>/feature/<number>-*'`).
  2. `gh issue edit <number> --add-label "in progress" --add-assignee @me`. Nothing goes to the main branch: the issue is where the team looks to see what is being built.
  3. The branch is `feature/<number>-<short-name>`.
  4. The Decisions the start message approves, and the tester's assumptions `build` adopts, go in the issue's body as they're made. An assumption the user confirms or changes at the end message is written in the body too, without its "assumed" mark or with the new answer. **To check by hand** doesn't go in the issue: it goes in the branch's checkpoint and, at the end, in the final message, which is the pull request's body.
- **Finish a feature:** steps 1 and 2 of `backlog.md` (SPEC.md and CHANGELOG.md). Instead of removing the entry, the skill that built it ends its final message with `Closes #<number>` (`../../build/references/git-flow.md`, The verification commit). GitHub closes the issue when that message reaches the repository's default branch, through the pull request's merge or the push of a local merge. When the main branch isn't the default one (a `Main branch:` line), GitHub doesn't close it: once the change is on the remote's main branch, close it with `gh issue close <number> --reason completed --comment "<the squashed commit's hash>"`. In every mode, once the change is on the main branch, take the label off (`gh issue edit <number> --remove-label "in progress"`): GitHub's filters would otherwise show a closed issue as still being built. The skill that built the feature does both in its Merge and push (`../../build/references/git-flow.md`).
- **A feature done outside `build`:** as in `backlog.md`; its commit's message ends with `Closes #<number>`, or close the issue as above once it's pushed.
- **Bug and Debt done by `fix` or `chore`:** the branch is `fix/<number>-<short-name>` or `chore/<number>-<short-name>`, and the final message (or a chore's one-line commit) ends with `Closes #<number>`.
- **Change status:** pausing removes the label and the assignee (`gh issue edit <number> --remove-label "in progress" --remove-assignee @me`); the branch stays, as in `backlog.md`.
- **Discard:** only on the user's word, as in `backlog.md`: `gh issue close <number> --reason "not planned" --comment "<why discarded> (<date>)"`. An `in progress` label and its assignee come off, and the branch, if any, is handled as `backlog.md` says.
- **Revert** (`../../build/references/git-flow.md`, When a merged change breaks): GitHub doesn't reopen an issue when its change is reverted. On the revert's branch, as part of the revert, reopen it (`gh issue reopen <number>`), remove the `in progress` label and its assignees, and add what went wrong to its Open questions. The revert's own final message has no `Closes` line: it would close the issue again.
- **Clean up and reorganize:** as in `backlog.md`, with the plan shown first. A request to relabel, classify or tag the issues is a reorganization. Here the plan is a list: each open issue with the labels and the milestone it gains and loses, the labels to create, each with its description, and the labels no open issue carries any more, which are deleted only with the OK (`gh label delete <name> --yes`; deleting one takes it off the closed issues too). An issue with no type label gets the one its body shows (`bug`, `debt` or `enhancement`), and a milestone is proposed, since only the user plans a version. Closed issues are history: they get no new labels, and lose only `in progress`.
- **Debt entries from a spec audit, a test pruning or a new SPEC.md** are created as issues, one per area, after the approval those steps already ask for (for a new SPEC.md, the OK to its finished draft, which shows them as issues to create, visible to everyone who can see the repository).

## Migrate from BACKLOG.md

When `setup` switches a project to issues and BACKLOG.md exists, show the user the list: one issue per entry, in the file's order, with its title, labels, milestone and the entries it needs. Discarded entries aren't migrated: they stay in git history. Creating them publishes the whole backlog at once, so wait for an explicit OK to the list (in `setup`, its step 8 message); it also covers the area labels and the milestones the list names. If the file's areas are phases, the list proposes the reorganization of `backlog.md` (Reorganize) first, so the issues don't start with labels that say when.

An In progress entry becomes an issue with the label, assigned to whoever builds it (the list asks; the user by default), and a comment naming its branch, which keeps its name: Resume finds the branch by that comment, and its final message ends with `Closes #<number>` like any other. When that branch next takes in the main branch, BACKLOG.md conflicts (deleted on one side, changed on the other): keep the deletion (`git rm BACKLOG.md`) and move the entry's To check by hand list into the next checkpoint's body.

Create them one by one with `gh issue create`, and show each link. Once all exist, write each Needs as a relation (Relations): the numbers aren't known before. Then remove BACKLOG.md (`git rm`) and switch the CLAUDE.md to issues (`setup`, Finish), both in the commit `setup` offers. If a creation fails halfway, stop: show which entries became issues and which didn't, and keep BACKLOG.md until all of them exist.
