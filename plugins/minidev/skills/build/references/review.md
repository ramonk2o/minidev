# Review

How a finished change gets its independent code review by the `reviewer` agent. Used by the `build` skill (always, even without a tester), and by the `fix` and `chore` skills whenever they change code.

## Launch

1. Stage the work as in `git-flow.md` (Stage the work): `git diff` doesn't show files git doesn't track yet, and the reviewer needs to see them.
2. Note `git status --short` and `git rev-parse HEAD`.
3. Launch the `reviewer` agent (agent type `minidev:reviewer`). Give it only:
   - what the change is for: the feature's backlog entry (`build`), the bug as reported or its Bug entry (`fix`), the chore's description or its Debt entry (`chore`), copied in full
   - the base commit: where the branch left the main branch (`git merge-base HEAD <main branch>`)
   - the project's lint and type-check commands, if any

   Don't pass your explanations, the conversation or your own view of what might be weak: its value is not knowing what you meant.
4. When it returns, check that `git status --short` and `git rev-parse HEAD` are the same as before. It's told never to edit files or git state, but it has a shell. Undo any change and tell the user what it touched.

## Act on the report

- **Blocking:** fix each one, or, if you disagree, tell the user why and let them decide. When the fix changes behavior:
  - `build`: test first, then a new `tester` round checks the change.
  - `fix`: test first; there's no tester round.
  - `chore`: the work is no longer only a chore. Stop and tell the user, and handle that part as a bug (`fix`) or a feature.
- **Suggestions:** apply the ones that are clearly better and cheap; for the rest, tell the user in a line each why not.

One review is enough. Launch a second, new reviewer only when the blocking fixes changed a lot of code, and never more than two.

## In the verification message

Each blocking finding as the reviewer wrote it, with how it was resolved, and the suggestions applied and declined.
