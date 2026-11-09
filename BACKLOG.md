# Backlog

Ideas, bugs and debt for this plugin, managed with sensei's `log` skill. Each entry starts from a real case. Done work leaves this file: what changed goes to CHANGELOG.md.

## setup

### Setup's commit in pull request mode
- **Type:** Bug
- **Motivation:** A cold reader of the GitHub-issues backlog change (2026-11-09) asked which branch `setup`'s final commit goes on when the integration is pull requests; the skill doesn't say. With a protected main branch, a commit on the local main can't be pushed, and since that commit now also removes a migrated BACKLOG.md, the team would see the new issues while the remote still has BACKLOG.md.
- **Description:** In either pull request mode, `setup` says where its commit goes (e.g. a `chore/setup-minidev` branch and a pull request, through `git-flow.md`), so it can reach a protected main branch.
- **Open questions:**
  - A branch and pull request always in pull request mode, or only when the main branch is protected?
