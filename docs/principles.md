# Principles

The rules every skill, agent and change in minidev is judged against. Each one is a statement a reviewer can check.

<!-- sensei:limits
skill_tokens: 5000
description_chars: 1024
-->

## Before writing

- A skill that writes files or runs a command with effects first shows, in one message, what it will do, the open points each with a recommended answer, and waits for the user's OK.
- Questions come in rounds, each with a recommended answer and its reason, never one at a time.
- Nothing the user didn't approve is written, committed or pushed.

## Checking results

- The user's work is checked by independent agents (`tester` and `reviewer` for a change, `auditor` and `refuter` for a check-up) that see only what they're given and never fix what they check; Claude doesn't filter their reports.
- A change to a skill's description runs the trigger evals before it's released.
- A change to a skill's steps runs the behavior evals before it's released.
- A change to the CLAUDE.md template in `setup`, the unattended-run prompt, a cycle check, a shared grader or the check-up's weight scale runs `evals/check-copies.py`, and every copy it lists is brought back in line.

## Skills and their files

- Skills don't stand alone: a reference shared by several skills lives in one skill's folder (e.g. `build/references/git-flow.md`), and the others point to it by its path, naming whose it is. It's never copied.
- Each rule lives in one place; other skills and the README point to it instead of restating it.
- The plugin ships whole, from `plugins/minidev/`; there are no per-skill zips.

## Size

- A SKILL.md stays under 5000 tokens; detail that only some runs need goes to `references/`.
- A description stays under 1024 characters.

## Language

- Every file in the plugin is in English.
- Skills talk to the user in the user's language.
- Trigger evals cover requests in English and Portuguese.

## Judging a proposal

1. Does it come from a real case, and does the change fix that case?
2. Does it ask before writing, with recommended answers?
3. Is each rule it adds or changes in one place, and do the skills that point to it still agree?
4. Which evals does it need (trigger, behavior, outcome, check-copies), and did they run?
5. Does every SKILL.md and description stay within the limits?
6. Is it in English, and does it still serve users who write in Portuguese?
