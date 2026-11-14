# CHECKUP.md

`CHECKUP.md`, at the project's root, holds the last check-up: what the next one compares itself with, and what it must not raise again. It's replaced whole at each check-up; git keeps the earlier ones (`git log -p -- CHECKUP.md`). Only a full check-up writes it, after the user's OK to the report.

It isn't a product document: BACKLOG.md, SPEC.md and CHANGELOG.md stay with the `document` skill, and a finding the user approves lives in the backlog, where it's worked on. This file keeps only where each finding went.

Write it in the project's documents language (its CLAUDE.md, `Documents:`).

## Format

```markdown
# Check-up

The last health check-up of this project, written by `/minidev:checkup` and replaced at each one. Earlier ones: `git log -p -- CHECKUP.md`.

- **Date:** <YYYY-MM-DD>
- **Commit:** <the main branch's commit the check-up read, full hash>
- **Changes since the last one:** <number, or "first check-up">
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
- **Area:** <area>
- **Weight:** <high, medium or low>
- **Evidence:** <as reported>
- **Cost of waiting:** <as reported>
- **When:** <as reported>
- **Status:** <Recorded: <the backlog entry's name or the issue's number> | Declined: <the user's reason>>

## Refuted

- <title> (<area>): <the refuter's reason, in a line>
```

Leave out a section with nothing in it, except Verdicts. A number that wasn't collected (no Python, a command that isn't installed) is written as "not collected", so the next check-up doesn't read it as zero.

## Reading it

The next check-up takes from it:
- **Commit**, for the history script's `--since`, and to count the changes since;
- **Verdicts** and **Numbers**, to show beside the new ones;
- **Findings** and **Refuted**, given to each area's auditor so it doesn't raise them again unless the evidence changed. A finding that was Recorded and whose entry is still open in the backlog is debt waiting, not a new finding.

A CHECKUP.md that doesn't follow this format (edited by hand, or from an older version) is read for what it has; what's missing counts as "first check-up".
