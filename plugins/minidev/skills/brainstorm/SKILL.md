---
name: brainstorm
description: Start a new software project from an idea, before any code exists. Interviews the user about the product and its first version, decides the architecture and stack with them, picks where to start, then scaffolds a project whose tests and build already run and records the plan in BACKLOG.md and SPEC.md, ready for the minidev cycle. Use it when the user wants to start, plan or kick off a new project or app, think through its architecture or decide where to begin, in any language (e.g. "I want to build an app that…", "quero começar um projeto novo", "how should I structure this new project?"). Not for adding a feature to an existing project: that's document (with grilling when the idea is open), then build.
---

# Brainstorm

Takes a project from an idea to an empty but working codebase: the product is understood, the technical decisions are made with their reasons, the first features are lined up in the order to build them, and the skeleton runs its tests and build. From there, the `minidev` cycle takes over: `setup` writes the CLAUDE.md and permissions, and `build` builds the first feature.

The order matters. The product comes before the stack, because the stack is chosen to serve the product (where it runs, what it stores, who uses it), not the other way around. The stack comes before the scaffold, because changing a decision costs a sentence now and a rewrite later.

Talk to the user in the language of the conversation. Write code, config and commit messages in English; the product documents follow the `document` skill's language rule.

Nothing is created before the user's OK on the plan (step 5).

## 1. Check the folder

This skill is for a project that doesn't exist yet. Look at the working folder:

- **Empty, or only notes** (a README, a sketch, a `.git` with no code): go on. Read any notes first; what they already decide isn't asked again.
- **Already has code:** this isn't a new project. Say so and point to `/minidev:setup` to adopt the cycle, and to `grilling` to think through a change. Stop.
- **The user is in an unrelated folder** (their home, another project): ask where the new project should live, and work there.

## 2. Product

Load the `grilling` skill and interview with its method: rounds of numbered questions, each with your recommended answer, asking only what can be decided now. The design tree for a new product usually covers:

- **Problem and people:** what's painful today, for whom, and how they cope without the product.
- **First version:** the smallest thing that's already useful to someone. Push for small: everything else is a later idea, not part of the start.
- **Out of scope:** what the first version deliberately doesn't do.
- **Surfaces:** where users meet the product (web app, mobile, CLI, browser extension, library, API, a bot…).
- **Data:** what it stores, where it must live (the user's device, a server, a third party), and what happens if it's lost.
- **Integrations:** other systems it reads from or writes to, and accounts or keys they need.
- **Constraints:** platforms, offline use, number of users, cost, hosting, privacy, deadlines.
- **The user's experience:** languages and tools they know well. A stack they can debug alone usually beats a better one they can't.

Skip branches the idea makes obvious (a CLI for personal use doesn't need a hosting question). Look facts up yourself instead of asking: what an API allows, what a platform requires, whether a library exists.

## 3. Architecture and stack

With the product settled, decide the technical shape, still in rounds with a recommendation each. Cover only what the first version needs:

- **Language and framework**, and how the project is created (the framework's official generator when there is one).
- **Architecture:** the few parts the product splits into and how they talk (e.g. "a static frontend and a small API", "a single CLI with a core module the commands call"), and where each rule from step 2 lives.
- **Storage:** database, files or local storage, matching the data answers.
- **Tests:** framework and how the product's rules will be tested without the real environment (fakes, a test database, an in-memory store). The cycle writes tests first, so this has to work from day one.
- **Run, build and distribution:** how it runs locally, how it's built, and where it will be deployed or published (only if the first version needs it).

Rules for the recommendations:

- **Boring and few.** Prefer mature, well-documented tools and the fewest dependencies that do the job. Every dependency is something to update and learn.
- **Facts are current.** Check versions, official generators and recommended setups in current docs before proposing them; don't rely on memory for what changes.
- **Show options only where the choice is really open.** Then give two or three, compared in a line each (what it's good at, what it costs), and recommend one. Where one option is clearly right, just recommend it with its reason.
- **Say what would change the decision** when it's close (e.g. "if you'll need more than one user later, start with the server database instead").

## 4. Where to start

Split the first version into features, each one something a user can see working, and put them in the order to build them:

1. **First feature: the thinnest path through the whole product.** One real use, end to end, crossing every part from step 3 (e.g. "create a note and see it in the list after reloading"). It proves the architecture early, while changing it is still cheap.
2. **Then by dependency and value:** what others need comes first; among the rest, what makes the product useful sooner.

For each feature, keep what step 2 and 3 decided about it: the rules become its Decisions, what's undecided its Open questions. Later ideas that came up go to the backlog too, after the first version's features.

## 5. Review the plan

Show everything in one message:

- **Product:** the problem, the people and the first version in a few sentences, plus what's out of scope.
- **Technical decisions**, each with its reason.
- **Scaffold:** what will be created (generator command, folders, test setup, a first smoke test) and the commands that will be run.
- **Features in order**, with one line each, and the later ideas.

Wait for the user's OK; they may change any part. This is the summary that ends the interview, so its approval is also the OK for the backlog entries in step 7.

## 6. Scaffold

Create the skeleton the plan approved. It has no product behavior yet: the first feature goes through `build`, test-first, like every other.

1. `git init` if the folder isn't a repository, with a short `.gitignore` for the stack (dependencies, build output, test reports, `.env`, OS files like `.DS_Store`, `.claude/settings.local.json`).
2. Generate the project with the framework's official generator when there is one, non-interactively, with the options decided in step 3. Remove the generator's demo content (sample pages, counters, logos) that isn't part of the product.
3. Lay out the parts from step 3 as folders or modules, empty or with a minimal entry point. Don't write code for features that aren't built yet.
4. Set up the test framework with one smoke test that passes (e.g. the app module loads, the CLI prints its help), and the shared fake or test store the rules will need, if step 3 decided one.
5. Run install, tests and build, and show that they pass. If something fails, fix the setup before going on: the cycle can't start on a skeleton that doesn't run.
6. A short `README.md`: what the project is, in one sentence, and how to install, run and test it.

## 7. Documents

Load the `document` skill and create the product documents with it; their formats belong to that skill.

- **BACKLOG.md:** the features from step 4 as Ideas, in the order to build them, and the later ideas after them. Each entry's Motivation comes from step 2, and its Constraints from the constraints of step 2 that apply only to that feature.
- **SPEC.md:** only what exists now: the Goal, the Constraints of the whole product from step 2 (platforms, offline use, privacy…), which aren't repeated in each entry, and the Technical decisions the scaffold put in place, with their reasons (naming the constraints that drove them, e.g. "SQLite in the browser: it must work offline"). No Behavior yet: the rules join the spec as each feature is built.

## 8. Finish

1. Offer the first commit with the scaffold and the documents. Don't commit without the OK.
2. Tell the user the next steps: run `/minidev:setup` to write the CLAUDE.md and permissions for the cycle, then build the first feature by name (e.g. "let's build <first feature>").
