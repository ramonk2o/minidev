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

Look before asking. Use only commands that read (`git status`, `git branch`, `git log`, `ls`, and the read-only `gh` calls the resume rules use when `gh` is signed in). Don't repeat what other skills already detect: take their signals as they state them.

| What you find | Next step |
|---|---|
| The folder is empty, or holds only notes | Plan the project: `brainstorm` (say what you want to build, or `/minidev:brainstorm`) |
| It has code but isn't a git repository, or its CLAUDE.md doesn't say it uses the cycle (as `../build/SKILL.md`, 1. Start, checks it) | The user types `/minidev:setup` once per project. Without it the cycle's skills stop and offer it |
| It uses the cycle, with work started: a work branch, uncommitted changes, or a pull request, merged ones included (which branches and pull requests to read, and how to go on, are in `../build/references/git-flow.md`, Resume) | Say what's in progress and how to go on: "continue X", or "the pull request was merged, update" |
| It uses the cycle, nothing started, and the backlog has entries (`BACKLOG.md`, or the issues when its CLAUDE.md says `Backlog: GitHub issues`) | Propose the first entry, by its type (`../document/references/backlog.md`): an Idea is built ("let's build X"), a Bug is fixed, Debt is a chore. Several that don't touch the same files can run together with `/minidev:swarm`, which the user types |
| It uses the cycle and the backlog is empty | Ask what they want to do: note or think through an idea (`document`, `interview`), fix something broken (`fix`), clean up without changing behavior (`chore`), or publish a version (`document`) |

When the user said what they're stuck on, answer that first and then give the next step. When the state doesn't settle the next step, ask one short question instead of guessing.

## 2. Say it

In a few sentences: where the project stands, the one next step you recommend, and the exact words or command that take it. Mention another path only when it's a real alternative. Don't recite the cycle or list every skill.

`setup` and `swarm` run only when the user types their command, so give the command. For the others, offer to start the step and, on a yes, hand over to that skill without doing its work here. Then stop.

## 3. Terms

When a word from the cycle (pull request, branch, test-first, spec, backlog, changelog) needs explaining, give one plain sentence tied to what the user is doing right now, not a lesson. The details already live in `../build/references/git-flow.md` and `../document/references/` (`spec.md`, `backlog.md`, `changelog.md`): read the one that fits instead of restating it, and point the user to it only when they ask for more. For a question about programming in general, answer in a sentence and go back to the next step.
