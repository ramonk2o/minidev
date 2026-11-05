# Review

How a finished change gets its independent code review by the `reviewer` agent. Used by the `build` skill (always, even without a tester), and by the `fix` and `chore` skills whenever they change code (except a trivial fix, which `fix` defines).

## Launch

1. Have the documents updated first (each skill says when), then stage the work as in `git-flow.md` (Stage the work): `git diff` doesn't show files git doesn't track yet, and the reviewer needs to see them, documents included.
2. Note the state as in `git-flow.md` (Check after an agent).
3. Launch the `reviewer` agent (agent type `minidev:reviewer`) with this prompt, filled in and nothing added:

   ```
   What the change is for:
   <the feature's backlog entry (build), the bug as reported or its Bug entry (fix), the chore's description or its Debt entry (chore), copied in full>
   <for a test prune: "Removals the user approved:" and the list>

   Product constraints (SPEC.md, Constraints):
   <the section, copied in full, or "none">

   Base commit: <git merge-base HEAD <main branch>>
   Lint and type-check commands: <commands, or "none">
   Tester: <"ran" or "didn't run: <bug fix | chore | no automated tests | small feature>">
   ```

   Don't pass your explanations, the conversation or your own view of what might be weak: its value is not knowing what you meant.
4. When it returns, check the repository as in `git-flow.md` (Check after an agent): the reviewer may not leave any change.

## Act on the report

- **Blocking:** fix each one, or, if you disagree, tell the user why and let them decide. When the fix changes behavior:
  - `build`: test first; no new `tester` round (the test and the finding it answers go in the verification message's Review section).
  - `fix`: test first; there's no tester round.
  - `chore`: the work is no longer only a chore. Stop and tell the user, and handle that part as a bug (`fix`) or a feature.
  A finding about the documents (a SPEC rule the code doesn't follow, a changelog line that says more than was done) is fixed with the `document` skill, or in the code if the document is right.
  If the fix would merge or remove a protected test (`test-value.md`, Protected tests), ask the user first.
- **Suggestions:** apply the ones that are clearly better and cheap; for the rest, tell the user in a line each why not.

One review is enough. Launch a second, new reviewer only when the blocking fixes changed a lot of code, and never more than two.

## In the verification message

The Review section of `git-flow.md` (The verification commit): each blocking finding as the reviewer wrote it, with how it was resolved, and the suggestions applied and declined.
