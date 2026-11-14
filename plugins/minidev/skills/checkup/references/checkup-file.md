# CHECKUP.md

`CHECKUP.md`, at the project's root, holds the last check-up: what the next one compares itself with, and what it must not raise again. It's replaced whole at each check-up; git keeps the earlier ones (`git log -p -- CHECKUP.md`). Only a full check-up writes it, after the user's OK to the report.

It isn't a product document: BACKLOG.md, SPEC.md and CHANGELOG.md stay with the `document` skill, and a finding the user approves lives in the backlog, where it's worked on. This file keeps only where each finding went: recorded in the backlog, handed over to the skill that owns the work, or declined.

Write it in the project's documents language (its CLAUDE.md, `Documents:`).

## Format

```markdown
# Check-up

The last health check-up of this project, written by `/minidev:checkup` and replaced at each one. Earlier ones: `git log -p -- CHECKUP.md`.

- **Date:** <YYYY-MM-DD>
- **Commit:** <the last change the check-up read: the history script's Last change line, full hash>
- **Changes since the last one:** <number, counted as the skill's When to run says, or "first check-up">
- **Cost:** <each agent's model and tokens, when the environment reported them; otherwise "not reported">

## Verdicts

| Area | Verdict | Last |
|---|---|---|
| Architecture | <Solid, With caveats or At risk> | <the last check-up's, or "–"> |
| Decisions and growth | … | … |
| Backlog | … | … |
| Documents and tests | … | … |

<One sentence: whether the software is solid so far, and the one thing that weighs most.>

## Numbers

| | Now | Last |
|---|---|---|
| Code (files, lines) | … | … |
| Tests (files, lines) | … | … |
| Changes read, fixes among them | … | … |
| Suite time, skipped tests | … | … |
| Dependencies: majors behind, known vulnerabilities | … | … |

Files that change most: <the top five, each with its changes and fixes>
Files that change together: <the pairs, or "none">

## Findings

### <title>
- **Found:** <the date of the check-up that found it>
- **Area:** <area>
- **Weight:** <high, medium or low>
- **Evidence:** <as reported>
- **Cost of waiting:** <as reported>
- **When:** <as reported>
- **Status:** <Recorded: <the backlog entry's name or the issue's number> | Handed over: <a spec audit, a test prune, a backlog clean-up or a SPEC.md correction> | Declined: <the user's reason, or "no reason given">>

## Refuted

- <title> (<area>, <the date it was refuted>): <the refuter's reason, in a line>
```

A finding the refuter weakened is written as it left it: its weight, and the part that held. What the agents reported in English is translated when the documents are in another language.

**Commit** is the last change, not HEAD: a document commit on top of it (an idea noted, this file's own) may still be rewritten before it's pushed, and a commit that no longer exists can't be counted from. Without the script, it's `git rev-list -1 --first-parent HEAD -- . ':(exclude)*.md'`.

**Carried over.** The file is what the next check-up must not raise again, so it keeps more than this check-up's findings. From the last file, copy as they are: every finding Recorded whose entry is still open, every Declined one, and the Refuted lines. Leave behind a Recorded finding whose entry is closed or gone (if the problem is still there, an auditor finds it again) and a Handed over one (it's raised again while it's true).

Leave out a section with nothing in it, except Verdicts. A number that wasn't collected (no Python, a command that isn't installed) is written as "not collected", so the next check-up doesn't read it as zero.

## Reading it

The next check-up takes from it:
- **Commit**, for the history script's `--since`, and to count the changes since;
- **Verdicts** and **Numbers**, to show beside the new ones;
- **Findings** and **Refuted**, given to every auditor, whatever the area, so none raises them again unless the evidence changed. A finding that was Recorded and whose entry is still open in the backlog is debt waiting, not a new finding: it counts in its area's verdict. A Handed over one has no entry holding it, so the auditor raises it again when it's still true.

A CHECKUP.md that doesn't follow this format (edited by hand, or from an older version) is read for what it has; what's missing counts as "first check-up".
