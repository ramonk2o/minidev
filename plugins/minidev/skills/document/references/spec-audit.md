# Spec audit

Checks SPEC.md against the code, rule by rule, in both directions: each rule against the code and tests, and the behavior the code exposes against the rules. Used:

- when SPEC.md is created for a product that already has code (`references/spec.md`, Write it from what exists), so it starts out checked;
- when `setup` adopts a project whose SPEC.md was written before the cycle;
- when the user asks ("audit the spec", "does SPEC.md match the code?", "o SPEC está atualizado?"), or asks to update SPEC.md without naming a change.

It reads; it changes no code. What it finds becomes SPEC.md corrections, Bug and Debt entries, and questions for the user.

## Scope

A small product is audited whole. With more than about 10 Behavior areas, or when the user asks, go one area at a time: after each, show its report and ask whether to go on. The commit of each part names the areas done ("Spec audit: Editor, Sync (2 of 7 areas)"), so a later session finds where it stopped with `git log --grep "Spec audit"`.

## Each rule

For each rule in Behavior, Data model, Technical decisions and Constraints, find the code that does it and a test that would fail if it broke. Judge a test by its assertions, not its name (`../../build/references/test-value.md`). Reading is enough; the suite doesn't need to run.

| What you find | What happens |
|---|---|
| Implemented, and a test checks it | Nothing. Count it. |
| Implemented, no test checks it (or only maybe) | The rule stays. It goes into a Debt entry for its area: `Missing tests: <area>`, listing the rules, for a later `chore`. |
| The code does something else | Ask which is right, with your recommendation and why: the code wrong is a bug (a Bug entry, or `fix` now if the user wants); the SPEC wrong is a correction to SPEC.md. Until answered, don't write it either way. |
| No code does it | Ask whether it was removed (the rule leaves SPEC.md) or it's a bug. |
| Behavior that looks accidental (an odd default, a case handled differently from its neighbors) | Ask whether it's a rule. Don't make it one on your own. |

## The other direction

Look at what users can meet: public functions and their options, commands and flags, endpoints, error messages, limits and defaults, files read or written. For each behavior someone could break that no rule states, propose a rule, in the SPEC's own style. Obvious behavior doesn't need one.

## Report

Show it in one message, grouped: what the code contradicts, rules not found, behavior that may be accidental, rules with no test (by area), rules proposed for behavior SPEC.md doesn't state, and how many rules checked out. Each item names the rule (or the code, for a missing one) and your recommendation. Wait for the OK; the user may approve parts.

## Apply

With this skill, once approved:
- SPEC.md: the corrections, removed rules and new rules (`references/spec.md`, Updating it).
- BACKLOG.md: one Debt entry per area with untested rules, one Bug entry per contradiction where the code is wrong (unless the user fixes it now with `fix`), as in `references/backlog.md`.

Commit them together, as one commit of these documents ("Spec audit: <areas>"). When the audit runs inside `setup` or while creating SPEC.md, the changes go in the commit that skill offers.
