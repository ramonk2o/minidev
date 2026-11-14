# Areas

The four briefs the `checkup` skill gives its auditors, one area per auditor. Copy an area's brief into that auditor's prompt as it is, from its heading to the next one. The auditor's own instructions (`agents/auditor.md`) say what a finding is and how to report it; a brief only says where to look.

## Architecture

As built, against as decided.

What was decided is in SPEC.md (Technical decisions, Data model, Constraints) and in the project's instructions (Conventions). What was built is the modules and what depends on what.

Look for:
- dependencies that run against the decided direction: a lower layer importing an upper one, a module reaching into another's internals;
- cycles between modules;
- a module that everything depends on, or that does several unrelated jobs, above all when it's among the files that change most;
- two solutions to the same problem (validation, calls to the outside, state, errors, dates, configuration): each change brought its own, and the next one has to choose or add a third;
- decisions in SPEC.md the code no longer follows, and decisions the code made that SPEC.md doesn't state, which the next person will break without knowing;
- the files in different folders that change together (from the numbers): what ties them, and whether it's a missing module or a detail that leaked;
- the folders where fixes concentrate: whether the same kind of bug keeps coming back for a structural reason.

And the reverse: a decision the code follows that isn't serving. Read the last changes to the files that change most (`git log -p`): the same workaround repeated in several of them points to a decision that should be taken again.

## Decisions and growth

What gets expensive to reverse, and what breaks when the product grows.

**Expensive to reverse.** For each of these the product has: the stored data's shape (schema, files, keys, ids), contracts with the outside (a public API, command-line flags, file formats, events, URLs), and authentication and permissions. Ask:
- does its shape fit what SPEC.md's Goal and the backlog say the product is becoming?
- what is already stored or published in a shape that will need migrating, and is there a way to migrate (versions, migrations) at all?
- what does the code rely on that the data doesn't guarantee (uniqueness, references that must exist, units, time zones, money as floating point)?

These get more expensive with every record stored and every user of the contract, so one that's wrong weighs more than its size in the code suggests.

**Growth.** Take the axes the product really has, from SPEC.md's Goal and Constraints: users, records, file sizes, requests. On each, what works today and breaks at ten times as much: a query or a call per item in a loop, a list read or shown whole with no limit, everything loaded in memory, work repeated on every request, a query with no index behind it, a cache, log or queue with no bound. Name the axis and the path. A product whose SPEC.md says it serves one person's scripts has no ten-times-users axis: don't invent one.

## Backlog

The backlog against the structure and the product's goal.

Read every open entry (BACKLOG.md, or the issues, with the command you were given), SPEC.md's Goal, and enough of the code's structure to place each entry in it.

Look for:
- the entries likely to be built next: whether each fits the structure as it is, or needs something the structure doesn't have (name it). Several entries needing the same missing thing is a decision to take before any of them is built;
- entries that contradict each other, a SPEC.md rule or a Constraint;
- duplicates, entries the code already does, and entries whose premise is gone (a module or behavior that no longer exists);
- Bug and Debt entries parked for long (an issue's date; `git log` of BACKLOG.md) in an area that keeps changing (from the numbers): debt being built on;
- whether debt is growing: Bug and Debt entries opened against closed since the last check-up;
- a backlog that pulls the product in directions the Goal doesn't hold together.

## Documents and tests

Whether the documents still describe what exists, and whether the tests and dependencies still make changing it safe. This is a sample, not a full audit: its job is to say whether a full one is due.

- **SPEC.md.** Take the areas whose code changed most (from the numbers), up to about 15 rules. Check each rule as the spec audit does (the first file whose path you were given, Each rule): the code that does it, and a test that would fail if it broke. Then, for each area:
  - three or more sampled rules fail, in any way: one finding with those rules as its evidence; its way out is a spec audit of the area;
  - otherwise, a rule the code contradicts, or that no code does: a finding of its own; its way out is settling which is right, the code or SPEC.md;
  - otherwise, a rule with no test: one finding for the area; its way out is a Missing tests entry.

  Say in Checked how many rules you sampled and how many held.
- **The project's instructions.** The commands CLAUDE.md names exist, the paths it names exist, and the last changes follow its Conventions.
- **Tests.** From the numbers: skipped tests and why each is skipped, and how long the suite takes against the last check-up. In the modules that change most: tests that fit the useless patterns (the second file whose path you were given), above all tests tied to how the code is written, which had to be rewritten along with it (`git log` of the test files).
- **Dependencies.** From the numbers: major versions behind, known vulnerabilities, packages no longer maintained. A finding only where waiting has a cost: a vulnerability in a path the product uses, a version whose support ends, an upgrade another one is waiting for.
