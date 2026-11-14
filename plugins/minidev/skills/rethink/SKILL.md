---
name: rethink
description: Take everything that bothers the user about a product already in use, as loose and unfinished as it comes, and turn it into backlog changes they approve. It reads the backlog and SPEC.md first, plays the points back by subject with the earlier decisions they collide with, questions them in rounds (the user's answers too) and ends in one plan of entries to create, change and discard, which an independent auditor checks, when it holds more than one, before anything is written through document. It changes no code and may leave points open. Run only when the user invokes it, optionally with the text (e.g. "/minidev:rethink", "/minidev:rethink the home is too crowded and…").
disable-model-invocation: true
argument-hint: "[what bothers you]"
---

# Rethink

Turns loose discontent with a product in use into backlog changes. The other ways into the backlog each take one thing the user can already name: an idea (`document`, with `interview` when behavior is open), a bug (`fix`), a finding about the code's health (`checkup`). This one takes many at once, in the state they come: "this bothers me", "this looks odd", no solution yet. It ends in one plan (entries to create, change and discard) that an independent reader checks, when it holds more than one write, before `document` writes it. It changes no code, and it doesn't have to settle everything: what the session can't decide is recorded as open.

Talk to the user in the language of the conversation.

## 1. Start

1. The project uses the cycle, as `build` checks it (`../build/SKILL.md`, 1. Start). If not, offer `/minidev:setup` and stop.
2. With no text in the request, say in a few lines what will happen (the steps below, that nothing is written before the plan is approved, that one agent reads the plan) and ask for everything at once, in any order, unfinished. With the text, go on.
3. Don't answer point by point while the user is still sending. When it isn't clear that they're done, ask once.

## 2. Read before answering

- **The backlog:** every open entry and the discarded ones (`../document/references/backlog.md`; `../document/references/issues.md` when it lives in GitHub issues). With issues, also the closed ones a point touches: an earlier decision lives there.
- **SPEC.md:** the rules, data, technical decisions and constraints the points touch.
- **What's In progress,** and on which branch.
- **The product:** where a point is about what the user sees, enough of the code to know what it does today.

Facts are yours to find. Don't ask the user what the repository answers.

## 3. Play it back

One message:

- **Collisions first:** each earlier decision a point goes against (a SPEC.md rule, an entry's Decisions, a finished feature), named, and what replacing it would undo.
- **The points, one subject each,** grouped by the part of the product. For each:
  - what the user said, in a line;
  - what exists today, and the entry or rule that already covers it, in whole or in part;
  - where it would go (the table below);
  - your own view when you have one: a better way, a cost they didn't mention, or a recommendation not to do it, with the reason and what you'd do instead.

  Two points that are one problem are shown as one; a point that is a symptom of another says so.
- **The first round of questions** (step 4).

Judge each point by what the product is for (SPEC.md's Goal), not by what the user seems to want to hear. A point that isn't worth its cost is told so once, with the reason; the decision is theirs.

| The point is | It goes to |
|---|---|
| Behavior that's wrong today | a Bug entry, for `fix` |
| A change that keeps the behavior | a Debt entry, for `chore` |
| New or changed behavior, decided enough to build | an Idea |
| New behavior with decisions still open | an Idea with them as Open questions; when several connect, the offer of an `interview` session |
| Something an open entry already covers | a change to that entry |
| Something that makes an open entry pointless | that entry, discarded |
| About how the code is built, not what the product does | not here: `/minidev:checkup`, which the user types |
| Dropped in the conversation | nothing; the plan lists it with the reason |

## 4. Rounds

Load the `minidev:interview` skill and ask with its method: rounds of numbered questions, each with your recommended answer, only what can be decided now. Four things differ here:

- **Many roots.** Ask across all the points in the same round. A model or rule that several points depend on goes first.
- **A fact only the user has** (a number from outside the repository, how the team works) gets no recommended answer: say what it decides.
- **Points may stay open.** Stop a point when its next question needs something the user doesn't know yet (a trial, a design, someone else's answer): it's recorded as an open question. Stop the rounds when what's left wouldn't change which entries exist or what they wait for.
- **The plan is the confirmation.** `interview` ends by asking the user to confirm a shared understanding. Here the plan's approval (step 7) is that confirmation: don't ask for it apart.

Judge the answers too. When an answer can't hold against the data, a SPEC.md rule or another answer, say so before the plan, with the evidence.

## 5. The plan

Draft every entry in `document`'s format (`../document/references/backlog.md`, Entry format), then build the plan from the drafts:

- **New entries,** in the order they'll be created: name, type, its area (marked when the area is new), a line or two, its Decisions and Open questions, and what it Needs.
- **Entries that change:** what changes in each (a Decision replaced, scope moved to another entry, an Open question answered).
- **Entries discarded,** each with the reason and, for every entry that Needs it, whether that need is dropped or that entry is discarded too.
- **Dropped:** the points that led to no entry, each with the reason.
- **A doubt that still decides an entry's text,** with the answer you'll use if they approve without answering.

The plan shows each entry in short, so the full drafts add no decision the plan doesn't show: approving the plan approves them.

- **One entry is one thing** that can be built and verified on its own. Split a point that is several; join small ones on the same screen.
- **No two entries change the same thing.** When two touch the same screen or rule, say which owns what.
- **Needs only for a real order** (`../document/references/backlog.md`, Relations between entries).
- **An entry In progress isn't rewritten:** someone is building from its text. Put what the session decided in a new entry that Needs it, or recommend pausing it when what's being built is no longer wanted. The user decides.
- **A decision that replaces a SPEC.md rule** goes in the entry's Decisions, naming the rule. SPEC.md isn't touched: it describes what exists.

## 6. The check

Whoever led the conversation wrote every draft with the same picture in mind, so two drafts that can't both be built look fine to them. When the plan holds two or more writes (entries created, changed or discarded, counted together), have it checked before showing it. Say you're doing so, and start the `auditor` agent (agent type `minidev:auditor`; on Sonnet when the environment lets you choose a model) with this prompt, filled in and nothing added:

```
Area brief: a plan of backlog changes, not written yet

These entries were drafted in one conversation with the user and will be written to the backlog as they are. Read them against each other, the open backlog, SPEC.md and enough of the code to place each one. Look for:
- two drafts, or a draft and an open entry, that change the same screen, rule or data in ways that can't both be built;
- a draft that goes against a SPEC.md rule or Constraint, or what a finished feature does, without saying it replaces it;
- a draft whose premise isn't true in the code or in SPEC.md;
- a Needs with no real order behind it, and a real order with no Needs;
- a draft that rests on a decision another open entry still has as an open question;
- a draft that is more than one thing to build, or that can't be verified on its own;
- an open entry the plan leaves pointless or out of date without changing it.
Leave out problems in entries the plan doesn't touch, and whether the ideas are good: the user decided them.

Plan:
<each new entry's draft in full, each change to an existing entry, each discard>

Backlog: <"BACKLOG.md", or "GitHub issues: gh issue list --state open --limit 200 --json number,title,labels,body,blockedBy">
Code graph: <its path, when the project already has one (a `graphify-out/` folder, for example), or "none">
Numbers: none
Earlier check-ups: none
```

Don't pass the conversation or your own doubts: an auditor told what to find finds it. A plan that wasn't checked (a single write, or a session that can't start agents) says so.

## 7. Approve and record

Show the plan, then the auditor's report whole when the check ran, then what you'd change in the plan for each finding (recommended). Ask for the OK; the user may approve parts. A plan reshaped after the check (entries added, split or merged) is checked again, and what changed is shown with the new report for one more OK: the redrafted entries weren't seen yet. An answer or a cut needs neither.

On the OK, write it with the `document` skill: the new entries in the order of their Needs, so each can name the ones it waits for, then the changes, then the discards. The approved plan is the OK for these writes (`../document/SKILL.md`, Confirmation). Each entry written says where it came from in its Notes ("from the rethink of <date>").

End with what was written, what stayed open and in which entry, and the step you'd take first, with its skill. A fix or an interview the user accepted starts now, with its own skill.
