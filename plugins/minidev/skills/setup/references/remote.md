# A GitHub repository for the project

The cycle's pull requests and issues need the project on GitHub. When the repository has no remote and `gh` is signed in, setup offers to create one. The user may decline: the project then uses local merge and BACKLOG.md, and setup can be run again later.

## Ask (step 3)

With the integration question, propose the repository: its name (the folder's), its owner (the signed-in account, unless the user names an organization) and its visibility, recommending private: the code leaves this machine, but nobody else sees it until the user decides. Say what each answer brings: yes, pull requests and the backlog in issues; no, local merge and BACKLOG.md.

## Show (step 8)

The repository to create (owner/name, visibility), said to upload the project's code to GitHub at the first push.

## Create (step 9)

1. After `git init` and before the CLAUDE.md, run `gh repo create <owner>/<name> --private --source . --remote origin` (`--public` if chosen), without `--push`. Give the user the link.
2. If it fails (the name is taken, no right to create in that organization), show the error and ask: another name or owner, or local merge and BACKLOG.md. Don't write a pull request CLAUDE.md for a repository that doesn't exist.
3. The remote has no main branch yet, so setup's commit goes on the main branch (step 9.3). Then push it (`git push -u origin <main branch>`) on the user's OK: the first pull request needs it there. If the user declines, say so.
