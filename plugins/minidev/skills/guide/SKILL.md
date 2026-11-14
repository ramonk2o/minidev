---
name: guide
description: Tell someone who doesn't know the minidev development cycle where their project stands and what to do next, in plain words. It reads the folder, git, CLAUDE.md, the backlog, the current branch, uncommitted changes and open pull requests, names the next step and the skill or command for it, and explains a term of the cycle (pull request, branch, test-first, spec, backlog, changelog) in one sentence. It writes nothing and does no other skill's work. Run only when the user invokes it, optionally with what they're stuck on (e.g. "/minidev:guide", "/minidev:guide I don't know what to do next").
disable-model-invocation: true
argument-hint: "[what you're stuck on]"
---

# Guide

Orients someone who doesn't know the `minidev` cycle: where the project stands, what the next step is and who does it. It only looks and says; the work belongs to `brainstorm`, `setup`, `document`, `interview`, `build`, `fix`, `chore` and `swarm`, and this skill leaves it to them. It changes no file, branch or commit.

Talk to the user in the language of the conversation, in plain words. A term of the cycle gets one short sentence the first time it comes up (see 3).

## 1. Read the state

Look before asking. Use only commands that read (`git status`, `git branch`, `git log`, `ls`, `gh auth status`, and the read-only `gh` calls the resume rules use once it's signed in). Don't repeat what other skills already detect: take their signals as they state them.

| What you find | Next step |
|---|---|
| The folder is empty, or holds only notes | Plan the project: `brainstorm` (say what you want to build, or `/minidev:brainstorm`) |
| It has code but isn't a git repository, or its CLAUDE.md doesn't say it uses the cycle (as `../build/SKILL.md`, 1. Start, checks it) | The user types `/minidev:setup` once per project. Without it the cycle's skills stop and offer it |
| It uses the cycle, with work started: a work branch, uncommitted changes, or a pull request, merged ones included (which branches and pull requests to read, and how to go on, are in `../build/references/git-flow.md`, Resume) | Say what's in progress and how to go on: "continue X", or "the pull request was merged, update" (both are `build` requests, which hands over to the right skill) |
| It uses the cycle, nothing started, and the backlog has entries (`BACKLOG.md`, or the issues when its CLAUDE.md says `Backlog: GitHub issues`) | Propose the first entry, by its type (`../document/references/backlog.md`): an Idea is built ("let's build X"), a Bug is fixed, Debt is a chore. Several that don't touch the same files can run together with `/minidev:swarm`, which the user types |
| It uses the cycle and the backlog is empty | Ask what they want to do, and route the answer as below |

**`gh` missing or signed out.** When the project's backlog or pull requests live on GitHub (its CLAUDE.md says `Backlog: GitHub issues` or an integration with pull requests) and `gh` isn't installed or isn't signed in (`gh auth status`), don't treat the backlog as empty: say that you can't see GitHub yet. Tell the user to install `gh` from cli.github.com, sign in by typing `gh auth login` in a terminal and following its questions (a GitHub account is needed), and then call `/minidev:guide` again. Read the rest of the state as usual, and meanwhile ask them to describe what's in the backlog so you can still suggest a step. You don't install or sign in for them.

**What the user wants.** When the user says what they want or what they're stuck on, whatever the backlog holds, answer that first, after checking that no backlog entry already is it (if one is, propose building that entry), and route it: a new idea goes to `document` when it's clear and to `interview` first when it leaves behavior open (then `build`), something broken to `fix`, a cleanup that changes no behavior to `chore`, a version to publish to `document`. Then give the next step. When the state doesn't settle the next step, ask one short question instead of guessing.

## 2. Say it

Short, at most five or six sentences: one sentence on where the project stands, the one next step you recommend, and the exact words or command that take it. Mention another path only when it's a real alternative.

Keep out what the user didn't ask for and the next skill will say when it starts: the names of files and tools (say "the project isn't set up yet", not that its CLAUDE.md lacks a line or that it's a git repository), the project's files and what's in them, a backlog entry's details, and how the next step works inside (its tests, reviews, branches). Don't recite the cycle or list every skill. Use the cycle's words (repository, branch, backlog, spec, pull request) only when the step needs them, each with a few words of explanation the first time; otherwise say it in everyday words. The first time, call the cycle "minidev's way of working" and say what it is in one short sentence (a fixed order of steps for planning, building and checking), without listing the steps, instead of "the cycle".

`setup` and `swarm` run only when the user types their command, so give the command. For the others, offer to start the step and, on a yes, hand over to that skill without doing its work here. Then stop.

## 3. Terms

When a word from the cycle (pull request, branch, test-first, spec, backlog, changelog) needs explaining, give one plain sentence tied to what the user is doing right now, not a lesson. The details already live in `../build/references/git-flow.md` and `../document/references/` (`spec.md`, `backlog.md`, `changelog.md`): read the one that fits instead of restating it, and point the user to it only when they ask for more. For a question about programming in general, answer in a sentence and go back to the next step.
