# A GitHub repository for the project

The cycle's pull requests and issues need the project on GitHub. When the repository has no remote and `gh` is signed in, setup offers to create one. The user may decline, at the question or at the review: the project then uses local merge and BACKLOG.md, and setup can be run again later. After a decline at the review, redo the proposals for local merge and BACKLOG.md and show them again.

## Ask (step 3)

With the integration question, propose the repository: its name (the folder's), its owner (the signed-in account, unless the user names an organization) and its visibility, recommending private: the code leaves this machine, but nobody else sees it until the user decides. Say what each answer brings: yes, pull requests, and step 3's backlog question with issues recommended; no, local merge and BACKLOG.md.

## Show (step 8)

The repository to create (owner/name, visibility), said to upload the project's code to GitHub at the first push.

## Create (step 9)

1. After `git init` and before the CLAUDE.md, run `gh repo create <owner>/<name> --private --source . --remote origin` (`--public` if chosen), without `--push`. Give the user the link.
2. If it fails (the name is taken, no right to create in that organization), show the error and ask: another name or owner, or local merge and BACKLOG.md. Don't write a pull request CLAUDE.md for a repository that doesn't exist.
3. The remote has no main branch yet, so setup's commit reaches the main branch without a pull request (step 9.3). Then push the main branch (`git push -u origin <main branch>`), on an OK of its own, apart from the commit's: the first pull request needs it there. If the user declines the push, say the main branch isn't on GitHub yet and the cycle's first pull request will need it pushed.
