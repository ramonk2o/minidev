# Backlog

Ideas, bugs and debt for this plugin, managed with sensei's `log` skill. Each entry starts from a real case. Done work leaves this file: what changed goes to CHANGELOG.md.

## setup

### The pull request commit starts from wherever the session is
- **Type:** Bug
- **Motivation:** A cold reader's finding on step 9.3: "start a `chore/minidev-setup` branch from where you are (`git switch -c`, which carries setup's uncommitted changes)". Setup never checks that the session is on the main branch, that the main branch matches the remote, or that the working tree holds only setup's changes. The request it breaks: `/minidev:setup` run on a feature branch, or with the user's own uncommitted work, in a project on GitHub.
- **Description:** In either pull request mode, setup's branch and pull request should carry only setup's changes. To reproduce: run setup in pull request mode from a branch other than the main branch, or with unrelated uncommitted changes; they go into `chore/minidev-setup` and its pull request.
- **Open questions:**
  - Check and ask the user, or follow `git-flow.md` (Start the branch), which starts from an up-to-date main branch with a clean working tree?

### Debt entries from a new SPEC.md and the migration to issues
- **Type:** Bug
- **Motivation:** A cold reader's finding on step 9.2: `document` creates SPEC.md, whose untested rules become `Missing tests` Debt entries, and migrates BACKLOG.md "from the list approved in step 8", with no order between the two. The request it breaks: `/minidev:setup` in a project with existing code, a BACKLOG.md and no SPEC.md, when the backlog moves to issues.
- **Description:** The Debt entries a new SPEC.md produces should reach the backlog with the user's approval, wherever it lives. To reproduce: follow step 9.2 in that project. With SPEC.md first, the Debt entries land in a BACKLOG.md that is about to be removed and aren't in the approved list; with the migration first, they become issues nobody approved.
- **Open questions:**
  - Which comes first, and how the new Debt entries get their OK before they become issues.
