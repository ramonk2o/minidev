# Backlog

Ideas, bugs and debt for this plugin, managed with sensei's `log` skill. Each entry starts from a real case. Done work leaves this file: what changed goes to CHANGELOG.md.

## Plugin

### Backlog in GitHub issues
- **Type:** Idea
- **Motivation:** The maintainer wants to use minidev in a team, where it would be better if part of what lives in local files were in GitHub issues. Today BACKLOG.md is a local file. In pull request mode, setting a feature In progress is a commit on the local main branch that waits for the next merge (`build/references/git-flow.md`, step "bring it up to date"), so the team doesn't see what is being built, and parallel edits to BACKLOG.md conflict.
- **Description:** A mode, usually paired with pull request mode, where the backlog's entries live in the repository's GitHub issues instead of BACKLOG.md. SPEC.md and CHANGELOG.md stay in files, since they change with the code and the release.
- **Open questions:**
  - The mapping proposed in the conversation, not yet decided: an entry is an issue whose body keeps today's fields; areas and Type are labels; In progress is an assignee, a label and the branch or PR link; finishing is `Closes #N` in the PR; Discarded is closed as "not planned" with the reason in a comment; a revert reopens the issue; "To check by hand" moves to the PR body.
  - How it's chosen: a `Backlog: BACKLOG.md | GitHub issues` line written by `setup`? Allowed without pull request mode?
  - Migrating an existing BACKLOG.md to issues in `setup`, and the read-only `gh issue view/list` permissions it would add.
  - Creating an issue publishes it to the team: does `document` show a draft and wait for the OK, and which writes (status changes?) stay direct?
  - The issue becomes the source of truth that others edit and comment on: reread it before using it, and how newer comments affect its Decisions.
  - Checking for duplicates with `gh issue list --search`, closed issues included.
  - Skills touched: `setup`, `document` (a variant of `references/backlog.md`), `build`, `fix`, `chore`, `brainstorm`; new eval cases and the README's "Developing the plugin".
  - GitHub Projects as a status board: proposed for later, since it needs extra `gh` scopes.
